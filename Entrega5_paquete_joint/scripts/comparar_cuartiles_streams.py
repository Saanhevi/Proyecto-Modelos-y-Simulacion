# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pathlib import Path

REFS = {
    "untreated": 51.58,
    "treated": 15.90,
    "adultAdmit": 33.32,
    "childAdmit": 2.10,
}
# Rangos paper documentados en PARAMETROS (min–max de réplicas del artículo)
PAPER_RNG = {
    "untreated": (0, 131),
    "treated": (0, 42),
    "adultAdmit": (0, 62),
    "childAdmit": (0, 3),
}

S = Path.home() / "Documents" / "replicas_kpis_STREAMS.csv"
N21 = Path(
    r"C:\Users\nicol\OneDrive - Universidad Nacional de Colombia\GENERAL\Documents\UNAL\Semestre 5\Modelos y Simulación\Informe 5\Entrega5_paquete_joint\csv\replicas_kpis_n21.csv"
)


def pi04(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path)
    return d[
        (d["pTransmit"].round(2) == 0.04) & (d["arrive"].between(3900, 4300))
    ].drop_duplicates("run_id")


def summarize(d: pd.DataFrame, name: str):
    print("=" * 72)
    print(f"{name}  n={len(d)}")
    print(
        f"{'KPI':12} {'media':>7} {'desv%':>7} {'p25':>6} {'p50':>6} {'p75':>6} "
        f"{'min':>5} {'max':>5} {'IQR':>6}"
    )
    worst_abs = -1.0
    worst = None
    abs_pct = []
    for k, ref in REFS.items():
        m = float(d[k].mean())
        desv = 100.0 * (m - ref) / ref
        abs_pct.append(abs(desv))
        if abs(desv) > worst_abs:
            worst_abs = abs(desv)
            worst = (k, desv, m)
        p25, p50, p75 = d[k].quantile([0.25, 0.5, 0.75])
        print(
            f"{k:12} {m:7.2f} {desv:7.2f} {p25:6.1f} {p50:6.1f} {p75:6.1f} "
            f"{d[k].min():5.0f} {d[k].max():5.0f} {p75-p25:6.1f}"
        )
    print(f"MAPE={np.mean(abs_pct):.2f}%")
    print(f"Peor KPI vs media paper: {worst[0]}  desv={worst[1]:+.2f}%  media={worst[2]:.2f}")
    return worst, float(np.mean(abs_pct))


s = pi04(S)
b = pi04(N21)
summarize(s, "STREAMS n=200")
summarize(b, "BASE n=21")

print("=" * 72)
print("Rangos (min–max) vs paper:")
print(f"{'KPI':12} {'paper':>12} {'STREAMS':>12} {'BASE':>12}")
for k, (lo, hi) in PAPER_RNG.items():
    print(
        f"{k:12} [{lo:>3},{hi:>3}]  "
        f"[{s[k].min():.0f},{s[k].max():.0f}]".ljust(14)
        + f"  [{b[k].min():.0f},{b[k].max():.0f}]"
    )

print("=" * 72)
print("Medianas vs media paper (cuán centrada está la distribución):")
for k, ref in REFS.items():
    print(
        f"  {k:12} paper_mean={ref:.2f}  "
        f"STREAMS_p50={s[k].median():.1f}  BASE_p50={b[k].median():.1f}"
    )
