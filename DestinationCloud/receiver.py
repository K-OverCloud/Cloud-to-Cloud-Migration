'''
Created on March 17, 2017
Updated on April 11, 2018
@author: Jargal
'''
import pyinotify
import os
import time
import logging

from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as novClient
from neutronclient.v2_0 import client as neutClient

from receiver.getClient import *
from receiver.glanceConfig import uploadImage
from receiver.configureCloud import *
from os import environ

#Input log directory in the file name
logging.basicConfig(filename='',level=logging.DEBUG)
logger = logging.getLogger()

# Watch manager
wm = pyinotify.WatchManager()  
mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CREATE  

#**********************INPUT***********************************
remote_dir = input('Enter shared directory at source cloud: ')
#**************************************************************

# Sample INPUT
#remote_dir = "controller1@172.26.17.151:/home/controller1/Cloud-to-Cloud-Migration/SourceCloud/shared/"

#Source cloud information
auth_url = environ['OS_AUTH_URL']
username = environ['OS_USERNAME']
password = environ['OS_PASSWORD']
project_name = environ['OS_PROJECT_NAME']
user_domain_name = environ['OS_USER_DOMAIN_NAME']
project_domain_name = environ['OS_PROJECT_DOMAIN_NAME']

# Destination cloud information
current_dir = os.getcwd()
config_file_path = current_dir+"/shared/configuration.json"
shared_dir = current_dir+"/shared/"
config_completed_dir = current_dir+"/shared/configurationCompleted"

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
            os.system("chmod o+r "+config_file_path)

            # from receiver.configCloud import configureNetwork
            configureNetwork(event.pathname, neutron, nova)
            sendFile(config_completed_dir, remote_dir)
        elif rcvFile == 'completed':
           print "\n\n Received completed message, migration completed!!!"
           exit()
        else:
           print "Completed to recieve the file %s in a directory: %s\n" %(rcvFile,event.pathname)
           rcvFileSplit = rcvFile.split(".")
           imageName = rcvFileSplit[0]
           
           print "Uploading image"
           #from receiver.glanceConfig import uploadImage
           uploadImage(glance, imageName, event.pathname)
           
           print "Start to create a VM"
           # from receiver.configCloud import instance
           instance(imageName, config_file_path, nova, neutron) 
            
def sendFile(fileDir, remoteDir):
    #os.system("bbcp -P 2 -V -s 16 %s %s" %(fileDir, remoteDir))
    os.system("sudo scp %s %s" %(fileDir, remoteDir))
          

if __name__=='__main__':
    os.system("figlet Receiver")
    nova = getNovaClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)
    neutron = getNeutronClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)
    glance = getGlanceClient(auth_url, username, password, project_name, user_domain_name, project_domain_name)

    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(shared_dir, mask, rec=True)
    print "Waiting to receive ...\n"

    notifier.loop()
