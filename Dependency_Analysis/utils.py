'''
Created on 2018. 7. 11.

@author: Jax
'''
from objects import GROUP
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import distance
import itertools
from sklearn.metrics.pairwise import euclidean_distances
from scipy.optimize import linear_sum_assignment
import networkx as nx
from operator import itemgetter

def getPCA(my_matrix, coordNum):
    my_model = PCA(n_components=2)
    my_model.fit_transform(my_matrix)

    cov = my_model.get_covariance()
    eigvals, eigvecs = np.linalg.eig(cov)
    
    temp = eigvals
    newMatrix = []

    while coordNum != 0:
        pc = np.argmax(temp)
        newMatrix.append(eigvecs[pc])
        temp[pc] = 0
        coordNum = coordNum - 1

    matrix = np.dot(newMatrix, my_matrix)
    
    return matrix

def getRadius(matrix, m):
    minx = min(matrix[0])
    maxx = max(matrix[0])
    width= maxx - minx
 
    miny = min(matrix[1])
    maxy = max(matrix[1])
    length = maxy - miny

    area = width*length
    rad = np.sqrt(area/(3.14*m))

    return rad

def getCoord(matrix):
    coord = []
    for i in range(len(matrix[0])):
        a = []
        a.append(matrix[0][i])
        a.append(matrix[1][i])
        coord.append(a)

    return coord    

        
def selectHeader(distances, rad, eList):
    neighborNumber = []
    neighborSet = []
    for  dist in distances:
        k = 0
        neighbors = []
        for i in range(len(dist)):
            if dist[i] <= rad and (i not in eList):
                k = k + 1
                neighbors.append(i)
        neighborNumber.append(k)
        neighborSet.append(neighbors)
        
    max_index = np.argmax(neighborNumber)
    
    headerNode = {"center":max_index, "nodes":neighborSet[max_index], "radius": rad}
    
    return headerNode

def updateGroups(nodes, distances, rad, groupNum):
    eList = []
    groups = []
    while groupNum != 0:
        header = selectHeader(distances, rad, eList)
        eList.extend(header["nodes"])
        groups.append(header)
        groupNum = groupNum - 1
        
    gNodes = set()
    for group in groups:
        gNodes.update(group["nodes"])
        
    ugNodes = nodes - gNodes
    
    for node in ugNodes:
        dList = []
        for group in groups:
            center = group["center"]
            dist =  distances[center][node] - rad
            dList.append(dist)
            
        min_index = np.argmin(dList)
        groups[min_index]["nodes"].append(node)
        
    return groups
    
def computeResource(group, vmList):
    cpu = 0
    mem = 0 
    storage = 0
    for node in group["nodes"]:
        cpu = cpu + vmList[node].cpu
        mem = mem + vmList[node].memory
        storage = storage + vmList[node].storage
    reqResource = {"cpu":cpu, "memory":mem, "storage":storage}
     
    return reqResource  

def getGroups(nodes, distances, rad, groupNum, vmList):
    groupList = []
    cluster ={"center":"", "order":"", "nodes":"", "radius":"", "reqResource":""}
    groups = updateGroups(nodes, distances, rad, groupNum)
    order = getGroupOrder(groups, distances)
    
    for group in groups:
        reqResource = computeResource(group, vmList)
        cluster["reqResource"] = reqResource
        cluster["center"] = group["center"]
        cluster["order"] = order.index(group["center"])
        cluster["nodes"] = group["nodes"]
        cluster["radius"] = group["radius"]
        groupList.append(cluster) 
        cluster ={"center":"", "order":"", "nodes":"", "radius":"", "reqResource":""}
        
    return groupList                

def findFarest(group, distances):
    center = group.center
    distance = distances[center]
    distList = []
    nodes = group.VMs
    for node in nodes:
        distList.append(distance[node])
    
    max_index = np.argmax(distList)
    
    return nodes[max_index]    


def findClosestGroup(groups, vm, excList):
    distances = []
    for group in groups:
        distances.append(vm.distances[group.center] - group.radius)
        
    for i in excList:
        distances[i] = float("inf")
        
    min_index = np.argmin(distances)
    
    return groups[min_index]
    
def checkConstraint(pm, group):
    if pm.cpu < group.cpu or pm.memory < group.memory or pm.storage < group.storage:
        return 1
    else:
        return 0   
    
def putRemovedVMs(removedVMs, groups, vmList, pmList, match):
    
    
    for i in removedVMs[:]:
        excList = []
        while len(excList) <= len(groups):
            closest = findClosestGroup(groups, vmList[i], excList)
            closest.addVM(vmList[i])
            if checkConstraint(pmList[match.index(closest.index)], closest) == 1:
                closest.delVM(vmList[i])
                excList.append(closest.index)
            else:
                removedVMs.remove(i)
                break
            
    return removedVMs

def satisfyConstraint(match, groups, pmList, vmList, distances):
    removedVMs = []
    for i in range(len(match)):
        groups[match[i]].setPM(pmList[i])
        while pmList[i].cpu<groups[match[i]].cpu or pmList[i].memory<groups[match[i]].memory or pmList[i].storage<groups[match[i]].storage:
            removedVMs.append(findFarest(groups[match[i]], distances))
            groups[match[i]].delVM(vmList[findFarest(groups[match[i]], distances)])
        
    return removedVMs
    
def matchingGroupToPM(pmList, groups):
    A = []
    for pm in pmList:
        B = []
        for group in groups:
            a = (np.true_divide(group.cpu,pm.cpu), np.true_divide(group.memory,pm.memory), np.true_divide(group.storage,pm.storage))
            b = (1,1,1)
            edist = distance.euclidean(a, b)
            if any([True for i in a if i > 1]) == True:
                edist = edist + 100
            
            B.append(edist) 
        A.append(B)
        
    row_ind, col_ind = linear_sum_assignment(A)  # @UnusedVariable
    
    return col_ind


def checkSameGroup(groups, i, j):
    for group in groups:
        if (i in group.VMs) and (j in group.VMs):
            return 0
    return 1

def getHopNumber(groups, i, j, topo):
    for group in groups:
        if i in group.VMs:
            index1 = group.order
    
    for group in groups:
        if j in group.VMs:
            index2 = group.order
    
    return topo[index1][index2]

def getOriginalHopNumber(groups, i, j, topo):
    k = 0 
    for group in groups:
        if i in group:
            index1 = k
        k = k + 1
    
    s = 0    
    for group in groups:
        if j in group:
            index2 = s
        s = s + 1
            
    return topo[index1][index2]
        
def computeTraffic(tMatrix, groups):
    T = 0
    I = 0
    for i in range(len(tMatrix)):
        for j in range(len(tMatrix)):
            I = checkSameGroup(groups, i, j)  
            T = T + (tMatrix[i][j]*I)
    T = T/2
    
    return T

def oCheckSameGroup(groups, i, j):
    for group in groups:
        if (i in group) and (j in group):
            return 0
    return 1
        
def oComputeTraffic(tMatrix, groups):
    T = 0
    I = 0
    for i in range(len(tMatrix)):
        for j in range(len(tMatrix)):
            I = oCheckSameGroup(groups, i, j)  
            T = T + (tMatrix[i][j]*I)
    T = T/2
    
    return T

def oComputeCost(tMatrix, groups, topo):
    C = 0
    I = 0
    for i in range(len(tMatrix)):
        for j in range(len(tMatrix)):
            I = getOriginalHopNumber(groups, i, j, topo) 
            C = C + (tMatrix[i][j]*I)
    C = C/2
    
    return C
                
def getSolution(pmList, vmList, distances, tMatrix, nodes, rad):
    tList = []
    solList =[]
    
    matches = list(itertools.permutations(range(len(pmList)), len(pmList)))
    for match in matches: 
        solution = {}
        groups = grouping(nodes, distances, rad, len(pmList), vmList)
        removedVMs = satisfyConstraint(match, groups, pmList, vmList, distances)
        conflictedVMs = putRemovedVMs(removedVMs, groups, vmList, pmList, match)
        if len(conflictedVMs) == 0:
            T = computeTraffic(tMatrix, groups)
            tList.append(T)
            solution = {"match":match, "groups":groups, "traffic":T}
            solList.append(solution)
    min_index = np.argmin(tList) 

    return solList[min_index]  

def getHungarionSolution(pmList, vmList, distances, tMatrix, nodes, rad, topo):
    groups = grouping(nodes, distances, rad, len(pmList), vmList)
        
    m = matchingGroupToPM(pmList, groups)
    match = []
    for a in m:
        match.append(a)
        
    removedVMs = satisfyConstraint(match, groups, pmList, vmList, distances)
    #removedVMsCases = list(itertools.permutations(removedVMs, len(removedVMs)))
    
    conflictedVMs = putRemovedVMs(removedVMs, groups, vmList, pmList, match)
    
    if len(conflictedVMs) == 0:
        T = computeTraffic(tMatrix, groups)
        cost = computeCost(tMatrix, groups, topo)
        solution = {"match":match, "groups":groups, "traffic":T, "cost":cost}
        return solution
    else:
        return False
         
def computeCost(tMatrix, groups, topo):
    C = 0
    I = 0
        
    for i in range(len(tMatrix)):
        for j in range(len(tMatrix)):
            I = getHopNumber(groups, i, j, topo) 
            C = C + (tMatrix[i][j]*I)
    C = C/2
    
    return C
    
def getGroupOrder(groups, distances):
    centers = []
    for group in groups:
        centers.append(group["center"])
    
    G = nx.Graph()
    
    for i in centers:
        G.add_node(i)
        
    for i in centers:
        for j in centers:
            if i != j:
                G.add_edge(i, j, weight = distances[i][j])
    order = []    
    sortedEdges =  sorted(G.edges(data=True), key=itemgetter(2))
    for (u,v,d) in sortedEdges:
        if (u not in order) and (v not in order):
            order.append(u)
            order.append(v)
            centers.remove(u)
            centers.remove(v)
            
    order.extend(centers)
    
    return order


def grouping(nodes, distances, rad, gnum, vm):  
    groups = []
    i = 0
    for group in getGroups(nodes, distances, rad, gnum, vm):
        groups.append(GROUP(i, group["center"], group["order"], group["nodes"], group["radius"], group["reqResource"]["cpu"], group["reqResource"]["memory"],group["reqResource"]["storage"], ))
        i = i + 1 
        
    return groups
    
def printSolution(solution):
    for group in solution["groups"]:
        print "Host PM:", group.matchedPM.index
        print "VMs:", group.VMs
        print "Required resource:", group.resource
        print "Matched PM resource:", group.matchedPM.resource
        print "\n"
    print "Amount of traffic in physical network (Kbps): ", solution["traffic"]     


def getAverageSolution(pmList, vmList, distances, flow_matrix, nodes, rad, oLocation, iterNum):
    
    pTraffic = 0
    oTraffic = 0
    for i in range(iterNum):
        solution = getHungarionSolution(pmList, vmList, distances, flow_matrix, nodes, rad)
        pTraffic = pTraffic + solution["traffic"]     
        oTraffic = oTraffic + oComputeTraffic(flow_matrix, oLocation)
     
    avTraffic = {"Proposed": pTraffic/iterNum, "Original": oTraffic/iterNum, "Difference": (oTraffic/iterNum - pTraffic/iterNum)}
    
    return avTraffic 
    
def createTopMatrix(topo, topoSize, pmLocation):
    for i in range(topoSize):
        for j in range(topoSize):
            if i != j:
                topo[i][j] = 4
                
    for location in pmLocation:
        topo[location[0]][location[1]] = 2
        topo[location[1]][location[0]] = 2
        
    return topo