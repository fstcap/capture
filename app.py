import ssl
from scapy.all import *
from threading import Thread, Event
from time import sleep

class Sniffer(Thread):
    def  __init__(self, interface='en0'):
        super(Sniffer, self).__init__()

        self.daemon = True

        self.socket = None
        self.interface = interface
        self.stop_sniffer = Event()

    def run(self):
        self.socket = conf.L2listen(
            type=ETH_P_ALL,
            iface=self.interface,
            filter="dst host m.baidu.com"
        )

        sniff(
            opened_socket=self.socket,
            prn=self.print_packet,
            stop_filter=self.should_stop_sniffer
        )

    def join(self, timeout=None):
        self.stop_sniffer.set()
        super().join(timeout)

    def should_stop_sniffer(self, packet):
        return self.stop_sniffer.isSet()

    def print_packet(self, packet):
        raw_layer = packet.getlayer(Raw)   
        try:
            raw_text = raw_layer.load
        except AttributeError:
            raw_text = 'without raw'
        print("\033[0;35m[!] Raw\033[0;34m -> \033[0;36m{raw}\033[0m".format(raw=raw_text))

sniffer = Sniffer()

print("\033[0;32m[*] Start sniffing...\033[0m")
sniffer.start()

try:
    while True:
        sleep(100)
except KeyboardInterrupt:
    print("\033[0;32m[*] Stop sniffing\033[0m")
    sniffer.join(2.0)

    if sniffer.isAlive():
        sniffer.socket.close()
