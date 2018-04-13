# Cloud-to-Cloud Migration 
## Summary ##
### Overview ###

The program works in OpenStack based cloud environment. It enables automated virtual machine migration between two different Openstack based cloud environments.

### Current Support ###
* Ubuntu Operating System 16.04.01 LTS
* OpenStack Ocata release

### Prerequisites: ###
1. Two OpenStack based clouds 
2. Install figlet and git on controller nodes  (# apt-get install figlet, git)
3. Set SSH connection without password between the controller nodes
4. Flavor name, and its related resources should be exactly same on both source and destination clouds
5. Additinional IP address for setting external network gateway on destination cloud 

### User guide: ###
1. Load ** admin-openrc ** file for Openstack identification on both source and destination clouds
2. Download Cloud-to-Cloud-Migration folder on the contreller nodes of both source and destination clouds 
   - git clone https://github.com/K-OverCloud/Cloud-to-Cloud-Migration.git
2. On the source cloud, move to Cloud-to-Cloud-Migration/SourceCloud/ directory
3. On the destination cloud, move to Cloud-to-Cloud-Migration/DestinationCloud/ directory
4. If ownership of shared folder is root, change it to user 
   - On the source cloud: #chown username:username -R ~/Cloud-to-Cloud-Migration/SourceCloud/shared/
   - On the destination cloud: #chown username:username -R ~/Cloud-to-Cloud-Migration/DestinationCloud/shared/
5. Execute receiver.py on the destination cloud ($ python receiver.py)
   - Enter shared directory at source cloud: "sourceUser@SourceIP:/home/sourceUser/Cloud-to-Cloud-Migration/SourceCloud/shared/"
6. Execute sender.py on the source cloud ($ python sender.py)
   - Enter shared directory at destination cloud: "destinationUser@DestinationIP:/home/destinationUser/Cloud-to-Cloud-Migration/DestinationCloud/shared/"
   - Enter external gateway IP for destination cloud: "IP for external network gateway" 
   - Enter VM migration order: ["VM1", "VM2", "VM3"]
 


