TheStretcher
============

EBS Volume Stretcher for EC2 Instances

Works for windows and Linux, but you will need to format it/extend it

Params:

+ instance id: a valid instance id
+ device mount point: as per the console or reported by BlockDeviceMapping
+ new disk size: in gigabytes

Syntax:
    ./TheStretcher.py i-6a51ba54 /dev/sdc 100
