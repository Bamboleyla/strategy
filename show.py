import finplot as fplt
import pandas as pd
from utils import get_indicators_colums


def show_plot(data, indicators):
    pc_high, pc_low, pc_mid, st_upper, st_lower = get_indicators_colums(
        indicators
    )  # Take names colums from indicators data

    config = {
        "legend": "PriceChanelGrid",
        "required_columns": [
            "OPEN",
            "CLOSE",
            "HIGH",
            "LOW",
            "DATE",
            pc_high,
            pc_low,
            pc_mid,
            st_upper,
            st_lower,
            "BUY_PRICE",
            "ST_PRICE",
            "SL_PRICE",
            "TP_PRICE",
        ],
        "plots": [
            {"column": pc_high, "color": "#7B93FF", "width": 2},
            {"column": pc_low, "color": "#7B93FF", "width": 2},
            {"column": pc_mid, "color": "#BFFF2B", "width": 3},
            {"column": st_upper, "color": "#FA0000", "width": 3},
            {"column": st_lower, "color": "#006400", "width": 3},
            {"column": "SL_LINE", "color": "#FF5B5B", "width": 2},
            {"column": "TP_LINE", "color": "#AAFF5B", "width": 2},
        ],
        "actions": [
            {"column": "BUY_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "ST_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "SL_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "TP_PRICE", "color": "#000000", "style": "x", "width": 2},
        ],
        "signals": [
            {
                "name": "BUY",
                "price_col": "BUY_PRICE",
                "offset": -1,
                "color": "#4a6",
                "style": "^",
                "legend": "buy",
                "width": 2,
            },
            {
                "name": "TAKE_PROFIT",
                "price_col": "TP_PRICE",
                "offset": 1,
                "color": "#4a6",
                "style": "o",
                "legend": "take profit",
                "width": 2,
            },
            {
                "name": "STOP_LOSS",
                "price_col": "SL_PRICE",
                "offset": -1,
                "color": "#FF5B5B",
                "style": "p",
                "legend": "stop loss",
                "width": 2,
            },
            {
                "name": "CLOSE_TIME",
                "price_col": "ST_PRICE",
                "offset": -1,
                "color": "#3C74BD",
                "style": "d",
                "legend": "close time",
                "width": 2,
            },
        ],
    }

    # Check for required columns
    missing_columns = [
        col for col in config["required_columns"] if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"There are no mandatory columns: {missing_columns}")

    # Create candlestick chart
    data.set_index("DATE", inplace=True)
    data.index = pd.to_datetime(data.index).tz_localize("Etc/GMT-5")
    fplt.candlestick_ochl(data[["OPEN", "CLOSE", "HIGH", "LOW"]])

    # Plot indicators
    for plot in config["plots"]:
        fplt.plot(
            data[plot["column"]],
            legend=plot["column"],
            color=plot["color"],
            width=plot["width"],
        )

    # Plot actions (points)
    for action in config["actions"]:
        col_data = data[action["column"]].dropna()
        if not col_data.empty:
            fplt.plot(
                col_data,
                legend=action["column"],
                color=action["color"],
                style=action["style"],
                width=action["width"],
            )

    # Plot signals (special markers)
    for signal in config["signals"]:
        col_data = data[signal["price_col"]].dropna()
        if not col_data.empty:
            fplt.plot(
                col_data + signal.get("offset", 0),
                legend=signal["legend"],
                color=signal["color"],
                style=signal["style"],
                width=signal["width"],
            )

    fplt.add_legend(config["legend"])
    fplt.show()
