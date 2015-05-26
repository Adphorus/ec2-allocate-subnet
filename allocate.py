#!/usr/bin/python -u

import sys
from collections import Counter

import boto.ec2


def get_limit(ec2, domain):
    limit = 0
    temp_ips = []
    try:
        while True:
            temp_ips.append(ec2.allocate_address(domain))
            limit += 1 
    except:
        if not limit:
            print("Unable to allocate any IP addresses. Check your IAM credentials.")
    finally:
        for ip in temp_ips:
            ip.release()
        return limit


def allocate(ec2, domain, number, tolerance):
    eips = []
    subnets = Counter()
    for x in range(number + tolerance):
        if is_vpc:
            ip = ec2.allocate_address(domain)
            eips.append(ip)
            subnets[ip.public_ip.split(".")[2]] += 1

    retry = False

    if subnets.most_common(1)[0][1] < number:
        retry = True
        for ip in eips:
            ip.release()

    return retry, subnets.most_common(1)[0][1]


if __name__ == "__main__":
    
    try:
        region = sys.argv[1]
        number = int(sys.argv[2])
        is_vpc = bool(sys.argv[3])
    except:
        print("Usage: ./allocate.py <region> <ip_count> <is_vpc>")
        print("Example: ./allocate.py us-east-1 5 True")
        sys.exit()

    try:
        ec2 = boto.ec2.connect_to_region(region)
    except:
        print("Unable to connect. Check your AWS credentials.")
        sys.exit()

    domain = "vpc" if is_vpc else None
    limit = get_limit(ec2, domain)

    if not limit:
        sys.exit()
    if number > limit:
        print("AWS IP Limit not enough. Can only allocate %s more IP addresses" % limit)
        sys.exit()

    tolerance = limit - number

    retry = True
    while retry:
        retry, succesful_amount = allocate(ec2, domain, number, tolerance)
        print("."),
    else:
        print("Allocated %s IP addresses" % succesful_amount)
