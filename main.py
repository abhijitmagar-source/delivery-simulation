import json

from utils import calculate_distance


with open("base_case.json", "r") as file:

    data = json.load(file)


warehouses = {}

for warehouse in data["warehouses"]:

    warehouses[warehouse["id"]] = (
        warehouse["location"]
    )


agents = {}

for agent in data["agents"]:

    agents[agent["id"]] = (
        agent["location"]
    )


packages = data["packages"]


report = {}

for agent_id in agents:

    report[agent_id] = {

        "packages_delivered": 0,

        "total_distance": 0
    }


def find_nearest_agent(warehouse_location):

    nearest_agent = None

    minimum_distance = float("inf")


    for agent_id, agent_location in agents.items():

        distance = calculate_distance(
            warehouse_location,
            agent_location
        )


        if distance < minimum_distance:

            minimum_distance = distance

            nearest_agent = agent_id


    return nearest_agent


for package in packages:

    warehouse_id = package["warehouse_id"]

    warehouse_location = warehouses[warehouse_id]

    destination = package["destination"]


    nearest_agent = find_nearest_agent(
        warehouse_location
    )


    agent_to_warehouse = calculate_distance(

        agents[nearest_agent],

        warehouse_location
    )


    warehouse_to_destination = calculate_distance(

        warehouse_location,

        destination
    )


    total_trip_distance = (

        agent_to_warehouse +

        warehouse_to_destination
    )


    report[nearest_agent]["packages_delivered"] += 1


    report[nearest_agent]["total_distance"] += (
        total_trip_distance
    )


for agent_id in report:

    delivered = report[agent_id]["packages_delivered"]

    distance = report[agent_id]["total_distance"]


    if delivered > 0:

        efficiency = distance / delivered

    else:

        efficiency = 0


    report[agent_id]["efficiency"] = efficiency


best_agent = min(

    report,

    key=lambda x: report[x]["efficiency"]
)


report["best_agent"] = best_agent


with open("report.json", "w") as file:

    json.dump(report, file, indent=4)


print("Simulation completed successfully.")