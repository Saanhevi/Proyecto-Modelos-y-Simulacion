# Diagramas del modelo híbrido (DS · MBA · SED)

Réplica AnyLogic — Meza-Palacios et al. (2026).  
Modelo: `Modelo_Entrega5_Hospital_Hibrido_streams.alp`

Convención de signos (ciclos causales): **`+`** = mismo sentido · **`−`** = sentido opuesto.

---

## 1. Diagrama de ciclos causales (Dinámica de Sistemas)

Población de Orizaba (macro). El contagio refuerza la prevalencia; la hospitalización drena infectados hacia la demanda hospitalaria.

```mermaid
flowchart TB
  subgraph R1["R1 · Reforzador — contagio en la comunidad"]
    S((Susceptible S))
    I((Infective I))
    Prev[prevalenceOfInfection<br/>I / N]
    FOI[forceOfInfection<br/>c · prev · π]
    Inf[flujo infection<br/>FOI · S]
    S -->|"−"| Inf
    Inf -->|"+"| I
    I -->|"+"| Prev
    Prev -->|"+"| FOI
    FOI -->|"+"| Inf
    Inf -->|"−"| S
  end

  subgraph B1["B1 · Balanceador — demanda hospitalaria"]
    HF[hospitalFlow<br/>I · patientToHospital]
    GTH[(goToHospital<br/>stock puente)]
    I -->|"+"| HF
    HF -->|"+"| GTH
    HF -->|"−"| I
  end

  c[contacRate c] -->|"+"| FOI
  pi[π probabilityOfTransmission] -->|"+"| FOI
  N[totalPopulation N] -->|"−"| Prev
  p2h[patientToHospital] -->|"+"| HF
```

### Lectura rápida

| Ciclo | Tipo | Idea |
|---|---|---|
| **R1** | Reforzador | Más infectados → más prevalencia → más FOI → más infecciones |
| **B1** | Balanceador | Más infectados → más flujo al hospital → baja I en la comunidad |

Parámetros de entrega: \(c=2.65\), \(\pi=0.04\), \(p_{2h}=0.009\), \(N=123182\), \(I_0=3400\).

---

## 2. Tres niveles: macro · meso · micro

```mermaid
flowchart TB
  subgraph MACRO["MACRO · Dinámica de Sistemas DS"]
    direction LR
    M1[Niveles S, I]
    M2[Flujos infection / hospitalFlow]
    M3[Stock puente goToHospital]
    M1 --- M2 --- M3
  end

  subgraph MESO["MESO · Modelado basado en agentes MBA"]
    direction LR
    A1[PhysicianCovid]
    A2[NurseCovid]
    A3[AuxiliarNurse]
    A1 --- A2 --- A3
  end

  subgraph MICRO["MICRO · Simulación de eventos discretos SED"]
    direction LR
    D1[Source / inject]
    D2[Triage · gates · NEWS]
    D3[Camas · recursos · egreso]
    D1 --- D2 --- D3
  end

  MACRO -->|"① DS → SED<br/>event: goToHospital>0 → inject"| MICRO
  MESO -->|"② MBA → SED<br/>capacity ResourcePool"| MICRO
  MICRO -->|"③ SED → MBA<br/>send Infection / contacto"| MESO
  MESO -->|"④ MBA → SED<br/>staff hospitalizado como paciente"| MICRO
  MICRO -.->|"⑤ KPIs en vivo<br/>untreated, treated, admits"| UI[Dashboard / decisión]
```

| Nivel | Pregunta que responde | Objetos AnyLogic |
|---|---|---|
| **Macro DS** | ¿Cuánta gente enferma y busca hospital? | Stocks, flows, `forceOfInfection` |
| **Meso MBA** | ¿Cuánto personal sano queda? | Poblaciones + statecharts |
| **Micro SED** | ¿Quién entra, espera o se va sin atención? | Process Modeling Library |

---

## 3. Comunicación bidireccional en tiempo de ejecución

La acoplamiento **no** es post-proceso: ocurre en el mismo reloj de simulación (Borshchev, 2013).

```mermaid
sequenceDiagram
  autonumber
  participant DS as DS (macro)
  participant Ev as Event acoplador
  participant SED as SED (micro)
  participant MBA as MBA (meso)
  participant RP as ResourcePools

  Note over DS: Cada paso continuo<br/>dI/dt, dS/dt, d(goToHospital)/dt

  DS->>Ev: goToHospital aumenta<br/>(flujo hospitalFlow)
  Ev->>Ev: condición goToHospital > 0
  Ev->>DS: goToHospital−−
  Ev->>SED: orizabaCovidPatients.inject(1)
  Note over Ev,SED: ① DS → SED (demanda)

  SED->>RP: seize médico / enfermera / auxiliar
  RP->>MBA: ¿agente en Susceptible?
  MBA-->>RP: capacidad efectiva
  Note over SED,MBA: ② MBA → SED (capacidad)

  SED->>MBA: send("Infection", staff.random())
  MBA->>MBA: uniform < umbral → Infected
  MBA->>RP: set_capacity / menos disponibles
  Note over SED,MBA: ③ SED → MBA → SED (retroalimentación)

  MBA->>SED: staff hospitalizado<br/>puede inyectarse como paciente
  Note over MBA,SED: ④ MBA → SED (demanda interna)

  SED-->>SED: KPIs untreated / treated / admits
```

### Demostración matemática del acoplamiento

**① DS → SED (demanda continua → arribos discretos)**

\[
\begin{aligned}
\text{hospitalFlow} &= I(t)\cdot p_{2h} \\
\frac{d}{dt}\texttt{goToHospital} &= \text{hospitalFlow} \\
\text{si }\texttt{goToHospital}>0 &\Rightarrow
\begin{cases}
\texttt{goToHospital}\leftarrow\texttt{goToHospital}-1 \\
\texttt{inject}(1)\ \text{en SED}
\end{cases}
\end{aligned}
\]

Unidades: el stock puente convierte un **flujo continuo** (personas/día) en **entidades enteras** del process flowchart.

**② MBA → SED (capacidad)**

\[
\texttt{ResourcePool.capacity}
\;=\;
\#\{\,a\in\text{staff}: a\in\texttt{Susceptible}\,\}\quad (+ \text{ajustes de política})
\]

Si el personal se infecta, la capacidad cae **en el mismo instante de simulación** en que el statechart cambia.

**③ SED → MBA (exposición)**

\[
\mathbb{P}(\text{mensaje Infection})
\;=\;
f(\text{contacto en servicio, umbrales }0.04\text{ / }0.3,\ \texttt{rngAbm})
\]

El mensaje `send("Infection", …)` altera el meso; el meso altera el ResourcePool; el SED siente colas/timeouts → **lazo cerrado**.

**④ MBA → SED (staff como paciente)**

Agente en estado hospitalizado puede convertirse en entidad del flujo COVID → misma ruta micro que un paciente de la comunidad.

---

## 4. Flujo de procesos SED (detalle operativo)

```mermaid
flowchart LR
  SRC[orizabaCovidPatients<br/>Source / inject] --> ARR[arriveCovidPatients]
  ARR --> PT{patientType<br/>p_child ≈ 0.059}
  PT -->|adulto| TR[triageRoom2]
  PT -->|niño| TR
  TR --> TD{triageDivision<br/>gates}
  TD -->|no atiende| UNT[untreated → sinkExit]
  TD -->|atiende| NEWS{rama NEWS / severidad}
  NEWS --> BED[Seize camas / vent / prone<br/>+ personal]
  BED --> LOS[Delay LOS<br/>Tablas 1–2]
  LOS --> OUT[Discharge / sinkExit<br/>kpiTreated en ventana]
```

Gates de entrega (contables Tabla 5): triage ≈ `0.00879` · untreated ≈ `0.01292`.  
Recursos: 80 camas COVID, 50 vent, 50 prone (paper).

---

## 5. Máquina de estados MBA (personal)

```mermaid
stateDiagram-v2
  [*] --> Susceptible
  Susceptible --> Infected: mensaje Infection<br/>+ sorteo rngAbm
  Infected --> Hospitalized: severidad / política
  Infected --> Recovered: recuperación
  Hospitalized --> Recovered: egreso
  Recovered --> Susceptible: reincorporación opcional

  note right of Susceptible
    Cuenta para ResourcePool.capacity
    (médicos / enfermeras / auxiliares)
  end note

  note right of Hospitalized
    Puede acoplarse al SED
    como paciente COVID
  end note
```

---

## 6. Resumen para la rúbrica

| Criterio | Dónde se ve |
|---|---|
| Niveles macro / meso / micro | §2 |
| Ciclos causales DS | §1 |
| Diagrama de flujo de procesos | §4 |
| Comunicación bidireccional en runtime | §3 (secuencia + ecuaciones) |
| Implementación | Event `goToHospital>0` + `inject`; `send("Infection")`; capacities de pools |

Archivos relacionados: `PARAMETROS_COMPROMISO_JOINT.md`, `RESULTADOS_STREAMS.md`, `index.html` (slides 03 y 06).
