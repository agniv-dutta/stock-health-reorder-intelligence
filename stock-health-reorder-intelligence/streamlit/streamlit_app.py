import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(
    page_title="Stock Health & Reorder Intelligence",
    layout="wide"
)

# ---------------------------------------------------
# Snowflake session (AUTO-PROVIDED)
# ---------------------------------------------------
session = get_active_session()

@st.cache_data
def load_data(query: str) -> pd.DataFrame:
    return session.sql(query).to_pandas()

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.title("📦 Stock Health & Reorder Intelligence")
st.caption("Unified inventory monitoring to prevent stock-outs and reduce waste")

st.markdown("""
### 🎯 Why this matters
Hospitals and NGOs often discover shortages too late.  
This dashboard identifies **stock-out risks early** and recommends **exact reorder quantities**
so critical supplies are always available where needed.
""")

# ---------------------------------------------------
# Heatmap (NO plotly, NO matplotlib)
# ---------------------------------------------------
st.header("🔥 Stock Risk Heatmap (Days of Cover)")

view_mode = st.radio(
    "Heatmap view",
    ["Current risk (aggregated)", "Daily trend"]
)

if view_mode == "Daily trend":
    heatmap_df = load_data("""
        SELECT LOCATION, ITEM, DATE, DAYS_OF_COVER
        FROM STOCK_METRICS
    """)
    pivot = heatmap_df.pivot_table(
        index=["LOCATION", "DATE"],
        columns="ITEM",
        values="DAYS_OF_COVER"
    )
else:
    heatmap_df = load_data("""
        SELECT LOCATION, ITEM, AVG(DAYS_OF_COVER) AS DAYS_OF_COVER
        FROM STOCK_METRICS
        GROUP BY LOCATION, ITEM
    """)
    pivot = heatmap_df.pivot_table(
        index="LOCATION",
        columns="ITEM",
        values="DAYS_OF_COVER"
    )


def color_days(val):
    if pd.isna(val):
        return ""
    elif val < 3:
        return "background-color:#b11226;color:white"   # CRITICAL
    elif val < 7:
        return "background-color:#f04e23;color:white"   # HIGH
    elif val < 14:
        return "background-color:#f6c343;color:black"   # MEDIUM
    else:
        return "background-color:#2ca25f;color:white"   # LOW

st.dataframe(
    pivot.style.applymap(color_days),
    use_container_width=True
)

# ---------------------------------------------------
# Alerts
# ---------------------------------------------------
st.header("⚠️ Critical & High-Risk Stock Alerts")

alerts_df = load_data("""
SELECT
    LOCATION,
    ITEM,
    CASE
        WHEN DAYS_OF_COVER < 3 THEN 'CRITICAL'
        WHEN DAYS_OF_COVER < 7 THEN 'HIGH'
        WHEN DAYS_OF_COVER < 14 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS RISK_LEVEL,
    ROUND(DAYS_OF_COVER, 1) AS DAYS_OF_COVER,
    CLOSING_STOCK,
    ROUND(AVG_DAILY_CONSUMPTION, 2) AS AVG_DAILY_CONSUMPTION,
    LEAD_TIME_DAYS,
    GREATEST(
        CEIL((LEAD_TIME_DAYS * AVG_DAILY_CONSUMPTION) - CLOSING_STOCK),
        0
    ) AS REORDER_QUANTITY,
    CASE
        WHEN DAYS_OF_COVER < 3 THEN 'Order immediately'
        WHEN DAYS_OF_COVER < 7 THEN 'Order within 24 hrs'
        ELSE 'Monitor'
    END AS ACTION_REQUIRED
FROM STOCK_HEALTH_DB.ANALYTICS.STOCK_METRICS
WHERE DAYS_OF_COVER < 7
ORDER BY DAYS_OF_COVER ASC
""")

st.dataframe(alerts_df, use_container_width=True)

# ---------------------------------------------------
# KPI Summary
# ---------------------------------------------------
st.header("📊 Inventory Summary")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Locations", alerts_df["LOCATION"].nunique())
c2.metric("Items", alerts_df["ITEM"].nunique())
c3.metric("Critical Items", (alerts_df["RISK_LEVEL"] == "CRITICAL").sum())
c4.metric("High Risk Items", (alerts_df["RISK_LEVEL"] == "HIGH").sum())
c5.metric("Min Days Cover", f"{alerts_df['DAYS_OF_COVER'].min():.1f}")
c6.metric("Units to Reorder", int(alerts_df["REORDER_QUANTITY"].sum()))

# ---------------------------------------------------
# Export
# ---------------------------------------------------
st.header("⬇️ Export Reorder Recommendations")

st.download_button(
    "Download CSV",
    alerts_df.to_csv(index=False),
    "reorder_recommendations.csv",
    "text/csv"
)

# ---------------------------------------------------
# Plain-language Insight (NO Cortex dependency)
# ---------------------------------------------------
st.header("🧠 Plain-Language Insight")

critical = (alerts_df["RISK_LEVEL"] == "CRITICAL").sum()
high = (alerts_df["RISK_LEVEL"] == "HIGH").sum()
min_cover = alerts_df["DAYS_OF_COVER"].min()
locations = ", ".join(alerts_df["LOCATION"].unique())

st.info(
    f"⚠️ {critical + high} items are at high or critical risk. "
    f"The most urgent shortages are observed at {locations}. "
    f"Some items have as little as {min_cover:.1f} days of stock remaining. "
    f"Immediate reordering is recommended."
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.caption(
    "Built with Snowflake SQL, Dynamic Tables & Streamlit · AI for Good"
)
