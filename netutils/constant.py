#-*- coding: utf-8 -*-

SIOCGIFNAME        = 0x8910          # get iface name
SIOCGIFCONF        = 0x8912          # get iface list
SIOCGIFFLAGS       = 0x8913          # get flags
SIOCGIFADDR        = 0x8915          # get PA address
SIOCGIFDSTADDR     = 0x8917          # get remote PA address
SIOCGIFBRDADDR     = 0x8919          # get broadcast PA address
SIOCGIFNETMASK     = 0x891b          # get network PA mask
SIOCGIFMETRIC      = 0x891d          # get metric
SIOCGIFMEM         = 0x891f          # get memory address (BSD)
SIOCGIFMTU         = 0x8921          # get MTU size
SIOCGIFENCAP       = 0x8925          # get/set encapsulations
SIOCSIFPFLAGS      = 0x8934          # set/get extended flags set
SIOCGIFCOUNT       = 0x8938          # get number of devices
SIOCWANDEV         = 0x894A          # get/set netdev parameters
SIOCGARP           = 0x8954          # get ARP table entry
SIOCGRARP          = 0x8961          # get RARP table entry
SIOCSHWTSTAMP      = 0x89b0          # set and get config
SIOCGHWTSTAMP      = 0x89b1          # get config
SIOCGHWMAC         = 0x8927          # get mac address

MAX_IFACE = 32    #Maximum number of interfaces(Aribtrary)
BYTES_LENGTH = MAX_IFACE * 32
