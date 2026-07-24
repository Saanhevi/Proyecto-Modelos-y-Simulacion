# Intento mejorar Fig. 8 sin romper Tabla 5

## Respuesta corta

**Sí, parcialmente:** Fig. 8 es DS (`c`, `I₀`, `p2h`); Tabla 5 es SED (gates).  
Si subes el flujo DS y **recalibras gates** al nuevo arrive, puedes bajar Fig. 8
manteniendo T5 bajo.

## Backup

Modelo T5 OK (MAPE T5 2,5 % / F8 9,2 %) congelado en:

`../exploracion_STRESS_SM5380_T5ok/`

## Barrido Rust (`sweep-stress-ds`, 1089 combos)

Con STRESS (Tri+staff) + auto-gates, filtro **T5 ≤ 3,5 %**, minimizar F8:

| | c | I₀ | p2h | gate | unt | T5 | F8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline T5ok | 2,65 | 3400 | 0,009 | 0,00789 | 0,01158 | ~2,5 %* | 9,2 % |
| **Elegido** | **3,0** | **4000** | **0,007** | **0,00714** | **0,01048** | **~1,9 %** | **~4,4 %** |

\*AnyLogic n=200; Rust baseline con auto-gate ~3,9 % (ruido n).

Validación Rust `stress-sm-f8` n=80:

| π | Paper SM | Flujo | Desvío |
|---:|---:|---:|---:|
| 0,02 | 1900 | 1926 | +1,4 % |
| 0,03 | 3500 | 3147 | −10,1 % |
| 0,04 | 5200 | 4919 | −5,4 % |
| 0,05 | 7000 | 7055 | +0,8 % |
| 0,06 | 8800 | 9189 | +4,4 % |
| **MAPE** | | | **4,4 %** |

## Aplicado al ALP activo

`exploracion_STRESS_SM5380/Modelo_Hospital_Hibrido_STRESS_SM5380.alp`  
→ corre `ExperimentoReplicas` + sensibilidad Fig. 8.
