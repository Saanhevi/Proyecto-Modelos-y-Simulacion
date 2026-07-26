# Entrega 5 · Simulación híbrida · Capacidad hospitalaria COVID

Réplica en **AnyLogic** del modelo híbrido (DS + SBA + SED) del artículo:

> Meza-Palacios, R., Aguilar-Lasserre, A. A., Moras-Sánchez, C. G., & Vázquez-Rodríguez, C. F. (2026). Development of a hybrid simulation model for hospital capacity in health emergencies. *Journal of Simulation*. https://doi.org/10.1080/17477778.2025.2610014

**Equipo:** Samuel Herrera · Katherinne Olaya · Fredy García · Ever Muñoz  
**Curso:** Modelos y Simulación · Universidad Nacional de Colombia  
**Repositorio del proyecto:** https://github.com/Saanhevi/Proyecto-Modelos-y-Simulacion

| Métrica | Valor |
|---|---:|
| MAPE Tabla 5 (n = 200) | **0,5 %** |
| MAPE Figura 8 | **4,4 %** |

Este paquete corresponde a la **Opción A** de entrega (proyecto fuente comprimido): modelo `.alp` + dependencias/scripts + documentación, listo para revisión de código y reproducción de gráficas.

---

## Contenido del directorio

```
Entrega5_Simulacion_Hibrida_Hospital_COVID/
├── README.md                          ← este archivo
├── Modelo_Hospital_Hibrido_COVID.alp  ← modelo AnyLogic (abrir aquí)
├── presentacion/
│   ├── index.html                     ← presentación (12 diapositivas)
│   └── img/                           ← figuras embebidas
├── csv/                               ← salidas de experimentos
├── graficas/                          ← PNG generados con Python
├── scripts/
│   ├── generar_graficas.py
│   └── requirements.txt
├── diagramas/                         ← CLD, Forrester, SED, agentes, acoplamiento
│   ├── diagrama_causal_cld.png
│   ├── diagrama_forrester_stock_flujo.png
│   ├── flujo_sed_area_covid.png
│   ├── statechart_personal_agentes.png
│   └── acoplamiento_ds_sba_sed.jpeg
├── docs/
    ├── PARAMETROS.md
    ├── RESULTADOS.md             
```

No se usan rutas absolutas: el modelo y los scripts esperan esta estructura relativa.

---

## 1. Cómo abrir y usar el modelo AnyLogic

### Requisitos

- AnyLogic **8** (Personal Learning Edition o superior).
- Abrir el `.alp` **desde esta carpeta** (no mover el archivo solo).

### Pasos

1. Abrir `Modelo_Hospital_Hibrido_COVID.alp` con AnyLogic.
2. Revisar el Main: bloques DS (stocks/flujos), SED (área COVID) y poblaciones de agentes (personal).
3. En el lanzador de AnyLogic aparecen estas corridas (nombre exacto):

| Corrida | Uso |
|---|---|
| `Modelo_Hospital_Hibrido_COVID / Simulation` | Corrida base / demo en vivo (tablero) |
| `Modelo_Hospital_Hibrido_COVID / ExperimentoReplicas` | Réplicas para Tabla 5 (π = 0,04 · n = 200) |
| `Modelo_Hospital_Hibrido_COVID / ParametersVariation` | Sensibilidad Figura 8 (π ∈ {0,02 … 0,06}) |

4. Para la corrida base (`Simulation`):
   - `probabilityOfTransmission` = **0,04**
   - horizonte **30** días, warm-up **8** días

### Qué mirar en la demo

- Tablero: no atendidos, tratados, ingresos adultos/niños, susceptibles/infectados.
- Puentes en vivo: `goToHospital` → inject al SED; contagio del personal → capacidad y posibles pacientes.

Detalle de parámetros: `docs/PARAMETROS.md`.

---

## 2. CSV que genera AnyLogic (automático)

Al correr los experimentos, el `.alp` **escribe solo** en la carpeta `csv/` (junto al modelo) y **sobrescribe** la corrida anterior:

| Experimento | Archivo que actualiza |
|---|---|
| `ExperimentoReplicas` | `csv/replicas_kpis_n200.csv` (reinicia al empezar el Run; luego append de cada réplica) |
| `ParametersVariation` | `csv/fig8_flujo_diario.csv` (reinicia al empezar el Run; luego append de las 5 curvas π) |
| `Simulation` (base) | `csv/historico_diario.csv` (sobrescribe cada corrida; Python no lo usa) |

Flujo:

1. Correr el experimento en AnyLogic.
2. Verificar en la consola la ruta absoluta del CSV (AnyLogic imprime `… <- p=…`).
3. Ejecutar `python generar_graficas.py` (sección 3).

**Qué toca y qué no:**

| Archivo | Quién lo produce | Qué hacer al re-correr |
|---|---|---|
| `csv/replicas_kpis_n200.csv` | AnyLogic (`ExperimentoReplicas`) | Nada: se sobrescribe solo |
| `csv/fig8_flujo_diario.csv` | AnyLogic (`ParametersVariation`) | Nada: se sobrescribe solo |
| `csv/historico_diario.csv` | AnyLogic (`Simulation`) | Nada: se sobrescribe solo |
| `csv/resumen_tabla5.csv` | Script Python | Se regenera solo al correr el script |
| `csv/resumen_fig8.csv` | Script Python | Se regenera solo al correr el script |
| `csv/meta.json` | Script Python | Se regenera solo al correr el script |

Si en la consola aparece un error de escritura, confirme que corre el modelo desde la carpeta del proyecto (donde está la carpeta `csv/`).

### 2.1 Réplicas (Tabla 5)

1. Ejecutar **`Modelo_Hospital_Hibrido_COVID / ExperimentoReplicas`** (π = 0,04 · n = 200).
2. Al terminar, debe existir / actualizarse:

```text
csv/replicas_kpis_n200.csv
```

Columnas mínimas esperadas por el script:

| Columna | Significado |
|---|---|
| `pTransmit` | Probabilidad de transmisión de esa corrida |
| `untreated` | No atendidos |
| `treated` | Tratados |
| `adultAdmit` | Ingresos adultos |
| `childAdmit` | Ingresos niños |
| `arrive` | (opcional) llegadas; se usa un filtro de robustez |

### 2.2 Sensibilidad Figura 8

1. Ejecutar **`Modelo_Hospital_Hibrido_COVID / ParametersVariation`** (π = 0,02 · 0,03 · 0,04 · 0,05 · 0,06).
2. Al terminar, debe existir / actualizarse:

```text
csv/fig8_flujo_diario.csv
```

Columnas mínimas:

| Columna | Significado |
|---|---|
| `pTransmit` | Valor de π |
| `day` | Día de simulación (0…30) |
| `flujoHospital` | Flujo acumulado a hospital |

### 2.3 Buenas prácticas

- No mueva ni renombre esos CSV (Python busca exactamente esos nombres en `csv/`).
- Tras terminar el experimento, ejecute el script de gráficas (sección 3).

---

## 3. Cómo generar las gráficas (Python)

### Requisitos

```bash
cd scripts
pip install -r requirements.txt
```

(Python 3.10+ recomendado.)

### Ejecutar

```bash
cd scripts
python generar_graficas.py
```

### Salidas

| Archivo | Uso |
|---|---|
| `graficas/tabla5_boxplots.png` | Dispersión de réplicas vs artículo |
| `graficas/tabla5_desvios.png` | Desvíos % Tabla 5 |
| `graficas/fig8_sensibilidad_flujo.png` | Flujo vs días (una curva por π) |
| `graficas/fig8_escala_vs_articulo.png` | Totales día 30 vs referencia Fig. 8 |
| `presentacion/img/*.png` | Copias con nombres usados por `index.html` |

Si falta un CSV, el script termina con un mensaje indicando qué archivo falta.

---

## 4. Presentación

Abrir en el navegador:

```text
presentacion/index.html
```

(flechas / espacio para avanzar). Las imágenes se cargan desde `presentacion/img/` con rutas relativas.

---

## 5. Documentación adicional

| Documento | Contenido |
|---|---|
| `docs/PARAMETROS.md` | Valores calibrados y fuentes |
| `docs/RESULTADOS.md` | Tablas de validación |
| `diagramas/` | Diagramas CLD, Forrester, SED, etc.

---
