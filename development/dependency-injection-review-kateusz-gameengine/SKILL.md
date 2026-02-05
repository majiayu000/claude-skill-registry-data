---
name: dependency-injection-review
description: Review code for proper DI patterns using DryIoc. Ensures no static singletons, validates constructor injection and service lifetimes. Use when reviewing code, refactoring static access, or debugging DI issues.
---

# Dependency Injection Review

## Table of Contents
- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Reference](#quick-reference)
- [Core Principles](#core-principles)
- [Review Checklist](#review-checklist)
  - [1. Constructor Injection Pattern](#1-constructor-injection-pattern)
  - [2. Service Registration](#2-service-registration)
  - [3. Interface-Based Design](#3-interface-based-design)
  - [4. Circular Dependency Detection](#4-circular-dependency-detection)
  - [5. Null Reference Validation](#5-null-reference-validation)
- [Registration Patterns](#registration-patterns)
- [Step-by-Step DI Review Workflow](#step-by-step-di-review-workflow)
- [Debugging DI Issues](#debugging-di-issues)

## Overview
This skill audits code for adherence to the game engine's dependency injection architecture using DryIoc. It ensures all services use constructor injection, identifies static singleton violations, and validates service registration patterns.

## When to Use
Invoke this skill when:
- Reviewing new code for DI compliance
- Refactoring static singletons to use DI
- Debugging service resolution errors
- Adding new services to the container
- Questions about service lifetime and registration
- Investigating circular dependency issues

## Quick Reference

## ✅ **Do**
* Primary constructors for all classes with dependencies
* Register services in `Program.cs`
* Use events for decoupling
* Interface-based design
* Use **Singleton** for stateful services

## ❌ **Don't**
* Static singletons
* Manual `new()` for services
* Null validation in constructors (non-nullable types handle this)
* Circular dependencies
* Concrete dependencies everywhere
* Use **Transient** for managers/factories
---
## Core Principles

### The Golden Rule
**NEVER create static singletons!** All singleton instances must be registered in the DI container.

### Exceptions
The ONLY acceptable static classes are pure constant classes:
- `EditorUIConstants` - UI sizing and styling constants
- `RenderingConstants` - Rendering configuration constants

Everything else uses dependency injection.

## Review Checklist

### 1. Constructor Injection Pattern

All dependencies must be injected through the primary constructor.

**✅ CORRECT (Use Primary Constructor)**:
```csharp
public class AnimationSystem(
    ITextureFactory textureFactory,
    IResourceManager resourceManager) : ISystem
{
    // Dependencies are automatically available as private readonly fields
    // Use textureFactory and resourceManager directly in methods
}
```

**❌ FORBIDDEN - Static Singleton**:
```csharp
public class AnimationSystem
{
    private static AnimationSystem? _instance;
    public static AnimationSystem Instance => _instance ??= new AnimationSystem();

    private AnimationSystem() { } // Private constructor
}
```

**❌ FORBIDDEN - Property Injection**:
```csharp
public class AnimationSystem
{
    public ITextureFactory TextureFactory { get; set; } // Don't use property injection!

    public AnimationSystem() { }
}
```

**❌ FORBIDDEN - Service Locator Pattern**:
```csharp
public class AnimationSystem
{
    private readonly ITextureFactory _textureFactory;

    public AnimationSystem()
    {
        // Don't resolve from container directly!
        _textureFactory = ServiceLocator.Resolve<ITextureFactory>();
    }
}
```

### 2. Service Registration

**Location**: `Editor/Program.cs` or `Runtime/Program.cs`

**Service Lifetime Guidelines**:
- **Singleton** (default): SceneManager, TextureFactory, ConsolePanel, RenderingSystem, ProjectManager
- **Transient**: ValidationService, TemporaryOperationContext, per-request processors
- **Scoped**: Not used in this engine (no HTTP request scope)

**Example: Editor/Program.cs Registration**:
```csharp
// Core managers (Singleton)
container.Register<ISceneManager, SceneManager>(Reuse.Singleton);
container.Register<IProjectManager, ProjectManager>(Reuse.Singleton);
container.Register<ISelectionManager, SelectionManager>(Reuse.Singleton);

// Factories (Singleton)
container.Register<ITextureFactory, TextureFactory>(Reuse.Singleton);
container.Register<IShaderFactory, ShaderFactory>(Reuse.Singleton);

// Panels (Singleton)
container.Register<ContentBrowserPanel>(Reuse.Singleton);
container.Register<ConsolePanel>(Reuse.Singleton);
container.Register<PropertiesPanel>(Reuse.Singleton);

// Systems (Singleton)
container.Register<RenderingSystem>(Reuse.Singleton);
container.Register<AnimationSystem>(Reuse.Singleton);

// Transient services
container.Register<IValidationService, ValidationService>(Reuse.Transient);
```

### 3. Interface-Based Design

Use interfaces for services that need abstraction, testability, or multiple implementations.

**✅ USE INTERFACES FOR**:
```csharp
// Managers - multiple implementations or testability
public interface ISceneManager
{
    Scene? ActiveScene { get; }
    void LoadScene(string path);
}

public class SceneManager(IDependency dep) : ISceneManager { }

// Factories - abstraction from creation logic
public interface ITextureFactory
{
    Texture2D CreateTexture(string path);
}

public class TextureFactory(ICache cache) : ITextureFactory { }

// Cross-cutting concerns - different implementations per platform
public interface IRendererAPI
{
    void DrawIndexed(uint indexCount);
}

public class OpenGLRendererAPI(IContext context) : IRendererAPI { }
```

**✅ SKIP INTERFACES FOR**:
```csharp
// Editor panels - concrete UI implementations
public class ConsolePanel(ILogger logger) { }

// ECS Systems - concrete game logic
public class AnimationSystem(ITextureFactory factory) : ISystem { }

// Pure data classes - no behavior to abstract
public class Transform
{
    public Vector3 Position { get; set; }
    public Vector3 Rotation { get; set; }
}

// Component Editors - concrete UI for specific components
public class TransformComponentEditor(IFieldEditor<Vector3> vector3Editor) { }
```

**Decision Guide**:
1. Will this have multiple implementations? → Use interface
2. Do you need to mock it for testing? → Use interface
3. Does it cross module boundaries? → Use interface
4. Is it just UI or concrete game logic? → Skip interface (register concrete class)

### 4. Circular Dependency Detection

**❌ FORBIDDEN**:
```csharp
// Service A depends on Service B
public class ServiceA
{
    public ServiceA(IServiceB serviceB) { }
}

// Service B depends on Service A - CIRCULAR!
public class ServiceB
{
    public ServiceB(IServiceA serviceA) { }
}
```

**✅ SOLUTIONS**:

**Option 1: Extract shared dependency**
```csharp
public class ServiceA
{
    public ServiceA(ISharedService shared) { }
}

public class ServiceB
{
    public ServiceB(ISharedService shared) { }
}
```

**Option 2: Use events for decoupling**
```csharp
public class ServiceA
{
    public event Action<Data>? OnDataChanged;
}

public class ServiceB(IServiceA serviceA)
{
    // Subscribe to events in constructor body or init method
    public void Initialize()
    {
        serviceA.OnDataChanged += HandleDataChanged;
    }
}
```

**Option 3: Pass data directly**
```csharp
// Instead of injecting the whole service, pass only the data needed
public class ServiceA
{
    public Data GetData() => _data;
}

public class ServiceB
{
    public void ProcessData(Data data) // Method parameter, not constructor
    {
        // Process data without depending on ServiceA
    }
}
```

**Decision Tree - Choosing a Solution**:
1. **Can you extract shared logic?** → Use Option 1 (Extract shared dependency)
2. **Is this an observer pattern scenario?** → Use Option 2 (Events)
3. **Does one service only need data, not behavior?** → Use Option 3 (Pass data directly)
4. **Still circular?** → Rethink your design - you may have incorrect separation of concerns

## Registration Patterns

### Registering with Dependencies
```csharp
// Service with dependencies (using primary constructor)
public class AnimationSystem(ITextureFactory textureFactory) : ISystem
{
    // Use textureFactory in methods
}

// Simple registration - DryIoc auto-resolves dependencies
container.Register<AnimationSystem>(Reuse.Singleton);
```

### Registering with Setup
```csharp
// Service needing initialization
container.Register<ISceneManager, SceneManager>(
    Reuse.Singleton,
    setup: Setup.With(allowDisposableTransient: true));
```

## Step-by-Step DI Review Workflow

When reviewing code for DI compliance, follow this systematic approach:

1. **Scan for static singletons**:
   ```bash
   grep -r "static.*Instance" --include="*.cs" Engine/ Editor/ | grep -v "Constants.cs"
   ```

2. **Check constructor injection**:
   - Verify all dependencies are in constructor parameters
   - Ensure no property injection or service locator usage

3. **Validate registrations**:
   - Open `Editor/Program.cs` or `Runtime/Program.cs`
   - Ensure all injected types are registered
   - Verify appropriate lifetime (Singleton vs Transient)

4. **Verify service lifetimes**:
   - Singleton services should NOT depend on Transient services
   - Check for proper disposal of IDisposable services

5. **Test resolution**:
   - Build and run the application
   - Watch for DI-related errors at startup
   - Circular dependencies will fail immediately

## Debugging DI Issues

For detailed troubleshooting steps, common error solutions, and automated validation scripts with expected outputs, see the [Debugging Guide](references/debugging-guide.md).

**Quick validation commands:**
- Detect static singletons: `grep -rn "static.*Instance.*=>" --include="*.cs" Engine/ Editor/ | grep -v "Constants.cs"`
- Find service locator usage: `grep -rn "ServiceLocator\|\.Resolve<" --include="*.cs" Engine/ Editor/`
- Check property injection: `grep -rn "{ get; set; }.*Factory\|{ get; set; }.*Manager" --include="*.cs" Engine/ Editor/`
