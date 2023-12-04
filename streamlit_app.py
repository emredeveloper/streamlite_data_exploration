import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Temayı seç
st.set_option('deprecation.showPyplotGlobalUse', False)

# Ana başlık
st.markdown('# Veri Seti Analizi')

# Veri seti seçimi
selected_dataset = st.sidebar.selectbox('Select Dataset', ['tips', 'iris'])

# Veri setini yükleme
if selected_dataset == 'tips':
    dataset = sns.load_dataset('tips')
elif selected_dataset == 'iris':
    dataset = sns.load_dataset('iris')

# Sidebar'ı oluştur
st.sidebar.header("Options")

# Dropdown'lar
sex = st.sidebar.selectbox('Select Gender', ['Male', 'Female'])
day = st.sidebar.selectbox('Select Day', dataset['day'].unique().tolist())
time = st.sidebar.selectbox('Select Time', dataset['time'].unique().tolist())

# Matplotlib Figürü oluşturma fonksiyonu
def create_bar_chart(selected_data, x_feature, y_feature):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_feature, y=y_feature, data=selected_data)
    plt.xticks(rotation=45)  # X ekseni etiketlerini 45 derece döndürme
    plt.tight_layout()
    st.pyplot()  # Streamlit için plt.show() yerine st.pyplot() kullanılır

# Save düğmesi (CSV dosyası için)
csv_name = st.sidebar.text_input('Enter CSV file name', 'selected_data')
save_csv_button = st.sidebar.button('Save as CSV')

# Save düğmesine tıklanma olayına tepki gösterme (CSV dosyası için)
def save_csv():
    selected_data = dataset[(dataset['sex'] == sex) & (dataset['day'] == day) & (dataset['time'] == time)]
    
    if not selected_data.empty:
        selected_data.to_csv(f"{csv_name}.csv", index=False)
        st.sidebar.success(f"Data saved as {csv_name}.csv")
    else:
        st.sidebar.warning("No data available for the selected filters.")

# Dropdown değişikliklerine tepki gösterme
selected_data = dataset[(dataset['sex'] == sex) & (dataset['day'] == day) & (dataset['time'] == time)]
if not selected_data.empty:
    x_feature = st.sidebar.selectbox('Select X Feature', dataset.columns.tolist())
    y_feature = st.sidebar.selectbox('Select Y Feature', dataset.columns.tolist())
    create_bar_chart(selected_data, x_feature, y_feature)
    
    # Veri seti hakkında genel istatistiksel bilgiler
    st.sidebar.subheader("General Statistics")
    st.sidebar.write(selected_data.describe())

    # Grafik türünü seçme
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar Plot", "Scatter Plot", "Line Plot"])

    # Seçilen grafik türüne göre görselleştirme
    if plot_type == "Bar Plot":
        create_bar_chart(selected_data, x_feature, y_feature)
    elif plot_type == "Scatter Plot":
        st.sidebar.subheader("Scatter Plot")
        st.sidebar.scatter_chart(data=selected_data, x=x_feature, y=y_feature)
    elif plot_type == "Line Plot":
        st.sidebar.subheader("Line Plot")
        st.sidebar.line_chart(data=selected_data)

    # Filtreleme seçenekleri
    st.sidebar.subheader("Additional Filters")
    smoker_filter = st.sidebar.checkbox("Filter by Smoker")
    if smoker_filter:
        selected_data = selected_data[selected_data['smoker'] == 'Yes']

    # Yeniden oluşturulan grafik
    create_bar_chart(selected_data, x_feature, y_feature)
else:
    st.sidebar.warning("No data available for the selected filters.")

# Ana sayfa içeriği
st.write(f"Welcome to the {selected_dataset.capitalize()} Dataset Analysis App!")
st.write("This app allows you to explore and analyze different datasets using Streamlit and Seaborn.")
st.write("Use the sidebar on the left to customize your analysis.")
