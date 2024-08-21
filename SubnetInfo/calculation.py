import ipaddress
def get_ip_network(ip_address):
    try:
        if "/" in ip_address:
            return ipaddress.ip_network(ip_address, strict=False)
        else:
            raise ValueError("Invalid IP address format")
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip_address}")
########################
# 1. Finding the No.of hosts
#  	input: ipv4 address
#     output: Network, Broadcast, available hosts
#           First, last address
def find_hosts(ip_address):
    ip=get_ip_network(ip_address)
    network = ip.network_address
    broadcast = ip.broadcast_address
    num_hosts = ip.num_addresses - 2
    first_address = network + 1
    last_address = broadcast - 1
    host_info = {}
    host_info["Network "] =str(network)
    host_info["Broadcast "] = str(broadcast)
    host_info["No of hosts "] = num_hosts
    host_info["First address "] = str(first_address)
    host_info["Last address "] = str(last_address)
    return host_info
#####################################################
####################################################
# 2. Subdivide a network based on
#    a: no of host required: 2^n-2
#       inputs: network, no of hosts
#    b: no of subnets required: 2^n
#       inputs: network, no of hosts
def subnet_by_hosts(network, required_hosts):
    ip_network = get_ip_network(network)
    available_hosts = ip_network.num_addresses
    if required_hosts + 2 > available_hosts:
        raise ValueError("Not enough available addresses in the network for the requested number of hosts")

    required_prefix_length = 0
    while 2 ** required_prefix_length < required_hosts + 2:
        required_prefix_length += 1
    subnets = [str(subnet) for subnet in ip_network.subnets(new_prefix=ip_network.prefixlen + required_prefix_length)]
    return subnets
####################################################
def subnet_by_subnets(network,required_subnets):
    ip=get_ip_network(network)
    available_subnets = 2 ** (32 - ip.prefixlen)
    if required_subnets > available_subnets:
        raise ValueError("Not enough available subnets in the network for the requested number of subnets")
    required_prefix_length=0
    while 2**required_prefix_length < required_subnets:
        required_prefix_length+=1
    subnets=[str(subnet) for subnet in ip.subnets(new_prefix=ip.prefixlen+required_prefix_length)]
    return subnets
