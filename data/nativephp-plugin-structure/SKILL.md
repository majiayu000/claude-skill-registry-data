---
name: NativePHP Plugin Structure
description: This skill explains NativePHP plugin structure and configuration. Use when the user asks about "plugin structure", "nativephp.json", "plugin manifest", "composer.json setup", "service provider", "facade", "plugin directory layout", "bridge_functions array", "plugin permissions", "plugin dependencies", "plugin repositories", "custom maven repository", "plugin secrets", "environment variables", "placeholder substitution", "plugin hooks", "copy_assets", "features", "uses-feature", "meta_data", "background_modes", "entitlements", or how to organize a NativePHP plugin package.
version: 1.0.3
---

# NativePHP Plugin Structure

NativePHP plugins are Composer packages that extend NativePHP with native iOS/Android functionality. This skill covers the complete plugin structure.

## Directory Layout

```
my-plugin/
├── composer.json                     # Composer package definition
├── nativephp.json                    # Plugin manifest (REQUIRED)
├── README.md                         # Plugin documentation
├── .gitignore
├── src/
│   ├── MyPluginServiceProvider.php   # Laravel service provider
│   ├── MyPlugin.php                  # Main API class
│   ├── Facades/
│   │   └── MyPlugin.php              # Laravel facade
│   ├── Events/                       # Events dispatched from native
│   │   └── MyPluginCompleted.php
│   └── Commands/
│       └── CopyAssetsCommand.php     # Lifecycle hook commands
├── resources/
│   ├── android/
│   │   └── MyPluginFunctions.kt      # Kotlin bridge functions
│   ├── ios/
│   │   └── MyPluginFunctions.swift   # Swift bridge functions
│   ├── js/
│   │   └── myPlugin.js               # JavaScript bridge module
│   └── boost/
│       └── guidelines/
│           └── core.blade.php        # Boost AI guidelines
└── tests/
    ├── Pest.php
    └── PluginTest.php                # Plugin validation tests
```

## composer.json

The Composer manifest must declare the package type as `nativephp-plugin`:

```json
{
    "name": "vendor/my-plugin",
    "description": "A NativePHP plugin that does something awesome",
    "type": "nativephp-plugin",
    "license": "MIT",
    "require": {
        "php": "^8.1",
        "nativephp/mobile": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "Vendor\\MyPlugin\\": "src/"
        }
    },
    "extra": {
        "laravel": {
            "providers": [
                "Vendor\\MyPlugin\\MyPluginServiceProvider"
            ],
            "aliases": {
                "MyPlugin": "Vendor\\MyPlugin\\Facades\\MyPlugin"
            }
        }
    }
}
```

### Critical Fields

| Field | Requirement |
|-------|-------------|
| `type` | MUST be `"nativephp-plugin"` |
| `require.nativephp/mobile` | Required dependency |
| `extra.laravel.providers` | Auto-register service provider |
| `extra.laravel.aliases` | Auto-register facade |

## nativephp.json - The Plugin Manifest

This is the **most important file** in a NativePHP plugin. It tells NativePHP what native functionality the plugin provides.

**Important**: Package metadata (`name`, `version`, `description`, `service_provider`) comes from `composer.json` — don't duplicate it here. The manifest only contains native-specific configuration.

### Complete Template

```json
{
    "namespace": "MyPlugin",

    "bridge_functions": [
        {
            "name": "MyPlugin.Execute",
            "android": "com.myvendor.plugins.myplugin.MyPluginFunctions.Execute",
            "ios": "MyPluginFunctions.Execute",
            "description": "Executes the main plugin action"
        },
        {
            "name": "MyPlugin.GetStatus",
            "android": "com.myvendor.plugins.myplugin.MyPluginFunctions.GetStatus",
            "ios": "MyPluginFunctions.GetStatus",
            "description": "Gets the current status"
        }
    ],

    "android": {
        "permissions": [
            "android.permission.CAMERA",
            "android.permission.VIBRATE"
        ],
        "dependencies": {
            "implementation": [
                "com.google.mlkit:barcode-scanning:17.2.0",
                "androidx.camera:camera-core:1.3.0"
            ]
        },
        "activities": [
            {
                "name": ".ScannerActivity",
                "theme": "@style/Theme.AppCompat.NoActionBar",
                "screenOrientation": "portrait",
                "exported": false
            }
        ],
        "services": [],
        "receivers": [],
        "providers": []
    },

    "ios": {
        "info_plist": {
            "NSCameraUsageDescription": "This plugin needs camera access to scan barcodes"
        },
        "dependencies": {
            "swift_packages": [
                {
                    "url": "https://github.com/example/package.git",
                    "version": "1.0.0"
                }
            ],
            "pods": [
                "TensorFlowLiteSwift"
            ]
        }
    },

    "assets": {
        "android": {
            "model.tflite": "assets/model.tflite"
        },
        "ios": {
            "model.mlmodel": "Resources/model.mlmodel"
        }
    },

    "events": [
        "Vendor\\MyPlugin\\Events\\SomethingHappened",
        "Vendor\\MyPlugin\\Events\\OperationCompleted"
    ],

    "hooks": {
        "copy_assets": "nativephp:my-plugin:copy-assets"
    }
}
```

### Manifest Sections Explained

#### bridge_functions

Maps PHP method calls to native implementations:

```json
"bridge_functions": [
    {
        "name": "MyPlugin.Execute",
        "android": "com.myvendor.plugins.myplugin.MyPluginFunctions.Execute",
        "ios": "MyPluginFunctions.Execute",
        "description": "What this function does"
    }
]
```

- `name`: The method name used in `nativephp_call('MyPlugin.Execute', [])`
- `android`: Full Kotlin class path (package + class name)
- `ios`: Swift class path (just the class names, enum.class format)
- `description`: Documentation for the function

**Naming convention**: `Namespace.Action` (e.g., `Camera.Capture`, `Haptics.Vibrate`)

#### android section

All Android-specific configuration goes under the `android` key:

```json
"android": {
    "permissions": [
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
        "android.permission.VIBRATE"
    ],
    "features": [
        {"name": "android.hardware.camera", "required": true},
        {"name": "android.hardware.camera.autofocus", "required": false}
    ],
    "repositories": [
        {
            "url": "https://api.mapbox.com/downloads/v2/releases/maven"
        }
    ],
    "dependencies": {
        "implementation": [
            "com.google.mlkit:barcode-scanning:17.2.0",
            "androidx.camera:camera-camera2:1.3.0"
        ]
    },
    "meta_data": [
        {
            "name": "com.google.android.geo.API_KEY",
            "value": "${GOOGLE_MAPS_API_KEY}"
        }
    ],
    "activities": [...],
    "services": [...],
    "receivers": [...],
    "providers": [...]
}
```

**permissions**: Array of Android permission strings
**features**: Hardware/software feature declarations (uses-feature)
**repositories**: Custom Maven repositories (see below)
**dependencies**: Gradle dependency strings (implementation, api, compileOnly, runtimeOnly)
**meta_data**: Application-level meta-data entries for SDK configuration
**activities/services/receivers/providers**: AndroidManifest.xml components

#### repositories (Custom Maven Repositories)

For SDKs not available on Maven Central or Google Maven (like Mapbox), add custom repositories:

```json
"android": {
    "repositories": [
        {
            "url": "https://api.mapbox.com/downloads/v2/releases/maven"
        }
    ]
}
```

For private repositories that require authentication:

```json
"android": {
    "repositories": [
        {
            "url": "https://private.maven.example.com/releases",
            "credentials": {
                "username": "user",
                "password": "${PRIVATE_SDK_TOKEN}"
            }
        }
    ]
}
```

The `${VAR}` syntax references environment variables from the user's `.env` file.

#### ios section

All iOS-specific configuration goes under the `ios` key:

```json
"ios": {
    "info_plist": {
        "NSCameraUsageDescription": "Explain why camera is needed",
        "NSMicrophoneUsageDescription": "Explain why microphone is needed",
        "MBXAccessToken": "${MAPBOX_ACCESS_TOKEN}"
    },
    "dependencies": {
        "swift_packages": [
            {
                "url": "https://github.com/example/package.git",
                "version": "1.0.0"
            }
        ],
        "pods": [
            {"name": "TensorFlowLiteSwift", "version": "~> 2.0"}
        ]
    },
    "background_modes": ["audio", "fetch", "processing"],
    "entitlements": {
        "com.apple.developer.maps": true,
        "com.apple.security.application-groups": ["group.com.example.shared"]
    }
}
```

**info_plist**: Object mapping Info.plist keys to values (permissions, API tokens, config)
**dependencies**: Swift Package URLs with versions, or CocoaPods names
**background_modes**: UIBackgroundModes values (audio, fetch, processing, location, remote-notification, bluetooth-central, bluetooth-peripheral)
**entitlements**: App entitlements for capabilities (Maps, App Groups, HealthKit, iCloud, etc.)
**init_function**: Swift function to call during plugin initialization (see below)

Use `${ENV_VAR}` placeholders for sensitive values like API tokens.

#### init_function (iOS/Android)

Plugins can specify an initialization function that runs during app startup. This is essential for plugins that need to:
- Initialize SDK singletons (Firebase, etc.)
- Register for lifecycle events via `NativePHPPluginRegistry`
- Subscribe to `NotificationCenter` events
- Set up delegates before bridge functions are called

**iOS:**
```json
"ios": {
    "init_function": "NativePHPMyPluginInit"
}
```

The function must be a `@_cdecl` exported C function in your Swift code:

```swift
@_cdecl("NativePHPMyPluginInit")
public func NativePHPMyPluginInit() {
    // Initialize singletons
    _ = MyPluginManager.shared
    _ = MyPluginDelegate.shared
    print("MyPlugin initialized")
}
```

**Android:**
```json
"android": {
    "init_function": "com.myvendor.plugins.myplugin.MyPluginInit"
}
```

The function must be a top-level function or object method in Kotlin:

```kotlin
fun MyPluginInit() {
    // Initialize singletons, subscribe to lifecycle events
    MyPluginDelegate.initialize()
}
```

**When to use init_function:**
- Your plugin has SDK singletons that must be created early
- You need to subscribe to `NativePHPLifecycle` events (Android) or `NotificationCenter` (iOS)
- You need to register with `NativePHPPluginRegistry` for `onAppLaunch` callbacks
- Your bridge functions depend on state that must be set up first

#### background_modes (iOS)

Enable background execution capabilities:

```json
"ios": {
    "background_modes": ["audio", "fetch", "processing", "location"]
}
```

Common values:
- `audio` — Audio playback or recording
- `fetch` — Background fetch
- `processing` — Background processing tasks
- `location` — Location updates
- `remote-notification` — Push notification processing
- `bluetooth-central` — Bluetooth LE central mode
- `bluetooth-peripheral` — Bluetooth LE peripheral mode

These are merged into `UIBackgroundModes` in Info.plist.

#### entitlements (iOS)

Configure app entitlements for capabilities:

```json
"ios": {
    "entitlements": {
        "com.apple.developer.maps": true,
        "com.apple.security.application-groups": ["group.com.example.shared"],
        "com.apple.developer.associated-domains": ["applinks:example.com"],
        "com.apple.developer.healthkit": true
    }
}
```

Values can be:
- **Boolean** — `true`/`false` for simple capabilities
- **Array** — For capabilities requiring multiple values (App Groups, Associated Domains)
- **String** — For single-value entitlements

Entitlements are written to `NativePHP.entitlements`. If the file doesn't exist, it's created automatically.

#### secrets (Environment Variables)

Plugins can declare required environment variables that users must provide in their `.env` file:

```json
"secrets": {
    "MAPBOX_ACCESS_TOKEN": {
        "description": "Public access token for Mapbox SDK (starts with pk.)",
        "required": true
    },
    "MY_API_KEY": {
        "description": "API key for the service",
        "required": false
    }
}
```

**Build-time validation**: If a required secret is missing, the build fails with a helpful error message telling the user which secrets to add to their `.env` file.

**Usage in manifest**: Reference secrets using `${VAR}` syntax in repositories, credentials, or assets:
- `"password": "${PRIVATE_SDK_TOKEN}"` in repository credentials
- `${MAPBOX_ACCESS_TOKEN}` in asset files (see below)

#### assets section

Static assets to copy during build are defined at the top level:

```json
"assets": {
    "android": {
        "android/res/values/mapbox_token.xml": "res/values/mapbox_token.xml"
    },
    "ios": {
        "model.mlmodel": "Resources/model.mlmodel"
    }
}
```

**Placeholder substitution**: Asset files can contain `${VAR}` placeholders that are automatically replaced with values from the user's `.env` file during the build.

Example XML asset template (`resources/android/res/values/mapbox_token.xml`):
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <string name="mapbox_access_token" translatable="false"
            tools:ignore="UnusedResources">${MAPBOX_ACCESS_TOKEN}</string>
</resources>
```

Supported file types for substitution: xml, json, txt, plist, strings, html, js, css, kt, swift, java

Use `assets` for small static files. Use the `copy_assets` hook for large files, ML models, or files that need processing.

#### events

Events that native code dispatches to PHP:

```json
"events": [
    "Vendor\\MyPlugin\\Events\\ScanCompleted",
    "Vendor\\MyPlugin\\Events\\OperationFailed"
]
```

These are the fully-qualified PHP class names. Livewire components listen with:
```php
#[On('native:Vendor\MyPlugin\Events\ScanCompleted')]
```

#### hooks

Lifecycle hooks for build-time operations:

```json
"hooks": {
    "copy_assets": "nativephp:my-plugin:copy-assets",
    "pre_compile": "nativephp:my-plugin:pre-compile",
    "post_compile": "nativephp:my-plugin:post-compile",
    "post_build": "nativephp:my-plugin:post-build"
}
```

Each hook is an Artisan command signature.

#### Android Manifest Components

Android activities, services, receivers, and providers are defined under `android`:

```json
"android": {
    "activities": [
        {
            "name": ".MyActivity",
            "theme": "@style/Theme.AppCompat.NoActionBar",
            "screenOrientation": "portrait",
            "exported": false,
            "launchMode": "singleTask",
            "configChanges": "orientation|screenSize",
            "intent-filters": [...]
        }
    ],
    "services": [
        {
            "name": ".MyService",
            "exported": false,
            "foregroundServiceType": "camera"
        }
    ],
    "receivers": [
        {
            "name": ".MyBroadcastReceiver",
            "exported": true,
            "intent-filters": [
                {
                    "action": ["android.intent.action.BOOT_COMPLETED"]
                }
            ]
        }
    ],
    "providers": []
}
```

**Name resolution**: Names starting with `.` are resolved from your plugin's package declaration (e.g., `.MyActivity` becomes `com.myvendor.plugins.myplugin.MyActivity` if your Kotlin files declare `package com.myvendor.plugins.myplugin`)

## Service Provider

The service provider registers your plugin with Laravel:

```php
<?php

namespace Vendor\MyPlugin;

use Illuminate\Support\ServiceProvider;

class MyPluginServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(MyPlugin::class, function ($app) {
            return new MyPlugin();
        });
    }

    public function boot(): void
    {
        // Register Artisan commands
        if ($this->app->runningInConsole()) {
            $this->commands([
                Commands\CopyAssetsCommand::class,
            ]);
        }

        // Publish config (optional)
        $this->publishes([
            __DIR__.'/../config/my-plugin.php' => config_path('my-plugin.php'),
        ], 'my-plugin-config');
    }
}
```

## Facade

Provides a clean API for users:

```php
<?php

namespace Vendor\MyPlugin\Facades;

use Illuminate\Support\Facades\Facade;

/**
 * @method static array execute(string $param)
 * @method static array getStatus()
 *
 * @see \Vendor\MyPlugin\MyPlugin
 */
class MyPlugin extends Facade
{
    protected static function getFacadeAccessor(): string
    {
        return \Vendor\MyPlugin\MyPlugin::class;
    }
}
```

## Main API Class

The implementation that calls native code:

```php
<?php

namespace Vendor\MyPlugin;

class MyPlugin
{
    public function execute(string $param): void
    {
        if (function_exists('nativephp_call')) {
            nativephp_call('MyPlugin.Execute', json_encode([
                'param' => $param,
            ]));
        }
    }

    public function getStatus(): void
    {
        if (function_exists('nativephp_call')) {
            nativephp_call('MyPlugin.GetStatus', '{}');
        }
    }
}
```

## Event Classes

Simple POJOs for native-to-PHP events:

```php
<?php

namespace Vendor\MyPlugin\Events;

use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class ScanCompleted
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public string $result,
        public string $format,
        public ?string $id = null
    ) {}
}
```

**Important**: Events do NOT use `ShouldBroadcast` or broadcasting channels. They're dispatched via JavaScript injection.

## Lifecycle Hook Commands

For build-time operations like copying ML models:

```php
<?php

namespace Vendor\MyPlugin\Commands;

use Native\Mobile\Commands\NativePluginHookCommand;

class CopyAssetsCommand extends NativePluginHookCommand
{
    protected $signature = 'nativephp:my-plugin:copy-assets';
    protected $description = 'Copy plugin assets to native projects';

    public function handle(): int
    {
        if ($this->isAndroid()) {
            $this->copyToAndroidAssets(
                'model.tflite',
                'model.tflite'
            );
        }

        if ($this->isIos()) {
            $this->copyToIosBundle(
                'model.mlmodel',
                'model.mlmodel'
            );
        }

        return self::SUCCESS;
    }
}
```

### Available Hook Methods

| Method | Purpose |
|--------|---------|
| `$this->isAndroid()` | Check if building for Android |
| `$this->isIos()` | Check if building for iOS |
| `$this->copyToAndroidAssets($src, $dest)` | Copy to Android assets |
| `$this->copyToIosBundle($src, $dest)` | Copy to iOS bundle |

## Native Code Location

### Android (Kotlin)

Place Kotlin files directly in `resources/android/`:

```
resources/android/
└── MyPluginFunctions.kt
```

Or with subdirectories for additional files:
```
resources/android/
├── MyPluginFunctions.kt
└── activities/
    └── ScannerActivity.kt
```

**Package naming**: Use `com.{vendor}.plugins.{pluginname}` format:
```kotlin
package com.myvendor.plugins.myplugin
```

**Note**: The nested `resources/android/src/` structure is also supported for backward compatibility.

### iOS (Swift)

Place Swift files directly in `resources/ios/`:

```
resources/ios/
└── MyPluginFunctions.swift
```

Or with subdirectories for additional files:
```
resources/ios/
├── MyPluginFunctions.swift
└── ViewControllers/
    └── ScannerViewController.swift
```

**Note**: The nested `resources/ios/Sources/` structure is also supported for backward compatibility.

## Registering with the App

After creating your plugin, users must install and explicitly register it.

### Step 1: Install the Plugin

```bash
composer require vendor/my-plugin
```

For local development, add a path repository to `composer.json`:

```json
{
    "repositories": [
        {
            "type": "path",
            "url": "./packages/my-plugin"
        }
    ]
}
```

### Step 2: Publish the Plugins Provider (First Time Only)

```bash
php artisan vendor:publish --tag=nativephp-plugins-provider
```

This creates `app/Providers/NativePluginsServiceProvider.php`.

### Step 3: Register the Plugin

```bash
php artisan native:plugin:register vendor/my-plugin
```

This automatically adds the plugin's service provider to your `plugins()` array:

```php
public function plugins(): array
{
    return [
        \Vendor\MyPlugin\MyPluginServiceProvider::class,
    ];
}
```

### Step 4: Verify Registration

```bash
# Show registered plugins
php artisan native:plugin:list

# Show all installed plugins (including unregistered)
php artisan native:plugin:list --all
```

### Why Explicit Registration?

This is a security measure. It prevents transitive dependencies from automatically registering plugins without user consent. Only plugins explicitly listed in the provider are compiled into native builds.

### Removing a Plugin

To unregister a plugin from the app (but keep it installed):
```bash
php artisan native:plugin:register vendor/my-plugin --remove
```

To completely uninstall a plugin (unregister + remove code + composer remove):
```bash
php artisan native:plugin:uninstall vendor/my-plugin
```

### What Happens After Registration

Once registered, NativePHP automatically:
1. Discovers the `nativephp-plugin` type
2. Reads `nativephp.json`
3. Registers bridge functions
4. Adds permissions to native projects
5. Includes dependencies in builds
6. Runs lifecycle hooks

## Best Practices

1. **Use descriptive namespaces**: `MyPlugin.Scan` not `M.S`
2. **Document all bridge functions**: Users need to know what each does
3. **Request minimal permissions**: Only what's actually needed
4. **Handle errors gracefully**: Return meaningful error messages
5. **Test on real devices**: Emulators don't always match real behavior
6. **Version your manifest**: Update version when making changes