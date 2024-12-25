import decimal
from pathlib import Path

import numpy as np
import pandas as pd

import tabula

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def paribas():
    print("paribas")
    file_path = "data/input/BNP_Paribas_TFI_sklady-portfeli-funduszy_3Q2024.xlsx"
    sheet_name = "Składy potfeli 3Q 2024"
    fund_name = "BNP_Paribas_Malych_i_Srednich_Spolek"

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    df.rename(
        columns=lambda x: x.replace("\n", " ").replace("  ", " ").strip(), inplace=True
    )

    df = df[df["Nazwa subfunduszu"] == fund_name]
    df = df[df["Typ instrumentu"] == "Akcje"]
    df = df[df["Waluta wykorzystywana do wyceny instrumentu"] == "PLN"]
    print(df.shape)
    df = df[
        [
            "Identyfikator funduszu lub Subfunduszu",
            "Nazwa subfunduszu",
            "Data wyceny",
            "Nazwa emitenta",
            "Identyfikator instrumentu - kod ISIN",
            "Procentowy udział w Aktywach ogółem",
        ]
    ]

    assets_perc_sum = df["Procentowy udział w Aktywach ogółem"].sum()
    df["Procentowy udział w Aktywach ogółem"] = df[
        "Procentowy udział w Aktywach ogółem"
    ].apply(lambda x: x / assets_perc_sum * 100)
    df.sort_values(
        by="Procentowy udział w Aktywach ogółem", ascending=False, inplace=True
    )

    df.rename(
        columns={
            "Identyfikator funduszu lub Subfunduszu": "ID funduszu",
            "Nazwa subfunduszu": "Nazwa funduszu",
            "Data wyceny": "Data",
            "Nazwa emitenta": "Nazwa spółki",
            "Identyfikator instrumentu - kod ISIN": "ID instrumentu",
            "Procentowy udział w Aktywach ogółem": "Udział [%]",
        },
        inplace=True,
    )

    df["Udział [%]"] = df["Udział [%]"].apply(
        lambda x: float(decimal.Decimal(x).quantize(decimal.Decimal("0.01")))
    )

    Path("data/output").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/output/BNP_Paribas.xlsx", index=False)


def quercus():
    print("quercus")
    file_path = "data/input/QUERCUS_Agresywny_portfel_subfunduszu_20240930.xlsx"
    sheet_name = "QAGR"
    fund_name = "QUERCUS Agresywny"

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    df.rename(
        columns=lambda x: x.replace("\n", " ").replace("  ", " ").strip(), inplace=True
    )

    df = df[df["NAZWA SUBFUNDUSZU"] == fund_name]
    df = df[df["TYP INSTRUMENTU"] == "Akcja"]
    df = df[df["WALUTA"] == "PLN"]
    print(df.shape)

    df["ID funduszu"] = "quercus_agresywny"
    df["Data"] = "2024-09-30"
    df.rename(
        {
            "NAZWA SUBFUNDUSZU": "Nazwa funduszu",
            "EMITENT": "Nazwa spółki",
            "KOD PAPIERU": "ID instrumentu",
            "UDZIAŁ % W AKTYWACH": "Udział [%]",
        },
        axis=1,
        inplace=True,
    )
    df = df[
        [
            "ID funduszu",
            "Nazwa funduszu",
            "Data",
            "Nazwa spółki",
            "ID instrumentu",
            "Udział [%]",
        ]
    ]

    assets_perc_sum = df["Udział [%]"].sum()
    df["Udział [%]"] = df["Udział [%]"] / assets_perc_sum * 100
    df["Udział [%]"] = df["Udział [%]"].apply(
        lambda x: float(decimal.Decimal(x).quantize(decimal.Decimal("0.01")))
    )
    df.sort_values(by="Udział [%]", ascending=False, inplace=True)

    Path("data/output").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/output/Quercus.xlsx", index=False)


def santander():
    print("santander")
    file_path = (
        "data/input/Santander TFI _ Bieżące składy portfela_pl_1697446468261.xlsx"
    )
    sheet_name = "Zestawienie"

    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)

    df.rename(
        columns=lambda x: x.replace("\n", " ").replace("  ", " ").strip(), inplace=True
    )

    df_tmp = pd.read_excel(file_path, sheet_name="Zestawienie")
    columns = df_tmp.columns.tolist()
    report_date = columns[2].strftime("%Y-%m-%d")

    fund_dict = {
        "MiŚ": "Santander Akcji Małych i Średnich Spółek",
        "Alfa": "Santander Prestiż Alfa",
    }

    for fund_key, fund_val in fund_dict.items():
        fund_df = df[df["Nazwa subfunduszu"] == fund_val]
        fund_df = fund_df[fund_df["Typ instrumentu"] == "Akcje"]
        fund_df = fund_df[
            fund_df["Waluta wykorzystywana do wyceny instrumentu"] == "PLN"
        ]
        print(fund_df.shape)

        fund_df["Data wyceny"] = report_date

        fund_df = fund_df[
            [
                "Standardowy identyfikator subfunduszu",
                "Nazwa subfunduszu",
                "Data wyceny",
                "Nazwa emitenta",
                "Identyfikator instrumentu - kod ISIN",
                "Wartość instrumentu w walucie wyceny funduszu",
            ]
        ]
        assets_value = fund_df["Wartość instrumentu w walucie wyceny funduszu"].sum()

        fund_df["Procentowy udział w Aktywach ogółem"] = fund_df[
            "Wartość instrumentu w walucie wyceny funduszu"
        ].apply(lambda x: x / assets_value * 100)
        fund_df["Procentowy udział w Aktywach ogółem"] = fund_df[
            "Procentowy udział w Aktywach ogółem"
        ].apply(lambda x: float(decimal.Decimal(x).quantize(decimal.Decimal("0.01"))))
        fund_df.sort_values(
            by="Procentowy udział w Aktywach ogółem", ascending=False, inplace=True
        )

        fund_df.rename(
            columns={
                "Standardowy identyfikator subfunduszu": "ID funduszu",
                "Nazwa subfunduszu": "Nazwa funduszu",
                "Data wyceny": "Data",
                "Nazwa emitenta": "Nazwa spółki",
                "Identyfikator instrumentu - kod ISIN": "ID instrumentu",
                "Procentowy udział w Aktywach ogółem": "Udział [%]",
            },
            inplace=True,
        )
        fund_df.drop(
            columns=["Wartość instrumentu w walucie wyceny funduszu"], inplace=True
        )

        Path("data/output").mkdir(parents=True, exist_ok=True)
        fund_df.to_excel(f"data/output/Santander_{fund_key}.xlsx", index=False)


def uniqa():
    print("uniqa")
    file_path = "data/input/Publikacja_portfela_FIO_20240930.pdf"
    fund_name = "UNIQA Selektywny Akcji Polskich"
    dfs = tabula.read_pdf(file_path, pages="all")
    df = pd.concat(dfs, ignore_index=True)

    df = df[df["Nazwa subfunduszu"] == fund_name]

    Path("data/output").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/output/UNIQA.xlsx", index=False)


def merge_outputs():
    print("merge")
    df = pd.DataFrame()
    files = Path("data/output").glob("*.xlsx")
    for f in files:
        tmp_df = pd.read_excel(f)
        df = pd.concat([df, tmp_df], ignore_index=True)
    Path("data/results").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/results/merged.xlsx", index=False)

    name_dict = dict()
    for row in df.iterrows():
        name_dict[row[1]["ID instrumentu"]] = row[1]["Nazwa spółki"]

    df = df.pivot_table(
        index=["ID instrumentu"],
        columns=["Nazwa funduszu"],
        values="Udział [%]",
        aggfunc="sum",
    ).reset_index()

    no_columns = len(df.columns)
    df["Mean [%]"] = df.apply(
        lambda x: np.nansum([x.iloc[i] for i in range(1, no_columns)])
        / (no_columns - 1),
        axis=1,
    )
    df["Mean [%]"] = df["Mean [%]"].apply(
        lambda x: float(decimal.Decimal(x).quantize(decimal.Decimal("0.01")))
    )

    df.sort_values(by="Mean [%]", ascending=False, inplace=True)

    df["Nazwa spółki"] = df["ID instrumentu"].map(name_dict)

    df.to_excel("data/results/pivot.xlsx", index=False)


# paribas()
# quercus()
# santander()
uniqa()
# merge_outputs()

# TODO dokończyć uniqa
# TODO przeanalizować historyczne różnice [wliczając liczbę akcji, wartość danego instrumentu + udział]
# TODO dodać market cap
# TODO dodać przynaleźność do indeksów
# TODO dodać dividend elite
# TODO dodac własne portfolio
# TODO dodać słownik ID instrumentu - ticker
