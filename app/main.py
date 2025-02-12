import config

def round_to_nearest_5(weight):
    """Round a number to the nearest 5."""
    return int(round(weight / 5.0)) * 5

def main():
    # Use the lift order from config.py
    lifts = config.LIFT_ORDER

    # Get the 1RM for each lift and calculate the training max
    # using the multiplier from config.py
    print("Enter your 1RM for each lift (numbers only):")
    one_rep_maxes = {}
    training_maxes = {}
    for lift in lifts:
        one_rm = float(input(f"  {lift} 1RM: "))
        one_rep_maxes[lift] = one_rm
        # Use the multiplier from config.py (e.g., 0.9)
        tm = one_rm * config.TRAINING_MAX_MULTIPLIER
        training_maxes[lift] = tm
        print(f"  {lift} Training Max (90% of 1RM): {tm:.2f}")

    # Choose an accessory protocol.
    print("\nSelect an accessory protocol:")
    print("  0: None")
    print("  1: Boring But Big (5 sets of 10 x 50% of training max)")
    print("  2: First Set Last (repeat the first main set)")
    print("  3: Pyramid (2 sets: 1st = second main set, 2nd = first main set)")
    try:
        accessory_choice = int(input("Enter your choice (0, 1, 2, or 3): "))
    except ValueError:
        print("Invalid input. Defaulting to no accessory work.")
        accessory_choice = 0

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

    # Number of weeks in the cycle.
    num_weeks = 4
    print("\nYour 5/3/1 Cycle:\n")
    
    # For each week...
    for week in range(1, num_weeks + 1):
        print(f"Week {week}:")
        # For each lift (in the order defined in config.py)
        for i, lift in enumerate(lifts):
            # Rotate the scheme assignment across the 4-week cycle.
            scheme_index = (i - (week - 1)) % 4
            scheme = schemes[scheme_index]
            reps = program[scheme]["reps"]
            percentages = program[scheme]["percentages"]

            # Calculate the main working sets.
            main_sets = []
            for rep, pct in zip(reps, percentages):
                weight = training_maxes[lift] * pct
                weight = round_to_nearest_5(weight)
                main_sets.append(f"{rep} x {weight}")

            # Print the main sets.
            print(f"  {lift}: " + ", ".join(main_sets))
            
            # Add accessory work if selected.
            if accessory_choice == 1:
                # Boring But Big: 5 sets of 10 at 50% of the training max.
                bbb_weight = round_to_nearest_5(training_maxes[lift] * 0.50)
                print(f"    Accessory (Boring But Big): 5 sets of 10 x {bbb_weight}")
            elif accessory_choice == 2:
                # First Set Last: Repeat the first main working set exactly.
                print(f"    Accessory (First Set Last): {main_sets[0]}")
            elif accessory_choice == 3:
                # Pyramid: 2 sets.
                # First pyramid set is the same as the second main set.
                # Second pyramid set is the same as the first main set.
                pyramid_set_1 = main_sets[1]
                pyramid_set_2 = main_sets[0]
                print("    Accessory (Pyramid): " + pyramid_set_1 + " then " + pyramid_set_2)
        print()  # Blank line after each week

if __name__ == "__main__":
    main()
