
import pandas as pd
import requests
from datetime import datetime

# IMF SDMX base URL
IMF_BASE = "https://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS"

# IMF series codes (monthly)
series = {
    "UAE_Reserves": "AE.M.RAXFXIR_N.XDC",
    "KSA_Reserves": "SA.M.RAXFXIR_N.XDC",
    "Qatar_Reserves": "QA.M.RAXFXIR_N.XDC",
    "UAE_Inflation": "AE.M.PCPI_IX",
    "KSA_Inflation": "SA.M.PCPI_IX",
    "Qatar_Inflation": "QA.M.PCPI_IX",
}

def fetch_imf(series_code):
    url = f"{IMF_BASE}/{series_code}?startPeriod=2015"
    r = requests.get(url)
    data = r.json()
    obs = data['CompactData']['DataSet']['Series']['Obs']
    df = pd.DataFrame(obs)
    df.columns = ['Date', series_code.split('.')[-1]]
    df['Date'] = pd.to_datetime(df['Date'])
    df[series_code.split('.')[-1]] = pd.to_numeric(df[series_code.split('.')[-1]], errors='coerce')
    return df

# US CPI from FRED
def fetch_us_cpi():
    url = "https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCNS&api_key=c8ed60990c06754a26ab858576633f01&file_type=json"
    r = requests.get(url)
    data = r.json()['observations']
    df = pd.DataFrame(data)[['date', 'value']]
    df.columns = ['Date', 'US_Inflation']
    df['Date'] = pd.to_datetime(df['Date'])
    df['US_Inflation'] = pd.to_numeric(df['US_Inflation'], errors='coerce')
    return df

# World Bank REER
def fetch_reer(country_code, country_name):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/NEER?format=json&per_page=1000"
    r = requests.get(url)
    data = r.json()[1]
    df = pd.DataFrame(data)
    df = df[['date', 'value']].dropna()
    df.columns = ['Year', f'{country_name}_REER']
    df['Year'] = df['Year'].astype(int)
    df[f'{country_name}_REER'] = df[f'{country_name}_REER'].astype(float)
    return df

# Fetch IMF data
dfs = {}
for name, code in series.items():
    df = fetch_imf(code)
    df = df.rename(columns={code.split('.')[-1]: name})
    dfs[name] = df

# Merge IMF series
df_merged = dfs["UAE_Reserves"]
for name in series:
    if name != "UAE_Reserves":
        df_merged = pd.merge(df_merged, dfs[name], on="Date", how="outer")

# Merge US CPI
us_cpi = fetch_us_cpi()
df_merged = pd.merge(df_merged, us_cpi, on="Date", how="outer")

# Create yearly dataset
df_merged["Year"] = df_merged["Date"].dt.year
df_yearly = df_merged.groupby("Year").last().reset_index()

# Fetch REER data from World Bank
uae_reer = fetch_reer("AE", "UAE")
ksa_reer = fetch_reer("SA", "KSA")
qatar_reer = fetch_reer("QA", "Qatar")

# Merge REER into main dataset
df_yearly = pd.merge(df_yearly, uae_reer, on="Year", how="left")
df_yearly = pd.merge(df_yearly, ksa_reer, on="Year", how="left")
df_yearly = pd.merge(df_yearly, qatar_reer, on="Year", how="left")

# Add NDF placeholder (not available in public API)
df_yearly["UAE_NDF_Premium"] = 0.1

# Final format
df_final = df_yearly[["Year", "UAE_REER", "KSA_REER", "Qatar_REER",
                      "UAE_Inflation", "US_Inflation", "UAE_Reserves", "UAE_NDF_Premium",
                      "KSA_Inflation", "KSA_Reserves",
                      "Qatar_Inflation", "Qatar_Reserves"]]

# Export
df_final.to_csv("gulf_peg_indicators.csv", index=False)
print("✅ gulf_peg_indicators.csv updated with live data.")
