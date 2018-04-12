'''
Created on March 2, 2017
Updated on April 11, 2018
@author: Jargal
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
from glanceclient import Client as glanceClient
from glanceclient.common import utils as utilsGlance

from sender.getClient import *
from sender.utils import *
from sender.neutronConfig import *
from sender.novaConfig import *
from sender.glanceConfig import *
from sender.getConfigurations import *
from os import *

#Input log directory in filename
logging.basicConfig(filename=' ',level=logging.DEBUG)
logger = logging.getLogger()

# Watch manager
wm = pyinotify.WatchManager()  
mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  # watched events

#Cloud information for authentication
auth_url = environ['OS_AUTH_URL']
username = environ['OS_USERNAME']
password = environ['OS_PASSWORD']
project_name = environ['OS_PROJECT_NAME']
user_domain_name = environ['OS_USER_DOMAIN_NAME']
project_domain_name = environ['OS_PROJECT_DOMAIN_NAME']

# Directory info
current_dir = os.getcwd() 
completed_file_path = current_dir+"/shared/completed"
shared_dir = current_dir+"/shared/"
config_file_path = current_dir+"/shared/configuration.json"

#**************************INPUT****************************************** 
remote_dir = input('Enter shared directory at destination cloud: ')
remote_gateway = input('Enter external gateway IP for destination cloud: ')
migrationOrder = input('Enter VM migration order in list: ')
# *************************************************************************

# Sample INPUT 
#remote_gateway = "172.26.17.137"
#remote_dir = "controller1@172.26.17.151:/home/controller1/Cloud-to-Cloud-Migration/DestinationCloud/shared/"
#migrationOrder = ["Instance1","Instance3","Instance2"]

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]
        print "Recieving a file named:", rcvFile

    def process_IN_CLOSE_WRITE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]

        if rcvFile == 'configurationCompleted':
           print "\n Received configuration completed message from destination, migration starts!!!"
           startMigration(nova, glance, migrationOrder, shared_dir, remote_dir)

def sendFile(filePath, remoteDir):
    #os.system("bbcp -P 2 -V -s 16 %s %s" %(filePath, remoteDir))
    os.system("scp %s %s" %(filePath, remoteDir))


def deleteInstance(instanceName):
    os.system("nova delete %s" %(instanceName))     

def startMigration(nova, glance, migrationOrder, shared_dir, remoteDir):
    print "Start Migration"
    for instanceName in migrationOrder: 
        stopInstance(nova, instanceName)
        snapshotId = takeSnapshot(nova, instanceName)
        downloadImage(glance, snapshotId, instanceName, shared_dir)
        image = instanceName+'.raw'
        sendFile(shared_dir+image, remoteDir)   
                 
        print "Migrated an instance %s" %(instanceName)
        print "****************************************\n\n"
    
    print "Migration completed, and sent completed message. "
    sendFile('~/images/completed', remoteDir)
    
    exit()


if __name__== '__main__':
    os.system("figlet Sender")
    # Getting autherized users
    nova = getNovaClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)
    neutron = getNeutronClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)
    glance = getGlanceClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)
     
    #Obtaining network and host configuration info   
    updateHostConfig(config_file_path, nova)
    updateNetworkConfig(config_file_path, neutron, remote_gateway)
    
    # Send obtained info to destination cloud
    sendFile(config_file_path, remote_dir)

    # Handler listenst shared location at source cloud 
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(shared_dir, mask, rec=True)
    notifier.loop()
