from pathlib import Path

import numpy as np
import pandas as pd


RAW_DATA_PATH = Path("data/raw/Car_sale_ads.csv")
PROCESSED_DATA_PATH = Path("data/processed/car_ads_clean.csv")


def load_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path, sep=",")


def mode_or_nan(values: pd.Series):
    mode_values = values.mode()
    if mode_values.empty:
        return np.nan
    return mode_values.iloc[0]


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    data["First_owner"] = data["First_owner"].map({"Yes": 1}).fillna(0).astype(int)
    data = data.drop("First_registration_date", axis=1)

    data["CO2_emissions"] = data["CO2_emissions"].fillna(
        data.groupby(
            ["Fuel_type", "Displacement_cm3", "Vehicle_version"]
        )["CO2_emissions"].transform("median")
    )
    data["CO2_emissions"] = data["CO2_emissions"].fillna(
        data.groupby(["Fuel_type", "Displacement_cm3"])["CO2_emissions"]
        .transform("median")
    )
    data["CO2_emissions"] = data["CO2_emissions"].fillna(
        data.groupby("Fuel_type")["CO2_emissions"].transform("median")
    )
    data["CO2_emissions"] = data["CO2_emissions"].fillna(
        data["CO2_emissions"].median()
    )

    data = data.drop(columns=["Vehicle_version"])
    data["Vehicle_generation"] = data["Vehicle_generation"].fillna("Unknown")
    data["Origin_country"] = data["Origin_country"].fillna("Other")

    drive_stats = (
        data.dropna(subset=["Drive"])
        .groupby(["Vehicle_brand", "Vehicle_model"])["Drive"]
        .agg(
            known_count="count",
            dominant_drive=mode_or_nan,
            dominant_share=lambda values: (
                values.value_counts(normalize=True).iloc[0]
            ),
        )
        .reset_index()
    )
    reliable_drive_stats = drive_stats[
        (drive_stats["known_count"] >= 10)
        & (drive_stats["dominant_share"] >= 0.90)
    ][["Vehicle_brand", "Vehicle_model", "dominant_drive"]]

    data = data.merge(
        reliable_drive_stats,
        on=["Vehicle_brand", "Vehicle_model"],
        how="left",
    )
    data["Drive"] = data["Drive"].fillna(data["dominant_drive"])
    data = data.drop(columns=["dominant_drive"])
    data["Drive"] = data["Drive"].fillna("Unknown")

    data.loc[
        (data["Fuel_type"] == "Electric") & data["Displacement_cm3"].isna(),
        "Displacement_cm3",
    ] = 0
    data["Displacement_cm3"] = data["Displacement_cm3"].fillna(
        data.groupby(
            ["Vehicle_brand", "Vehicle_model", "Fuel_type"]
        )["Displacement_cm3"].transform("median")
    )
    data["Displacement_cm3"] = data["Displacement_cm3"].fillna(
        data.groupby(["Vehicle_brand", "Fuel_type"])["Displacement_cm3"]
        .transform("median")
    )
    data["Displacement_cm3"] = data["Displacement_cm3"].fillna(
        data.groupby("Fuel_type")["Displacement_cm3"].transform("median")
    )

    door_corrections = {
        ("Fiat", "Freemont"): 5,
        ("Mazda", "5"): 5,
        ("Mitsubishi", "Outlander"): 5,
        ("Opel", "Zafira"): 5,
        ("Renault", "Espace"): 5,
        ("Volvo", "XC 90"): 5,
        ("Volkswagen", "Caravelle"): 5,
        ("Tesla", "Model S"): 5,
        ("Volkswagen", "Golf"): 5,
        ("Volvo", "S90"): 4,
    }
    for (brand, model), doors in door_corrections.items():
        data.loc[
            (data["Vehicle_brand"] == brand)
            & (data["Vehicle_model"] == model)
            & (data["Doors_number"] >= 7),
            "Doors_number",
        ] = doors

    data.loc[
        (data["Vehicle_brand"] == "Inny")
        & (data["Vehicle_model"] == "Other")
        & (data["Doors_number"] >= 7),
        "Doors_number",
    ] = np.nan
    data.loc[data["Doors_number"] == 1, "Doors_number"] = np.nan

    data["Doors_number"] = data["Doors_number"].fillna(
        data.groupby(["Vehicle_brand", "Vehicle_model", "Type"])[
            "Doors_number"
        ].transform(mode_or_nan)
    )
    data["Doors_number"] = data["Doors_number"].fillna(
        data.groupby("Type")["Doors_number"].transform(mode_or_nan)
    )

    data.loc[data["Condition"] == "New", "Mileage_km"] = 0
    data.loc[
        (data["Condition"] == "Used") & (data["Mileage_km"] > 1_000_000),
        "Mileage_km",
    ] = np.nan
    data = data.dropna(subset=["Mileage_km"])

    data.loc[
        (data["Power_HP"] < 50) | (data["Power_HP"] > 1000),
        "Power_HP",
    ] = np.nan
    data["Power_HP"] = data["Power_HP"].fillna(
        data.groupby(
            ["Vehicle_brand", "Vehicle_model", "Fuel_type", "Displacement_cm3"]
        )["Power_HP"].transform("median")
    )
    data["Power_HP"] = data["Power_HP"].fillna(
        data.groupby(["Vehicle_brand", "Vehicle_model", "Fuel_type"])[
            "Power_HP"
        ].transform("median")
    )
    data["Power_HP"] = data["Power_HP"].fillna(
        data.groupby(["Vehicle_brand", "Vehicle_model"])["Power_HP"]
        .transform("median")
    )
    data["Power_HP"] = data["Power_HP"].fillna(
        data.groupby("Fuel_type")["Power_HP"].transform("median")
    )
    data["Power_HP"] = data["Power_HP"].fillna(data["Power_HP"].median())

    data.loc[data["Fuel_type"] == "Electric", "Transmission"] = "Automatic"
    data = data.dropna(subset=["Transmission"])

    data = data[data['Currency'] == 'PLN'].copy()

    return data


def save_data(data: pd.DataFrame, path: Path = PROCESSED_DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)


def main() -> None:
    df = load_data()
    data = preprocess_data(df)
    save_data(data)
    print(f"Saved cleaned dataset to {PROCESSED_DATA_PATH}")
    print(data.shape)


if __name__ == "__main__":
    main()
