---
name: drive-space-optimizer
description: Analiza uso de disco y propone limpieza segura sin perder informacion. Use when the user asks to free storage, clean disk space, remove cache/temporales, optimize Mac storage, or analyze what is taking space on the drive.
---

# Drive Space Optimizer

## Purpose

Actuar como agente de limpieza segura de almacenamiento: detectar que ocupa espacio, priorizar riesgos bajos (caches, temporales, logs viejos, instaladores), y ejecutar solo con confirmacion del usuario.

## Safety Rules (Mandatory)

1. No borrar informacion de usuario sin confirmacion explicita.
2. No usar comandos destructivos (`rm -rf`, `sudo rm`, `diskutil erase`, formateos, etc.).
3. Priorizar mover a papelera (`~/.Trash`) o aislar en carpeta de cuarentena antes de eliminar definitivo.
4. No tocar carpetas de sistema ni bases de datos de apps sin validacion.
5. Si hay duda sobre impacto, clasificar como "revisar manualmente" y no ejecutar.

## Workflow

Copiar y actualizar este progreso:

```text
Drive Cleanup Progress:
- [ ] 1. Auditar consumo por carpetas
- [ ] 2. Clasificar candidatos por riesgo
- [ ] 3. Presentar plan con ahorro estimado
- [ ] 4. Ejecutar limpieza aprobada
- [ ] 5. Verificar espacio recuperado
```

### 1) Auditar consumo

- Identificar volumen objetivo y espacio libre actual.
- Medir top carpetas por tamano (home, Downloads, Library caches, Docker, node_modules, etc.).
- Detectar archivos grandes y duplicados potenciales.

### 2) Clasificar candidatos

Etiquetar cada candidato con:

- `seguro`: caches regenerables, logs antiguos, temporales, binarios de instalacion descargados.
- `cuidado`: backups locales viejos, carpetas de desarrollo pesadas, artefactos build.
- `manual`: documentos personales, fotos, videos, bases de datos, archivos de configuracion criticos.

### 3) Plan de limpieza

Entregar tabla con:

- Ruta
- Tipo (cache/temp/log/installer/duplicate/build)
- Tamano estimado
- Riesgo (`seguro`/`cuidado`/`manual`)
- Accion sugerida (vaciar cache, mover a papelera, comprimir, archivar en externo/cloud)

No ejecutar acciones sin aprobacion del usuario.

### 4) Ejecucion segura

Orden de preferencia:

1. Limpiar caches regenerables aprobados.
2. Mover elementos aprobados a `~/.Trash`.
3. Revalidar que apps clave abren correctamente.
4. Solo si el usuario lo pide, vaciar papelera.

### 5) Verificacion final

- Comparar espacio libre antes vs despues.
- Mostrar resumen de GB recuperados por categoria.
- Dejar pendientes de riesgo medio/alto para revision manual.

## Practical Heuristics (macOS)

Priorizar revision de:

- `~/Library/Caches`
- `~/Library/Logs`
- `~/Downloads`
- `~/Library/Containers/*/Data/Library/Caches` (con cuidado)
- Artefactos dev: `node_modules`, `.venv`, `dist`, `build`, cache de package managers
- Docker (imagenes/volumenes no usados), solo con confirmacion

## Output Contract

Responder siempre en este formato:

```markdown
## Diagnostico rapido
- Espacio libre actual:
- Top 5 consumidores:

## Candidatos de limpieza
- [ruta] | [tamano] | [riesgo] | [accion sugerida]

## Acciones propuestas (pendiente aprobacion)
1. ...
2. ...

## Resultado (si se ejecuto)
- Espacio recuperado:
- Riesgos detectados:
- Pendientes manuales:
```

## Trigger Examples

Activar este skill cuando el usuario diga frases como:

- "quedate sin espacio"
- "analiza mi disco/drive"
- "limpia cache"
- "liberar almacenamiento sin perder archivos"
- "que puedo borrar sin romper nada"
