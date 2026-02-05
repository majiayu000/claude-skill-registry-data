---
name: library-release-checker
description: GitHubや公式ドキュメントからライブラリのリリース情報を取得し、破壊的変更・非推奨化・ビルトイン化を特定する
allowed-tools: WebFetch, WebSearch
---

# リリース情報取得スキル

**役割**: Web調査に特化。ライブラリのリリース情報を公式ソースから取得する。

**入力**: ライブラリ名、現在バージョン、目標バージョン（呼び出し元から渡される）

## 調査対象

1. **破壊的変更（Breaking Changes）**
2. **非推奨化（Deprecations）**
3. **ビルトイン化（不要になるパッケージ）**
4. **マイグレーションガイドのURL**

## 情報ソース

### GitHub
```
https://github.com/{org}/{repo}/releases
https://github.com/{org}/{repo}/blob/main/CHANGELOG.md
https://github.com/{org}/{repo}/blob/main/MIGRATION.md
```

### 公式ドキュメント
| ライブラリ | リリースノート | マイグレーションガイド |
|-----------|--------------|---------------------|
| React | https://react.dev/blog | https://react.dev/blog/2024/04/25/react-19-upgrade-guide |
| Next.js | https://nextjs.org/blog | https://nextjs.org/docs/app/guides/upgrading |
| Vue | https://blog.vuejs.org | https://v3-migration.vuejs.org |
| Angular | https://blog.angular.io | https://angular.dev/update-guide |
| TypeScript | https://devblogs.microsoft.com/typescript | https://www.typescriptlang.org/docs/handbook/release-notes |

### EOL情報
```
https://endoflife.date/{library}
```

## 出力フォーマット

```json
{
  "breakingChanges": [
    {
      "title": "API名変更",
      "description": "useRouter → useNavigation",
      "version": "15.0.0",
      "severity": "high"
    }
  ],
  "deprecations": [
    {
      "api": "getServerSideProps",
      "replacement": "Server Components",
      "version": "15.0.0"
    }
  ],
  "builtins": [
    {
      "package": "@next/font",
      "reason": "next/fontにビルトイン",
      "version": "13.0.0"
    }
  ],
  "references": {
    "releaseNotes": "https://...",
    "migrationGuide": "https://...",
    "changelog": "https://..."
  }
}
```

## 検索キーワード

リリースノート内で以下を検索:
- `breaking change`, `breaking`
- `deprecated`, `deprecation`
- `removed`, `no longer`
- `built-in`, `included`, `bundled`
- `migration`, `upgrade`
