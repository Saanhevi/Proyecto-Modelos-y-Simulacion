# Parámetros · STRESS SM5380 (congelado)

Modelo: `Modelo_Hospital_Hibrido_STRESS_SM5380.alp`  
Validado AnyLogic n=200 · MAPE T5 **0,5 %** · Fig. 8 **4,4 %**

## Dinámica de sistemas

| Parámetro | Valor | Fuente |
|---|---:|---|
| Fórmula `forceOfInfection` | producto `c·prev·π` | SEIR / It.3 |
| N población | 123 182 | Orizaba |
| `contacRate` | **3,0** | barrido Rust Fig.8 |
| `Infective` / `Susceptible` | **4000** / **119182** | barrido Rust |
| `patientToHospital` | **0,007** | barrido Rust |
| `probabilityOfTransmission` base | 0,04 | paper |

## Discrete-event (huecos + SM)

| Parámetro | Valor | Nota |
|---|---:|---|
| Source base | Triangular(12, 15, 18)/día | SM5380 |
| Inject DS | `goToHospital` → `orizabaCovidPatients` | paper |
| Inject ABM | personal no disponible (delta 6 h) | SM snippet |
| Gate True→triage | **0,00714** | recalibrado |
| untreated \| False | **0,01048** | recalibrado |
| `p_child` | 0,059 | joint-sed |
| `kpiTreated` | DischargeInWindow | joint-sed |
| Camas / vent / prono | 80 / 50 / 50 | paper |
| chemicalAnalyst | `nChemicalAnalyst` (=4) | cableado SM |
| LOS / triage | Tablas 1–2 | sin tocar |

## Experimentos

- Warm-up 8 · horizonte 30 · interés 22  
- `ExperimentoReplicas`: **200** réplicas, streams  
- Fig. 8: π ∈ {0,02…0,06}  

Ver `RECALIBRACION_RUST.md` y `FIG8_RECALIB_RUST.md` para el proceso de búsqueda.
