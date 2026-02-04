---
name: .claude/skills/electron-distribution/SKILL.md
description: |
  Electronアプリケーションの配布・自動更新専門知識

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/electron-distribution/resources/auto-update.md`: 自動更新実装詳細
  - `.claude/skills/electron-distribution/resources/release-channels.md`: リリースチャネル管理
  - `.claude/skills/electron-distribution/resources/store-distribution.md`: ストア配布ガイド
  - `.claude/skills/electron-distribution/templates/update-server.ts`: 更新サーバーテンプレート
  - `.claude/skills/electron-distribution/scripts/release.sh`: リリーススクリプト

  専門分野:
  - 自動更新: electron-updater設定
  - リリース管理: バージョニング、チャネル
  - ストア配布: Mac App Store、Microsoft Store
  - アップデートサーバー: 自前・GitHub Releases

  使用タイミング:
  - 自動更新機能を実装する時
  - リリースフローを構築する時
  - アプリストアに配布する時
  - 更新サーバーを設定する時

version: 1.0.0
---

# .claude/skills/electron-distribution/SKILL.md

Electronアプリケーションの配布・自動更新専門知識

---

## 概要

### 目的

Electronアプリケーションを効率的に配布し、
シームレスな自動更新を提供する。

### 対象者

- Electronアプリ開発者
- DevOpsエンジニア
- リリースマネージャー

---

## 配布方法の選択

### 配布チャネル比較

| 方法                | メリット           | デメリット   | 推奨ケース       |
| ------------------- | ------------------ | ------------ | ---------------- |
| **GitHub Releases** | 無料、簡単         | 帯域制限あり | OSS、小規模      |
| **S3/CloudFront**   | 高速、スケーラブル | コスト       | 中〜大規模       |
| **Mac App Store**   | 信頼性、発見性     | 審査、制約   | macOSメイン      |
| **Microsoft Store** | 信頼性、自動更新   | 審査         | Windowsメイン    |
| **自前サーバー**    | 完全制御           | 運用負荷     | エンタープライズ |

---

## 自動更新（electron-updater）

### 基本設定

```yaml
# electron-builder.yml
publish:
  - provider: github
    owner: your-username
    repo: your-repo
    releaseType: release
```

### 更新サービス実装

```typescript
// main/services/updater.ts
import { autoUpdater, UpdateInfo } from "electron-updater";
import { app, BrowserWindow, dialog } from "electron";
import log from "electron-log";

// ログ設定
autoUpdater.logger = log;
log.transports.file.level = "info";

// 更新チェック設定
autoUpdater.autoDownload = false;
autoUpdater.autoInstallOnAppQuit = true;

export class UpdateService {
  private mainWindow: BrowserWindow | null = null;

  constructor(win: BrowserWindow) {
    this.mainWindow = win;
    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    // 更新確認中
    autoUpdater.on("checking-for-update", () => {
      this.sendToRenderer("update-status", { status: "checking" });
    });

    // 更新あり
    autoUpdater.on("update-available", (info: UpdateInfo) => {
      this.sendToRenderer("update-status", {
        status: "available",
        version: info.version,
        releaseNotes: info.releaseNotes,
      });

      // ユーザーに確認
      dialog
        .showMessageBox(this.mainWindow!, {
          type: "info",
          title: "更新があります",
          message: `バージョン ${info.version} が利用可能です。ダウンロードしますか？`,
          buttons: ["後で", "ダウンロード"],
          defaultId: 1,
        })
        .then(({ response }) => {
          if (response === 1) {
            autoUpdater.downloadUpdate();
          }
        });
    });

    // 更新なし
    autoUpdater.on("update-not-available", () => {
      this.sendToRenderer("update-status", { status: "up-to-date" });
    });

    // ダウンロード進捗
    autoUpdater.on("download-progress", (progress) => {
      this.sendToRenderer("update-progress", {
        percent: progress.percent,
        bytesPerSecond: progress.bytesPerSecond,
        total: progress.total,
        transferred: progress.transferred,
      });
    });

    // ダウンロード完了
    autoUpdater.on("update-downloaded", (info: UpdateInfo) => {
      this.sendToRenderer("update-status", {
        status: "downloaded",
        version: info.version,
      });

      dialog
        .showMessageBox(this.mainWindow!, {
          type: "info",
          title: "更新の準備完了",
          message: "更新をインストールするにはアプリを再起動してください。",
          buttons: ["後で", "今すぐ再起動"],
          defaultId: 1,
        })
        .then(({ response }) => {
          if (response === 1) {
            autoUpdater.quitAndInstall(false, true);
          }
        });
    });

    // エラー
    autoUpdater.on("error", (error) => {
      log.error("Update error:", error);
      this.sendToRenderer("update-status", {
        status: "error",
        message: error.message,
      });
    });
  }

  private sendToRenderer(channel: string, data: unknown): void {
    this.mainWindow?.webContents.send(channel, data);
  }

  // 手動更新チェック
  async checkForUpdates(): Promise<void> {
    try {
      await autoUpdater.checkForUpdates();
    } catch (error) {
      log.error("Check for updates failed:", error);
    }
  }

  // ダウンロード開始
  downloadUpdate(): void {
    autoUpdater.downloadUpdate();
  }

  // インストール
  quitAndInstall(): void {
    autoUpdater.quitAndInstall(false, true);
  }
}

// メインプロセスで初期化
app.whenReady().then(() => {
  const mainWindow = createMainWindow();
  const updateService = new UpdateService(mainWindow);

  // 起動時に更新チェック（遅延）
  setTimeout(() => {
    updateService.checkForUpdates();
  }, 3000);

  // IPC登録
  ipcMain.handle("update:check", () => updateService.checkForUpdates());
  ipcMain.handle("update:download", () => updateService.downloadUpdate());
  ipcMain.handle("update:install", () => updateService.quitAndInstall());
});
```

### Renderer側UI

```tsx
// renderer/components/UpdateNotification.tsx
import { useEffect, useState } from "react";

interface UpdateStatus {
  status:
    | "checking"
    | "available"
    | "downloading"
    | "downloaded"
    | "up-to-date"
    | "error";
  version?: string;
  message?: string;
}

interface UpdateProgress {
  percent: number;
  bytesPerSecond: number;
  total: number;
  transferred: number;
}

export function UpdateNotification() {
  const [status, setStatus] = useState<UpdateStatus | null>(null);
  const [progress, setProgress] = useState<UpdateProgress | null>(null);

  useEffect(() => {
    const cleanupStatus = window.electronAPI.onUpdateStatus(setStatus);
    const cleanupProgress = window.electronAPI.onUpdateProgress(setProgress);

    return () => {
      cleanupStatus();
      cleanupProgress();
    };
  }, []);

  if (!status || status.status === "up-to-date") {
    return null;
  }

  return (
    <div className="update-notification">
      {status.status === "checking" && <p>更新を確認中...</p>}

      {status.status === "available" && (
        <div>
          <p>バージョン {status.version} が利用可能です</p>
          <button onClick={() => window.electronAPI.downloadUpdate()}>
            ダウンロード
          </button>
        </div>
      )}

      {status.status === "downloading" && progress && (
        <div>
          <p>ダウンロード中: {Math.round(progress.percent)}%</p>
          <progress value={progress.percent} max={100} />
        </div>
      )}

      {status.status === "downloaded" && (
        <div>
          <p>更新の準備完了</p>
          <button onClick={() => window.electronAPI.installUpdate()}>
            再起動してインストール
          </button>
        </div>
      )}

      {status.status === "error" && (
        <p className="error">更新エラー: {status.message}</p>
      )}
    </div>
  );
}
```

---

## リリースチャネル

### チャネル設定

```yaml
# electron-builder.yml
publish:
  - provider: github
    owner: your-username
    repo: your-repo
    channel: ${channel}
```

```typescript
// main/services/updater.ts
// チャネル設定
function setUpdateChannel(channel: "stable" | "beta" | "alpha"): void {
  autoUpdater.channel = channel;
  autoUpdater.allowPrerelease = channel !== "stable";
  autoUpdater.allowDowngrade = false;
}

// ユーザー設定から読み込み
const userSettings = store.get("updateChannel", "stable");
setUpdateChannel(userSettings);
```

### バージョニング戦略

```
# Semantic Versioning
stable:  1.0.0, 1.0.1, 1.1.0, 2.0.0
beta:    1.1.0-beta.1, 1.1.0-beta.2
alpha:   1.1.0-alpha.1, 2.0.0-alpha.1

# package.json
{
  "version": "1.1.0-beta.1"
}
```

---

## GitHub Releases配布

### electron-builder.yml

```yaml
publish:
  - provider: github
    owner: your-org
    repo: your-app
    releaseType: release # or draft, prerelease
    private: false
```

### リリースワークフロー

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    strategy:
      matrix:
        include:
          - os: macos-latest
            platform: mac
          - os: windows-latest
            platform: win
          - os: ubuntu-latest
            platform: linux

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - run: npm ci
      - run: npm run build

      - name: Publish
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # macOS署名
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_ID_PASSWORD: ${{ secrets.APPLE_ID_PASSWORD }}
          CSC_LINK: ${{ secrets.MAC_CERTS }}
          CSC_KEY_PASSWORD: ${{ secrets.MAC_CERTS_PASSWORD }}
          # Windows署名
          WIN_CERT_FILE: ${{ secrets.WIN_CERT_FILE }}
          WIN_CERT_PASSWORD: ${{ secrets.WIN_CERT_PASSWORD }}
        run: npm run publish -- --${{ matrix.platform }}
```

---

## S3/CloudFront配布

### 設定

```yaml
# electron-builder.yml
publish:
  - provider: s3
    bucket: your-app-releases
    region: us-east-1
    acl: public-read
    path: /releases/${os}/${arch}
```

### CloudFront設定（Terraform例）

```hcl
resource "aws_cloudfront_distribution" "releases" {
  origin {
    domain_name = aws_s3_bucket.releases.bucket_regional_domain_name
    origin_id   = "S3-releases"
  }

  enabled = true

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-releases"
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

### カスタム更新サーバー

```typescript
// update-server/server.ts
import express from "express";
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

const app = express();
const s3 = new S3Client({ region: "us-east-1" });

// 更新情報エンドポイント
app.get("/update/:platform/:version", async (req, res) => {
  const { platform, version } = req.params;

  try {
    // 最新バージョン取得
    const latestVersion = await getLatestVersion(platform);

    if (compareVersions(latestVersion, version) > 0) {
      res.json({
        version: latestVersion,
        files: await getDownloadUrls(platform, latestVersion),
        releaseDate: await getReleaseDate(latestVersion),
        releaseNotes: await getReleaseNotes(latestVersion),
      });
    } else {
      res.status(204).send();
    }
  } catch (error) {
    res.status(500).json({ error: "Failed to check updates" });
  }
});

// ダウンロードエンドポイント
app.get("/download/:platform/:version/:file", async (req, res) => {
  const { platform, version, file } = req.params;

  // 署名付きURL生成
  const signedUrl = await generateSignedUrl(
    `releases/${platform}/${version}/${file}`,
  );

  res.redirect(signedUrl);
});

app.listen(3000);
```

---

## Mac App Store配布

### 制約事項

| 機能                   | 通常配布         | MAS           |
| ---------------------- | ---------------- | ------------- |
| 自動更新               | electron-updater | App Store     |
| サンドボックス         | 任意             | 必須          |
| ハードニングランタイム | 推奨             | 必須          |
| 署名                   | Developer ID     | Mac App Store |
| ネイティブモジュール   | 可               | 制限あり      |

### electron-builder設定

```yaml
# electron-builder.yml
mas:
  target: mas

  hardenedRuntime: true
  gatekeeperAssess: false

  entitlements: build/entitlements.mas.plist
  entitlementsInherit: build/entitlements.mas.inherit.plist

  # MAS用署名
  identity: "3rd Party Mac Developer Application: Company (TEAM_ID)"

  # プロビジョニングプロファイル
  provisioningProfile: build/embedded.provisionprofile

masDev:
  identity: "Mac Developer: Your Name (XXXXXXXXXX)"
  provisioningProfile: build/embedded-dev.provisionprofile
```

```plist
<!-- build/entitlements.mas.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
</dict>
</plist>
```

---

## Microsoft Store配布

### AppX設定

```yaml
# electron-builder.yml
win:
  target:
    - target: appx
      arch:
        - x64
        - arm64

appx:
  applicationId: CompanyName.AppName
  displayName: My Electron App
  identityName: 12345CompanyName.AppName
  publisher: CN=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  publisherDisplayName: Company Name
  languages:
    - ja-JP
    - en-US
  addAutoLaunchExtension: false
  showNameOnTiles: true
  backgroundColor: "#ffffff"
```

---

## リリースチェックリスト

### リリース前

- [ ] バージョン番号更新
- [ ] CHANGELOGの更新
- [ ] 全プラットフォームでテスト
- [ ] コード署名の確認
- [ ] 依存関係のセキュリティ監査
- [ ] リリースノート作成

### リリース後

- [ ] ダウンロードリンク確認
- [ ] 自動更新テスト
- [ ] インストールテスト（クリーン環境）
- [ ] アップグレードテスト（既存インストール）
- [ ] クラッシュレポート監視

---

## 関連リソース

### 詳細ドキュメント

- `resources/auto-update.md` - 自動更新詳細
- `resources/release-channels.md` - チャネル管理
- `resources/store-distribution.md` - ストア配布

### テンプレート・スクリプト

- `templates/update-server.ts` - 更新サーバー
- `scripts/release.sh` - リリーススクリプト
