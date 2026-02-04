---
name: comet-scaffold
description: React Native 脚手架 comet CLI 命令规范与项目配置。当用户提到"comet"、"脚手架"、"scaffold"、"初始化项目"、"创建应用"、"项目结构"、"comet.yaml"时使用此 skill。
---

# Comet 脚手架命令规范

基于 React Native 通用脚手架设计方案的 CLI 命令与配置约定。

## 核心配置文件

### comet.yaml

脚手架的单一配置源，记录所有工程约定：

```yaml
name: my_app
org: com.example

package_manager: pnpm

build_tool: expo_prebuild # expo_prebuild | bare
architecture: new # new | old
integration: greenfield # greenfield | brownfield

state_management: zustand
server_state: tanstack_query
router: react_navigation

styling_engine: nativewind # nativewind | unistyles | restyle | stylesheet
forms: rhf_zod # rhf_zod | none
permissions: unified # unified | none
deep_linking: true
app_scheme: myapp
universal_links:
  - example.com

envs:
  - name: development
    android_flavor: dev
    ios_scheme: MyApp-Dev
    env_file: .env.development
  - name: staging
    android_flavor: stg
    ios_scheme: MyApp-Stg
    env_file: .env.staging
  - name: production
    android_flavor: prod
    ios_scheme: MyApp
    env_file: .env.production

modules:
  network: true
  storage: true
  i18n: true
  sentry: true
  svg: true
  e2e: false
```

---

## CLI 命令

### 创建应用

```bash
comet create app <app_name> \
  --org com.example \
  --package-manager pnpm \
  --build-tool expo_prebuild \
  --architecture new \
  --integration greenfield \
  --state-management zustand \
  --router react_navigation \
  --enable-network \
  --enable-storage \
  --with-i18n \
  [--with-sentry] \
  [--with-ci]
```

**行为**：

- Expo Prebuild（默认）：基于 `npx create-expo-app@latest` 初始化
- Bare RN（可选）：基于 `npx @react-native-community/cli init` 初始化
- 生成标准目录结构（`src/app`、`src/core`、`src/features`）
- 初始化多环境配置
- 若指定 `--with-ci`，生成 `.github/workflows/ci.yml`

### 创建 Feature

```bash
comet create feature <feature_name> \
  [--route Counter] \
  [--no-domain] \
  [--no-data]
```

**生成结构**：

```text
src/features/<feature_name>/
  presentation/
    screens/<FeatureName>Screen.tsx
    components/<FeatureName>View.tsx
    stores/use<FeatureName>Store.ts
  domain/
    entities/<featureName>.ts
    repositories/<featureName>Repository.ts
  data/
    datasources/<FeatureName>RemoteDataSource.ts
    repositories/<FeatureName>RepositoryImpl.ts
```

**选项**：

- `--route`：自动在 Root Navigator 注册路由
- `--no-domain`：不生成 domain 层
- `--no-data`：不生成 data 层

### 创建 Service

```bash
comet create service <service_name>
```

在 `src/core/` 下生成服务骨架，如 `analytics`、`crash_reporting` 等。

### 辅助命令

| 命令                 | 说明                          |
| -------------------- | ----------------------------- |
| `comet lint`         | 运行 ESLint + TypeScript 检查 |
| `comet format`       | 运行 Prettier                 |
| `comet test`         | 运行 Jest（可选 Detox）       |
| `comet doctor`       | 检查项目是否符合脚手架约定    |
| `comet upgrade-core` | 统一升级核心依赖版本          |

---

## 项目目录结构

### 顶层目录

```text
project_root/
  app.json or app.config.ts   # Expo 配置
  android/                    # 原生 Android（Prebuild 生成）
  ios/                        # 原生 iOS（Prebuild 生成）
  src/                        # 源代码
  assets/                     # 静态资源
  __tests__/                  # 测试文件
  .vscode/ or .idea/          # IDE 配置
  babel.config.js
  metro.config.js
  tsconfig.json
  package.json
  comet.yaml                  # 脚手架配置
  README.md
```

### src 目录结构

```text
src/
  app/
    App.tsx                   # 根组件：Provider、NavigationContainer
    bootstrap.ts              # 应用引导初始化
    di.ts                     # 可选：跨 feature 核心依赖收口
    navigation/
      routes.ts               # 路由常量/类型（ParamList）
      RootNavigator.tsx       # Root Navigator

  core/                       # 无业务基础设施
    config/
      env.ts                  # 环境抽象
      appConfig.ts            # 配置汇总
    error/
      appError.ts             # 错误模型
      errorMapper.ts          # 错误映射
      errorReporter.ts        # 错误上报
    forms/
      formTypes.ts            # 表单类型
      zodSchemas.ts           # Zod Schema
    network/
      httpClient.ts           # axios/fetch 封装
      interceptors/
        authInterceptor.ts
        loggingInterceptor.ts
    permissions/
      permissions.ts          # 权限类型
      usePermission.ts        # 权限 Hook
    storage/
      keyValueStorage.ts      # KV 存储抽象
      secureStorage.ts        # 安全存储
    theme/
      tokens.ts               # 设计 token
      theme.ts                # 主题对象
    styling/
      styling.ts              # 样式引擎适配
    i18n/
      i18n.ts                 # i18next 初始化
    utils/
      logger.ts
      result.ts               # Result 类型
    components/
      AppScaffold.tsx
      LoadingIndicator.tsx
      ErrorView.tsx
      PrimaryButton.tsx

  features/                   # Feature-first 业务模块
    counter/                  # 示例 feature
      presentation/
        screens/
          CounterScreen.tsx
        components/
          CounterView.tsx
        stores/
          useCounterStore.ts
      domain/
        entities/
          counter.ts
        repositories/
          counterRepository.ts
      data/
        datasources/
          counterLocalDataSource.ts
        repositories/
          counterRepositoryImpl.ts
```

---

## 技术选型（默认）

| 类别     | 技术                                 |
| -------- | ------------------------------------ |
| 构建工具 | Expo（Prebuild / CNG）               |
| 底层架构 | New Architecture                     |
| 语言     | TypeScript（strict）                 |
| 包管理   | pnpm                                 |
| 导航     | React Navigation 7                   |
| 状态管理 | Zustand + TanStack Query             |
| 样式     | NativeWind                           |
| 表单     | React Hook Form + Zod                |
| 网络     | axios                                |
| 存储     | AsyncStorage / MMKV                  |
| 国际化   | i18next                              |
| 监控     | Sentry                               |
| 测试     | Jest + @testing-library/react-native |

---

## 临时初始化（comet 未落地前）

### Expo（推荐）

```bash
npx create-expo-app@latest MyApp
cd MyApp
npx expo start

# 需要原生工程时
npx expo prebuild --clean
```

### Bare React Native

```bash
npx @react-native-community/cli@latest init MyApp
cd MyApp
npx react-native run-android
# 或
npx react-native run-ios
```

---

## 环境切换

### 原生构建维度

- iOS：Scheme/Configuration（Debug/Staging/Release）
- Android：productFlavors（dev/staging/prod）+ buildTypes

### JS 侧读取

- Expo：`app.config.ts` + EAS 环境变量
- Bare RN：`react-native-config` + `.env.*`

### 运行脚本示例

```json
{
  "scripts": {
    "ios:dev": "expo start --ios",
    "ios:stg": "expo start --ios --variant staging",
    "android:dev": "expo start --android",
    "android:stg": "expo start --android --variant staging"
  }
}
```

---

## 依赖版本参考（2025-12）

以模板 `package.json` + lockfile 为准，以下仅供参考：

| 包                       | 版本    |
| ------------------------ | ------- |
| react                    | 19.2.3  |
| react-native             | 0.83.0  |
| @react-navigation/native | 7.1.25  |
| zustand                  | 5.0.9   |
| @tanstack/react-query    | 5.90.12 |
| axios                    | 1.13.2  |
| i18next                  | 25.7.2  |
| @sentry/react-native     | 7.7.0   |

定期运行 `npx expo doctor` 和 `pnpm outdated` 检查兼容性。
