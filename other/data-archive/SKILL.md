---
name: data-archive
description: >
  Documentar, versionar y cerrar proyectos de análisis de datos.
  Trigger: Cuando terminás un proyecto y querés dejar todo ordenado para el futuro.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-archive

Archivar no es "tirar todo en una carpeta y olvidarte". Es **dejarle la posta a tu yo del futuro** (o a quien herede el proyecto). Un buen archive hace que dentro de 6 meses puedas volver, entender qué hiciste, por qué, y replicarlo sin tener que adivinar.

## Trigger

- El proyecto está terminado y listo para commitear/entregar
- Vas a cambiar de proyecto y querés cerrar el actual ordenadamente
- Alguien más va a tomar tu lugar y necesita entender lo que hiciste
- El cliente/stakeholder pidió los entregables finales

## Workflow de archivo

### 1. Limpiá el código
Eliminá celdas rotas, código comentado que no sirve, variables temporales. Corré el notebook de arriba a abajo para asegurarte de que funciona sin errores.

### 2. Documentá las decisiones clave
No documentes el "qué" (ya está en el código), documentá el "por qué". Por qué elegiste ese enfoque, por qué descartaste tal variable, por qué ese filtro.

### 3. Guardá datos en formato portable
Los CSVs raw no se tocan. Los datos procesados guardalos en Parquet (más rápido, más chico, preserva tipos).

### 4. Congelá dependencias
Un `pip freeze > requirements.txt` o un `conda env export > environment.yml` le ahorra dolores de cabeza a tu yo del futuro.

### 5. Commit con mensaje que explique el proyecto
No pongas "análisis final". Poné "ventas Q1: análisis de caída en segmento PyME, conclusión: efecto estacional, recomendación: ajustar campaña Marzo".

## Patrones y ejemplos

### Template de resumen de proyecto

```markdown
## Resumen del proyecto
- **Pregunta**: {qué queríamos descubrir}
- **Datos**: {fuente, tamaño, período}
- **Enfoque**: {qué hicimos y por qué}
- **Resultado principal**: {hallazgo clave en 1-2 líneas}
- **Limitaciones**: {qué no pudimos hacer, datos que faltaron}
- **Aprendizaje**: {qué harías distinto la próxima}
- **Dueño**: {quién lo hizo} | **Fecha**: {cuándo}
```

### Script de cierre automatizado

```python
from pathlib import Path
import pandas as pd
import subprocess

def archivar_proyecto(ruta_proyecto: str, mensaje_commit: str):
    """Prepara y commitea el proyecto para archivo"""
    ruta = Path(ruta_proyecto)

    # 1. Exportar datos procesados a Parquet
    df = pd.read_csv(ruta / 'datos_procesados.csv')
    df.to_parquet(ruta / 'datos_final.parquet', index=False)
    print("✅ Datos exportados a Parquet")

    # 2. Generar requirements
    subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
    with open(ruta / 'requirements.txt', 'w') as f:
        f.write(result.stdout)
    print("✅ Dependencias congeladas")
```

### Checklist de archivo (para no saltarte nada)

```markdown
- [ ] Notebooks limpios (sin outputs basura, corridos de principio a fin)
- [ ] Datos procesados guardados en Parquet (no solo CSV)
- [ ] requirements.txt o environment.yml actualizado
- [ ] README del proyecto escrito con resumen y cómo ejecutar
- [ ] Hallazgos documentados (en el README, en Engram o donde corresponda)
- [ ] Git tag con versión (git tag -a v1.0 -m "Versión final")
- [ ] Archivos temporales/cache eliminados
- [ ] Visualizaciones exportadas (PNG/HTML) si son parte del entregable
```

## Alternativas

| Herramienta | Para qué sirve |
|-------------|---------------|
| **DVC** | Versionado de datasets grandes, tracking de pipelines ML |
| **Pachyderm** | Data lineage completo: cada paso del pipeline queda registrado |
| **Engram** | Memoria persistente del agente: guarda decisiones y aprendizajes clave |
| **Manual + README** | Para proyectos chicos, un README bien escrito alcanza |

**Recomendación**: Para proyectos exploratorios cortos, alcanza con README + requirements.txt. Para proyectos largos o productivos, usá DVC versioning + Engram para las decisiones.

## Anti-patrones

- ❌ **Archivar sin documentar el "por qué"** — el código dice qué hiciste, no por qué lo hiciste así
- ❌ **Guardar datasets gigantes sin comprimir** — CSV de 2GB cuando Parquet ocupa 200MB
- ❌ **No limpiar notebooks** — outputs de 5000 líneas, celdas que fallaron, imports sin uso
- ❌ **Commit único "final" sin mensaje descriptivo** — después es imposible encontrar algo
- ❌ **No congelar dependencias** — 6 meses después las librerías cambiaron y tu código no corre
