---
name: Code Review Helper
description: Proporciona ayuda para revisar código siguiendo las mejores prácticas de Roastr, verificando calidad, seguridad y documentación antes de crear un PR.
---

# Code Review Helper

## Propósito

Esta skill ayuda a realizar revisiones de código completas antes de hacer commit o crear un PR, asegurando que el código cumple con los estándares de calidad de Roastr.

## Instrucciones

Cuando Claude necesite hacer una revisión de código, esta skill le proporciona un checklist estructurado:

### Checklist de Revisión

1. **Calidad de Código**
   - ✅ No hay console.logs olvidados
   - ✅ No hay TODOs sin documentar
   - ✅ Código sigue convenciones del proyecto
   - ✅ Variables con nombres descriptivos

2. **Seguridad**
   - ✅ No hay credenciales o secrets hardcodeados
   - ✅ Variables de entorno usadas correctamente
   - ✅ Validación de inputs de usuario
   - ✅ Sin vulnerabilidades de SQL injection

3. **Tests**
   - ✅ Tests unitarios para nuevo código
   - ✅ Tests de integración para flujos complejos
   - ✅ Cobertura de código adecuada
   - ✅ Todos los tests pasando

4. **Documentación**
   - ✅ `spec.md` actualizado si aplica
   - ✅ Nodos GDD actualizados
   - ✅ Comentarios inline donde sea necesario
   - ✅ Changelog del PR

5. **Performance**
   - ✅ No hay N+1 queries
   - ✅ Cache implementado cuando sea apropiado
   - ✅ Rate limiting respetado

### Flujo de Revisión

```
1. Leer el diff del código a revisar
2. Ejecutar tests relacionados
3. Verificar cada punto del checklist
4. Reportar hallazgos en formato estructurado
5. Sugerir correcciones cuando sea necesario
```

## Ejemplos

### Ejemplo 1: Revisión de Endpoint

**Input**: Revisar un nuevo endpoint de API

**Output**:

```markdown
## Code Review - GET /api/new-feature

✅ **Security**: Header de autenticación verificado
✅ **Validation**: Inputs validados con Joi
✅ **Tests**: 5 tests unitarios + 2 integration
⚠️ **Documentation**: Falta actualizar spec.md con nuevo endpoint
❌ **Performance**: Posible N+1 en query de usuarios

### Sugerencias

- Añadir paginación para listas grandes
- Documentar en spec.md la sección de APIs
```

### Ejemplo 2: Revisión de Componente UI

**Input**: Revisar componente React nuevo

**Output**:

```markdown
## Code Review - UserProfile.jsx

✅ **Structure**: Componente modular y reusable
✅ **Styling**: Usa Tailwind tokens correctamente
✅ **Accessibility**: ARIA labels presentes
⚠️ **Documentation**: Falta comentar estados complex
❌ **Tests**: No hay tests E2E con Playwright

### Sugerencias

- Añadir tests visuales con Playwright
- Documentar manejo de estados loading/error
```

## Criterios de Aprobación

Un PR está listo cuando:

- ✅ Todos los puntos del checklist pasan
- ✅ 0 comentarios de CodeRabbit esperados
- ✅ Tests pasando al 100%
- ✅ Documentación actualizada
- ✅ Sin conflictos con main

## Notas Importantes

- Esta skill complementa a CodeRabbit, no lo reemplaza
- Siempre seguir los estándares definidos en `docs/QUALITY-STANDARDS.md`
- Priorizar calidad sobre velocidad
