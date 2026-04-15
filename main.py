import json
import sys


# This function reads the JSON input file and returns the data
def load_input(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


# This function checks if the input JSON has the correct structure
def validate_input(data):
    required_keys = ["processes", "resources", "available", "max", "allocation"]

    # Check if all required keys exist
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    processes = data["processes"]
    resources = data["resources"]
    available = data["available"]
    max_matrix = data["max"]
    allocation = data["allocation"]

    # Basic validation checks
    if len(available) != resources:
        raise ValueError("Length of 'available' must match number of resources.")

    if len(max_matrix) != processes:
        raise ValueError("'max' rows must match number of processes.")

    if len(allocation) != processes:
        raise ValueError("'allocation' rows must match number of processes.")

    # Check each row length
    for row in max_matrix:
        if len(row) != resources:
            raise ValueError("Each row in 'max' must match number of resources.")

    for row in allocation:
        if len(row) != resources:
            raise ValueError("Each row in 'allocation' must match number of resources.")


# This function computes the NEED matrix using: need = max - allocation
def compute_need(max_matrix, allocation):
    processes = len(max_matrix)
    resources = len(max_matrix[0])

    need = []

    # Loop through each process and resource
    for i in range(processes):
        row = []
        for j in range(resources):
            value = max_matrix[i][j] - allocation[i][j]
            row.append(value)
        need.append(row)

    return need


# This function checks if a process can finish with current available resources
def can_finish(need_row, work):
    for j in range(len(work)):
        if need_row[j] > work[j]:
            return False  # Cannot run this process yet
    return True


# Main Banker’s Safety Algorithm
def bankers_safety(processes, available, max_matrix, allocation):
    # Step 1: Calculate NEED matrix
    need = compute_need(max_matrix, allocation)

    # Work represents available resources during simulation
    work = available[:]

    # Track which processes have finished
    finished = [False] * processes

    # Store safe sequence
    safe_sequence = []

    # Keep looping as long as we are making progress
    made_progress = True

    while made_progress:
        made_progress = False

        # Go through processes in order (tie-breaking: smallest index first)
        for i in range(processes):
            if not finished[i] and can_finish(need[i], work):

                # If process can finish, release its resources
                for j in range(len(work)):
                    work[j] += allocation[i][j]

                finished[i] = True
                safe_sequence.append(f"P{i + 1}")
                made_progress = True

    # If all processes finished → SAFE state
    if all(finished):
        return {
            "state": "SAFE",
            "safe_sequence": safe_sequence
        }

    # Otherwise → DEADLOCK
    else:
        deadlocked_processes = []

        for i in range(processes):
            if not finished[i]:
                deadlocked_processes.append(f"P{i + 1}")

        return {
            "state": "DEADLOCK",
            "deadlocked_processes": deadlocked_processes
        }


def main():
    # Make sure user provides input file
    if len(sys.argv) != 2:
        print("Usage: python3 main.py input.json", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Load and validate input
        data = load_input(input_file)
        validate_input(data)

        processes = data["processes"]
        available = data["available"]
        max_matrix = data["max"]
        allocation = data["allocation"]

        # Run Banker’s algorithm
        result = bankers_safety(processes, available, max_matrix, allocation)

        # Output result as JSON
        json.dump(result, sys.stdout, indent=2)

    except Exception as e:
        # Output error in JSON format (for debugging)
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)


# Run the program
if __name__ == "__main__":
    main()