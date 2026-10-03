---
name: user-story-standards
description: "Buenas practicas, formato y ejemplos de historias de usuario para QA. Incluye principios INVEST, adaptacion por modo de prueba y guia de identificacion de historias."
---

# User Story Standards Skill

Estandares para redaccion de historias de usuario y criterios de aceptacion verificables.

## Formato Base

```markdown
## HU-NN: {Titulo descriptivo}

**Como** {rol del usuario}
**Quiero** {accion o funcionalidad}
**Para** {beneficio o valor de negocio}

### Criterios de Aceptacion
1. **CA-NN.1**: {Criterio verificable con condicion y resultado esperado}
2. **CA-NN.2**: {Criterio verificable}
3. **CA-NN.3**: {Criterio verificable}

### Datos de Prueba
- {Dato 1}: {valor especifico}
- {Dato 2}: {valor especifico}

### Notas
- {Observaciones del descubrimiento funcional}
```

## Principios INVEST
- **I**ndependent: Cada historia se puede probar por separado
- **N**egotiable: Los detalles se pueden ajustar
- **V**aluable: Aporta valor al usuario/negocio
- **E**stimable: Se puede estimar el esfuerzo
- **S**mall: Tamanio adecuado para una iteracion
- **T**estable: Criterios verificables con Si/No

## Adaptacion por Modo de Prueba

### Modo `positivos`
- Criterios orientados a flujos exitosos y resultados correctos
- NO incluir criterios de error ni de borde
- Minimo 3 criterios Happy Path por historia

### Modo `negativos`
- Criterios orientados al manejo de errores y datos invalidos
- NO incluir criterios de flujo exitoso
- Minimo 3 criterios de error por historia

### Modo `borde`
- Criterios orientados a valores limite y condiciones extremas
- Incluir limites inferiores, superiores, cadenas vacias, caracteres especiales
- Minimo 3 criterios de borde por historia

### Modo `e2e`
- Una unica historia por flujo de negocio principal
- Criterios describen pasos del flujo completo en secuencia
- Minimo 1 historia E2E; maximo 2

## Guia de Identificacion de Historias

| Funcionalidad observada | Tipo de historia |
|------------------------|-----------------|
| Formulario de busqueda | Consulta/Busqueda de {entidad} |
| Formulario de registro/creacion | Creacion de {entidad} |
| Tabla/listado de datos | Visualizacion de {entidad} |
| Botones de edicion en filas | Edicion de {entidad} |
| Menu de navegacion con secciones | Una historia por seccion funcional principal |
| Login/autenticacion | Acceso al sistema |
| Filtros y ordenamiento | Gestion de {entidad} |

## Criterios de Calidad
- Criterios verificables con Si/No
- Datos especificos (no genericos)
- Enfoque por modo estricto
- Lenguaje de negocio, no tecnico
- Numeracion consecutiva: HU-01, HU-02
- Criterios: CA-{HU}.{n}
