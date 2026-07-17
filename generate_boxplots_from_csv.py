"""
generate_boxplots_from_csv.py
─────────────────────────────
Ejecutar DESPUÉS de correr ExperimentoReplicas en AnyLogic (20 réplicas).
El CSV se escribe en: C:/Users/<tu_usuario>/Documents/replicas_kpis.csv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "replicas_kpis.csv")
OUTPUT_DIR = BASE_DIR

# ── Reference values from Article Table 5 (Proposed Model) ──────────────────
ART_MEANS = {
    "kpiUntreated":    51.58,
    "kpiTreated":      15.90,
    "kpiAdultAdmit":   33.32,
    "kpiChildAdmit":    2.10,
}

# ── Style ────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 11, "axes.labelsize": 12, "axes.titlesize": 13,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
})
COLORS = {
    "rose":    "#f43f5e",
    "emerald": "#10b981",
    "blue":    "#3b82f6",
    "purple":  "#8b5cf6",
    "slate":   "#1e293b",
    "slate4":  "#475569",
    "bg":      "#f8fafc",
    "bg2":     "#f1f5f9",
}

# ── Load CSV ──────────────────────────────────────────────────────────────────
if not os.path.exists(CSV_PATH):
    print(f"ERROR: CSV not found at {CSV_PATH}")
    print("Run ExperimentoReplicas in AnyLogic first (20 replicas).")
    exit(1)

df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from CSV.")
print(df[["replica", "kpiUntreated", "kpiTreated", "kpiAdultAdmit", "kpiChildAdmit"]].to_string())

# ── Plot 1: 4 Box Plots ────────────────────────────────────────────────────────
kpi_config = [
    ("kpiUntreated",  "Pacientes No Atendidos\n(Acumulado Mes)",   COLORS["rose"],    51.58),
    ("kpiTreated",    "Pacientes Tratados\n(Media Diaria)",         COLORS["emerald"], 15.90),
    ("kpiAdultAdmit", "Adultos Admitidos\nÁrea COVID",             COLORS["blue"],    33.32),
    ("kpiChildAdmit", "Niños Admitidos\nÁrea COVID",               COLORS["purple"],   2.10),
]

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.patch.set_facecolor(COLORS["bg"])
axes = axes.flatten()

for i, (col, title, color, art_mean) in enumerate(kpi_config):
    ax = axes[i]
    ax.set_facecolor(COLORS["bg2"])
    data = df[col].dropna()

    # Box plot
    sns.boxplot(y=data, ax=ax, color=color, width=0.42,
                linewidth=2, fliersize=7,
                flierprops=dict(marker="D", markerfacecolor=color,
                                markeredgecolor="white", alpha=0.6))
    # Jitter overlay
    sns.stripplot(y=data, ax=ax, color=COLORS["slate"], alpha=0.45,
                  size=6, jitter=0.15)

    # Reference lines
    sim_mean = data.mean()
    ax.axhline(art_mean,  color="#ef4444", linestyle="--", lw=2.0,
               label=f"Media artículo ({art_mean:.2f})")
    ax.axhline(sim_mean,  color=COLORS["emerald"], linestyle="-.", lw=2.0,
               label=f"Media réplicas ({sim_mean:.2f})")

    # Diff annotation
    pct_diff = (sim_mean - art_mean) / art_mean * 100
    col_diff = COLORS["emerald"] if abs(pct_diff) < 5 else COLORS["rose"]
    ax.text(0.97, 0.07, f"Δ = {pct_diff:+.1f}%", transform=ax.transAxes,
            ha="right", va="bottom", fontweight="bold", color=col_diff,
            fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="#e2e8f0", alpha=0.92))

    # Stats box
    q1, q3 = data.quantile(0.25), data.quantile(0.75)
    stats_text = (f"n = {len(data)}\n"
                  f"Med = {data.median():.1f}\n"
                  f"IQR = [{q1:.1f}, {q3:.1f}]\n"
                  f"Rango = [{data.min():.0f}, {data.max():.0f}]")
    ax.text(0.97, 0.97, stats_text, transform=ax.transAxes,
            va="top", ha="right", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor="#cbd5e1", alpha=0.92))

    ax.set_title(title, fontweight="bold", color=COLORS["slate"], pad=10)
    ax.set_ylabel("Cantidad de Pacientes", fontsize=10)
    ax.set_xlabel("")
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)

    for spine in ax.spines.values():
        spine.set_edgecolor("#cbd5e1")

fig.suptitle(
    "Distribución de KPIs Clave — 20 Réplicas (Modelo Propuesto Híbrido)\n"
    "Validación vs. Estadísticos Reportados en Tabla 5 del Artículo",
    fontweight="bold", fontsize=15, color=COLORS["slate"], y=1.01
)
plt.tight_layout()
out1 = os.path.join(OUTPUT_DIR, "kpis_boxplot_real.png")
plt.savefig(out1, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"\n[OK] Box plots saved: {out1}")


# ── Plot 2: Validation comparison bar chart ─────────────────────────────────
all_kpis = [
    ("kpiArriveCovid",    "Llegadas\nCOVID/día",      68.867, "#3b82f6"),
    ("kpiTriageResp",     "Triage\nResp./día",          8.133, "#8b5cf6"),
    ("kpiUntreated",      "No Atendidos\n/día",          5.000, "#f43f5e"),
    ("kpiWaitAvg",        "Espera media\n(días)",         6.433, "#f59e0b"),
    ("kpiDischargeCovid", "Egresos COVID\n(mes)",        72.300, "#10b981"),
    ("kpiAdultAdmit",     "Adultos\nCOVID (mes)",        33.320, "#06b6d4"),
    ("kpiChildAdmit",     "Niños\nCOVID (mes)",           2.100, "#a855f7"),
]

labels   = [c[1] for c in all_kpis]
hist_avg = [c[2] for c in all_kpis]
rep_avg  = [df[c[0]].mean() for c in all_kpis]
rep_ci   = [1.96 * df[c[0]].std() / np.sqrt(len(df)) for c in all_kpis]
diff_pct = [(r-h)/h*100 for r, h in zip(rep_avg, hist_avg)]

x     = np.arange(len(labels))
width = 0.32

fig, ax = plt.subplots(figsize=(14, 7.5))
fig.patch.set_facecolor(COLORS["bg"])
ax.set_facecolor(COLORS["bg2"])

b1 = ax.bar(x - width/2, hist_avg, width,
            label="Datos Históricos (Artículo)", color="#64748b", alpha=0.82)
b2 = ax.bar(x + width/2, rep_avg,  width,
            label="Réplicas AnyLogic (n=20)",    color="#06b6d4", alpha=0.88)
ax.errorbar(x + width/2, rep_avg, yerr=rep_ci,
            fmt="none", ecolor=COLORS["slate"], elinewidth=2, capsize=5,
            label="IC 95%")

# Labels inside bars
for rect, val in zip(b1, hist_avg):
    ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.8,
            f"{val:.1f}", ha="center", fontsize=8.5, fontweight="bold", color=COLORS["slate4"])
for rect, val in zip(b2, rep_avg):
    ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.8,
            f"{val:.1f}", ha="center", fontsize=8.5, fontweight="bold", color=COLORS["slate"])

# Diff % annotations
for idx, pct in enumerate(diff_pct):
    col_t = COLORS["emerald"] if abs(pct) < 5 else COLORS["rose"]
    ymax  = max(hist_avg[idx], rep_avg[idx] + rep_ci[idx]) * 1.08
    ax.annotate(f"{pct:+.1f}%", xy=(idx, ymax), ha="center", va="bottom",
                fontweight="bold", color=col_t, fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="#e2e8f0", alpha=0.9))

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10.5, fontweight="bold")
ax.set_ylabel("Promedio (Período)", fontweight="bold", fontsize=12)
ax.set_title("Validación Cruzada: Histórico vs. Réplicas AnyLogic\n"
             "(n = 20 réplicas, IC 95%, datos reales exportados del modelo)",
             fontweight="bold", fontsize=14, pad=14)
ax.set_ylim(0, max(hist_avg) * 1.28)
ax.legend(loc="upper right", fontsize=10, framealpha=0.9)
for sp in ax.spines.values():
    sp.set_edgecolor("#cbd5e1")

plt.tight_layout()
out2 = os.path.join(OUTPUT_DIR, "validation_comparison_real.png")
plt.savefig(out2, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()
print(f"[OK] Comparison bar chart saved: {out2}")
print("\n=== Done! Run in AnyLogic, then execute this script. ===")
