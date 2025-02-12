def training_max(one_rep_max):
    # Calculate the training max (90% of one rep max rounded to nearest 5).
    return 5 * round(one_rep_max * 0.9 / 5)
