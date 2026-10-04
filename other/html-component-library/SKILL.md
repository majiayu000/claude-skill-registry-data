---
name: HTML Component Library - Movistar
key: html-component-library
description: Componentes HTML reutilizables basados en los layouts oficiales de Movistar (PPT template + Brand Book + Toolkit). Consume tokens de brand-visual-guidelines-movistar y assets (fuentes, logos) vía slots de movistar-visual-production.
version: 2.4.0
owner: agent-d
status: active
depends_on:
  - brand-visual-guidelines-movistar
  - brand-visual-composition-movistar
  - movistar-visual-production
source: 250917_Movistar_PlantillaPPT.pptx (27 layouts) + 091022_Movistar_Refresh_Guidelines.pptx + 2025_Movistar_Toolkit_OnePage.pdf
---

# HTML Component Library - Movistar

Esta librería proporciona los componentes HTML que D (Art Director) utiliza para construir mockups de campaña. Los patrones están basados en los layouts oficiales de Movistar (plantilla PPT de 27 layouts, Brand Book y Toolkit). El resultado no es producción final, pero es lo suficientemente cercano para que el equipo de Comunicación pueda revisar y aprobar.

> **Importante:** esta librería NO define colores, tipografías ni assets propios. Consume tokens de `brand-visual-guidelines-movistar` y assets de `movistar-visual-production` (fuentes, logos, vía slots). Si necesitas un valor que no está en los tokens, no lo inventes: déjalo como TODO y flaggéalo.

### Carga obligatoria en todo HTML

Todo HTML producido por D usa slots que `movistar-visual-production/scripts/assemble.py` rellena. El modelo NUNCA copia base64 a mano:

1. **Tipografia**: escribir `{{FONT_FACE_MIN}}` al inicio del `<style>` (o `{{FONT_FACE}}` si se necesitan italicas o pesos 300/500).
2. **Tokens**: escribir `{{TOKENS_CSS}}` a continuación y usar las variables `--movistar-*`.
3. **Logos**: usar los slots `{{LOGO_MARK}}`, `{{LOGO_MARK_INVERSE}}`, `{{LOGO_LOCKUP}}`, `{{LOGO_LOCKUP_INVERSE}}` como valor de `src`.

### Regla de oro

Si un componente necesita un valor que no existe en los tokens, usa `var(--movistar-blue)` como fallback y anade un comentario `/* TODO: definir token para [propósito] */`.

---

## 2. Patrones de layout

Los siguientes patrones estan derivados de los 27 layouts oficiales de la plantilla PPT de Movistar, adaptados a HTML responsive. Cada patron incluye el HTML y CSS listos para copiar.

### 2.1. Header de marca (brand bar)

Barra superior con el logo M posicionado a la derecha según las reglas de grid del brand book. El logo entra por slot: `{{LOGO_MARK}}` (fondo claro) o `{{LOGO_MARK_INVERSE}}` (fondo oscuro/azul).

```html
<header class="brand-header">
  <img src="{{LOGO_MARK}}" alt="Movistar" class="brand-logo">
</header>

<style>
.brand-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 25px;
  position: relative;
}
.brand-logo {
  width: 60px;
  height: auto;
  min-width: 60px; /* Nunca inferior a 60px en digital */
}
@media (max-width: 480px) {
  .brand-header { padding: 15px; }
}
</style>
```

### 2.2. Hero con contenedor conectado

Este es el layout FIRMA de Movistar. Un contenedor conectado con vertices redondeados (8px) que contiene el texto, posicionado junto al logo M. Basado en las slides 126-131 del brand book.

```html
<section class="hero-connected">
  <div class="hero-container">
    <h1 class="hero-title">[Titular]</h1>
    <p class="hero-subtitle">[Subtitulo / propuesta de valor]</p>
    <a href="#" class="cta-primary">[CTA]</a>
  </div>
  <div class="hero-image" data-prompt="[Descripción de imagen para producción]">
    <span class="placeholder-label">[imagen pendiente]</span>
  </div>
</section>

<style>
.hero-connected {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  min-height: 500px;
  background: var(--movistar-white);
  position: relative;
}
.hero-container {
  padding: var(--space-2xl) var(--space-xl);
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: var(--movistar-blue);
  border-radius: 0 8px 8px 0;
  color: var(--movistar-white);
}
.hero-title {
  font-size: 3rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 1.1;
  margin: 0 0 var(--space-md) 0;
}
.hero-subtitle {
  font-size: 1.25rem;
  font-weight: var(--font-weight-regular);
  margin: 0 0 var(--space-lg) 0;
  opacity: 0.9;
}
.hero-image {
  background: var(--movistar-blue-light);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 14px;
}
@media (max-width: 768px) {
  .hero-connected { grid-template-columns: 1fr; }
  .hero-container { border-radius: 0 0 8px 8px; }
  .hero-image { min-height: 250px; }
  .hero-title { font-size: 2rem; }
}
</style>
```

### 2.3. Hero a sangre (fondo completo)

Fondo completo de color o imagen. Se usa para máximo impacto (tier LOVE). Basado en PPT Portada 01.

```html
<section class="hero-fullbleed" style="background-color: var(--movistar-blue);">
  <div class="hero-fullbleed-content">
    <h1>[Titular de impacto]</h1>
    <p>[Subtitulo]</p>
    <a href="#" class="cta-primary cta-on-blue">[CTA]</a>
  </div>
</section>

<style>
.hero-fullbleed {
  min-height: 500px;
  display: flex;
  align-items: center;
  padding: var(--space-2xl) var(--space-xl);
  color: var(--movistar-white);
}
.hero-fullbleed-content {
  max-width: 600px;
}
.hero-fullbleed h1 {
  font-size: 3.5rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 1.05;
  margin: 0 0 var(--space-md) 0;
}
.hero-fullbleed p {
  font-size: 1.25rem;
  margin: 0 0 var(--space-lg) 0;
  opacity: 0.9;
}
.cta-on-blue {
  background: var(--movistar-white);
  color: var(--movistar-blue);
}
.cta-on-blue:hover {
  background: var(--movistar-black);
  color: var(--movistar-white);
}
@media (max-width: 768px) {
  .hero-fullbleed { min-height: 350px; padding: var(--space-xl) var(--space-lg); }
  .hero-fullbleed h1 { font-size: 2.25rem; }
}
</style>
```

### 2.4. Sección texto + imagen

El layout interior más comun (PPT layouts 20-22). Texto a la izquierda, imagen a la derecha. Tres variantes.

```html
<!-- Variante A: 1 imagen grande -->
<section class="content-text-image">
  <div class="content-text">
    <h2>[Titulo de sección]</h2>
    <p class="content-subtitle">[Subtitulo]</p>
    <p>[Body text con detalle del producto o servicio.]</p>
  </div>
  <div class="content-image" data-prompt="[Descripción de imagen]">
    <span class="placeholder-label">[imagen pendiente]</span>
  </div>
</section>

<!-- Variante B: 2 imagenes lado a lado -->
<section class="content-text-image">
  <div class="content-text">
    <h2>[Titulo]</h2>
    <p>[Body text]</p>
  </div>
  <div class="content-image-grid">
    <div class="content-image" data-prompt="[Imagen 1]"><span class="placeholder-label">[img 1]</span></div>
    <div class="content-image" data-prompt="[Imagen 2]"><span class="placeholder-label">[img 2]</span></div>
  </div>
</section>

<style>
.content-text-image {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--space-xl);
  padding: var(--space-2xl) var(--space-xl);
  align-items: start;
}
.content-text h2 {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-sm) 0;
}
.content-subtitle {
  font-size: 1rem;
  font-weight: var(--font-weight-medium);
  color: var(--movistar-text-muted);
  margin: 0 0 var(--space-md) 0;
}
.content-image {
  background: var(--movistar-blue-light);
  border-radius: 8px;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 14px;
}
.content-image-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}
@media (max-width: 768px) {
  .content-text-image { grid-template-columns: 1fr; }
  .content-image-grid { grid-template-columns: 1fr; }
}
</style>
```

### 2.5. Grid de cards (productos / features)

Basado en PPT layout 24 (grid de iconos/imagenes, 5x3). Adaptado a HTML responsive.

```html
<section class="card-grid-section">
  <h2>[Titulo de sección]</h2>
  <div class="card-grid">
    <!-- Repetir por cada card -->
    <div class="card">
      <div class="card-image" data-prompt="[Descripción de imagen o icono]">
        <span class="placeholder-label">[img]</span>
      </div>
      <p class="card-label">[Nombre de producto o feature]</p>
    </div>
    <!-- ... más cards ... -->
  </div>
</section>

<style>
.card-grid-section {
  padding: var(--space-2xl) var(--space-xl);
}
.card-grid-section h2 {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-lg) 0;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: var(--space-lg);
}
.card {
  text-align: center;
}
.card-image {
  aspect-ratio: 16/10;
  background: var(--movistar-blue-light);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 12px;
  margin-bottom: var(--space-sm);
}
.card-label {
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  margin: 0;
}
</style>
```

### 2.6. Bloque de precio

Basado en `brand-visual-composition-movistar` sección 7 (composición de precio). Tres variantes: entero, decimal, promocional.

```html
<!-- Precio entero -->
<div class="price-block">
  <span class="price-number">20</span>
  <div class="price-details">
    <span class="price-currency">EUR</span>
    <span class="price-period">/mes</span>
  </div>
</div>

<!-- Precio con decimales -->
<div class="price-block">
  <span class="price-number">29</span>
  <div class="price-details">
    <span class="price-decimals">,95</span>
    <span class="price-currency">EUR</span>
    <span class="price-period">/mes</span>
  </div>
</div>

<!-- Precio promocional con anterior tachado -->
<div class="price-promo-block">
  <div class="price-block">
    <span class="price-number">20</span>
    <div class="price-details">
      <span class="price-decimals">,00</span>
      <span class="price-currency">EUR</span>
      <span class="price-period">/mes</span>
    </div>
  </div>
  <div class="price-previous">
    <span class="price-strikethrough">29,95EUR/mes</span>
  </div>
</div>

<style>
.price-block {
  display: flex;
  align-items: flex-start;
  gap: 4px;
  font-family: var(--font-family);
}
.price-number {
  font-size: 4rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 0.85;
  letter-spacing: -0.02em;
  color: var(--movistar-black);
}
.price-details {
  display: flex;
  flex-direction: column;
  padding-top: 0.2em;
}
.price-decimals {
  font-size: 2rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 1;
}
.price-currency {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  line-height: 1;
}
.price-period {
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  color: var(--movistar-text-muted);
}
.price-promo-block { display: flex; flex-direction: column; gap: var(--space-xs); }
.price-previous { font-size: 0.875rem; color: var(--movistar-text-muted); }
.price-strikethrough { text-decoration: line-through; }

/* Precio sobre fondo azul */
.on-blue .price-number,
.on-blue .price-decimals,
.on-blue .price-currency { color: var(--movistar-white); }
.on-blue .price-period,
.on-blue .price-previous { color: rgba(255,250,245,0.7); }
</style>
```

### 2.7. Separador de sección

Basado en PPT Separador 01/02. Divisor de texto grande entre secciones.

```html
<section class="section-divider">
  <span class="section-number">01</span>
  <h2 class="section-title">[Titulo de sección]</h2>
</section>

<style>
.section-divider {
  padding: var(--space-2xl) var(--space-xl);
  background: var(--movistar-blue);
  color: var(--movistar-white);
  display: flex;
  align-items: baseline;
  gap: var(--space-lg);
}
.section-number {
  font-size: 1rem;
  font-weight: var(--font-weight-bold);
  opacity: 0.6;
}
.section-title {
  font-size: 2.5rem;
  font-weight: var(--font-weight-extrabold);
  margin: 0;
}
</style>
```

### 2.8. Footer con legal

Footer de marca: logo M, texto legal, links opcionales.

```html
<footer class="brand-footer">
  <div class="footer-content">
    <img src="{{LOGO_MARK}}" alt="Movistar" class="footer-logo">
    <p class="legal">[Condiciones en movistar.es. Precio con IVA incluido. Consulta disponibilidad.]</p>
  </div>
</footer>

<style>
.brand-footer {
  padding: var(--space-lg) var(--space-xl);
  border-top: 1px solid var(--movistar-blue-light);
}
.footer-content {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
}
.footer-logo {
  width: 40px;
  height: auto;
  flex-shrink: 0;
}
.legal {
  font-size: 0.75rem;
  font-weight: var(--font-weight-light);
  color: var(--movistar-text-muted);
  line-height: 1.4;
  margin: 0;
}
@media (max-width: 480px) {
  .footer-content { flex-direction: column; align-items: flex-start; }
}
</style>
```

### 2.9. Galeria (2 o 3 imagenes con caption)

Basado en PPT layouts 26-27.

```html
<!-- 3 imagenes -->
<section class="gallery">
  <h2>[Titulo]</h2>
  <div class="gallery-grid gallery-3">
    <div class="gallery-item">
      <div class="gallery-image" data-prompt="[Descripción imagen 1]"><span class="placeholder-label">[img 1]</span></div>
      <p class="gallery-caption">[Caption 1]</p>
    </div>
    <div class="gallery-item">
      <div class="gallery-image" data-prompt="[Descripción imagen 2]"><span class="placeholder-label">[img 2]</span></div>
      <p class="gallery-caption">[Caption 2]</p>
    </div>
    <div class="gallery-item">
      <div class="gallery-image" data-prompt="[Descripción imagen 3]"><span class="placeholder-label">[img 3]</span></div>
      <p class="gallery-caption">[Caption 3]</p>
    </div>
  </div>
</section>

<style>
.gallery { padding: var(--space-2xl) var(--space-xl); }
.gallery h2 { font-size: 1.75rem; font-weight: var(--font-weight-bold); margin: 0 0 var(--space-lg) 0; }
.gallery-grid { display: grid; gap: var(--space-lg); }
.gallery-3 { grid-template-columns: repeat(3, 1fr); }
.gallery-2 { grid-template-columns: repeat(2, 1fr); }
.gallery-image {
  aspect-ratio: 4/3;
  background: var(--movistar-blue-light);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 14px;
}
.gallery-caption {
  font-size: 0.875rem;
  font-weight: var(--font-weight-medium);
  margin: var(--space-sm) 0 0 0;
}
@media (max-width: 768px) {
  .gallery-3, .gallery-2 { grid-template-columns: 1fr; }
}
</style>
```

### 2.10. Device showcase

Basado en PPT layout 2_12A_Texto_Device. Texto a la izquierda, mockups de dispositivo a la derecha.

```html
<section class="device-showcase">
  <div class="device-text">
    <h2>[Titulo del producto]</h2>
    <p class="device-subtitle">[Subtitulo]</p>
    <p>[Descripción del producto o servicio]</p>
    <a href="#" class="cta-primary">[CTA]</a>
  </div>
  <div class="device-frames">
    <div class="device-frame" data-prompt="[Pantalla dispositivo 1]">
      <div class="device-screen placeholder-label">[pantalla 1]</div>
    </div>
    <div class="device-frame" data-prompt="[Pantalla dispositivo 2]">
      <div class="device-screen placeholder-label">[pantalla 2]</div>
    </div>
  </div>
</section>

<style>
.device-showcase {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: var(--space-xl);
  padding: var(--space-2xl) var(--space-xl);
  align-items: center;
}
.device-text h2 {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-sm) 0;
}
.device-subtitle {
  font-size: 1rem;
  font-weight: var(--font-weight-medium);
  color: var(--movistar-text-muted);
  margin: 0 0 var(--space-md) 0;
}
.device-frames {
  display: flex;
  gap: var(--space-lg);
  justify-content: center;
}
.device-frame {
  width: 180px;
  height: 360px;
  background: var(--movistar-black);
  border-radius: 24px;
  padding: 8px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
}
.device-screen {
  width: 100%;
  height: 100%;
  background: var(--movistar-blue-light);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--movistar-text-muted);
  font-size: 12px;
}
@media (max-width: 768px) {
  .device-showcase { grid-template-columns: 1fr; }
  .device-frames { flex-wrap: wrap; }
  .device-frame { width: 140px; height: 280px; }
}
</style>
```

### 2.11. Pasos numerados (Como funciona)

Componente universal en las landings de movistar.es. Tres circulos azules numerados con título y descripción. Aparece en las 3 landings analizadas (Renting, Alarmas, Tarifas) con el mismo patron visual.

```html
<section class="steps-section">
  <h2>[Como funciona / Contrata en 3 pasos]</h2>
  <div class="steps-grid">
    <div class="step">
      <div class="step-number">1</div>
      <h3 class="step-title">[Titulo del paso]</h3>
      <p class="step-desc">[Descripción breve del paso, 1-2 líneas]</p>
    </div>
    <div class="step">
      <div class="step-number">2</div>
      <h3 class="step-title">[Titulo del paso]</h3>
      <p class="step-desc">[Descripción breve del paso, 1-2 líneas]</p>
    </div>
    <div class="step">
      <div class="step-number">3</div>
      <h3 class="step-title">[Titulo del paso]</h3>
      <p class="step-desc">[Descripción breve del paso, 1-2 líneas]</p>
    </div>
  </div>
</section>

<style>
.steps-section {
  padding: var(--space-2xl) var(--space-xl);
  background: #EFF5FB; /* azul muy claro, patron web */
  text-align: center;
}
.steps-section h2 {
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-xl) 0;
}
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-xl);
  max-width: 900px;
  margin: 0 auto;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
}
.step-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--movistar-blue);
  color: var(--movistar-white);
  font-size: 1.25rem;
  font-weight: var(--font-weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-sm);
}
.step-title {
  font-size: 1.125rem;
  font-weight: var(--font-weight-bold);
  margin: 0;
}
.step-desc {
  font-size: 0.875rem;
  color: var(--movistar-text-muted);
  margin: 0;
  max-width: 250px;
}
@media (max-width: 768px) {
  .steps-grid { grid-template-columns: 1fr; gap: var(--space-lg); }
}
</style>
```

### 2.12. Card de producto web (con dual CTA)

Card para comparadores de producto en landings web. Patron gold standard: borde fino, sin sombra, badges de estado, dual CTA (boton + link).

```html
<div class="product-card">
  <div class="product-badge product-badge--green">Novedad</div>
  <h3 class="product-name">[Nombre del producto]</h3>
  <ul class="product-features">
    <li>[Feature 1]</li>
    <li>[Feature 2]</li>
    <li>[Feature 3]</li>
  </ul>
  <div class="product-price">
    <span class="product-price-number">[20]</span>
    <div class="product-price-details">
      <span class="product-price-currency">EUR</span>
      <span class="product-price-period">/mes</span>
    </div>
  </div>
  <div class="product-ctas">
    <a href="#" class="cta-primary">[Contratar]</a>
    <a href="#" class="cta-link">[Más información] ></a>
  </div>
</div>

<style>
.product-card {
  background: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  padding: var(--space-lg);
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
/* SIN box-shadow -- patron gold standard web */
.product-badge {
  position: absolute;
  top: var(--space-md);
  left: var(--space-md);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: var(--font-weight-bold);
  color: #FFFFFF;
}
.product-badge--green { background: #048239; }
.product-badge--red { background: #8B0000; }
.product-badge--blue { background: var(--movistar-blue); }
.product-name {
  font-size: 1.25rem;
  font-weight: var(--font-weight-bold);
  margin: var(--space-lg) 0 0 0;
}
.product-features {
  list-style: disc;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: var(--movistar-text-muted);
  margin: 0;
}
.product-features li { margin-bottom: 4px; }
.product-price {
  display: flex;
  align-items: flex-start;
  gap: 4px;
}
.product-price-number {
  font-size: 2.5rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 0.85;
}
.product-price-details {
  display: flex;
  flex-direction: column;
  padding-top: 0.2em;
}
.product-price-currency { font-size: 1rem; font-weight: var(--font-weight-bold); }
.product-price-period { font-size: 0.75rem; color: var(--movistar-text-muted); }
.product-ctas {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-top: auto;
}
.cta-link {
  color: var(--movistar-blue);
  text-decoration: none;
  font-weight: var(--font-weight-bold);
  font-size: 0.875rem;
  font-family: var(--font-family);
}
.cta-link:hover { text-decoration: underline; }
</style>
```

### 2.13. WOW Banner M+ (carousel hero)

Banner horizontal para el carousel hero de Movistar Plus+. Ratio ~5:1. Layout 40/60 (copy izquierda, visual derecha). Ver `app-movistarplus.md` para reglas completas.

```html
<!-- Variante fondo claro -->
<div class="mplus-wow" style="background: var(--movistar-white);">
  <div class="mplus-wow-copy">
    <img src="{{LOGO_MARK}}" alt="Movistar" class="mplus-wow-logo">
    <p class="mplus-wow-overline">[Overline opcional: Por ser de Movistar, ...]</p>
    <h1 class="mplus-wow-title" style="color: var(--movistar-black);">[Titular bold 2-3 líneas]</h1>
    <div class="mplus-wow-price">
      <span class="mplus-wow-price-number">[15]</span>
      <div class="mplus-wow-price-details">
        <span class="mplus-wow-price-currency">EUR</span>
        <span class="mplus-wow-price-period">/mes</span>
      </div>
    </div>
    <a href="#" class="mplus-wow-cta">[Contrata aquí] ></a>
  </div>
  <div class="mplus-wow-visual" data-prompt="[Descripción de imagen]">
    <span class="placeholder-label">[imagen pendiente]</span>
  </div>
</div>

<!-- Variante fondo oscuro -->
<div class="mplus-wow mplus-wow--dark" style="background: #0a0a0a;">
  <div class="mplus-wow-copy">
    <img src="{{LOGO_MARK_INVERSE}}" alt="Movistar" class="mplus-wow-logo">
    <p class="mplus-wow-overline" style="color: #D3EEFF;">[Overline]</p>
    <h1 class="mplus-wow-title" style="color: var(--movistar-white);">[Titular]</h1>
    <a href="#" class="mplus-wow-cta" style="color: #5BA8FF;">[CTA] ></a>
  </div>
  <div class="mplus-wow-visual" data-prompt="[Descripción]">
    <span class="placeholder-label">[imagen pendiente]</span>
  </div>
</div>

<style>
.mplus-wow {
  width: 1920px;
  height: 384px;
  display: grid;
  grid-template-columns: 40% 60%;
  overflow: hidden;
  position: relative;
  font-family: var(--font-family);
}
.mplus-wow-copy {
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  z-index: 1;
}
.mplus-wow-logo {
  width: 60px;
  height: auto;
  position: absolute;
  top: 24px;
  left: 24px;
}
.mplus-wow-overline {
  font-size: 14px;
  font-weight: var(--font-weight-regular);
  margin: 0;
  color: var(--movistar-text-muted);
}
.mplus-wow-title {
  font-size: 32px;
  font-weight: var(--font-weight-extrabold);
  line-height: 1.1;
  margin: 0;
}
.mplus-wow-price {
  display: flex;
  align-items: flex-start;
  gap: 4px;
}
.mplus-wow-price-number {
  font-size: 3rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 0.85;
}
.mplus-wow-price-details {
  display: flex;
  flex-direction: column;
  padding-top: 0.2em;
}
.mplus-wow-price-currency { font-size: 1.25rem; font-weight: var(--font-weight-bold); }
.mplus-wow-price-period { font-size: 0.75rem; color: var(--movistar-text-muted); }
.mplus-wow-cta {
  color: var(--movistar-blue);
  text-decoration: underline;
  font-weight: var(--font-weight-bold);
  font-size: 1rem;
  font-family: var(--font-family);
  margin-top: 4px;
}
/* NUNCA usar boton relleno ni outline en WOW. Siempre link con underline y > */
.mplus-wow-visual {
  background: var(--movistar-blue-light);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 14px;
}
</style>
```

### 2.14. Videocartela M+ (pieza standalone)

Pieza expandida del WOW con QR, precio grande y body copy. Ratio ~16:9. Se genera solo cuando hay precio o acción concreta. Ver `app-movistarplus.md`.

```html
<div class="mplus-vc" style="background: var(--movistar-white);">
  <div class="mplus-vc-copy">
    <img src="{{LOGO_MARK}}" alt="Movistar" class="mplus-vc-logo">
    <h1 class="mplus-vc-title">[Titular expandido, más grande que en WOW]</h1>
    <p class="mplus-vc-subtitle">[Subtitulo / propuesta de valor]</p>
    <p class="mplus-vc-body">[Body copy extendido, 2-4 líneas con detalle del producto]</p>

    <div class="mplus-vc-action-row">
      <div class="mplus-vc-price-block">
        <div class="mplus-vc-product-name">[Nombre producto]</div>
        <div class="mplus-vc-price">
          <span class="mplus-vc-price-prefix">Desde</span>
          <span class="mplus-vc-price-number">[15]</span>
          <div class="mplus-vc-price-details">
            <span class="mplus-vc-price-currency">EUR</span>
            <span class="mplus-vc-price-period">/mes</span>
          </div>
        </div>
        <p class="mplus-vc-price-sub">Sin permanencia</p>
      </div>
      <div class="mplus-vc-qr" data-prompt="QR con watermark M de Movistar">
        <span class="placeholder-label">[QR + M]</span>
      </div>
    </div>

    <p class="mplus-vc-help">[Si necesitas ayuda, llama al 900 xxx xxx]</p>
  </div>
  <div class="mplus-vc-visual" data-prompt="[Misma imagen que el WOW, más grande]">
    <span class="placeholder-label">[imagen pendiente]</span>
  </div>
</div>

<style>
.mplus-vc {
  width: 1920px;
  height: 1080px;
  display: grid;
  grid-template-columns: 45% 55%;
  overflow: hidden;
  position: relative;
  font-family: var(--font-family);
}
.mplus-vc-copy {
  padding: 48px 56px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  z-index: 1;
}
.mplus-vc-logo {
  width: 72px;
  height: auto;
  position: absolute;
  top: 32px;
  left: 32px;
}
.mplus-vc-title {
  font-size: 48px;
  font-weight: var(--font-weight-extrabold);
  line-height: 1.05;
  margin: 0;
  color: var(--movistar-black);
}
.mplus-vc-subtitle {
  font-size: 20px;
  font-weight: var(--font-weight-bold);
  color: var(--movistar-blue);
  margin: 0;
}
.mplus-vc-body {
  font-size: 16px;
  font-weight: var(--font-weight-regular);
  line-height: 1.5;
  margin: 0;
  color: var(--movistar-text-muted);
}
.mplus-vc-action-row {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 8px;
}
.mplus-vc-product-name {
  font-size: 24px;
  font-weight: var(--font-weight-extrabold);
  color: var(--movistar-blue);
}
.mplus-vc-price {
  display: flex;
  align-items: flex-start;
  gap: 4px;
}
.mplus-vc-price-prefix {
  font-size: 14px;
  font-weight: var(--font-weight-regular);
  color: var(--movistar-text-muted);
  align-self: flex-start;
  padding-top: 4px;
}
.mplus-vc-price-number {
  font-size: 4rem;
  font-weight: var(--font-weight-extrabold);
  line-height: 0.85;
  letter-spacing: -0.02em;
}
.mplus-vc-price-details {
  display: flex;
  flex-direction: column;
  padding-top: 0.3em;
}
.mplus-vc-price-currency { font-size: 1.5rem; font-weight: var(--font-weight-bold); }
.mplus-vc-price-period { font-size: 0.875rem; color: var(--movistar-text-muted); }
.mplus-vc-price-sub {
  font-size: 14px;
  font-weight: var(--font-weight-bold);
  margin: 0;
}
.mplus-vc-qr {
  width: 120px;
  height: 120px;
  background: #FFFFFF;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 12px;
  flex-shrink: 0;
}
.mplus-vc-help {
  font-size: 12px;
  color: var(--movistar-text-muted);
  margin: 0;
}
.mplus-vc-visual {
  background: var(--movistar-blue-light);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  color: var(--movistar-text-muted);
  font-size: 14px;
}
</style>
```

---

## 3. Componentes base

### 3.1. CTA principal

```html
<a href="#" class="cta-primary">[CTA aquí]</a>

<style>
.cta-primary {
  display: inline-block;
  padding: 14px 32px;
  background: var(--movistar-cta);
  color: var(--movistar-white);
  text-decoration: none;
  font-weight: var(--font-weight-bold);
  font-family: var(--font-family);
  border-radius: 8px;
  font-size: 1rem;
  letter-spacing: 0.02em;
  transition: background 0.2s;
}
.cta-primary:hover { background: var(--movistar-cta-hover); }
</style>
```

### 3.2. CTA secundario

```html
<a href="#" class="cta-secondary">[CTA secundario]</a>

<style>
.cta-secondary {
  display: inline-block;
  padding: 14px 32px;
  background: transparent;
  color: var(--movistar-cta);
  text-decoration: none;
  font-weight: var(--font-weight-bold);
  font-family: var(--font-family);
  border: 2px solid var(--movistar-cta);
  border-radius: 8px;
  font-size: 1rem;
  letter-spacing: 0.02em;
  transition: all 0.2s;
}
.cta-secondary:hover {
  background: var(--movistar-cta);
  color: var(--movistar-white);
}
</style>
```

### 3.3. CTA link (secundario web)

En landings web, el CTA secundario NO es un boton outline sino un link de texto con flecha. Usar este componente en vez de `cta-secondary` cuando se genera una landing para movistar.es.

```html
<a href="#" class="cta-link">[Más información] ></a>

<style>
.cta-link {
  display: inline-block;
  color: var(--movistar-blue);
  text-decoration: none;
  font-weight: var(--font-weight-bold);
  font-family: var(--font-family);
  font-size: 1rem;
  padding: 4px 0;
}
.cta-link:hover { text-decoration: underline; }
</style>
```

> **Cuando usar cada CTA secundario:** `cta-secondary` (boton outline) para piezas offline (email, display, tienda). `cta-link` para landing web (movistar.es). Ver `app-web.md` sección "CTAs en landing web".

### 3.5. Contenedor destacado

Para resaltar una palabra o dato específico. Máximo 1 por pieza. Vertices redondeados a 8px.

```html
<span class="highlight-container">[dato destacado]</span>

<style>
.highlight-container {
  display: inline-block;
  padding: 4px 12px;
  background: var(--movistar-blue-light);
  border-radius: 8px;
  font-weight: var(--font-weight-bold);
}
/* Variantes por color secundario */
.highlight-green { background: var(--movistar-green-light); }
.highlight-yellow { background: var(--movistar-yellow-light); }
.highlight-coral { background: var(--movistar-coral-light); }
</style>
```

### 3.6. Placeholder semantico para imagen

```html
<div class="placeholder-image"
     data-prompt="[Descripción de imagen para producción]"
     data-format="[email-hero|display|landing-hero|social-feed]"
     data-dimensions="[600x300]"
     style="aspect-ratio: 2/1;">
  <span class="placeholder-label">[imagen pendiente -- ver data-prompt]</span>
</div>

<style>
.placeholder-image {
  width: 100%;
  background: var(--movistar-blue-light);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--movistar-blue);
  border-radius: 8px;
}
.placeholder-label {
  color: var(--movistar-text-muted);
  font-size: 14px;
  font-family: var(--font-family);
}
</style>
```

---

## 4. Landing page completa (ejemplo de ensamblaje)

Ejemplo de como D ensambla los componentes de las secciones 2-3 en una landing page completa:

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Titulo de campaña]</title>
<style>
  /* 1. Tipografia vía slot -- assemble.py lo rellena. NUNCA pegar base64 a mano */
  {{FONT_FACE_MIN}}

  /* 2. CSS variables -- COPIAR TAL CUAL de brand-visual-guidelines-movistar sección 5 */
  /* NOTA: para landing web (movistar.es), cambiar --movistar-white a #FFFFFF
     y --movistar-bg a #FFFFFF. Usar #EFF5FB para secciones alternas.
     #FFFAF5 es solo para piezas offline. Ver app-web.md. */
  :root {
    --movistar-blue: #0066FF;
    --movistar-white: #FFFAF5; /* offline; en web cambiar a #FFFFFF */
    --movistar-black: #262423;
    --movistar-blue-light: #D3EEFF;
    --movistar-green-light: #CEF7BF;
    --movistar-yellow-light: #FFE99C;
    --movistar-coral-light: #FFC5A8;
    --movistar-blue-dark: #022D67;
    --movistar-green-dark: #38552B;
    --movistar-yellow-dark: #5E4A09;
    --movistar-coral-dark: #62301A;
    --movistar-primary: var(--movistar-blue);
    --movistar-bg: var(--movistar-white);
    --movistar-text: var(--movistar-black);
    --movistar-text-muted: #6F7176;
    --movistar-cta: var(--movistar-blue);
    --movistar-cta-hover: #005EEB;
    --font-family: "Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
    --font-weight-light: 300;
    --font-weight-regular: 400;
    --font-weight-medium: 500;
    --font-weight-bold: 700;
    --font-weight-extrabold: 800;
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 40px;
    --space-2xl: 64px;
  }
  body {
    font-family: var(--font-family);
    color: var(--movistar-text);
    background-color: var(--movistar-bg);
    line-height: 1.5;
  }
  h1 { font-size: 2.25rem; font-weight: var(--font-weight-extrabold); line-height: 1.15; }
  h2 { font-size: 1.75rem; font-weight: var(--font-weight-regular); line-height: 1.2; } /* subtitulos Regular (Refresh Guidelines 2025) */
  h3 { font-size: 1.25rem; font-weight: var(--font-weight-medium); line-height: 1.3; }
  p  { font-size: 1rem; font-weight: var(--font-weight-regular); }
  * { margin: 0; padding: 0; box-sizing: border-box; }

  /* 3. Estilos de componentes usados (copiar de secciones 2-3 de esta skill) */
</style>
</head>
<body>
  <!-- Brand header con M (sección 2.1 -- slot {{LOGO_MARK}} fondo claro / {{LOGO_MARK_INVERSE}} fondo oscuro) -->
  <!-- Hero (conectado 2.2, a sangre 2.3, o texto+imagen 2.4 según tier) -->
  <!-- Sección de contenido (2.4, 2.5, 2.10) -->
  <!-- Precio (2.6 si aplica) -->
  <!-- CTA de refuerzo (3.1 o 3.2) -->
  <!-- Footer con legal (2.8) -->
</body>
</html>
```

**OBLIGATORIO:** D copia el bloque `:root` de arriba tal cual. NO define variables propias (`--blue`, `--font`, `--dark`, etc.). Los nombres `--movistar-*`, `--space-*` y `--font-weight-*` son los que consumen todos los componentes de esta skill. Si D usa nombres distintos, los componentes no funcionan.

D ensambla los componentes de las secciones 2-3 según las necesidades de la campaña. La estructura es flexible: no todas las campañas necesitan todos los componentes. El tier (LOVE/CHOOSE/BUY) determina la libertad visual (ver `communication-tiers-movistar`).

---

## 5. Email (HTML table-based)

### 5.1. Estructura base email

Los emails usan layout basado en tablas para compatibilidad con Outlook y otros clientes legacy. MAIA produce la versión desktop (600px). **No se pueden usar CSS variables en email** porque la mayoria de clientes de correo no las soportan -- se usan valores HEX literales tomados de los tokens. Ver `app-email.md` para la guia completa de bloques modulares.

```html
<!-- Wrapper -->
<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color:#F5F5F5;">
  <tr><td align="center">
    <!-- Body -->
    <table role="presentation" cellpadding="0" cellspacing="0" width="600" style="background-color:#FFFAF5;font-family:'Movistar Sans','Helvetica Neue',Helvetica,Arial,sans-serif;">

      <!-- HEADER: M logo top-right -->
      <tr>
        <td align="right" style="padding:20px 24px 0 24px;">
          <img src="{{LOGO_MARK}}" alt="Movistar" width="64" height="47" style="display:block;" />
        </td>
      </tr>

      <!-- BADGE (opcional, solo emails para clientes existentes) -->
      <tr>
        <td style="padding:16px 24px 0 24px;">
          <span style="display:inline-block;padding:6px 16px;background:#0066FF;color:#FFFAF5;font-size:13px;font-weight:700;border-radius:9999px;">Ser cliente tiene ventajas</span>
        </td>
      </tr>

      <!-- HERO: titular + imagen -->
      <tr>
        <td style="padding:16px 24px 0 24px;">
          <h1 style="margin:0 0 16px 0;font-size:32px;font-weight:800;color:#262423;line-height:1.15;">[Titular con <span style="color:#0066FF;">keyword</span> destacada]</h1>
        </td>
      </tr>
      <tr>
        <td>
          <div style="width:375px;height:220px;background:#EFF5FB;" data-prompt="[Fotografía lifestyle o producto en contexto]">
            <!-- {{SLOT_HERO_IMAGE}} -->
          </div>
        </td>
      </tr>

      <!-- PRECIO (cuando aplica) -->
      <tr>
        <td align="center" style="padding:24px;">
          <span style="display:block;font-size:14px;font-weight:700;color:#0066FF;">Desde</span>
          <span style="font-size:64px;font-weight:800;color:#262423;line-height:1;">15</span>
          <span style="font-size:24px;font-weight:800;color:#262423;">€</span>
          <span style="font-size:14px;color:#6F7176;">/mes</span>
        </td>
      </tr>

      <!-- CTA -->
      <tr>
        <td align="center" style="padding:0 24px 24px 24px;">
          <a href="#" style="display:inline-block;padding:14px 32px;background:#0066FF;color:#FFFAF5;text-decoration:none;font-weight:700;border-radius:9999px;font-size:16px;">[CTA texto]</a>
        </td>
      </tr>

      <!-- BENEFICIOS 2x2 (ejemplo) -->
      <tr>
        <td style="padding:0 24px;">
          <table role="presentation" cellpadding="0" cellspacing="8" width="100%">
            <tr>
              <td width="50%" style="background:#EFF5FB;border-radius:8px;padding:16px;vertical-align:top;">
                <!-- icono 48px -->
                <p style="margin:0 0 4px 0;font-size:16px;font-weight:700;color:#262423;">[Titulo beneficio]</p>
                <p style="margin:0;font-size:14px;color:#6F7176;line-height:1.4;">[Body 2-3 líneas]</p>
              </td>
              <td width="50%" style="background:#EFF5FB;border-radius:8px;padding:16px;vertical-align:top;">
                <p style="margin:0 0 4px 0;font-size:16px;font-weight:700;color:#262423;">[Titulo beneficio]</p>
                <p style="margin:0;font-size:14px;color:#6F7176;line-height:1.4;">[Body 2-3 líneas]</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- FOOTER LEGAL -->
      <tr>
        <td style="padding:24px;text-align:center;">
          <p style="margin:0;font-size:12px;color:#6F7176;line-height:1.5;">[Condiciones de la oferta]</p>
          <p style="margin:8px 0 0 0;font-size:12px;color:#6F7176;">
            <a href="#" style="color:#6F7176;">Aviso legal</a> |
            <a href="#" style="color:#6F7176;">Protección de datos</a> |
            <a href="#" style="color:#6F7176;">Baja de comunicaciones</a>
          </p>
        </td>
      </tr>

    </table>
  </td></tr>
</table>
```

### 5.2. Reglas de email-safety

Cuando D produce email:

- Usa tablas para layout (compatibilidad Outlook).
- CSS inline para reglas criticas. Los CSS variables NO funcionan en email: usar valores literales de los tokens.
- No usa Flexbox/Grid para layout principal.
- Imagenes con `alt` siempre presentes.
- Ancho de producción MAIA: **600px** (desktop). La adaptación mobile la gestiona maquetación.
- Tipografias web safe con fallback: `font-family: "Movistar Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;`
- Botones CTA: usar `<a>` estilizado, no `<button>`. `border-radius: 9999px` (pill).
- Colores siempre con los HEX de los tokens (#0066FF, #FFFAF5, #262423). Nunca los antiguos (#019DF4, #00B5E2).
- Emails son modulares: combinar bloques según producto. Ver `app-email.md` para el catálogo completo de 15 bloques.

---

## 6. Composiciones SVG (solo vector bajo petición explicita)

> **Nota v2.1:** por defecto, los canales de imagen (tienda, social, exterior, M+ banners) se producen como **HTML de dimensiones fijas + render a PNG** (ver `movistar-visual-production`, workflow paso 2 y 5). Esta sección aplica UNICAMENTE cuando se pide un entregable vectorial editable. Los slots ({{FONT_FACE_MIN}}, {{LOGO_*}}) funcionan igual en SVG: assemble.py los rellena.

### 6.1. Reglas generales de composición SVG

- **Dimensiones reales del soporte.** El `viewBox` del SVG debe coincidir con las dimensiones del formato final (ej. 1080x1080 para feed Instagram, 800x1200 para caballete tienda).
- **Grid y jerarquía Y.** Aplicar las mismas reglas de `brand-visual-composition-movistar`: calcular X (lado corto / 16), posicionar logo, calcular Y para jerarquía tipografica.
- **Tipografia embebida (OBLIGATORIO).** Todo SVG debe incluir `<defs><style>{{FONT_FACE_MIN}}</style></defs>` al inicio; assemble.py rellena el slot con el @font-face en base64. NUNCA pegar base64 a mano. Además, usar `font-family="Movistar Sans, Helvetica Neue, Helvetica, Arial, sans-serif"` en todos los `<text>`. Los atributos `font-weight` deben coincidir con los pesos oficiales: 300 (Light), 400 (Regular), 500 (Medium), 700 (Bold), 800 (ExtraBold).
- **Colores (paleta cerrada).** Usar SOLO estos HEX: #0066FF, #FFFAF5, #262423, #d3eeff, #cef7bf, #ffe99c, #ffc5a8, #6F7176, #005EEB. Ningun otro HEX esta permitido en piezas de campaña. NO inventar tonos "navy", "dark blue" ni similares. **Unica excepción:** los colores semanticos de feedback de `brand-visual-composition-movistar` sección 4 (positivo #048239, alerta #926C00, negativo #C10000 y sus hovers) se permiten SOLO en interfaces funcionales (web logada, formularios, estados de error), nunca como recurso gráfico de campaña.
- **Logo.** Usar `<image href="{{LOGO_MARK}}">` (fondo claro) o `<image href="{{LOGO_MARK_INVERSE}}">` (fondo oscuro/azul); assemble.py rellena el data URI. No usar `<text>` ni `<g>` con comentarios placeholder.
- **Vertices redondeados.** Todos los contenedores deben usar `rx="8"` (8px).
- **Fotografias.** Marcar con `<rect>` + atributo `data-prompt` describiendo la imagen necesaria. Producción sustituye el rect por la foto real.

### 6.2. Composición base -- formato vertical (tienda, stories)

```svg
<svg viewBox="0 0 800 1200" xmlns="http://www.w3.org/2000/svg"
     font-family="Movistar Sans, Helvetica Neue, Helvetica, Arial, sans-serif">
  <defs>
    <style>
      {{FONT_FACE_MIN}}
    </style>
  </defs>

  <!-- Fondo -->
  <rect width="800" height="1200" fill="#FFFAF5"/>

  <!-- Placeholder fotografía -->
  <rect x="0" y="0" width="800" height="500" rx="8"
        fill="#d3eeff" stroke="#0066FF" stroke-width="2" stroke-dasharray="8,4"
        data-prompt="[Descripción de imagen para producción]"
        data-format="[tienda-caballete|stories]"/>
  <text x="400" y="260" text-anchor="middle" fill="#6F7176" font-size="16">
    [imagen pendiente -- ver data-prompt]
  </text>

  <!-- Titular -->
  <text x="50" y="570" fill="#262423" font-size="48" font-weight="800">
    [Titular]
  </text>

  <!-- Subtitulo -->
  <text x="50" y="630" fill="#6F7176" font-size="22" font-weight="500">
    [Subtitulo / propuesta de valor]
  </text>

  <!-- CTA -->
  <rect x="50" y="680" width="250" height="50" rx="8" fill="#0066FF"/>
  <text x="175" y="712" text-anchor="middle" fill="#FFFAF5" font-size="18" font-weight="700">
    [CTA]
  </text>

  <!-- Logo M fondo claro: slot rellenado por assemble.py -->
  <image href="{{LOGO_MARK}}"
         x="720" y="1110" width="60" height="50" aria-label="Movistar"/>
</svg>
```

### 6.3. Composición base -- formato cuadrado (feed social)

```svg
<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg"
     font-family="Movistar Sans, Helvetica Neue, Helvetica, Arial, sans-serif">
  <defs>
    <style>
      {{FONT_FACE_MIN}}
    </style>
  </defs>

  <!-- Fondo azul Movistar -->
  <rect width="1080" height="1080" fill="#0066FF"/>

  <!-- Titular en blanco -->
  <text x="80" y="200" fill="#FFFAF5" font-size="64" font-weight="800">
    [Titular línea 1]
  </text>
  <text x="80" y="280" fill="#FFFAF5" font-size="64" font-weight="800">
    [Titular línea 2]
  </text>

  <!-- Subtitulo -->
  <text x="80" y="350" fill="#FFFAF5" font-size="28" font-weight="500" opacity="0.85">
    [Subtitulo]
  </text>

  <!-- Placeholder fotografía -->
  <rect x="80" y="420" width="920" height="460" rx="8"
        fill="#d3eeff" stroke="#FFFAF5" stroke-width="2" stroke-dasharray="8,4"
        data-prompt="[Descripción de imagen para producción]"
        data-format="[feed-instagram|feed-facebook]"/>
  <text x="540" y="660" text-anchor="middle" fill="#6F7176" font-size="16">
    [imagen pendiente -- ver data-prompt]
  </text>

  <!-- Logo M fondo oscuro/azul: slot rellenado por assemble.py -->
  <image href="{{LOGO_MARK_INVERSE}}"
         x="970" y="990" width="75" height="63" aria-label="Movistar"/>
</svg>
```

### 6.3b. Composición alternativa -- feed social fondo claro con producto (Meta)

La plantilla 6.3 usa fondo azul solido, adecuada para piezas de contenido/deporte. Pero el patron más frecuente en META real es fondo claro (beige, salmon, verde mint) con producto en cutout. Ver `app-meta.md` para el catálogo completo de layouts.

```svg
<svg viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg"
     font-family="Movistar Sans, Helvetica Neue, Helvetica, Arial, sans-serif">
  <defs>
    <style>
      {{FONT_FACE_MIN}}
    </style>
  </defs>

  <!-- Fondo claro (beige Movistar, salmon, verde mint o azul claro según campaña) -->
  <rect width="1080" height="1080" fill="#FFFAF5"/>

  <!-- Titular (ExtraBold negro, keyword en azul) -->
  <text x="540" y="180" text-anchor="middle" fill="#262423" font-size="72" font-weight="800">
    [Titular línea 1]
  </text>
  <text x="540" y="270" text-anchor="middle" fill="#262423" font-size="72" font-weight="400">
    [Titular línea 2]
  </text>

  <!-- Placeholder producto en cutout (centrado) -->
  <rect x="240" y="300" width="600" height="480" rx="8"
        fill="#d3eeff" stroke="#0066FF" stroke-width="2" stroke-dasharray="8,4"
        data-prompt="[Producto en cutout sobre fondo transparente]"
        data-format="[feed-meta]"/>
  <text x="540" y="550" text-anchor="middle" fill="#6F7176" font-size="16">
    [producto pendiente -- ver data-prompt]
  </text>

  <!-- Precio XXL (si aplica) -->
  <text x="80" y="880" fill="#262423" font-size="96" font-weight="800">
    0<tspan font-size="48">€/mes</tspan>
  </text>
  <text x="80" y="920" fill="#6F7176" font-size="28" font-weight="400">
    Con miMovistar
  </text>

  <!-- "Ser Cliente tiene ventajas" (si aplica) -->
  <text x="80" y="1020" fill="#262423" font-size="28" font-weight="400">
    Ser Cliente <tspan font-style="italic">tiene ventajas</tspan>
  </text>

  <!-- Logo M fondo claro -->
  <image href="{{LOGO_MARK}}"
         x="970" y="990" width="75" height="63" aria-label="Movistar"/>
</svg>
```

> **Nota META:** en piezas para Meta/Social, NO incluir boton CTA pill. El CTA lo proporciona la plataforma (boton nativo del anuncio). Solo en stories se puede anadir "Llama gratis al 900..." como refuerzo. Ver `app-meta.md` para todas las reglas.

### 6.4. Composición base -- formato apaisado (exterior/OOH, display grande)

```svg
<svg viewBox="0 0 1920 600" xmlns="http://www.w3.org/2000/svg"
     font-family="Movistar Sans, Helvetica Neue, Helvetica, Arial, sans-serif">
  <defs>
    <style>
      {{FONT_FACE_MIN}}
    </style>
  </defs>

  <!-- Fondo -->
  <rect width="1920" height="600" fill="#FFFAF5"/>

  <!-- Placeholder fotografía (mitad izquierda) -->
  <rect x="0" y="0" width="960" height="600" rx="8"
        fill="#d3eeff" stroke="#0066FF" stroke-width="2" stroke-dasharray="8,4"
        data-prompt="[Descripción de imagen para producción]"
        data-format="[exterior-valla|display-980x250]"/>
  <text x="480" y="310" text-anchor="middle" fill="#6F7176" font-size="18">
    [imagen pendiente -- ver data-prompt]
  </text>

  <!-- Titular (mitad derecha, grande, legible a distancia) -->
  <text x="1020" y="250" fill="#262423" font-size="72" font-weight="800">
    [Titular corto]
  </text>

  <!-- Subtitulo -->
  <text x="1020" y="330" fill="#6F7176" font-size="32" font-weight="500">
    [Subtitulo]
  </text>

  <!-- CTA -->
  <rect x="1020" y="380" width="300" height="60" rx="8" fill="#0066FF"/>
  <text x="1170" y="418" text-anchor="middle" fill="#FFFAF5" font-size="22" font-weight="700">
    [CTA]
  </text>

  <!-- Logo M fondo claro: slot rellenado por assemble.py -->
  <image href="{{LOGO_MARK}}"
         x="1800" y="28" width="90" height="75" aria-label="Movistar"/>
</svg>
```

### 6.5. Cuando usar cada plantilla

| Canal | Plantilla base | Adaptar viewBox a |
|---|---|---|
| Tienda -- caballete (70x100 cm) | Vertical | Proporciones del caballete (impresion) |
| Tienda -- pantalla digital (55") | Vertical | 1080x1920 (mismo ratio y pixeles que stories) |
| Stories (Instagram, Meta) | Vertical | 1080x1920 |
| Feed social (Instagram, Facebook) | Cuadrado | 1080x1080 |
| Exterior / OOH | Apaisado | Dimensiones reales del soporte |
| M+ banner | Apaisado o cuadrado según formato | Segun especificación M+ |
| Display grande (980x250) | Apaisado | 980x250 |
| Display MPU (300x250) | Cuadrado o vertical según layout | 300x250 |

D adapta la plantilla al caso: cambia copies, ajusta proporciones, aplica el tier visual (LOVE = más libertad cromatica, BUY = precio como foco). Las plantillas son punto de partida, no camisas de fuerza.

> **Nota display:** el fondo del banner NO es siempre `#FFFAF5`. Cambia según campaña: beige para hogar, azul solido para Swap/contenido, verde mint para dispositivos, bicolor para FTTR. Ver `app-ads.md` para layouts completos por formato y tipo de campaña, incluyendo reglas de CTA por formato (320x100 sin CTA pill, 300x600 siempre con CTA, etc.).

---

## 7. Reglas transversales

### 7.1. Accesibilidad mínima

- Contraste mínimo AA en todo texto sobre fondo (ver tabla de combinaciones en `brand-visual-guidelines-movistar`).
- `alt` semantico en imagenes (no "imagen": describir contenido).
- Estructura semantica (`<h1>` único por documento, jerarquía sin saltos).
- `lang="es"` en `<html>`.
- CTAs con texto descriptivo (no "click aquí").

### 7.2. Anti-patrones

- NO usar React, Vue, Tailwind CDN u otros frameworks.
- NO producir HTML minificado o sin indentar.
- NO inventar paleta o tipografía. Consumir siempre de `brand-visual-guidelines-movistar`.
- NO usar los colores antiguos (#019DF4, tipografía "Telefónica"). Si los encuentras en cualquier referencia, ignoralos y usa los tokens vigentes.
- NO generar fotografias vía API externa. D si produce SVG y composiciones HTML/CSS renderizables. Las fotografias van como placeholders semanticos con `data-prompt` para que producción las complete.
- NO reescribir copies del Estrategia Creativa. Usar los originales, flaggear si no caben.
- NO crear disenos "creativos" que rompan los patrones de esta skill sin justificarlo en `design_rationale_<sub>.md`.
- NO usar `border-radius: 4px`. Siempre 8px en digital (regla del brand book).
- NO colocar texto con `<text>` como placeholder de logo. Usar los slots `{{LOGO_MARK}}` / `{{LOGO_MARK_INVERSE}}`.

### 7.3. Contenedores: siempre vertices redondeados

Todos los contenedores en toda pieza tienen vertices redondeados a 8px en digital (1/6 del margen en print). Esto incluye: contenedores conectados, contenedores de imagen, contenedores de resalte, cards, botones. Sin excepciones.

---

## 8. Estructura de design_rationale_<sub>.md

Cada pieza viene acompanada de un rationale:

```markdown
# Design Rationale - <campaign-slug> / <piece-name>

## Decisión visual principal
[Que jerarquía sigue y por que refuerza la idea creativa del Plan]

## Layout
[Tabla / single column / multiples columnas y por que]

## Adaptación mobile
[Que cambia entre desktop y mobile. Por que]

## Alternativas descartadas
- **[Alternativa A]**: descartada porque [razon]
- **[Alternativa B]**: descartada porque [razon]

## Flags / sugerencias
- [Si crees que la estrategia o el copy pueden mejorar, dilo aquí con propuesta concreta]

## TODOs para producción
- [Cosas que necesitan ser completadas por el equipo de producción]
```

---

## 9. Mantenimiento

- Los tokens visuales viven SOLO en `brand-visual-guidelines-movistar`. Esta libreria los consume, no los define.
- Las reglas de composición (grid, jerarquía Y, posición de logo) viven en `brand-visual-composition-movistar`.
- La tipografía (woff2) y los logos (SVG) viven como archivos en `movistar-visual-production/brand/` y se inyectan vía slots con assemble.py.
- Cuando el design system completo de Movistar este disponible para integración, sustituir los componentes placeholder por los oficiales.
- Anadir componentes adicionales solo cuando se usen en al menos 2 campañas diferentes.
- Cada cambio incrementa `versión` del skill.
