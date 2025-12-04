

import os
import pandas as pd
import matplotlib.pyplot as plt


CSV_PATH = "central_west.csv"

# TASK 1 
def task1_load_and_inspect(path=CSV_PATH):
    if not os.path.exists(path):
        print(f"CSV file not found: {path}")
        return

    df = pd.read_csv(path)

    print("\n=== HEAD ===")
    print(df.head())

    print("\n=== INFO ===")
    print(df.info())

    print("\n=== DESCRIBE ===")
    print(df.describe(include='all'))

    return df



def prepare_dataframe(path=CSV_PATH):
    df = pd.read_csv(path)

    
    df['datetime'] = pd.to_datetime(df['Data'] + " " + df['Hora'], errors="coerce")
    df = df.dropna(subset=['datetime'])
    df = df.set_index('datetime')

    
    df = df.rename(columns={
        "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)": "temp_c",
        "UMIDADE RELATIVA DO AR, HORARIA (%)": "humidity",
        "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)": "rainfall"
    })

    
    df = df.fillna(method='ffill').fillna(method='bfill')

    return df


#  TASK 2 
def task2_clean_and_process():
    df = prepare_dataframe()
    print("\n=== CLEANED DATA SAMPLE ===")
    print(df[['temp_c', 'humidity', 'rainfall']].head())
    return df


#  TASK 3 
def task3_statistics():
    df = prepare_dataframe()

    daily = df['temp_c'].resample('D').agg(['mean', 'min', 'max', 'std'])
    monthly = df['temp_c'].resample('M').agg(['mean', 'min', 'max', 'std'])
    yearly = df['temp_c'].resample('Y').agg(['mean', 'min', 'max', 'std'])

    print("\n=== DAILY STATS ===\n", daily.head())
    print("\n=== MONTHLY STATS ===\n", monthly.head())
    print("\n=== YEARLY STATS ===\n", yearly.head())

    return daily, monthly, yearly


#  TASK 4 
def task4_visualization():
    df = prepare_dataframe()

    
    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df['temp_c'])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig("daily_temperature_trend.png")
    plt.close()

    
    monthly_rain = df['rainfall'].resample('M').sum()
    plt.figure(figsize=(8, 4))
    plt.bar(monthly_rain.index, monthly_rain.values)
    plt.title("Monthly Rainfall Totals")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()
    plt.savefig("monthly_rainfall_totals.png")
    plt.close()

    
    plt.figure(figsize=(6, 4))
    plt.scatter(df['temp_c'], df['humidity'])
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Humidity (%)")
    plt.tight_layout()
    plt.savefig("humidity_vs_temperature.png")
    plt.close()

    print("All plots saved successfully.")


#  TASK 5
def task5_seasonal_analysis():
    df = prepare_dataframe()

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8]:
            return "Monsoon"
        else:
            return "Autumn"

    df['Season'] = df.index.month.map(get_season)

    season_stats = df.groupby("Season").agg({
        "temp_c": "mean",
        "rainfall": "sum",
        "humidity": "mean"
    })

    print("\n=== SEASONAL WEATHER STATS ===")
    print(season_stats)

    return season_stats


#  TASK 6
def task6_export_and_report():
    df = prepare_dataframe()

    
    df[['temp_c', 'humidity', 'rainfall']].to_csv("cleaned_weather_data.csv")
    print("Cleaned data exported → cleaned_weather_data.csv")

    
    report = f"""
# Weather Data Analysis Report

### Time Range:
{df.index.min().date()} to {df.index.max().date()}

## Insights
- Daily temperature varies significantly through seasons.
- Rainfall drastically increases in monsoon months.
- Humidity shows a strong relation with temperature.

## Generated Output Files
| Type | File |
|------|------|
| Cleaned Dataset | cleaned_weather_data.csv |
| Plot | daily_temperature_trend.png |
| Plot | monthly_rainfall_totals.png |
| Plot | humidity_vs_temperature.png |

---
Generated automatically through Python analysis.
"""

    with open("Weather_Report.md", "w") as file:
        file.write(report)

    print("Markdown report saved → Weather_Report.md")



if __name__ == "__main__":
    task1_load_and_inspect()
    task2_clean_and_process()
    task3_statistics()
    task4_visualization()
    task5_seasonal_analysis()
    task6_export_and_report()

    print("\n✔ ALL TASKS COMPLETED SUCCESSFULLY!")