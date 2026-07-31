def calculate_reward(weight_kg: float) -> int:
    return max(1, int(weight_kg * 10))
