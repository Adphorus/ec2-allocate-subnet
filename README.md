# ec2-allocate-subnet
Tries to allocate given number of ip addresses on the same subnet. We were able to generate 8 addresses on the same subnet within an hour of runtime.

####Usage: 

  `$ python allocate.py <region> <ip_count> <is_vpc>`
####Example:

  `$ ./allocate.py us-east-1 5 True`
  
####Requirements:
  `boto`

You need to have your IAM credentials configured on your environment. See [here](https://boto.readthedocs.org/en/latest/getting_started.html#configuring-boto-credentials).



