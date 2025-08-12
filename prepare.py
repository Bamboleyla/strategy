"""
This module contains the prepare method for the new_terminal.
"""

import pandas as pd
from myLib.indicators import price_chanel, super_trend


def prepare_data(quotes: pd.DataFrame, indicators) -> pd.DataFrame:
    new_quotes = quotes.copy()
    # We remove the lines with the same values ​​in the columns Open, High, Low, Close
    new_quotes = new_quotes[
        ~(
            (new_quotes["OPEN"] == new_quotes["CLOSE"])
            & (new_quotes["OPEN"] == new_quotes["HIGH"])
            & (new_quotes["OPEN"] == new_quotes["LOW"])
        )
    ]
    new_quotes = new_quotes.reset_index(drop=True)

    for indicator in indicators:
        if indicator["type"] == "price_chanel":
            new_quotes = price_chanel(df=new_quotes, period=indicator["period"])
        elif indicator["type"] == "super_trend":
            new_quotes = super_trend(
                df=new_quotes,
                config=[
                    {
                        "period": indicator["period"],
                        "multiplier": indicator["multiplier"],
                    }
                ],
            )
        else:
            raise ValueError("Indicator type is not supported")

    return new_quotes
