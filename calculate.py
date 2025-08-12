import pandas as pd
import numpy as np
from utils import get_indicators_colums
from tqdm import tqdm


def calculate_data(data: pd.DataFrame, indicators: list[dict]) -> pd.DataFrame:
    # Initialize columns
    cols_to_init = [
        "BUY_PRICE",  # buy price position
        "SELL_PRICE",  # sell price position
        "SL_PRICE",  # stop loss price
        "TP_PRICE",  # take profit price
        "COMMISSION",  # commission for one action
        "EQUITY",  # equity
        "POSITION",  # position size
        "TRADE_RESULT",  # trade result
    ]

    for col in cols_to_init:
        data[col] = np.nan

    pc_high, pc_low, pc_mid, st_upper, st_lower = get_indicators_colums(
        indicators
    )  # Take names colums from indicators data

    # add prev data columns
    prev_pc_low_col = f"prev_{pc_low}"
    prev_pc_high_col = f"prev_{pc_high}"
    prev_st_lower_col = f"prev_{st_lower}"

    data[prev_pc_low_col] = data[pc_low].shift(1)
    data[prev_pc_high_col] = data[pc_high].shift(1)
    data[prev_st_lower_col] = data[st_lower].shift(1)

    data["DATE"] = pd.to_datetime(data["DATE"])
    open_time = pd.Timestamp("07:00:00").time()
    close_time = pd.Timestamp("23:00:00").time()
    stop_time = pd.Timestamp("23:40:00").time()

    # init state
    trade_balance = 0
    position = 0
    equity = 0
    position_price = None
    take_profit = None
    stop_loss = None

    for i in tqdm(data.index, desc="Processing data"):
        # check worktime conditions
        if data.loc[i, "DATE"].time() < open_time:
            continue
        if position == 0:
            if (
                data.loc[i, st_lower] is not None
                and data.loc[i, pc_low] > data.loc[i, st_lower]
            ):
                price = round(
                    ((data.loc[i, pc_high] - data.loc[i, st_lower]) / 3)
                    + data.loc[i, st_lower],
                    2,
                )
                if (
                    data.loc[i, "LOW"] < price
                    and data.loc[i, "DATE"].time() < close_time
                ):
                    position_price = price
                    position = 1
                    stop_loss = round(data.loc[i, st_lower], 3)
                    take_profit = round(data.loc[i, pc_high], 3)
                    commission = round(position_price * 0.0005, 2)
                    trade_balance -= position_price - commission

                    data.loc[i, "BUY_PRICE"] = position_price
                    data.loc[i, "SL_PRICE"] = stop_loss
                    data.loc[i, "TP_PRICE"] = take_profit
                    data.loc[i, "COMMISSION"] = commission
                    data.loc[i, "POSITION"] = position

        elif position > 0:
            if data.loc[i, "HIGH"] > take_profit:
                position = 0
                stop_loss = None
                commission = round(take_profit * 0.0005, 2)
                equity += round(trade_balance + take_profit - commission, 2)
                trade_balance = 0
                data.loc[i, "SELL_PRICE"] = take_profit
                take_profit = None
                data.loc[i, "COMMISSION"] = commission
                data.loc[i, "POSITION"] = position
                data.loc[i, "EQUITY"] = equity
            elif (
                data.loc[i, "DATE"].time() == stop_time or data.loc[i, st_lower] is None
            ):
                position = 0
                stop_loss = None
                take_profit = None
                commission = round(data.loc[i, "OPEN"] * 0.0005, 2)
                equity += round(trade_balance + data.loc[i, "OPEN"] - commission, 2)
                trade_balance = 0
                data.loc[i, "SELL_PRICE"] = data.loc[i, "OPEN"]
                data.loc[i, "COMMISSION"] = commission
                data.loc[i, "POSITION"] = position
                data.loc[i, "EQUITY"] = equity
            elif data.loc[i, "LOW"] < stop_loss:
                position = 0
                commission = round(stop_loss * 0.0005, 2)
                equity += round(trade_balance + stop_loss - commission, 2)
                trade_balance = 0
                data.loc[i, "SELL_PRICE"] = stop_loss
                stop_loss = None
                take_profit = None
                data.loc[i, "COMMISSION"] = commission
                data.loc[i, "POSITION"] = position
                data.loc[i, "EQUITY"] = equity
            else:
                if take_profit != data.loc[i, pc_high]:
                    take_profit = data.loc[i, pc_high]
                if stop_loss != data.loc[i, st_lower]:
                    stop_loss = data.loc[i, st_lower]
                data.loc[i, "SL_PRICE"] = stop_loss
                data.loc[i, "TP_PRICE"] = take_profit

    return data
