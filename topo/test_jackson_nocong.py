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
from time import sleep
from os import system

cores = [2, 3, 4, 5, 6, 7]
add_load = True
def myNetwork():

#    setLogLevel('debug')
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')

    h1 = net.addHost('h1', cls=CPULimitedHost, ip='10.0.0.1', defaultRoute=None)
    h1.setCPUs(cores=cores[0])
    h1.setCPUFrac(f=20.0, sched='host')

    h2 = net.addHost('h2', cls=CPULimitedHost, ip='10.0.0.2', defaultRoute=None)
    h2.setCPUs(cores=cores[1])
    h2.setCPUFrac(f=20.0, sched='host')

    h3 = net.addHost('h3', cls=CPULimitedHost, ip='10.0.0.3', defaultRoute=None)
    h3.setCPUs(cores=cores[2])
    h3.setCPUFrac(f=20.0, sched='host')

    h4 = net.addHost('h4', cls=CPULimitedHost, ip='10.0.0.4', defaultRoute=None)
    h4.setCPUs(cores=cores[3])
    h4.setCPUFrac(f=20.0, sched='host')

    h5 = net.addHost('h5', cls=CPULimitedHost, ip='10.0.0.5', defaultRoute=None)
    h5.setCPUs(cores=cores[4])
    h5.setCPUFrac(f=20.0, sched='host')

    h6 = net.addHost('h6', cls=CPULimitedHost, ip='10.0.0.6', defaultRoute=None)
    h6.setCPUs(cores=cores[5])
    h6.setCPUFrac(f=20.0, sched='host')




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

    intfs = {}
    for i, switch in enumerate(net.switches):
        intfs[str(switch)] = switch.intfs
    
    interfaces = []
    for host in intfs:
	for intf in intfs[host]:
		if (str((intfs[host])[intf]) != 'lo'):
	        	interfaces.append(str((intfs[host])[intf]))
    print(interfaces)

    capture = net.addHost('capture', cls=CPULimitedHost, ip='10.0.0.10', defaultRoute=None, inNamespace=False)
    capture.setCPUs(cores=1)
    capture.setCPUFrac(f=15.0, sched='host')

    info( '*** Add links\n')
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])

    info( '*** Post configure switches and hosts\n')

    capture.sendCmd('./capture.sh '+(' '.join(interfaces)))
    h6.cmd('python -m SimpleHTTPServer 80 &')
    
    sleep(5)
    info( '*** Generating traffic \n')
    if add_load:
        for host_i in range(6):
	    for host_j in range(6):
		command = 'taskset -c ' + str(cores[host_i]) + ' ping -i 0.01 ' + str(net.hosts[host_j].IP()) + " | awk '{print \"" + str(net.hosts[host_i].IP()) + "\",$4, $6, $7 }' > data/ping_" + str(host_i) + '_' + str(host_j) + '.data &'
		info("Command "+command+"\n")
    		result=net.hosts[host_i].cmd(command)


    [h1.cmd('echo "12345" | nc '+h6.IP()+' 80') for i in range(5000)]
    info( '*** End of tests\n')

    sleep(15)
    system('killall -9 ping; killall -9 nc')
    capture.sendInt()
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

