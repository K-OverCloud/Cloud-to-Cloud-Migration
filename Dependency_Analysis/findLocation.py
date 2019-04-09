'''
Created on 2018. 7. 11.

@author: Jax
'''
from sklearn.metrics.pairwise import euclidean_distances
from utils import getPCA, getRadius, getCoord, getSolution, printSolution
from objects import VM, PM
import matplotlib.pylab as plt

#**********************Set Input*************************************
vm = []
pm = []
nodes = {}  
flow_matrix = []

#**********************************************************************

if __name__== '__main__':

    matrix = getPCA(flow_matrix, 2)
    coord = getCoord(matrix)
    rad = getRadius(matrix, len(pm))
    distances = euclidean_distances(coord, coord)   
      
    for i in range(len(vm)):
        vm[i].setCoord(coord[i])
        vm[i].setDistance(distances[i])
      
    solution = getSolution(pm, vm, distances, flow_matrix, nodes, rad)
         
    printSolution(solution)    
     
    #Plotting nodes
    plt.scatter(matrix[0], matrix[1], s=500)
    
    labels = ['VM{0}'.format(i) for i in range(len(nodes))]
    for label, x, y in zip(labels, matrix[0], matrix[1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3, rad=0'))
   
    plt.show()
