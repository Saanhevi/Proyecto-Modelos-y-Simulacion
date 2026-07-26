# Parámetros del modelo (réplica AnyLogic)

Archivo: `Modelo_Hospital_Hibrido_COVID.alp`  
Validación: n = 200 réplicas · MAPE Tabla 5 ≈ **0,5 %** · MAPE Figura 8 ≈ **4,4 %**

## Dinámica de sistemas

| Parámetro | Valor | Fuente |
|---|---:|---|
| Fórmula `forceOfInfection` | producto `c · prev · π` | artículo / implementación |
| N población | 123 182 | Consulta propia · Secretaría de Economía (México); no numérica en el cuerpo del paper |
| `contacRate` | **3,0** | calibración del equipo |
| `Infective` / `Susceptible` iniciales | **4000** / **119182** | calibración del equipo |
| `patientToHospital` | **0,007** | calibración del equipo |
| `probabilityOfTransmission` (caso base) | 0,04 | artículo |

## Eventos discretos (área COVID)

| Parámetro | Valor | Nota |
|---|---:|---|
| Source base | Triangular(12, 15, 18) pacientes/día | suplemento del artículo |
| Inject desde DS | `goToHospital` → `orizabaCovidPatients` | artículo |
| Inject desde ABM | personal no disponible (chequeo cada 6 h) | suplemento |
| Gate True → triage | **0,00714** | calibración del equipo |
| Probabilidad untreated (rama False) | **0,01048** | calibración del equipo |
| `p_child` | 0,059 | calibración del equipo |
| Camas / ventiladores / prono | 80 / 50 / 50 | artículo |
| Tiempos de estancia | Tablas 1–2 | artículo (sin recalibrar) |

## Experimentos

- Warm-up: 8 días · horizonte: 30 · días de interés: 22  
- Réplicas (Tabla 5): **200**, π = 0,04, generadores independientes por bloque  
- Sensibilidad Figura 8: π ∈ {0,02 · 0,03 · 0,04 · 0,05 · 0,06}  
