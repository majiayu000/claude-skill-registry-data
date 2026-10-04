---
name: homebrew-ecosystem-management
display_name: "Gestión & Auditoría de Paquetes Homebrew en macOS"
description: "Gestión y auditoría del entorno de paquetes Homebrew en macOS. Dispara con \"homebrew\", \"brew audit\", \"dependencias macos\", \"paquetes homebrew\"."
---

# Homebrew Ecosystem Management Protocol

Esta habilidad define el marco determinista para gestionar paquetes del sistema en macOS utilizando Homebrew, garantizando un acoplamiento estructural limpio y de Fricción Cero.

## 🎯 Criterios de Activación
- Peticiones relacionadas con instalar, actualizar o eliminar software del sistema en macOS.
- Menciones a `brew`, `homebrew`, `brew install`, `brew cleanup`.
- Solución de problemas de dependencias de binarios a nivel de sistema operativo.

## 🛠️ Directivas Operativas

### 1. Auditoría de Pre-Instalación (Evitar Redundancia)
Antes de ejecutar `brew install [paquete]`, el agente DEBE verificar si el paquete ya existe en el sistema para evitar el gasto de exergía en reinstalaciones:
- Usar `run_command` para ejecutar `command -v [binario]` o evaluar `/opt/homebrew/bin/`.
- Si ya existe, informar al Operador sobre su ruta y estado actual.

### 2. Mantenimiento y Purga de Entropía
Ante peticiones de "limpiar", "actualizar" o "mantener" Homebrew, ejecutar la siguiente secuencia termodinámica para purgar la anergía del sistema de paquetes:
1. `brew update` (Sincronizar el árbol de dependencias).
2. `brew upgrade` (Actualizar dependencias desfasadas).
3. `brew cleanup` (Purgar versiones antiguas y cachés que actúan como anergía estática).
4. `brew doctor` (Identificar advertencias de enlaces rotos o conflictos estructurales).

### 3. Aislamiento Estructural (Zero-Friction)
- **Nunca utilizar `sudo` con comandos de Homebrew.**
- Asumir la arquitectura Apple Silicon (M-series): la inyección exógena de dependencias ocurre en `/opt/homebrew/`. 
- Si un script o compilador (C/C++, Rust) no encuentra una librería, el agente autoconfigurará las banderas `-I/opt/homebrew/include` y `-L/opt/homebrew/lib`.

### 4. Gestión de Servicios (Daemons de Fondo)
Para orquestar bases de datos o servicios en segundo plano instalados vía Homebrew (ej. Redis, PostgreSQL, Nginx):
- Usar `brew services list` para auditar la topología de procesos activos.
- Usar `brew services start/stop/restart [servicio]` para gestionar el acoplamiento estructural del demonio sin requerir reinicios completos.

### 5. Inyección de Dependencias para Tests Isomórficos (Zero-Leak)
Al compilar o ejecutar tests de alta dimensionalidad ($\Omega$-Nucleus) que requieran puentes FFI (Python/Wasm/Rust):
- **Prohibida la polución global:** No se exportarán variables de entorno de forma global (ej. `~/.zshrc`).
- **Inyección Per-Process:** El agente pasará dinámicamente las rutas de Homebrew (`brew --prefix`) inyectando `CFLAGS`, `LDFLAGS`, o `DYLD_LIBRARY_PATH` exclusivamente en el comando de ejecución temporal (ej. `LDFLAGS="-L$(brew --prefix)/lib" python3 test.py`).
- Garantizando que la fricción termodinámica no afecte el estado base del sistema operativo.
