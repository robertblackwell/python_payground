import csv
import pprint
import sys

# maps a macaddress to an ip address
class MacAddressMapping:
    name = ""
    mac_address =""
    ip_address =""

class DeviceMacMappings:
    name = ""

    # each entry in the mapping array will be an
    # instance of MacAddressMaping
    mac_mappings = []


class Mappings:
    mappings = {}

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
        if device.name in mappings:
            raise "device named {} already in mappings".format(device.name)
        mappings[device.name] = device

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
            mapping = MacAddressMapping()
            mapping.name = current_dev_name
            mapping.mac_address = row[1]
            mapping.ip_address = row[2]

            device = all_mappings.get_device(current_dev_name)
            if device is None:
                device = DeviceMacMappings()
                device.name = current_dev_name
                device.mac_mappings = [mapping]
                all_mappings.mappings[current_dev_name] = device
            else:
                device.mac_mappings.append(mapping)
    return all_mappings

def write_mappings(table, file_ext):
    previous_device_name = "" 
    outfile = None
    for dev_name in table.mappings:
        print(dev_name)
        device = table.mappings[dev_name]
        outfile = open(device.name + "." + file_ext, "w")
        for map in device.mac_mappings:
            outfile.write("Device Name: {} MacAddr: {} ip_address {}\n"
                .format(map.name, map.mac_address, map.ip_address))
        outfile.close()

def main():
    table = build_mappings("./tmp_csv.csv")
    # 
    # in here can do all kings of processing on the data
    # 
    write_mappings(table, "something")
    print("table done")


main()