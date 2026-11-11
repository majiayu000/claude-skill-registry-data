---
name: arquitectura
description: Convenciones de arquitectura de las APIs .NET de la plantilla base — capas, dónde va cada archivo, patrón Interactor/Validator/InputPort, validators genéricos, reglas puras, servicios, repositorios genéricos, transacciones, registro en el contenedor de dependencias, errores y códigos HTTP, listados paginados y búsqueda, procesos en segundo plano. Usar al crear un caso de uso o endpoint nuevo, al agregar un servicio, entidad o regla, al decidir en qué carpeta va un archivo, o al responder cómo está estructurado el proyecto.
---

# Arquitectura

Proyecto único con Clean Architecture **por convención de carpetas** (no hay ensamblados que
impidan cruzar capas, así que la disciplina es de quien escribe). El patrón es **vertical slice
sobre Interactor / InputPort**: cada endpoint es una carpeta con su caso de uso completo.

## Regla de oro

```
Controller → Interactor → Validator → InputPort → Service / Rules → Repository → EF
```

- **Los controllers no orquestan.** Resuelven el Interactor con `[FromServices]` y devuelven
  `BaseResponse<T>`. Lo único permitido sobre el input es pasar ruta o query al DTO
  (`input.Id = id;`). Un `if`, una elección entre dos casos de uso o una transformación van en un
  caso de uso, aunque sea glue code.
- **Los Services devuelven entidades, no DTOs.** El mapeo a `OutputDTO` se hace en el InputPort.
- **Las Rules son estáticas y puras.** Las usan tanto el Validator como el InputPort.

## Crear un caso de uso

### 1. Carpeta

```
Business/UseCases/<Área>/[<Subárea>/]<Nombre>/
```

`<Nombre>` en imperativo e inglés (`CreateEmployee`, `GetEmployeeById`, `ApproveRequest`). **Todos
los archivos llevan el nombre como prefijo.**

### 2. Archivos

```csharp
// <Nombre>InputDTO.cs — omitir si no recibe nada (usar EmptyInputDTO<TOut>)
public class XInputDTO : IInputDTO, IRequest<XOutputDTO> { }

// <Nombre>OutputDTO.cs — los DTOs hijos van en ESTE MISMO archivo
public class XOutputDTO : IOutputDTO { }

// <Nombre>Validator.cs — solo si hay algo que validar (ver "Validators")
public class XValidator : IRequestValidator<XInputDTO, XOutputDTO>
{
    public async Task<List<string>> ValidateAsync(XInputDTO input, CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        // 1. Campos básicos, sin base de datos.
        if (errors.Count > 0) return errors;   // cortar antes de consultar
        // 2. Reglas que consultan la base.
        return errors;
    }
}

// <Nombre>InputPort.cs — interfaz e implementación EN EL MISMO ARCHIVO
public interface IXInputPort : IInputPort<XInputDTO, XOutputDTO> { }

public class XInputPort : IXInputPort
{
    public async Task<XOutputDTO> ExecuteAsync(XInputDTO input, CancellationToken cancellationToken = default) { }
}

// <Nombre>Interactor.cs
public class XInteractor : Interactor<XInputDTO, XOutputDTO>
{
    public XInteractor(IRequestValidator<XInputDTO, XOutputDTO> validator, IXInputPort inputPort)
        : base(validator, inputPort) { }

    public static IServiceCollection AddDependency(IServiceCollection services)
    {
        services.AddScoped<IRequestValidator<XInputDTO, XOutputDTO>, XValidator>();
        services.AddScoped<IXInputPort, XInputPort>();
        services.AddScoped<XInteractor>();
        return services;
    }
}
```

| Situación | Dónde |
|---|---|
| Helper que usa solo este caso de uso | En su carpeta |
| DTO compartido entre casos de uso del área | `<Área>/Shared/` |
| Sub-caso de uso (simulación, vista previa) | Anidado: `<Nombre>/Preview<Nombre>/` |
| Listado paginado | Ver "Listados y búsqueda" |

### 3. Registrar

Una línea en `Business/UseCases/UseCasesDependencyInjection.cs`:

```csharp
XInteractor.AddDependency(services);
```

### 4. Endpoint

Antes de escribir el `[HasPermission]`, **consultar al usuario qué permiso lleva** (skill
`permisos`). Al terminar, escribir los tests del Validator y del InputPort (skill
`pruebas-endpoint`). El hook `.claude/hooks/endpoint-nuevo.js` lo recuerda.

```csharp
[HasPermission(Permissions.<Pantalla>.<Operación>)]
[HttpPost("ruta")]
public async Task<ActionResult<BaseResponse<XOutputDTO>>> Accion(
    [FromBody] XInputDTO input,
    [FromServices] XInteractor interactor,
    CancellationToken cancellationToken)
{
    var output = await interactor.HandleAsync(input, cancellationToken);
    return Ok(BaseResponse<XOutputDTO>.Ok(output));
}
```

Si un endpoint tiene dos modos (por ejemplo `dryRun`), **un solo caso de uso** decide internamente.
Dos casos de uso elegidos desde el controller terminan con la misma regla escrita dos veces.

## Validators: propio o genérico

En `Business/Contracts/` hay tres genéricos con sus DTOs:

| Genérico | DTO | Cuándo |
|---|---|---|
| `EmptyRequestValidator<TIn,TOut>` | `EmptyInputDTO<TOut>` | No hay nada sintáctico que validar |
| `ByIdValidator<TIn,TOut>` | `ByIdInputDTO<TOut>` | Solo verificar `Id > 0` |
| `ByCodeValidator<TIn,TOut>` | `ByCodeInputDTO<TOut>` | Solo verificar `Code` no vacío |

```csharp
services.AddScoped<
    IRequestValidator<EmptyInputDTO<XOutputDTO>, XOutputDTO>,
    EmptyRequestValidator<EmptyInputDTO<XOutputDTO>, XOutputDTO>>();
```

**Escribir un validator propio** en cuanto se cumpla cualquiera de estas condiciones:

1. hay más de un campo que validar;
2. hay reglas de formato, rango o multiplicidad;
3. hay que **consultar la base** (existencia, duplicados, solapes, límites disponibles);
4. hay **autorización por recurso** (¿este usuario puede actuar sobre este registro?).

- **Validator** = "¿es admisible?". Devuelve una `List<string>` acumulada, con mensajes en
  español, frases completas y dirigidos al usuario final. Cada mensaje dice qué está mal y, si se
  puede, cómo corregirlo ("La cantidad supera el máximo permitido: el máximo es 30.").
- **InputPort** = ejecuta asumiendo que es admisible. Lo que no se pudo saber antes se informa con
  `BusinessException(ErrorCodes.X, "...")`.
- Que ambos repitan la carga de una entidad es normal y deliberado: así el Validator da un mensaje
  preciso.
- Si el Validator necesita el mismo cálculo que hará el InputPort (por ejemplo, un máximo
  permitido), usar **el mismo método o regla**, nunca una copia: el número que informa el error
  debe ser exactamente el que la ejecución aceptaría.

## Dónde va la lógica nueva

```
¿Cálculo puro, sin base de datos?       → Business/Rules/<Área>/ (clase estática, sin DI, con tests)
¿Consulta o persistencia reutilizable?  → Business/Services/<Área>/ (método en un Service NUEVO)
¿Secuencia de pasos de ESTE endpoint?   → el InputPort
¿Texto de cara al usuario repetido?     → una clase estática de mensajes en Rules (un solo lugar)
```

- **Los Services existentes no se modifican** para una funcionalidad nueva: ni refactorizar, ni
  extraer métodos, ni agregar métodos a su interfaz. Ya los usan endpoints en producción, y
  cambiarlos arriesga romper el front aunque el contrato HTTP no cambie. Se crea un Service nuevo con
  su interfaz, aunque duplique lógica. Leer métodos existentes está bien. Si reutilizar exige cambiar
  algo existente, preguntar antes.
- **Repositories**: solo los tres genéricos (`IBaseRepository<T>`, `IReadonlyRepository<T>`,
  `IUnitOfWork`). **Nunca crear un repositorio por entidad.** `Query()` ya trae el filtro de
  borrado lógico; `QueryUnfiltered()` lo omite.
- **Services**: reciben `IBaseRepository<TEntity>` + `IUnitOfWork`, componen consultas de EF y
  persisten.
- **Transacciones**: el InputPort arma el grafo completo y se lo pasa al Service en **una sola
  llamada** (`CreateAsync(entity, children, ct)`). Nunca varios `SaveChangesAsync` desde el
  InputPort: si el segundo falla, el primero queda guardado a medias.

## Efectos secundarios (correo, avisos, bitácora)

- Van **después de persistir**: nunca se avisa de algo que todavía puede fallar.
- **Nunca propagan.** Un correo que falla no revierte ni hace fallar la operación ya guardada: se
  envuelve en un método `TrySend…Async` con try/catch y log.
- Las operaciones sensibles (cargas masivas, borrados, cambios de permisos) dejan registro en la
  bitácora de auditoría si el proyecto tiene una, con quién, cuándo y el detalle de lo que falló.

## Errores y códigos HTTP

`ExceptionMiddleware` traduce las excepciones; **no hay try/catch en Controllers ni Interactors**.

| Situación | Excepción | HTTP |
|---|---|---|
| Validación fallida | (la lanza el Interactor) `BusinessException(ErrorCodes.ValidationError)` | 400 |
| Regla de negocio en el InputPort | `BusinessException(ErrorCodes.X, msg)` | 400 |
| No existe | `NotFoundException` | 404 |
| Autenticado y con permiso, pero no sobre ESTE recurso | `ForbiddenException(ErrorCodes.X, msg)` | 403 |
| Sin sesión o token inválido | lo resuelve la autenticación | 401 |

**Nunca 401 por falta de permiso**: el front cierra la sesión ante un 401. Si el proyecto no trae
`ForbiddenException`, agregarla en `Common/Exceptions/` (con `Code` y `Message`, igual que
`BusinessException`) y mapearla a 403 en `ExceptionMiddleware`, tanto en el status como en el
código de error.

Los códigos de error son constantes en `Common/Errors/ErrorCodes.cs`, en `UPPER_SNAKE`
(`EMPLOYEE_ACCESS_DENIED`). El front decide por el código, nunca por el texto.

## Listados y búsqueda

- Los listados se paginan en SQL (`Skip`/`Take` en la consulta, nunca en memoria). Si el proyecto
  tiene `FindExpression` + `PaginatedOutputDTO`, el InputDTO recibe `FindExpression Filter` y el
  OutputDTO hereda `PaginatedOutputDTO`. El tamaño de página tiene tope (por ejemplo, 100).
- Búsqueda por texto libre:
  - escapar los comodines de `LIKE` (`%`, `_`, `[`) antes de armar el patrón;
  - buscar **por palabra**: AND entre palabras y OR entre columnas, para que "juan perez" encuentre
    nombre y apellido aunque estén en columnas distintas;
  - poner tope al largo del texto (por ejemplo, 100 caracteres) y a la cantidad de palabras (por
    ejemplo, 5), validados en el Validator antes de consultar.
- Los filtros de alcance (organización, equipo, lo que el usuario puede ver) se aplican **siempre**
  en la consulta, no después de traer los datos.

## Procesos en segundo plano

- `BackgroundService` con sus `Options` (`Enabled`, hora de corrida). `Enabled = false` en
  `appsettings.Development.json` para no correr contra bases compartidas.
- **Idempotentes por datos**: antes de procesar, revisar si ya se hizo (por ejemplo, si el mes ya
  tiene su movimiento). Así una corrida repetida o atrasada no duplica nada y se pone al día sola.
- Una transacción por elemento; un fallo se registra y **no aborta** el resto de la corrida.
- Además del worker, un endpoint de administración para correrlo a mano, que devuelva el resumen de
  la corrida.

## Registro en el contenedor: tres lugares

| Qué | Dónde |
|---|---|
| Servicios, DbContext, repositorios, seguridad, `Configure<TOptions>`, `AddHostedService` | `Extensions/DependencyInjection.cs` |
| Una línea por caso de uso | `Business/UseCases/UseCasesDependencyInjection.cs` |
| Validator + InputPort + Interactor (solo esos tres) | El `AddDependency` estático del Interactor |

- **Un servicio nuevo va SIEMPRE en `DependencyInjection.cs`**, nunca dentro de un `AddDependency`.
- Registrar siempre por interfaz: `services.AddScoped<IXService, XService>();`.
- Todo `Scoped` por defecto. `Singleton` solo para lo que no tiene estado por request.

## Entidad nueva

1. `AppDomain/Entities/<Área>/XEntity.cs`: hereda `AuditableEntity` (auditoría automática + borrado
   lógico) o `BaseEntity` para catálogos inmutables.
2. `Persistence/ExtraConfiguration/<Área>/XConfiguration.cs` con `IEntityTypeConfiguration<XEntity>`.
   Se descubre sola con `ApplyConfigurationsFromAssembly`. Declarar el esquema:
   `builder.ToTable("Tabla", "Esquema")`. Precisión explícita en todo `decimal`.
3. `DbSet<XEntity>` en `Persistence/Context/AppDbContext.cs`.
4. Migración (skill `migraciones`).

Al guardar, `AuditableEntityInterceptor` (`Persistence/Interceptors/`) llena `CreatedAt`, `CreatedBy`,
`UpdatedAt` y `UpdatedBy`, y convierte un `Delete` en borrado lógico: no asignarlos a mano. Para
reactivar algo borrado (en lugar de insertarlo y chocar con un índice único), leerlo con
`QueryUnfiltered()`.

## Convenciones transversales

- **Idioma:** comentarios de código nuevos, mensajes al usuario y documentación, en español. Nombres
  de clases, métodos y propiedades, en inglés.
- Todo método asíncrono recibe y propaga `CancellationToken`, y se llama `…Async`.
- **Booleanos con prefijo `Is` / `Has` / `Can`** (`IsActive`, `HasPendingRequest`, `CanEdit`).
- **Las bajas no son `DELETE`**: dar de baja un registro con historia (un colaborador, un usuario)
  es un `PATCH` que lo desactiva. `DELETE` queda para catálogos y borrados de administración.
- **Fecha y hora:** en código nuevo, inyectar `TimeProvider` (registrado como
  `services.AddSingleton(TimeProvider.System)`) en lugar de `DateTime.Now`. Así los tests pueden
  fijar "hoy" con `FakeTimeProvider` (paquete `Microsoft.Extensions.TimeProvider.Testing`).
- Comentar el **porqué**, no el qué: la regla de negocio, el caso que motivó una validación, la
  trampa que evita. Un comentario que repite el código sobra.
- Formato: `.editorconfig` en la raíz (UTF-8, CRLF, 4 espacios en C#).

## Skills relacionadas

| Tarea | Skill |
|---|---|
| Permiso de un endpoint, pantalla u operación nueva; alcance por recurso; diagnosticar un 403 | `permisos` |
| Tests de Validators, InputPorts y Rules | `pruebas-endpoint` |
| Migraciones de esquema y de datos | `migraciones` |
| Documentar un cambio para el front y versionarlo | `contrato-api` |
