import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import xarray as xr

# 1. Buka kedua file NetCDF secara eksplisit dan gabungkan berurutan
ds_1 = xr.open_dataset("Average Wave/1-8des_Wave.nc")
ds_2 = xr.open_dataset("Average Wave/9-16_Wave.nc")
ds_wave = xr.concat([ds_1, ds_2], dim="time")

# 2. Ambil variabel utama tinggi gelombang signifikan (hs)
var_name = [v for v in ds_wave.data_vars if v not in ["crs", "spatial_ref"]][0]

# 3. Ambil deret waktu PER JAM dari 1 titik sampel (tanpa menampilkan koordinat ke publik)
hs_series = (
    ds_wave[var_name].isel(lat=0, lon=0).to_series().dropna().sort_index()
)

# ==========================================
# 4. RINGKASAN KARAKTERISTIK DATA GABUNGAN (1-16 DESEMBER 2025)
# ==========================================
print("=== RINGKASAN KARAKTERISTIK DATA Hs (1-16 DESEMBER 2025) ===")
print(f"Rentang Waktu        : {hs_series.index.min()} s/d {hs_series.index.max()}")
print(f"Jumlah Observasi (N) : {len(hs_series)} data per jam")
print(f"Nilai Minimum        : {hs_series.min():.4f} m")
print(f"Nilai Maksimum       : {hs_series.max():.4f} m")
print(f"Rata-rata (Mean)     : {hs_series.mean():.4f} m")
print(f"Standar Deviasi      : {hs_series.std():.4f} m")

# ==========================================
# 5. UJI STASIONERITAS (AUGMENTED DICKEY-FULLER TEST)
# ==========================================
print("\n=== HASIL UJI STASIONERITAS DATA MENTAH Hs PER JAM ===")
result = adfuller(hs_series)

print(f"ADF Statistic : {result[0]:.4f}")
print(f"p-value       : {result[1]:.4f}")
print("Critical Values:")
for key, value in result[4].items():
    print(f"   {key}: {value:.4f}")

print("\n=== KESIMPULAN UJI ADF ===")
if result[1] <= 0.05:
    print("✅ Data Hs mentah STASIONER (p-value <= 0.05)")
else:
    print(
        "❌ Data Hs mentah TIDAK STASIONER (p-value > 0.05) -> Perlu"
        " Differencing (d=1)"
    )

# ==========================================
# 6. VISUALISASI DATA AKTUAL GABUNGAN 2 FILE
# ==========================================
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    hs_series.index,
    hs_series.values,
    color="#1f77b4",
    linewidth=1.3,
    marker="o",
    markersize=2.5,
    label="Tinggi Gelombang Signifikan ($H_s$)",
)

# Format Sumbu X (Tanggal)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d Des"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.xaxis.set_minor_locator(mdates.HourLocator(interval=6))

plt.title(
    "Dinamika Tinggi Gelombang Signifikan ($H_s$) Per Jam\nPerairan Laut Jawa"
    " hingga Laut Flores (1–16 Desember 2025)",
    fontsize=12,
    fontweight="bold",
)
plt.xlabel("Waktu Pengamatan (2025)", fontsize=10)
plt.ylabel("Tinggi Gelombang Signifikan $H_s$ (m)", fontsize=10)
plt.xticks(rotation=45)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(loc="upper right")

plt.tight_layout()
plt.savefig("Average Wave/grafik_data_aktual_hs.png", dpi=300)
print(
    "\nGrafik data aktual berhasil disimpan ke 'Average"
    " Wave/grafik_data_aktual_hs.png'"
)
plt.show()