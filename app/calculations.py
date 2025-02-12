import config

def round_to_nearest_5(weight):
    """Round a weight value to the nearest 5."""
    return int(round(weight / 5.0)) * 5

def calculate_training_max(one_rm):
    """
    Calculate the training max given a one-rep max.
    Uses the multiplier from config.py.
    """
    return one_rm * config.TRAINING_MAX_MULTIPLIER

def calculate_main_sets(training_max, scheme):
    """
    Calculate main working sets for a given training max and scheme.
    'scheme' should be a dict with keys 'reps' and 'percentages'.
    """
    sets = []
    for rep, pct in zip(scheme["reps"], scheme["percentages"]):
        weight = round_to_nearest_5(training_max * pct)
        sets.append(f"{rep} x {weight}")
    return sets

def calculate_accessory(accessory_choice, training_max, main_sets):
    """
    Generate accessory work output based on the accessory_choice:
      1 -> Boring But Big (5 sets of 10 at 50% of training max)
      2 -> First Set Last (repeat the first main set)
      3 -> Pyramid (2 sets: 1st = second main set, 2nd = first main set)
    """
    if accessory_choice == 1:
        weight = round_to_nearest_5(training_max * 0.50)
        return f"Accessory (Boring But Big): 5 sets of 10 x {weight}"
    elif accessory_choice == 2:
        return f"Accessory (First Set Last): {main_sets[0]}"
    elif accessory_choice == 3:
        return f"Accessory (Pyramid): {main_sets[1]} then {main_sets[0]}"
    else:
        return ""
