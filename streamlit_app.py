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

# Function to create a bar chart
def create_bar_chart(selected_data, x_feature, y_feature):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_feature, y=y_feature, data=selected_data)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

# Function to display the correlation matrix for numeric columns
def display_correlation_matrix(selected_data):
    st.write("### Correlation Matrix")

    # Select numeric columns
    numerical_columns = selected_data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Calculate correlation matrix for numeric columns
    correlation_matrix = selected_data[numerical_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
    st.pyplot()

# Function to save the DataFrame as a CSV file
def save_as_csv(selected_data, csv_name='exported_data'):
    csv_file = selected_data.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv_file).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_name}.csv">Click to Download {csv_name}.csv</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# Function to display the scatter plot
def display_scatter_plot(selected_data, x_feature, y_feature):
    st.write("### Scatter Plot")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_feature, y=y_feature, data=selected_data, hue='sex', palette='viridis', size='total_bill')
    plt.title(f'Scatter Plot between {x_feature} and {y_feature}')
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    st.pyplot()

# Function to display the regression plot
def display_regression_plot(selected_data, x_feature, y_feature):
    st.write("### Regression Plot")

    plt.figure(figsize=(10, 6))
    sns.regplot(x=x_feature, y=y_feature, data=selected_data, scatter_kws={'s': 30}, line_kws={'color': 'red'})
    plt.title(f'Regression Plot between {x_feature} and {y_feature}')
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    st.pyplot()

# React to dropdown changes
selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]

# Apply additional filters (smoker)
if smoker_filter:
    selected_data = selected_data[selected_data['smoker'] == 'Yes']

# Drop NaN values
selected_data = selected_data.dropna()

# Display the selected data
st.write("## Selected Data")
st.write(selected_data)

if not selected_data.empty:
    x_feature = st.sidebar.selectbox('Select X Feature', selected_data.columns.tolist())
    y_feature = st.sidebar.selectbox('Select Y Feature', selected_data.columns.tolist())
    create_bar_chart(selected_data, x_feature, y_feature)

    # General statistical information about the dataset
    st.sidebar.subheader("General Statistics")
    st.sidebar.write(selected_data.describe())

    # Choose the plot type
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Plot", "Scatter Plot", "Line Plot", "Scatter Plot with Regression"])

    # Visualization based on the selected plot type
    if plot_type == "Bar Plot":
        create_bar_chart(selected_data, x_feature, y_feature)
    elif plot_type == "Scatter Plot":
        display_scatter_plot(selected_data, x_feature, y_feature)
    elif plot_type == "Line Plot":
        st.sidebar.subheader("Line Plot")
        st.sidebar.line_chart(data=selected_data)
    elif plot_type == "Scatter Plot with Regression":
        display_scatter_plot(selected_data, x_feature, y_feature)
        display_regression_plot(selected_data, x_feature, y_feature)

    # Display Correlation Matrix
    display_correlation_matrix(selected_data)

    # Save button outside the conditional block
    if st.sidebar.button("Save as CSV"):
        save_as_csv(selected_data, csv_name='exported_data')
        st.sidebar.success("Data saved. Click the download link to get the CSV file")

else:
    st.warning("No data available for the selected filters.")
