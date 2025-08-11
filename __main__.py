"""Main file for the project"""

import time
import pandas as pd

from prepare import prepare_method

start_time = time.time()
quotes = pd.read_csv("data/quotes.csv")

# create config
config = {
    "indicators": [
        {"type": "price_chanel", "period": 30},
        {"type": "super_trend", "period": 30, "multiplier": 7},
    ],
}

# prepare and save data
prepared_quotes = prepare_method(quotes, config["indicators"])
prepared_quotes.to_csv("data/prepared_quotes.csv", index=False)


print(f"Execution time: {time.time() - start_time}")
