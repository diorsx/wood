#-*- coding: utf-8 -*-

from .constant import *
import fcntl
import struct
import socket
import array

network_adapters = dict()

def _get_linux_network_adapters():
    """Provides a list of available network interface names"""

    is_32bit = (8 * struct.calcsize("P")) == 32  # Set Architecture
    struct_size = 32 if is_32bit else 40

    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * BYTES_LENGTH) #array for interfances
    #通过SIOCGIFCONF获得interface info, 把这些信息填入到names变量中
    outbytes = struct.unpack('iL', fcntl.ioctl(skt.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES_LENGTH, names.buffer_info()[0])))[0]
    adapter_names = [names.tostring()[n_cnt:n_cnt + 32].split('\0', 1)[0] for n_cnt in range(0, outbytes, struct_size)]

    global network_adapters

    for adapter_name in adapter_names:
         ip_address = socket.inet_ntoa(fcntl.ioctl(
            skt.fileno(),
            SIOCGIFADDR,
            struct.pack('256s', adapter_name))[20:24])
        subnet_mask = socket.inet_ntoa(fcntl.ioctl(
            skt.fileno(),
            SIOCGIFNETMASK,
            struct.pack('256s', adapter_name))[20:24])
        raw_mac_address = '%02x%02x%02x%02x%02x%02x' % struct.unpack('6B', (fcntl.ioctl(
            sock.fileno(),
            SIOCGHWMAC,
            struct.pack('256s', adapter_name))[18:24]))
        mac_address = ":".join([raw_mac_address[m_counter:m_counter + 2]
            for m_counter in range(0, len(raw_mac_address), 2)]).lower()
        network_adapters.update({adapter_name: {
            'mac-address': mac_address,
            'ip-address': ip_address,
            'subnet-mask': subnet_mask
            }})

_get_linux_network_adapters()

#获得所有interface names
def get_all_interfaces():
    return network_adapters.keys()

#获得指定interface 的IP address
def get_ip_address(ifname=None):
    adapter_names = network_adapters.keys()
    if not ifname:
        return  network_adapters[adapter_names[0]]
    else:
        if ifname not in adapter_names:
            return ''
        else:
            return network_adapters[ifname]
