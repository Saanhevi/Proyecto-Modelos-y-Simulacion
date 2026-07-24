# -*- coding: utf-8 -*-
"""
generar_graficas.py — paquete STRESS SM5380 (c=3, I0=4000, p2h=0.007)

Uso (desde scripts/):
    python generar_graficas.py

Lee csv/replicas_kpis_STRESS_f8_n200.csv y csv/fig8_flujo_diario.csv
Escribe PNG en graficas/ e img/ + resúmenes CSV/JSON.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PKG = Path(__file__).resolve().parent.parent
CSV = PKG / "csv"
OUT_G = PKG / "graficas"
OUT_I = PKG / "img"

INTEREST = 22
TABLA5 = {
    "untreated": 51.58,
    "treated": 15.90,
    "adultAdmit": 33.32,
    "childAdmit": 2.10,
}
# Material suplementario SM5380
FIG8 = {0.02: 1900, 0.03: 3500, 0.04: 5200, 0.05: 7000, 0.06: 8800}
COLORS = {
    0.02: "#4a7ab5",
    0.03: "#e07b3a",
    0.04: "#8a8a8a",
    0.05: "#d4b84a",
    0.06: "#5a9e5a",
}


def main() -> None:
    OUT_G.mkdir(exist_ok=True)
    OUT_I.mkdir(exist_ok=True)
    CSV.mkdir(exist_ok=True)

    src = CSV / "replicas_kpis_STRESS_f8_n200.csv"
    if not src.exists():
        raise SystemExit(f"Falta {src}")

    rep = pd.read_csv(src)
    rep = rep[rep["pTransmit"].round(2) == 0.04].copy()
    if "arrive" in rep.columns:
        med = float(rep["arrive"].median())
        rep = rep[(rep["arrive"] > med * 0.85) & (rep["arrive"] < med * 1.15)]

    daily = pd.read_csv(CSV / "fig8_flujo_diario.csv")
    daily["pTransmit"] = daily["pTransmit"].round(2)
    daily = daily.sort_values(["pTransmit", "day"]).drop_duplicates(
        ["pTransmit", "day"], keep="last"
    )

    rows = []
    for col, ref in TABLA5.items():
        m = float(rep[col].mean())
        sd = float(rep[col].std(ddof=1))
        se = sd / np.sqrt(len(rep))
        rows.append(
            {
                "KPI": col,
                "n": len(rep),
                "media": m,
                "IC95_lo": m - 1.96 * se,
                "IC95_hi": m + 1.96 * se,
                "std": sd,
                "paper": ref,
                "desv_pct": 100 * (m - ref) / ref,
            }
        )
    t5 = pd.DataFrame(rows)
    mape = float(t5["desv_pct"].abs().mean())
    t5.to_csv(CSV / "resumen_tabla5.csv", index=False)

    sens = []
    for pi in sorted(daily["pTransmit"].unique()):
        sub = daily[daily["pTransmit"] == pi]
        f30 = float(sub.loc[sub["day"] == sub["day"].max(), "flujoHospital"].iloc[0])
        paper = FIG8[float(pi)]
        sens.append(
            {
                "pi": float(pi),
                "flujo_d30": f30,
                "paper": paper,
                "desv_pct": 100 * (f30 - paper) / paper,
            }
        )
    ts = pd.DataFrame(sens)
    mape8 = float(ts["desv_pct"].abs().mean())
    ts.to_csv(CSV / "resumen_fig8.csv", index=False)

    # Fig.9 boxplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    cfg = [
        ("untreated", "A. No atendidos", "#e11d48"),
        ("treated", "B. Tratados", "#059669"),
        ("adultAdmit", "C. Adultos", "#2563eb"),
        ("childAdmit", "D. Niños", "#7c3aed"),
    ]
    for ax, (col, title, color) in zip(axes.ravel(), cfg):
        ax.boxplot(
            rep[col],
            patch_artist=True,
            boxprops=dict(facecolor=color, alpha=0.35),
            medianprops=dict(color=color, lw=2),
        )
        ax.axhline(TABLA5[col], color="#0f172a", ls="--", lw=1.4, label=f"Paper {TABLA5[col]}")
        ax.set_title(title)
        ax.set_xticks([1])
        ax.set_xticklabels([f"n={len(rep)}"])
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", alpha=0.3)
    fig.suptitle(f"Tabla 5 / Fig.9 — STRESS SM5380 (MAPE={mape:.2f}%)", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_G / "fig9_boxplots_tabla5.png", dpi=160, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(t5))
    cols = ["#0d9488" if abs(v) < 5 else "#e11d48" for v in t5["desv_pct"]]
    ax.bar(x, t5["desv_pct"], color=cols)
    ax.axhline(0, color="k", lw=0.8)
    ax.axhline(5, color="#94a3b8", ls=":")
    ax.axhline(-5, color="#94a3b8", ls=":")
    ax.set_xticks(x)
    ax.set_xticklabels(t5["KPI"])
    ax.set_ylabel("Desvío % vs Tabla 5")
    ax.set_title(f"Desvíos Tabla 5 (MAPE={mape:.2f}%)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_G / "desvios_tabla5.png", dpi=160, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for pi in sorted(daily["pTransmit"].unique()):
        sub = daily[daily["pTransmit"] == pi].sort_values("day")
        ax.plot(
            sub["day"],
            sub["flujoHospital"],
            "-",
            lw=2.2,
            color=COLORS.get(float(pi)),
            label=f"{pi:.2f}",
            marker="o",
            ms=3,
        )
    ax.set_xlabel("Days")
    ax.set_ylabel("Patient flow to the hospital (acum.)")
    ax.set_title("Figure 8 (réplica STRESS) — sensibilidad")
    ax.set_xlim(0, 30)
    ax.legend(title="π", loc="center left", bbox_to_anchor=(1.01, 0.5))
    ax.grid(True, axis="y", alpha=0.35)
    fig.tight_layout()
    fig.savefig(OUT_G / "fig8_flujo_vs_dias.png", dpi=160, bbox_inches="tight")
    plt.close()

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    pis = ts["pi"].tolist()
    ax.plot(pis, ts["flujo_d30"], "o-", color="#0f766e", lw=2.2, ms=9, label="Réplica STRESS")
    ax.plot(pis, [FIG8[p] for p in pis], "s--", color="#b45309", lw=2, ms=8, label="Paper/SM Fig.8")
    ax.set_xlabel("π")
    ax.set_ylabel("Flujo acum. día 30")
    ax.set_title(f"Fig. 8 escala (MAPE≈{mape8:.2f}%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_G / "fig8_escala_vs_paper.png", dpi=160, bbox_inches="tight")
    plt.close()

    aliases = {
        "fig9_boxplots_tabla5.png": "fig9_tabla5.png",
        "desvios_tabla5.png": "desvios_tabla5.png",
        "fig8_flujo_vs_dias.png": "fig8_flujo.png",
        "fig8_escala_vs_paper.png": "fig8_escala.png",
    }
    for src_name, dst in aliases.items():
        data = (OUT_G / src_name).read_bytes()
        (OUT_I / dst).write_bytes(data)

    meta = {
        "modelo": "STRESS_SM5380_f8",
        "mape_t5": round(mape, 2),
        "mape_fig8": round(mape8, 2),
        "n": int(len(rep)),
        "params": {
            "contacRate": 3.0,
            "Infective0": 4000,
            "patientToHospital": 0.007,
            "gate": 0.00714,
            "untreated_false": 0.01048,
            "p_child": 0.059,
        },
        "untreated": round(float(rep["untreated"].mean()), 2),
        "treated": round(float(rep["treated"].mean()), 2),
        "adult": round(float(rep["adultAdmit"].mean()), 2),
        "child": round(float(rep["childAdmit"].mean()), 2),
        "arrive_day": round(float((rep["arrive"] / INTEREST).mean()), 2),
        "desv": {r["KPI"]: round(float(r["desv_pct"]), 2) for _, r in t5.iterrows()},
    }
    (CSV / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("OK graficas ->", OUT_G)
    print("OK img ->", OUT_I)
    print("META", meta)


if __name__ == "__main__":
    main()
