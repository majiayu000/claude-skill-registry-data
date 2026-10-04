---
name: scaffold-flutter-riverpod-drift
description: 当用户要起一个 Flutter app 项目,采用 Riverpod 状态管理 + Drift 本地数据库 + 可选云同步的成熟架构时使用。脱胎于 BeeCount(蜜蜂记账)生产实践,包含 Design Token 系统、Repository 多端切换、缓存→Stream 切流、严格 Drift 迁移纪律、PrimaryHeader/SectionCard 统一页面骨架等模式。触发关键词:"scaffold Flutter Riverpod 项目"、"新建一个 Flutter app"、"起一个 BeeCount 风格的 Flutter 项目"、"flutter app with riverpod and drift"、"create flutter mobile app starter"、"按 flutter-riverpod-drift 模板建项目"。不适用于纯 Flutter web、用 BLoC/GetX 的项目、demo 级 app。
---

# Flutter + Riverpod + Drift 脚手架技能

## 这套架构是什么

一个**生产级 Flutter app 骨架**,核心信念是"约定大于配置":通过强制 Design Token + Repository 抽象 + Drift 迁移纪律 + 统一日志/Toast/Header,让 app 在规模变大时不腐烂。**核心定位:有云同步可能、有本地 DB 缓存需求、看重设计一致性的成熟 app。**

不是 demo 起手式,不是"helloworld counter app"。它假定你愿意为长期可维护性付一点首日成本。

## 选型表

| 层 | 选型 | 为什么 |
|---|------|--------|
| State Mgmt | flutter_riverpod ^2.5 | 编译期类型安全,不依赖 `BuildContext`,refs 显式 — 比 Provider/GetX 更适合中大型 app |
| Local DB | Drift ^2.20 + sqlite3_flutter_libs | type-safe DSL + 代码生成,migration 工具成熟,Stream 监听原生 |
| 设计系统 | 自建 `BeeTokens` / `BeeDimens` / `BeeShadows` / `BeeTextTokens` | Material `ThemeData` 颗粒度不够,亮/暗模式手工切麻烦,Token 一次写好自动适配 |
| 页面骨架 | `PrimaryHeader` + `SectionCard` | AppBar 在自定义状态栏色/渐变/暗黑模式分割线时太多奇技淫巧;自定义 Header 一劳永逸 |
| Toast | 自建 `showToast(context, msg)` | `ScaffoldMessenger.showSnackBar` 在 Header 自定义后容易被遮、且样式控制差 |
| 日志 | 自建 `LoggerService` 全局 instance | 需要持久化 / 应用内查看 / 原生桥接,`print` 都做不到 |
| 响应式 | `.scaled(context, ref)` double/int/EdgeInsets 扩展 | 用户字体设置 × 屏幕尺寸双因子缩放,统一一处实现 |
| i18n | flutter_localizations + `.arb` | 官方方案,跑 `flutter gen-l10n` 出代码,IDE 补全友好 |
| 路由 | Navigator 1.0 + MaterialPageRoute | 不上 go_router,大多数 app 用不到深链;真要深链再加 app_links |
| Cloud(可选) | supabase_flutter / 自建 REST | Repository 抽象层在中间,后端选型不锁死 |
| 数据库迁移 | Drift `MigrationStrategy.onUpgrade` | 唯一允许的迁移入口;禁止启动期 raw SQL / 自维护 schema_migrations |

## 仓库布局(`lib/` 树)

```
lib/
├── main.dart                       # 入口:bindings + Riverpod ProviderScope + runApp
├── app.dart                        # App widget:MaterialApp + 主题/locale 注入
├── theme.dart                      # BeeTheme.light/dark:Token + primaryColor → ThemeData
│
├── providers.dart                  # (可选)顶层 barrel,向后兼容老 import
├── providers/                      # 按 domain 拆的 Riverpod providers
│   ├── theme_providers.dart        # primaryColorProvider, darkModeProvider, darkModePatternStyleProvider
│   ├── font_scale_provider.dart    # effectiveFontScaleProvider
│   ├── database_providers.dart     # databaseProvider, repositoryProvider
│   ├── language_provider.dart      # localeProvider
│   ├── ui_state_providers.dart     # cachedXxxProvider, switch-to-stream triggers
│   └── <domain>_providers.dart     # 业务域:auth/cloud_mode/sync/...
│
├── data/
│   ├── db.dart                     # Drift database:schemaVersion + onUpgrade(唯一迁移入口)
│   ├── db.g.dart                   # build_runner 产物(gitignored 还是 commit 看团队)
│   └── repositories/
│       ├── repositories.dart       # barrel
│       ├── base_repository.dart    # abstract class 聚合所有 *_repository interface
│       ├── <entity>_repository.dart    # 每个 entity 一个 interface(纯抽象)
│       ├── local/
│       │   ├── local_repository.dart       # 委托到每个子 repo
│       │   └── local_<entity>_repository.dart  # Drift 实现
│       └── cloud/                  # 可选:云端实现
│           ├── cloud_repository.dart
│           └── cloud_<entity>_repository.dart
│
├── pages/
│   ├── main/                       # 首页、底部 tab 主入口
│   ├── <feature>/                  # 按功能域拆,与 providers/ 对称
│   └── settings/                   # 设置页(参考骨架最完整 — 第一个新页面参考它)
│
├── widgets/
│   ├── ui/                         # 通用 UI 基元(无业务知识)
│   │   ├── ui.dart                 # 导出 barrel
│   │   ├── primary_header.dart     # ⭐ 替代 AppBar,ConsumerWidget 拿 ref
│   │   ├── toast.dart              # ⭐ showToast(context, msg),替代 SnackBar
│   │   ├── dialog.dart             # showBeeDialog 系列
│   │   └── ...                     # wheel pickers / popup / dropdown
│   └── biz/                        # 业务级组件(可能有 domain 知识)
│       └── section_card.dart       # ⭐ SectionCard:卡片容器,Token 驱动
│
├── styles/
│   ├── tokens.dart                 # ⭐ BeeTokens / BeeDimens / BeeShadows / BeeTextTokens
│   └── colors.dart                 # 调色板常量(只被 tokens.dart 引用)
│
├── services/
│   ├── system/
│   │   └── logger_service.dart     # ⭐ global `logger` instance,替代 print/debugPrint
│   ├── ui/
│   │   └── ui_scale_service.dart   # scaled 算法实现
│   └── <domain>/                   # 业务 service(不直接访问 DB,通过 Repository)
│
├── utils/
│   ├── ui_scale_extensions.dart    # ⭐ .scaled(context, ref) 扩展(double/int/EdgeInsets/BorderRadius)
│   └── ...
│
├── models/                         # 纯 DTO,不是 Drift ORM(domain object,跨层传输)
└── l10n/
    ├── app_en.arb
    ├── app_zh.arb
    └── app_localizations.dart      # flutter gen-l10n 产物
```

**几个关键约定**:

- **`providers.dart` 在根目录**:历史原因(很多老页面 `import '../providers.dart'`),作为 barrel 向后兼容。新代码直接 import `providers/<specific>_providers.dart` 即可。
- **`widgets/ui/` 严格无业务知识**:这里的组件可以 copy 到任何 Flutter 项目用。业务组件去 `widgets/biz/`。
- **`pages/` 与 `providers/` 按 domain 对称**:`pages/budget/` ↔ `providers/budget_providers.dart`,容易找。
- **`data/` 是数据层唯一入口**:UI 永远不直接 import `data/db.dart`,只通过 Repository(再通过 Provider 包装)。

## 9 个核心模式(必读)

### 1. Design Token 系统(替代直接颜色值)

`lib/styles/tokens.dart` 提供 4 个 token 类:

```dart
class BeeTokens {
  // Surface(背景)
  static Color scaffoldBackground(BuildContext c) =>
      isDark(c) ? Colors.black : Colors.grey.shade50;
  static Color surface(BuildContext c) =>
      isDark(c) ? const Color(0xFF1C1C1E) : Colors.white;
  static Color surfaceHeader(BuildContext c) =>
      isDark(c) ? Colors.black : Theme.of(c).colorScheme.primary;

  // Text / Icon / Border / Semantic(成功/警告/错误)
  static Color textPrimary(BuildContext c) => ...;
  static Color iconPrimary(BuildContext c) => ...;
  static Color divider(BuildContext c) => ...;

  static bool isDark(BuildContext c) =>
      Theme.of(c).brightness == Brightness.dark;
}

class BeeDimens {
  static const p4 = 4.0, p8 = 8.0, p12 = 12.0, p16 = 16.0, p24 = 24.0;
  static const radius8 = 8.0, radius12 = 12.0, radius16 = 16.0;
}

class BeeShadows {
  static const card = [BoxShadow(blurRadius: 8, color: Colors.black12)];
}

class BeeTextTokens {
  static TextStyle title(BuildContext c) => TextStyle(
        fontSize: 18, fontWeight: FontWeight.w600,
        color: BeeTokens.textPrimary(c));
  static TextStyle label(BuildContext c) => ...;
  static TextStyle body(BuildContext c) => ...;
}
```

**使用规则**:UI 颜色 = `BeeTokens.xxx(context)`,不要 `Colors.grey.shade100` 也不要 `Color(0xFFXXX)`。间距/圆角用 `BeeDimens.pN/radiusN` 常量(高优:相对 scale 不变)或 `.scaled()` 扩展(高优:跟用户字号设置同步)。

### 2. PrimaryHeader + SectionCard 页面骨架(替代 AppBar)

```dart
class ExamplePage extends ConsumerStatefulWidget {
  const ExamplePage({super.key});
  @override
  ConsumerState<ExamplePage> createState() => _ExamplePageState();
}

class _ExamplePageState extends ConsumerState<ExamplePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: BeeTokens.scaffoldBackground(context),
      body: Column(
        children: [
          PrimaryHeader(
            title: '页面标题',
            subtitle: '副标题',         // 可选
            showBack: true,
            actions: [/* IconButton 系列 */],
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.symmetric(
                horizontal: 12.0.scaled(context, ref),
                vertical: 8.0.scaled(context, ref),
              ),
              children: [
                SectionCard(
                  child: Column(children: [/* 内容块 */]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

`SectionCard` 内部用 `BeeTokens.surface(context)` 当背景,亮色加 `BeeShadows.card`,暗黑加主题色边框 — 自动适配。

### 3. Repository 多端切换(数据访问唯一入口)

四层结构:
- **Interface**:`lib/data/repositories/<entity>_repository.dart` — 纯抽象方法签名
- **Base**:`lib/data/repositories/base_repository.dart` — `abstract class BaseRepository implements <Entity1>Repository, <Entity2>Repository, ... {}`
- **Local 实现**:`lib/data/repositories/local/local_<entity>_repository.dart` — Drift 操作
- **Cloud 实现**(可选):`lib/data/repositories/cloud/cloud_<entity>_repository.dart` — Supabase/REST

`local_repository.dart` 和 `cloud_repository.dart` 各自委托到对应子 repo。`repositoryProvider` 根据 `appModeProvider` 返回 Local 或 Cloud 实例。

**业务代码访问数据的唯一方式**:
```dart
// ❌ UI 不要直接调:
final repo = ref.watch(repositoryProvider);
return FutureBuilder(future: repo.getAllX(), ...);  // 每次 build 都查!

// ✅ UI 用 Provider 包一层:
final xsProvider = FutureProvider<List<X>>((ref) async {
  ref.watch(xListRefreshProvider);  // 监听刷新触发器
  final repo = ref.watch(repositoryProvider);
  return repo.getAllX();
});
// 在 widget 里 final xs = ref.watch(xsProvider);
```

**加新数据操作的 4 步**:
1. 在 `<entity>_repository.dart` interface 加方法签名
2. 在 `local/local_<entity>_repository.dart` 实现 Drift 版
3. 在 `local/local_repository.dart` 加委托
4. (可选)cloud 端同步实现

**绝不允许**业务代码出现 `if (ref.watch(appModeProvider) == AppMode.cloud)` — 这是泄漏抽象。

### 4. Drift 严格迁移纪律

`schemaVersion` 每次 schema 变更必须 +1。所有迁移**只能**在 `db.dart` 的 `MigrationStrategy.onUpgrade` 写:

```dart
class BeeDatabase extends _$BeeDatabase {
  BeeDatabase() : super(_openConnection());

  @override
  int get schemaVersion => N;  // 每次改 schema +1

  @override
  MigrationStrategy get migration => MigrationStrategy(
    onUpgrade: (migrator, from, to) async {
      if (from < 2) {
        await customStatement(
          'ALTER TABLE foo ADD COLUMN bar INTEGER NOT NULL DEFAULT 0;');
      }
      if (from < 3) {
        await migrator.createTable(newTable);
      }
      // ... 累积所有 from < N 的块
    },
  );
}
```

**绝对禁止**:
- ❌ `main.dart` 或启动代码里手动建独立 `BeeDatabase()` 跑迁移
- ❌ `CREATE TABLE x AS SELECT FROM old_x` 重建表(新字段不会自动同步)
- ❌ 自维护 `schema_migrations` 版本表

新用户首次安装走 Drift 默认 `onCreate` → `createAll()`,自动建完整 schema。

### 5. Riverpod Provider 组织约定

- **全局共享**:`lib/providers/<domain>_providers.dart`,文件名按 domain 拆(`theme_providers.dart`、`budget_providers.dart`、`sync_providers.dart` 等)
- **页面内部**:定义在页面文件顶部,scope 小
- **命名**:
  - `xxxProvider` — `Provider<T>`
  - `xxxStreamProvider` — `StreamProvider<T>`
  - `xxxFutureProvider` — `FutureProvider<T>`
  - `xxxRefreshProvider` — `StateProvider<int>` 触发器(`ref.read(...notifier).state++` 触发依赖它的 provider 重建)

**核心 provider 命名(scaffold 应预设)**:
```dart
final primaryColorProvider = StateProvider<Color>((ref) => const Color(0xFFFFC107));
final effectiveFontScaleProvider = StateProvider<double>((ref) => 1.0);
final databaseProvider = Provider<BeeDatabase>((ref) => BeeDatabase());
final repositoryProvider = Provider<BaseRepository>((ref) => LocalRepository(ref.watch(databaseProvider)));
```

### 6. 缓存 + Stream 双阶段(列表页秒开)

列表页(首页、账单、记录)的标准模式:
1. App 启动时,splash 预加载前 N 条数据写入 `cachedXxxProvider`
2. 列表页 `initState` 读 cache 立即渲染(秒开,无 loading)
3. 同时启动一个 Stream 监听数据库
4. 用户做任何会改数据的交互(编辑、删除、切换 context)前,调 `switchToStreamMode()` 抛弃 cache 走实时 Stream

伪代码:
```dart
class TransactionList extends ConsumerStatefulWidget { ... }

class _TransactionListState extends ConsumerState<TransactionList> {
  bool _useCache = true;

  void switchToStreamMode() => setState(() => _useCache = false);

  @override
  Widget build(BuildContext context) {
    if (_useCache) {
      final cached = ref.watch(cachedTransactionsProvider);
      return _list(cached);
    }
    final streamAsync = ref.watch(transactionsStreamProvider);
    return streamAsync.when(data: _list, ...);
  }
}
```

**必须触发 `switchToStreamMode()` 的场景**:点击编辑、切换账本/分类/筛选器、任何会让 cache 过时的用户操作。

### 7. 统一日志(`LoggerService`)

`lib/services/system/logger_service.dart` 暴露全局 `logger` 实例:

```dart
import '../../services/system/logger_service.dart';

logger.debug('TAG', '调试');
logger.info('Sync', '同步开始,5 条 change');
logger.warning('Auth', 'token 即将过期');
logger.error('Network', '请求失败', error, stackTrace);
```

**绝对禁止** `print()` / `debugPrint()` / 第三方 logger 包 — 因为 LoggerService 会:
- 持久化到本地(48h 滚动)
- 在应用内日志面板可查看 / 导出
- 桥接到原生侧(Android/iOS 日志)
- Debug build 自动 console 输出

### 8. 响应式缩放(`.scaled()` 扩展)

`lib/utils/ui_scale_extensions.dart`:
```dart
extension UIScaleDouble on double {
  double scaled(BuildContext c, WidgetRef ref) {
    final s = ref.watch(effectiveFontScaleProvider);
    return UIScaleService.scale(c, this, s);
  }
}
// 同样实现 UIScaleInt / UIScaleEdgeInsets / UIScaleBorderRadius
```

使用:
```dart
SizedBox(height: 16.0.scaled(context, ref))
Padding(padding: EdgeInsets.all(12).scaled(context, ref))
```

**所有"看起来跟文字大小有关的尺寸"必须用 `.scaled()`** — 用户调大字号时整个布局会等比放大。纯硬编码(如固定 1px 边框)用 `BeeDimens` 常量。

### 9. Toast 替代 SnackBar

```dart
import '../widgets/ui/ui.dart';  // 已导出 showToast

showToast(context, '保存成功');
```

`ScaffoldMessenger.showSnackBar()` **禁用** — 在自定义 PrimaryHeader 下样式会错位 + 难以全局自定义。

## scaffold 执行流程(AI 执行步骤)

当用户说"按 flutter-riverpod-drift 起一个新项目叫 Foo"时,按以下顺序执行。

### Step 1: 收集参数

一次性问全(不要来回往返):
- **项目名**:kebab-case(如 `foo-app`)+ Dart 包名(snake_case,如 `foo_app`)
- **目标路径**:默认 `~/code/mine/<project-name>`
- **organization**:用于 bundle id 反向域名(默认 `com.<github_owner>`)
- **GitHub owner**:用于 repo URL 等
- **云同步**:无 / Supabase / 自建 REST(默认无 — 先把本地骨架跑通)
- **i18n 语言**:中文 / 英文 / 双语(默认双语 zh + en)
- **可选模块**:home_widget / 通知(local_notifications)/ 摄像头(ML Kit)/ Excel 导入 — 默认全关,有需要再开

### Step 2: `flutter create` 起空壳

```bash
flutter create \
  --org com.<github_owner> \
  --project-name <pkg_name> \
  --platforms=ios,android \
  --description "<description>" \
  <target_path>
```

完成后,清掉默认 `lib/main.dart` 和 `test/widget_test.dart` 内容(保留文件,稍后重建)。

### Step 3: 写 pubspec.yaml 基线依赖

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  flutter_riverpod: ^2.5.1
  drift: ^2.20.2
  sqlite3_flutter_libs: ^0.5.24
  path_provider: ^2.1.4
  path: ^1.9.0
  intl: ^0.19.0
  shared_preferences: ^2.3.2
  package_info_plus: ^8.0.2
  collection: ^1.18.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0
  drift_dev: ^2.20.2
  build_runner: ^2.4.13

flutter:
  uses-material-design: true
  generate: true  # 启用 flutter gen-l10n
```

可选依赖(按 Step 1 选项追加):
- 云同步=Supabase → `supabase_flutter: ^2.5.6`
- 通知 → `flutter_local_notifications: ^17.2.2` + `timezone: ^0.9.4`
- home_widget → `home_widget: ^0.7.0`
- 文件 → `file_picker: ^8.1.2` + `share_plus: ^12.0.1`

### Step 4: 创建 lib/ 目录树 + 基础文件

按上面"仓库布局"建所有目录。然后生成以下文件:

1. `lib/main.dart` — `WidgetsFlutterBinding.ensureInitialized()` + `ProviderScope` + `runApp(const App())`
2. `lib/app.dart` — `MaterialApp` 包装,注入 theme + locale
3. `lib/theme.dart` — `BeeTheme.light(primary)` / `BeeTheme.dark(primary)` 工厂
4. `lib/styles/tokens.dart` — `BeeTokens` / `BeeDimens` / `BeeShadows` / `BeeTextTokens` 四个类(看上面"9 个核心模式 #1")
5. `lib/styles/colors.dart` — 基础调色板常量
6. `lib/data/db.dart` — 一个 `Users` 表占位 + `BeeDatabase` + `schemaVersion=1` + 空 `MigrationStrategy`
7. `lib/data/repositories/base_repository.dart` — 占位 abstract class
8. `lib/data/repositories/local/local_repository.dart` — 占位实现
9. `lib/data/repositories/<entity>_repository.dart` — 用户实体 interface 占位
10. `lib/data/repositories/local/local_<entity>_repository.dart` — Drift 实现占位
11. `lib/providers/theme_providers.dart` — `primaryColorProvider` + `darkModeProvider`
12. `lib/providers/font_scale_provider.dart` — `effectiveFontScaleProvider`
13. `lib/providers/database_providers.dart` — `databaseProvider` + `repositoryProvider`
14. `lib/providers/language_provider.dart` — `localeProvider`
15. `lib/widgets/ui/ui.dart` — barrel: export primary_header / toast / dialog
16. `lib/widgets/ui/primary_header.dart` — 实现(看"9 个核心模式 #2")
17. `lib/widgets/ui/toast.dart` — `showToast(context, msg)` 实现
18. `lib/widgets/ui/dialog.dart` — `showBeeDialog` 系列
19. `lib/widgets/biz/section_card.dart` — `SectionCard` widget(Token 驱动 + 阴影/边框)
20. `lib/services/system/logger_service.dart` — `LoggerService` + global `logger` 实例
21. `lib/services/ui/ui_scale_service.dart` — scale 算法
22. `lib/utils/ui_scale_extensions.dart` — `.scaled()` 扩展(双精度 + EdgeInsets + BorderRadius)
23. `lib/pages/main/home_page.dart` — 示例首页(用 PrimaryHeader + SectionCard 骨架)
24. `lib/pages/settings/settings_page.dart` — 设置页(主题色、字号、语言、深色模式开关)
25. `lib/l10n/app_zh.arb` + `lib/l10n/app_en.arb` — 基础翻译(commonSave / commonCancel / pageHome / pageSettings)
26. `l10n.yaml` — flutter gen-l10n 配置

### Step 5: 代码生成 + 跑一次自检

```bash
cd <target>
flutter pub get
dart run build_runner build -d        # Drift 代码生成
flutter gen-l10n                        # i18n 代码生成
flutter analyze                         # 静态分析,期望 0 issues
flutter test                            # 期望 0 测试 / 默认 widget test 删掉
flutter run                             # 真机或模拟器跑起来
```

任何一步失败,**立即停下报错**给用户。常见坑:
- iOS pod install 失败:`cd ios && pod install` 单独跑,可能需要 `pod repo update`
- Android Gradle 慢:首次同步 5-10 分钟正常,不要 timeout
- Drift 找不到 `*.g.dart`:确认 `dart run build_runner build -d`(-d 是 delete-conflicting-outputs,关键)

### Step 6: 提示下一步

最后给用户清单:

1. **改主题色**:`providers/theme_providers.dart` 的 `primaryColorProvider` 初始值改成项目品牌色
2. **填 i18n**:`lib/l10n/app_*.arb` 补齐文案,跑 `flutter gen-l10n`
3. **替换 app icon / splash**:用 `flutter_launcher_icons` + `flutter_native_splash`(都不在基线依赖,按需装)
4. **配 signing**:Android `android/key.properties` + iOS Xcode 团队签名
5. **建第一个业务实体**:跟 AI 说"加一个 <实体> 资源",AI 应按"4 步加新数据操作"流程,生成 Drift 表 + Repository interface/impl + Provider + 增删改查 endpoint

## 不要从 BeeCount 抄过来的部分

BeeCount 是个完整账本 app,有很多领域逻辑**不要默认带到新项目**:

- ❌ 账本/交易/分类/账户 ORM 模型(`Ledgers`/`Transactions`/`Categories`/`Accounts` 表)— 域特定
- ❌ 共享账本(`SharedLedger*` 系列、`LedgerMembers`)— 跟"多人协作"绑定
- ❌ 同步引擎(`lib/cloud/sync/sync_engine.dart` 那套 LWW + projection + change_id)— 复杂,新项目按需重设计
- ❌ 周期记账(`recurring_transactions`)— 域特定
- ❌ 标签系统(`Tags`/`TransactionTags`)— 域特定(但 tag 系统的"通用形态"可以参考)
- ❌ 预算(`Budgets`)— 域特定
- ❌ AI Kit(`packages/flutter_ai_kit*`)— 单独的子 monorepo,按需引入
- ❌ home_widget Android/iOS 平台代码 — 自定义太多,需要单独适配
- ❌ OCR / 智能记账(ML Kit + image_cropper)— 域特定
- ❌ Excel 导入(openpyxl 思路 + `excel` 包)— 域特定
- ❌ 蜜蜂主题(BeeCount 黄色 + 蜜蜂图案 / honeycomb 暗黑模式 pattern)— 品牌特定
- ❌ 云端 Supabase schema — 设计跟账本绑死,新项目要按自己领域重设计

**保留并按需启用**:
- ✅ Design Token 系统(模板,但具体色值按品牌调)
- ✅ Repository / Provider / Drift 三层架构
- ✅ PrimaryHeader / SectionCard / Toast / Logger / Scale
- ✅ 主题色 / 字号 / 语言 / 深色模式 设置项
- ✅ 缓存 + Stream 切流模式

## 反模式(已踩过的坑)

- ❌ `AppBar` — 一律用 `PrimaryHeader`,否则状态栏色和 Header 渐变对不上
- ❌ `ScaffoldMessenger.showSnackBar` — 用 `showToast`,SnackBar 会被自定义 Header 挡住
- ❌ `print` / `debugPrint` — 用 `logger.info/debug/warning/error`
- ❌ `Colors.grey.shade100` / 直接 hex 颜色 — 用 `BeeTokens.surface(context)` 等
- ❌ 硬编码 padding/margin 字面量 — 用 `.scaled(context, ref)` 或 `BeeDimens.pN`
- ❌ UI 直接 `ref.watch(repositoryProvider).getX()` 配 `FutureBuilder` — 用 Provider 包一层
- ❌ 业务代码 `if (appMode == AppMode.cloud)` — Repository 抽象层应该屏蔽这种判断
- ❌ Drift 之外的迁移(启动期 raw SQL / 自维护版本表)— 一律走 `MigrationStrategy.onUpgrade`
- ❌ 在 `main.dart` 之外 new `BeeDatabase()` — 用 `databaseProvider`
- ❌ 忘了 ConsumerWidget / ConsumerStatefulWidget — 否则拿不到 `ref`
- ❌ 在 `.arb` 之外写中文/英文 hardcoded — 都走 `AppLocalizations.of(context).xxx`
- ❌ `setState()` 调外部数据源 — 用 Provider + ref.read/watch

## 升级与变体

- **加云同步**(后期决定要):在 `lib/data/repositories/cloud/` 加 cloud 实现,改 `repositoryProvider` 根据 `appModeProvider` 切换。无需改 UI 任何一行代码
- **切 BLoC / Provider 状态管理**:不推荐 — 整套 provider 命名约定都要重写。如果团队偏好 BLoC,这个 skill 不是最佳选择
- **加 go_router**:适用于深链多、tab 间复杂跳转的场景。在 `lib/router/` 加路由表,`app.dart` 切到 `MaterialApp.router`
- **加 Flutter Web**:`sqlite3_flutter_libs` 替换为 `drift_web` + `sql.js`,改 `databaseProvider` 实现。其它代码不动
- **加桌面端**:macOS / Linux / Windows 加目标平台,Drift 已经原生支持,其它依赖检查是否支持(home_widget 不支持桌面)
- **多语言扩展**:`lib/l10n/app_<lang>.arb` 加文件,`flutter gen-l10n` 重跑
- **加 AI 能力**:参考 BeeCount 的 `packages/flutter_ai_kit*` 设计 — 把 AI 能力抽到 package,主 app 通过统一接口调用,provider 切换(LocalFirst / CloudFirst 策略)
