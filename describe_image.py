import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy
#imread is a function to read a image
img = plt.imread('Fig_Tree.jpg')
width = img.shape[0]
height = img.shape[1]
#Reshape turn into a matrix with a new shape [[ [1,2,3 ] , [4,5,6] , [7,8,9]  ] , [ [ ] , [ ] , [ ]  ]] to  (2D)[ [ ] , [ ] , [ ]  ]
#print(img.shape) # >>> (1000, 750, 3)
img = img.reshape(width * height,3) 
#print(img.shape) # >>> (750000, 3)

kmeans = KMeans(n_clusters = 15).fit(img)

labels = kmeans.predict(img) #Like 
#Four colors averages in the image
clusters = kmeans.cluster_centers_  

#Create a image new all white white same size with img
#img2 = numpy.zeros_like(img)

img2 = numpy.zeros((width,height,3), dtype = numpy.uint8)

index = 0
for i in range(width):
    for j in range(height):
        label_of_pixel = labels[index]
        img2[i][j] = clusters[label_of_pixel]
        index += 1
# for i in range(len(img2)):
#         img2[i] = clusters[labels[i]]

img2 = img2.reshape(width,height,3)

matplotlib.pyplot.imshow(img2)

matplotlib.pyplot.show()
#print(clusters)