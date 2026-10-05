---
name: express5
description: Patrones de Express 5 y TypeScript. Usa cuando trabajes con rutas, middleware, o cualquier codigo del backend API.
---

# Express 5 - Patrones Modernos

Cuando escribas codigo backend para PROSEGUIT, usa exclusivamente APIs de Express 5:

## Cambios clave en Express 5
- **Async error handling nativo**: Los errores en funciones async se capturan automaticamente (no necesitas try/catch ni next(err) en cada handler)
- **`req.query` retorna `URLSearchParams`** (no objeto plano)
- **Path route matching** usa `path-to-regexp` v8 (sintaxis ligeramente diferente)
- **`res.render()` es async**
- **Removido**: `app.del()`, `req.param()`, `req.host` plural, `res.json(status, obj)`

## Patron de rutas PROSEGUIT
```typescript
import { Router } from 'express';

const router = Router();

// Express 5: async handlers atrapan errores automaticamente
router.get('/equipment', async (req, res) => {
  const data = await equipmentService.findAll(req.query);
  res.json(data);
});

// Express 5: nuevo path matching - usar {param} en vez de :param para regex
router.get('/equipment/:id', async (req, res) => {
  const equipo = await equipmentService.findById(req.params.id);
  res.json(equipo);
});

export default router;
```

## Middleware pattern
```typescript
import { Request, Response, NextFunction } from 'express';

// Express 5: middleware async tambien captura errores
const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    res.status(401).json({ error: 'No autorizado' });
    return;
  }
  // verificar token...
  next();
};
```

## Error handler global
```typescript
// Express 5: error handler sigue siendo 4 parametros
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Error interno del servidor' });
});
```

## Patrones a EVITAR
- NO envolver handlers async en try/catch generico -> Express 5 lo hace solo
- NO usar `req.param()` -> usar `req.params.nombre`
- NO usar `res.json(status, data)` -> usar `res.status(status).json(data)`
