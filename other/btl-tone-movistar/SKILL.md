---
name: Tono BTL y Guardrails Operativos - Movistar
key: btl-tone-movistar
description: Tipologias de tono BTL (desarrollo/captación/fidelización), priorización de sesgos por tipologia, y guardrails operativos (acuerdo Apple, partners, Peace of Life).
version: 2.0.0
owner: superreal
status: active
source: Maia BTL Specialist v2 Peace of Life (Secciones D.4, K, L) - validado por Comunicación Movistar
depends_on:
  - brand-voice-movistar
  - communication-tiers-movistar
---

# Tono BTL y Guardrails Operativos - Movistar

Skill compartida. Planner y Creative Copywriter la cargan para campañas BTL (email, SMS, banners descodificador, push). Complementa `brand-voice-movistar` (tono general) con las particularidades del canal directo al cliente.

El tono BTL se construye SOBRE el tono general de Movistar, no lo reemplaza. Primero aplican las reglas de `brand-voice-movistar`; luego las de esta skill.

---

## 1. Tipologias de tono BTL

### 1.1. Tono comercial: Desarrollo (clientes Movistar)

**Objetivo:** Desarrollar al cliente dentro del portfolio de Movistar y partners.

**Tono:** Cercania, "familia Movistar", cuidamos a los nuestros durante toda la relación.

**Mensaje:** Ofertas/propuestas por pertenencia a la comunidad + beneficio humano.

**Enfasis:** Personalización según necesidad/momento de vida.

**Ejemplos:**
- "Por ser cliente" / "Esta oferta es solo para ti, por ser de Movistar"
- "La fibra que necesitas para tu segundo hogar"
- "Entretenimiento para todos"

### 1.2. Tono comercial: Captación (clientes de otros operadores con consentimiento)

**Contexto:** No nos conocen. Enfoque de descubrimiento del portfolio: "tenemos soluciones que no imaginan."

**Fortalezas a poner en valor:** Experiencia Movistar + intangibles + beneficios directos (no solo precio).

**Mensajes guia:**
- "Más de lo que imaginas, por menos de lo que piensas"
- "Con la mejor conectividad 5G"
- "Almacenamiento ilimitado con Movistar Cloud incluido"

### 1.3. Tono fidelización

**Objetivo:** Que el cliente saque el máximo partido a lo contratado y fortalecer relación marca-cliente.

**Contenidos tipicos:** Estrenos destacados, vision de expertos, nuevos partners, mejoras del producto/servicio, beneficios "por ser de Movistar."

**Tono:** Marca que acompana y enriquece el dia a dia; relación solida más alla de la venta.

**Mensajes guia:**
- "Los estrenos que no te puedes perder en noviembre"
- "El toque British llega a Movistar (BBC Player)"
- "Consigue hasta cinco dispositivos por ser de Movistar"

---

## 2. Priorización de sesgos por tipologia

Usa estos sesgos cuando encajen con la oferta/contenido. No forzar.

**Comercial (Desarrollo y Captación):**
- Escasez y aversion a la perdida para promos con fecha
- Prueba social y autoridad para captación (somos lideres)
- Anclaje para ofertas con descuento
- Efecto dotación para paquetes convergentes
- Efecto halo para dispositivos y partners

**Fidelización:**
- Aversion a la perdida para incentivar consumo de contenidos ("no te lo pierdas")
- Autoridad para destacar contenidos ("el estreno más visto...", "más de X millones de visionados...")
- Efecto halo vía expertos y rigor

---

## 3. Guardrails operativos

Reglas de negocio duras que el sistema debe verificar. No son sugerencias.

### 3.1. Acuerdo Apple (BLOQUEANTE)
**Regla:** Clientes Apple NUNCA reciben promos de dispositivos de competencia.
**Aplicación:** El Creative Copywriter debe verificar el segmento del público objetivo antes de escribir copies de Dispositivos. Si el brief incluye público Apple, las piezas de dispositivos Android/Samsung/etc. NO se generan para ese segmento.
**Si se incumple:** Flag bloqueante. La pieza no se entrega.

### 3.2. Partners
**Regla:** Respetar siempre guias de cobranding, naming oficial y aplicación de logos de cada partner.
**Aplicación:** Ver los mandatories específicos en `product-verticals-movistar` por cada vertical con partner.

### 3.3. Consistencia Peace of Life
**Regla:** Si una propuesta creativa no cumple con el principio de "Hablamos como personas que cuidan de personas" y no proyecta la emoción Peace of Life, debe ser reformulada.
**Aplicación:** Se verifica contra las reglas formales de `brand-voice-movistar`. No requiere scoring subjetivo.

### 3.4. Protección de marca
- No emitir juicios de valor negativos sobre Movistar
- No hacer comparativas directas agresivas o desleales hacia la competencia
- Si no se dispone de un dato, no inventarlo. Usar formulación genérica o placeholder.

---

## Como usan los agentes esta skill

### Planner
- Determina la tipologia BTL (comercial desarrollo / comercial captación / fidelización) para cada canal
- La tipologia influye en el tono que el Creative Copywriter debe usar
- Si el brief mezcla captación y desarrollo en el mismo canal, lo marca como flag

### Creative Copywriter
- Carga OBLIGATORIAMENTE esta skill para campañas BTL
- Aplica el tono de la tipologia correspondiente (sección 1)
- Selecciona sesgos de behavioral economics adecuados (sección 2)
- Verifica guardrails (sección 3) antes de entregar, especialmente el acuerdo Apple

### Campaign Manager
- En Cierre, verifica que la tipologia BTL es coherente con el brief
- Verifica que no hay incumplimiento del acuerdo Apple

---

## Mantenimiento

- Si se firman nuevos acuerdos comerciales (tipo acuerdo Apple), anadirlos a la sección 3.
- Cambios mayores incrementan `versión`.
