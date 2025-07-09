import os
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Gulf Currency Peg Health Dashboard (UAE, KSA, Qatar)")

# Load data
df = pd.read_csv("gulf_peg_indicators.csv")

# Compute differentials
df["UAE_Infl_Diff"] = df["UAE_Inflation"] - df["US_Inflation"]
df["KSA_Infl_Diff"] = df["KSA_Inflation"] - df["US_Inflation"]
df["Qatar_Infl_Diff"] = df["Qatar_Inflation"] - df["US_Inflation"]

# REER Plot
st.subheader("Real Effective Exchange Rate (REER)")
fig_reer = go.Figure()
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["UAE_REER"], name="UAE REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["KSA_REER"], name="KSA REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=df["Qatar_REER"], name="Qatar REER"))
fig_reer.add_trace(go.Scatter(x=df["Year"], y=[105]*len(df), name="REER Warning", line=dict(dash='dot', color='red')))
fig_reer.update_layout(height=400, width=1000)
st.plotly_chart(fig_reer)
st.markdown("**What this shows:** The Real Effective Exchange Rate (REER) reflects the inflation-adjusted value of a currency against trading partners.\n"
            "**Interpretation:** If REER rises, the currency becomes less competitive; a REER above 105 may signal overvaluation and stress on the peg.")

# Inflation Differential Plot
st.subheader("Inflation Differential vs US")
fig_infl = go.Figure()
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["UAE_Infl_Diff"], name="UAE - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["KSA_Infl_Diff"], name="KSA - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=df["Qatar_Infl_Diff"], name="Qatar - US"))
fig_infl.add_trace(go.Scatter(x=df["Year"], y=[3]*len(df), name="Inflation Threshold", line=dict(dash='dot', color='red')))
fig_infl.update_layout(height=400, width=1000)
st.plotly_chart(fig_infl)
st.markdown("**What this shows:** The inflation differential compares each country's inflation to that of the U.S.\n"
            "**Interpretation:** A persistent differential above 3% may indicate domestic overheating, eroding the peg's credibility.")

# FX Reserves Plot with Axis Break
st.subheader("FX Reserves (with Axis Break)")
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
st.plotly_chart(fig_res)
st.markdown("**What this shows:** This chart uses two y-axes to make UAE and Qatar reserve movements visible despite Saudi Arabia’s larger scale.\n"
            "**Interpretation:** Movements in smaller countries are now apparent, revealing trends that would otherwise appear flat.")

# NDF Premium
st.subheader("UAE NDF Premium")
fig_ndf = go.Figure()
fig_ndf.add_trace(go.Scatter(x=df["Year"], y=df["UAE_NDF_Premium"], name="NDF Premium"))
fig_ndf.add_trace(go.Scatter(x=df["Year"], y=[0.5]*len(df), name="NDF Threshold", line=dict(dash='dot', color='red')))
fig_ndf.update_layout(height=400, width=1000)
st.plotly_chart(fig_ndf)
st.markdown("**What this shows:** The offshore market's 3-month forward premium for AED vs USD.\n"
            "**Interpretation:** When this rises above 0.5%, it suggests that markets are pricing in a future devaluation—an early sign of stress on the peg.")

st.markdown("**Data sources:** BIS, IMF, national banks (compiled and modeled)")
