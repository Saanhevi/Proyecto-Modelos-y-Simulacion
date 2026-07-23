# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pathlib import Path

TABLA5 = {
    "untreated": 51.58,
    "treated": 15.90,
    "adultAdmit": 33.32,
    "childAdmit": 2.10,
}
FIG8 = {0.02: 1800, 0.03: 3500, 0.04: 5200, 0.05: 7000, 0.06: 8800}

STREAMS = Path(r"C:\Users\nicol\Documents\replicas_kpis_STREAMS.csv")
EXPLORA = Path(r"C:\Users\nicol\Documents\replicas_kpis_EXPLORA_prodFig8.csv")
N21 = Path(
    r"C:\Users\nicol\OneDrive - Universidad Nacional de Colombia\GENERAL\Documents\UNAL\Semestre 5\Modelos y Simulación\Informe 5\Entrega5_paquete_joint\csv\replicas_kpis_n21.csv"
)


def pi04_full(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[(df["pTransmit"].round(2) == 0.04) & (df["arrive"] >= 3900) & (df["arrive"] <= 4300)]
    return df.drop_duplicates(subset=["run_id"], keep="first").copy()


def mape_t5(df: pd.DataFrame):
    rows = []
    abs_pct = []
    for k, ref in TABLA5.items():
        m = float(df[k].mean())
        d = 100.0 * (m - ref) / ref
        abs_pct.append(abs(d))
        rows.append(
            {
                "KPI": k,
                "paper": ref,
                "media": m,
                "desv_pct": d,
                "min": float(df[k].min()),
                "max": float(df[k].max()),
                "std": float(df[k].std(ddof=1)) if len(df) > 1 else 0.0,
            }
        )
    return rows, float(np.mean(abs_pct))


def print_block(title: str, df: pd.DataFrame):
    rows, mape = mape_t5(df)
    print("=" * 64)
    print(f"{title}  n={len(df)}  MAPE Tabla5={mape:.2f}%")
    print(f"{'KPI':12} {'paper':>8} {'media':>8} {'desv%':>8} {'min':>6} {'max':>6}")
    for r in rows:
        print(
            f"{r['KPI']:12} {r['paper']:8.2f} {r['media']:8.2f} {r['desv_pct']:8.2f} "
            f"{r['min']:6.0f} {r['max']:6.0f}"
        )
    print(
        f"arrive media={df['arrive'].mean():.1f}  "
        f"(~{df['arrive'].mean()/22:.1f}/día si INTEREST=22)  "
        f"paper Tabla3 ~68.9/día"
    )
    return mape


def fig8_last_by_pi(path: Path):
    df = pd.read_csv(path)
    df = df[df["arrive"] > 500].copy()
    print("=" * 64)
    print(f"Fig.8  {path.name}  (dsToHospital vs paper)")
    abs_pct = []
    for pi, ref in FIG8.items():
        sub = df[df["pTransmit"].round(2) == pi]
        if sub.empty:
            print(f"  pi={pi:.2f}  SIN DATOS")
            continue
        val = float(sub.iloc[-1]["dsToHospital"])
        d = 100.0 * (val - ref) / ref
        abs_pct.append(abs(d))
        print(f"  pi={pi:.2f}  paper={ref:5.0f}  AL={val:7.0f}  desv={d:+6.1f}%")
    mape = float(np.mean(abs_pct)) if abs_pct else float("nan")
    print(f"MAPE Fig.8 = {mape:.2f}%")
    return mape


def main():
    s = pi04_full(STREAMS)
    b = pi04_full(N21)
    e = pi04_full(EXPLORA)

    mape_s = print_block("STREAMS (modelo con RNG independientes)", s)
    mape_b = print_block("BASE n21 del paquete (modelo anterior)", b)
    mape_e = print_block("EXPLORA_prodFig8 limpio (mismo modelo base)", e)

    mape8_s = fig8_last_by_pi(STREAMS)
    mape8_e = fig8_last_by_pi(EXPLORA)

    print("=" * 64)
    print("RESUMEN")
    print(f"  MAPE T5 STREAMS : {mape_s:.2f}%   (n={len(s)})")
    print(f"  MAPE T5 BASE n21: {mape_b:.2f}%   (n={len(b)})  [doc: ~3.7%]")
    print(f"  MAPE T5 EXPLORA : {mape_e:.2f}%   (n={len(e)})")
    print(f"  MAPE Fig.8 STREAMS: {mape8_s:.2f}%")
    print(f"  MAPE Fig.8 EXPLORA: {mape8_e:.2f}%   [doc: ~8.7%]")
    better = "SÍ" if mape_s < mape_b else "NO"
    print(f"  ¿STREAMS mejora MAPE T5 vs base? {better}  (delta={mape_s-mape_b:+.2f} pp)")


if __name__ == "__main__":
    main()
