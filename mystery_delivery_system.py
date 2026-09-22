import json   # module for reading and converting json 
import math

with open('base_case.json',"r") as json_file:
    data=json.load(json_file)     # loading json file and storing it into a variable 




# function for calculating euclidean distance 

def euclidean_distance(point1,point2):
    distance=math.sqrt(((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2) )
    return distance

print(euclidean_distance([5,5],[0,0]))