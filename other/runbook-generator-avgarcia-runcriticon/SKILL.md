---
name: runbook-generator
description: Genera un runbook operativo en docs/runbooks/ siguiendo la plantilla del proyecto y cruzando con el ADR que lo invoca. Usar cuando se alcance un disparador que requiera un runbook nuevo (rotación de secreto, acceso a RDS, respuesta a brecha, disaster recovery, atención de un derecho RGPD, alarma de AMG, actualización de JDK). Crea el archivo con frecuencia, prerrequisitos, procedimiento paso a paso, rollback y registro.
---

# Runbook Generator — Runcriticon

Genera un runbook operativo coherente con la convención de [`docs/runbooks/README.md`](../../../docs/runbooks/README.md) y la plantilla de rotación de [`docs/arquitectura/configuracion-y-secretos-en-modulos.md`](../../../docs/arquitectura/configuracion-y-secretos-en-modulos.md) §9.

## Cuándo usar

El catálogo de `docs/runbooks/README.md` enumera ~14 runbooks previstos por los ADRs. Esta skill se invoca cuando llega el momento de crear uno:

| Runbook | Invocado por | Disparador |
|---|---|---|
| `acceso-rds.md` | ADR-0006 D13 | Primer acceso administrativo a RDS |
| `rotacion-{secreto}.md` | ADR-0013 D10/D11 | Primera rotación (trimestral DB / anual crypto) o sospecha |
| `respuesta-a-brecha.md` | ADR-0014 D26 | Antes de la beta |
| `disaster-recovery.md` | ADR-0006 D29 | Antes de la beta |
| `derechos-rgpd-acceso.md` / `-oposicion.md` | ADR-0014 D12/D15 | Antes de la beta |
| `alarmas/{alarma}.md` | ADR-0011 D16 | Al configurar cada alarma en AMG |
| `actualizacion-jdk.md` | ADR-0016 D5 | Primer upgrade de GraalVM CE |

## Argumentos

```
/runbook-generator rotacion-session-signing-key
/runbook-generator acceso-rds
/runbook-generator respuesta-a-brecha
```

## Proceso

1. **Identificar el ADR que invoca el runbook** (de la tabla del catálogo o preguntando).
2. **Leer la sub-decisión origen** para extraer frecuencia, plazos, garantías.
3. **Elegir la plantilla** según el tipo:
   - **Rotación de secreto** → plantilla de `configuracion-y-secretos-en-modulos.md` §9.
   - **Procedimiento operativo** (acceso, DR, brecha) → plantilla genérica de abajo.
4. **Rellenar** con los datos concretos del ADR (cifras, comandos AWS CLI, cruces).
5. **Crear** `docs/runbooks/{nombre}.md`.
6. **No commitear** automáticamente.

## Plantilla genérica (procedimiento operativo)

```markdown
# Runbook — {título}

> Invocado por {ADR-XXXX DN}. {Una frase de propósito.}

## Cuándo se ejecuta

- {Disparador concreto, con cifra si aplica.}

## Quién puede ejecutarlo

- {Rol / persona. Para acciones sobre producción: requiere MFA, cruce ADR-0006 D27.}

## Prerrequisitos

- [ ] {Acceso AWS CLI con MFA / ventana de mantenimiento / equipo notificado / etc.}

## Procedimiento

1. **{Paso}**:
   ```bash
   {comando concreto}
   ```
2. **{Paso}**: ...

## Verificación

- [ ] {Cómo comprobar que salió bien.}

## Rollback

- {Cómo deshacer si el paso falla.}

## Registro

- Anotar la ejecución en `docs/runbooks/log-{tipo}.md`: fecha, ejecutor, resultado.

## Cruces

- {ADR-XXXX DN}, {subdocumento.md §N}.
```

## Plantilla de rotación de secreto

Usar la de [`configuracion-y-secretos-en-modulos.md`](../../../docs/arquitectura/configuracion-y-secretos-en-modulos.md) §9, que ya incluye:

- Frecuencia (trimestral DB / anual crypto y proveedor — ADR-0013 D10).
- Generación del nuevo valor (`openssl rand -hex 32` para crypto; dashboard del proveedor para tokens).
- Persistencia en SSM (`aws ssm put-parameter --name /runcriticon/{env}/{component}/{name} --value ... --type SecureString --overwrite`).
- Redeploy de App Runner (`aws apprunner start-deployment`).
- Verificación del flujo afectado.
- Consecuencias (ej. rotar `session-signing-key` invalida sesiones activas — ADR-0003 D11).
- Registro en `docs/runbooks/log-rotaciones.md`.

## Reglas

- **Comandos concretos**, no genéricos. Si el runbook menciona SSM, el comando lleva el path canónico real.
- **Cruce inline** al ADR origen en cada paso relevante.
- **Rollback siempre presente**, aunque sea "no aplica" con justificación.
- **Registro siempre presente**: ningún procedimiento operativo se ejecuta "en silencio" (coherente con el principio de responsabilidad proactiva de ADR-0014).
- Si el runbook es de rotación y el secreto **no está en el catálogo** (ADR-0013 D6), avisar de que falta añadirlo primero.

## Antipatrones

- Comandos con valores reales de secretos (usar placeholders `$NUEVO_VALOR`).
- Runbook sin sección de verificación.
- Rotación sin mencionar el efecto colateral (invalidación de sesiones, cuota del proveedor, etc.).
