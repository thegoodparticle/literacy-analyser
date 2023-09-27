import pandas as pd

df = pd.read_csv("resources/test_data.csv")

districts = set()

for i in range(len(df)):
    if df.loc[i, "Census Year"] == 1991:
        districts.add(df.loc[i, "District"])
    
print(len(districts))

literacy_rate = f"{2/3:.2%}"
print(type(literacy_rate))