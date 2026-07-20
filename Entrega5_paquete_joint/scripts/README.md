# Scripts del paquete Entrega 5

## Regenerar gráficas (Fig. 8, Fig. 9 / Tabla 5, desvíos)

Desde esta carpeta:

```bash
pip install -r requirements.txt
python generar_graficas.py
```

Lee `../csv/replicas_kpis_n21.csv` y `../csv/fig8_flujo_diario.csv`.  
Escribe PNG en `../graficas/` y aliases en `../img/` para `index.html`.

## Regenerar el PDF de la presentación

```bash
pip install -r requirements.txt
playwright install chromium
python html_to_pdf.py
```

Genera `../presentacion.pdf` (una página por diapositiva).
