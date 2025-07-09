import os
import pandas as pd
import plotly.graph_objects as go


# Load data
df = pd.read_csv("gulf_peg_indicators.csv")

# Compute differentials
df["UAE_Infl_Diff"] = df["UAE_Inflation"] - df["US_Inflation"]
df["KSA_Infl_Diff"] = df["KSA_Inflation"] - df["US_Inflation"]
df["Qatar_Infl_Diff"] = df["Qatar_Inflation"] - df["US_Inflation"]

# REER Plot
fig_reer = go.Figure()
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["UAE_REER"], name="UAE REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["KSA_REER"], name="KSA REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["Qatar_REER"], name="Qatar REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=[105]*len(df), name="REER Warning", line=dict(dash='dot', color='red')))
fig_reer.update_layout(height=400, width=1000)

# Inflation Differential Plot
fig_infl = go.Figure()
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["UAE_Infl_Diff"], name="UAE - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["KSA_Infl_Diff"], name="KSA - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["Qatar_Infl_Diff"], name="Qatar - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=[3]*len(df), name="Inflation Threshold", line=dict(dash='dot', color='red')))
fig_infl.update_layout(height=400, width=1000)

# FX Reserves Plot with Axis Break
fig_res = go.Figure()
fig_res.add_trace(go.Scatter(x=df["Year"], y=df["KSA_Reserves"], name="KSA Reserves", yaxis="y1"))
fig_res.add_trace(go.Scatter(x=df["Year"], y=df["UAE_Reserves"], name="UAE Reserves", yaxis="y2"))
fig_res.add_trace(go.Scatter(x=df["Year"], y=df["Qatar_Reserves"], name="Qatar Reserves", yaxis="y2"))
fig_res.update_layout(
    xaxis=dict(title="Year"),
    yaxis=dict(
        title="KSA Reserves (USD Bn)",
        range=[400, 700],
        showgrid=False
    ),
    yaxis2=dict(
        title="UAE & Qatar Reserves (USD Bn)",
        overlaying='y',
        side='right',
        range=[30, 130],
        showgrid=True
    ),
    height=500,
    width=1000,
    legend=dict(x=0.01, y=0.99)
)

# NDF Premium
fig_ndf = go.Figure()
fig_ndf.add_trace(go.Scatter(x=df["Year"], y=df["UAE_NDF_Premium"], name="NDF Premium"))
fig_ndf.add_trace(go.Scatter(x=df["Year"], y=[0.5]*len(df), name="NDF Threshold", line=dict(dash='dot', color='red')))
fig_ndf.update_layout(height=400, width=1000)

