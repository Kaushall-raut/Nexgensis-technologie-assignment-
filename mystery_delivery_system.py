import json   # module for reading and converting json 


with open('base_case.json',"r") as json_file:
    data=json.load(json_file)     # loading json file and storing it into a variable 


print(data['warehouses'][0])

