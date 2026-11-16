import numpy as np
import pandas as pd
import xarray as xr

# 1. Baca kedua file NetCDF
ds_1 = xr.open_dataset("Average Wave/1-8des_Wave.nc")
ds_2 = xr.open_dataset("Average Wave/9-16_Wave.nc")

# 2. Gabungkan berdasarkan dimensi waktu
ds_gabungan = xr.concat([ds_1, ds_2], dim="time")
var_name = [v for v in ds_gabungan.data_vars if v not in ["crs", "spatial_ref"]][0]

# 3. Ambil data perairan valid (buang daratan NaN & lepas koordinat lat/lon)
df_ocean = ds_gabungan[var_name].to_dataframe().reset_index().dropna(subset=[var_name])

# 4. Ubah tanggal menjadi kode urutan angka (0, 1, 2, ..., 15)
time_encoded, _ = pd.factorize(df_ocean["time"], sort=True)

# 5. Transformasi Logaritma (log1p = ln(1 + x) agar aman dari nilai 0)
hs_vals = df_ocean[var_name].values
hs_log = np.log1p(hs_vals)

df_log = pd.DataFrame({
    "time_step": time_encoded,
    "hs_log": np.round(hs_log, 6)
})

# 6. Acak urutan baris (atau ambil sampel) agar posisi grid spasial asli tidak bisa dilacak
df_github_safe = df_log.sample(frac=1, random_state=42).reset_index(drop=True)

# 7. Simpan ke CSV baru
df_github_safe.to_csv("dataset_gelombang_log.csv", index=False)
print("Total baris tersimpan:", len(df_github_safe))
print(df_github_safe.head(10).to_string(index=False))