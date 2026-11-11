---
name: migraciones
description: Cómo hacer migraciones en las APIs de la plantilla base (EF Core + SQL Server) — migraciones de esquema, migraciones de datos con SQL idempotente en lugar de HasData, el Down obligatorio con borrado lógico, no editar migraciones aplicadas, sembrar un dato para todas las organizaciones o registros existentes, probar Up y Down, y correr SQL a mano con sqlcmd. Usar al crear o cambiar una entidad, al sembrar o corregir datos, al agregar un catálogo, una política o un permiso, o al diagnosticar una migración que falla.
---

# Migraciones

Dos tipos, y nunca mezclados en la misma migración salvo que el dato dependa del esquema nuevo:

| Tipo | Cómo se genera | Contenido |
|---|---|---|
| **Esquema** (tabla, columna, índice, FK) | `dotnet ef migrations add <Nombre>` sobre el cambio de la entidad y su configuración | Lo que genera EF, revisado a mano |
| **Datos** (catálogos, permisos, políticas, correcciones) | `dotnet ef migrations add <Nombre>` sin cambios de modelo | Solo `migrationBuilder.Sql(...)` idempotente |

Nombre en PascalCase que diga qué hace: `AddCustomerTaxId`, `SeedInvoiceStatuses`,
`FixDuplicatedCodes`.

## Reglas

- **Nunca editar una migración ya aplicada** en algún ambiente (ni la inicial). Lo que falte va en
  una migración nueva.
- **Los datos no van con `HasData`.** Los Ids explícitos de `HasData` chocan con filas creadas a mano
  en producción que el snapshot del modelo no conoce. Los datos van con SQL idempotente y dejan que
  la identidad asigne el Id.
- **Todo `Up` es re-ejecutable**: `IF NOT EXISTS ... INSERT`, `UPDATE ... WHERE` acotado, y
  reactivación de lo que esté borrado lógicamente (`IsDeleted = 1`) en lugar de insertarlo de nuevo.
- **Todo `Down` revierte lo que hizo el `Up`**, en orden inverso y con **borrado lógico**
  (`IsActive = 0, IsDeleted = 1`), nunca `DELETE`. Tiene que poder correrse dos veces sin error
  (filtrar por `IsDeleted = 0`). Lo que la migración no creó no se toca. Un `Down` vacío solo se
  acepta en correcciones de datos que no tienen vuelta atrás, y se explica en un comentario.
- **Un comentario `<summary>` en la clase** dice qué hace, por qué y cómo se revierte.
- `decimal` siempre con precisión explícita en la configuración (`HasPrecision(18, 4)` o la que
  corresponda). Cambiar la precisión de una columna con datos es una migración de esquema que hay que
  revisar: puede truncar.
- Nada de datos de prueba en las migraciones. Los datos de desarrollo van en `Scripts/`.

## Dato que existe por organización (o por cualquier "dueño")

Si el dato debe existir para cada organización, cliente o empresa (una política, una configuración),
la migración lo inserta para **todas** las que ya existen. Si el código que lo lee no cae a un valor
por defecto, una organización sin la fila rompe en producción.

```sql
INSERT INTO [Esquema].[Tabla] ([Code], [OrganizationCode], [Value], [IsActive], [CreatedAt], [CreatedBy], [IsDeleted])
SELECT N'NUEVO_CODIGO', o.[OrganizationCode], N'valor', 1, GETDATE(), 0, 0
FROM (SELECT DISTINCT [OrganizationCode] FROM [Esquema].[Tabla]) o
WHERE NOT EXISTS (
    SELECT 1 FROM [Esquema].[Tabla] t
    WHERE t.[Code] = N'NUEVO_CODIGO' AND t.[OrganizationCode] = o.[OrganizationCode]);
```

Un índice único sobre la clave natural (`Code`, `OrganizationCode`) hace el insert seguro de repetir.

Y quien cree una organización nueva tiene que crearle también ese dato: revisar el caso de uso de
alta.

## Corrección de datos

- Primero un `SELECT` que muestre exactamente qué filas cambian y cuántas. Se le muestra al usuario
  antes de escribir el `UPDATE`.
- El `UPDATE` con el mismo `WHERE` que el `SELECT`, más una condición que lo vuelva idempotente (que
  no vuelva a cambiar lo ya corregido).
- Si la corrección es de una sola vez y no debe viajar a otros ambientes, va como script en
  `docs/` o `Scripts/` con su nombre (`fix-<tema>.sql`), no como migración.

## Probar antes de entregar

```powershell
dotnet ef migrations script <Anterior> <Nueva>      # revisar el SQL que se va a correr
dotnet ef database update <Nueva>                   # Up
dotnet ef database update <Anterior>                # Down
dotnet ef database update <Nueva>                   # Up otra vez: debe reactivar sin chocar con índices únicos
```

Contra una base compartida, preguntar antes de aplicar: otros pueden estar usándola.

## Correr SQL a mano (`sqlcmd`)

- Usar `-I` (o `SET QUOTED_IDENTIFIER ON;` al inicio). Sin eso, un `INSERT`/`UPDATE`/`DELETE`
  sobre una tabla con índices filtrados o columnas calculadas falla con el error 1934.
- Las consultas de solo lectura se pueden correr sin pedir permiso. Las que escriben, se le muestran
  al usuario y se corren solo con su aprobación.
- Nunca escribir la cadena de conexión ni la contraseña en documentos, commits ni respuestas.

## Documentación

En `CHANGELOG.md`, sección `[Unreleased]` → `### Base de datos`: el nombre de cada migración y qué
hace. Desplegar la API nunca es solo copiar binarios: quien despliega tiene que saber qué migraciones
arrastra.
