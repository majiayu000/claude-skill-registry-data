---
name: agent-browser
description: "Workflow para testear cambios frontend con agent-browser CLI, validar rutas, contenido UI y regresiones visuales basicas. USE FOR: smoke tests de paginas, checks de navegacion, validacion de textos clave, evidencia rapida en localhost y troubleshooting de ejecucion del browser."
---

# Agent Browser Research

## Objetivo
Testear cambios frontend con evidencia reproducible desde CLI para verificar UI/UX esperada y detectar regresiones funcionales tempranas.

## Cuándo usar
- Validar paginas y navegacion despues de cambios UI.
- Ejecutar smoke tests rapidos en localhost.
- Confirmar textos/elementos clave sin montar un framework E2E completo.
- Reproducir errores visuales basicos y capturar evidencia.

## Prerrequisitos
1. App corriendo localmente (por ejemplo en http://localhost:3000).
2. agent-browser instalado y con browser listo.

Comandos base:

```bash
agent-browser --help
agent-browser install
```

## Workflow recomendado
1. Preparar entorno de browser:

```bash
agent-browser install
```

2. Verificar pagina inicial:

```bash
agent-browser open http://localhost:3000
agent-browser eval "document.body.innerText.includes('Ir al dashboard')"
```

3. Verificar rutas criticas del dashboard:

```bash
agent-browser open http://localhost:3000/dashboard/analysis
agent-browser eval "document.body.innerText.includes('Analysis') && document.body.innerText.includes('Resumen')"

agent-browser open http://localhost:3000/dashboard/launch-registry
agent-browser eval "document.body.innerText.includes('Launch registry') && document.body.innerText.includes('Cordillera One')"

agent-browser open http://localhost:3000/simulate
agent-browser eval "document.body.innerText.includes('Parametros') && document.body.innerText.includes('Stream')"
```

4. (Opcional) Capturar evidencia visual:

```bash
agent-browser screenshot ./artifacts/landing.png
agent-browser open http://localhost:3000/dashboard/analysis
agent-browser screenshot ./artifacts/analysis.png
```

## Criterios de aprobado (smoke)
- Landing carga y el CTA principal existe.
- Analysis muestra titulo y resumen.
- Launch registry muestra titulo y al menos un registro mock esperado.
- /simulate mantiene compatibilidad funcional con la vista Mission.

## Troubleshooting

### Error: Chrome exited early / missing shared libraries
Sintoma comun en Linux:
- `error while loading shared libraries: libnspr4.so`

Solucion:

```bash
agent-browser install --with-deps
```

Luego reintentar:

```bash
agent-browser open http://localhost:3000
```

### Si una ejecucion parece colgada
Usar timeout para diagnostico rapido:

```bash
timeout 15s agent-browser open http://localhost:3000
```

## Salida esperada
- Checks `agent-browser eval` retornan `true` para cada asercion definida.
- Evidencia opcional en screenshots para revision visual.

