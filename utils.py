def get_indicators_colums(indicators):
    pc_period = indicators[0]["period"]
    st_period = indicators[1]["period"]
    st_multiplier = indicators[1]["multiplier"]

    # Generation of names of columns
    pc_high = f"PC_{pc_period}_HIGH"
    pc_low = f"PC_{pc_period}_LOW"
    pc_mid = f"PC_{pc_period}_MID"
    st_upper = f"ST_UPPER_{st_period}_{st_multiplier}"
    st_lower = f"ST_LOWER_{st_period}_{st_multiplier}"

    return pc_high, pc_low, pc_mid, st_upper, st_lower
