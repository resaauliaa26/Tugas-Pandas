import os
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
os.makedirs("static", exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("data_dm_jabar.csv")

# =====================
# RINGKASAN
# =====================
total_rows = len(df)
total_cols = len(df.columns)
total_kab = df["nama_kabupaten_kota"].nunique()
tahun_tersedia = sorted(df["tahun"].unique())

# Statistik deskriptif
statistik = df.describe().round(2).to_html(classes="table", border=0)

# =====================
# GRAFIK
# =====================

# BAR CHART (PINK)
df_2019 = df[df["tahun"] == 2019]
top10 = df_2019.sort_values("jumlah_penderita_dm", ascending=False).head(10)

plt.figure(figsize=(8,4))
plt.barh(
    top10["nama_kabupaten_kota"],
    top10["jumlah_penderita_dm"],
    color="#ff6f91"
)
plt.xlabel("Jumlah Penderita DM")
plt.title("Top 10 Kabupaten/Kota DM Tertinggi (2019)")
plt.tight_layout()
plt.savefig("static/bar.png")
plt.close()

# LINE CHART (BIRU)
per_tahun = df.groupby("tahun")["jumlah_penderita_dm"].sum()

plt.figure(figsize=(6,4))
plt.plot(
    per_tahun.index,
    per_tahun.values,
    marker="o",
    linewidth=3,
    color="#4d96ff"
)
plt.xlabel("Tahun")
plt.ylabel("Jumlah Penderita DM")
plt.title("Total Penderita DM per Tahun")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("static/line.png")
plt.close()

# PIE CHART (PINK–UNGU–BIRU)
def kategori(x):
    if x > 50000:
        return "Tinggi"
    elif x > 10000:
        return "Sedang"
    else:
        return "Rendah"

df_2019["kategori"] = df_2019["jumlah_penderita_dm"].apply(kategori)
pie = df_2019["kategori"].value_counts()

plt.figure(figsize=(4,4))
plt.pie(
    pie,
    labels=pie.index,
    autopct="%1.1f%%",
    colors=["#4d96ff", "#ff6f91", "#845ec2"],
    startangle=90
)
plt.title("Proporsi Kategori DM (2019)")
plt.tight_layout()
plt.savefig("static/pie.png")
plt.close()

# =====================
# ROUTE
# =====================
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        data=df.to_dict("records"),
        columns=df.columns,
        total_rows=total_rows,
        total_cols=total_cols,
        total_kab=total_kab,
        tahun=tahun_tersedia,
        statistik=statistik
    )

if __name__ == "__main__":
    app.run(debug=True)