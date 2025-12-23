# 📦 Stock Health & Reorder Intelligence

A Snowflake-powered inventory analytics solution that helps hospitals, NGOs, and public distribution systems **prevent stock-outs and reduce waste** by monitoring stock health and generating proactive reorder recommendations.

---

## 🎯 Problem Statement

Critical supplies such as medicines and food often run out unexpectedly due to fragmented inventory data, manual monitoring, and delayed detection of stock risks. This results in service disruption, wastage, and increased operational costs—especially in healthcare and public welfare systems.

---

## 💡 Solution Overview

This project provides a **Snowflake-native analytics pipeline** and a **Streamlit dashboard** that:
- Tracks daily inventory levels  
- Calculates consumption trends  
- Predicts stock-out risks using *Days of Cover*  
- Recommends reorder quantities  
- Presents insights in both visual and plain-language formats  

The solution is designed for **AI for Good** use cases where reliability and explainability matter.

---

## 🧠 Key Features

- Daily stock ingestion and analytics  
- Average daily consumption calculation  
- Days of Cover–based risk assessment  
- Risk classification: **CRITICAL / HIGH / MEDIUM / LOW**  
- Reorder quantity recommendations using lead time  
- Stock risk heatmap by location and item  
- Critical and high-risk stock alerts  
- Exportable reorder recommendations (CSV)  
- Plain-language operational insights for decision-makers  

---

## 🏗️ Architecture

**Data Flow:**

1. Daily stock data uploaded into Snowflake  
2. Analytics computed using Snowflake SQL views  
3. Risk and reorder logic applied in the analytics layer  
4. Streamlit app visualizes insights directly from Snowflake  

> Built entirely using Snowflake SQL and Streamlit — no external infrastructure required.

---

## 🧰 Tech Stack

- **Data Platform:** Snowflake  
- **Analytics:** Snowflake SQL (window functions, views)  
- **Visualization:** Streamlit (in-Snowflake)  
- **Programming:** Python  
- **Data Source:** CSV / operational inventory systems  

---

## 📁 Project Structure

```text
stock-health-reorder-intelligence/
├── sql/
│   └── setup_and_analytics.sql
│
├── streamlit/
│   └── streamlit_app.py
│
├── data/
│   └── sample_daily_stock.csv
│
├── docs/
│   ├── architecture_diagram.png
│   ├── use_case_diagram.png
│   └── screenshots/
│
└── README.md
```



This creates all required tables and analytical views.

### 3️⃣ Run Streamlit App
Deploy `streamlit/streamlit_app.py` using **Streamlit in Snowflake**.

---

## 🌍 AI for Good Impact

- Prevents shortages of critical medical supplies  
- Reduces overstocking and wastage  
- Enables proactive, data-driven procurement  
- Improves reliability of healthcare and public service delivery  

---

## 🔮 Future Enhancements

- Demand forecasting using time-series models  
- Automated reorder triggers  
- Supplier performance analysis  
- Mobile-friendly dashboards  
- ERP and procurement system integration  

---

## 👤 Author

**Agniv Dutta**  
AI for Good Hackathon Submission

