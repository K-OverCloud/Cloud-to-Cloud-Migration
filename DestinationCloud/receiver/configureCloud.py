from getClient import *
from utils import *
from neutronConfig import *
from novaConfig import *
from glanceConfig import *
import time

def instance(name, config_file_path, novaClient, neutronClient):
     #networkList = getNameToNetwork(config_file_path)
     iData = getInstanceData(name, config_file_path)
     instance = createInstance(novaClient, name, iData['network'], iData['flavor'])
     print "completed to create a VM \n"
     
     if iData['floatingIP']:
          extnet = getExtnetName(config_file_path, neutronClient)
          os.system("neutron floatingip-create --floating-ip-address "+iData['floatingIP']+" "+extnet)
          time.sleep(10)
          addFloatingIP(novaClient, instance.name, iData['floatingIP'])
          print "Allocated floating IP %s" %(iData['floatingIP'])

def getExtnetName(config_file_path, neutronClient):
    networks = getNetworkInfo(config_file_path)

    for networkInfo in networks:
          if networkInfo["external"] == True:
             return networkInfo["name"]

def configureNetwork(config_file_path, neutronClient, novaClient):
    networks = getNetworkInfo(config_file_path)

    for networkInfo in networks:
          network =  createNetwork(neutronClient, networkInfo["name"], "true", networkInfo["external"],networkInfo["network_type"], networkInfo["shared"])
          print "Created a network:", networkInfo["name"]
          networkID = network["network"]["id"]
          for subnet in networkInfo["subnets"]:
               createSubnet(neutronClient, subnet["name"], subnet["cidr"], subnet["ip_version"], networkID)
               print "Created a subnet %s in the network %s" %(subnet["name"], networkInfo["name"])

    routers = getRouterInfo(config_file_path)

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

