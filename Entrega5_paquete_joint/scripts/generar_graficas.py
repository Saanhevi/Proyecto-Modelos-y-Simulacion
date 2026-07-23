# -*- coding: utf-8 -*-
"""
generar_graficas.py
-------------------
Regenera las gráficas de validación del paquete Entrega 5 a partir de los CSV
en ../csv/ y escribe PNG en ../graficas/ e ../img/ (nombres usados por index.html).

Uso (desde esta carpeta scripts/):
    python generar_graficas.py

Dependencias: pandas, numpy, matplotlib
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
TABLA3 = {
    "arrive": 68.867,
    "triage": 8.133,
    "untreated": 5.000,
    "waitAvg": 6.433,
    "discharge": 72.30,
}
FIG8 = {0.02: 1800, 0.03: 3500, 0.04: 5200, 0.05: 7000, 0.06: 8800}
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

    # Entrega final: streams independientes, n=200 (MAPE T5 ~3.0%).
    # Fallback al n21 histórico si falta el CSV streams.
    streams = CSV / "replicas_kpis_streams_n200.csv"
    src = streams if streams.exists() else (CSV / "replicas_kpis_n21.csv")
    rep_all = pd.read_csv(src)
    rep = rep_all[
        (rep_all["pTransmit"].round(2) == 0.04) & (rep_all["arrive"] > 500)
    ].copy()
    med = float(rep["arrive"].median())
    rep = rep[(rep["arrive"] > med * 0.85) & (rep["arrive"] < med * 1.15)]

    daily = pd.read_csv(CSV / "fig8_flujo_diario.csv")
    daily["pTransmit"] = daily["pTransmit"].round(2)
    daily = daily.sort_values(["pTransmit", "day"]).drop_duplicates(
        ["pTransmit", "day"], keep="last"
    )

    # resumen T5
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

    t3rows = []
    for col, hist in TABLA3.items():
        vals = rep[col] if col in ("waitAvg", "discharge") else rep[col] / INTEREST
        m = float(vals.mean())
        t3rows.append(
            {"KPI": col, "media": m, "hist": hist, "desv_pct": 100 * (m - hist) / hist}
        )
    pd.DataFrame(t3rows).to_csv(CSV / "resumen_tabla3.csv", index=False)

    # Fig.9 boxplots Tabla 5
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    cfg = [
        ("untreated", "A. No atendidos", "#e11d48"),
        ("treated", "B. Tratados", "#059669"),
        ("adultAdmit", "C. Adultos", "#2563eb"),
        ("childAdmit", "D. Ninos", "#7c3aed"),
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
    fig.suptitle(f"Tabla 5 / Fig.9 (MAPE={mape:.1f}%)", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_G / "fig9_boxplots_tabla5.png", dpi=160, bbox_inches="tight")
    plt.close()

    # desvios
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(t5))
    cols = ["#0d9488" if abs(v) < 10 else "#e11d48" for v in t5["desv_pct"]]
    ax.bar(x, t5["desv_pct"], color=cols)
    ax.axhline(0, color="k", lw=0.8)
    ax.axhline(5, color="#94a3b8", ls=":")
    ax.axhline(-5, color="#94a3b8", ls=":")
    ax.set_xticks(x)
    ax.set_xticklabels(t5["KPI"])
    ax.set_ylabel("Desvio % vs Tabla 5")
    ax.set_title(f"Desvios Tabla 5 (MAPE={mape:.1f}%)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_G / "desvios_tabla5.png", dpi=160, bbox_inches="tight")
    plt.close()

    # Fig.8 curvas
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
    ax.set_title("Figure 8 (replica) — sensibilidad")
    ax.set_xlim(0, 30)
    ax.legend(title="pi", loc="center left", bbox_to_anchor=(1.01, 0.5))
    ax.grid(True, axis="y", alpha=0.35)
    fig.tight_layout()
    fig.savefig(OUT_G / "fig8_flujo_vs_dias.png", dpi=160, bbox_inches="tight")
    plt.close()

    # Fig.8 escala
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    pis = ts["pi"].tolist()
    ax.plot(pis, ts["flujo_d30"], "o-", color="#0f766e", lw=2.2, ms=9, label="Replica")
    ax.plot(pis, [FIG8[p] for p in pis], "s--", color="#b45309", lw=2, ms=8, label="Paper Fig.8")
    ax.set_xlabel("pi")
    ax.set_ylabel("Flujo acum. dia 30")
    ax.set_title(f"Fig. 8 escala (MAPE~{mape8:.1f}%)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_G / "fig8_escala_vs_paper.png", dpi=160, bbox_inches="tight")
    plt.close()

    # Tabla 3 (contexto / trade-off; no es Fig.7 del paper)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    keys = ["arrive", "triage", "untreated", "waitAvg", "discharge"]
    labels = ["Llegadas/dia", "Triage/dia", "Untreated/dia", "WaitAvg", "Discharge"]
    hist = [TABLA3[k] for k in keys]
    ours = [float(pd.read_csv(CSV / "resumen_tabla3.csv").set_index("KPI").loc[k, "media"]) for k in keys]
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w / 2, hist, w, label="Historico Tabla 3", color="#64748b")
    ax.bar(x + w / 2, ours, w, label="Replica", color="#0d9488")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Tabla 3 — contexto (trade-off documentado)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_G / "tabla3_validacion.png", dpi=160, bbox_inches="tight")
    plt.close()

    # aliases presentation
    aliases = {
        "fig9_boxplots_tabla5.png": "fig9_tabla5.png",
        "desvios_tabla5.png": "desvios_tabla5.png",
        "fig8_flujo_vs_dias.png": "fig8_flujo.png",
        "fig8_escala_vs_paper.png": "fig8_escala.png",
    }
    for src, dst in aliases.items():
        data = (OUT_G / src).read_bytes()
        (OUT_I / dst).write_bytes(data)

    abanico = float(
        ts.loc[ts.pi == 0.06, "flujo_d30"].iloc[0]
        - ts.loc[ts.pi == 0.02, "flujo_d30"].iloc[0]
    )
    meta = {
        "mape_t5": round(mape, 2),
        "mape_fig8": round(mape8, 2),
        "n": int(len(rep)),
        "untreated": round(float(rep["untreated"].mean()), 2),
        "treated": round(float(rep["treated"].mean()), 2),
        "adult": round(float(rep["adultAdmit"].mean()), 2),
        "child": round(float(rep["childAdmit"].mean()), 2),
        "arrive_day": round(float((rep["arrive"] / INTEREST).mean()), 2),
        "abanico": round(abanico, 0),
        "desv": {r["KPI"]: round(float(r["desv_pct"]), 1) for _, r in t5.iterrows()},
    }
    (CSV / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("OK graficas ->", OUT_G)
    print("OK img presentacion ->", OUT_I)
    print("META", meta)


if __name__ == "__main__":
    main()
