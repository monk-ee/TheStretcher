TheStretcher
============

EBS Volume Stretcher for EC2 Instances

Works for windows and Linux, but you will need to format it/extend it

Params:

+ instance id: a valid instance id
+ device mount point: as per the console or reported by BlockDeviceMapping
+ new disk size: in gigabytes

Syntax:

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