'''
Created on 2018. 7. 11.

@author: Jax
'''
from sklearn.metrics.pairwise import euclidean_distances
from utils import getPCA, getRadius, getCoord, getSolution, printSolution
from objects import VM, PM
import matplotlib.pylab as plt

#********************Inputs***************************************
vm = []
vm.append(VM(0, 3, 5, 100))
vm.append(VM(1, 2, 8, 120))
vm.append(VM(2, 1, 4, 90))
vm.append(VM(3, 4, 3, 80))
vm.append(VM(4, 2, 1, 70))
vm.append(VM(5, 2, 2, 170))
vm.append(VM(6, 1, 5, 80))
vm.append(VM(7, 2, 5, 80))
vm.append(VM(8, 2, 3, 150))
vm.append(VM(9, 3, 4, 80))
   
pm = []
pm.append(PM(0, 10, 20, 700))
pm.append(PM(1, 12, 23, 420))
pm.append(PM(2, 11, 27, 250))
    
nodes = {0,1,2,3,4,5,6,7,8,9}  

flow_matrix = [[  0, 307,  50, 318, 807, 443, 792,  18, 259,  52],
               [307,   0,  86, 145, 202, 709, 598, 898, 451, 918],
               [ 50,  86,   0, 221, 135, 586, 758, 219, 251, 414],
               [318, 145, 221,   0, 933, 645, 903, 715, 597,  53],
               [807, 202, 135, 933,   0, 857,  85, 607,  24, 106],
               [443, 709, 586, 645, 857,   0, 187, 364, 351, 312],
               [792, 598, 758, 903,  85, 187,   0, 142, 868, 984],
               [ 18, 898, 219, 715, 607, 364, 142,   0, 485, 672],
               [259, 451, 251, 597,  24, 351, 868, 485,   0,  15],
               [ 52, 918, 414,  53, 106, 312, 984, 672,  15,   0]]

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
