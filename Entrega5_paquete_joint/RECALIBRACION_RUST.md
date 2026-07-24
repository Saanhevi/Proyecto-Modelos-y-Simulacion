# Por qué subió el MAPE STRESS · recalibración Rust

## Causa

Los gates SED (`p_gate≈0,00879`, `p_untreated≈0,01292`) se calibraron para
**~186 llegadas/día** (solo inject DS).

El SM añade:
- Source base **Tri(12,15,18)/día** (~+15/día)
- Inject ABM de personal (~+2–3/día)

→ ~**199–201 llegadas/día**. Con los mismos gates, untreated / treated / admits
suben casi en proporción → MAPE T5 **8,6 %** (n=200 AL).

Fig. 8 no cambia: es puro DS.

## Qué se puede tocar (fiel al artículo)

| Pieza | ¿Publicada? | Acción |
|---|---|---|
| Tri(12,15,18), ABM inject, 80 camas, DS | Sí (paper/SM) | **Mantener** |
| Gates ambulatorio / untreated | Hueco (no en paper) | **Recalibrar** |
| `p_child` | Hueco | Fino; 0,059 sigue OK |

## Barrido Rust (`sweep-stress`, 888 combos, n=40)

Baseline STRESS sin tocar gates: MAPE T5 ≈ **9,6 %** (paridad con AL 8,6 %).

**Mejor con staff≈3** (como `staffInfected` AL ≈ 2,9):

| Parámetro | Antes | Nuevo |
|---|---:|---:|
| `p_gate` (True→triage) | 0,00879 | **0,00789** |
| `p_untreated` (False) | 0,01292 | **0,01158** |
| `p_child` | 0,059 | **0,059** (sin cambio) |

Rust predice MAPE T5 ≈ **2,5 %** · Fig. 8 ≈ **8,7 %**.

CSV: `barrido_stress_rust.csv` · comando:
`cargo run --release -- sweep-stress -n 40`

## Aplicado al ALP exploratorio

En `Modelo_Hospital_Hibrido_STRESS_SM5380.alp` ya están gate/unt nuevos.  
Volver a correr `ExperimentoReplicas` (200) y contrastar.
