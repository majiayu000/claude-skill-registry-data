---
name: Componentes One-Pager del Planner - Movistar
key: planner-onepager-components-movistar
description: CSS verificado para los one-pagers HTML del Maia Planner. Cubre base compartida, calendario Gantt y carga por soporte. Brief Canales aun no verificado (pendiente fixture). Corrige bugs C1, C3 y C4 del diagnostico. No define colores propios (fuente unica en 02-planner.md).
version: 0.2.0
owner: client
status: active
depends_on: []
---

# Componentes One-Pager del Planner - Movistar

## Por qué existe esta skill

Antes de esta skill, el Maia Planner no tenía ningún fichero -- ni skill, ni plantilla, ni bloque de código -- que definiera el CSS real de sus 8 one-pagers HTML. Solo tenía una descripción en prosa (`02-planner.md`, sección "Exportes visuales", líneas 270-453: colores en tabla, radios y paddings sueltos en texto) y el modelo escribía el CSS desde cero en cada ticket, con nombres de clase distintos cada vez. Eso es lo que permitió que el bug de `04-diagnostico/analisis-prompt-producer.md` (C3: `.soporte-card { overflow: hidden }` + `grid-template-columns: repeat(3, 1fr)` sin `minmax`) apareciera sin que nadie lo detectara -- no hay control de versiones sobre un CSS que se reinventa cada vez.

Esta skill fija ese CSS. Verificado contra el output real de esta campaña (`03-outputs/v15-fragmentos/ag-s2-cal.html` y `ag-s2-carga.html`, re-extraídos limpios el 2026-09-03): las clases y valores de aquí son los que el Planner YA usa en la práctica -- esto no es un diseño nuevo, es el mismo sistema con los dos bugs conocidos corregidos y con responsive añadido (ninguno de los dos ficheros lo tenía: `tiene_media_query_pantalla: false` en el manifest).

**No define colores propios.** Los valores hex son los mismos que ya están en `02-planner.md` líneas 296-313 (rotación de 12 tonos por territorio) y 435-449 (paleta global). Si esta skill y el prompt alguna vez discrepan en un valor de color, gana el prompt y hay que avisar -- esta skill es la capa de implementación, no la fuente de la decisión de marca.

## Cómo usarla

1. Copia el bloque de CSS que corresponda (base + el específico del one-pager) tal cual, sin reescribir selectores ni inventar nombres de clase nuevos para un componente que ya existe aquí.
2. Sustituye `{{SCOPE}}` por el prefijo de aislamiento de ESE fichero concreto (el mismo patrón que ya usa el Planner: `ag-s2-cal` para `calendario_canales_global_v<N>.html`, `ag-s2-carga` para `carga_soporte_global_v<N>.html`, y el equivalente para cada uno de los otros 6 one-pagers -- un prefijo único por fichero, nunca reutilizado entre ficheros distintos).
3. Si necesitas un componente visual que no está aquí, constrúyelo siguiendo la prosa de `02-planner.md` como hasta ahora, pero si se repite en más de un one-pager, añádelo a esta skill en la siguiente iteración en vez de reinventarlo cada vez -- registra un flag `{"tipo": "componente_no_catalogado", "severidad": "baja", "componente": "<nombre>"}`.

---

## 1. Base compartida (los 8 one-pagers)

Idéntica en todos los one-pagers verificados -- header, subtítulo, leyenda, badges de stream, chips de medio, pie de página.

```css
{{SCOPE}} * { box-sizing: border-box; }
{{SCOPE}} { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; margin: 0; padding: 32px 40px; background: #FFFFFF; color: #262423; }
{{SCOPE}} h1 { color: #0066FF; font-size: 26px; margin: 0 0 4px 0; }
{{SCOPE}} .subtitle { color: #6F7176; font-size: 14px; margin: 0 0 20px 0; }
{{SCOPE}} .legend { display: flex; gap: 40px; margin-bottom: 24px; flex-wrap: wrap; }
{{SCOPE}} .legend-item { display: flex; align-items: center; gap: 10px; }
{{SCOPE}} .legend-icon { width: 34px; height: 34px; border-radius: 50%; background: #F5F7FA; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
{{SCOPE}} .legend-text b { display: block; font-size: 13px; color: #262423; }
{{SCOPE}} .legend-text .legend-label { font-size: 12px; color: #6F7176; }
{{SCOPE}} .stream-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; color: #FFFFFF; margin-right: 6px; }
{{SCOPE}} .chip { display: inline-block; background: #F5F7FA; border-radius: 4px; padding: 2px 8px; font-size: 11px; color: #262423; margin: 2px 4px 0 0; }
{{SCOPE}} .foot { margin-top: 28px; padding-top: 14px; border-top: 1px solid #EEEEEE; font-size: 12px; color: #6F7176; display: flex; justify-content: space-between; align-items: center; }
{{SCOPE}} .footnote { font-size: 12px; color: #6F7176; margin-top: 18px; }
```

**Corrección respecto al output verificado (C4 del diagnóstico -- rótulo de la pastilla de stream en gris sobre fondo saturado):**

La regla de la v0.1.0 era `{{SCOPE}} .legend-text span { color: #6F7176 }`, un selector genérico "cualquier `span` dentro de `.legend-text`". Como la pastilla de stream es un `<span class="stream-badge">` que vive **dentro** de ese contenedor, ese selector la alcanzaba sin querer:

| Selector | Especificidad con el prefijo de scope | Resultado |
|---|---|---|
| `{{SCOPE}} .legend-text span` | 3 clases + 1 elemento | Gana |
| `{{SCOPE}} .stream-badge` | 3 clases | Pierde |

El `color: #FFFFFF` declarado en `.stream-badge` nunca llegaba a aplicarse y el rótulo salía en `rgb(111,113,118)` sobre azul, morado o verde. Verificado con `getComputedStyle` en Chromium sobre el deck ejecutivo de octubre (2026-09-14), no por inspección visual.

**La corrección es dar clase propia al texto secundario en vez de apuntar al tipo de elemento.** Nada de `!important`: el problema era el selector, no el peso.

**Regla general que se deriva de esto y que aplica a toda la skill:** dentro de un contenedor que pueda alojar una pastilla, un badge o cualquier elemento con fondo de color, **nunca se declara color sobre un tipo de elemento** (`span`, `div`, `b`). El color va siempre sobre una clase propia. Un selector de tipo alcanza descendientes que no estabas mirando y gana por especificidad al selector de clase del componente.

**Marcado HTML de la leyenda** (explícito, porque la clase nueva lo hace obligatorio):

```html
<div class="legend-item">
  <div class="legend-icon"><!-- icono --></div>
  <div class="legend-text">
    <b><span class="stream-badge" style="background:#0066FF;">Growth</span></b>
    <span class="legend-label">12 territorios</span>
  </div>
</div>
```

**Lo que NO se resuelve aquí.** El contraste del blanco sobre algunos fondos de pastilla sigue siendo bajo aunque el color ya se aplique: blanco sobre `#00C48C` da 2,3:1 y sobre `#8B5CF6` da 3,9:1, por debajo del 4,5:1 exigible. La corrección es oscurecer esos fondos dentro del mismo tono, pero **los colores de stream viven solo en `02-planner.md`** y esta skill no crea una segunda fuente de verdad sobre ellos. Queda registrado aquí como dato para que se decida allí.

### Responsive (nuevo -- ninguno de los one-pagers verificados lo traía)

Breakpoints alineados con la sección Layout del Maia Storyteller (`05-storyteller.md`, líneas 296-300: 1024 / 768 / 480), para que el one-pager ya sea responsive en origen y el Storyteller no tenga que parchearlo al integrar.

```css
@media (max-width: 1024px) {
  {{SCOPE}} .table-scroll { overflow-x: auto; }
}
@media (max-width: 768px) {
  {{SCOPE}} { padding: 20px; }
  {{SCOPE}} .legend { gap: 20px; }
}
@media (max-width: 480px) {
  {{SCOPE}} .hero-grid,
  {{SCOPE}} .soportes-grid,
  {{SCOPE}} .metrics-row { grid-template-columns: 1fr; }
}
@media print {
  {{SCOPE}} { padding: 10px 16px; }
}
```

---

## 2. Calendario Gantt (`calendario_<subcorriente>_v<N>.html`, `calendario_canales_global_v<N>.html`)

Implementa `02-planner.md` líneas 276-341 (estructura del Gantt, rotación de 12 tonos, 6 reglas críticas de rendering).

```css
{{SCOPE}} .table-scroll { overflow-x: auto; }
{{SCOPE}} table.maintable { border-collapse: collapse; width: 100%; min-width: 900px; table-layout: fixed; }
{{SCOPE}} table.maintable td,
{{SCOPE}} table.maintable th { border-bottom: 1px solid #EEEEEE; padding: 8px 10px; vertical-align: middle; overflow-wrap: anywhere; }
{{SCOPE}} table.gantt td:first-child { width: 34%; border-right: 1px solid #EEEEEE; }
{{SCOPE}} table.matrix th { background: #F5F7FA; font-size: 12px; padding: 8px; }
```

**Corrección respecto al output verificado (C1 del diagnóstico -- barras solapadas con el cabecero de fila):** el `table-layout: fixed` se mantiene (es necesario para que las columnas de semana midan lo mismo entre filas -- si se cambia a `auto` se rompe la lectura de Gantt), pero ahora:
- la tabla vive dentro de `.table-scroll` (`overflow-x: auto`) con un `min-width: 900px` explícito, así que en pantallas estrechas hace scroll horizontal en vez de comprimir las columnas hasta que el texto se pisa;
- las celdas llevan `overflow-wrap: anywhere`, así que un texto de barra largo ("Samsung Fold&Flip: precompra + compra (prioridad #1)") envuelve dentro de su celda en vez de invadir la fila de al lado.

**Marcado HTML** (igual que el output verificado, solo añade el wrapper `.table-scroll`):

```html
<div class="table-scroll">
<table class="maintable gantt">
  <thead><tr><th>Territorio</th><!-- 1 th por semana --></tr></thead>
  <tbody>
    <tr><td colspan="10" style="background:#F5F7FA; padding:10px 14px; font-weight:700; font-size:12px;"><span class="stream-badge" style="background:#0066FF;">Growth</span></td></tr>
    <tr>
      <td><!-- icono + nombre territorio + descripción --></td>
      <td colspan="N" style="padding:6px 4px;">
        <div style="background:#0066FF; opacity:1; border-radius:6px; padding:8px 10px; color:#FFFFFF; font-size:12px; font-weight:600; text-align:center;">Texto de la barra</div>
        <div style="margin-top:4px;"><span class="chip">Email</span><span class="chip">Tienda</span></div>
      </td>
      <td colspan="M"></td>
    </tr>
  </tbody>
</table>
</div>
```

Rotación de color por territorio (12 tonos) y color por stream en el calendario global: usar los valores ya definidos en `02-planner.md` líneas 296-313 y 337 -- esta skill no los repite para no tener dos fuentes de verdad sobre el mismo dato.

---

## 3. Carga por soporte (`carga_soporte_global_v<N>.html`)

Implementa `02-planner.md` líneas 402-431.

```css
{{SCOPE}} .card { background: #FFFFFF; border: 1px solid #EEEEEE; border-radius: 8px; padding: 20px; }
{{SCOPE}} .hero-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 16px; }
{{SCOPE}} .hero-stat { background: #F5F7FA; border-radius: 8px; padding: 14px; text-align: center; overflow-wrap: anywhere; }
{{SCOPE}} .hero-stat .v { font-size: 22px; font-weight: 800; color: #0066FF; overflow-wrap: anywhere; }
{{SCOPE}} .hero-stat .l { font-size: 11px; color: #6F7176; margin-top: 4px; }
{{SCOPE}} .soportes-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 24px; }
{{SCOPE}} .soporte-card { border: 1px solid #EEEEEE; border-radius: 8px; overflow: visible; }
{{SCOPE}} .soporte-head { background: #0066FF; color: #FFFFFF; padding: 12px 16px; font-weight: 700; font-size: 13px; border-radius: 8px 8px 0 0; overflow-wrap: anywhere; }
{{SCOPE}} .soporte-short { padding: 10px 16px 0 16px; font-weight: 700; color: #262423; font-size: 15px; }
{{SCOPE}} .metrics-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; padding: 12px 16px; }
{{SCOPE}} .metric-box { background: #F5F7FA; border-radius: 6px; padding: 8px; text-align: center; overflow-wrap: anywhere; }
{{SCOPE}} .metric-box .mv { font-weight: 700; font-size: 14px; color: #262423; overflow-wrap: anywhere; }
{{SCOPE}} .metric-box .ml { font-size: 10px; color: #6F7176; }
{{SCOPE}} .badges-row { padding: 0 16px 12px 16px; display: flex; gap: 6px; flex-wrap: wrap; }
{{SCOPE}} .soporte-desc { padding: 0 16px 16px 16px; font-size: 12px; color: #6F7176; }
```

**Corrección respecto al output verificado (C3 del diagnóstico -- texto cortado a zoom 100%):**

| Antes (output real, v1) | Ahora | Por qué |
|---|---|---|
| `grid-template-columns: repeat(4, 1fr)` en `.hero-grid` | `repeat(4, minmax(0, 1fr))` | `1fr` a secas es `minmax(auto, 1fr)`: la columna no encoge por debajo del contenido. Con `minmax(0, 1fr)` sí puede encoger y el texto envuelve en vez de desbordar. |
| `grid-template-columns: repeat(3, 1fr)` en `.metrics-row` | `repeat(3, minmax(0, 1fr))` | Mismo motivo -- esta era la línea exacta del bug C3 en `03-outputs/v15-fragmentos/ag-s2-carga.html`. |
| `.soporte-card { overflow: hidden }` | `overflow: visible`, con el `border-radius` movido a `.soporte-head` (`8px 8px 0 0`) | El `overflow: hidden` de la tarjeta solo hacía falta para que la cabecera azul respetara la esquina redondeada. Puesto el radio directamente en la cabecera, no hace falta recortar el resto de la tarjeta -- y así el texto ya no se corta si por lo que sea no encoge del todo. |
| Sin `overflow-wrap` en `.hero-stat`, `.metric-box` | `overflow-wrap: anywhere` en los nodos de texto/valor | Red de seguridad adicional: aunque el grid ya no desborde, un valor inesperadamente largo (ej. "Media-alta" en una columna estrecha) envuelve en vez de recortarse. |

**Marcado HTML** (igual que el output verificado):

```html
<div class="card">
  <div style="display:flex; gap:24px; flex-wrap:wrap;">
    <div style="flex:2; min-width:280px;"><!-- lectura rápida + claves operativas --></div>
    <div style="flex:3; min-width:320px;">
      <div class="hero-grid">
        <div class="hero-stat"><div class="v">37</div><div class="l">Total activaciones soporte</div></div>
        <!-- 3 hero-stat más -->
      </div>
    </div>
  </div>
</div>

<div class="soportes-grid">
  <div class="soporte-card">
    <div class="soporte-head">BTL / EMAIL / CRM</div>
    <div class="soporte-short">BTL/CRM</div>
    <div class="metrics-row">
      <div class="metric-box"><div class="mv">9-12</div><div class="ml">Campañas</div></div>
      <!-- 2 metric-box más -->
    </div>
    <div class="badges-row"><span class="stream-badge" style="background:#00C48C;">Dispositivos 5</span></div>
    <div class="soporte-desc">Territorios: ...</div>
  </div>
  <!-- 3 soporte-card más -->
</div>
```

---

## 4. Qué falta aquí (deliberadamente, para no inventar)

- **Brief Canales por sub-corriente** (`brief_canales_territorio_<subcorriente>_v<N>.html`): no verificado contra ningún output real todavía -- no tengo un fixture de este fichero. La prosa de `02-planner.md` líneas 342-386 sigue siendo la única referencia hasta que se verifique un output real y se añada aquí.
- **Colores por territorio y por stream**: intencionadamente no repetidos aquí -- viven solo en `02-planner.md` para no crear una segunda fuente de verdad.
- **Contraste de los fondos de pastilla de stream**: diagnosticado aquí (sección 1, corrección C4) pero no corregido aquí. Los valores hex son decisión de `02-planner.md`.
- Activada como `status: active`. El Maia Planner la carga con fallback graceful (si no esta disponible, usa la prosa de `02-planner.md` como antes).

---

## 5. Historial

| Version | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-09-03 | Version inicial. Base compartida, Gantt y carga por soporte. Corrige C1 y C3 |
| 0.2.0 | 2026-09-15 | Corrige C4: el selector `.legend-text span` alcanzaba la pastilla de stream y le ganaba por especificidad, dejando el rotulo en gris sobre fondo saturado. Se sustituye por `.legend-text .legend-label` y se documenta la regla general de no declarar color sobre tipos de elemento. Se deja registrado el contraste insuficiente de dos fondos de stream, cuya correccion corresponde a `02-planner.md` |
