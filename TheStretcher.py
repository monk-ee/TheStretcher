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

    def __init__(self,ec2_instance_id,disk_partition,disk_size):
        self.load_configuration()
        self.set_timezone()
        self.ec2_connect()
        self.sns_connect()

        self.sns_message()

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
            self.snsconn = boto.sns.connect_to_region(self.config['general']['region'])
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

    def stop_instance(self, instance):
        if instance.state == "running":
            self.sns_stop.append(instance.id)
            instance.stop()

    def start_instance(self, instance):
        if instance.state == "stopped":
            self.sns_start.append(instance.id)
            instance.start()

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


if __name__ == "__main__":
    ts = TheStretcher()


