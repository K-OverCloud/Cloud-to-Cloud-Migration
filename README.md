# Cloud-to-Cloud Migration Framework
## Summary ##
### Overview ###

The program works in OpenStack based cloud environment. It enables automated virtual machine migration between two different Openstack based cloud environments.

### Current Support ###
* Ubuntu Operating System 16.04.01 LTS
* OpenStack Ocata release

### Prerequisites: ###
* Two OpenStack based cloud environment, each cloud consists of contoller and compute nodes 
  * Source cloud for sending VMs
  * Destination cloud for receiving VMs
* Install figlet   (# apt-get install figlet)
* Download Cloud-to-Cloud-Migration folder on the contreller nodes of both  source and destination clouds
* On the source cloud, move to Cloud-to-Cloud-Migration/SourceCloud/ directory
* On the destination cloud, move to Cloud-to-Cloud-Migration/DestinationCloud/ directory



