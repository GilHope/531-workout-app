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

def generate_workout_plan(num_weeks, one_rms, accessory_choice):
    """
    Generate the workout plan.
      - num_weeks: number of weeks requested.
      - one_rms: dict mapping lift names to one rep maxes.
      - accessory_choice: 0,1,2, or 3.
    
    Returns a dict where each week (key) maps to a dict of lifts and their workouts.
    """
    # Initialize training maxes for each lift.
    training_maxes = {}
    for lift, one_rm in one_rms.items():
        training_maxes[lift] = calculate_training_max(one_rm)

    # Define the four main 5/3/1 schemes.
    schemes = ["5/5/5", "3/3/3", "5/3/1", "deload"]
    program = {
        "5/5/5": {
            "reps": [5, 5, 5],
            "percentages": [0.65, 0.75, 0.85]
        },
        "3/3/3": {
            "reps": [3, 3, 3],
            "percentages": [0.70, 0.80, 0.90]
        },
        "5/3/1": {
            "reps": [5, 3, 1],
            "percentages": [0.75, 0.85, 0.95]
        },
        "deload": {
            "reps": [5, 5, 5],
            "percentages": [0.40, 0.50, 0.60]
        }
    }

    workout_plan = {}

    lifts = config.LIFT_ORDER

    for week in range(1, num_weeks + 1):
        week_plan = {}
        for i, lift in enumerate(lifts):
            scheme_index = (i - (week - 1)) % 4
            scheme_name = schemes[scheme_index]
            scheme = program[scheme_name]
            main_sets = calculate_main_sets(training_maxes[lift], scheme)
            accessory = ""
            if accessory_choice in [1, 2, 3]:
                accessory = calculate_accessory(accessory_choice, training_maxes[lift], main_sets)
            week_plan[lift] = {
                "scheme": scheme_name,
                "main_sets": main_sets,
                "accessory": accessory
            }
        workout_plan[week] = week_plan

        # End of 4-week cycle: update training maxes if there are more weeks.
        if week % 4 == 0 and week < num_weeks:
            for lift in training_maxes:
                if lift in ["Bench", "OHP"]:
                    training_maxes[lift] += 5
                elif lift in ["Squat", "Deadlift"]:
                    training_maxes[lift] += 10
    return workout_plan
