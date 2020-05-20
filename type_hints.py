import csv
import pprint
import sys
from typing import Dict, List, Optional


# for a named device maps a mac address to an ip address
class MacToIp:
    def __init__(self, aname: str, a_mac: str, an_ip: str) -> None:
        self.name = aname
        self.mac_address = a_mac
        self.ip_address = an_ip

# a device name with a list of mac-ip mappings
class Device:
    def __init__(self, name: str, mapping: MacToIp) -> None:
        self.name = name
        self.mac_to_ips: List[MacToIp] = [mapping]

    def add(self, mac_to_ip) -> None:
        if mac_to_ip.name != self.name:
            raise "trying to add {} to Device with name: {}".format(name, self.name)
        self.mac_to_ips.append(mac_to_ip)

# a collection of Device instances indexed by device name
class Devices:
    def __init__(self) -> None:
        self.devices_dict: Dict[str, Device] = {}

    def has_device(self, name: str) -> bool:
        if name in self.devices_dict:
            return True
        else:
            return False

    def get_device(self, name) -> Optional[Device]:
        if name in self.devices_dict:
            return self.devices_dict[name]
        else:
            return None

    def add_device(self, device: Device) -> None:
        if device.name in self.devices_dict:
            raise "device named {} already in mappings".format(device.name)
        self.devices_dict[device.name] = device

# creates a Mappings instance from an input file
def read_devices(filename: str) -> Devices:
    devices: Devices = Devices()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:

            current_dev_name = row[0]
            mac_to_ip = MacToIp(row[0], row[2], row[1])
            device = devices.get_device(current_dev_name)
            if device is None:
                device = Device(row[0], mac_to_ip)
                devices.add_device(device)
            else:
                device.add(mac_to_ip)
    return devices


def write_devices(devices: Devices, file_ext: str) -> None:
    for dev_name in devices.devices_dict:
        print(dev_name)
        device = devices.get_device(dev_name)
        outfile = open(device.name + "." + file_ext, "w")
        for mtoip in device.mac_to_ips:
            outfile.write("Device Name: {} MacAddr: {} ip_address {}\n"
                          .format(mtoip.name, mtoip.mac_address, mtoip.ip_address))
        outfile.close()


def main():
    devices: Devices = read_devices("./tmp_csv.csv")
    # 
    # in here can do all kings of processing on the data
    # 
    write_devices(devices, "something")
    print("table done")


main()
