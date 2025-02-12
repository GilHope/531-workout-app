# main.py
import config
import calculations

def main():
    # Use the lift order from config.py
    lifts = config.LIFT_ORDER

    # Ask the user for the number of weeks to calculate for.
    try:
        num_weeks = int(input("Enter the number of weeks to calculate for: "))
    except ValueError:
        print("Invalid input. Defaulting to 4 weeks.")
        num_weeks = 4

    # Get the 1RM for each lift and calculate the initial training max.
    print("\nEnter your 1RM for each lift (numbers only):")
    training_maxes = {}
    for lift in lifts:
        try:
            one_rm = float(input(f"  {lift} 1RM: "))
        except ValueError:
            print("Invalid number entered. Defaulting to 0.")
            one_rm = 0.0
        tm = calculations.calculate_training_max(one_rm)
        training_maxes[lift] = tm
        print(f"  {lift} Training Max ({config.TRAINING_MAX_MULTIPLIER*100:.0f}% of 1RM): {tm:.2f}")

    # Choose an accessory protocol.
    print("\nSelect an accessory protocol:")
    print("  0: None")
    print("  1: Boring But Big (5 sets of 10 at 50% of training max)")
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

    print("\nYour 5/3/1 Cycle:\n")
    # Loop for each week as specified by the user.
    for week in range(1, num_weeks + 1):
        print(f"Week {week}:")
        for i, lift in enumerate(lifts):
            # Rotate the scheme assignment across the weeks.
            scheme_index = (i - (week - 1)) % 4
            scheme_name = schemes[scheme_index]
            scheme = program[scheme_name]
            
            # Calculate the main working sets.
            main_sets = calculations.calculate_main_sets(training_maxes[lift], scheme)
            print(f"  {lift}: " + ", ".join(main_sets))
            
            # Add accessory work if selected.
            if accessory_choice in [1, 2, 3]:
                accessory_text = calculations.calculate_accessory(accessory_choice, training_maxes[lift], main_sets)
                print("    " + accessory_text)
        print()  # Blank line after each week

        # If we've completed a 4-week cycle and there are more weeks to go,
        # update the training maxes for the next cycle.
        if week % 4 == 0 and week < num_weeks:
            for lift in training_maxes:
                if lift in ["Bench", "OHP"]:
                    training_maxes[lift] += 5
                elif lift in ["Squat", "Deadlift"]:
                    training_maxes[lift] += 10
            print("Cycle complete. Training maxes have been increased for the next cycle.\n")

if __name__ == "__main__":
    main()
