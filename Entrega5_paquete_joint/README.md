# Entrega 5 — Paquete de entrega

Réplica AnyLogic del artículo Meza-Palacios et al. (2026).

## Abrir la presentación
- **Rúbrica (12 diapositivas):** doble clic en `presentacion_rubrica_12.html` ← usar esta para Moodle / video.
- Copia extendida (14 slides, más detalle visual): `index.html`
- PDF: `presentacion.pdf` (regenerar si hace falta desde la versión de 12)

## Modelo AnyLogic (entrega final)
**`Modelo_Entrega5_Hospital_Hibrido_streams.alp`** — streams independientes + 200 réplicas.

Baseline (sin streams, calibración n=21): `Modelo_Entrega5_Hospital_Hibrido.alp`

Detalle: `RESULTADOS_STREAMS.md` · `README_STREAMS.md` · `PARAMETROS_COMPROMISO_JOINT.md`

## Contenido
- `index.html` + `img/` — presentación
- `presentacion.pdf` — misma presentación en PDF
- `DIAGRAMAS_HIBRIDO.md` — ciclos causales DS + desglose macro/meso/micro + acoplamiento bidireccional (Mermaid)
- `graficas/` — Fig. 8, Fig. 9 / Tabla 5 y desvíos
- `csv/` — réplicas (incl. `replicas_kpis_streams_n200.csv`) y resúmenes
- `scripts/` — regenerar gráficas y PDF

## Regenerar gráficas / PDF
Ver `scripts/README.md`.

## Resultados (entrega)
- **MAPE Tabla 5 ≈ 3.0 %** (streams, **n=200**)
- MAPE Fig. 8 ≈ 8.7 %
- Baseline histórico: MAPE T5 ≈ 3.7 % (n=21, 1 RNG)
