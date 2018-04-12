<<<<<<< HEAD
Cloud-to-Cloud Migration Framework
=======
Cloud to Cloud Migration 
>>>>>>> 20d128af4b6809f5a311e57da1a2b8835663a8dd

This is the first version, and it is still under development. 

Overview

<<<<<<< HEAD
The program works in OpenStack based cloud environment, where single OpenStack based cloud consists of controller node and compute node. It enables virtual machine migration between two different Openstack based cloud environments. To use the program, two Openstack based cloud environments are required. After configuring the cloud environments, copy the file named SourceCloud on source cloud, and copy the file named DestinationCloud on destination cloud. The program enables migration of VMs from source cloud to destination cloud. Following is a detailed step of using the program.

<<<<<<< HEAD
=======
This program works in OpenStack based cloud environment, where single OpenStack based cloud consists of controller node and compute node. The program enables virtual machine migration between two different Openstack based cloud environments. To use the program, two Openstack based cloud environments are required. After configuring the cloud environments, copy the file named SourceCloud on source cloud, and copy the file named DestinationCloud on destination cloud.  The program enables migration of VMs from source cloud to destination cloud. Following is a detailed step of using the program.

>>>>>>> 20d128af4b6809f5a311e57da1a2b8835663a8dd
i) Prerequisite:
   Install followings on both controlled nodes of source and destination clouds 
   1. Install BBCP
      # apt-get -y install build-essential zlib1g-dev libssl-dev
      # wget http://www.slac.stanford.edu/~abh/bbcp/bbcp.tgz
      # tar xvfz bbcp.tgz
      # cd bbcp/src
      # make
      # mv ../bin/*/bbcp /usr/local/bin/
   2. Install Figlet
   # apt-get install figlet
     
  3. Set SSH login without password between the controller nodes
  #
       
      
<<<<<<< HEAD
=======
Current Support

Ubuntu Operating System 16.04.01 LTS
OpenStack Ocata
>>>>>>> 7a95ff4... Updated version
=======
>>>>>>> 20d128af4b6809f5a311e57da1a2b8835663a8dd
