---
name: elk-skill
description: "Elastic Stack を用いた Active Directory ログ分析・脅威検知支援スキル。Elasticsearch クエリ、Logstash パイプライン、Kibana 可視化を通じて、Windows イベントログおよび Sysmon ログの多角的な脅威検知を実現します。Active Directory 攻撃検知に最適化。Elasticsearch クエリ設計、Windows/AD 脅威検知、Logstash パイプライン、Kibana ダッシュボード、SIEM 運用保守をサポート。"
license: MIT
compatibility: "Requires Elasticsearch 7.x+, Logstash 7.x+, Kibana 7.x+, Windows Event Logs, Sysmon logs. Integrates with active-directory-skill for multi-layer threat detection."
metadata:
  author: ktod4ts
  version: "2.2"
  tags: "elk,elasticsearch,kibana,logstash,beats,siem,threat-detection,ad-security,windows-event-logs,sysmon,kerberos,ntlm,pass-the-hash,kerberoasting"
  capabilities: "query-construction,ad-threat-detection,sysmon-correlation,attack-chain-detection,pipeline-design,dashboarding-siem,ops-maintenance"
  input-types: "question (string),context (object)"
  output-types: "answer (string),Elasticsearch query examples,Logstash pipeline config,Kibana dashboard design,detection logic"
  permissions: "repository (dashboard/rule/config storage),workspace (local settings/sample logs)"
  constraints: "No raw credentials/secrets. Explicit approval required for production changes. Provided configs are templates requiring environment-specific validation."
  safe-usage: "Apply auto-masking for passwords/PII in logs. Gradual validation in staging recommended. Regular rule review to minimize false positives."
  integration-notes: "Works with active-directory-skill for AD attack detection. Multi-layer threat detection: Windows AD events + Sysmon client-side monitoring + attack chain correlation."
  future-roadmap: "Enhanced Windows event log correlation, advanced Sysmon attack pattern detection, automated incident response templates."
---

# ELK Skill — Active Directory ログ監視統合版

このスキルは Elastic Stack を用いた **Windows イベントログ + Sysmon の多層的なログ分析・脅威検知** に対応しています。特に **Active Directory 攻撃検知とクライアント側の攻撃チェーン検出** に最適化されています。

## 主な機能

### 1. Windows イベントログ解析（ドメインコントローラ + クライアント）

#### ドメインコントローラ側のイベント（従来の AD 攻撃検知）
- **Event ID 4624** (ログオン成功) — ログオンパターン、異常なアカウント利用
- **Event ID 4625** (ログオン失敗) — ブルートフォース、Pass-the-Hash 失敗
- **Event ID 4768** (Kerberos AS-REQ / TGT) — ASREProast の検知
- **Event ID 4769** (Kerberos ST / TGS-REP) — Kerberoasting の検知
- **Event ID 4771** (Kerberos 事前認証失敗) — ASREProast 試行
- **Event ID 4776** (NTLM 認証) — NTLM リレー攻撃の検知
- **Event ID 4720-4738** (ユーザー・コンピュータ属性変更) — 権限昇格の準備段階

#### クライアント側のイベント（Sysmon + Windows セキュリティログ）
- **Sysmon Event ID 1** (プロセス作成) — 悪意あるプロセス起動、権限昇格実行ファイル
- **Sysmon Event ID 3** (ネットワーク接続) — C2 通信、横展開への接続試行
- **Sysmon Event ID 7** (DLL ロード) — DLL インジェクション、LOLBINS の検知
- **Sysmon Event ID 8** (プロセス間メモリアクセス) — メモリインジェクション、特権昇格
- **Sysmon Event ID 10** (プロセスアクセス) — Mimikatz などの認証情報ダンプツール検知
- **Sysmon Event ID 11** (ファイル作成) — NTDS.dit ダンプ、スタートアップスクリプト変更
- **Sysmon Event ID 13** (レジストリ設定変更) — 永続化機構の確立（Run キー、LSA Registry 変更）
- **Sysmon Event ID 17/18** (パイプ作成/接続) — Cobalt Strike、MSBuild.exe 悪用検知
- **Sysmon Event ID 22** (DNS クエリ) — 悪意あるドメイン解決、データ流出先への通信

### 2. AD 攻撃検知クエリテンプレート

#### ドメインコントローラ側（Windows イベントログ）
- **Kerberoasting**: 同一ユーザーからの大量 4769 イベント検知
- **ASREProast**: DONT_REQ_PREAUTH フラグ付きユーザーからの 4768 + 4771
- **Pass-the-Hash**: 4625 → 4624 の異常な短時間連続
- **権限昇格**: 4672 の前に予期しない 4769/4771 がない場合
- **Unconstrained Delegation**: 特定コンピュータへのログイン → TGT ダンプ
- **SID History 注入**: 5136 イベント（AD オブジェクト変更）での SID History 属性変更

#### クライアント側（Sysmon + Windows セキュリティログ）による攻撃検知
- **認証情報ダンプ**: Sysmon Event ID 10（ProcessAccess）で LSASS.exe へのアクセスを検知
  - 攻撃ツール: Mimikatz, Dumpert, procdump
  - 検知条件: TargetImage == "C:\Windows\System32\lsass.exe" AND GrantedAccess in [0x1010, 0x1038, 0x143A, 0x1438, 0x1000]
  
- **DLL インジェクション**: Sysmon Event ID 7（ImageLoad）で異常な DLL ロード場所を検知
  - 検知対象: System32 以外の場所からのロード、一時フォルダ（%TEMP%, %AppData%）
  - 関連 ID: Event ID 8（CreateRemoteThread）と組み合わせ
  
- **横展開への接続**: Sysmon Event ID 3（NetworkConnection）で以下を検知
  - 不明な IP/ホスト名への接続
  - SMB (445), RDP (3389), WinRM (5985) への接続
  - DC Discovery: Kerberos ポート (88) への複数接続
  
- **永続化の確立**: Sysmon Event ID 13（RegistryEvent）で以下を検知
  - HKLM\Software\Microsoft\Windows\CurrentVersion\Run への追加
  - LSA 関連キーの変更（LSA Backdoor）
  - シェルスタート値の変更

- **ファイルベース検知**: Sysmon Event ID 11（FileCreate）で以下を検知
  - NTDS.dit ファイルへのアクセス（VSS 経由のダンプ）
  - SAM、SYSTEM レジストリ ハイブのコピー
  - スタートアップフォルダへのファイル作成

### 3. Logstash パイプライン設計

#### 入力: WinLogBeat または Filebeat（DC + クライアント）
```
input {
  beats {
    port => 5044
    tags => ["windows-security", "sysmon"]
  }
}
```

#### フィルタ: Windows イベント + Sysmon 標準化
```
filter {
  # ========== Windows Security Event の標準化 ==========
  if [winlog] {
    mutate {
      rename => { "[winlog][event_id]" => "event.code" }
      rename => { "[winlog][computer_name]" => "host.name" }
      rename => { "[winlog][event_data][TargetUserName]" => "user.target" }
      rename => { "[winlog][event_data][SubjectUserName]" => "user.source" }
      rename => { "[winlog][event_data][ComputerName]" => "source.computer" }
      rename => { "[winlog][event_data][IpAddress]" => "source.ip" }
      rename => { "[winlog][event_data][WorkstationName]" => "source.workstation" }
    }
  }
  
  # ========== Sysmon イベント（Event ID 1-25）の標準化 ==========
  if [winlog][provider_name] == "Microsoft-Windows-Sysmon" or [event][provider] == "Sysmon" {
    
    # Event ID 1: Process Creation
    if [event][code] == 1 {
      mutate {
        rename => { "[winlog][event_data][ProcessGuid]" => "process.guid" }
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][Image]" => "process.name" }
        rename => { "[winlog][event_data][CommandLine]" => "process.command_line" }
        rename => { "[winlog][event_data][ParentProcessId]" => "process.parent.pid" }
        rename => { "[winlog][event_data][ParentImage]" => "process.parent.name" }
        rename => { "[winlog][event_data][User]" => "process.user" }
      }
      # 基本的なプロセス異常検知
      if [process][name] =~ /(cmd\.exe|powershell\.exe|cscript\.exe|wscript\.exe)/ {
        mutate {
          add_field => { "threat.detection.type" => "suspicious_interpreter" }
        }
      }
    }
    
    # Event ID 3: Network Connection
    if [event][code] == 3 {
      mutate {
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][Image]" => "process.name" }
        rename => { "[winlog][event_data][SourceIp]" => "source.ip" }
        rename => { "[winlog][event_data][SourcePort]" => "source.port" }
        rename => { "[winlog][event_data][DestinationIp]" => "destination.ip" }
        rename => { "[winlog][event_data][DestinationPort]" => "destination.port" }
        rename => { "[winlog][event_data][Protocol]" => "network.protocol" }
        rename => { "[winlog][event_data][InitiatedConnection]" => "network.direction" }
      }
    }
    
    # Event ID 7: DLL Load
    if [event][code] == 7 {
      mutate {
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][Image]" => "process.name" }
        rename => { "[winlog][event_data][ImageLoaded]" => "file.name" }
      }
    }
    
    # Event ID 10: Process Access (LSASS ダンプ検知)
    if [event][code] == 10 {
      mutate {
        rename => { "[winlog][event_data][SourceProcessId]" => "process.source.pid" }
        rename => { "[winlog][event_data][SourceImage]" => "process.source.name" }
        rename => { "[winlog][event_data][TargetProcessId]" => "process.target.pid" }
        rename => { "[winlog][event_data][TargetImage]" => "process.target.name" }
        rename => { "[winlog][event_data][GrantedAccess]" => "process.access.granted" }
      }
      # LSASS アクセス検知
      if [process][target][name] =~ /lsass\.exe/ {
        mutate {
          add_field => { "threat.detection.type" => "credential_access" }
          add_field => { "threat.severity" => "critical" }
        }
      }
    }
    
    # Event ID 13: Registry Event (永続化検知)
    if [event][code] == 13 {
      mutate {
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][TargetObject]" => "registry.path" }
        rename => { "[winlog][event_data][Details]" => "registry.value" }
      }
      # 危険なレジストリパス検知
      if [registry][path] =~ /(HKLM.*Run|HKLM.*Services|HKLM.*LSA)/ {
        mutate {
          add_field => { "threat.detection.type" => "persistence" }
        }
      }
    }
    
    # Event ID 17/18: Named Pipe Event
    if [event][code] in [17, 18] {
      mutate {
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][PipeName]" => "pipe.name" }
      }
      # 悪意あるパイプ名検知（Cobalt Strike など）
      if [pipe][name] =~ /(\\\\\\.\\pipe\\.*chrome.*|postex.*|msagent)/ {
        mutate {
          add_field => { "threat.detection.type" => "c2_communication" }
        }
      }
    }
    
    # Event ID 22: DNS Query
    if [event][code] == 22 {
      mutate {
        rename => { "[winlog][event_data][ProcessId]" => "process.pid" }
        rename => { "[winlog][event_data][QueryName]" => "dns.question.name" }
        rename => { "[winlog][event_data][QueryStatus]" => "dns.response_code" }
      }
    }
  }
}
```

#### 出力: Elasticsearch
```
output {
  elasticsearch {
    hosts => ["https://localhost:9200"]
    index => "windows-security-%{+YYYY.MM.dd}"
    user => "${ES_USER}"
    password => "${ES_PASSWORD}"
  }
}
```

### 4. Kibana ダッシュボード設計

#### 1. AD 攻撃検知ダッシュボード（DC + クライアント）

##### Overview パネル
- **タイムライン**: 疑わしいイベント（Sysmon + Windows Event）の時系列
- **グラフ**: Event ID 4769 / Sysmon Event ID 1（疑わしいプロセス）の日別トレンド
- **テーブル**: 高リスク検知（LSASS アクセス、レジストリ永続化）の一覧

##### クライアント側脅威検知パネル

**Sysmon Event ID 1 + 10 統合**:
- タイムライン: 権限昇格スクリプト実行 (cmd.exe/powershell.exe) → LSASS.exe アクセス
- テーブル: LSASS アクセスプロセス一覧（ソース、アクセス権限、時刻）

**Sysmon Event ID 13 (Registry) 検知**:
- テーブル: HKLM\Software\Microsoft\Windows\Run への追加
- テーブル: LSA レジストリキーの変更（Skeleton Key, DCSync 永続化）

**Sysmon Event ID 17/18 (Named Pipe)**:
- テーブル: 悪意あるパイプ名（Cobalt Strike, Metasploit）の検知
- グラフ: パイプ名別の発生回数

**Sysmon Event ID 3 (Network Connection) 検知**:
- テーブル: DC への不正な接続（Kerberos ポート 88, LDAP ポート 389 への多数接続）
- 地図表示: 接続元 IP の地理的分布（異常な場所からのアクセス）

#### 2. 攻撃チェーン検知ダッシュボード（DC + クライアント統合）

**Pass-the-Hash 攻撃検知フロー**:
1. Sysmon Event ID 10: LSASS.exe へのプロセスアクセス（クライアント）
2. 数秒～数分後: Sysmon Event ID 3: SMB 接続 (445) またはネットワークシェア接続（クライアント）
3. リモート DC での Event ID 4625: NTLM 認証失敗（DC）
4. その直後: Event ID 4624: ログオン成功（DC）

**ダッシュボード実装**:
```
Kibana Correlation Search
query.bool.must:
  - event.code: 10
    process.target.name: lsass.exe
  - time_range: now-5m
correlate_with:
  - event.code: 3
    destination.port: 445
    time_offset: +30s
  - event.code: 4625
    event.code: 4624
    time_offset: +2m
```

#### 3. Sysmon ログ量管理パネル

**ログ生成量の監視**（SwiftOnSecurity config 使用時）:
- グラフ: Event ID 別のログ生成レート
- テーブル: ホスト別のログ生成量（上位 10）
- アラート: 1 時間あたりのログ生成量が閾値超過した場合

**注記**: SwiftOnSecurity の sysmonconfig-export.xml を使用する場合、以下の Event ID が大量のログを生成するため、ホスト数によっては Elasticsearch ディスク容量を計画：
- Event ID 3 (Network Connection): ~100-1000 イベント/ホスト/日
- Event ID 22 (DNS Query): ~500-5000 イベント/ホスト/日

**推奨フィルタ**:
- ALLOWED/DENIED の除外、localhost への接続除外
- 内部 DNS クエリの除外（組織内ドメイン）
- よく知られたプロセスのフィルタリング（Chrome, Edge など）

## 想定ユースシーン

### シーン 1: DC 側の Kerberoasting + クライアント側の不正プロセス検知
```
プロンプト:
"ドメインコントローラで Event ID 4769 が大量に発生している。
同時にクライアントの Sysmon で Event ID 1 (cmd.exe/powershell.exe の実行) と 
Event ID 10 (LSASS.exe へのアクセス) が検知されています。
これらを関連付ける Elasticsearch クエリと Kibana ダッシュボード設計を教えて"

応答:
1. 時間窓 5 分以内の Event ID 4769 と Sysmon Event ID 10 を相関させる DSL
2. Timeline ダッシュボード: Event 4769 の発生時刻 ± 2 分に Sysmon Event 10 があるかを確認
3. Alert 設定: 同一ユーザーで上記パターンが検知された場合の通知
```

### シーン 2: Pass-the-Hash 攻撃の多段階検知
```
プロンプト:
"クライアントで Sysmon Event 10 (LSASS.exe アクセス) が検知された直後に、
Sysmon Event 3 で SMB (445) への接続が記録され、
その 2 分後に DC で Event ID 4625 (NTLM 認証失敗) と Event ID 4624 (成功) が短時間に連続している。
これが Pass-the-Hash 攻撃か検証したい"

応答:
1. 多段階相関クエリ: Sysmon Event 10 → Event 3 (445) → Event 4625 + 4624 の時系列
2. Kibana Correlation Detection: 上記パターンが検知されたら即座に Alert
3. 追加調査: ソースプロセス、ターゲットユーザー、接続先ホストの詳細
```

### シーン 3: Sysmon Event ID 13 による永続化検知
```
プロンプト:
"Sysmon Event ID 13 (Registry Modification) で、
HKLM\Software\Microsoft\Windows\CurrentVersion\Run に 
疑わしいプロセス名が追加されているのを検知したい。
どのような Elasticsearch クエリとダッシュボード設計が最適ですか？"

応答:
1. Event ID 13 + レジストリパス フィルタリング Elasticsearch DSL
2. Kibana テーブル: registry.path, registry.value, process.name を表示
3. Alert ルール: HKLM\.*Run への変更が検知された場合の通知
```

### シーン 4: Sysmon Event 3 による横展開検知
```
プロンプト:
"クライアント側の Sysmon Event ID 3 で、
複数のホストへ SMB (445) または RDP (3389) への接続が検知されています。
これが横展開（Lateral Movement）か検証し、
攻撃チェーンを可視化したいです"

応答:
1. Elasticsearch: Sysmon Event 3 で destination.port in [445, 3389] かつ複数ホストへの接続
2. Kibana ネットワーク図: ソースホスト → 複数の接続先ホストの可視化
3. Timeline: 時系列でどのホストに いつ接続したかを追跡
```

## 推奨される Logstash パイプライン構成

### 入力: WinLogBeat または Filebeat
```
input {
  beats {
    port => 5044
  }
}
```

### フィルタ: Windows イベントログ標準化
```
filter {
  if [type] == "wineventlog" {
    mutate {
      rename => { "[winlog][event_id]" => "event_id" }
      rename => { "[winlog][computer_name]" => "computer" }
      rename => { "[winlog][event_data][TargetUserName]" => "target_user" }
      rename => { "[winlog][event_data][ComputerName]" => "source_computer" }
      rename => { "[winlog][event_data][IpAddress]" => "source_ip" }
    }
  }
}
```

### 出力: Elasticsearch
```
output {
  elasticsearch {
    hosts => ["https://localhost:9200"]
    index => "windows-security-%{+YYYY.MM.dd}"
    user => "${ES_USER}"
    password => "${ES_PASSWORD}"
  }
}
```

## Kibana 検知ダッシュボード推奨構成

### 1. Overview パネル
- Event ID 4624 / 4625 の日別トレンド
- Event ID 4768 / 4769 の日別トレンド
- 最も活動の多いユーザー TOP 10

### 2. Anomaly Detection パネル
- 機械学習: ユーザーごとのログオン時刻・回数・ホスト数の異常
- 統計的異常: 通常と異なる IP アドレスからのアクセス

### 3. Alert 設定パネル
- 条件: Event ID 4769 count > 15 in 1h per user → Alert
- 条件: Event ID 4625 count > 5 + 4624 success within 5min → Alert
- 条件: Event ID 5136 + SID History attribute change → Alert

### 4. Investigation パネル
- タイムラインビュー：ユーザーの全イベント（4624/4625/4768/4769）を時系列表示
- テーブルビュー：ホスト別・ユーザー別の統計

## セキュリティ・運用上の考慮事項

### ログ保持期間
- **セキュリティイベント**: 最低 90 日（推奨 1 年）
- **監査ログ**: 最低 365 日（規制要件による）
- **Sysmon ログ**: 最低 30 日（ログ量が多い場合は短期、重要性が高い場合は長期）
- **ILM ポリシー**: 30 日後に Warm ノードへ、90 日後に Cold ノードへ遷移

### データマスキング
- ユーザーパスワード・NTLM ハッシュ: 自動削除ルール適用
- PII (名前・メールアドレス): 匿名化オプション設定
- コマンドライン引数（認証情報が含まれる場合）: マスキング

### アクセス制御
- Kibana スペース・ロールベースアクセス制御 (RBAC)
- 監視人員のみが検知ダッシュボード・アラート設定にアクセス
- Sysmon イベントは機密情報（プロセス実行内容）を含むため、アクセス制限

### Sysmon 設定ファイル管理（SwiftOnSecurity config 等）

#### 推奨設定
- SwiftOnSecurity の sysmonconfig-export.xml をベースに使用
- 組織固有の要件に合わせてカスタマイズ
  - 除外ルール: 自社アンチウイルス、バックアップツール、定期実行スクリプト
  - フィルタ設定: DNS クエリ、ネットワーク接続の過度なフィルタリング（ノイズ削減）

#### Sysmon ログ生成量の管理
| Event ID | 説明 | 日間ログ量/ホスト | フィルタ推奨 |
|----------|------|------------------|-------------|
| 1 | プロセス作成 | 100-500 | - |
| 3 | ネットワーク接続 | 1000-5000 | localhost 除外、内部 IP 除外 |
| 7 | DLL ロード | 500-2000 | System32 一部除外 |
| 10 | プロセスアクセス | 0-1000 | 含める/除外のルール明示 |
| 13 | レジストリ変更 | 100-1000 | User Profile の軽微な変更を除外 |
| 22 | DNS クエリ | 2000-5000 | 内部ドメイン除外、404 応答除外 |

**計算例**: 100 ホストで 1 日あたり約 500 万イベント（低フィルタ） → 約 500GB/月のディスク使用

#### ディスク容量計画
- **Elasticsearch: 圧縮率 50% を想定**
  - 100 ホスト × 500 万イベント/日 × 30 日 × 0.5 KB/イベント × 50% 圧縮 ≈ 375 GB/月
- **推奨: SSD RAID6 構成で 1 TB 以上を確保**
- **アーカイブ: 90 日以上は Cold Node または S3 へ移行**

### パフォーマンス最適化
- **WinLogBeat**: バッチサイズ 1000 イベント、送信間隔 5 秒に設定
- **Logstash**: worker スレッド数 = CPU コア数 / 2
- **Elasticsearch**: heap サイズ 30 GB（max 31 GB）以上を確保

## 使い方（例プロンプト）

### AD + Sysmon 統合脅威検知関連
- "DC の Event ID 4769 + クライアントの Sysmon Event ID 10 (LSASS アクセス) を同時検知する Elasticsearch 相関クエリを作成して"
- "Sysmon Event ID 1 (powershell.exe) → Event ID 10 (LSASS.exe) → Event ID 3 (SMB 445) の攻撃チェーンを検知する Kibana Timeline を設計してください"
- "Pass-the-Hash 攻撃の検知: DC の Event 4625/4624 と クライアントの Sysmon Event 10/3 を 5 分以内で関連付けるアラートルール設定を教えて"
- "Sysmon Event ID 13 (Registry) で HKLM\Run への追加を検知し、その実行プロセス (Event ID 1) を特定する Kibana テーブル設計を教えてください"

### Sysmon ログ量管理関連
- "SwiftOnSecurity sysmonconfig-export.xml 使用時の 100 ホスト環境でのログ生成量を見積もり、Elasticsearch ディスク容量計画をしてください"
- "Sysmon Event ID 3 (Network Connection) と Event ID 22 (DNS Query) のログノイズを削減するフィルタルール（除外条件）を設定してください"
- "Sysmon ログの ILM ポリシー設定: 30 日 → Warm, 90 日 → Cold, 180 日 → Delete の構成方法を教えて"

## 将来対応予定

ELK Skill は現在 Active Directory とログ監視の統合に特化しており、以下の拡張を検討しています：

- 高度な攻撃パターン検知（多段階のKerberos攻撃、権限昇格フロー）
- 自動インシデント応答テンプレート生成
- Windows イベントログ相関の機械学習モデル統合

---
