#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import TCLink

import time

class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # self.addLink(s1, s2, bw=10)
        # self.addLink(h1, s1, bw=10)
        # self.addLink(h2, s1, bw=10)
        # self.addLink(h3, s2, bw=10)

        self.addLink(s1, s2)
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)



class RyuController(Controller):
    "Custom Controller class to invoke Ryu"
    def start( self ):
        "Start Ryu OpenFlow controller"
        self.cmd("sed '/OFPFlowMod(/,/)/s/)/, table_id=1)/' " \
          "ryu/ryu/app/simple_switch_13.py > ryu/ryu/app/qos_simple_switch_13.py")
        self.cmd("ryu-manager ryu.app.rest_qos ryu.app.qos_simple_switch_13 " \
            "ryu.app.rest_conf_switch &")

def measurements(net):
    s1 = net.get('s1')
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    s1.cmd('./configure_queues.sh')

    # h3.cmd('iperf -s -u -i 1 -p 5001 &')
    # h2.cmd('iperf -c 10.0.0.3 -p 5001 -u -b 1G -t 20 &')

    h3.cmd('iperf -s -i 1 -p 5001 &')
    h2.cmd('iperf -c 10.0.0.3 -p 5001 -b 1G -t 20 &')

    h3.cmd('ffplay udp://10.0.0.3:1234 &')

    time.sleep(5)

    h1.cmd('ffmpeg -i Big_Buck_Bunny_1080_10s_30MB.mp4 -f mpegts udp://10.0.0.3:1234')

    time.sleep(15)

if __name__ == '__main__':
    setLogLevel('info')

    topo = CustomTopo()
    net = Mininet(topo, controller=RyuController, link=TCLink)

    s1 = net.get('s1')
    s1.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    s1.cmd('ovs-vsctl set-manager ptcp:6632')

    s2 = net.get('s2')
    s1.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    s1.cmd('ovs-vsctl set-manager ptcp:6632')

    net.start()

    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    net.pingAll()

    print("wait")
    time.sleep(10)
    #CLI(net)

    measurements(net)

    net.stop()

