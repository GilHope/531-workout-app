from flask import render_template, request
from app import app
from app import config
import app.calculations as calculations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_weeks = int(request.form.get('num_weeks'))
        except (ValueError, TypeError):
            num_weeks = 4

        # Enforce week limits: must be between 4 and 20.
        if num_weeks < 4:
            num_weeks = 4
        elif num_weeks > 20:
            num_weeks = 20

        try:
            accessory_choice = int(request.form.get('accessory_choice', 0))
        except (ValueError, TypeError):
            accessory_choice = 0

        # Retrieve 1RM values for each lift.
        one_rms = {}
        for lift in config.LIFT_ORDER:
            try:
                one_rm = float(request.form.get(lift))
            except (ValueError, TypeError):
                one_rm = 100.0  # default value if conversion fails
            # Enforce weight limits: must be between 100 and 1000.
            if one_rm < 100:
                one_rm = 100
            elif one_rm > 1000:
                one_rm = 1000
            one_rms[lift] = one_rm

        # Determine if the user wants warm-up sets.
        include_warmup = True if request.form.get("include_warmup") else False

        # Generate the workout plan.
        workout_plan = calculations.generate_workout_plan(num_weeks, one_rms, accessory_choice, include_warmup)
        return render_template('results.html', workout_plan=workout_plan)
    
    # GET request: render the form.
    return render_template('index.html', lifts=config.LIFT_ORDER)

