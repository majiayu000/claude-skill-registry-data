---
name: Principios de Copywriting - Movistar
key: copywriting-principles-movistar
description: 9 principios de copywriting creativo, estructura de pieza, guia de inicio y código visual. Las reglas formales de identidad verbal estan en brand-voice-movistar. Skill obligatoria para el Creative Copywriter.
version: 1.1.0
owner: superreal
status: active
source: Brand Guardian v4 RAG Movistar (secciones 1.2 y 1.3) - validado por Comunicación Movistar
depends_on:
  - brand-voice-movistar
---

# Principios de Copywriting - Movistar

Skill compartida. El Creative Copywriter la carga obligatoriamente antes de escribir copies finales. Los Agentes A y B la consultan como referencia. Se complementa con `brand-voice-movistar` (identidad, tono, evaluación) y `estilo-terminologia-movistar` (grafías, precios, formatos).

> Origen: Brand Guardian v4 RAG Movistar, secciones 1.2 (Tono de la marca) y 1.3 (Guía de copywriting). Cualquier discrepancia con otras fuentes se resuelve a favor de `brand-voice-movistar` para identidad/tono y a favor de este archivo para técnica de redacción.

---

## 1. Los 9 principios de copywriting creativo

Estos principios guían la creación de copies con calidad Movistar. Van más allá de las reglas formales: definen cómo pensamos y escribimos.

### 1.1. Una idea central poderosa
Cada pieza gira en torno a una sola gran idea emocional o funcional.
- Ejemplo: "Donde hay familia, que esté Movistar."

### 1.2. Titulares breves que emocionan
Frases con ritmo, aliteración, contraste.
- Ejemplo: "Fibra sin líos. Y sin miedo."

### 1.3. Hazlo sobre la persona, no sobre ti
- Incorrecto: "Hemos lanzado la mejor fibra"
- Correcto: "Para que conectes sin preocuparte. Siempre."

### 1.4. Escenas cotidianas, no tecnológicas
Como IKEA convierte una lámpara en un símbolo de lectura nocturna, Movistar muestra lo que el producto permite vivir.
- Ejemplo: "Tu hija enseñándole el árbol de Navidad a su abuela por videollamada. Y todo funciona."

### 1.5. Metáforas y analogías que acerquen lo complejo
- Ejemplo: "Fibra que llega como la luz del sol: a todos los rincones."

### 1.6. Sound bites y frases para recordar
- Ejemplo: "Sin cortes. Sin líos. Sin sustos."
- Ejemplo: "Tu vida. Conectada."

### 1.7. Beneficio mejor que característica
- Incorrecto: "Incluye App de gestión WiFi"
- Correcto: "Tienes el control de tu casa desde el móvil."

### 1.8. Inspira, pero con los pies en la tierra
Claridad + emoción cotidiana.
- Ejemplo: "El WiFi no cambia tu vida. Pero sí tu lunes a las 8."

### 1.9. Conecta desde la cultura cuando toque
Habla desde la tecnología, no sobre ella.
- Ejemplo: "2023 fue el año en que compartiste más memes por WiFi que fotos. Y nosotros estuvimos ahí."
- Ejemplo: "La primera llamada a tu ex. El primer FaceTime con tu nieta. Siempre hubo cobertura."

---

## 2. Cómo empezar un buen copy para Movistar

Secuencia de trabajo recomendada:

1. **Piensa en una sola gran idea.** Ejemplo: "Donde hay familia, que esté Movistar."
2. **Empieza desde la vida, no desde el producto.** Ejemplo: "Tu hija enseñándole el árbol a su abuela en videollamada. Y todo funciona."
3. **Convierte el beneficio en escena.** Ejemplo: "Tu wifi sin cortes. También en el baño."
4. **Elimina tecnicismos. Usa analogías.** Ejemplo: "Cobertura que te abraza hasta el último rincón."
5. **Escribe como si te estuvieran escuchando.** Ejemplo: "Lo activas. Y listo."

---

## 3. Código visual para un copy

El copy no vive solo: vive dentro de un layout. Estas reglas conectan texto y diseño:

- **Titulares generosos:** respira, impacta, ordena.
- **Jerarquía clara:** titular, subtítulo, beneficio, acción.
- **Espacio importa:** nunca atosigues con texto.
- **Textos y diseño cuentan lo mismo:** lo que dice el texto debe verse reflejado en el visual.

---

## 4. Estructura estándar de una pieza

Según el soporte, las piezas pueden variar. Este es el estándar:

### 4.1. Titular
Enfocado en captar atención y emocionar.
- Ejemplo: "Donde hay familia, que esté Movistar."

### 4.2. Subtítulo
Enfocado en aterrizar la promesa.
- Ejemplo: "Fibra adicional para conectar a los tuyos, donde estén."

### 4.3. Cuerpo
Enfocado en detallar beneficios con tono humano.
- Ejemplo: "Tus hijos, tus padres, tu segunda casa... todos conectados con calidad Movistar por solo 15 €/mes."

### 4.4. Cierre
Enfocado en cerrar con confianza y cercanía.
- Ejemplo: "Y si algún día te falla algo, estamos por ti."

---

## 5. Reglas formales de identidad verbal

Las reglas formales de copy (mayusculas, persona gramatical, tuteo, titulares, emojis, símbolos, terminologia de producto, lenguaje inclusivo, diversidad) estan definidas en `brand-voice-movistar` sección 5. No se duplican aquí.

El Creative Copywriter carga ambas skills: `brand-voice-movistar` para identidad verbal + evaluación de tono, y esta skill para técnica creativa y estructura de pieza.

---

## Cómo usan los agentes esta skill

- **Strategist:** Referencia para detectar copies en el input que violen principios formales.
- **Planner:** No la usa directamente (no escribe copies).
- **Creative Copywriter:** La carga OBLIGATORIAMENTE. Aplica los 9 principios creativos al idear territorios y copies. Las 19 reglas formales las verifica contra `brand-voice-movistar` sección 5 (fuente única); si un copy viola una regla, lo reescribe y documenta en `formal_rules_check`.
- **Art Director:** La consulta para verificar que la jerarquía visual respeta el código visual para copy (sección 3).

## Mantenimiento

- Cualquier cambio requiere validación del equipo de Comunicación Movistar.
- Cambios mayores incrementan `versión`.
- Si se detecta discrepancia con Brand Guardian v4, se sincroniza y documenta.
