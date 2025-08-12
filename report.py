import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter


def report_method(data: pd.DataFrame) -> None:
    """Generate a trading strategy performance report with visualizations"""
    # Fill position values
    data["POSITION"] = data["POSITION"].ffill().fillna(0)

    # Create SELL_PRICE from ST/SL/TP prices
    data["SELL_PRICE"] = (
        data["ST_PRICE"].combine_first(data["SL_PRICE"]).combine_first(data["TP_PRICE"])
    )

    # Initialize trade profit column
    data["TRADE_PROFIT"] = np.nan

    # Calculate trade profit for each trade
    last_buy_price = None
    last_buy_commission = None

    for i in data.index:
        if not pd.isna(data.at[i, "BUY_PRICE"]):
            last_buy_price = data.at[i, "BUY_PRICE"]
            last_buy_commission = data.at[i, "COMMISSION"]
        elif not pd.isna(data.at[i, "SELL_PRICE"]):
            if last_buy_price is not None:
                sell_price = data.at[i, "SELL_PRICE"]
                sell_commission = data.at[i, "COMMISSION"]
                # Calculate profit: (sell - buy) - (buy_commission + sell_commission)
                profit = (sell_price - last_buy_price) - (
                    last_buy_commission + sell_commission
                )
                data.at[i, "TRADE_PROFIT"] = profit
                last_buy_price = None
                last_buy_commission = None

    # Use existing EQUITY for cumulative profit (forward fill)
    data["CUMULATIVE_PROFIT"] = data["EQUITY"].ffill().fillna(0)

    # Create detailed signal type
    data["SIGNAL_TYPE"] = np.nan
    data.loc[data["BUY_PRICE"].notna(), "SIGNAL_TYPE"] = "BUY"
    data.loc[data["SL_PRICE"].notna(), "SIGNAL_TYPE"] = "STOP_LOSS"
    data.loc[data["TP_PRICE"].notna(), "SIGNAL_TYPE"] = "TAKE_PROFIT"
    data.loc[data["ST_PRICE"].notna(), "SIGNAL_TYPE"] = "STOP_TIME"

    # Filter only rows with trades
    trades = data.dropna(subset=["SIGNAL_TYPE"]).copy()

    # Calculate buy-and-hold strategy return
    first_open = data["OPEN"].iloc[0]
    last_close = data["CLOSE"].iloc[-1]
    buy_hold_profit = last_close - first_open

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # Trading strategy profit plot
    ax.step(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        "b-",
        where="post",
        linewidth=2,
        label="Trading strategy",
    )

    # Fill for positive and negative values
    ax.fill_between(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        0,
        where=(data["CUMULATIVE_PROFIT"] >= 0),
        facecolor="green",
        alpha=0.3,
        step="post",
    )
    ax.fill_between(
        data["DATE"],
        data["CUMULATIVE_PROFIT"],
        0,
        where=(data["CUMULATIVE_PROFIT"] <= 0),
        facecolor="red",
        alpha=0.3,
        step="post",
    )

    # Zero level line
    ax.axhline(0, color="black", linestyle="-", linewidth=1)

    # Buy-and-hold plot
    ax.plot(
        [data["DATE"].iloc[0], data["DATE"].iloc[-1]],
        [0, buy_hold_profit],
        "r--",
        linewidth=2,
        label="Buy & Hold (1 share)",
    )

    # Date format settings
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)

    # Axis and legend settings
    ax.set_xlabel("Date")
    ax.set_ylabel("Profit/Loss")
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.legend()
    ax.grid(True)
    ax.set_title("Strategy Performance Comparison")

    plt.tight_layout()
    plt.show()

    # Signal statistics
    signal_counts = trades["SIGNAL_TYPE"].value_counts()

    # Calculate trade statistics
    trade_results = data.dropna(subset=["TRADE_PROFIT"]).copy()
    profitable = (trade_results["TRADE_PROFIT"] > 0).sum()
    unprofitable = (trade_results["TRADE_PROFIT"] <= 0).sum()
    total_trades = profitable + unprofitable
    win_rate = (profitable / total_trades * 100) if total_trades > 0 else 0

    # Final balance (last non-null EQUITY value)
    total_balance = (
        data["EQUITY"].dropna().iloc[-1] if not data["EQUITY"].dropna().empty else 0
    )

    # Print statistics
    print("\nTrade Statistics:")
    print("=" * 40)
    print(f"Signal counts:")
    for signal, count in signal_counts.items():
        print(f"- {signal}: {count}")

    print("\nTrade Results:")
    print(f"- Profitable trades: {profitable}")
    print(f"- Unprofitable trades: {unprofitable}")
    print(f"- Win Rate: {win_rate:.2f}%")
    print(f"- Final balance: {total_balance:.2f}")
    print("=" * 40)
