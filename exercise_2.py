"""
Exercise 2 for brush up.

Tristany Armangue i Jubert
"""

### Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/SergiQuintana/Python-for-Economics/main/sample_census.csv"
    )

# Show the head
print(df.head())

# Show some summary statistics
print(df.describe())

# Female indicator
df["female"] = np.where(df.SEX == 1, 0, 1)
df["gender"] = np.where(df.SEX == 1, "Male", "Female")
print(df[["SEX","female"]])


# Full time work
def full_time(row):
    if (row["WKSWORK2"] >= 5) and (row["UHRSWORK"] >= 35):
        return 1
    else:
        return 0

df["full_time"] = df.apply(lambda x: full_time(x), axis=1)
print(df[["WKSWORK2","UHRSWORK","full_time"]].head(10))

# Keep only those in LF and with positive finite wage income
df_lf = df[df["LABFORCE"] == 2]
print(df_lf["INCWAGE"].describe())

# Get average in INCWAGE by gender
print(df_lf.groupby("female")["INCWAGE"].mean())
mean_female = df_lf.groupby("female")["INCWAGE"].mean()[1]
mean_male = df_lf.groupby("female")["INCWAGE"].mean()[0]

# KDEs
ax = df_lf.groupby("gender")["INCWAGE"].plot.kde()
plt.axvline(x = mean_female, color = 'tab:blue', label = 'Mean', linestyle="--")
plt.axvline(x = mean_male, color = 'tab:orange', linestyle="--")

plt.legend()
plt.xlim([0, 700000])
plt.xlabel("Yearly Wage Income (USD)")
plt.title("Distributions of Yearly Wage Earnings by Gender - 2021")
plt.show()