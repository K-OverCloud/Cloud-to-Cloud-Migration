'''
Created on 2018. 7. 11.

@author: Jax
'''
# Classes for VMs, groups, PMs
class VM():
    def __init__(self, index, cpu, memory, storage):
        self.index = index
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
         
    def setCoord(self, coord):
        self.coord = coord    
        
    def setDistance(self, distances):
        self.distances = distances
        
class PM():
    def __init__(self, index, cpu, memory, storage):
        self.index = index
        self.cpu = cpu
        self.memory = memory
        self.storage = storage
        self.resource = {"CPU": self.cpu, "memory": self.memory, "storage": self.storage}         
        
class GROUP():
    def __init__(self, index, center, order, VMs, radius, cpu, memory, storage):
        self.index = index
        self.VMs = VMs
        self.center = center
        self.order = order
        self.radius = radius
        self.cpu = cpu
        self.memory = memory
        self.storage = storage 
        self.resource = {"cpu":self.cpu, "memory":self.memory, "storage":self.storage}
        self.matchedPM = None
        
    def addVM(self, vm):
        self.VMs.append(vm.index)
        self.cpu = self.cpu + vm.cpu
        self.memory = self.memory + vm.memory
        self.storage = self.storage + vm.storage
        self.resource = {"CPU":self.cpu, "memory": self.memory, "storage":self.storage}
        
    def delVM(self, vm):
        self.VMs.remove(vm.index)
        self.cpu = self.cpu - vm.cpu
        self.memory = self.memory - vm.memory
        self.storage = self.storage - vm.storage
        self.resource = {"CPU":self.cpu, "memory": self.memory, "storage":self.storage}
    
    def setPM(self, pm):
        self.matchedPM = pm
        
    def updateRad(self, rad):
        self.radius = rad
    
        


    
        
        
        
    