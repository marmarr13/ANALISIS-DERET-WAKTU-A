import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.stattools import adfuller

# 1. Load & gabungkan data NetCDF (1-16 Desember)
file_pattern = "Average Wave/*_Wave.nc"
ds_wave = xr.open_mfdataset(file_pattern, combine='by_coords')

# 2. Ambil variabel utama tinggi gelombang (hs)
var_name = [v for v in ds_wave.data_vars if v not in ['crs', 'spatial_ref']][0]

# 3. Ambil deret waktu PER JAM dari 1 titik koordinat di lintasan (tanpa di-mean)
# isel(lat=0, lon=0) mengambil titik koordinat spesifik
hs_series = ds_wave[var_name].isel(lat=0, lon=0).to_series().dropna()
print(f"Total titik data per jam (1-16 Des): {len(hs_series)} data jam")

# 4. Uji Stasioneritas (Augmented Dickey-Fuller Test)
print("\n=== HASIL UJI STASIONERITAS DATA MENTAH Hs PER JAM ===")
result = adfuller(hs_series)

print(f"ADF Statistic : {result[0]:.4f}")
print(f"p-value       : {result[1]:.4f}")
print("Critical Values:")
for key, value in result[4].items():
    print(f"   {key}: {value:.4f}")

# 5. Kesimpulan Statistik
print("\n=== KESIMPULAN ===")
if result[1] <= 0.05:
    print("✅ Data Hs mentah STASIONER (p-value <= 0.05)")
else:
    print("❌ Data Hs mentah TIDAK STASIONER (p-value > 0.05)")

# ==========================================
# 6. VISUALISASI GRAFIK DATA JAM DENGAN LABEL TANGGAL
# ==========================================
fig, ax = plt.subplots(figsize=(14, 6))

# Plot deret waktu per jam berdasarkan index Datetime asli
ax.plot(hs_series.index, hs_series.values, color='#1f77b4', linewidth=1.2, marker='o', markersize=3, label='Hs Per Jam (m)')

# Atur Sumbu X agar menampilkan label Tanggal (1 Des, 2 Des, dst)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b')) # Format: 01 Des, 02 Des
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))   # Tampilkan tick label setiap pergantian hari

# Tambahkan minor ticks untuk menandai tiap jam di dalam hari
ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))  # Garis penanda tiap 6 jam

plt.title('Time Series Tinggi Gelombang Signifikan ($H_s$) Per Jam - Rute Surabaya - Makassar (1-16 Des)', fontsize=12, fontweight='bold')
plt.xlabel('Tanggal', fontsize=10)
plt.ylabel('Tinggi Gelombang $H_s$ (meter)', fontsize=10)
plt.xticks(rotation=45)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='upper right')

plt.tight_layout()
plt.savefig("Average Wave/grafik_timeseries_per_jam.png", dpi=300)
print("\nGrafik per jam berhasil disimpan ke 'Average Wave/grafik_timeseries_per_jam.png'")
plt.show()