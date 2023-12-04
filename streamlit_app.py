import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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
    selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]
    
    if not selected_data.empty:
        selected_data.to_csv(f"{csv_name}.csv", index=False)
        st.success(f"Data saved as {csv_name}.csv")
    else:
        st.warning("No data available for the selected filters.")

# Dropdown değişikliklerine tepki gösterme
selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]
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
st.write("Welcome to the Tips Dataset Analysis App!")
st.write("This app allows you to explore and analyze the 'tips' dataset using Streamlit and Seaborn.")
st.write("Use the sidebar on the left to customize your analysis.")

# Örnek içerik ekleme
st.write("Here are some key insights:")
st.write("- The dataset contains information about tips given in a restaurant.")
st.write("- You can filter the data based on gender, day, and time.")
st.write("- Choose different features for X and Y axes to visualize the data.")
st.write("- Save the filtered data as a CSV file using the 'Save as CSV' button in the sidebar.")
