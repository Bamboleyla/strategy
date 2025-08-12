"""Main file for the project"""

import time
import pandas as pd

from prepare import prepare_data
from calculate import calculate_data
from show import show_plot

start_time = time.time()
# quotes = pd.read_csv("data/quotes.csv")

# create config
config = {
    "indicators": [
        {"type": "price_chanel", "period": 30},
        {"type": "super_trend", "period": 30, "multiplier": 7},
    ],
}

# prepare and save data
# prepared_quotes = prepare_data(quotes, config["indicators"])
# prepared_quotes.to_csv("data/prepared_quotes.csv", index=False)

# calculate and save data
prepared_quotes = pd.read_csv("data/prepared_quotes.csv")

calculated_quotes = calculate_data(prepared_quotes, config["indicators"])
calculated_quotes.to_csv("data/calculated_quotes.csv", index=False)

show_plot(calculated_quotes, config["indicators"])

print(f"Execution time: {time.time() - start_time}")
