import csv
import pprint
import sys
import ipaddress
import ip_utils
    
# maps a macaddress to an ip address
class MacAddressMapping:
    # name
    # mac_addrress
    # ip_address
    def __init__(self, a_name, a_mac, an_ip):
        self.name = a_name
        self.mac_address = a_mac
        self.ip_address = an_ip.strip()
        self.ipaddress_object = None
        # 
        # a list of valid network addresses that this ip could belong to
        # 
        self.net_addrs = []


class DeviceMacMappings:
    # name
    # mac_mappings an array/list of MacAddressMappings
    # 
    def __init__(self, a_name, a_mac_addr_mapping):
        self.name = a_name
        self.mac_mappings = [a_mac_addr_mapping]

    def add_mapping(self, a_mac_addr_mapping):
        self.mac_mappings.append(a_mac_addr_mapping)


class Mappings:
    # 
    # mappins an array or list of DeviceMacMappings
    # 
    def __init__(self):
        self.mappings = {}

    def has_device(self, name):
        if name in self.mappings:
            return True
        else:
            return False

    def get_device(self, name):
        if name in self.mappings:
            return self.mappings[name]
        else:
            return None

    def add_device(self, device):
        if device.name in self.mappings:
            raise "device named {} already in mappings".format(device.name)
        self.mappings[device.name] = device

# if len(sys.argv) != 2:
#     print("requires exactly one argument - name of csv file")
#     sys.exit
# filename = sys.argv[1]    
    filename = "tmp_csv.csv"

# creates a Mappings instance from an input file
def build_mappings(filename):
    all_mappings = Mappings()
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            current_dev_name = row[0]
            new_mac_mapping = MacAddressMapping(row[0], row[2], row[1])
            device = all_mappings.get_device(current_dev_name)
            if device is None:
                device = DeviceMacMappings(row[0], new_mac_mapping)
                all_mappings.add_device(device)
            else:
                device.add_mapping(new_mac_mapping)

    return all_mappings

def write_mappings(table, file_ext):
    previous_device_name = "" 
    outfile = None
    for dev_name in table.mappings:
        device = table.mappings[dev_name]
        outfile = open(device.name + "." + file_ext, "w")
        for map in device.mac_mappings:
            outfile.write("Device Name: {} MacAddr: {} ip_address {}\n"
                .format(map.name, map.mac_address, map.ip_address))
        outfile.close()

def calculate_possible_network_addresses(table):

    previous_device_name = "" 
    outfile = None
    for dev_name in table.mappings:
        device = table.mappings[dev_name]
        for map in device.mac_mappings:
            ip = ip_utils.is_valid_ipaddress(map)
            net_addrs = ip_utils.find_network_addresses(map.ip_address)
            map.net_addrs = net_addrs
            if ip is None:
                print("device {} mac address: {} has invalid ip addrerss {}"
                    .format(device.name, device.mac_address, device.ip_address))


def main():
    table = build_mappings("./tmp_csv.csv")
    # 
    # in here can do all kings of processing on the data
    # 
    a = ip_utils.get_subnets(ipaddress.ip_network('192.168.0.0/20'))
    b = ip_utils.find_all_subnets_containing_host('192.168.0.0/20', 31, '192.168.3.27')

    calculate_possible_network_addresses(table)
    # 
    # in here can do all kings of processing on the data
    # 
    write_mappings(table, "something")
    print("table done")


main()