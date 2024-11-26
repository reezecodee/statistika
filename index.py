import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Membuat dataset penjualan
data = {
    'NA_Sales': [45.3, 23.1, 67.5, 12.8, 56.2, 34.6, 89.7, 17.5, 62.4, 29.8, 
                 41.2, 73.6, 15.9, 52.7, 38.4, 81.3, 26.5, 59.1, 33.7, 70.2],
    'EU_Sales': [32.6, 18.7, 54.3, 9.5, 42.1, 27.8, 71.2, 14.6, 49.5, 22.3, 
                 36.9, 59.7, 11.8, 43.6, 30.2, 65.4, 20.7, 47.3, 26.1, 56.8],
    'JP_Sales': [22.4, 13.5, 38.7, 6.9, 30.2, 19.6, 50.1, 10.3, 35.6, 16.2, 
                 26.7, 42.3, 8.5, 31.4, 21.8, 46.5, 14.9, 33.8, 18.7, 40.6],
    'Other_Sales': [15.7, 9.2, 26.8, 4.6, 21.3, 13.5, 34.9, 7.1, 24.6, 11.4, 
                    18.5, 29.4, 5.9, 21.8, 15.3, 32.6, 10.3, 23.5, 13.2, 28.7]
}

# Membuat DataFrame
df = pd.DataFrame(data)

# Fungsi untuk membuat data berkelompok
def kelompokkan_data(series, jumlah_kelas=5):
    # Menghitung interval kelas
    min_val = series.min()
    max_val = series.max()
    rentang = max_val - min_val
    lebar_kelas = rentang / jumlah_kelas
    
    # Membuat interval kelas
    kelas = pd.cut(series, bins=jumlah_kelas, include_lowest=True)
    
    # Membuat tabel frekuensi
    tabel_frekuensi = pd.DataFrame({
        'Interval': kelas.cat.categories.astype(str),
        'Frekuensi': kelas.value_counts(sort=False).values,
        'Proporsi': kelas.value_counts(normalize=True, sort=False).values
    }).reset_index()
    
    # Menambahkan nilai tengah interval
    tabel_frekuensi['Nilai_Tengah'] = [(interval.left + interval.right) / 2 for interval in tabel_frekuensi['Interval']]
    
    return tabel_frekuensi

# Fungsi untuk menghitung statistik deskriptif
def hitung_statistik(tabel_frekuensi):
    # Mean
    mean = np.average(
        tabel_frekuensi['Nilai_Tengah'], 
        weights=tabel_frekuensi['Frekuensi']
    )
    
    # Median (menggunakan interpolasi)
    total_frekuensi = tabel_frekuensi['Frekuensi'].sum()
    median_posisi = total_frekuensi / 2
    
    # Standar Deviasi
    variance = np.average(
        (tabel_frekuensi['Nilai_Tengah'] - mean)**2, 
        weights=tabel_frekuensi['Frekuensi']
    )
    std_dev = np.sqrt(variance)
    
    return {
        'Mean': mean,
        'Standar_Deviasi': std_dev,
    }

# Analisis untuk setiap wilayah
print("Analisis Data Penjualan Berkelompok:")
for kolom in df.columns:
    print(f"\n{kolom}:")
    tabel_frekuensi = kelompokkan_data(df[kolom])
    print("Tabel Frekuensi:")
    print(tabel_frekuensi)
    
    statistik = hitung_statistik(tabel_frekuensi)
    print("\nStatistik Deskriptif:")
    for key, value in statistik.items():
        print(f"{key}: {value:.2f}")

# Visualisasi distribusi
plt.figure(figsize=(12,8))
for i, kolom in enumerate(df.columns, 1):
    plt.subplot(2,2,i)
    sns.histplot(df[kolom], kde=True)
    plt.title(f'Distribusi {kolom}')
    plt.xlabel('Penjualan (Juta)')
    plt.ylabel('Frekuensi')

plt.tight_layout()
plt.show()