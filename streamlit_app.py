import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64

# Set the theme
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load the 'tips' dataset from the Seaborn library
tips = sns.load_dataset('tips')

# Page layout
st.set_page_config(
    page_title="Tips Dataset Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Main title
st.markdown('# Tips Dataset Analysis')

# Sidebar
st.sidebar.header("Options")

# Dropdowns
sex = st.sidebar.selectbox('Select Gender', ['Male', 'Female'])
day = st.sidebar.selectbox('Select Day', tips['day'].unique().tolist())
time = st.sidebar.selectbox('Select Time', ['Lunch', 'Dinner'])

# Additional Filters
st.sidebar.subheader("Additional Filters")
smoker_filter = st.sidebar.checkbox("Filter by Smoker")

# Heatmap and Correlation option
show_heatmap = st.sidebar.checkbox("Show Heatmap")
show_correlation = st.sidebar.checkbox("Show Correlation Matrix")

# Function to create a bar chart
def create_bar_chart(selected_data, x_feature, y_feature):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_feature, y=y_feature, data=selected_data)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

# Function to display the correlation matrix
def display_correlation_matrix(selected_data):
    st.write("### Correlation Matrix")

    # Select non-categorical columns
    numerical_columns = selected_data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Handle NaN values in the correlation matrix
    with np.errstate(divide='ignore', invalid='ignore'):
        correlation_matrix = selected_data[numerical_columns].corr()
        st.write(sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5).figure)

# React to dropdown changes
selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]

# Apply additional filters (smoker)
if smoker_filter:
    selected_data = selected_data[selected_data['smoker'] == 'Yes']

# Check for NaN values in the dataset
nan_values = selected_data.isnull().sum()
st.sidebar.write("NaN Values in the Data:")
st.sidebar.write(nan_values)

# Drop NaN values
selected_data = selected_data.dropna()

if not selected_data.empty:
    x_feature = st.sidebar.selectbox('Select X Feature', selected_data.columns.tolist())
    y_feature = st.sidebar.selectbox('Select Y Feature', selected_data.columns.tolist())
    create_bar_chart(selected_data, x_feature, y_feature)

    # General statistical information about the dataset
    st.sidebar.subheader("General Statistics")
    st.sidebar.write(selected_data.describe())

    # Choose the plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Plot", "Scatter Plot", "Line Plot"])

    # Visualization based on the selected plot type
    if plot_type == "Bar Plot":
        create_bar_chart(selected_data, x_feature, y_feature)
    elif plot_type == "Scatter Plot":
        st.sidebar.subheader("Scatter Plot")
        st.sidebar.scatter_chart(data=selected_data, x=x_feature, y=y_feature)
    elif plot_type == "Line Plot":
        st.sidebar.subheader("Line Plot")
        st.sidebar.line_chart(data=selected_data)

    # Display Heatmap
    if show_heatmap:
        st.write("### Heatmap")
        display_correlation_matrix(selected_data)

    # Save button click event
    if st.sidebar.button("Save as CSV"):
        # Your save_csv function implementation here
        st.sidebar.success("Data saved. Click the download link to get the CSV file.")
else:
    st.warning("No data available for the selected filters.")
