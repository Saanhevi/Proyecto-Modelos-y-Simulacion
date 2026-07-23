# Variante streams independientes

Archivo: `Modelo_Entrega5_Hospital_Hibrido_streams.alp`

## Por qué más réplicas
La rúbrica pide *streams* independientes. Con n=20 el MAPE aún “baila” (vimos ~10 % y ~4 %).  
Para ver a qué tiende: **200 réplicas**.

`ExperimentoReplicas` usa **ReplicationPerIteration = 200** por defecto.  
El contador de pantalla lee el total con `nReplicasConfig()` (desde Properties → Replications per iteration).  
Si cambias ese número en Properties, haz **Build** y vuelve a lanzar el experimento: el texto “X / N” debe seguir el nuevo N.

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
