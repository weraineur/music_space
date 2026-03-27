import pandas as pd

url = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"

df = pd.read_csv(url)

planets = df[
    [
        "name",
        "system_distance",
        "system_rightascension",
        "system_declination",
        "mass",
        "temperature",
    ]
].copy()

planets["type"] = "planet"

planets = planets.rename(
    columns={
        "name": "nom",
        "system_distance": "distance",
        "system_rightascension": "ascension_droite",
        "system_declination": "declinaison",
        "mass": "masse",
        "temperature": "temperature",
    }
)

print(planets.head())
print()
print(planets.isnull().sum())
print()
print(planets.info())
print()

planets.to_csv("planets.csv", index=False, encoding="utf-8")

print("CSV cree : planets.csv")
print()