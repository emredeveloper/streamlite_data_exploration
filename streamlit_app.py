import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Seaborn kütüphanesinden tips veri setini yükleme
tips = sns.load_dataset('tips')

# Ana başlık
st.markdown('# Tips Veri Seti Analizi')

# Dropdown'lar
sex = st.selectbox('Select Gender', ['Male', 'Female'])
day = st.selectbox('Select Day', tips['day'].unique().tolist())
time = st.selectbox('Select Time', ['Lunch', 'Dinner'])

# Matplotlib Figürü oluşturma fonksiyonu
def create_bar_chart(selected_data, x_feature, y_feature):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x_feature, y=y_feature, data=selected_data)
    plt.xticks(rotation=45)  # X ekseni etiketlerini 45 derece döndürme
    plt.tight_layout()
    st.pyplot()  # Streamlit için plt.show() yerine st.pyplot() kullanılır

# Save düğmesi (CSV dosyası için)
csv_name = st.text_input('Enter CSV file name', 'selected_data')
save_csv_button = st.button('Save as CSV')

# Save düğmesine tıklanma olayına tepki gösterme (CSV dosyası için)
def save_csv():
    selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]
    
    if not selected_data.empty:
        selected_data.to_csv(f"{csv_name}.csv", index=False)
        st.success(f"Data saved as {csv_name}.csv")
    else:
        st.warning("No data available for the selected filters.")

# Save düğmesine tıklanma olayına tepki gösterme (CSV dosyası için)
if save_csv_button:
    save_csv()

# Dropdown değişikliklerine tepki gösterme
selected_data = tips[(tips['sex'] == sex) & (tips['day'] == day) & (tips['time'] == time)]
if not selected_data.empty:
    x_feature = 'smoker'  # İsterseniz farklı bir özelliği seçebilirsiniz
    y_feature = 'total_bill'  # İsterseniz farklı bir özelliği seçebilirsiniz
    create_bar_chart(selected_data, x_feature, y_feature)
else:
    st.warning("No data available for the selected filters.")
