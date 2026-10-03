---
name: scaffold-unit-tests
description: Scaffold unit test classes cho tất cả handlers của một entity (Create, Update, Delete, Restore, GetList, GetById)
argument-hint: [ServiceName EntityName]
allowed-tools: Write, Read, Bash, Edit
---

# Scaffold Unit Tests `$ARGUMENTS`

Usage: `/scaffold-unit-tests ServiceName EntityName`

## Bước 0 — Tạo test project (nếu chưa có)

```bash
# Tạo xUnit test project
dotnet new xunit -n {Service}.UnitTests -o services/{Service}/tests/{Service}.UnitTests
dotnet sln add services/{Service}/tests/{Service}.UnitTests/{Service}.UnitTests.csproj

# Thêm reference tới Application project
dotnet add services/{Service}/tests/{Service}.UnitTests/{Service}.UnitTests.csproj \
  reference services/{Service}/src/{Service}.Application/{Service}.Application.csproj

# Cài packages bắt buộc
cd services/{Service}/tests/{Service}.UnitTests
dotnet add package Moq
dotnet add package FluentAssertions
dotnet add package MockQueryable.Moq
dotnet add package xunit.runner.visualstudio
```

> **Tại sao cần MockQueryable.Moq?** `GetAllAsync()` trả `IQueryable<T>` không thể mock trực tiếp bằng Moq vì `IQueryable` cần provider để chạy `.Where()`, `.ToListAsync()`. Package này cung cấp `.BuildMock()` để tạo in-memory queryable hợp lệ.

**Yêu cầu:** Test project phải tồn tại với packages: xUnit, Moq, FluentAssertions, MockQueryable.Moq

## Bước 1 — Đọc handlers thực tế

Trước khi viết tests, đọc TẤT CẢ handler files của entity để biết:
- Dependencies được inject
- Business logic và error cases
- External services được gọi

## Bước 2 — Tạo test files

### Command Test: `tests/{Service}.UnitTests/Handlers/Commands/{Entity}CreateCommandHandlerTests.cs`

```csharp
using FluentAssertions;
using MockQueryable.Moq;
using Moq;
using Xunit;
using {Service}.Application.Commands.{Entity}Create;
using {Service}.Application.Interfaces;
using {Service}.Domain.Entities;

namespace {Service}.UnitTests.Handlers.Commands;

public class {Entity}CreateCommandHandlerTests
{
    private readonly Mock<IServiceUnitOfWork> _uowMock;
    private readonly Mock<IGenericRepository<{Entity}>> _repoMock;
    private readonly {Entity}CreateCommandHandler _handler;

    public {Entity}CreateCommandHandlerTests()
    {
        _uowMock = new Mock<IServiceUnitOfWork>();
        _repoMock = new Mock<IGenericRepository<{Entity}>>();
        _uowMock.Setup(u => u.{Entity}s).Returns(_repoMock.Object);
        _uowMock.Setup(u => u.BeginTransactionAsync()).Returns(Task.CompletedTask);
        _uowMock.Setup(u => u.CommitTransactionAsync()).Returns(Task.CompletedTask);
        _uowMock.Setup(u => u.RollbackTransactionAsync()).Returns(Task.CompletedTask);
        _handler = new {Entity}CreateCommandHandler(_uowMock.Object);
    }

    [Fact]
    public async Task Handle_ValidInput_ReturnsSuccess()
    {
        _repoMock.Setup(r => r.AnyAsync(It.IsAny<Expression<Func<{Entity}, bool>>>()))
            .ReturnsAsync(false);

        var result = await _handler.Handle(
            new {Entity}CreateCommand { Name = "Test" }, CancellationToken.None);

        result.IsSuccess.Should().BeTrue();
        result.Data.Should().NotBeNull();
        _repoMock.Verify(r => r.AddAsync(It.IsAny<{Entity}>()), Times.Once);
        _uowMock.Verify(u => u.CommitTransactionAsync(), Times.Once);
    }

    [Fact]
    public async Task Handle_DuplicateName_ReturnsFailure()
    {
        _repoMock.Setup(r => r.AnyAsync(It.IsAny<Expression<Func<{Entity}, bool>>>()))
            .ReturnsAsync(true);

        var result = await _handler.Handle(
            new {Entity}CreateCommand { Name = "Existing" }, CancellationToken.None);

        result.IsSuccess.Should().BeFalse();
        _repoMock.Verify(r => r.AddAsync(It.IsAny<{Entity}>()), Times.Never);
    }

    [Fact]
    public async Task Handle_DbError_RollsBackTransaction()
    {
        _repoMock.Setup(r => r.AnyAsync(It.IsAny<Expression<Func<{Entity}, bool>>>()))
            .ReturnsAsync(false);
        _uowMock.Setup(u => u.CommitTransactionAsync())
            .ThrowsAsync(new Exception("DB error"));

        var result = await _handler.Handle(
            new {Entity}CreateCommand { Name = "Test" }, CancellationToken.None);

        result.IsSuccess.Should().BeFalse();
        _uowMock.Verify(u => u.RollbackTransactionAsync(), Times.Once);
    }
}
```

### Query Test: `tests/{Service}.UnitTests/Handlers/Queries/{Entity}GetListQueryHandlerTests.cs`

```csharp
public class {Entity}GetListQueryHandlerTests
{
    private readonly Mock<IServiceUnitOfWork> _uowMock;
    private readonly Mock<IGenericRepository<{Entity}>> _repoMock;
    private readonly {Entity}GetListQueryHandler _handler;

    public {Entity}GetListQueryHandlerTests()
    {
        _uowMock = new Mock<IServiceUnitOfWork>();
        _repoMock = new Mock<IGenericRepository<{Entity}>>();
        _uowMock.Setup(u => u.{Entity}s).Returns(_repoMock.Object);
        _handler = new {Entity}GetListQueryHandler(_uowMock.Object);
    }

    [Fact]
    public async Task Handle_ReturnsPagedResults()
    {
        var data = Enumerable.Range(1, 15).Select(i => new {Entity}
        {
            Id = Guid.NewGuid(), Name = $"Item {i}", IsDeleted = false, CreatedAt = DateTime.UtcNow
        }).ToList();

        // ⚠️ Dùng MockQueryable.Moq cho IQueryable
        _repoMock.Setup(r => r.GetAllAsync()).Returns(data.AsQueryable().BuildMock());

        var result = await _handler.Handle(
            new {Entity}GetListQuery { PageNumber = 1, PageSize = 10, IsDeleted = false },
            CancellationToken.None);

        result.IsSuccess.Should().BeTrue();
        result.Data!.Items.Should().HaveCount(10);
        result.Data.TotalItems.Should().Be(15);
        result.Data.HasNextPage.Should().BeTrue();
    }

    [Fact]
    public async Task Handle_ExcludesDeleted()
    {
        var data = new List<{Entity}>
        {
            new() { Id = Guid.NewGuid(), Name = "Active", IsDeleted = false },
            new() { Id = Guid.NewGuid(), Name = "Deleted", IsDeleted = true },
        };
        _repoMock.Setup(r => r.GetAllAsync()).Returns(data.AsQueryable().BuildMock());

        var result = await _handler.Handle(
            new {Entity}GetListQuery { IsDeleted = false }, CancellationToken.None);

        result.Data!.TotalItems.Should().Be(1);
    }
}
```

### Validation Test: `tests/{Service}.UnitTests/Validators/{Entity}CreateCommandValidationTests.cs`

```csharp
public class {Entity}CreateCommandValidationTests
{
    [Fact]
    public async Task Validate_ValidInput_ReturnsSuccess()
    {
        var cmd = new {Entity}CreateCommand { Name = "Valid Name" };
        var result = await cmd.ValidateAsync();
        result.IsSuccess.Should().BeTrue();
        result.ListErrors.Should().BeEmpty();
    }

    [Theory]
    [InlineData("")]
    [InlineData(null)]
    public async Task Validate_EmptyName_ReturnsError(string? name)
    {
        var cmd = new {Entity}CreateCommand { Name = name! };
        var result = await cmd.ValidateAsync();
        result.IsSuccess.Should().BeFalse();
        result.ListErrors.Should().Contain(e => e.Field == "Name");
    }
}
```

## Bước 3 — Run tests

```bash
cd services/{Service}/tests/{Service}.UnitTests
dotnet test --verbosity normal
```

## Rules
- Đọc ACTUAL handler code trước khi viết tests
- Mock TẤT CẢ dependencies qua constructor injection
- Dùng `MockQueryable.Moq` (`.BuildMock()`) cho `GetAllAsync()` IQueryable
- Test: happy path, validation fail, not found, deleted, DB error, rollback
- Naming: `MethodName_Scenario_ExpectedBehavior`
- Verify: `mock.Verify(x => x.Method(), Times.Once/Never)`
