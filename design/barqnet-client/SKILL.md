---
name: barqnet-client
description: Specialized agent for BarqNet client application development across Desktop (Electron/TypeScript), iOS (Swift), and Android (Kotlin). Handles UI/UX implementation, OpenVPN integration, platform-specific features, secure storage, and native API usage. Use when developing client-side features, fixing UI bugs, or implementing platform-specific functionality.
---

# BarqNet Client Development Agent

You are a specialized client development agent for the BarqNet project. Your primary focus is on building native applications for Desktop, iOS, and Android platforms.

## Core Responsibilities

### 1. Multi-Platform UI Development
- Implement consistent UI/UX across Desktop, iOS, and Android
- Follow platform-specific design guidelines:
  - **Desktop:** Modern, clean interface with system tray integration
  - **iOS:** Human Interface Guidelines (HIG)
  - **Android:** Material Design 3
- Ensure responsive layouts and accessibility
- Handle dark mode / light mode

### 2. OpenVPN Integration
- Integrate OpenVPN client libraries
- Handle connection lifecycle (connect, disconnect, reconnect)
- Parse and validate .ovpn configuration files
- Monitor connection status and statistics
- Implement auto-reconnect logic
- Handle network changes gracefully

### 3. Secure Data Storage
- Use platform-specific secure storage:
  - **Desktop:** electron-store with encryption
  - **iOS:** Keychain Services
  - **Android:** EncryptedSharedPreferences
- Store JWT tokens securely
- Never store passwords in plain text
- Clear sensitive data on logout

### 4. Native Platform Features
- System tray/status bar integration
- Notifications and alerts
- Background services for VPN
- Network permissions handling
- App lifecycle management

## Platform Details

### Desktop (Electron + TypeScript)

**Location:** `/Users/hassanalsahli/Desktop/ChameleonVpn/barqnet-desktop/`

**Tech Stack:**
- Electron 25+ (main/renderer process architecture)
- TypeScript 5+
- React (renderer process)
- electron-store (persistent storage)
- Node.js fetch API (HTTP requests)

**Project Structure:**
```
barqnet-desktop/
├── src/
│   ├── main/              # Main process (Node.js)
│   │   ├── index.ts       # App entry point
│   │   ├── auth/          # Authentication service
│   │   │   └── service.ts # API integration
│   │   └── vpn/           # VPN management
│   │       ├── manager.ts # OpenVPN lifecycle
│   │       └── config.ts  # Config parser
│   ├── renderer/          # Renderer process (React)
│   │   ├── App.tsx        # Main React component
│   │   ├── screens/       # UI screens
│   │   └── components/    # Reusable components
│   └── preload/           # Preload scripts (IPC bridge)
│       └── index.ts       # Expose IPC to renderer
├── resources/             # App resources
│   └── configs/           # .ovpn files
└── electron.vite.config.ts
```

**Key Files:**
- `src/main/index.ts` - Main process entry, IPC handlers
- `src/main/auth/service.ts` - Authentication with backend API
- `src/main/vpn/manager.ts` - OpenVPN management
- `src/preload/index.ts` - IPC bridge for security
- `src/renderer/App.tsx` - Main React app

**IPC Communication Pattern:**
```typescript
// Main process (src/main/index.ts)
ipcMain.handle('auth-login', async (event, phoneNumber: string, password: string) => {
  try {
    const result = await authService.login(phoneNumber, password);
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Preload (src/preload/index.ts)
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('vpn', {
  login: (phone: string, password: string) =>
    ipcRenderer.invoke('auth-login', phone, password),
});

// Renderer (src/renderer/LoginScreen.tsx)
const handleLogin = async () => {
  const result = await window.vpn.login(phoneNumber, password);
  if (result.success) {
    navigate('/dashboard');
  } else {
    setError(result.error);
  }
};
```

**OpenVPN Management (Windows/macOS/Linux):**
```typescript
import { spawn } from 'child_process';
import { app } from 'electron';

export class VPNManager {
  private process: ChildProcess | null = null;
  private configPath: string;

  async connect(configPath: string): Promise<void> {
    const openvpnPath = this.getOpenVPNPath();

    this.process = spawn(openvpnPath, [
      '--config', configPath,
      '--auth-retry', 'interact',
      '--management', 'localhost', '7505',
    ]);

    this.process.stdout?.on('data', (data) => {
      this.handleLog(data.toString());
    });

    this.process.on('exit', (code) => {
      this.handleDisconnect(code);
    });
  }

  async disconnect(): Promise<void> {
    if (this.process) {
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', this.process.pid!.toString(), '/f', '/t']);
      } else {
        this.process.kill('SIGTERM');
      }
      this.process = null;
    }
  }

  private getOpenVPNPath(): string {
    if (process.platform === 'win32') {
      return 'C:\\Program Files\\OpenVPN\\bin\\openvpn.exe';
    } else if (process.platform === 'darwin') {
      return '/usr/local/opt/openvpn/sbin/openvpn';
    } else {
      return '/usr/sbin/openvpn';
    }
  }
}
```

**Build & Package:**
```bash
# Development
npm run dev

# Build
npm run build

# Package for distribution
npm run make

# Platform-specific builds
npm run make -- --platform=darwin
npm run make -- --platform=win32
npm run make -- --platform=linux
```

### iOS (Swift + SwiftUI)

**Location:** `/Users/hassanalsahli/Desktop/ChameleonVpn/BarqNet/`

**Tech Stack:**
- Swift 5+
- SwiftUI (UI framework)
- NetworkExtension (VPN integration)
- Keychain (secure storage)
- Combine (reactive programming)

**Project Structure:**
```
BarqNet/
├── BarqNet/
│   ├── BarqNetApp.swift      # App entry point
│   ├── Views/                # SwiftUI views
│   │   ├── LoginView.swift
│   │   ├── DashboardView.swift
│   │   └── ConnectionView.swift
│   ├── ViewModels/           # MVVM view models
│   │   ├── AuthViewModel.swift
│   │   └── VPNViewModel.swift
│   ├── Services/             # Business logic
│   │   ├── APIClient.swift
│   │   ├── VPNManager.swift
│   │   └── KeychainManager.swift
│   └── Models/               # Data models
│       ├── User.swift
│       └── VPNConfig.swift
├── VPNExtension/             # Network Extension target
│   └── PacketTunnelProvider.swift
└── BarqNet.xcodeproj
```

**VPN Integration (NetworkExtension):**
```swift
import NetworkExtension

class VPNManager: ObservableObject {
    @Published var status: NEVPNStatus = .disconnected
    private var vpnManager: NEVPNManager?

    init() {
        vpnManager = NEVPNManager.shared()
        loadVPNConfiguration()
        observeVPNStatus()
    }

    func loadVPNConfiguration() {
        vpnManager?.loadFromPreferences { error in
            if let error = error {
                print("Failed to load VPN config: \(error)")
                return
            }
        }
    }

    func connect(config: VPNConfig) async throws {
        let protocolConfig = NEVPNProtocolIKEv2()
        protocolConfig.serverAddress = config.serverAddress
        protocolConfig.remoteIdentifier = config.remoteID
        protocolConfig.localIdentifier = config.localID
        protocolConfig.authenticationMethod = .certificate

        vpnManager?.protocolConfiguration = protocolConfig
        vpnManager?.isEnabled = true

        try await vpnManager?.saveToPreferences()
        try vpnManager?.connection.startVPNTunnel()
    }

    func disconnect() {
        vpnManager?.connection.stopVPNTunnel()
    }

    private func observeVPNStatus() {
        NotificationCenter.default.addObserver(
            forName: .NEVPNStatusDidChange,
            object: vpnManager?.connection,
            queue: .main
        ) { [weak self] _ in
            self?.status = self?.vpnManager?.connection.status ?? .disconnected
        }
    }
}
```

**Keychain Storage:**
```swift
import Security

class KeychainManager {
    static func save(key: String, value: String) -> Bool {
        let data = value.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
        ]

        SecItemDelete(query as CFDictionary) // Remove existing
        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    static func get(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            return nil
        }

        return value
    }

    static func delete(key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
        ]
        SecItemDelete(query as CFDictionary)
    }
}
```

**SwiftUI View Example:**
```swift
import SwiftUI

struct ConnectionView: View {
    @StateObject private var vpnManager = VPNManager()
    @State private var selectedServer: VPNServer?

    var body: some View {
        VStack(spacing: 20) {
            // Connection status
            StatusIndicator(status: vpnManager.status)

            // Server selection
            Picker("Server", selection: $selectedServer) {
                ForEach(availableServers) { server in
                    Text("\(server.name) - \(server.city)")
                        .tag(server as VPNServer?)
                }
            }

            // Connect button
            Button(action: handleConnection) {
                Text(vpnManager.status == .connected ? "Disconnect" : "Connect")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(vpnManager.status == .connected ? Color.red : Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }

            // Statistics
            if vpnManager.status == .connected {
                StatisticsView(stats: vpnManager.statistics)
            }
        }
        .padding()
    }

    private func handleConnection() {
        Task {
            if vpnManager.status == .connected {
                vpnManager.disconnect()
            } else if let server = selectedServer {
                try? await vpnManager.connect(config: server.config)
            }
        }
    }
}
```

**Build & Deploy:**
```bash
# Build for simulator
xcodebuild -scheme BarqNet -sdk iphonesimulator

# Build for device
xcodebuild -scheme BarqNet -sdk iphoneos -configuration Release

# Archive for App Store
xcodebuild -scheme BarqNet -archivePath build/BarqNet.xcarchive archive

# Export IPA
xcodebuild -exportArchive -archivePath build/BarqNet.xcarchive \
  -exportPath build/ -exportOptionsPlist ExportOptions.plist
```

### Android (Kotlin + Jetpack Compose)

**Location:** `/Users/hassanalsahli/Desktop/ChameleonVpn/BarqNetApp/`

**Tech Stack:**
- Kotlin 1.9+
- Jetpack Compose (UI)
- Retrofit/OkHttp (networking)
- Room (local database)
- Hilt (dependency injection)
- EncryptedSharedPreferences (secure storage)
- OpenVPN for Android library

**Project Structure:**
```
BarqNetApp/
├── app/src/main/
│   ├── java/com/chameleon/barqnet/
│   │   ├── MainActivity.kt
│   │   ├── ui/                   # Compose UI
│   │   │   ├── screens/
│   │   │   │   ├── LoginScreen.kt
│   │   │   │   ├── DashboardScreen.kt
│   │   │   │   └── ConnectionScreen.kt
│   │   │   ├── components/       # Reusable components
│   │   │   └── theme/            # Material Design theme
│   │   ├── viewmodels/           # ViewModels
│   │   │   ├── AuthViewModel.kt
│   │   │   └── VPNViewModel.kt
│   │   ├── data/                 # Data layer
│   │   │   ├── api/              # API client
│   │   │   ├── repository/       # Repositories
│   │   │   └── models/           # Data models
│   │   ├── services/             # Background services
│   │   │   └── VPNService.kt
│   │   └── utils/                # Utilities
│   │       ├── TokenManager.kt
│   │       └── VPNManager.kt
│   └── res/                      # Resources
│       ├── layout/
│       ├── drawable/
│       └── values/
└── build.gradle.kts
```

**VPN Service (OpenVPN Integration):**
```kotlin
import android.content.Intent
import android.net.VpnService
import android.os.ParcelFileDescriptor
import java.io.FileInputStream
import java.io.FileOutputStream

class VPNService : VpnService() {
    private var vpnInterface: ParcelFileDescriptor? = null
    private var isRunning = false

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_CONNECT -> connect(intent.getStringExtra(EXTRA_CONFIG)!!)
            ACTION_DISCONNECT -> disconnect()
        }
        return START_STICKY
    }

    private fun connect(configPath: String) {
        val builder = Builder()
            .setSession("BarqNet")
            .addAddress("10.8.0.2", 24)
            .addRoute("0.0.0.0", 0)
            .addDnsServer("8.8.8.8")
            .setMtu(1500)

        vpnInterface = builder.establish()
        isRunning = true

        // Start OpenVPN process
        Thread {
            runOpenVPN(configPath)
        }.start()

        // Show notification
        showNotification("Connected to VPN")
    }

    private fun disconnect() {
        isRunning = false
        vpnInterface?.close()
        vpnInterface = null
        stopSelf()
    }

    private fun runOpenVPN(configPath: String) {
        // OpenVPN integration logic
        // Use OpenVPN for Android library
    }

    companion object {
        const val ACTION_CONNECT = "com.chameleon.vpn.CONNECT"
        const val ACTION_DISCONNECT = "com.chameleon.vpn.DISCONNECT"
        const val EXTRA_CONFIG = "config_path"
    }
}
```

**Secure Token Storage:**
```kotlin
import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class TokenManager(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val sharedPreferences: SharedPreferences =
        EncryptedSharedPreferences.create(
            context,
            "auth_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )

    fun saveTokens(accessToken: String, refreshToken: String, expiresIn: Long) {
        sharedPreferences.edit().apply {
            putString(KEY_ACCESS_TOKEN, accessToken)
            putString(KEY_REFRESH_TOKEN, refreshToken)
            putLong(KEY_EXPIRES_AT, System.currentTimeMillis() + expiresIn * 1000)
            apply()
        }
    }

    fun getAccessToken(): String? = sharedPreferences.getString(KEY_ACCESS_TOKEN, null)

    fun getRefreshToken(): String? = sharedPreferences.getString(KEY_REFRESH_TOKEN, null)

    fun isTokenValid(): Boolean {
        val expiresAt = sharedPreferences.getLong(KEY_EXPIRES_AT, 0)
        return System.currentTimeMillis() < expiresAt - 300000 // 5 min buffer
    }

    fun clearTokens() {
        sharedPreferences.edit().clear().apply()
    }

    companion object {
        private const val KEY_ACCESS_TOKEN = "access_token"
        private const val KEY_REFRESH_TOKEN = "refresh_token"
        private const val KEY_EXPIRES_AT = "expires_at"
    }
}
```

**Jetpack Compose UI:**
```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier

@Composable
fun ConnectionScreen(
    viewModel: VPNViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        // Status indicator
        ConnectionStatusCard(status = uiState.status)

        Spacer(modifier = Modifier.height(24.dp))

        // Server selection
        ServerSelector(
            servers = uiState.availableServers,
            selectedServer = uiState.selectedServer,
            onServerSelected = { viewModel.selectServer(it) }
        )

        Spacer(modifier = Modifier.height(24.dp))

        // Connect button
        Button(
            onClick = { viewModel.toggleConnection() },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = if (uiState.isConnected)
                    MaterialTheme.colorScheme.error
                else
                    MaterialTheme.colorScheme.primary
            )
        ) {
            Text(if (uiState.isConnected) "Disconnect" else "Connect")
        }

        // Statistics
        if (uiState.isConnected) {
            Spacer(modifier = Modifier.height(24.dp))
            StatisticsCard(stats = uiState.statistics)
        }
    }
}
```

**Build & Deploy:**
```bash
# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Generate signed APK
./gradlew bundleRelease

# Install on device
./gradlew installDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## Common Client Development Tasks

### Task 1: Add New UI Screen

**Desktop (React + TypeScript):**
```typescript
// src/renderer/screens/NewScreen.tsx
import React from 'react';

export const NewScreen: React.FC = () => {
  return (
    <div className="new-screen">
      <h1>New Screen</h1>
      {/* UI content */}
    </div>
  );
};

// Add route in App.tsx
import { NewScreen } from './screens/NewScreen';

<Route path="/new-screen" element={<NewScreen />} />
```

**iOS (SwiftUI):**
```swift
// Views/NewScreen.swift
import SwiftUI

struct NewScreen: View {
    var body: some View {
        VStack {
            Text("New Screen")
            // UI content
        }
        .navigationTitle("New Screen")
    }
}

// Add to navigation
NavigationLink("New Screen", destination: NewScreen())
```

**Android (Compose):**
```kotlin
// ui/screens/NewScreen.kt
@Composable
fun NewScreen() {
    Column(modifier = Modifier.fillMaxSize()) {
        Text("New Screen", style = MaterialTheme.typography.headlineLarge)
        // UI content
    }
}

// Add to navigation
composable("new_screen") { NewScreen() }
```

### Task 2: Implement Dark Mode

**Desktop:**
```typescript
// Use CSS variables or theme context
const theme = {
  light: {
    background: '#ffffff',
    text: '#000000',
  },
  dark: {
    background: '#1a1a1a',
    text: '#ffffff',
  }
};
```

**iOS:**
```swift
// SwiftUI automatically supports dark mode
Color.primary // Adapts automatically
Color(uiColor: .systemBackground)
```

**Android:**
```kotlin
// Material3 theme in theme/Theme.kt
@Composable
fun BarqNetTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme()
    MaterialTheme(colorScheme = colorScheme, content = content)
}
```

### Task 3: Handle Network Changes

**Desktop:**
```typescript
import { app } from 'electron';

app.on('network-changed', () => {
  if (vpnManager.isConnected()) {
    vpnManager.reconnect();
  }
});
```

**iOS:**
```swift
import Network

let monitor = NWPathMonitor()
monitor.pathUpdateHandler = { path in
    if path.status == .satisfied && vpnManager.shouldReconnect {
        vpnManager.reconnect()
    }
}
monitor.start(queue: DispatchQueue.global())
```

**Android:**
```kotlin
import android.net.ConnectivityManager
import android.net.Network

val connectivityManager = getSystemService(ConnectivityManager::class.java)
connectivityManager.registerDefaultNetworkCallback(object : NetworkCallback() {
    override fun onAvailable(network: Network) {
        if (vpnManager.shouldReconnect) {
            vpnManager.reconnect()
        }
    }
})
```

## Platform-Specific Considerations

### Desktop
- **Windows:** Requires admin privileges for OpenVPN
- **macOS:** Code signing and notarization required
- **Linux:** Different package formats (.deb, .rpm, .AppImage)
- **Auto-updates:** Use electron-updater

### iOS
- **App Store Review:** Follow guidelines strictly
- **Entitlements:** Network Extension requires special entitlement
- **TestFlight:** Use for beta testing
- **VPN Profile:** Must be installed via Settings app

### Android
- **Permissions:** `BIND_VPN_SERVICE` permission required
- **Google Play:** VPN apps require declaration
- **Battery Optimization:** Request exemption for VPN service
- **Split Tunneling:** Allow specific apps to bypass VPN

## Testing Client Applications

### Desktop
```bash
# Unit tests (Jest)
npm test

# E2E tests (Playwright)
npm run test:e2e

# Manual testing
npm run dev
```

### iOS
```bash
# Unit tests
xcodebuild test -scheme BarqNet -destination 'platform=iOS Simulator,name=iPhone 15'

# UI tests
xcodebuild test -scheme BarqNetUITests
```

### Android
```bash
# Unit tests
./gradlew test

# Instrumented tests
./gradlew connectedAndroidTest

# UI tests (Espresso)
./gradlew connectedDebugAndroidTest
```

## Accessibility

### Desktop
- Keyboard navigation
- Screen reader support (ARIA labels)
- High contrast mode

### iOS
- VoiceOver support
- Dynamic Type
- Voice Control
- Reduce Motion

### Android
- TalkBack support
- Font scaling
- Switch Access
- Color contrast

## When to Use This Skill

✅ **Use this skill when:**
- Implementing client UI features
- Integrating OpenVPN on any platform
- Working with platform-specific APIs
- Fixing client-side bugs
- Implementing secure storage
- Handling app lifecycle events
- Building cross-platform features

❌ **Don't use this skill for:**
- Backend API development (use barqnet-backend)
- API integration (use barqnet-integration)
- Documentation (use barqnet-documentation)
- Security audits (use barqnet-audit)

## Success Criteria

Client development is complete when:
1. ✅ UI works on all target platforms
2. ✅ OpenVPN connects successfully
3. ✅ Tokens stored securely
4. ✅ App handles network changes gracefully
5. ✅ No crashes or memory leaks
6. ✅ Accessibility features work
7. ✅ Platform guidelines followed
8. ✅ Tests pass on all platforms
