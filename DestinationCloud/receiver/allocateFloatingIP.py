from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as novClient
from neutronclient.v2_0 import client as neutClient
from glanceclient import Client as glanceClient
from glanceclient.common import utils

controllerIP = "172.26.17.153"
username = "admin"
password = "2229"
project_name = "admin"
user_domain_name = "default"
project_domain_name = "default"


def getNovaClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name):
    auth = v3.Password(auth_url= 'http://'+controllerIP+':35357/v3',
                           username = username,
                           password= password,
                           project_name = project_name,
                           user_domain_name = user_domain_name,
                           project_domain_name = project_domain_name)
    sess = session.Session(auth=auth)
    nova = novClient.Client("2.1", session=sess)

    return nova





def addFloatingIP(nova, instanceName, floatingIP):
    try:
        notActive = True
        while notActive:
                instance = nova.servers.find(name=instanceName)
                if instance.status == 'ACTIVE':
                        notActive = False
        print "Instance created\n"

        instance.add_floating_ip(floatingIP)
        print "Floating ip allocated : %s %s" %(instanceName, floatingIP)
    except Exception as e:
        print str(e)

instanceName = raw_input("Instance Name Prefix:")
index1 = raw_input("Index1:")
index2 = raw_input("Index2:")

start = raw_input("IP start:")
end = raw_input("IP end:")

nova = getNovaClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)

i = int(start)
last = int(end)

insIndex1 = int(index1)
insIndex2 = int(index2)
while i <= last:
    for j in range(insIndex1, (insIndex2+1), 1):
            name = instanceName+"-"+str(j)
            floatingIP = "192.168.100."+str(i)
            addFloatingIP(nova, name, floatingIP)
            i = i + 1

