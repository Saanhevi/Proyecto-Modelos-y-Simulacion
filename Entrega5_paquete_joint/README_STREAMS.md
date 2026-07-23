# Variante streams independientes

Archivo: `Modelo_Entrega5_Hospital_Hibrido_streams.alp`

## Por qué más réplicas
La rúbrica pide *streams* independientes. Con n=20 el MAPE aún “baila” (vimos ~10 % y ~4 %).  
Para ver a qué tiende: **200 réplicas**.

`ExperimentoReplicas` usa **ReplicationPerIteration = 200** y el campo `nReplicasTotal = 200` (Additional class code) para el contador de pantalla.  
Si cambias el nº de réplicas en Properties, actualiza también `nReplicasTotal` para que el texto “X / N” coincida.

## Protocolo de corrida limpia
1. Cierra el modelo original; abre solo el `_streams.alp` (reabrir si ya estaba abierto).
2. CSV n=80 archivado como `Documents\replicas_kpis_STREAMS_n80.csv`.
3. Corre **ExperimentoReplicas**.
4. Al terminar (~200 filas π=0.04), avisa para calcular MAPE.

## Streams
| Stream | Uso |
|---|---|
| `rngSed` | Demoras triangulares SED |
| `rngAbm` | Infección staff + duración infectado |
| `rngGate` | Gate untreated |
| `rngBranch` | Branch hospitalización staff (p=0.3) |

`SelectOutput` (NEWS, etc.) sigue en el RNG por defecto.
