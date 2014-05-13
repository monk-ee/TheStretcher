#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""TheStretcher.py: A utility for stretching ec2 volumes with minimal effort."""

# Requires: your boto config file (~/.boto) to contain your aws credentials
#
# [Credentials]
# aws_access_key_id = <your access key>
# aws_secret_access_key = <your secret key>

__project__ = 'TheStretcher'
__author__ = "monkee"
__license__ = "GPL"
__version__ = "0.9.0"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"

import boto.ec2, boto.sns
import yaml, sys,logging,time,os


class TheStretcher:
    """
    Stretches an ebs volume attached to an instance and cleans up after itself

    :param ec2_instance_id: a valid ec2 instance id
    :param disk_partition: a disk partition to stretch
    :param disk_size: a new disk size

    """
    conn = ""
    config = ""
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    sns_stop = list()
    sns_start = list()
    ec2_instance_id = ""
    disk_partition = ""
    disk_size = ""
    old_ebs = ""
    new_ebs = ""
    snapshot = ""
    instance = ""

    def __init__(self,argv):
        try:
            self.ec2_instance_id = argv[1]
            self.disk_partition = argv[2]
            self.disk_size = argv[3]
        except BaseException as emsg:
            sys.exit("Missing arguments" + str(emsg))

        self.load_configuration()
        self.set_timezone()
        self.ec2_connect()
        self.sns_connect()
        self.get_instance()
        self.stop_instance()
        self.get_attached_volumes()
        self.snapshot_ebs_volume()
        self.check_snapshot_availability()
        self.create_volume_from_snapshot()
        self.check_volume_availability()
        self.detach_old_volume()
        self.attach_volume_to_instance()
        self.delete_snapshot()
        self.delete_old_volume()
        self.start_instance()
        #self.sns_message()

    def load_configuration(self):
        try:
            config_str = open(os.path.dirname(__file__) + '/config.yml', 'r')
            self.config = yaml.load(config_str)
            logfile = os.path.dirname(__file__) + "/" + self.config['general']['logfile']
            logging.basicConfig(filename=logfile, level=logging.INFO)
        except IOError as error:
            exit("Could not load config.yml: " + str(error))
        except:
            raise
            exit("Unexpected error:" + str(sys.exc_info()[0]))

    def set_timezone(self):
        try:
            os.environ["TZ"]=self.config['general']['time_zone']
            time.tzset()
            self.time = time.time()
        except Exception as error:
            exit("Could not set time related stuff- very bad")

    def ec2_connect(self):
        try:
            self.conn = boto.ec2.connect_to_region(self.config['general']['region'])
        except:
            #done again
            exit("Failed to connect to EC2")

    def sns_connect(self):
        try:
            self.snsconn = boto.sns.connect_to_region(self.config['general']['region'])
        except (BaseException) as emsg:
            #done again
            logging.warning(self.timestamp + ': No SNS configured correctly - carry on - ' + str(emsg))
            #no sns configured or some issue
            pass

    def get_instance(self):
        reservations = self.conn.get_all_instances(filters={'instance-id' : self.ec2_instance_id})
        self.instance = reservations[0].instances[0]

    def stop_instance(self):
        if self.instance.state == "running":
            self.sns_stop.append(self.ec2_instance_id)
            self.instance.stop()

    def start_instance(self):
        if self.instance.state == "stopped":
            self.sns_start.append(self.ec2_instance_id)
            self.instance.start()

    def sns_message(self):
        message = ""

        for item in self.sns_start:
            message += "Started Instance:" + item + "\n"
        for item in self.sns_stop:
            message += "Stopped Instance:" + item + "\n"

        if message != "":
            try:
                self.snsconn.publish(self.config['general']['sns_topic'], message, "TheSleeper was invoked")
            except:
                pass

    def create_volume_from_snapshot(self):
         self.new_ebs = self.conn.create_volume(self.disk_size, self.config['general']['zone'], self.snapshot)

    def check_volume_availability(self):
        curr_vol = self.conn.get_all_volumes([self.new_ebs.id])[0]
        while curr_vol.status != 'available':
            time.sleep(10)
            curr_vol = self.conn.get_all_volumes([self.new_ebs.id])[0]

    def attach_volume_to_instance(self):
        self.conn.attach_volume (self.new_ebs.id, self.ec2_instance_id, self.disk_partition)

    def snapshot_ebs_volume(self):
        self.snapshot = self.conn.create_snapshot(self.old_ebs.id, 'TheStretcher Volume Snapshot')

    def delete_snapshot(self):
        self.conn.delete_snapshot(self.snapshot.id)

    def delete_old_volume(self):
        self.conn.delete_volume(self.old_ebs.id)

    def check_snapshot_availability(self):
        curr_snapshot = self.conn.get_all_snapshots([self.snapshot.id])[0]
        print(curr_snapshot.status)
        while curr_snapshot.status != 'completed':
            time.sleep(10)
            curr_snapshot = self.conn.get_all_snapshots([self.snapshot.id])[0]

    def detach_old_volume(self):
        self.conn.detach_volume(self.old_ebs.id,self.ec2_instance_id,self.disk_partition)

    def get_attached_volumes(self):
        filters = {'attachment.instance-id': self.ec2_instance_id}
        vols = self.conn.get_all_volumes(filters=filters)
        for vol in vols:
            print(vol.attach_data.device)
            if vol.attach_data.device == self.disk_partition:
                self.old_ebs = vol
                return
        exit("No volumes found matching that mount point.")

if __name__ == "__main__":
    ts = TheStretcher(sys.argv)


