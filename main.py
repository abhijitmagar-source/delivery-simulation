import json
from utils import calculate_distance

# reading json data
with open("base_case.json", "r") as file:
    data = json.load(file)

# creating warehouse dictionary
warehouses = {}

for warehouse in data["warehouses"]:
    warehouses[warehouse["id"]] = warehouse["location"]

# creating agents dictionary
agents = {}

for agent in data["agents"]:
    agents[agent["id"]] = agent["location"]

# getting packages list
packages = data["packages"]

# creating report dictionary
report = {}

for agent_id in agents:
    report[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0
    }

# function to find nearest agent
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

# processing all packages
for package in packages:

    warehouse_id = package["warehouse_id"]

    warehouse_location = warehouses[warehouse_id]

    destination = package["destination"]

    nearest_agent = find_nearest_agent(
        warehouse_location
    )

    # distance from agent to warehouse
    agent_to_warehouse = calculate_distance(
        agents[nearest_agent],
        warehouse_location
    )

    # distance from warehouse to destination
    warehouse_to_destination = calculate_distance(
        warehouse_location,
        destination
    )

    # total trip distance
    total_trip_distance = (
        agent_to_warehouse +
        warehouse_to_destination
    )

    # updating report
    report[nearest_agent]["packages_delivered"] += 1

    report[nearest_agent]["total_distance"] += (
        total_trip_distance
    )

# calculating efficiency
for agent_id in report:

    delivered = report[agent_id]["packages_delivered"]

    distance = report[agent_id]["total_distance"]

    if delivered > 0:
        efficiency = distance / delivered
    else:
        efficiency = 0

    report[agent_id]["efficiency"] = round(
        efficiency,
        2
    )

    report[agent_id]["total_distance"] = round(
        report[agent_id]["total_distance"],
        2
    )

# finding best agent
best_agent = min(
    report,
    key=lambda x: report[x]["efficiency"]
)

report["best_agent"] = best_agent

# writing final report
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

print("Simulation completed successfully.")