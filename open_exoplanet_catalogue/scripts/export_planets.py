import pandas as pd

url = "https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt"

df = pd.read_csv(url)

print(df.head())
