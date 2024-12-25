from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd
import tabula


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
    print(df.shape)
    df = df[
        [
            "Identyfikator funduszu lub Subfunduszu",
            "Nazwa subfunduszu",
            "Data wyceny",
            "Nazwa emitenta",
            "Identyfikator instrumentu - kod ISIN",
            "Waluta wykorzystywana do wyceny instrumentu",
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
            "Waluta wykorzystywana do wyceny instrumentu": "Waluta",
            "Procentowy udział w Aktywach ogółem": "Udział [%]",
        },
        inplace=True,
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

    df["ID Funduszu"] = "quercus_agresywny"
    df["Data"] = "2024-09-30"
    df.rename(
        {
            "NAZWA SUBFUNDUSZU": "Nazwa funduszu",
            "EMITENT": "Nazwa spółki",
            "KOD PAPIERU": "ID instrumentu",
            "UDZIAŁ % W AKTYWACH": "Udział [%]",
            "WALUTA": "Waluta",
        },
        axis=1,
        inplace=True,
    )
    df = df[
        [
            "ID Funduszu",
            "Nazwa funduszu",
            "Data",
            "Nazwa spółki",
            "ID instrumentu",
            "Waluta",
            "Udział [%]",
        ]
    ]

    assets_perc_sum = df["Udział [%]"].sum()
    df["Udział [%]"] = df["Udział [%]"] / assets_perc_sum * 100
    df.sort_values(by="Udział [%]", ascending=False, inplace=True)

    Path("data/output").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/output/Quercus.xlsx", index=False)


def santander():
    print("santander")
    file_path = (
        "data/input/Santander TFI _ Bieżące składy portfela_pl_1697446468261.xlsx"
    )
    sheet_name = "Zestawienie"
    fund_name = "Santander Akcji Małych i Średnich Spółek"

    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)

    df.rename(
        columns=lambda x: x.replace("\n", " ").replace("  ", " ").strip(), inplace=True
    )

    df = df[df["Nazwa subfunduszu"] == fund_name]
    df = df[df["Typ instrumentu"] == "Akcje"]
    df = df[df["Waluta wykorzystywana do wyceny instrumentu"] == "PLN"]
    df = df[df["Waluta wyceny aktywów i zobowiązań funduszu"] == "PLN"]
    print(df.shape)

    df_tmp = pd.read_excel(file_path, sheet_name="Zestawienie")
    columns = df_tmp.columns.tolist()
    report_date = columns[2].strftime("%Y-%m-%d")
    df["Data wyceny"] = report_date

    df = df[
        [
            "Standardowy identyfikator subfunduszu",
            "Nazwa subfunduszu",
            "Data wyceny",
            "Nazwa emitenta",
            "Identyfikator instrumentu - kod ISIN",
            "Waluta wykorzystywana do wyceny instrumentu",
            "Wartość instrumentu w walucie wyceny funduszu",
        ]
    ]
    assets_value = df["Wartość instrumentu w walucie wyceny funduszu"].sum()

    df["Procentowy udział w Aktywach ogółem"] = df[
        "Wartość instrumentu w walucie wyceny funduszu"
    ].apply(lambda x: x / assets_value * 100)
    df.sort_values(
        by="Procentowy udział w Aktywach ogółem", ascending=False, inplace=True
    )

    df.rename(
        columns={
            "Standardowy identyfikator subfunduszu": "ID funduszu",
            "Nazwa subfunduszu": "Nazwa funduszu",
            "Data wyceny": "Data",
            "Nazwa emitenta": "Nazwa spółki",
            "Identyfikator instrumentu - kod ISIN": "ID instrumentu",
            "Waluta wykorzystywana do wyceny instrumentu": "Waluta",
            "Procentowy udział w Aktywach ogółem": "Udział [%]",
        },
        inplace=True,
    )
    df.drop(columns=["Wartość instrumentu w walucie wyceny funduszu"], inplace=True)

    Path("data/output").mkdir(parents=True, exist_ok=True)
    df.to_excel("data/output/Santander.xlsx", index=False)


def uniqa():
    print("uniqa")
    file_path = "data/input/Publikacja_portfela_FIO_20240930.pdf"
    fund_name = "UNIQA Selektywny Akcji Polskich"
    dfs = tabula.read_pdf(file_path, pages="all")
    print(len(dfs))
    print(dfs[0].shape)
    print(dfs[0].head())

# paribas()
# quercus()
# santander()
uniqa()

# TODO dokończyć uniqa
# TODO dodać santander prestiż alfa
# TODO przeanalizować historyczne różnice w santanderowych
# TODO dodać wartość pojedynczego instrumentu
# TODO dodać market cap/przynaleźność do indeksów
# TODO dodać podsumowanie/groupby
# TODO dodać dividend elite
# TODO round do 2 miejsc
