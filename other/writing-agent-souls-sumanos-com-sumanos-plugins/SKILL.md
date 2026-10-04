---
name: writing-agent-souls
description: Cómo escribir un buen SOUL (system prompt) de agente Hermes — estructura, buenas prácticas y errores típicos. Usar al crear o mejorar la identidad de un agente.
---

# Cómo escribir un buen SOUL de agente

El SOUL es el system prompt del agente: define quién es, cómo se comporta y qué no hace. Máximo 8000 caracteres. Es lo que más impacta en la calidad del agente.

## Estructura recomendada
1. **Identidad** (1-2 frases): qué es el agente, para quién trabaja, su tono. Ej: "Sos el asistente de ventas de [Negocio]. Hablás cálido y claro, en español rioplatense."
2. **Qué hace**: sus tareas concretas (responder consultas, tomar pedidos, agendar).
3. **Cómo se comporta**: reglas de estilo (breve, sin tecnicismos), cuándo escalar a un humano, qué datos pedir.
4. **Qué NO hace / límites**: temas fuera de alcance, no inventar precios/stock, no prometer lo que no puede.
5. **Datos del negocio** (si los hay): horarios, productos, políticas, concretos.

## Buenas prácticas
- Concreto mejor que genérico: "Respondé en 2-3 frases" mejor que "sé conciso".
- Poné ejemplos de respuestas buenas si el tono importa.
- Si el agente usa skills o canales, decí cuándo usarlos.
- Evitá contradicciones (el engine puede comportarse raro con instrucciones que chocan).

## Errores típicos
- SOUL gigante y vago: el agente se dispersa. Mejor corto y preciso.
- Pedir cosas que el agente no puede hacer sin la tool/canal: frustración.
- Olvidar el idioma/tono: respuestas frías o en otro idioma.

Recordá: `edit_soul` REEMPLAZA todo el SOUL. Antes de editar, leé el actual con `read_soul`, conservá lo bueno y mejorá.
