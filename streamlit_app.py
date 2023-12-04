import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Temayı seç
st.set_option('deprecation.showPyplotGlobalUse', False)

# Seaborn kütüphanesinden tips veri setini yükleme
tips = sns.load_dataset('tips')

# Sayfa düzenleme
st.set_page_config(
    page_title="Tips Dataset Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Ana başlık
st.markdown('# Tips Veri Seti Analizi')

# Sidebar'ı oluştur
st.sidebar.header("Options")

# Dropdown'lar
sex = st.sidebar.selectbox('Select Gender', ['Male', 'Female'])
day = st.sidebar.selectbox('Select Day', tips['day'].unique().tolist())
time = st.sidebar.selectbox('Select Time', ['Lunch', 'Dinner'])

# Filtreleme seçenekleri
st.sidebar.subheader("Additional Filters")
smoker_filter = st.sidebar.checkbox("Filter by Smoker")

# Heatmap ve Korelasyon gösterim seçimi
show_heatmap = st.sidebar.checkbox("Show Heatmap and Correlation")

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

# Dropdown değişikliklerine tepki gösterme
selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]

# Ek filtreleme (smoker)
if smoker_filter:
    selected_data = selected_data[selected_data['smoker'] == 'Yes']

# Veri setinde NaN değerleri kontrol etme
nan_values = selected_data.isnull().sum()
st.sidebar.write("NaN Values in the Data:")
st.sidebar.write(nan_values)

# NaN değerleri temizleme
selected_data = selected_data.dropna()

if not selected_data.empty:
    x_feature = st.sidebar.selectbox('Select X Feature', selected_data.columns.tolist())
    y_feature = st.sidebar.selectbox('Select Y Feature', selected_data.columns.tolist())
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

    # Korelasyon Matrisi ve Heatmap
    if show_heatmap:
        st.write("### Correlation Matrix")

    # Kategorik olmayan sütunları seç
        numerical_columns = selected_data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    # Korelasyon matrisindeki NaN değerlere yönelik uyarıyı engelleme
    with np.errstate(divide='ignore', invalid='ignore'):
        correlation_matrix = selected_data[numerical_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)

    st.pyplot()


    # Save düğmesine tıklanma olayına tepki gösterme (CSV dosyası için)
    # Save düğmesine tıklanma olayına tepki gösterme (CSV dosyası için)
def save_csv():
    selected_data = dataset.copy()
    if 'sex' in dataset.columns:
        selected_data = selected_data[selected_data['sex'] == sex]
    if 'day' in dataset.columns:
        selected_data = selected_data[selected_data['day'] == day]
    if 'time' in dataset.columns:
        selected_data = selected_data[selected_data['time'] == time]
    
    if not selected_data.empty:
        # Dosyayı Streamlit'ten kullanıcıya indirme
        csv_file = selected_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Click to Download {csv_name}.csv",
            data=csv_file,
            file_name=f"{csv_name}.csv",
            mime="text/csv"
        )
        st.success(f"Data saved. Click the download button to get the CSV file.")
    else:
        st.warning("No data available for the selected filters.")

else:
    st.sidebar.warning("No data available for the selected filters.")
