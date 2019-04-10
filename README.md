# Cloud-to-Cloud Migration 

## Overview ##
The program works in OpenStack based cloud environment. It enables automated virtual machine migration between two different Openstack based cloud environments. Also it analyzes communication dependencies of the VMs in the cloud and decides migration order of the VMs in order to reduce service downtime. 

### Current Support ###
* Ubuntu Operating System 16.04.01 LTS
* OpenStack Ocata release

### Prerequisites: ###
1. Two OpenStack based clouds (Source and Destination clouds)
2. Install followings 
```
  # apt-get install figlet, git
  # apt-get install python-pip
  # pip install -U scikit-learn
  # pip intall numpy 
  # pip install matplotlib  
```
3. Set SSH connection without password between the controller nodes
4. Flavor name, and its related resources should be exactly same on both source and destination clouds
5. Additinional IP address for setting external network gateway on destination cloud 
   - It is required for step 7 of user guide

### User guide: ###
Running cloud migrator
1. Load *admin-openrc* file for Openstack identification on both source and destination clouds
2. Download Cloud-to-Cloud-Migration folder on the contreller nodes of both source and destination clouds 
   ```
   $ git clone https://github.com/K-OverCloud/Cloud-to-Cloud-Migration.git
   ```
3. On the source cloud, move to Cloud-to-Cloud-Migration/SourceCloud/ directory
4. On the destination cloud, move to Cloud-to-Cloud-Migration/DestinationCloud/ directory
5. If ownership of shared folder is root, change it to user 
   - On the source cloud: 
    ```
    # chown username:username -R ~/Cloud-to-Cloud-Migration/SourceCloud/shared/
    ```
   - On the destination cloud:
   ```
    # chown username:username -R ~/Cloud-to-Cloud-Migration/DestinationCloud/shared/
    ```
6. Execute receiver.py on the destination cloud 
     ```
     $ python receiver.py
     ```
     - Enter shared directory at source cloud: "sourceUser@SourceIP:/home/sourceUser/Cloud-to-Cloud-Migration/SourceCloud/shared/"  
     > For convenience, you can set the input manually as sample input in receiver.py file
 
7. Execute sender.py on the source cloud 
    ```
     $ python sender.py
    ```
   - Enter shared directory at destination cloud: "destinationUser@DestinationIP:/home/destinationUser/Cloud-to-Cloud-Migration/DestinationCloud/shared/"
   - Enter external gateway IP for destination cloud: "IP for external network gateway" 
   - Enter VM migration order: ["VM1", "VM2", "VM3"]
   > For convenience, you can set the inputs manually as sample input in sender.py file
 
 >  For re-using the migration tool, do following:
 >  1. On the destination, delete **configurations.json**, **completed**, and **all image files** in /Cloud-to-Cloud-Migration/DestinationCloud/shared/ folder
 >  2. On the source, delete **configurationCompleted**, and **all image files** in /Cloud-to-Cloud-Migration/SourceCloud/shared/ folder
 >  3. Remove all network configurations, instances, and images on the destination cloud 

Running dependency analyzer
```
$ cd /Cloud-to-Cloud-Migration/Dependency_Analysis/
$ python findLocation.py

```
## Flow Diagram
![Alt Text](https://raw.githubusercontent.com/K-OverCloud/Cloud-to-Cloud-Migration/master/FlowDiagram.png)


