import csv
import pprint
import sys
import ipaddress
import ip_utils


# maps a macaddress to an ip address and holds the name
# of the device for which this mapping pertains
class MacToIp:
    def __init__(self, a_name, a_mac, an_ip):
        self.name = a_name
        self.mac_address = a_mac
        self.ip_address = an_ip.strip()

# a device name al a list of mac-ip mappings for that device
class Device:
    def __init__(self, name, mac_to_ip):
        self.name = name
        self.mac_to_ips = [mac_to_ip]

    def add(self, mac_to_ip):
        if self.name != mac_to_ip.name:
            raise ("trying to add map with name {} to device with name {}".format(mac_to_ip.name, self.name))
        self.mac_to_ips.append(mac_to_ip)

# a list of devices indexed by device name
class Devices:
    def __init__(self):
        self.devices = {}

    def has_device(self, name):
        if name in self.devices:
            return True
        else:
            return False

    def get_device(self, name):
        if name in self.devices:
            return self.devices[name]
        else:
            return None

    def add_device(self, device):
        if device.name in self.devices:
            raise "device named {} already in mappings".format(device.name)
        self.devices[device.name] = device


# creates a Devices instance from an input file
def read_devices(filename):
    devs = Devices()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            current_dev_name = row[0]
            m_to_ip = MacToIp(row[0], row[2], row[1])
            device = devs.get_device(current_dev_name)
            if device is None:
                device = Device(row[0], m_to_ip)
                devs.add_device(device)
            else:
                device.add(m_to_ip)

    return devs

# for each device in devs: Devices print a file of mac-address to ip mappins
# the output file for each device is named "device.name"+"."+file_ext
def write_devices(devs, file_ext):
    previous_device_name = ""
    outfile = None
    for dev_name in devs.devices:
        device = devs.get_device(dev_name)
        if device is None:
            raise("got a name: {} from Devices but then failed to give me device". format(dev_name))
        outfile = open(device.name + "." + file_ext, "w")
        for m_to_i in device.mac_to_ips:
            outfile.write("Device Name: {} MacAddr: {} ip_address {}\n"
                          .format(m_to_i.name, m_to_i.mac_address, m_to_i.ip_address))
        outfile.close()


def main():
    devices = read_devices("./tmp_csv.csv")
    # 
    # in here can do all kinds of processing on the data
    # 
    #
    # in here can do all kinds of processing on the data
    # 
    write_devices(devices, "something")
    print("table done")


main()
