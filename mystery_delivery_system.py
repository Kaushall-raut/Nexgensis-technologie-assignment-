import json   # module for reading and converting json 
import math

with open('base_case.json',"r") as json_file:
    data=json.load(json_file)     # loading json file and storing it into a variable 




# function for calculating euclidean distance 

def euclidean_distance(point1,point2):
    distance=math.sqrt(((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2) )
    return distance




def nearest_Agent_finder(warehouse_location,agent):   # function agent nearest to the warehouse location
   shortest_distance=float("inf")       # assigning shortest distance infinity
   nearest_agent=None                       
   for i  in agent:
   
    distance=euclidean_distance(i["location"],warehouse_location)      #calculating euclidean distance of each agent
    if distance<shortest_distance:
       shortest_distance=distance
       nearest_agent=i["id"]
   return nearest_agent
                                                        

nearest_Agent_finder([50,75],data["agents"])


def get_warehouse_location(warehouse_id,warehouses):  #function for getting warehouse location
   
   for i in warehouses:
    if warehouse_id.upper()==i["id"]:
      return i["location"]


# location=get_warehouse_location("w2",data["warehouses"])

def package_assigner(data):    # function for assigning package
    
    for package in data["packages"]:
       warehouse_id=package["warehouse_id"]

       warehouse_location=get_warehouse_location(warehouse_id,data["warehouses"])
       nearest_Agent=nearest_Agent_finder(warehouse_location,data["agents"])
       print(nearest_Agent)


package_assigner(data)