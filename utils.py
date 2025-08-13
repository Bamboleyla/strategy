import pandas as pd


def get_indicators_colums(indicators: dict):
    """
    Generate names of columns for Price Chanel and Super Trend indicators.

    Parameters
    ----------
    indicators : list of dict
        List of indicators with parameters. The first element is for Price Chanel,
        the second for Super Trend.

    Returns
    -------
    tuple of str
        Names of columns in the following order: Price Chanel high, low, mid, Super Trend upper, lower.

    Examples
    --------
    >>> get_indicators_colums([{"type": "price_chanel", "period": 30}, {"type": "super_trend", "period": 30, "multiplier": 7}])
    ('PC_30_HIGH', 'PC_30_LOW', 'PC_30_MID', 'ST_UPPER_30_7', 'ST_LOWER_30_7')
    """
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


def resample_dataframe(df: pd.DataFrame, timeframe_multiplier: int):

    df["DATE"] = pd.to_datetime(df["DATE"])

    df.set_index("DATE", inplace=True)

    new_timeframe = f"{5 * timeframe_multiplier}min"

    # Агрегируем данные
    resampled_df = df.resample(new_timeframe).agg(
        {
            "OPEN": "first",
            "HIGH": "max",
            "LOW": "min",
            "CLOSE": "last",
            "VOLUME": "sum",
            "TICKER": "first",
        }
    )

    resampled_df.reset_index(inplace=True)
    resampled_df = resampled_df[resampled_df["VOLUME"] != 0]

    return resampled_df
