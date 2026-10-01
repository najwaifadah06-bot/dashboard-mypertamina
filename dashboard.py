import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Membuat Header/Judul Web
st.title("Dashboard Analisis Sentimen Aplikasi MyPertamina - Kelompok BBDM 26D")
st.write("Tekan tombol di bawah ini untuk melihat hasil analisis data ulasan.")

# 2. Membuat Tombol Interaktif
if st.button("Jalankan Pengumpulan & Analisis Data"):
    try:
        # Membaca data dari file CSV
        df = pd.read_csv("reviews(2).csv")
        
        # 3. Logika Sentimen (Positif, Netral, Negatif)
        def tentukan_sentimen(skor):
            if skor >= 4:
                return "Positif"
            elif skor == 3:
                return "Netral"
            else:
                return "Negatif"
        
        # Memasukkan hasil sentimen ke dalam tabel data
        df['Sentimen'] = df['score'].apply(tentukan_sentimen)
        
        # Menghitung angka-angka untuk ringkasan
        total_ulasan = len(df)
        rata_rata_rating = round(df['score'].mean(), 2)
        jumlah_negatif = len(df[df['Sentimen'] == 'Negatif'])
        persentase_negatif = round((jumlah_negatif / total_ulasan) * 100, 2)
        
        st.divider() # Garis pembatas agar rapi
        
        # 4. Menampilkan Ringkasan Angka (Metrik)
        st.subheader("Ringkasan Analisis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ulasan", total_ulasan)
        col2.metric("Rata-rata Rating", rata_rata_rating)
        col3.metric("Persentase Sentimen Negatif", f"{persentase_negatif}%")
        
        # 5. Visualisasi Grafik Pie Chart
        st.subheader("Grafik Proporsi Sentimen")
        jumlah_sentimen = df['Sentimen'].value_counts()
        
        # Membuat gambar grafik
        fig, ax = plt.subplots()
        warna = ['#4CAF50', '#F44336', '#FFC107'] # Warna hijau, merah, kuning
        ax.pie(jumlah_sentimen, labels=jumlah_sentimen.index, autopct='%1.1f%%', colors=warna, startangle=90)
        ax.axis('equal') # Memastikan grafik berbentuk lingkaran sempurna
        
        # Menampilkan grafik ke web
        st.pyplot(fig)
        
        # 6. Menampilkan Tabel Data
        st.subheader("Detail Data Ulasan")
        # Memilih kolom yang ingin ditampilkan
        tabel_tampil = df[['userName', 'score', 'Sentimen', 'content']]
        # Menampilkan tabel yang bisa di-scroll
        st.dataframe(tabel_tampil, use_container_width=True)
    except FileNotFoundError:
        st.error("File 'reviews(2).csv' tidak ditemukan. Pastikan file berada di direktori yang sama.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
