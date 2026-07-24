# Material suplementario · Meza-Palacios et al. (2026)

Fuente: `tjsm_a_2610014_sm5380.pdf` (STRESS guidelines · Monks et al., 2019).  
Complementa el manuscrito con lógica, datos, experimentación e implementación.

## Hallazgos útiles (no siempre en el paper)

### Figura 8 — flujo medio a hospital (SD)
| probabilityOfTransmission | Pacientes a hospital (SM) | Valor usado antes (lectura Fig. 8) |
|---:|---:|---:|
| 0.02 | **1900** | 1800 |
| 0.03 | 3500 | 3500 |
| 0.04 | 5200 | 5200 |
| 0.05 | 7000 | 7000 |
| 0.06 | 8800 | 8800 |

→ Actualizamos la referencia paper a **1900** en π=0.02. MAPE Fig. 8 pasa de ~8,7 % a ~**9,2 %** (misma réplica).

### Tabla 5 — departamento COVID (propuesto vs inicial)
| KPI | Inicial | Propuesto |
|---|---:|---:|
| Untreated | 90,5 | **51,58** |
| Treated | 12,68 | **15,9** |
| Adults admitted | 19,48 | **33,32** |
| Children admitted | 4,1 | **2,10** |

### Tabla 3 — hospital completo (histórico vs propuesto)
| KPI | Histórico µ | Propuesto µ |
|---|---:|---:|
| Arrive Covid | 68,867 | 66,680 |
| Respiratory Triage | 8,133 | 7,942 |
| Untreated | 5,000 | 4,864 |
| Patients waiting | 6,433 | 6,137 |

### Llegadas DES modificado
- Source base: **Triangular(12, 15, 18) pacientes/día**
- Además: `OrizabaCovidPatient.inject()` (desde SD) y `medicalstaffCovidPatient1.inject()` (desde ABM)

### ABM — personal no disponible (promedio)
- COVID nurses ≈ **3** · Physicians ≈ **3** · Nurse auxiliaries ≈ **4**

### Código ABM (Physician) — snippet STRESS
`eventPhysician`: si hay médicos no disponibles → `medicalstaffCovidPatient1.inject(...)` y `covidPhysicians.set_capacity(physicianCovidsStat())`.  
Replicar lógica para enfermeras y auxiliares.

### Rigor / experimentación
- Warm-up **8** días · horizonte **30** · interés **22** días
- Paper: **20** réplicas (baja varianza reportada)
- Triangulares verificadas con **Chi-cuadrado** y **Kolmogorov–Smirnov**
- Orden de ejecución: **SD → desencadenante DES → chequeo ABM** (eventos ABM cada **6 h**)
- RNG: generador por defecto de AnyLogic (nosotros añadimos streams por rúbrica del curso)
- Software: AnyLogic PLE · ~1248 s / corrida media · 1,3 GB RAM

### Datos
Hospital 2021 = IMSS + Secretaría de Salud (México). Acceso público sujeto a autorización; portal SINAVE: https://www.sinave.gob.mx/

### Alcance del modelo
Código del paper **no es público** (requiere autorización IMSS + ITO).
