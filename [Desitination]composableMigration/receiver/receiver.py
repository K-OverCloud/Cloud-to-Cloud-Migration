'''
Created on March 7, 2017
@author: Jax, Hani
'''

import pyinotify
import os
import time

import json
import traceback
import logging

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as novClient
from neutronclient.v2_0 import client as neutClient

from getClient import *
from utils import *
from neutronConfig import *
from novaConfig import *
from glanceConfig import *

logging.basicConfig(filename='/home/controller2/composableMigration/log/receiver.log',level=logging.DEBUG)
logger = logging.getLogger()


wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  # watched events

controllerIP = "172.26.17.153" 
username = "admin"
password = "2229"
project_name = "admin"
user_domain_name = "default"
project_domain_name = "default"

config_completed_dir = "/home/controller2/images/configurationCompleted"
remote_dir = "controller1@172.26.17.151:/home/controller1/images"
configFilePath = "/home/controller2/images/configuration.json"
imagesPath = "/home/controller2/images/"

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CREATE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]
        
        if rcvFile == 'completed':
           print "\n\n Received complete message, migration completed!!!"
           exit()
        else:                   
           print "Recieving a file named:", rcvFile
   
    def process_IN_CLOSE_WRITE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]
        
        if rcvFile == "configuration.json":
            os.system("chmod o+r ~/images/configuration.json")
            configureNetwork( event.pathname, neutron, nova)
            sendFile(config_completed_dir, remote_dir)
        elif rcvFile == 'completed':
           print "\n\n Received complete message, migration completed!!!"
           exit()
        else:
           print "Completed to recieve the file %s in a directory: %s\n" %(rcvFile,event.pathname)
           rcvFileSplit = rcvFile.split(".")
           imageName = rcvFileSplit[0]
           
           print "Start to upload image"
           uploadImage(glance, imageName, event.pathname)
           
           time.sleep(10)
           print "Start to create a VM"
           instance(imageName, configFilePath, nova) 
            
def sendFile(fileDir, remoteDir):
    os.system("bbcp -P 2 -V -s 16 %s %s" %(fileDir, remoteDir))
          
def instance(name, configFilePath, novaClient):
     networkList = getNameToNetwork(configFilePath)
     print networkList[name]
     instance = createInstance(novaClient, name, networkList[name])
     print "completed to create a VM \n"
     
     floatingIPList = getNameToIP(configFilePath)
     os.system("neutron floatingip-create --floating-ip-address "+floatingIPList[name]+"  Extnet")
     time.sleep(10)
     addFloatingIP(novaClient, instance.name, floatingIPList[name])
     print "Allocated floating IP %s" %(floatingIPList[name])



def configureNetwork(configFilePath, neutronClient, novaClient):
    networks = getNetworkInfo(configFilePath)

    for networkInfo in networks:
          network =  createNetwork(neutronClient, networkInfo["name"], "true", networkInfo["external"],networkInfo["network_type"], networkInfo["shared"])
          print "Created a network:", networkInfo["name"]
          networkID = network["network"]["id"]
          for subnet in networkInfo["subnets"]:
               createSubnet(neutronClient, subnet["name"], subnet["cidr"], subnet["ip_version"], networkID)
               print "Created a subnet %s in the network %s" %(subnet["name"], networkInfo["name"])

    routers = getRouterInfo(configFilePath)

    for routerInfo in routers:
         network_name = routerInfo["external_gateway_info"]["network"]
         network_id = novaClient.networks.find(label=network_name).id
         for subnet in neutronClient.list_subnets()["subnets"]:
              if subnet["network_id"] == network_id:
                        subnet_id = subnet["id"]
         name =  routerInfo["name"]
         admin_state_up = routerInfo["admin_state_up"]
         enable_snat =  routerInfo["external_gateway_info"]["enable_snat"]
         ip_address =  routerInfo["external_gateway_info"]["external_fixed_ips"][0]["ip_address"]

         router = createRouter(neutronClient, name, network_id, enable_snat, ip_address, subnet_id, admin_state_up)
         if router:
             print "Created a router:", name

    for networkInfo in networks:
        external = networkInfo["external"]
        if  str(external) == "False":
               networkName = networkInfo["name"]
               network_id = novaClient.networks.find(label=networkName).id
               for subnet in neutronClient.list_subnets()["subnets"]:
                     if subnet["network_id"] == network_id:
                          subnet_id = subnet["id"]
                          connectSubnetToRouter(neutronClient, router["router"]["id"], subnet_id)
                          print "Connected the subnet %s to the rourer %s" %(subnet["name"], router["router"]["name"])

if __name__=='__main__':
    os.system("figlet Receiver")
    nova = getNovaClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)
    neutron = getNeutronClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)
    glance = getGlanceClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(imagesPath, mask, rec=True)
    print "Waiting to receive migrated images ...\n"

    notifier.loop()
