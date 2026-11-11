
# DAY 1: Building a simple agent loop
# No external libraries or API keys required.

orders = [
    {"order_id": 101, "country": "Australia", "amount": 1200},
    {"order_id": 102, "country": "Australia", "amount": 850},
    {"order_id": 103, "country": "New Zealand", "amount": 500},
    {"order_id": 104, "country": "Australia", "amount": 1500},
    {"order_id": 105, "country": "New Zealand", "amount": 300},
]


# -----------------------------
# 1. Define the available tools
# -----------------------------

def inspect_schema():
    """Return the available dataset columns."""
    return list(orders[0].keys())


def filter_orders(country):
    """Return orders belonging to a country."""
    return [
        order for order in orders
        if order["country"].lower() == country.lower()
    ]


def sum_revenue(rows):
    """Calculate total revenue for supplied orders."""
    return sum(order["amount"] for order in rows)


# The agent can only call tools registered here.
TOOLS = {
    "inspect_schema": inspect_schema,
    "filter_orders": filter_orders,
    "sum_revenue": sum_revenue,
}


# --------------------------------
# 2. Define the agent's decision logic
# --------------------------------

def choose_next_action(observations, target_country):

    completed_tools = {
        observation["tool"]
        for observation in observations
    }

    # First, inspect the dataset.
    if "inspect_schema" not in completed_tools:
        return {
            "tool": "inspect_schema",
            "args": {}
        }

    # Next, filter the relevant records.
    if "filter_orders" not in completed_tools:
        return {
            "tool": "filter_orders",
            "args": {"country": target_country}
        }

    # Finally, calculate revenue from the filtered records.
    if "sum_revenue" not in completed_tools:

        matching_orders = next(
            observation["result"]
            for observation in observations
            if observation["tool"] == "filter_orders"
        )

        return {
            "tool": "sum_revenue",
            "args": {"rows": matching_orders}
        }

    # No more actions are needed.
    return None


# -----------------------------
# 3. Implement the agent loop
# -----------------------------

def run_agent(goal, target_country, max_steps=5):

    observations = []

    print("GOAL:", goal)

    for step in range(1, max_steps + 1):

        action = choose_next_action(
            observations,
            target_country
        )

        # Stop when the planner has finished.
        if action is None:
            break

        tool_name = action["tool"]

        # Only registered tools are permitted.
        if tool_name not in TOOLS:
            raise ValueError(
                f"Tool is not allowed: {tool_name}"
            )

        print(f"\nStep {step}: calling {tool_name}")

        result = TOOLS[tool_name](**action["args"])

        # Save the tool result as an observation.
        observations.append({
            "tool": tool_name,
            "result": result
        })

        print("Observation:", result)

    else:
        raise RuntimeError(
            "Agent reached its maximum number of steps."
        )

    total = next(
        observation["result"]
        for observation in observations
        if observation["tool"] == "sum_revenue"
    )

    print(
        f"\nFinal answer: Total revenue for "
        f"{target_country} is {total}."
    )


# -----------------------------
# 4. Run the agent
# -----------------------------

run_agent(
    goal="Find total sales revenue for New Zealand",
    target_country="New Zealand"
)
