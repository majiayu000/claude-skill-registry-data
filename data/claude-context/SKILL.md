---
name: claude-context
description: Carga el archivo CLAUDE_PROMPT.md como contexto para aplicar las instrucciones y mejores prácticas del proyecto. Úsalo cuando el usuario quiera aplicar las guías personalizadas, principios de trabajo, o cuando diga "load claude context", "usa el prompt", "aplica CLAUDE_PROMPT", "/claude" o "/bot".
allowed-tools: Read
---

# Cargar Contexto de Claude

## ¿Qué hace este skill?

Este skill lee el archivo `CLAUDE_PROMPT.md` desde la raíz del proyecto y lo aplica como contexto para la conversación actual. Asegura que Claude siga las instrucciones personalizadas y mejores prácticas definidas para el proyecto VetaLaser.

## ¿Cuándo usar?

Pide a Claude que cargue el contexto cuando quieras:
- Aplicar las instrucciones personalizadas del proyecto
- Establecer guías específicas para generación de código
- Cargar estándares y mejores prácticas del equipo
- Habilitar comportamiento o restricciones especializadas
- Recordar a Claude los principios de trabajo (reutilización, schema único, etc.)

**Ejemplos de activación:**
- "Load claude context"
- "Usa el prompt"
- "Aplica CLAUDE_PROMPT"
- "/claude"
- "/bot"
- "Carga las instrucciones del proyecto"
- "Recuerda las mejores prácticas"

## ¿Cómo funciona?

1. Claude lee el archivo `CLAUDE_PROMPT.md` desde la raíz del proyecto
2. El contenido se convierte en parte del contexto de la conversación
3. Claude sigue las instrucciones y guías durante toda la sesión
4. Las mejores prácticas se aplican automáticamente

## Instrucciones para Claude

Cuando este skill está activo:

1. **Lee el archivo** `CLAUDE_PROMPT.md` desde la raíz del proyecto usando la herramienta Read
2. **Extrae las instrucciones clave:**
   - Rol y responsabilidades
   - Principios de trabajo (reutilización de código, gestión de BD, seguridad)
   - Workflow para nuevas funcionalidades
   - Patrones de código del proyecto
   - Recordatorios importantes
3. **Integra las instrucciones** en tu comportamiento y respuestas
4. **Confirma al usuario** qué instrucciones estás aplicando con un resumen breve
5. **Continúa siguiendo** estas guías durante toda la conversación

Si `CLAUDE_PROMPT.md` no existe, informa al usuario y ofrece crearlo.

## Ejemplo de uso

```
Usuario: /claude

Claude debería:
1. Leer CLAUDE_PROMPT.md
2. Mostrar un resumen de las instrucciones clave encontradas
3. Confirmar que el contexto está ahora activo
4. Aplicar las guías en todas las respuestas siguientes
```

## Salida esperada

Después de cargar el contexto, Claude debería responder algo como:

```
✅ Contexto cargado desde CLAUDE_PROMPT.md

Principios activos:
• Reutilización de código (buscar antes de crear)
• Gestión de BD: solo 00_complete_schema.sql
• Seguridad: RLS, validaciones, autenticación
• Commits: descriptivos con emojis
• Deployment: Netlify + Supabase Edge Functions

Estoy listo para trabajar siguiendo las mejores prácticas del proyecto VetaLaser.
¿En qué puedo ayudarte?
```

## Notas adicionales

- Este skill es específico del proyecto VetaLaser
- El archivo CLAUDE_PROMPT.md contiene el contrato de trabajo completo
- Las instrucciones persisten durante toda la conversación
- Puedes recargar el contexto en cualquier momento ejecutando el skill nuevamente
