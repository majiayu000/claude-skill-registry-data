---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Protocolo sistemático de depuración en 6 fases. Enfoque estructurado ante errores con verificaciones rápidas, pruebas aisladas, regla de los 20 minutos y plantilla de informe de errores.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="bugfix-protocol banner">

> **Español** — Versión oficial en español de `bugfix-protocol`.


# Bugfix Protocol: Depuración Sistemática en 6 Fases

Enfoque estructurado para la resolución de errores — desde el análisis de síntomas hasta la verificación.
Evita el ensayo y error sin rumbo y garantiza que las soluciones sean sostenibles.

---

## Resumen y Propósito

| Fase | Nombre | Objetivo | Tiempo máx. |
|------|--------|----------|-------------|
| 1 | Verificaciones rápidas | Descartar causas evidentes | 2 min |
| 2 | Diagnóstico | Localizar la causa raíz | 10 min |
| 3 | Prueba aislada | Hacer que el error sea reproducible | 5 min |
| 4 | Corrección | Corrección mínima | 10 min |
| 5 | Verificación | Verificar la solución + comprobar efectos secundarios | 5 min |
| 6 | Documentación | Preservar el conocimiento | 2 min |

**Regla de los 20 minutos:** Si no hay avances tras 20 minutos, cambia de enfoque o busca ayuda.

---

## Fase 1: Verificaciones rápidas (2 min)

Antes de profundizar, comprueba las causas más comunes:

### Lista de verificación

- [ ] **¿Error de sintaxis?** Lee atentamente el mensaje de error, comprueba la línea
- [ ] **¿Error de importación?** ¿Módulo instalado? ¿Nombre correcto? ¿Importación circular?
- [ ] **¿Error tipográfico?** ¿Nombres de variables/funciones correctos?
- [ ] **¿Tipo de datos incorrecto?** ¿Cadena en lugar de int? ¿None donde se esperaba un objeto?
- [ ] **¿Caché desactualizada?** Elimina `__pycache__`, reinicia
- [ ] **¿Entorno incorrecto?** ¿venv correcto activo? ¿Versión de Python correcta?
- [ ] **¿Codificación?** UTF-8 vs. cp1252 (Windows clásico)

### Acciones rápidas

```bash
# Limpiar caché
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Comprobar importaciones
python -c "import modulename"

# Comprobar sintaxis
python -m py_compile file.py
```

---

## Fase 2: Diagnóstico (10 min)

### Estrategia: De fuera hacia dentro

1. **Analizar mensaje de error** — Lee la traza de pila (traceback) de abajo hacia arriba
2. **Comprobar cambios recientes** — `git diff`, `git log --oneline -10`
3. **Usar herramientas de diagnóstico** — Utiliza herramientas específicas del proyecto

### Herramientas de diagnóstico (Ejemplos)

Según el proyecto, las secuencias de comandos de diagnóstico especializadas pueden ser útiles:

| Herramienta | Propósito |
|-------------|-----------|
| `import_diagnose.py` | Analizar problemas de importación |
| `method_analyzer.py` | Comprobar firmas de métodos |
| `env_checker.py` | Validar variables de entorno/rutas |

> **Nota:** Crea herramientas de diagnóstico específicas del proyecto o utiliza las existentes.
> Lo que importa es el enfoque sistemático, no la herramienta específica.

### Técnicas de depuración

```python
# 1. Depuración con print (rápida pero efectiva)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Puntos de interrupción (interactivo)
breakpoint()  # Python 3.7+

# 3. Traza de pila extendida
import traceback
traceback.print_exc()

# 4. Registro en lugar de print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## Fase 3: Prueba aislada (5 min)

### Ejemplo mínimo reproducible (MRE)

Objetivo: Reproducir el error con el código mínimo.

```python
# test_bug.py — Prueba de reproducción mínima
"""
Bug: [Descripción corta]
Expected: [Lo que debería suceder]
Actual: [Lo que sucede en su lugar]
"""

# Configuración mínima
# ... solo lo esencial

# Desencadenante del error
# ... código exacto que desencadena el error

# Resultado esperado
# assert result == expected, f"Got {result}"
```

### Estrategias de aislamiento

1. **Nuevo archivo:** Reproduce el error en un archivo separado
2. **Eliminar dependencias:** Una por una, hasta que el error desaparezca
3. **Búsqueda binaria:** Divide el bloque de código a la mitad, comprueba qué mitad contiene el error
4. **Git bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## Fase 4: Corrección (10 min)

### Principios

1. **Mínimo:** Cambia lo menos posible
2. **Comprender:** Nunca corrijas a ciegas — comprende POR QUÉ está roto
3. **Una cosa:** Una corrección por commit, no soluciones múltiples problemas a la vez
4. **Compatible hacia atrás:** No rompas la funcionalidad existente

### Patrones de corrección

```python
# MAL: Tratar el síntoma
try:
    result = broken_function()
except:  # Ignorar todo
    result = default_value

# BIEN: Corregir la causa raíz
def broken_function():
    if input_data is None:  # Causa real: falta comprobación de None
        return default_value
    return process(input_data)
```

### Categorías comunes de corrección

| Categoría | Corrección típica |
|-----------|-------------------|
| None/Null | Cláusula de guarda: `if x is None: return default` |
| Error de índice | Comprobación de límites: `if i < len(lst)` |
| Error de tipo | Conversión explícita: `str(x)`, `int(x)` |
| Error de importación | Corregir ruta, instalar paquete |
| Codificación | Especificar UTF-8 explícitamente: `encoding='utf-8'` |
| Condición de carrera | Bloqueo/Mutex, o cambiar el orden |
| Error de estado | Comprobar inicialización, añadir restablecimiento |

---

## Fase 5: Verificación (5 min)

### Lista de verificación

- [ ] **Error corregido:** El problema original ya no ocurre
- [ ] **MRE supera:** La prueba aislada se ejecuta correctamente
- [ ] **Sin regresión:** Las pruebas existentes siguen pasando
- [ ] **Casos límite:** Entrada vacía, None, datos grandes probados
- [ ] **Herramientas del proyecto:** Comprueba el directorio de herramientas del proyecto para herramientas de prueba/validación relevantes

### Comandos de prueba

```bash
# Pruebas unitarias
python -m pytest tests/ -v

# Solo pruebas afectadas
python -m pytest tests/test_module.py -v -k "test_name"

# Verificación de tipos
python -m mypy file.py

# Linter
python -m flake8 file.py
```

---

## Fase 6: Documentación (2 min)

### Plantilla de informe de errores

```markdown
## Bug Report: [Título corto]

**Date:** YYYY-MM-DD
**Severity:** critical / high / medium / low
**Component:** [Módulo/Archivo]

### Symptom
[Lo que ve el usuario / mensaje de error]

### Root Cause
[Causa raíz técnica]

### Fix
[Qué se cambió + por qué]

### Affected Files
- `file1.py` — [Cambio]
- `file2.py` — [Cambio]

### Prevention
[¿Cómo se puede prevenir este tipo de error en el futuro?]
```

### Formato del mensaje de commit

```
fix: [Descripción corta de la corrección]

Cause: [Causa raíz en una frase]
Fix: [Qué se cambió]
Test: [Cómo se verificó]
```

---

## PyQt6 / Depuración de GUI — Trampas comunes

> Esta sección es relevante para proyectos de GUI de escritorio con PyQt6/PySide6.

### Las 5 principales trampas de PyQt6

| Trampa | Problema | Solución |
|--------|----------|----------|
| **Desconexión Signal-Slot** | Señal conectada pero el manejador no se ejecuta | `print` en manejador, comprobar firma |
| **Seguridad de hilos (Thread Safety)** | Actualización de GUI desde hilo de trabajo | `QMetaObject.invokeMethod` o usar señal |
| **Cascada de diseño (Layout)** | Widget invisible/desplazado | `widget.show()`, comprobar jerarquía de layout |
| **Bloqueo del bucle de eventos** | La GUI se congela | Mover operaciones largas a QThread |
| **Recolección de basura** | El widget desaparece repentinamente | Mantener referencia como `self.widget` |

### Ayudantes de depuración de PyQt6

```python
# Imprimir jerarquía de widgets
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Depuración de señales
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## Referencia rápida

```
¿ERROR ENCONTRADO?
     |
     v
[Fase 1: Verificaciones rápidas]  ── ¿Evidente? -> CORREGIR
     |
     v
[Fase 2: Diagnóstico]  ──────────── ¿Causa clara? -> Fase 4
     |
     v
[Fase 3: Prueba aislada]  ──────── ¿Reproducible? -> Fase 4
     |                                  |
     |                             ¿No reproducible?
     |                                  |
     |                             Añadir registros,
     |                             esperar recurrencia
     v
[Fase 4: Corrección]  ───────────── Mínima + comprendida
     |
     v
[Fase 5: Verificación]  ────────── ¿Pruebas en verde? -> Fase 6
     |                                  |
     |                             ¿Pruebas en rojo? -> Volver a Fase 4
     v
[Fase 6: Documentación]  ───────── Informe de error + commit
```

### Regla de los 20 minutos

Si estás atascado tras 20 minutos:

1. **Cambiar de enfoque** — Prueba una técnica de depuración diferente
2. **Pato de goma (Rubber duck)** — Explica el problema en voz alta (o escríbelo)
3. **Toma un descanso** — Aléjate durante 5 minutos, regresa con mente fresca
4. **Busca ayuda** — Pregunta a un colega, Stack Overflow, documentación
5. **Restablecer** — `git stash`, empieza completamente de nuevo
