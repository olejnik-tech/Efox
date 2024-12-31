class Target:
    def __init__(self, interface=None, router_mac=None, router_ssid=None, device_mac=None, channel=None):
        self.interface = interface
        self.router_mac = router_mac
        self.router_ssid = router_ssid
        self.device_mac = device_mac
        self.channel = channel

    def set_target(self, interface, router_mac, router_ssid, device_mac, channel):
        self.interface = interface
        self.router_mac = router_mac
        self.router_ssid = router_ssid
        self.device_mac = device_mac
        self.channel = channel