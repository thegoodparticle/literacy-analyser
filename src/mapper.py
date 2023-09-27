import pandas as pd

# using pandas to read the CSV file as DataFrames
df = pd.read_csv("resources/MHA_Population_Report.csv")

# iterate through all the dataframes (rows in CSV file)
for i in range(len(df)):
    # we are interested in Census Year 2001 and 2011 only
    if df.loc[i, "Census Year"] in (2001, 2011):
        # print the output as key-value pair separated by a tab
        # Key: District,Census Year
        # Value: Total Literates, Total Population
        print('%s,%s\t%d,%d' % (df.loc[i, "District"], df.loc[i, "Census Year"],
                            df.loc[i, "Total literates"], df.loc[i, "Total population"]))