from typing import List, Tuple, NamedTuple

# Item structure similar to the C++ struct in algorithms.h
class Item(NamedTuple):
    weight: int
    value: int
    ratio: float

def solve_backtracking(capacity: int, weights: List[int], values: List[int]) -> Tuple[int, List[int]]:
    """
    Solves the 0/1 Knapsack problem using a backtracking approach with pruning.
    
    Args:
        capacity: The maximum weight capacity of the knapsack.
        weights: List of weights for each item.
        values: List of values for each item.
        
    Returns:
        A tuple containing (best_value, best_selection_indices).
    """
    
    # Input validation
    if len(weights) != len(values):
        raise ValueError("Weights and values sizes must match")
    if capacity <= 0:
        raise ValueError("Capacity must be positive")
    
    # Prepare items list
    items = []
    for w, v in zip(weights, values):
        if w <= 0 or v <= 0:
            raise ValueError("Weights and values must be positive")
        items.append(Item(weight=w, value=v, ratio=v / w))
    
    # Sort items by value/weight ratio for better pruning (descending order)
    # Note: This changes the indices relative to the original input.
    # The returned indices will refer to this sorted list, matching the C++ logic.
    items.sort(key=lambda x: x.ratio, reverse=True)
    
    # State variables to track the best solution found so far
    # Using a mutable container (class or dict) or nonlocal variables allows the recursive function to update them.
    state = {
        "best_value": 0,
        "best_selection": [],
        "node_count": 0
    }
    
    def backtrack(index: int, current_weight: int, current_value: int, current_selection: List[int]):
        state["node_count"] += 1  # Increment node count for performance analysis
        
        # Prune by infeasibility - if current weight exceeds capacity
        if current_weight > capacity:
            return
        
        # Prune by optimality - upper bound check
        # Calculate the sum of values of all remaining items to see if we can possibly beat the best_value
        remaining_value = sum(item.value for item in items[index:])
        
        if current_value + remaining_value <= state["best_value"]:
            return
        
        # Base case - all items processed
        if index == len(items):
            if current_value > state["best_value"]:
                state["best_value"] = current_value
                state["best_selection"] = list(current_selection) # Create a copy
            return
        
        # Recursive Step 1: Include current item if feasible
        item = items[index]
        if current_weight + item.weight <= capacity:
            current_selection.append(index)
            backtrack(index + 1, 
                     current_weight + item.weight, 
                     current_value + item.value, 
                     current_selection)
            current_selection.pop() # Backtrack
        
        # Recursive Step 2: Exclude current item
        backtrack(index + 1, 
                 current_weight, 
                 current_value, 
                 current_selection)

    # Start backtracking
    initial_selection = []
    backtrack(0, 0, 0, initial_selection)
    
    # Sort selected items for consistent output
    state["best_selection"].sort()
    
    return state["best_value"], state["best_selection"]

# Example usage block to demonstrate functionality
if __name__ == "__main__":
    try:
        cap = 50
        w = [10, 20, 30]
        v = [60, 100, 120]
        best_val, best_sel = solve_backtracking(cap, w, v)
        print(f"Best Value: {best_val}")
        print(f"Selected Item Indices (sorted by ratio): {best_sel}")
    except ValueError as e:
        print(f"Error: {e}")