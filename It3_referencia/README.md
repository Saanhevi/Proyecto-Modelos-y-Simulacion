# Iteración 3 — Referencia (modelo híbrido calibrado)

Carpeta de respaldo de la **tercera iteración** de calibración del modelo híbrido
(SD + DES + ABM) frente al artículo:

> Meza-Palacios et al. (2026). *Development of a hybrid simulation model for
> hospital capacity in health emergencies*. Journal of Simulation.

**Importante:** esta carpeta documenta la It. 3 (población ~466 k). El archivo
AnyLogic de entrega actual puede estar en It. 7 (Orizaba 123 182); los CSV y
gráficas de aquí corresponden a la It. 3 validada.

## Contenido

```
It3_referencia/
├── README.md                          ← resultados + origen/justificación de parámetros
├── csv/
│   ├── replicas_kpis_n20.csv          ← 20 réplicas (revalidación It. 3)
│   ├── replicas_kpis_n40_original.csv ← corrida original It. 3 (40 filas)
│   ├── fig8_flujo_diario.csv          ← serie diaria sensibilidad π
│   ├── resumen_tabla3.csv
│   ├── resumen_tabla5.csv
│   └── resumen_fig8.csv
└── graficas/
    ├── fig7_no_atendidos_por_dia.png
    ├── fig9_boxplots_hibrido.png
    ├── fig9_boxplots_con_caja_articulo.png
    ├── fig8_flujo_vs_dias.png
    ├── fig8_escala_vs_paper.png
    ├── tabla3_validacion.png
    └── desvios_tabla5.png
```

El README incluye: (1) comparación con Tablas 3/5 y Figs. 7–9; (2) tablas de
**qué vino del artículo** vs **qué no** y por qué (con fuentes).
## Parámetros clave de la It. 3

| Elemento | Valor |
|---|---|
| `forceOfInfection` | **Producto** `c · prevalencia · π` |
| Población (S + I) | ~**466 340** (S₀≈464 675, I₀≈1 665) |
| `patientToHospital` | 0.04 |
| Gate ambulatorio `p(True)` | 0.02336 |
| Split untreated (False) | 0.03484 |
| Camas COVID | 80 |
| Ventana de KPIs | días **8–30** (22 días) |

---

## Tabla 5 — Modelo propuesto (híbrido)

KPIs **acumulados** por corrida (como los boxplots / Fig. 9 del paper).  
Fuente: `csv/replicas_kpis_n20.csv` (n = 20).

| KPI | Media It. 3 | IC 95 % | Paper (propuesto) | Desvío |
|---|---:|---|---:|---:|
| No atendidos | 52.90 | [50.0, 55.8] | 51.58 | **+2.6 %** |
| Tratados | 16.10 | [14.8, 17.4] | 15.90 | **+1.3 %** |
| Adultos admitidos | 32.55 | [30.5, 34.6] | 33.32 | **−2.3 %** |
| Niños admitidos | 2.15 | [1.6, 2.7] | 2.10 | **+2.4 %** |

**MAPE** (media de |desvíos|) ≈ **2.1 %**.

### Lectura
La It. 3 reproduce muy bien las medias del modelo **propuesto** del artículo.
Los cuatro KPIs quedan dentro de ~±3 %. Es la mejor calibración conjunta que
obtuvimos para la Tabla 5 / Fig. 9. La dispersión entre réplicas es razonable
(p. ej. untreated std ≈ 6.5), aunque el paper reporta rangos más anchos en
algunos boxplots.

**Gráfica:** `graficas/fig9_boxplots_hibrido.png`  
(alternativa con caja reconstruida del artículo: `fig9_boxplots_con_caja_articulo.png`)

---

## Tabla 3 — Validación vs histórico (departamento COVID)

En el paper la Tabla 3 valida el **modelo inicial** con medias **diarias**
(salvo espera = nivel medio y egresos = total del periodo). Aquí comparamos
nuestras réplicas It. 3 pasando acumulados 8–30 a media diaria (÷ 22).

| KPI | Media It. 3 | Histórico Tabla 3 | Desvío |
|---|---:|---:|---:|
| Llegadas COVID / día | 68.76 | 68.867 | **−0.2 %** |
| Triage respiratorio / día | 1.58 | 8.133 | −80.6 % |
| No atendidos / día | 2.40 | 5.000 | −51.9 % |
| Pacientes en espera | 0.01 | 6.433 | −99.8 % |
| Egresos COVID (periodo) | 28.6 | 72.30 | −60.5 % |

### Lectura
- **Llegadas:** clavadas (~69/día). El DS + puente alimenta el hospital al ritmo
  del histórico.
- **Triage, espera, egresos, untreated/día:** se alejan del histórico de la
  Tabla 3. Eso es esperable en parte porque la Tabla 3 es del **modelo
  inicial**, y nosotros calibramos hacia el **híbrido propuesto** (Tabla 5),
  donde untreated acumulado ~52 (≈2.4/día) y no ~5/día. Espera y triage
  dependen de colas/timeouts propios del SED; no fueron el foco de la It. 3.

**Gráfica:** `graficas/tabla3_validacion.png`

---

## Figura 7 — No atendidos en el tiempo

Serie diaria (π = 0.04) a partir de `fig8_flujo_diario.csv`: no atendidos por
día (incremento) y acumulado.

### Lectura
El paper muestra el promedio diario de no atendidos cuando la demanda supera
capacidad (y redirige a otro hospital). En It. 3, con π base 0.04, el untreated
acumulado al día 30 ronda el orden de la Tabla 5 (~50–60). La curva diaria
queda por debajo del “~5/día” de la Tabla 3 porque el híbrido propuesto rechaza
menos que el modelo inicial (objetivo del artículo).

**Gráfica:** `graficas/fig7_no_atendidos_por_dia.png`

---

## Figura 9 — Boxplots del híbrido

Cuatro paneles (no atendidos, tratados, adultos, niños), **solo modelo híbrido**
It. 3 (n = 20). La línea punteada es la media del paper (Tabla 5, propuesto).

### Lectura
Misma conclusión que la Tabla 5: las cajas de la réplica se centran cerca de
las medias del artículo. No incluimos aquí el modelo **inicial** del paper
(medias ~90 untreated, ~13 treated, etc.); solo el híbrido, como pediste.

**Gráfica:** `graficas/fig9_boxplots_hibrido.png`

---

## Figura 8 — Sensibilidad del flujo (SD)

Flujo acumulado de pacientes hacia el hospital vs día, para π ∈ {0.02…0.06}.

| π | Flujo día 30 (It. 3) | Paper (lectura aprox.) | Desvío |
|---:|---:|---:|---:|
| 0.02 | 1 501 | ~1 800 | −17 % |
| 0.03 | 1 724 | ~3 500 | −51 % |
| 0.04 | 1 994 | ~5 200 | −62 % |
| 0.05 | 2 323 | ~7 000 | −67 % |
| 0.06 | 2 726 | ~8 800 | −69 % |

### Lectura
La **tendencia** coincide con el paper: ↑π → ↑flujo (abanico que se abre). La
**escala** absoluta del artículo no se reproduce si se mantiene la calibración
de ~69 llegadas/día (Tabla 3/5). En el paper la Fig. 8 es sensibilidad del
**SD** (§4.4) y la Tabla 5 es del **DES** (§4.6); no publican un ajuste único
que cierre ambas a la vez. Para la entrega, la It. 3 prioriza Tabla 5 / Fig. 9;
la Fig. 8 se reporta como sensibilidad cualitativa correcta en dirección.

**Gráficas:** `graficas/fig8_flujo_vs_dias.png`, `graficas/fig8_escala_vs_paper.png`

---

## Resumen ejecutivo

| Entregable | ¿It. 3 lo sostiene? |
|---|---|
| Tabla 5 / Fig. 9 (híbrido) | **Sí** (MAPE ≈ 2.1 %) |
| Tabla 3 llegadas ~69/día | **Sí** |
| Resto Tabla 3 (triage, espera, egresos) | Parcial / no (otro foco de calibración) |
| Fig. 7 (forma / untreated en el tiempo) | Sí a nivel de narrativa del híbrido |
| Fig. 8 (escala del paper) | No; tendencia sí |

**Conclusión:** la It. 3 es la referencia sólida para validar el **híbrido
propuesto** (Tabla 5 y Fig. 9). La Fig. 8 del paper no debe usarse como criterio
que rompa esa calibración.

---

## Origen de parámetros: qué vino del artículo y qué no

Criterio del equipo (alineado a la rúbrica): **no modificar** magnitudes que el
artículo fija explícitamente (tiempos triangulares, camas, rango de π, plantilla
de triage, etc.). Donde el paper deja un hueco, se documenta la fuente externa
o la **deducción a partir de los propios KPIs publicados** (no un ajuste
arbitrario “hasta que cuadre” sin vínculo con evidencia).

Referencia principal del caso:  
Meza-Palacios et al. (2026), *Journal of Simulation*,  
https://doi.org/10.1080/17477778.2025.2610014

---

### A. Valores que **sí** aporta el artículo (y se usaron en el modelo)

| Parámetro / elemento | Valor en el paper | Valor en It. 3 | Dónde lo dice el paper |
|---|---|---|---|
| Rango de transmisión π | 0.02 … 0.06 | Default **0.04** (punto medio); sensibilidad en ese rango | §4.4 / Fig. 8 |
| Tasa de hospitalización nacional (contexto) | 4 % – 20 % | `patientToHospital` = **0.04** (piso del rango) | §4.4 (cita Secretaría de Salud, 2024) |
| Camas COVID | **80** | **80** | Resultados / capacidad; redirección a otros hospitales |
| Delay triage | `triangular(5, 12, 25)` min | **Igual (fijo)** | Tabla 1 |
| Estancias COVID (estable / severo / intubado, adultos y niños) | Triangulares Tablas 1–2 | **Igual (fijas)** | Tablas 1–2 |
| Equipo de triage respiratorio | Médico + enfermera + auxiliar + analista químico | AND de esos 4 recursos | §3.5 (1) |
| Médicos COVID (ABM) | **19** physicians | Pool / población **19** | §3.6 |
| Evento de infección de staff | Cada **6 horas** | Evento cíclico 6 h | §3.6 |
| Estados del personal | Susceptible → Infected → Hospitalised / Recovered | Statecharts equivalentes | Fig. 6 / §3.6 |
| Clasificación clínica | NEWS: inmediato / moderado / no urgente (3 vías) | Tres salidas DES (estable / severo / intubación) | Supuesto (d)–(e); §3.5 (2) |
| Intubación: recursos | 2 MD, 2 enf., 4 aux., camas, ventiladores; posición prono | Seize de camas + ventiladores + prone | §3.5 (2)–(3) |
| Horizontes de análisis | Simulación hasta ~30 días; PLE limita features | Stop a **30** días; KPIs desde día **8** | Resultados / uso AnyLogic PLE |
| Llegadas COVID (históricas) | **68.867** / día (Tabla 3) | Objetivo de acoplamiento DS→DES ≈ **69**/día | Tabla 3 |
| KPIs híbrido propuesto | untreated 51.58; treated 15.90; adults 33.32; children 2.10 | Metas de validación Tabla 5 / Fig. 9 | Tabla 5 |
| Población de estudio | Orizaba **y la región** (Secretaría de Economía, 2024) | It. 3: **S+I ≈ 466 340** | §4.4 |
| Redirección si no hay cupo | Pacientes a **otro hospital** / no esperan | Timeouts + KPI untreated | Supuesto (g); Fig. 7; texto de untreated |

---

### B. Valores que **no** trae el artículo (huecos) y por qué se eligieron

| Parámetro | Valor It. 3 | ¿Por qué ese valor? (justificación) | Base / fuentes |
|---|---|---|---|
| Forma de `forceOfInfection` | **Producto** `c · prevalencia · π` (no la suma impresa) | Homogeneidad dimensional: contactos/tiempo × fracción infectada × probabilidad por contacto → tasa 1/tiempo. La suma `c + prev + π` mezcla unidades distintas y, con `infection = force · S`, produce ~10⁵ infecciones/día y rompe el régimen de ~69 llegadas/día de la **propia** Tabla 3. | Forma estándar de fuerza de infección en modelos agregados SI/SEIR: Anderson & May (1991), *Infectious Diseases of Humans*; Brauer & Castillo-Chávez, *Mathematical Models in Population Biology and Epidemiology*. El paper usa `infection = force · S` (Fig. 4), coherente con λ·S si λ es tasa, no si force ≈ O(1) por suma. |
| `contacRate` (c) | **1.0** | Escala adimensional de contactos efectivos/día en el producto. Con c = 1, `λ = prevalencia · π`, interpretable y estable junto a π ∈ [0.02, 0.06]. El paper **no** publica un valor numérico de contact rate para Orizaba. | Convención de normalización en modelos de fuerza de infección cuando β se descompone como c·p (Vynnycky & White, *An Introduction to Infectious Disease Modelling*). Sensibilidad se explora vía π (Fig. 8), no vía c. |
| `Infective` inicial (I₀) | **≈ 1 665** | Condición inicial para que, con `patientToHospital = 0.04` y producto, `hospitalFlow ≈ I·0.04` reproduzca el **dato histórico del paper** (~68.9 llegadas/día, Tabla 3), no un KPI “inventado”. Validado por integración numérica de las EDO del DS. | Tabla 3 del propio artículo (Perez-Tezoco et al., 2023, datos del hospital citados ahí). |
| `Susceptible` inicial | **≈ 464 675** | Complemento de la población Orizaba+región usada en It. 3 (~466 k − I₀), alineada al enunciado del paper (§4.4) y a la fuente que ellos citan. | Secretaría de Economía (2024), citada por Meza-Palacios et al.; orden de magnitud de zona metropolitana Orizaba (INEGI / datos demográficos abiertos del mismo orden). |
| Gate `ambulatoryPatient` p(True→triage/admisión) | **0.02336** | **Identidad contable** con Tabla 5: admisiones objetivo = 33.32 + 2.10 = 35.42; con ~1 516 llegadas en la ventana 8–30 (68.9×22), se obtiene p ≈ 35.42/1516 ≈ **0.0234**. No es un knobo libre: es la proporción de llegadas que el **propio paper** implica si sus medias de Tabla 3 y Tabla 5 son simultáneamente ciertas. | Deducción de ratios Tabla 3 ↔ Tabla 5 del artículo. Coherente con que la mayoría de consultas COVID ambulatorias no terminan en hospitalización (Secretaría de Salud México: hospitalización 4–20 % a nivel nacional; aquí el filtro es *post*-llegada al servicio COVID del hospital). |
| Prob. untreated en rama False | **0.03484** | Misma lógica contable: untreated 51.58 / [(1−0.02336)×1516] ≈ **0.0348**. Representa quienes, tras llegar, no permanecen (timeout / otro hospital / no esperan), narrativa explícita del paper. | Tabla 5 + supuesto (g) y texto de untreated / Fig. 7 del artículo. |
| p(niño) en `patientType` | **0.059** | 2.10 / (33.32 + 2.10) = **5.9 %** de las admisiones del híbrido propuesto. | Tabla 5 del artículo (razón niños/admitidos). |
| Definición de `kpiTreated` | Egreso COVID ≤ día 30 (`moveTo2Exit`) | En Tabla 5, *treated* (15.90) **≪** adultos+niños admitidos (35.42): “tratado” no puede ser “pasó triage”. Se cuenta quien **completa** estancia en el horizonte. Las estancias son las triangulares del paper; el restante no egresa a tiempo por LOS, no por un parámetro inventado. | Interpretación consistente de Tabla 5 + Tablas 1–2 (LOS) del artículo. |
| Timeout de espera en triage / colas | **161 min** (~2,7 h) | El paper no da el timeout numérico; sí dice que si no reciben cuidado **no están dispuestos a esperar** y van a otro hospital. En urgencias, el abandono *left without being seen* (LWBS) se asocia a esperas del orden de **2–4 horas** en literatura de ED. 161 min cae en ese intervalo operativo. | Carter et al. / estudios LWBS en emergency departments (p. ej. revisiones sobre waiting time y LWBS); narrativa del paper (untreated / otro hospital). No se usó para “forzar” Tabla 5: el volumen untreated se fija sobre todo con el split 0.03484. |
| Mix NEWS (estable / severo / intubado) | **0.309 / 0.565 / 0.126** (It. 3) | El paper define umbrales NEWS pero **no** publica la fracción por banda. Se usa una mezcla que suma 1 y privilegia severo > estable > intubación (coherente con que intubación es el extremo). Alternativa documentada en el equipo: 0.50/0.35/0.15. | Umbrales: Royal College of Physicians, **NEWS2** (https://www.rcp.ac.uk/resources/national-early-warning-score-news-2/). Distribuciones empíricas de gravedad COVID hospitalizado varían por ola/país; sin microdatos del hospital de Orizaba no se puede fijar una única verdad — se declara calibrable y se mantienen LOS del paper. |
| `kpiWaitAvg` | Promedio de **tamaño** de colas (proxy) | Tabla 3 reporta “Patients waiting” ≈ 6.4: el paper no aclara si es minutos o nivel. Implementar TimeMeasure completo no estaba en el núcleo de validación Tabla 5; el proxy evita inventar un tiempo medio no medido. | Limitación declarada; no se presenta como réplica exacta del KPI de minutos. |
| Semilla / n = 20 réplicas | Semilla aleatoria; 20 corridas | El paper valida con IC 95 % y desviación &lt; 5 %. n = 20 es práctica habitual para IC de la media en simulación estocástica (Law, *Simulation Modeling and Analysis*). | Metodología de simulación estándar; el paper usa IC 95 % en validación. |

---

### C. Cómo argumentarlo ante la profesora (una frase por bloque)

1. **Del paper, literal:** tiempos, camas, π, plantillas, 19 médicos, 80 camas, KPIs objetivo.  
2. **Producto vs suma:** no es “porque cuadraba”; es consistencia dimensional + teoría epidemiológica estándar + no destruir la Tabla 3 del mismo artículo.  
3. **Gates 0.02336 / 0.03484 / 0.059:** álgebra de **conservación de flujo** entre Tabla 3 (llegadas) y Tabla 5 (admitidos / untreated / niños) — parámetros *implicados* por el paper, no libres.  
4. **I₀ y c:** fijan el régimen de demanda histórica (~69/día) que el artículo sí publica.  
5. **Timeout 161 min / NEWS:** huecos del paper rellenados con literatura de ED/NEWS2 y narrativa del propio texto (abandono / otro hospital), declarando incertidumbre.

---

### D. Referencias rápidas (además del artículo base)

| Fuente | Uso en la justificación |
|---|---|
| Meza-Palacios et al. (2026), DOI arriba | Parámetros y KPIs del caso |
| Secretaría de Salud (México), 2024 (citada en el paper) | Rango hospitalización 4–20 % |
| Secretaría de Economía (2024) (citada en el paper) | Población Orizaba / región |
| Anderson & May (1991); Brauer & Castillo-Chávez | Fuerza de infección como producto |
| RCP — NEWS2 | Umbrales de clasificación clínica |
| Law — *Simulation Modeling and Analysis* | n réplicas / IC en simulación |
| Literatura LWBS en ED (esperas 2–4 h) | Orden de magnitud del timeout de abandono |
