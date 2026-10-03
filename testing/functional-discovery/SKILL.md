---
name: functional-discovery
description: "Procedimiento sistemático para explorar una aplicacion web, documentar paginas, formularios y flujos funcionales. Checklist y formato de salida para functional-discovery.md."
---

# Functional Discovery Skill

Procedimiento para explorar una aplicacion web de forma sistematica y documentar su funcionalidad.

## Estrategia de Exploracion

### Orden de navegacion
1. Pagina de inicio / dashboard
2. Menu principal (de izquierda a derecha, de arriba a abajo)
3. Submenus y paginas secundarias
4. Formularios y acciones disponibles
5. Paginas de detalle o resultado

### Para cada pagina
1. Navegar a la URL con `playwright_browser_navigate`
2. Esperar carga con `playwright_browser_wait_for`
3. Obtener snapshot con `playwright_browser_snapshot`
4. Capturar screenshot con `playwright_browser_take_screenshot`
5. Documentar elementos encontrados

### Para formularios
1. Snapshot para identificar campos y sus selectores
2. Documentar cada campo: label, tipo, requerido, placeholder, validaciones
3. NO enviar formularios con datos reales a menos que sean de prueba

## Formato de Salida (functional-discovery.md)

```markdown
# Descubrimiento Funcional - {Nombre de la Aplicacion}

**URL**: {url}
**Fecha**: {fecha}
**Total de paginas**: {n}
**Total de formularios**: {n}

---

## Pagina: {Nombre}

**URL**: {ruta}
**Proposito**: {descripcion}

### Elementos Interactivos
- {elemento}: {tipo} - {funcion}

### Formulario: {Nombre} (si aplica)
| Campo | Tipo | Requerido | Placeholder | Validaciones |
|--------|------|-----------|-------------|-------------|
| {campo} | {tipo} | Si/No | {texto} | {reglas} |

### Capturas
- screenshot-pagina.png
```

## Constraints
- SOLO documentar lo que se OBSERVA directamente
- NO ejecutar acciones destructivas
- Capturar screenshot de CADA pagina visitada
- Documentar TODOS los campos de formulario
- Guardar screenshots usando ruta ABSOLUTA
- Siempre cerrar el navegador al finalizar
