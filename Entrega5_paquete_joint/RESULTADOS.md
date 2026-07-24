# Resultados · STRESS SM5380 (AnyLogic)

Fecha: 24-jul-2026 · `ExperimentoReplicas` n=200 + sensibilidad Fig. 8  
CSV: `csv/replicas_kpis_STRESS_f8_n200.csv` · `csv/fig8_flujo_diario.csv`

## Tabla 5 (π = 0,04)

| KPI | Paper | Media AL | IC 95% | Desvío |
|---|---:|---:|---|---:|
| untreated | 51,58 | **51,13** | [50,3 ; 52,0] | **−0,9 %** |
| treated | 15,90 | **16,00** | [15,5 ; 16,6] | **+0,6 %** |
| adultAdmit | 33,32 | **33,24** | [32,5 ; 34,0] | **−0,2 %** |
| childAdmit | 2,10 | **2,10** | [1,9 ; 2,3] | **+0,2 %** |
| **MAPE** | | | | **0,5 %** |

arrive ≈ **223 /día** · `staffInfected` ≈ **3,1**

## Figura 8 (ref. suplemento SM5380)

| π | Paper | Réplica | Desvío |
|---:|---:|---:|---:|
| 0,02 | 1900 | 1927 | +1,4 % |
| 0,03 | 3500 | 3148 | −10,1 % |
| 0,04 | 5200 | 4920 | −5,4 % |
| 0,05 | 7000 | 7056 | +0,8 % |
| 0,06 | 8800 | 9190 | +4,4 % |
| **MAPE** | | | **4,4 %** |

## Comparativo de escenarios

| Escenario | MAPE T5 | MAPE Fig.8 |
|---|---:|---:|
| Entrega streams (curso) | 3,0 % | 9,2 % |
| STRESS T5ok (backup) | 2,5 % | 9,2 % |
| **STRESS + DS F8 (este)** | **0,5 %** | **4,4 %** |

Gráficas: `graficas/` · regenerar con `scripts/generar_graficas.py`.
