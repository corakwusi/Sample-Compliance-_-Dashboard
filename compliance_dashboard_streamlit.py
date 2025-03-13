import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Title
st.title("Automated Compliance Dashboard")

# Load data
file_path = "Sample_Compliance_Dashboard_.xlsx"
dashboard_df = pd.read_excel(file_path, sheet_name='Dashboard')

# Convert Due_Date to datetime, handle errors
dashboard_df['Due_Date'] = pd.to_datetime(dashboard_df['Due_Date'], errors='coerce')

# Calculate Days Remaining
today = pd.to_datetime(datetime.today())
dashboard_df['Days_Remaining'] = (dashboard_df['Due_Date'] - today).dt.days

# Add a Start_Date for timeline visualization
dashboard_df['Start_Date'] = today

# Filter options
risk_categories = dashboard_df['RiskCategory'].unique()
selected_risk = st.sidebar.selectbox("Filter by Risk Category", options=["All"] + list(risk_categories))

# Filter data based on selection
if selected_risk != "All":
    filtered_df = dashboard_df[dashboard_df['RiskCategory'] == selected_risk]
else:
    filtered_df = dashboard_df

# Display Data Table
st.subheader("Compliance Returns Table")
st.dataframe(filtered_df[['Returns', 'RiskCategory', 'Due_Date', 'Days_Remaining', 'Submission_Status']])

# Display Timeline Chart
st.subheader("Submission Timeline")
fig = px.timeline(
    filtered_df.dropna(subset=['Due_Date']),
    x_start='Start_Date',
    x_end='Due_Date',
    y='Returns',
    color='RiskCategory',
    title='Compliance Submission Timeline'
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig)

# KPI Section
st.subheader("Dashboard KPIs")
st.metric("Total Returns", len(filtered_df))
st.metric("Overdue Returns", filtered_df[filtered_df['Days_Remaining'] < 0].shape[0])
st.metric("High Risk Returns", filtered_df[filtered_df['RiskCategory'] == 'High'].shape[0])

st.success("Dashboard Loaded Successfully!")
