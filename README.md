TheStretcher
============

EBS Volume Stretcher for EC2 Instances

Works for windows and Linux, but you will need to format it/extend it


Syntax
========

    usage: TheStretcher.py [-h] [-r] [-c] [-i IOPS]
                       instance disk_partition disk_size

    A utility for stretching ec2 volumes with minimal effort.

    positional arguments:
        instance              An EC2 instance ID
        disk_partition        The mount point eg. /dev/sdb
        disk_size             The new disk size in GB.

    optional arguments:
        -h, --help            show this help message and exit
        -r, --restart         Stop and restart the instance.
        -c, --cleanup         Delete all snapshots and volumes on completion.
        -i IOPS, --iops IOPS  Add provisioned IOPS to the new volume.

Configuration
==========
Requires: your boto config file (~/.boto) to contain your aws credentials

    [Credentials]
    aws_access_key_id = <your access key>
    aws_secret_access_key = <your secret key>

 + You may need to change your region and timezone.


Proxy
==========
You may need to add proxy information to your .boto file

    [Boto]
    debug = 0
    num_retries = 10

    proxy = myproxy.com
    proxy_port = 8080


SNS Topic
==========
You can configure an AWS SNS Topic, then you can publish to email or whatever.
Add your Topic ARN to the config.yml and I am assuming you have setup the SNS Stuff.


Dependencies
==========
 + PyYAML==3.10
 + boto==2.27.0
 + argparse==1.2.1


Author
==========
Contact me on twitter @monkee_magic
