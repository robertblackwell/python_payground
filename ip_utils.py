import pprint
import ipaddress

#
# get subnets recursive - stops when prefix length gets to stopping_prefix_length
# net_ip IPv/4/6Network
# stopping_prefix_length integer
#
def get_subnets(snet_ip, stopping_prefix_length=30):
    subnets = []
    if snet_ip.prefixlen == stopping_prefix_length:
        return subnets
    for sn in snet_ip.subnets():
        subnets = subnets + [sn] + get_subnets(sn)
    return subnets


#
#  tests if this host_ip is in the network of the net_ip
# host_ip IPv/4/6Address
# net_ip IPv/4/6Network
#
def is_ip_in_network(host_ip, net_ip):
    net_addrs = []
    ip = ipaddress.ip_address(host_ip)
    for addr in net_ip:
        if ip == addr:
            net_addrs.append(net_ip)
            break
            # print("found {} {}".format(host_ip, net_ip))
    return net_addrs


#
# host_ip a IPv4/6Address representing an ip address of a host
# net_ip a network ip address as ipaddress.ip_network
#
def is_in_net(host_ip, net_ip):
    net_addrs = []
    ip = host_ip
    for addr in net_ip:
        if ip == addr:
            net_addrs.append(net_ip)
            break
            # print("found {} {}".format(host_ip, net_ip))
    return net_addrs


#
# filters a list of subnets to return only those
# that contain the given host_ip
# @param list(ipaddress.ip_network)  subnets
# @param integer stopping_prefix_length
# @param IPv4/6Address host_ip
# 
def filter_subnets(subnets, host_ip):
    result_subnets = []
    for sn in subnets:
        if is_in_net(host_ip, sn):
            result_subnets.append(sn)
    return result_subnets


#
# @param string starting_net
# @param integer stopping_prefix_length
# @param string host_ip
# 
def find_all_subnets_containing_host(starting_net, stopping_prefix_length, host_ip):
    starting_sn = ipaddress.ip_network(starting_net)
    h_ip = ipaddress.ip_address(host_ip)
    if is_in_net(starting_sn, h_ip):
        subnets = [starting_sn];
    subnets += get_subnets(starting_sn, stopping_prefix_length)
    result = filter_subnets(subnets, h_ip);
    return result


#
# returns an array of valid network addresses
# that this ip could belong to.
# 
# This is a very naive algorithm - it simply generates all
# candidate network ip by replacing the last octet with 0/n
# probably with is not a wide enough search
# 
def find_network_addresses(ip):
    net_addrs = []
    parts = ip.split('.')
    for i in range(64):
        p = '0/{}'.format(i)
        parts[3] = p
        s = ".".join(parts)
        try:
            tmp = ipaddress.ip_network(s)
            net_addrs = net_addrs + is_ip_in_network(ip, tmp)
            # print("{} is a valid network address".format(s))
        except:
            pass
            # print("{} is not a valid network address".format(s))
    # print('done')
    return net_addrs


# validate and update the ipaddress_object in a
# MacAddressMapping instance parameter 
# return the ipaddress.ip_address instance if valid
# return None is invalid
def is_valid_ipaddress(mac_mapping):
    try:
        tmp = ipaddress.ip_address('192.168.0.2')
        tmp = ipaddress.ip_address('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        tmp = ipaddress.ip_address(mac_mapping.ip_address)
        mac_mapping.ipaddress_object = tmp
        tmp2 = ipaddress.ip_network('50.193.103.0/25')
        return tmp
    except:
        return None


if __name__ == "__main__":
    # 
    # in here can do all kings of processing on the data
    # 
    host_ip = '192.168.3.27'
    net_ip = '192.168.0.0/20'
    a = get_subnets(ipaddress.ip_network(net_ip))
    b = find_all_subnets_containing_host(net_ip, 31, host_ip)
    print("here are the subnets of {} that {} could belong to".format(net_ip, host_ip))
    pprint.pprint(b)
