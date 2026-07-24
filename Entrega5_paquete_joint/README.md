# Paquete STRESS SM5380 · Meza-Palacios et al. (2026)

Réplica AnyLogic alineada al **material suplementario** (STRESS) + calibración
Rust/AnyLogic para minimizar MAPE de Tabla 5 y Figura 8.

## Resultados (AnyLogic n=200)

| Métrica | Valor |
|---|---:|
| **MAPE Tabla 5** | **0,5 %** |
| **MAPE Figura 8** (ref. SM) | **4,4 %** |

Backup del escenario solo-T5 (F8≈9,2 %): `../exploracion_STRESS_SM5380_T5ok/`

## Abrir

| Archivo | Uso |
|---|---|
| `index.html` | Presentación 12 slides (doble clic) |
| `Modelo_Hospital_Hibrido_STRESS_SM5380.alp` | Modelo AnyLogic |
| `img/` | Figuras embebidas en la presentación |

## Contenido

```
exploracion_STRESS_SM5380/
├── index.html                 # presentación
├── Modelo_*.alp               # AnyLogic
├── csv/                       # réplicas + resúmenes
├── graficas/                  # PNG de análisis
├── img/                       # copias para index.html
├── scripts/generar_graficas.py
├── README.md                  # este archivo
├── RESULTADOS.md              # tablas T5 / Fig.8
├── PARAMETROS.md              # snapshot de parámetros
├── MATERIAL_SUPLEMENTARIO_SM5380.md
├── DIAGRAMAS_HIBRIDO.md
├── RECALIBRACION_RUST.md      # gates STRESS
└── FIG8_RECALIB_RUST.md       # barrido DS Fig.8
```

## Regenerar gráficas

```bash
cd scripts
python generar_graficas.py
```

## Parámetros clave

- DS: `contacRate=3,0` · `I₀=4000` · `p2h=0,007` · FOI producto  
- SED: gate `0,00714` · untreated `0,01048` · `p_child=0,059`  
- SM: Source Tri(12,15,18)/día + inject ABM · streams · n=200  

Detalle: `PARAMETROS.md` · `RESULTADOS.md`
