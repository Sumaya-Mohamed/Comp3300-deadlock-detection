# COMP3300 Deadlock Detection (Banker's Safety Algorithm) Winter 2026

## Group Members: Zahra Elahi, Sumaya Mohamed, Lindsay Torres 

### Project Description

Deadlock is a reoccurring issue seen in various operating systems where two processes are permanently locked from further execution because each one is waiting for resources from the other. Applications and systems tend to degrade dramatically once stuck in a deadlock as a result from overhead and other factors. This program utilizes the Banker's Safe Algorithm in Python and JSON, aiming to provide insight of the implementation for how operating systems detect deadlocks.

### Design Decisions

Our program includes multiple modular functions to promote readibility, ease of use, and to break down a complex program into independent functions. Some notable modular functions implemented for this project include the following: 

```
## def validate_input(data)
## compute_need(max_matrix, allocation)
## can_finish(need_row, work)
```

These methods exist to simplify the source code so less bloating occurs to accelerate development. 

The actual Banker's Safety Algorithm is implented in ```def bankers_safety(..)```, where it follows the general framework provided by the requirements in the assignment guidelines. At the start of the function, we begin by computing the need matrix.

```
def bankers_safety(processes, available, max_matrix, allocation):
    need = compute_need(max_matrix, allocation)
        ...
```

This is done by a helper function to reduce complexity in code logic.

```
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
```

It calculates the need matrix using need = max - allocation and returns the matrix to the caller. 

From there, the method uses a while loop that runs as long as at least one process was able to finish in the previous iteration. It iterates through each process and performs a deterministic safety check because of this condition implemented in the loop: 

``` if not finished[i] and can_finish(need[i], work): ```

This condition is where the algorithm decides whether it is safe for this process to run right now, given that it has not already finished and its remaining needs can be satisfied by current resources. It's deterministic because there is no variability between these condition checks, all of the processes are checked in the same order and the ```can_finish(need[i],work)``` returns whether the process can run or not. 

Finally, it outputs whether all of the processes had finished executing in an if-else condition.

```
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

```

Where an array called ```finished``` holds a boolean value of whether the process finished executing or if they are stuck in deadlock.

### Tie-Breaking Policy 

The Tie-Breaking Policy defines how to choose between mutually acceptable options. For the Banker's Safety Algorithm, a "mutually acceptable option" is denoted by whether multiple processes can safely run (need <= available) and becomes a question of which process should be ran first. 

Thus, the workaround for this suggests that the smallest process index runs first. In our program, this is reinforced by:

```hile made_progress:
        made_progress = False

        # Go through processes in order (tie-breaking: smallest index first)
        for i in range(processes):

                ...
```

It repeatedly re-scans through a fixed-list of processes ```P1 -> P2 -> P3 -> ...``` where it selects the first valid process encountered. Afterwards, it updates available resources each time a process completes until no process in a full scan can make progress. 

Therefore, when multiple processes are eligible to execute, the method selects the first one in index order based on a repeated number of scans in the process list. 

### AI Usage 
AI Tools were used to gain deeper understanding of the Banker's Safety Algorithm as a concept,its reasoning for why its implemented in such a way and to debug the source code when compiler issues were presented. 

The source code was implemented by the developer's own creative thinking, application of knowledge and design.