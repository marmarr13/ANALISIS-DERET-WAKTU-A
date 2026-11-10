import pandas as pd
import xarray as xr

# 1. Load & gabungkan kedua file NetCDF sekaligus
# Menggunakan pattern glob (*_Wave.nc) untuk membaca 1-8des_Wave.nc dan 9-16_Wave.nc
file_pattern = "Average Wave/*_Wave.nc"
ds_wave = xr.open_mfdataset(file_pattern, combine='by_coords')

# 2. Tampilkan informasi & struktur dataset yang sudah digabung
print("=== METADATA & STRUKTUR FILE NETCDF GABUNGAN ===")
print(ds_wave)

# 3. Otomatis mengambil variabel utama ('hs')
var_name = [v for v in ds_wave.data_vars if v not in ['crs', 'spatial_ref']][0]
print(f"\nVariabel utama yang terdeteksi: '{var_name}'")

# 4. Konversi seluruh isi dataset gabungan ke Pandas DataFrame
df = ds_wave.to_dataframe().reset_index()

# 5. Bersihkan baris bernilai NaN (area daratan)
df_clean = df.dropna(subset=[var_name])

# 6. Tampilkan pratinjau data
print("\n=== PRATINJAU DATA GABUNGAN (10 Baris Pertama) ===")
print(df_clean.head(10))

# 7. Simpan hasil gabungan ke file CSV
output_csv = "Average Wave/data_wave_1-16des.csv"
df_clean.to_csv(output_csv, index=False)
print(f"\nData 16 hari berhasil digabungkan dan disimpan ke '{output_csv}'!")