from utils import *

def updateNetworkConfig(file_path, neutronClient):
    networks = neutronClient.list_networks()['networks']
    subnets = neutronClient.list_subnets()['subnets']
    routers = neutronClient.list_routers()['routers']
    floatingIPs = neutronClient.list_floatingips()['floatingips']
    data = config_json_read(file_path)
    
    nets = []
    for network in networks:
         name = network['name']
         external = network['router:external'] 
         network_type = network['provider:network_type']  
         shared = network['shared']
         snets = []
         for subnet in subnets:
             if network['id'] == subnet['network_id']:
                 snet = {'name': subnet['name'], 'cidr':subnet['cidr'],'ip_version': subnet['ip_version']}
                 snets.append(snet)
         net = {'name': name, 'external': external, 'network_type': network_type, 'shared': shared, 'subnets': snets }
         nets.append(net)              
    
    routersList = []
    for router in routers:
         external_fixed_ips = []
         name = router['name']
         admin_state_up = router['admin_state_up']
         for network in networks:
              if network['id'] == router['external_gateway_info']['network_id']:
                   networkName = network['name']
                   enable_snat =  router['external_gateway_info']['enable_snat']
         
         external_fixed_ips = []
         for external_fixed_ip in router['external_gateway_info']['external_fixed_ips']:
                
                for subnet in subnets:
                    if subnet['id'] ==  external_fixed_ip['subnet_id']:
                               #fixed_ip = {"ip_address":external_fixed_ip["ip_address"], "subnet_name":subnet['name']}
                               fixed_ip = {"ip_address":remote_gateway, "subnet_name":subnet['name']}
                               fixed_ip = {"ip_address":external_fixed_ip["ip_address"], "subnet_name":subnet['name']}
                               external_fixed_ips.append(fixed_ip)     
         
         external_gateway_info = {"network":networkName, "enable_snat":enable_snat, "external_fixed_ips":external_fixed_ips}
         
         routerInfo = {"name":name, "admin_state_up":admin_state_up, "external_gateway_info":external_gateway_info} 
         routersList.append(routerInfo)         
    

    floatingIPList = []
    for floatingIP in floatingIPs :
         floatingIPList.append(floatingIP['floating_ip_address'])

   
    data['Networks'] = nets
    data['Routers'] = routersList
    data['FloatingIPs'] = floatingIPList 
    config_json_write(file_path, data)

def updateHostConfig(file_path, novaClient):
    instanceList = novaClient.servers.list()
    flavors = novaClient.flavors.list()
    VMs = [] 
     
    for instance in instanceList:
          floatingIP = ""
          flavor_id = instance.flavor['id']
          for flavor in flavors:
               if flavor.id == flavor_id:
                   flavor_name = flavor.name

          for network_name, snets in instance.addresses.items():
               #print name
               for snet in snets:
                   if snet['OS-EXT-IPS:type'] == 'floating':
                         floatingIP = snet["addr"]            
          
          vm = {'name': instance.name, 'flavor': flavor_name,  'network': network_name, 'floatingIP': floatingIP}
          VMs.append(vm)
    data = config_json_read(file_path)
    data['VMs'] = VMs
    config_json_write(file_path, data)
