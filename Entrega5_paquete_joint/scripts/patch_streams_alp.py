# -*- coding: utf-8 -*-
"""Crea/parchea la variante del .alp con streams independientes."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "Modelo_Entrega5_Hospital_Hibrido_streams.alp"
text = path.read_text(encoding="utf-8")

text = text.replace(
    "<Name><![CDATA[Modelo_exploracion_Fig8_producto]]></Name>",
    "<Name><![CDATA[Modelo_Entrega5_Hospital_Hibrido_streams]]></Name>",
    1,
)
text = text.replace(
    "<JavaPackageName><![CDATA[modelo_hospital_covid]]></JavaPackageName>",
    "<JavaPackageName><![CDATA[modelo_hospital_covid_streams]]></JavaPackageName>",
    1,
)
text = text.replace("<Id>1783897912793</Id>", "<Id>1783897912893</Id>", 1)
text = text.replace("replicas_kpis_EXPLORA_prodFig8.csv", "replicas_kpis_STREAMS.csv")

old_startup = (
    'archivoCSV.println("Dia,NoTratados,TasaTransmision,FlujoHospital");\n'
    "// admitidosCovid: cualquier patient que ocupo cama COVID (incluye admision < dia 8).\n"
    "// kpiTreated (SED joint): egreso en [8,30] si estuvo en admitidosCovid (DischargeInWindow).\n"
    "// admitidosVentana: solo admisiones en [8,30] para adultAdmit/childAdmit.\n"
    "admitidosVentana = new java.util.HashSet<Agent>();\n"
    "admitidosCovid = new java.util.HashSet<Agent>();"
)

new_startup = (
    'archivoCSV.println("Dia,NoTratados,TasaTransmision,FlujoHospital");\n'
    "// Streams independientes (experimento). Semillas derivadas del RNG de esta corrida/replica\n"
    "// para que ExperimentoReplicas (randomSeed) siga produciendo replicas distintas.\n"
    "long baseSeed = getDefaultRandomGenerator().nextLong();\n"
    "rngSed = new Random(baseSeed ^ 0xA11CEL);\n"
    "rngAbm = new Random(baseSeed ^ 0xB0B1L);\n"
    "rngGate = new Random(baseSeed ^ 0xC0DEL);\n"
    "rngBranch = new Random(baseSeed ^ 0xD00DL);\n"
    'traceln("STREAMS init base=" + baseSeed);\n'
    "// admitidosCovid: cualquier patient que ocupo cama COVID (incluye admision < dia 8).\n"
    "// kpiTreated (SED joint): egreso en [8,30] si estuvo en admitidosCovid (DischargeInWindow).\n"
    "// admitidosVentana: solo admisiones en [8,30] para adultAdmit/childAdmit.\n"
    "admitidosVentana = new java.util.HashSet<Agent>();\n"
    "admitidosCovid = new java.util.HashSet<Agent>();"
)

if old_startup not in text:
    raise SystemExit("startup block not found")
text = text.replace(old_startup, new_startup, 1)

rng_vars = """
				<Variable Class="PlainVariable">
					<Id>1999433000001</Id>
					<Name><![CDATA[rngSed]]></Name>
					<X>1000</X><Y>660</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>false</PresentationFlag>
					<ShowLabel>false</ShowLabel>
					<Properties SaveInSnapshot="false" Constant="false" AccessType="public" StaticVariable="false">
						<Type><![CDATA[Random]]></Type>        
					</Properties>
				</Variable>
				<Variable Class="PlainVariable">
					<Id>1999433000002</Id>
					<Name><![CDATA[rngAbm]]></Name>
					<X>1000</X><Y>685</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>false</PresentationFlag>
					<ShowLabel>false</ShowLabel>
					<Properties SaveInSnapshot="false" Constant="false" AccessType="public" StaticVariable="false">
						<Type><![CDATA[Random]]></Type>        
					</Properties>
				</Variable>
				<Variable Class="PlainVariable">
					<Id>1999433000003</Id>
					<Name><![CDATA[rngGate]]></Name>
					<X>1000</X><Y>710</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>false</PresentationFlag>
					<ShowLabel>false</ShowLabel>
					<Properties SaveInSnapshot="false" Constant="false" AccessType="public" StaticVariable="false">
						<Type><![CDATA[Random]]></Type>        
					</Properties>
				</Variable>
				<Variable Class="PlainVariable">
					<Id>1999433000004</Id>
					<Name><![CDATA[rngBranch]]></Name>
					<X>1000</X><Y>735</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>false</PresentationFlag>
					<ShowLabel>false</ShowLabel>
					<Properties SaveInSnapshot="false" Constant="false" AccessType="public" StaticVariable="false">
						<Type><![CDATA[Random]]></Type>        
					</Properties>
				</Variable>
"""

anchor = """					<Name><![CDATA[admitidosCovid]]></Name>
					<X>1000</X><Y>630</Y>
					<Label><X>10</X><Y>0</Y></Label>
					<PublicFlag>false</PublicFlag>
					<PresentationFlag>false</PresentationFlag>
					<ShowLabel>false</ShowLabel>
					<Properties SaveInSnapshot="true" Constant="false" AccessType="default" StaticVariable="false">
						<Type><![CDATA[java.util.HashSet<Agent>]]></Type>        
					</Properties>
				</Variable>
"""
if anchor not in text:
    raise SystemExit("admitidosCovid anchor not found")
if "rngSed" not in text:
    text = text.replace(anchor, anchor + rng_vars, 1)

replacements = [
    ("triangular( 5, 12, 25 )", "triangular( 5, 12, 25, rngSed )"),
    ("triangular(560, 6480, 17280)", "triangular(560, 6480, 17280, rngSed)"),
    ("triangular(1440, 10080, 36000)", "triangular(1440, 10080, 36000, rngSed)"),
    (
        "if (nurseCovids.size() > 0 && uniform() < 0.04)",
        "if (nurseCovids.size() > 0 && uniform(rngAbm) < 0.04)",
    ),
    (
        "if (nurseAuxiliares.size() > 0 && uniform() < 0.04)",
        "if (nurseAuxiliares.size() > 0 && uniform(rngAbm) < 0.04)",
    ),
    (
        "if (physicianCovids.size() > 0 && uniform() < 0.04)",
        "if (physicianCovids.size() > 0 && uniform(rngAbm) < 0.04)",
    ),
    (
        "if (uniform() < 0.01292) { kpiUntreated++; }",
        "if (uniform(rngGate) < 0.01292) { kpiUntreated++; }",
    ),
    ("triangular(3,5,10)", "triangular(3,5,10, main.rngAbm)"),
    ("uniform(0,1) < 0.3", "uniform(0,1, main.rngBranch) < 0.3"),
]

for a, b in replacements:
    n = text.count(a)
    print(f"{n:3d}  {a!r}")
    if n == 0 and a not in text and b not in text:
        print("  WARNING missing")
    text = text.replace(a, b)

text = text.replace(
    "DASHBOARD INTERACTIVO - CAPACIDAD HOSPITALARIA",
    "DASHBOARD (streams) - CAPACIDAD HOSPITALARIA",
    1,
)

path.write_text(text, encoding="utf-8")

readme = path.parent / "README_STREAMS.md"
readme.write_text(
    """# Variante streams independientes

Archivo: `Modelo_Entrega5_Hospital_Hibrido_streams.alp`

## Qué cambió
4 RNGs (`java.util.Random`) en Main, reinicializados en cada corrida:

| Stream | Uso |
|---|---|
| `rngSed` | Tiempos triangulares SED (triage / estancias) |
| `rngAbm` | Infección periódica del staff + duración infectado |
| `rngGate` | Probabilidad untreated en el gate |
| `rngBranch` | Branch hospitalización staff (p=0.3) |

Semillas derivadas del RNG por defecto de la corrida, así `ExperimentoReplicas` sigue dando réplicas distintas.

**Nota:** los `SelectOutput` (NEWS, ambulatory, etc.) siguen con el RNG por defecto de AnyLogic.

## Cómo probar
1. Abrir este `.alp` (paquete Java: `modelo_hospital_covid_streams`).
2. Correr `ExperimentoReplicas` o `Simulation`.
3. CSV: `Documents/replicas_kpis_STREAMS.csv` (no pisa el CSV del modelo original).
4. Comparar medias/MAPE vs el CSV del modelo base.

## Expectativa
Una corrida cambia de trayectoria; con ~20 réplicas las medias deberían quedar parecidas.
""",
    encoding="utf-8",
)

print("wrote", path)
print("ok rngSed" if "rngSed = new Random" in path.read_text(encoding="utf-8") else "FAIL init")
