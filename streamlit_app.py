import streamlit as st
import pandas as pd
import base64

# Yüklü veri çerçevesi
uploaded_data = pd.DataFrame()

# Veri çerçevesine yeni veri eklemek için bir Streamlit formu
st.sidebar.header("Add New Data")
new_data = st.sidebar.form(key="new_data_form")
new_value = new_data.text_input("Enter New Value", key="new_value")
submit_button = new_data.form_submit_button("Add New Data")

# Eğer form gönderildiyse, yeni veriyi veri çerçevesine ekle
if submit_button:
    new_row = pd.DataFrame({"New Column": [new_value]})
    uploaded_data = pd.concat([uploaded_data, new_row], ignore_index=True)

# Yüklü veri çerçevesini göster
st.write("## Uploaded Data")
st.write(uploaded_data)

# Yüklü veriyi CSV olarak kaydet
if st.button("Update and Save as CSV"):
    # CSV'yi kaydet
    csv_file = uploaded_data.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv_file).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="updated_data.csv">Click to Download Updated CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
    st.success("Data updated and saved as CSV.")

# Function to handle file upload and analysis
def handle_uploaded_file():
    global uploaded_data
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        uploaded_data = pd.read_csv(uploaded_file)

        st.write("## Uploaded Data")
        st.write(uploaded_data)

        # Perform analysis on the uploaded data (you can customize this part)
        st.write("## General Information about the uploaded data:")
        st.write(uploaded_data.info())

        # Example analysis
        st.write("## Example Analysis on the uploaded data:")
        selected_column = st.selectbox("Select Column for Visualization", uploaded_data.columns)

        # Line plot instead of bar chart
        st.line_chart(uploaded_data[selected_column])

# Call the function to handle file upload and analysis
handle_uploaded_file()


        # Update button
        if st.button("Update and Save as CSV"):
            # Save updated CSV
            save_as_csv(uploaded_data, csv_name='updated_data')
            st.success("Data updated and saved as CSV.")

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

# Call the function to handle file upload and analysis
handle_uploaded_file()

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

