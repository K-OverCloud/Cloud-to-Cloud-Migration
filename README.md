# Cloud-to-Cloud Migration Framework
## Summary ##
### Overview ###

The program works in OpenStack based cloud environment, where single OpenStack based cloud consists of controller node and compute node. It enables virtual machine migration between two different Openstack based cloud environments. To use the program, two Openstack based cloud environments are required. After configuring the cloud environments, copy the file named SourceCloud on source cloud, and copy the file named DestinationCloud on destination cloud. The program enables migration of VMs from source cloud to destination cloud. Following is a detailed step of using the program.

### Current Support ###
* Ubuntu Operating System 16.04.01 LTS
* OpenStack Ocata release

### Prerequists: ###
* Two OpenStack based cloud environment, each cloud consists of contoller and compute nodes 
* * Source cloud for sending VMs
* * Destination cloud for receiving VMs
* Install figlet   (# apt-get install figlet)
* Download Cloud-to-Cloud-Migration folder on the contreller nodes of both  source and destination clouds
* On the source cloud, move to Cloud-to-Cloud-Migration/SourceCloud/ directory
* On the destination cloud, move to Cloud-to-Cloud-Migration/DestinationCloud/ directory



