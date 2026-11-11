---
name: pruebas-endpoint
description: Cómo escribir los tests de las APIs de la plantilla base — tests unitarios con xunit + Moq del Validator y del InputPort de cada caso de uso, y de las Rules puras; dónde van, qué casos cubrir (corte sin BD, alcance por recurso, existencia, BusinessException, persistencia en una sola llamada), cómo fijar la fecha y cómo crear el proyecto de tests si no existe. Usar SIEMPRE después de crear un endpoint o caso de uso nuevo, al cambiar las reglas de un Validator, InputPort o Rule, o cuando se pidan tests.
---

# Tests (Validator, InputPort y Rules)

Todo endpoint nuevo sale con tests de **su Validator y su InputPort**, y toda Rule nueva con los
suyos. Todo caso de uso que se modifique sale con tests de lo que cambió: así la cobertura crece sin
un esfuerzo aparte.

El controller y el Interactor no se prueban: el controller no tiene lógica (skill `arquitectura`) y
el Interactor es la clase base `Interactor<,>`, igual para todos.

## Si el proyecto de tests no existe

```powershell
dotnet new xunit -n <Proyecto>.Tests -f net10.0
dotnet add <Proyecto>.Tests package Moq
dotnet add <Proyecto>.Tests reference <Proyecto>/<Proyecto>.csproj
dotnet sln <Solución>.slnx add <Proyecto>.Tests/<Proyecto>.Tests.csproj
```

En el `.csproj` de tests: `<Nullable>enable</Nullable>`, `<ImplicitUsings>enable</ImplicitUsings>` y
`<Using Include="Xunit" />`. Si un test necesita miembros `internal`, agregar
`<InternalsVisibleTo Include="<Proyecto>.Tests" />` en el proyecto principal.

## Dónde y cómo se llaman

```
<Proyecto>.Tests/UseCases/<Área>/[<Subárea>/]<Nombre>/
    <Nombre>ValidatorTests.cs
    <Nombre>InputPortTests.cs
<Proyecto>.Tests/Rules/<Área>/<Regla>Tests.cs
```

- Misma ruta que el código bajo `Business/`. El namespace la sigue:
  `<Proyecto>.Tests.UseCases.<Área>...<Nombre>`.
- Métodos en **español con guiones bajos**, describiendo la regla y no el método:
  `Sin_id_corta_sin_consultar_la_base`, `Cantidad_mayor_al_maximo_se_rechaza_con_el_maximo`.
- Un `<summary>` corto en la clase que diga qué cubre.
- Varias entradas inválidas equivalentes → `[Theory]` + `[InlineData]`.
- Si el test nace de un caso real (un bug, un dato de producción), un comentario de una línea con el
  caso.

## Armado

```csharp
public class XValidatorTests
{
    private readonly Mock<IXService> _xService = new();
    private readonly Mock<IXAccessService> _accessService = new();

    private XValidator CreateValidator() => new(_xService.Object, _accessService.Object);
}
```

- Se mockean **las interfaces que recibe el constructor**: Services, servicios de acceso,
  `ICurrentUserService`, etc.
- **Las Rules no se mockean**: son estáticas y puras, se ejecutan de verdad y tienen sus propios
  tests.
- **Sin base de datos ni `DbContext`.** Si el caso de uso recibe `IBaseRepository<T>` directamente,
  mockear `Query()` con `new List<T>{...}.AsQueryable()`. Si el código usa métodos async de EF
  (`ToListAsync`), eso ya es un test de integración: avisar al usuario.
- Mocks sueltos (`MockBehavior.Default`): devuelven `default` en lo no configurado. Configurar solo
  lo que el caso necesita. Ojo: un método que devuelve un objeto queda en `null` si no se configura;
  si el código lo usa en el camino feliz, configurarlo en el constructor del test.
- Para devolver algo que depende de los argumentos:

  ```csharp
  _service.Setup(s => s.PlanAsync(It.IsAny<int>(), It.IsAny<decimal>(), It.IsAny<CancellationToken>()))
      .ReturnsAsync((int _, decimal requested, CancellationToken _) => new Plan(requested));
  ```

## Fecha y hora

- Nada de `DateTime.Now` en los asserts.
- Si el código recibe `TimeProvider`, usar `FakeTimeProvider` (paquete
  `Microsoft.Extensions.TimeProvider.Testing`) y fijar la fecha:
  `new FakeTimeProvider(new DateTimeOffset(2026, 11, 3, 0, 0, 0, TimeSpan.Zero))`.
- Si el código todavía lee `DateTime.Now`, usar fechas que no dependan de hoy: claramente pasadas
  para lo válido y claramente futuras (por ejemplo, el año 2999) para "no puede ser futura". Anotar
  la deuda: ese código debería recibir `TimeProvider`.

## Validator: qué cubrir

Un test por **cada mensaje de error** del Validator, más estos:

| Caso | Assert |
|---|---|
| Campos básicos inválidos | El mensaje exacto (`Assert.Equal(["…"], errors)`) **y** `VerifyNoOtherCalls()` en los mocks de BD: el Validator corta antes de consultar |
| Sin alcance sobre el recurso | El mock lanza `ForbiddenException` → `Assert.ThrowsAsync<ForbiddenException>`, y que **no** siguió consultando |
| Alcance pedido | `Verify(EnsureCanAccessAsync(id, <parámetros exactos>, ...), Times.Once)`. Es contrato de seguridad: un cambio accidental tiene que romper el test |
| Entidad inexistente, duplicada o en conflicto | El mensaje exacto |
| Una regla anterior falla | Las consultas o cálculos posteriores **no** se ejecutan (`Times.Never`) |
| Límite exacto (igual al máximo, igual a la fecha mínima) | Cuál de los dos lados es válido. Los bordes son donde viven los bugs |
| Entrada válida | `Assert.Empty(errors)` |

Con `EmptyRequestValidator`, `ByIdValidator` o `ByCodeValidator` **no** se escribe
`ValidatorTests`: las reglas viven en el InputPort y se prueban ahí.

## InputPort: qué cubrir

| Caso | Assert |
|---|---|
| Cada `throw new BusinessException(...)` | `Assert.ThrowsAsync<BusinessException>` + `Assert.Equal(ErrorCodes.X, ex.Code)` + que **no** persistió (`Times.Never`) |
| Camino feliz: persistencia | El Service se llama **una vez** (`Times.Once`) con el grafo armado; `It.Is<T>(e => …)` para los campos que calcula el InputPort |
| Camino feliz: salida | El mapeo entidad → `OutputDTO` de lo que calcula el InputPort (no hace falta repetir lo que solo se copia) |
| Procesos por fila (importaciones, lotes) | Una fila con error no se persiste y las demás sí; los contadores del resumen |
| Efectos secundarios (correo, aviso) | Si el envío falla (`ThrowsAsync` en el mock), la operación igual termina bien |

Para revisar el objeto que se pasó al Service, capturarlo:

```csharp
XEntity? saved = null;
_xService.Setup(s => s.CreateAsync(It.IsAny<XEntity>(), It.IsAny<CancellationToken>()))
    .Callback<XEntity, CancellationToken>((e, _) => saved = e)
    .ReturnsAsync((XEntity e, CancellationToken _) => e);
```

## Rules: qué cubrir

Son funciones puras: entrada → salida, sin mocks. Cubrir el caso normal, cada rama, los bordes
(cero, negativo, máximo exacto, fin de mes, año bisiesto si hay fechas) y el redondeo si hay
decimales. Un `[Theory]` con una tabla de casos suele ser lo más legible.

## Correr

```powershell
dotnet test <Proyecto>.Tests/<Proyecto>.Tests.csproj --filter "FullyQualifiedName~UseCases.<Área>.<Nombre>"
dotnet test   # la suite completa, antes de dar el cambio por terminado
```

Reportar el resultado tal cual: cuántos pasaron y la salida de los que fallaron.

## Trampas

- **Un test que pasa sin haber pasado por el mock no prueba nada.** En cada caso negativo,
  verificar que el flujo cortó (`Times.Never` / `VerifyNoOtherCalls`), no solo el mensaje.
- **El 403 de alcance no es un error de validación**: el servicio de acceso lanza
  `ForbiddenException`, no agrega a la lista de errores.
- **Los mensajes se comparan exactos**, porque son texto de cara al usuario. Si cambia un mensaje en
  el código, cambia en el test.
- Asignaciones que solo evitan que EF reinserte navegaciones (`entity.Parent = null!`) no se
  testean: son detalle de persistencia.
