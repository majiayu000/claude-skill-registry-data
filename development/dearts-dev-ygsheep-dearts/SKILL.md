---
name: dearts-dev
description: DearTs Framework 开发技能。基于 SDL3 + ImGui 的 C++20 现代应用框架，提供完整的应用生命周期管理、类型安全事件系统、Content Registry 和插件架构。适用于 DearTs Framework 相关的所有开发任务，包括应用程序开发、事件驱动架构、插件系统、多视图应用等。
---

# DearTs Framework 开发技能

## 概述

DearTs 是一个基于 SDL3 + ImGui 的现代 C++20 应用程序框架，参考 ImHex 设计理念，提供完整的模块化架构。

**核心特性：**
- C++20 (Concepts, Ranges, std::format)
- SDL3 + ImGui 2.13.3 (Docking, Multi-viewport)
- 类型安全事件总线 (EventBus)
- Result<T, E> 错误处理
- Content Registry (ImHex 风格命令/工具/设置系统)
- 多视图停靠窗口系统
- 插件架构 (API 版本检查，动态加载)
- 异步日志 (liblogger)
- 任务管理器 (TaskManager)
- 配置管理 (ConfigManager)

## 快速开始

### 1. 项目结构

```
DearTs/
├── core/              # 核心系统
│   ├── app/           # 应用生命周期
│   ├── events/        # 事件总线
│   ├── ui/            # ImGui 集成、视图
│   ├── content/       # Content Registry
│   ├── tasks/         # 任务管理
│   ├── plugin/        # 插件系统
│   └── config/        # 配置管理
├── plugins/           # 插件实现
│   └── builtin/       # 内置插件
└── main/gui/          # 入口
```

### 2. 创建应用

```cpp
#include "core/app/application.h"

class MyApp : public DearTs::Core::Application {
    bool on_initialize() override {
        LOG_INFO("Application starting");
        return true;
    }

    void on_render() override {
        ImGui::Begin("Hello");
        ImGui::Text("Hello DearTs!");
        ImGui::End();
    }
};

int main() {
    MyApp app;
    return app.run();
}
```

### 3. 创建插件

```cpp
#include "core/plugin/plugin.h"

class MyPlugin : public IPlugin {
public:
    PluginInfo get_info() const override {
        return PluginInfo{
            .name = "MyPlugin",
            .author = "You",
            .description = "My plugin",
            .version = "1.0.0",
            .api_version = "1.0.0"
        };
    }

    Result<void, std::string> on_load() override {
        // 注册命令、视图
        ContentRegistry::Commands::register_handler(
            "my.action", "My Action", []() { /* ... */ }
        );
        ContentRegistry::Views::add<MyView>();
        return Result::ok();
    }
};

// 注册插件
PluginManager::instance().add_builtin(
    std::make_unique<MyPlugin>()
);
```

### 4. 核心系统快速示例

**事件系统:**
```cpp
// 订阅
EventBus::Token token = EventBus::instance().subscribe<Event>(
    [](const Event& e) { /* handle */ }
);

// 发布
EventBus::instance().publish(Event{ ... });
// Token RAII 自动取消订阅
```

**配置管理:**
```cpp
ConfigScope cfg("app.window");
cfg.set("width", 1280);
int width = cfg.get_or<int>("width", 1280);

// 加载/保存 JSON
ConfigManager::instance().load_from_file("config.json");
ConfigManager::instance().save_to_file("config.json");
```

**任务管理:**
```cpp
auto task = TaskManager::instance().launch(
    "Loading File",
    [](const auto& cancel) {
        for (int i = 0; i < 100 && !cancel; i++) {
            // do work
        }
    }
);
```

**日志:**
```cpp
LOG_INFO("Loading: {}", filename);
LOG_ERROR("Failed: {}", error);
```

## 核心系统架构

### 1. 应用生命周期

```
UNINITIALIZED → INITIALIZING → RUNNING ←→ PAUSED
                            ↓         ↓
                         STOPPING ←──┘
                            ↓
                        STOPPED
```

### 2. 插件生命周期

```
未加载 (Unloaded)
    ↓ add_builtin() / load_from_file()
已加载 (Loaded)
    ↓ enable()
已启用 (Enabled)
    ↓ disable()
已加载 (Loaded)
    ↓ unload()
未加载 (Unloaded)
```

### 3. 数据流

```
用户操作
    ↓
ContentRegistry::Commands::invoke()
    ↓
EventBus::publish(Event)
    ↓
插件事件处理器
    ↓
UI 更新 / 后台任务
```

## 构建和运行

### 构建

```bash
# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Run
./build/bin/DearTsApp.exe
```

### 依赖

- CMake 3.20+
- C++20 编译器 (MSVC 2022 / GCC 11+ / Clang 13+)
- SDL3
- ImGui 2.13.3+
- nlohmann/json
- fmtlib

## 参考文档

### 📘 核心 API 手册（优先阅读）

| 文档 | 说明 | 用途 |
|------|------|------|
| **[config_manager_api.md](references/config_manager_api.md)** | ConfigManager 完全手册 | 配置管理、层级键、JSON 持久化 |
| **[logger_api.md](references/logger_api.md)** | Logger 完全手册 | 日志记录、文件输出、级别控制 |
| **[task_manager_api.md](references/task_manager_api.md)** | TaskManager 完全手册 | 异步任务、进度跟踪、任务取消 |
| **[plugin_system_api.md](references/plugin_system_api.md)** | Plugin System 完全手册 | 插件开发、生命周期、API 集成 |

### 📕 其他参考文档

**核心系统:**
- [result_type.md](references/result_type.md) - Result<T, E> 类型详解
- [event_system.md](references/event_system.md) - EventBus 事件系统
- [content_registry.md](references/content_registry.md) - Content Registry 详解
- [ui_system.md](references/ui_system.md) - UI 系统（视图、停靠窗口）

**应用层:**
- [application_api.md](references/application_api.md) - Application 类 API
- [task_system.md](references/task_system.md) - 任务系统详解
- [plugin_system.md](references/plugin_system.md) - 插件系统详解

**集成指南:**
- [sdl3_init.md](references/sdl3_init.md) - SDL3 初始化指南
- [imgui_integration.md](references/imgui_integration.md) - ImGui 集成指南
- [cmake_config.md](references/cmake_config.md) - CMake 配置详解
- [logging_guide.md](references/logging_guide.md) - 日志系统使用指南

### 📙 示例和模板

**插件示例:**
- `plugins/builtin/` - 内置插件完整实现
- `plugins/builtin/include/views/` - 视图示例

**代码模板:**
- `assets/app_template.cpp` - 应用程序模板
- `assets/view_template.cpp` - 视图模板
- `assets/plugin_template.cpp` - 插件模板
- `assets/cmake_template.txt` - CMake 模板

**渲染示例:**
- `examples/SDL3_ImGui_Hybrid_Rendering.md` - SDL3 + ImGui 混合渲染
- `examples/interactive_sdl_render.md` - 交互式 SDL 渲染

## 常见任务快速索引

| 任务 | 查阅文档 |
|------|---------|
| **创建插件** | [plugin_system_api.md](references/plugin_system_api.md) |
| **管理配置** | [config_manager_api.md](references/config_manager_api.md) |
| **异步任务** | [task_manager_api.md](references/task_manager_api.md) |
| **添加日志** | [logger_api.md](references/logger_api.md) |
| **事件系统** | [event_system.md](references/event_system.md) |
| **注册命令** | [content_registry.md](references/content_registry.md) |
| **创建视图** | [ui_system.md](references/ui_system.md) |
| **错误处理** | [result_type.md](references/result_type.md) |
| **CMake 配置** | [cmake_config.md](references/cmake_config.md) |

## 开发最佳实践

### ✅ DO

1. **使用 Result<T, E> 处理错误**
   ```cpp
   Result<Data, std::string> load() {
       if (error) return Result::err("Failed");
       return Result::ok(data);
   }
   ```

2. **使用 RAII 管理资源**
   - EventBus::Token (自动取消订阅)
   - ConfigScope (自动前缀)
   - 智能指针

3. **查看 API 文档而非源码**
   - 4 个核心 API 手册在 `references/`
   - 每个手册都有完整示例

4. **使用 Content Registry**
   ```cpp
   ContentRegistry::Commands::register_handler("id", "Name", callback);
   ContentRegistry::Views::add<MyView>();
   ```

### ❌ DON'T

1. **不要用异常做控制流** - 使用 Result<T, E>
2. **不要忘记 API 版本** - 插件必须匹配
3. **不要使用全局状态** - 存储在插件成员或 ConfigManager
4. **不要手动管理资源** - 让 RAII 处理

## 技能使用场景

此技能在以下场景自动激活：

- 创建基于 SDL3 + ImGui 的 C++ 应用
- 实现类型安全的事件系统
- 开发插件系统
- 创建多视图停靠窗口
- 使用 Result 类型错误处理
- 使用 ConfigManager 管理配置
- 使用 TaskManager 执行异步任务
- 使用 Logger 记录日志
- 开发 UI 插件（视图、命令、工具）
- 查看 DearTs API 文档

## 项目资源

### 文档
- 项目文档: `docs/`
- 插件快速开始: `plugins/QUICKSTART.md`
- 插件用户指南: `docs/plugin_system_guide.md`

### 架构图
- 14 个高分辨率架构图: `docs/diagrams/`
- 包括：生命周期、类关系、事件流程、渲染管线等

### 外部链接
- SDL3 文档: https://wiki.libsdl.org/SDL3/
- ImGui GitHub: https://github.com/ocornut/imgui
- ImHex GitHub: https://github.com/WerWolv/ImHex
- CMake 文档: https://cmake.org/documentation/
- C++ 参考: https://en.cppreference.com/w/cpp

---

**技能版本**: 3.0.0
**最后更新**: 2025-12-30
**框架版本**: DearTs Framework 1.0.0
