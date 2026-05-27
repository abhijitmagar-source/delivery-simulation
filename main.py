import json
from utils import calculate_distance

# Load data from JSON file
with open("base_case.json", "r") as file:
    data = json.load(file)

# Store warehouse IDs with their locations
warehouses = {}
for warehouse in data["warehouses"]:
    warehouses[warehouse["id"]] = warehouse["location"]

# Store agent IDs with their locations
agents = {}
for agent in data["agents"]:
    agents[agent["id"]] = agent["location"]

# Get all packages
packages = data["packages"]

# Initialize report for each agent
report = {}
for agent_id in agents:
    report[agent_id] = {
        "packages_delivered": 0,
        "total_distance": 0
    }

# Function to find the nearest agent to a warehouse
def find_nearest_agent(warehouse_location):
    nearest_agent = None
    minimum_distance = float("inf")

    # Compare distance of all agents
    for agent_id, agent_location in agents.items():
        distance = calculate_distance(
            warehouse_location,
            agent_location
        )

        # Update nearest agent if smaller distance found
        if distance < minimum_distance:
            minimum_distance = distance
            nearest_agent = agent_id

    return nearest_agent

# Process each package delivery
for package in packages:

    # Get warehouse and destination details
    warehouse_id = package["warehouse_id"]
    warehouse_location = warehouses[warehouse_id]
    destination = package["destination"]

    # Find nearest agent
    nearest_agent = find_nearest_agent(warehouse_location)

    # Calculate distance from agent to warehouse
    agent_to_warehouse = calculate_distance(
        agents[nearest_agent],
        warehouse_location
    )

    # Calculate distance from warehouse to destination
    warehouse_to_destination = calculate_distance(
        warehouse_location,
        destination
    )

    # Total distance traveled for delivery
    total_trip_distance = (
        agent_to_warehouse +
        warehouse_to_destination
    )

    # Update agent delivery count
    report[nearest_agent]["packages_delivered"] += 1

    # Update total distance traveled by agent
    report[nearest_agent]["total_distance"] += total_trip_distance

# Calculate efficiency for each agent
for agent_id in report:

    delivered = report[agent_id]["packages_delivered"]
    distance = report[agent_id]["total_distance"]

    # Avoid division by zero
    if delivered > 0:
        efficiency = distance / delivered
    else:
        efficiency = 0

    # Store rounded efficiency value
    report[agent_id]["efficiency"] = round(efficiency, 2)

    # Store rounded total distance
    report[agent_id]["total_distance"] = round(distance, 2)

# Find agent with best efficiency
best_agent = min(
    report,
    key=lambda x: report[x]["efficiency"]
)

# Add best agent to report
report["best_agent"] = best_agent

# Save final report to JSON file
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# Success message
print("Simulation completed successfully.")