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
import yaml, sys,logging,time,os,re
import argparse


class TheStretcher(object):
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

    def __init__(self, arg):
        try:
            self.ec2_instance_id = arg.instance
            self.disk_partition = arg.disk_partition
            self.disk_size = arg.disk_size
            self.restart = arg.restart
            self.cleanup = arg.cleanup
            self.iops = arg.iops
            self.dryrun =arg.dryrun
        except BaseException as emsg:
            sys.exit("Missing arguments" + str(emsg))

        self.check_arguments()
        self.load_configuration()
        self.set_timezone()
        if not self.dryrun:
            self.ec2_connect()
            self.sns_connect()
            self.get_instance()
            self.stop_instance()
            self.get_attached_volumes()
            self.snapshot_ebs_volume()
            self.check_snapshot_availability()
            self.create_new_volume_from_snapshot()
            self.check_new_volume_availability()
            self.detach_old_volume()
            self.check_detached_old_volume()
            self.attach_new_volume_to_instance()
            if self.cleanup:
                self.delete_snapshot()
                self.delete_old_volume()
            if self.restart:
                self.start_instance()
            self.sns_message()

    def load_configuration(self):
        try:
            config_str = open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml', 'r')
            self.config = yaml.load(config_str)
            logfile = os.path.dirname(os.path.abspath(__file__)) + "/" + self.config['general']['logfile']
            logging.basicConfig(filename=logfile, level=logging.INFO)
        except IOError as error:
            exit("Could not load config.yml: " + str(error))
        except:
            raise
            exit("Unexpected error:" + str(sys.exc_info()[0]))

    def check_arguments(self):
        match_instance_id = re.match('^(i\-[A-Fa-f0-9]*)$', self.ec2_instance_id)
        if not match_instance_id:
            exit("Instance Id needs to be in the i-xxxxxx format.")

        if self.disk_partition == "":
            exit("Disk partition required eg. /dev/sda1,/dev/sdb,xvdf")

        try:
            if (int(self.disk_size)%1 != 0):
                exit("Disk size needs to be a whole number (in GB).")
        except:
             exit("Disk size needs to be an integer (in GB).")

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
        for item in self.sns_stop:
            message += "Stopped Instance:" + item + "\n"

        message += "Stretched " + self.disk_partition + " to " + self.disk_size + "GB \n"

        for item in self.sns_start:
            message += "Started Instance:" + item + "\n"

        if message != "":
            try:
                self.snsconn.publish(self.config['general']['sns_topic'], message, "TheStretcher was invoked")
            except:
                pass

    def create_new_volume_from_snapshot(self):
        if self.iops is None:
            self.new_ebs = self.conn.create_volume(self.disk_size, self.config['general']['zone'], self.snapshot,dry_run=self.dryrun)
        else:
            self.new_ebs = self.conn.create_volume(self.disk_size, self.config['general']['zone'], self.snapshot, 'io1', self.iops,dry_run=self.dryrun)

    def check_new_volume_availability(self):
        curr_vol = self.conn.get_all_volumes([self.new_ebs.id])[0]
        while curr_vol.status != 'available':
            time.sleep(10)
            curr_vol = self.conn.get_all_volumes([self.new_ebs.id])[0]

    def attach_new_volume_to_instance(self):
        self.conn.attach_volume(self.new_ebs.id, self.ec2_instance_id, self.disk_partition,dry_run=self.dryrun)

    def snapshot_ebs_volume(self):
        self.snapshot = self.conn.create_snapshot(self.old_ebs.id, 'TheStretcher Volume Snapshot',dry_run=self.dryrun)

    def delete_snapshot(self):
        self.conn.delete_snapshot(self.snapshot.id,dry_run=self.dryrun)

    def delete_old_volume(self):
        self.conn.delete_volume(self.old_ebs.id,dry_run=self.dryrun)

    def check_snapshot_availability(self):
        curr_snapshot = self.conn.get_all_snapshots([self.snapshot.id])[0]
        while curr_snapshot.status != 'completed':
            time.sleep(10)
            curr_snapshot = self.conn.get_all_snapshots([self.snapshot.id])[0]

    def detach_old_volume(self):
        self.conn.detach_volume(self.old_ebs.id, self.ec2_instance_id, self.disk_partition,dry_run=self.dryrun)

    def get_attached_volumes(self):
        filters = {'attachment.instance-id': self.ec2_instance_id}
        vols = self.conn.get_all_volumes(filters=filters)
        for vol in vols:
            if vol.attach_data.device == self.disk_partition:
                self.old_ebs = vol
                return
        exit("No volumes found matching that mount point.")

    def check_detached_old_volume(self):
        #it seems you have to wait just a little for the dang thing to detach
        time.sleep(15)

if __name__ == "__main__":
    #grab the arguments when the script is ran
    parser = argparse.ArgumentParser(description='A utility for stretching ec2 volumes with minimal effort.')
    parser.add_argument('-r', '--restart', action='store_true', default=False, help='Stop and restart the instance.')
    parser.add_argument('-c', '--cleanup', action='store_true', default=False, help='Delete all snapshots and volumes on completion.')
    parser.add_argument('-d', '--dryrun', action='store_true', default=False, help='Fake runs for testing purposes.')
    parser.add_argument('-i', '--iops', type=int, help='Add provisioned IOPS to the new volume.')
    parser.add_argument('instance', help='An EC2 instance ID')
    parser.add_argument('disk_partition', help='The mount point eg. /dev/sdb')
    parser.add_argument('disk_size', help='The new disk size in GB.')
    args = parser.parse_args()
    ts = TheStretcher(args)


