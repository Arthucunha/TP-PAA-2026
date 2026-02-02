from typing import List, Tuple, NamedTuple

# Item structure
class Item(NamedTuple):
    weight: int
    volume: int
    value: int
    ratio: float


def solve_backtracking_2d(
    max_weight: int,
    max_volume: int,
    weights: List[int],
    volumes: List[int],
    values: List[int]
) -> Tuple[int, List[int]]:
    """
    Solves the 0/1 Knapsack problem with TWO constraints (weight + volume)
    using backtracking with pruning.

    Returns:
        (best_value, best_selection_indices)
    """

    if not (len(weights) == len(volumes) == len(values)):
        raise ValueError("weights, volumes and values must have same size")

    if max_weight <= 0 or max_volume <= 0:
        raise ValueError("Capacities must be positive")

    # Build item list
    items = []
    for w, vol, val in zip(weights, volumes, values):
        if w <= 0 or vol <= 0 or val <= 0:
            raise ValueError("Weights, volumes and values must be positive")

        # Heuristic ratio: value per (weight + volume)
        items.append(
            Item(
                weight=w,
                volume=vol,
                value=val,
                ratio=val / (w + vol)
            )
        )

    # Sort for better pruning
    items.sort(key=lambda x: x.ratio, reverse=True)

    state = {
        "best_value": 0,
        "best_selection": [],
        "node_count": 0
    }

    def backtrack(
        index: int,
        current_weight: int,
        current_volume: int,
        current_value: int,
        current_selection: List[int]
    ):
        state["node_count"] += 1

        # Infeasibility pruning
        if current_weight > max_weight or current_volume > max_volume:
            return

        # Upper bound pruning (simple but correct)
        remaining_value = sum(item.value for item in items[index:])
        if current_value + remaining_value <= state["best_value"]:
            return

        # Leaf node
        if index == len(items):
            if current_value > state["best_value"]:
                state["best_value"] = current_value
                state["best_selection"] = list(current_selection)
            return

        item = items[index]

        # Include item
        current_selection.append(index)
        backtrack(
            index + 1,
            current_weight + item.weight,
            current_volume + item.volume,
            current_value + item.value,
            current_selection
        )
        current_selection.pop()

        # Exclude item
        backtrack(
            index + 1,
            current_weight,
            current_volume,
            current_value,
            current_selection
        )

    backtrack(0, 0, 0, 0, [])

    state["best_selection"].sort()
    return state["best_value"], state["best_selection"]


# Example usage
if __name__ == "__main__":
    W = 50
    V = 60

    weights = [10, 20, 30]
    volumes = [20, 25, 30]
    values = [60, 100, 120]

    best_val, best_sel = solve_backtracking_2d(
        W, V, weights, volumes, values
    )

    print("Best value:", best_val)
    print("Selected indices (sorted by ratio order):", best_sel)
