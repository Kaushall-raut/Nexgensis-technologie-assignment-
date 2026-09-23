import json   # module for reading and converting json
import math
import random
import csv


with open('Python Assignment(Delivery System Test Cases)/test_case_1.json',"r") as json_file:

    data=json.load(json_file)     # loading json file and storing it into a variable




ENABLE_RANDOM_DELAYS = True
ENABLE_ASCII_ROUTES = True
ENABLE_MIDDAY_AGENT = True
ENABLE_CSV_EXPORT = True


# function for calculating euclidean distance

def euclidean_distance(point1,point2):

    distance=math.sqrt(((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2) )

    return distance


def nearest_Agent_finder(warehouse_location,agent):   # function agent nearest to the warehouse location

    shortest_distance=float("inf")       # assigning shortest distance infinity

    nearest_agent=None

    # agents are stored as dictionary in this test case
    for agent_id,location in agent.items():

        distance=euclidean_distance(location,warehouse_location)      #calculating euclidean distance of each agent

        if distance<shortest_distance:

            shortest_distance=distance
            nearest_agent=agent_id

    return nearest_agent


nearest_Agent_finder([95,4],data["agents"])


def get_warehouse_location(warehouse_id,warehouses):  #function for getting warehouse location

    # warehouses are stored as dictionary in this test case
    return warehouses[warehouse_id]


# location=get_warehouse_location("w2",data["warehouses"])


def package_assigner(data):    # function for assigning package

    agent_assign={}

    for package in data["packages"]:

        warehouse_id=package["warehouse"]

        warehouse_location=get_warehouse_location(
            warehouse_id,
            data["warehouses"]
        )

        nearest_Agent=nearest_Agent_finder(
            warehouse_location,
            data["agents"]
        )

        if nearest_Agent not in agent_assign:

            agent_assign[nearest_Agent]=[]

        agent_assign[nearest_Agent].append(package["id"])

    return agent_assign


agent_assign=package_assigner(data)

print("\nPackage Assignment:")
print(agent_assign)



# BONUS - RANDOM DELIVERY DELAY


def random_delivery_delay():

    return random.randint(1,10)



# BONUS - ADD NEW AGENT MID-DAY


def add_new_agent(data,current_location,agent_statistic,routes):

    new_agent_id="A5"

    # making sure the new agent does not already exist
    if new_agent_id in data["agents"]:

        new_agent_id="A6"

    new_agent_location=[20,20]

    data["agents"][new_agent_id]=new_agent_location.copy()

    current_location[new_agent_id]=new_agent_location.copy()

    agent_statistic[new_agent_id]={
        "packages_delivered":0,
        "total_distance":0
    }

    routes[new_agent_id]=[]

    print("\nNew agent joined:",new_agent_id)

    return new_agent_id


# BONUS - ASCII ROUTE VISUALIZATION


def visualize_routes(routes):

    print("\n")
    print("========================================")
    print("ASCII ROUTE VISUALIZATION")
    print("========================================")

    for agent_id,agent_routes in routes.items():

        print(f"\n{agent_id}:")

        if len(agent_routes)==0:

            print("  No packages delivered")

        else:

            for route in agent_routes:

                print(
                    f"  {agent_id} "
                    f"-> {route['warehouse']} "
                    f"-> {route['destination']} "
                    f"(Package {route['package']})"
                )


# function for exporting top performer 

def export_top_performer(report):

    best_agent=report["best_agent"]

    best_agent_data=report[best_agent]

    with open("top_performer.csv","w",newline="") as csv_file:

        writer=csv.writer(csv_file)

        writer.writerow([
            "Agent",
            "Packages Delivered",
            "Total Distance",
            "Efficiency"
        ])

        writer.writerow([
            best_agent,
            best_agent_data["packages_delivered"],
            best_agent_data["total_distance"],
            best_agent_data["efficiency"]
        ])

    print("\nTop performer exported to top_performer.csv")


# function for checking agent current location after or before delivery

def agent_current_location(data,agent_assign):

    current_location={}

    agent_statistic={}

    best_agent=None

    best_efficiency=float("inf")

    routes={}

    # agents are stored as dictionary in this test case
    for agent_id,location in data["agents"].items():

        current_location[agent_id]=location.copy()

        agent_statistic[agent_id] = {

            "packages_delivered":0,

            "total_distance":0

        }

        routes[agent_id]=[]


#    print(current_location)


    

    package_queue=[]

    for agent_id,package_ids in agent_assign.items():

        for package_id in package_ids:

            package_queue.append(
                [agent_id,package_id]
            )




    packages_before_new_agent=len(data["packages"])//2

    processed_packages=0

    new_agent_added=False



    while len(package_queue)>0:

        agent_id,package_id=package_queue.pop(0)

        for package in data["packages"]:

            if package["id"]==package_id:

                #    print(agent_id,package)

                warehouse_id=package["warehouse"]

                warehouse_location=get_warehouse_location(
                    warehouse_id,
                    data["warehouses"]
                )

                agent_current_location=current_location[agent_id]

                distance_to_warehouse=euclidean_distance(
                    agent_current_location,
                    warehouse_location
                )

                destination=package["destination"]

                distance_to_destination=euclidean_distance(
                    warehouse_location,
                    destination
                )

                #    print(agent_id,distance_to_warehouse)

                # print(agent_id, distance_to_warehouse, distance_to_destination)

                total_distance=(
                    distance_to_warehouse+
                    distance_to_destination
                )


           
                # BONUS - RANDOM DELIVERY DELAY
               

                if ENABLE_RANDOM_DELAYS:

                    delay=random_delivery_delay()

                    print(
                        f"{package_id} delivered by "
                        f"{agent_id} "
                        f"(Delay: {delay} minutes)"
                    )

                else:

                    delay=0


                agent_statistic[agent_id]["packages_delivered"]+=1

                agent_statistic[agent_id]["total_distance"]+=total_distance


               
                # BONUS problem - STORE ROUTE
               

                routes[agent_id].append({

                    "package":package_id,

                    "warehouse":warehouse_id,

                    "destination":destination.copy(),

                    "delay":delay

                })


                current_location[agent_id]=package["destination"].copy()

                processed_packages+=1


           
                # BONUS problem- NEW AGENT JOINS MID-DAY
            

                if (
                    ENABLE_MIDDAY_AGENT
                    and new_agent_added==False
                    and processed_packages>=packages_before_new_agent
                ):

                    new_agent_id=add_new_agent(
                        data,
                        current_location,
                        agent_statistic,
                        routes
                    )

                    new_agent_added=True

                    remaining_packages=[]

                    for item in package_queue:

                        remaining_packages.append(item[1])


                    # remove old remaining assignments
                    package_queue=[]


                    # reassign remaining packages
                    for remaining_package_id in remaining_packages:

                        for remaining_package in data["packages"]:

                            if remaining_package["id"]==remaining_package_id:

                                remaining_warehouse_id=(
                                    remaining_package["warehouse"]
                                )

                                remaining_warehouse_location=(
                                    get_warehouse_location(
                                        remaining_warehouse_id,
                                        data["warehouses"]
                                    )
                                )

                                # finding nearest agent using
                                # current agent locations
                                nearest_agent=nearest_Agent_finder(
                                    remaining_warehouse_location,
                                    current_location
                                )

                                package_queue.append([
                                    nearest_agent,
                                    remaining_package_id
                                ])

                                break


                # package found, so stop searching
                break


   # calculating efficiency

    for agent_id,details in agent_statistic.items():

        packages=details["packages_delivered"]

        distance=details["total_distance"]

        if packages>0:

            efficiency=distance/packages

        else:

            efficiency=0

        details["efficiency"]=efficiency


        # agents with zero packages should not
        # become the best agent

        if packages>0:

            if efficiency<best_efficiency:

                best_efficiency=efficiency

                best_agent=agent_id


    agent_statistic["best_agent"]=best_agent

    return agent_statistic,routes


# generating report 

report,routes=agent_current_location(
    data,
    agent_assign
)

# saving report 

with open("report.json","w") as file:

    json.dump(
        report,
        file,
        indent=4
    )


# printing report 

print("\n")
print("========================================")
print("FINAL REPORT")
print("========================================")

print(
    json.dumps(
        report,
        indent=4
    )
)


if ENABLE_ASCII_ROUTES:

    visualize_routes(routes)



if ENABLE_CSV_EXPORT:

    export_top_performer(report)  # exporting csv file