# Cloud-to-Cloud Migration 
## Summary ##
### Overview ###

The program works in OpenStack based cloud environment. It enables automated virtual machine migration between two different Openstack based cloud environments.

### Current Support ###
* Ubuntu Operating System 16.04.01 LTS
* OpenStack Ocata release

### Prerequisites: ###
1. Two OpenStack based cloud environment, each cloud consists of contoller and compute nodes 
  * Source cloud for sending VMs
  * Destination cloud for receiving VMs
2. Install figlet   (# apt-get install figlet)
3. Set SSH connection without password between the controller nodes
4. No network and instance configurations on destination cloud 
5. Check resource size on destination cloud 
  * Enough resource for creating all related configrations in source cloud

### User guide: ###
1. Download Cloud-to-Cloud-Migration folder on the contreller nodes of both  source and destination clouds
  * On the source cloud, move to Cloud-to-Cloud-Migration/SourceCloud/ directory
  * On the destination cloud, move to Cloud-to-Cloud-Migration/DestinationCloud/ directory
2. Set owner of shared folders on both source and destination clouds
  * On the source cloud: #chown username:username -R ~/Cloud-to-Cloud-Migration/SourceCloud/shared/
  * On the destination cloud: #chown username:username -R ~/Cloud-to-Cloud-Migration/DestinationCloud/shared/
3. Execute sender.py and receiver.py scripts on the source and destination clouds, respectively
  * On the source cloud: #python sender.py
  * On the destination cloud: #python receiver.py



