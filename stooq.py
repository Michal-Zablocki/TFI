from datetime import datetime
from pathlib import Path

import pandas as pd


def get_data():
    """Aggregates data from https://stooq.com/db/h/"""
    nc_dfs = []
    wse_dfs = []
    mini_wse_dfs = []
    dirs = [
        "nc indices",
        "nc stocks",
        "wse etfs",
        "wse futures",
        "wse indices",
        "wse stocks",
    ]
    for directory in dirs:
        print(directory)
        files = Path(f"data/input/d_pl_txt/data/daily/pl/{directory}").glob("*.txt")
        for file in files:
            try:
                df = pd.read_csv(file)
                df["<DATE>"] = df["<DATE>"].astype(str)

                if directory.startswith("nc "):
                    df = df[df["<DATE>"].str.startswith("2024")]
                    nc_dfs.append(df)

                elif directory.startswith("wse "):
                    if directory == "wse stocks":
                        df = df[
                            df["<DATE>"].str.startswith("2024")
                            | df["<DATE>"].str.startswith("2023")
                        ]
                        mini_wse_dfs.append(df)
                    df = df[df["<DATE>"].str.startswith("2024")]
                    wse_dfs.append(df)

            except pd.errors.EmptyDataError:
                pass
    main_df = pd.concat(nc_dfs + wse_dfs)
    main_df.to_csv("data/results/stooq_2024.csv", index=False)

    mini_df = main_df[["<TICKER>", "<DATE>", "<CLOSE>", "<VOL>"]]
    mini_df.to_csv("data/results/stooq_2024_mini.csv", index=False)

    mini_wse_df = pd.concat(mini_wse_dfs)
    mini_wse_df = mini_wse_df[["<TICKER>", "<DATE>", "<CLOSE>", "<VOL>"]]

    mini_wse_df["key"] = mini_wse_df.apply(
        lambda x: f"{x['<TICKER>']}_{x['<DATE>'][:4]}-{x['<DATE>'][4:6]}-{x['<DATE>'][6:]}",
        axis=1,
    )

    mini_wse_df["obrot"] = mini_wse_df.apply(
        lambda x: round(x["<CLOSE>"] * x["<VOL>"] / 1000, 3), axis=1
    )

    mini_wse_df = mini_wse_df[
        ["key", "<TICKER>", "<DATE>", "<CLOSE>", "<VOL>", "obrot"]
    ]

    mini_wse_df.to_csv("data/results/stooq_wse_2324_mini.csv", index=False)


get_data()
