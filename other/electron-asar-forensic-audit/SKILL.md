---
name: electron-asar-forensic-audit
description: Auditoría forense y extracción binaria in-memory de archivos Electron app.asar y binarios nativos auxiliares sin dependencias. Dispara con "auditar app electron", "extraer asar", "asar python", "descompilar electron", "forense electron app", "ingeniería inversa", "ingeniería inversa electron".
---

# Protocolo de Auditoría Forense Electron (In-Memory ASAR Parser)

## 1. Principio de Operación
Cuando se audita un bundle de Electron (`.app/Contents/Resources/app.asar`), **NO utilices `npx @electron/asar`**. 
Utiliza el ejecutable de Python in-memory para leer la estructura binaria de cabecera de 16 bytes:
- **Bytes 0-3**: Magic Header (`uint32`)
- **Bytes 4-7**: Offset Size (`uint32`)
- **Bytes 8-11**: Total Header Size (`uint32`)
- **Bytes 12-15**: JSON Header Length (`uint32`)
- **Resto**: Estructura JSON indexada con `offset` y `size` de cada archivo.

---

## 2. Snippet de Inspección In-Memory (Zero-Dependency)

```python
import struct, json, re

def scan_asar(asar_path):
    with open(asar_path, 'rb') as f:
        data = f.read(16)
        u1, u2, header_size, json_size = struct.unpack('<IIII', data)
        header = json.loads(f.read(json_size).decode('utf-8'))
        header_offset = 16 + json_size

        def find_files(node, path=''):
            res = []
            if 'files' in node:
                for k, v in node['files'].items():
                    res.extend(find_files(v, f'{path}/{k}' if path else k))
            else:
                res.append((path, node.get('size'), node.get('offset')))
            return res

        files, offset_base = find_files(header), header_offset
        return files, offset_base, f
```

---

## 3. Extracción de Métodos gRPC, Endpoints y Modelos
Aplica expresiones regulares sobre los buffers leídos directamente de `f.seek(header_offset + offset)` sin escribir artefactos temporales en disco para evitar restricciones del sandbox local.

```python
# Ejemplo: Extraer endpoints gRPC de aiserver.v1
rpcs = re.findall(r'aiserver\.v1\.([A-Za-z0-9]+Service)/([A-Za-z0-9]+)', content)

# Ejemplo: Extraer identificadores de modelos LLM
models = re.findall(r'\"(grok[^\"]*|claude[^\"]*|gpt-4[^\"]*)\"', content)
```

---

## 4. Auditoría de Seguridad e Identidad del Bundle
1. Extraer firmas con `codesign -dvvv '/Applications/AppName.app'`.
2. Verificar notarización de Apple con `spctl -a -t exec -vvv '/Applications/AppName.app'`.
3. Inspeccionar permisos y ATS en `Info.plist` (`NSAllowsArbitraryLoads`).
4. Extraer entitlements del binario ejecutable y sus auxiliares (`Grok Bot Helper.app`).

---

## 5. Extracción Semántica Profunda (Telemetría, Headers y Feature Flags)
Para comprender la identidad de red, capacidades de experimentación (A/B testing) y seguimiento de telemetría (como los eventos `cloud_agent` o `computer_use`), aplica los siguientes patrones al contenido decodificado in-memory:

```python
# Feature Flags (Statsig)
gates = re.findall(r'checkGate\s*\(\s*[\'\"]([^\'\"]+)[\'\"]', content)
configs = re.findall(r'getConfig\s*\(\s*[\'\"]([^\'\"]+)[\'\"]', content)

# Custom HTTP Headers (Identidad de red y autenticación oculta)
headers = re.findall(r'[\'\"](x-[a-zA-Z0-9-]+)[\'\"]\s*:', content)

# Telemetría de Eventos Operacionales
events = re.findall(r'trackEvent\s*\(\s*[\'\"]([^\'\"]+)[\'\"]', content)
events += re.findall(r'logEvent\s*\(\s*[\'\"]([^\'\"]+)[\'\"]', content)
```

---

## 6. Correlación con Binarios Nativos Auxiliares (`Contents/Resources/bin/`)
Las aplicaciones agénticas en Electron suelen delegar la computación intensiva, LSP y el razonamiento a daemons nativos compilados:
1. **Inspección de binarios acompañantes:**
   `ls -la Contents/Resources/bin/` (buscar ejecutables como `language_server`, `bridge`, `encoder`).
2. **Identificación estática del compilador y runtime (Zero-Execution):**
   ```bash
   strings Contents/Resources/bin/<binary> | grep -E "(rustc|go.buildid|libc\+\+)" | head -n 5
   ```
3. **Detección de argumentos de arranque y puertos loopback:**
   Buscar llamadas `spawn` en los scripts de Electron descompilados in-memory para identificar puertos locales, tokens de sesión y endpoints de inferencia:
   ```python
   # Buscar llamadas spawn y argumentos in-memory
   spawns = re.findall(r'spawn\s*\(\s*[^,]+,\s*(\[[^\]]+\])', content)
   ```

---

## 7. Detección de Protocolos RPC y Bridges en Loopback
Para identificar si la aplicación desacopla el renderer de un daemon backend mediante IPC estructurado:
* **Dependencias de Red Loopback:** Inspeccionar presencia de `@connectrpc/connect-node`, `@connectrpc/connect` o `@bufbuild/protobuf` en `package.json`.
* **Esquemas Protobuf Compilados:** Extraer archivos en `dist/proto/*_pb.js` in-memory para mapear contratos de servicio RPC, esquemas de request/response y orígenes de código fuente en monorepos corporativos (ej. `google3: cs/...`).
