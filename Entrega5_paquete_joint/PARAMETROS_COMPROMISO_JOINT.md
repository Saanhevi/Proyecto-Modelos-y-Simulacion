# Snapshot · Compromiso joint-sed (AnyLogic validado)

Fecha: 19-jul-2026  
Modelo: `exploracion_Fig8_producto/Modelo_exploracion_Fig8_producto.alp`  
Corrida: réplicas n=21 (π=0.04) + ParametersVariation Fig. 8  

**Este es el mejor punto validado en AnyLogic hasta la fecha** (MAPE T5 **7.8%**, Fig. 8 **8.7%**).  
Los tres KPIs principales (untreated / treated / adultAdmit) quedan a &lt;3 % del paper.

---

## Parámetros que produjeron estos resultados

| Parámetro | Valor | Notas |
|---|---:|---|
| Fórmula `forceOfInfection` | producto `c·prev·π` | Hueco (paper imprime suma) |
| N población | 123 182 | Orizaba ciudad |
| `contacRate` | **2.65** | Hueco |
| `Infective` / `Susceptible` | **3400** / **119782** | |
| `patientToHospital` | **0.009** | |
| `probabilityOfTransmission` base | 0.04 | Rango paper 0.02–0.06 |
| Gate True→triage | **0.00879** | Contable T5 |
| untreated \| False | **0.01292** | Contable T5 |
| `patientType` p(niño) | **0.070** | Hueco (esta corrida) |
| `kpiTreated` | **DischargeInWindow** | Egreso en [8,30] si ocupó cama COVID |
| NEWS | 0.309 / 0.565 / 0.126 | Sin cambio |
| Timeout triage | 161 min | |
| Camas / vent / prone | 80 / 50 / 50 | Camas = paper |
| LOS / triage delay | Tablas 1–2 paper | **No tocados** |

Preset Rust equivalente: `compromiso-joint-sed` (con `p_child=0.070` en esta corrida).

---

## Resultados AnyLogic

### Tabla 5 (n=21, π=0.04)

| KPI | Paper | Media AL | IC95 | Desvío | Rango AL | Rango paper |
|---|---:|---:|---|---:|---|---|
| untreated | 51.58 | **51.52** | [48.8, 54.2] | **−0.1 %** | 39–63 | 0–131 |
| treated | 15.90 | **15.62** | [14.2, 17.1] | **−1.8 %** | 7–21 | 0–42 |
| adultAdmit | 33.32 | **34.10** | [32.0, 36.2] | **+2.3 %** | 26–44 | 0–62 |
| childAdmit | 2.10 | 2.67 | [1.9, 3.4] | +27.0 % | 0–6 | 0–3 |
| **MAPE** | | | | **7.8 %** | | |

### Fig. 8 (flujo acum. día 30)

| π | Paper | AnyLogic | Desvío |
|---:|---:|---:|---:|
| 0.02 | 1800 | 1825 | **+1.4 %** |
| 0.03 | 3500 | 2849 | −18.6 % |
| 0.04 | 5200 | 4393 | −15.5 % |
| 0.05 | 7000 | 6460 | −7.7 % |
| 0.06 | 8800 | 8834 | **+0.4 %** |
| **MAPE** | | | **8.7 %** |

Abanico (π0.06−π0.02) ≈ **7008** (paper ~7000).

### Tabla 3 (contexto)

Arrive ≈ **185.6**/día vs paper **68.9** — trade-off consciente para clavar Fig. 8 + Tabla 5.

---

## Evolución de calibración

| Etapa | MAPE T5 | treated | childAdmit | Fig.8 |
|---|---:|---:|---:|---:|
| joint (gates It.3) | 10.2 % | −22 % | +13 % | 8.7 % |
| SED DischargeInWindow + p=0.05 | 8.5 % | −9 % | −21 % | 8.7 % |
| **SED + p=0.07 (este snapshot)** | **7.8 %** | **−1.8 %** | +27 % | **8.7 %** |

CSV fuente de esta corrida (backup mental): medias arriba.  
Figuras: `boxplots_tabla5_EXPLORA_prodFig8.png`, `fig8_*_EXPLORA_prodFig8.png`.

---

## Siguiente paso documentado

Afinar solo `p_child` (bajar desde 0.070) para acercar childAdmit a 2.10 sin romper treated/untreated/adult.  
Interpolación empírica AL: 0.050→1.67, 0.070→2.67 ⇒ objetivo 2.10 ≈ **p_child ≈ 0.059**.

### Aplicado 19-jul-2026 (post-snapshot)

- `patientType` **0.070 → 0.059** (Rust + predicción AL).
- Snapshot de la corrida p=0.07 **conservado arriba** como referencia del mejor treated/untreated/adult.

### Validación AL p_child=0.059 (n=21) — **mejor MAPE T5 a la fecha**

| KPI | Paper | Media AL | Desvío |
|---|---:|---:|---:|
| untreated | 51.58 | 53.76 | +4.2 % |
| treated | 15.90 | 16.38 | **+3.0 %** |
| adultAdmit | 33.32 | 34.81 | +4.5 % |
| childAdmit | 2.10 | 1.90 | **−9.3 %** |
| **MAPE T5** | | | **5.3 %** |
| MAPE Fig.8 | | | **8.7 %** (igual) |

Parámetros finales del escenario exploración: los de la tabla superior con **p_child=0.059** y DischargeInWindow.

### Revalidación 19-jul-2026 (misma config, `goToHospital > 0`) — **MAPE T5 3.7 %**

| KPI | Paper | Media AL | Desvío |
|---|---:|---:|---:|
| untreated | 51.58 | 52.81 | **+2.4 %** |
| treated | 15.90 | 15.19 | **−4.5 %** |
| adultAdmit | 33.32 | 33.67 | **+1.0 %** |
| childAdmit | 2.10 | 1.95 | **−7.0 %** |
| **MAPE T5** | | | **3.7 %** |
| MAPE Fig.8 | | | **8.7 %** |

Misma configuración; la diferencia vs 5.3 % es ruido Monte Carlo (n=21). **Congelar baseline aquí.**

### Entrega final 22-jul-2026 — streams independientes · **MAPE T5 3.0 % (n=200)**

Misma parametrización + 4 RNGs (`rngSed` / `rngAbm` / `rngGate` / `rngBranch`).  
Ver `RESULTADOS_STREAMS.md` y `Modelo_Entrega5_Hospital_Hibrido_streams.alp`.

| KPI | Paper | Media AL (n=200) | Desvío |
|---|---:|---:|---:|
| untreated | 51.58 | 52.16 | **+1.1 %** |
| treated | 15.90 | 15.62 | **−1.8 %** |
| adultAdmit | 33.32 | 34.42 | +3.3 % |
| childAdmit | 2.10 | 1.98 | −5.7 % |
| **MAPE T5** | | | **3.0 %** |
| MAPE Fig.8 | | | **8.7 %** |

### Pasada final (enteros + gate×1.05) — validado AL n=21

| KPI | Paper | gate 0.00879 | **gate 0.00923 + enteros** |
|---|---:|---:|---:|
| untreated | 51.58 | +4.2 % | **−0.1 %** |
| treated | 15.90 | +3.0 % | **+0.0 %** |
| adultAdmit | 33.32 | +4.5 % | +6.0 % |
| childAdmit | 2.10 | **−9.3 %** | +20.2 % |
| **MAPE T5** | | **5.3 %** | 6.6 % |
| MAPE Fig.8 | | 8.7 % | 8.7 % |

`treated`/`untreated` quedaron perfectos; subió adult/child y el MAPE empeoró vs la corrida anterior.  
**Mejor MAPE sigue siendo gate=0.00879 + p_child=0.059 + DischargeInWindow** (5.3 %). Enteros en `goToHospital` no movieron Fig. 8.

### Última prueba p_child=0.062 — **rechazada** (n=21)

| KPI | Paper | Media AL | Desvío | vs p=0.059 |
|---|---:|---:|---:|---|
| untreated | 51.58 | 54.19 | +5.1 % | similar |
| treated | 15.90 | 14.90 | −6.3 % | peor |
| adultAdmit | 33.32 | 32.48 | −2.5 % | ok |
| childAdmit | 2.10 | **3.05** | **+45 %** | sobrepasó |
| **MAPE T5** | | | **14.7 %** | vs **5.3 %** |
| MAPE Fig.8 | | | 8.7 % | igual |

Conclusión: subir p_child de 0.059→0.062 **empeora** child (ruido + sesgo).  
**Congelar:** gate **0.00879** + p_child **0.059** + DischargeInWindow + `goToHospital >= 1`.
