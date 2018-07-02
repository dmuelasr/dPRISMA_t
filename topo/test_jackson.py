#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h6.setCPUs(cores='7')
    h6.setCPUFrac(f=20.0, sched='host')

    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h4.setCPUs(cores='5')
    h4.setCPUFrac(f=20.0, sched='host')

    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h5.setCPUs(cores='6')
    h5.setCPUFrac(f=20.0, sched='host')


    h2 = net.addHost('h2', cls=CPULimitedHost, ip='10.0.0.2', defaultRoute=None)
    h2.setCPUs(cores='3')
    h2.setCPUFrac(f=20.0, sched='host')

    h1 = net.addHost('h1', cls=CPULimitedHost, ip='10.0.0.1', defaultRoute=None)
    h1.setCPUs(cores='2')
    h1.setCPUFrac(f=20.0, sched='host')

    h3 = net.addHost('h3', cls=CPULimitedHost, ip='10.0.0.3', defaultRoute=None)
    h3.setCPUs(cores='4')
    h3.setCPUFrac(f=20.0, sched='host')

    info( '*** Add links\n')
    h1s1 = {'bw':10}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    s1h2 = {'bw':10}
    net.addLink(s1, h2, cls=TCLink , **s1h2)
    s1h3 = {'bw':10}
    net.addLink(s1, h3, cls=TCLink , **s1h3)
    s1s2 = {'bw':10}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    net.addLink(s2, h4)
    s2h5 = {'bw':10}
    net.addLink(s2, h5, cls=TCLink , **s2h5)
    s2h6 = {'bw':10}
    net.addLink(s2, h6, cls=TCLink , **s2h6)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

