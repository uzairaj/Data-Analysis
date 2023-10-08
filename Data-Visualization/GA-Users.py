import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import numpy as np


file_name = 'C:/Users/all/GA-Users.xlsx'

user_data = pd.read_excel(file_name)
user_data.head()

#EDA
user_data['Date'] = pd.to_datetime(user_data['Date'])
user_data.info()

user_data['Data Source'].replace('(not set)', 'Not define', inplace=True)
user_data['Browser'].replace('(not set)', 'Not define', inplace=True)
user_data['Browser'].replace("'Mozilla", 'Mozilla', inplace=True)

user_data['City'].replace('(not set)', 'Not define', inplace=True)
user_data['City'].replace(69125, 'Incorrect value', inplace=True)
user_data['City'].replace(24550, 'Incorrect value', inplace=True)
user_data['City'].replace(86495, 'Incorrect value', inplace=True)
user_data['City'].replace(24550, 'Incorrect value', inplace=True)
user_data['City'].replace(8971, 'Incorrect value', inplace=True)
user_data['City'].replace('6th of October City', 'Incorrect value', inplace=True)
user_data['City'].unique()

user_data.drop_duplicates(inplace=True)
#print(user_data.head())



#version 1

user_data['Year'] = user_data['Date'].dt.year
user_data['Month'] = user_data['Date'].dt.month
user_data['Day'] = user_data['Date'].dt.day

st.title("Company Users Graph")


# Add filters for year, month, and day
show_all_years = st.sidebar.checkbox("Show Data for All Years")
show_all_months = st.sidebar.checkbox("Show Data for All Months")
show_all_days = st.sidebar.checkbox("Show Data for All Days")

if not show_all_years:
    year_filter = st.sidebar.selectbox("Select Year:", user_data['Year'].unique())

if not show_all_months:
    month_filter = st.sidebar.selectbox("Select Month:", user_data['Month'].unique())

if not show_all_days:
    day_filter = st.sidebar.selectbox("Select Day:", user_data['Day'].unique())

default_company = "Company A"  # Change this to your default company
company_filter = st.sidebar.selectbox("Choose Company:", user_data['Company'].unique(), index=user_data['Company'].unique().tolist().index(default_company))

# Add a "Generate Report" button
if st.sidebar.button("Generate Report"):
    # Filter the data based on selected filters
    filtered_data = user_data[user_data['Company'] == company_filter]
    
    if not show_all_years:
        filtered_data = filtered_data[filtered_data['Year'] == year_filter]
    
    if not show_all_months:
        filtered_data = filtered_data[filtered_data['Month'] == month_filter]
    
    if not show_all_days:
        filtered_data = filtered_data[filtered_data['Day'] == day_filter]
    
    # Display the filtered data
    # st.write("Filtered Data:")
    # st.write(filtered_data)

    # Display the graph
    fig = px.bar(filtered_data, x='Year', y=['Users', 'New Users'], barmode='group', title='Company Users Graph')
    st.plotly_chart(fig)

    browser_counts = filtered_data['Browser'].value_counts().reset_index()
    browser_counts.columns = ['Browser', 'Count']
    fig_browser = px.bar(browser_counts, x='Browser', y='Count', title='Browser Counts')
    fig_browser.update_xaxes(title_text='Browser')
    fig_browser.update_yaxes(title_text='Count')
    st.plotly_chart(fig_browser)

    # Display the top 10 cities by user count
    st.write("Top 10 Cities by Most Users Count:")
    city_users_count = filtered_data.groupby('City')['Users'].sum().reset_index()
    top_10_cities_users = city_users_count.sort_values(by='Users', ascending=False).head(10)
    st.write(top_10_cities_users)

    # Display the top 10 cities by new user count
    st.write("Top 10 Cities from Where Most New Users Came:")
    city_new_users_count = filtered_data.groupby('City')['New Users'].sum().reset_index()
    top_10_cities_new_users = city_new_users_count.sort_values(by='New Users', ascending=False).head(10)
    st.write(top_10_cities_new_users)


