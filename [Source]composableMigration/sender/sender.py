'''
Created on March 2, 2017
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

from getClient import *
from utils import *
from neutronConfig import *
from novaConfig import *
from glanceConfig import *
from getConfigurations import *

#logging.basicConfig(filename='/home/controller1/composableMigration/log/sender.log',level=logging.DEBUG)
#logger = logging.getLogger()


wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  # watched events

controllerIP = "172.26.17.151"
username = "admin"
password = "2229"
project_name = "admin"
user_domain_name = "default"
project_domain_name = "default"

remote_dir = "controller2@172.26.17.153:/home/controller2/images/"
config_file_path = "/home/controller1/composableMigration/config/configuration.json"
images_path = "/home/controller1/images/"
migrationOrder = ["ApplicationServer-4","DBServer-5", "WebServer-1", "ApplicationServer-2","DBServer-2", "ApplicationServer-3", "DBServer-3", "DBServer-1", "DBServer-4", "DBServer-6", "ApplicationServer-1","WebServer-2"]


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]
        print "Recieving a file named:", rcvFile

    def process_IN_CLOSE_WRITE(self, event):
        rcvDir = event.pathname.split("/")
        rcvFile = rcvDir[len(rcvDir)-1]

        if rcvFile == 'configurationCompleted':
           print "\n Received configuration completed message from destination, migration start!!!"
           startMigration(nova, glance, migrationOrder, images_path, remote_dir)

def sendFile(filePath, remoteDir):
    os.system("bbcp -P 2 -V -s 16 %s %s" %(filePath, remoteDir))

def deleteInstance(instanceName):
    os.system("nova delete %s" %(instanceName))     

def startMigration(nova, glance, migrationOrder, images_path, remoteDir):
    print "Start Migration"
    for instanceName in migrationOrder: 
        stopInstance(nova, instanceName)
        snapshotId = takeSnapshot(nova, instanceName)
        if snapshotId:
              downloadImage(glance, snapshotId, instanceName, images_path)
        #time.sleep(10)
        deleteInstance(instanceName)
        image = instanceName+'.raw'
        time.sleep(5)
        sendFile(images_path+image, remoteDir)   
                 
        print "Migrated an instance %s" %(instanceName)
        print "****************************************\n\n"
    
    print "Migration completed, and sent completed message. "
    sendFile('~/images/completed', remoteDir)
    
    exit()


if __name__== '__main__':
    os.system("figlet Sender")
    nova = getNovaClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)
    neutron = getNeutronClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)
    glance = getGlanceClient(controllerIP, username, password, project_name, user_domain_name, project_domain_name)
    
    #startMigration(nova, glance, migrationOrder, images_path, remote_dir)

    updateHostConfig(config_file_path, nova, neutron)
    updateNetworkConfig(config_file_path, neutron)
    sendFile(config_file_path, remote_dir)
    
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch('/home/controller1/images/', mask, rec=True)
    notifier.loop()
