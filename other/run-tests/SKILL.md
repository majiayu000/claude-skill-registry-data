---
name: run-tests
description: Correr tests del backend y frontend de PROSEGUIT. Usa despues de hacer cambios de codigo para verificar que todo funciona.
allowed-tools: Bash(npm test *), Bash(npx vitest *)
argument-hint: "[backend|frontend|all|archivo-especifico]"
---

# Run Tests - PROSEGUIT

Ejecuta los tests del proyecto.

## Sin argumentos o "all": todos los tests
```bash
cd backend && npm test && cd ../frontend && npm test
```

## Argumento "backend": solo backend
```bash
cd backend && npm test
```

## Argumento "frontend": solo frontend
```bash
cd frontend && npm test
```

## Archivo especifico
```bash
npx vitest run $ARGUMENTS
```

## Tests con watch mode (desarrollo)
```bash
cd backend && npm test -- --watch
# o
cd frontend && npm test -- --watch
```

## Tests con coverage
```bash
cd backend && npm test -- --coverage
cd frontend && npm test -- --coverage
```

## Cuando un test falla
1. Leer el mensaje de error completo
2. Identificar el archivo y linea del fallo
3. Verificar si el test esta desactualizado o si hay un bug real
4. Correr solo ese test: `npx vitest run path/to/test.ts`
5. Fixear y re-correr
