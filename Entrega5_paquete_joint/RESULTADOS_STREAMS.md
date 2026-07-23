# Resultados · modelo streams (entrega final)

Fecha: 22-jul-2026  
Modelo: `Modelo_Entrega5_Hospital_Hibrido_streams.alp`  
Experimento: `ExperimentoReplicas` · **n = 200** · π = 0.04  

## Por qué streams
La rúbrica pide control de **semillas / streams independientes**.  
Se crearon 4 RNGs en Main (`rngSed`, `rngAbm`, `rngGate`, `rngBranch`), reinicializados en cada réplica a partir del RNG de la corrida.

El modelo sin streams (`Modelo_Entrega5_Hospital_Hibrido.alp`) queda como baseline de calibración (n=21, MAPE T5 ~3.7 %).

## Parámetros (iguales al compromiso joint)
Mismos que `PARAMETROS_COMPROMISO_JOINT.md` (producto FOI, N=123182, c=2.65, I₀=3400, p2h=0.009, π=0.04, gates, p_child=0.059, DischargeInWindow).

## Tabla 5 · n=200 (streams)

| KPI | Paper | Media AL | Desvío | p25 | p50 | p75 |
|---|---:|---:|---:|---:|---:|---:|
| untreated | 51.58 | 52.16 | +1.1 % | 48 | 52 | 57 |
| treated | 15.90 | 15.62 | −1.8 % | 13 | 16 | 18 |
| adultAdmit | 33.32 | 34.42 | +3.3 % | 30 | 34 | 38 |
| childAdmit | 2.10 | 1.98 | −5.7 % | 1 | 2 | 3 |
| **MAPE** | | | **2.99 %** | | | |

CSV: `csv/replicas_kpis_streams_n200.csv`

## Comparación rápida

| Versión | n | MAPE T5 |
|---|---:|---:|
| Baseline (1 RNG) | 21 | ~3.7 % |
| Streams (lotes de 20) | 20–21 | 4–10 % (inestable) |
| Streams | 80 | 3.8 % |
| **Streams (entrega)** | **200** | **3.0 %** |

Con n=20 el MAPE “baila”; con n=200 se estabiliza. El paper usó 20; reportamos 200 para estimar mejor las medias.

## Fig. 8
Sin cambio material vs baseline: MAPE Fig. 8 **~8.7 %** (`dsToHospital` idéntico: 1826…8834).  
CSV histórico: `csv/fig8_flujo_diario.csv` / `csv/resumen_fig8.csv`.

## Cómo reproducir
1. Abrir `Modelo_Entrega5_Hospital_Hibrido_streams.alp`
2. Correr `ExperimentoReplicas` (200 réplicas)
3. CSV en `Documents/replicas_kpis_STREAMS.csv`
4. `python scripts/generar_graficas.py` (usa `replicas_kpis_streams_n200.csv`)

Ver también `README_STREAMS.md`.
