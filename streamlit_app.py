import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Veri setlerini yükleme
dataset_names = ['tips', 'iris']  # Eklemek istediğiniz diğer veri setlerini buraya ekleyin
selected_dataset_name = st.sidebar.selectbox('Select Dataset', dataset_names)

# Veri setini seçilen isme göre yükleme
if selected_dataset_name == 'tips':
    dataset = sns.load_dataset('tips')
elif selected_dataset_name == 'iris':
    dataset = sns.load_dataset('iris')
# Ekstra veri setlerini eklemek için buraya ekleyebilirsiniz

# Ana başlık
st.markdown(f'# {selected_dataset_name.capitalize()} Dataset Analysis')

# Dropdown'lar
if 'sex' in dataset.columns:
    sex = st.selectbox('Select Gender', dataset['sex'].unique())
if 'day' in dataset.columns:
    day = st.selectbox('Select Day', dataset['day'].unique())
if 'time' in dataset.columns:
    time = st.selectbox('Select Time', dataset['time'].unique())

# Matplotlib Figürü oluşturma fonksiyonu
def create_bar_chart(selected_data, x_feature, y_feature):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_feature, y=y_feature, data=selected_data)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

# Save düğmesi (CSV dosyası için)
csv_name = st.text_input('Enter CSV file name', 'selected_data')
save_csv_button = st.button('Save as CSV')

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
        selected_data.to_csv(f"{csv_name}.csv", index=False)
        st.success(f"Data saved as {csv_name}.csv")
    else:
        st.warning("No data available for the selected filters.")

# Dropdown değişikliklerine tepki gösterme
selected_data = dataset.copy()
if 'sex' in dataset.columns:
    x_feature = st.selectbox('Select X Feature', dataset.columns.tolist())
    y_feature = st.selectbox('Select Y Feature', dataset.columns.tolist())
    create_bar_chart(selected_data, x_feature, y_feature)
    
    # Veri seti hakkında genel istatistiksel bilgiler
    st.write("### General Statistics")
    st.write(selected_data.describe())

    # Grafik türünü seçme
    plot_type = st.selectbox("Select Plot Type", ["Bar Plot", "Scatter Plot", "Line Plot"])

    # Seçilen grafik türüne göre görselleştirme
    if plot_type == "Bar Plot":
        create_bar_chart(selected_data, x_feature, y_feature)
    elif plot_type == "Scatter Plot":
        st.write("### Scatter Plot")
        st.scatter_chart(data=selected_data, x=x_feature, y=y_feature)
    elif plot_type == "Line Plot":
        st.write("### Line Plot")
        st.line_chart(data=selected_data)

    # Filtreleme seçenekleri
    st.write("### Additional Filters")
    if 'smoker' in dataset.columns:
        smoker_filter = st.checkbox("Filter by Smoker")
        if smoker_filter:
            selected_data = selected_data[selected_data['smoker'] == 'Yes']

    # Yeniden oluşturulan grafik
    create_bar_chart(selected_data, x_feature, y_feature)
else:
    st.warning("No data available for the selected filters.")
