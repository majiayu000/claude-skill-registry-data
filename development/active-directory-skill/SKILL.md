---
name: active-directory-skill
description: "Active Directory 攻撃・検知に関する包括的な知識スキル。Kerberos 認証プロトコル、権限昇格、ドメイン間信頼悪用、LDAP 攻撃、Windows ログ分析による脅威検知など、AD セキュリティの多岐にわたるトピックをカバーしています。ELKと統合し、IT セキュリティの基盤を提供。認証フロー、権限昇格経路、永続化技術、ドメイン間信頼悪用、ログ分析検知、LDAP 操作、防御戦略の 8 つの主要機能をサポートします。"
license: MIT
compatibility: "Requires Elasticsearch 7.x+, Windows Event Logs, Logstash for log parsing. Integrates with ELK-skill for SIEM analysis."
metadata:
  author: ktod4ts
  version: "1.2"
  tags: "active-directory,kerberos,windows-security,threat-detection,privilege-escalation,ad-security,authentication,ntlm,ticket-forgery,domain-trust,ldap,windows-event-logs,elk-integration,security-awareness,diamond-ticket,sapphire-ticket,gmsa,foreign-security-principals,print-spooler,kerberos-delegation"
  capabilities: "attack-methodology,authentication-flow,privilege-escalation-paths,persistence-techniques,forest-privilege-escalation,log-analysis-detection,ldap-operations,defense-strategies,next-gen-kerberos-attacks,gmsa-security,fsp-auditing,delegation-attacks"
  input-types: "question (string),attack-context (object)"
  output-types: "answer (string),detection-query (string)"
  permissions: "knowledge-base,workspace"
  constraints: "Educational and defensive purposes only. Requires written approval for practical testing. Illegal access is forbidden. All test activities must be recorded and reported."
  safe-usage: "Practical testing requires written approval from system owner/administrator. Security policy compliance required. Incident response procedures should be in place before attack simulation."
  limitations: "Educational knowledge provision focus. Responsible testing requires owner approval. AD environment complexity may require environment-specific adaptation."
  notes: "Works best with ELK-skill for Windows event log threat detection. v1.2 adds next-gen Kerberos attacks (Diamond/Sapphire Tickets), GMSA security, FSP auditing, and advanced Kerberos delegation attacks. Knowledge base continuously expanded. Organization-specific AD configuration understanding recommended."
---

# Active Directory Attack & Detection Skill

## 概要
このスキルは、Active Directory (AD) 環境における攻撃技術とログを用いた検知方法についての包括的な知識を提供します。Kerberos認証プロトコル、権限昇格、ドメイン間の信頼関係悪用、ログ分析による脅威検知など、AD セキュリティに関連する多岐にわたるトピックをカバーしています。

## 対応トピック

### 1. AD 基本概要 & 構成
- **ドメイン / ツリー / フォレスト構造**: AD 階層の理解
- **ドメインコントローラ (DC)**: LDAP, Kerberos, NTLM の役割
- **ドメイン信頼関係**: Parent-Child, External, Forest Trust など
- **セキュリティ境界**: フォレストがセキュリティ境界として機能

### 2. 認証 & Kerberos プロトコル
- **TGT / ST / PAC**: チケット関連の基本概念
- **AS-REQ / AS-REP / TGS-REQ / TGS-REP**: Kerberos 認証フロー
- **暗号化方式**: DES / RC4 / AES128 / AES256
- **Salt 計算**: ユーザーとコンピュータの salt の違い
- **事前認証 (Pre-auth)**: DONT_REQ_PREAUTH 属性と悪用
- **Service Principal Name (SPN)**: SPN の形式と役割
- **サービス-ユーザー拡張**: S4U2Self / S4U2Proxy
- **ユーザー間認証 (U2U)**: デスクトップサービスでの使用

### 3. 認証攻撃 (認証情報なし)
- **ユーザー列挙**:
  - Kerbrute による列挙（KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN）
  - SMB / LDAP 匿名列挙
  - OWA (Outlook Web Access) からの列挙
  - MS-NRPC インターフェース悪用
  
- **LLMNR / NBT-NS ポイズニング**: NTLM チャレンジハッシュの取得
- **NTLM リレー攻撃**: 認証の横取りと悪用
- **Hash Shucking & NT-Candidate**: NT ハッシュコーパスの再利用検証

### 4. 認証攻撃 (認証情報あり)
- **ASREProast**: 事前認証無効ユーザーの TGT 抽出
- **Kerberoast**: SPNを持つサービスアカウントの ST 抽出とオフラインクラック
- **Kerberoasting without pre-authentication**: 認証なしでの Kerberoast
- **Password Spraying / Brute Force**: 複数ユーザーへの攻撃
- **リモート接続悪用**: RDP, SSH, WinRM, FTP を経由した認証
- **ローカル権限昇格**: SAM / LSASS / キャッシュからのクレデンシャル抽出

### 5. 権限昇格 (特権認証情報あり)
- **Pass the Hash (PtH)**: NTLM ハッシュを用いた認証
- **Over Pass the Hash / Pass the Key**: Kerberos チケット取得
- **Pass the Ticket (PtT)**: チケット盗用による認証
- **コンピュータ共有への横移動**: SMB 共有スキャン, クレデンシャル検索
- **Printer Spooler Service 悪用**: 権限付き認証の強制
- **RDP セッション悪用**: セッションハイジャック
- **LAPS**: ローカル Administrator パスワード管理の悪用
- **MSSQL 信頼リンク**: データベース間の信頼関係の悪用

### 6. 権限昇格 (高権限)
- **Kerberos チケット偽造 (次世代型)**:
  - **Golden Ticket**: KRBTGT のパスワードハッシュから TGT を完全偽造 (ゼロから作成)
  - **Diamond Ticket**: 正当な低特権 TGT を複合し、その PAC を改ざんして権限昇格。TGT のチケット本体は DC から正当に発行されたものを使用するため検出が困難
    - 方法1: TGT の cname と PAC を変更してドメイン管理者を偽装
    - 方法2: 通常ユーザーのパッケージを維持したまま PAC のみ改ざん (権限値を上書き)
  - **Sapphire Ticket**: 低特権ユーザーの認証情報を取得し、U2U + S4U2Self を組み合わせて、高特権ユーザーの正当な PAC を抽出してから、元のユーザーの TGT に挿入。真の高特権 PAC を使用するため検出は Golden/Diamond より困難
    - PA_FOR_USER で高特権ユーザーを指定
    - sname に低特権ユーザー名を設定
    - ENC-TKT-IN-SKEY フラグを有効化
    - 取得した高特権 PAC を低特権 TGT に統合
  - 検知方法: Windows Event 4768/4769 で同一ホストからの異なるユーザーの TGT/TGS、Event 4627 でのグループメンバーシップ不正性、U2U パラメータの不正な組み合わせ

- **Kerberos 委任攻撃**:
  - **Unconstrained Delegation**: メモリからの TGT ダンプ → 任意サービスへのアクセス (リスク大)
  - **Constrained Delegation**: S4U2Self / S4U2Proxy 悪用 → 指定サービスのみ委任可能 (より制限的)
  - **Protocol Transition**: 他の認証方式 (NTLM など) からの委任 → 任意ユーザー偽装が可能
  - **Resource-based Constrained Delegation (RBCD)**: リソース側で委任設定 → 書き込み権限からの権限昇格が容易
  - Unconstrained から Constrained への移行必須。SPN が登録されていない委任は無効化推奨

- **権限 / ACL 悪用**: DACL / ACE の改ざん
- **SID History 注入**: SID 偽造による権限昇格
- **AD CS (Certificate Services)**:
  - ESC1-ESC14: 証明書テンプレート脆弱性
  - 証明書盗用 / 偽造
  - アカウント / ドメイン永続化
  
- **Print Spooler 悪用 (Petitpotam / PrinterBug / Printerbug)**:
  - RpcRemoteFindFirstPrinterChangeNotification を悪用
  - ドメインコントローラで Print Spooler サービスが起動していると、DC 自身の認証情報を取得可能
  - NTLM リレー攻撃や LSASS クレデンシャルダンプへ発展
  - 対策: DC の Print Spooler サービス無効化 (GPO で spooler を Disabled に設定)

### 7. ドメイン管理者権限後の悪用
- **ドメインクレデンシャル ダンプ**:
  - DCSync / NTDS.dit 窃取
  - DSRM (Directory Services Restore Mode) 認証情報
  
- **Golden Ticket / Silver Ticket / Diamond Ticket**: 偽造チケット悪用
- **永続化**:
  - Skeleton Key: マスターパスワード設定
  - Custom SSP: クレデンシャル平文取得
  - DCShadow: ログ記録なしの AD 改ざん
  - AdminSDHolder 悪用: 特権グループのメンバーシップ自動復元
  - ACL Persistence: 将来の権限昇格パス確保

### 8. ドメイン間信頼悪用 & フォレスト権限昇格
- **信頼関係の列挙**: Get-DomainTrust, nltest
- **Child-to-Parent 昇格**:
  - SID History Injection
  - Configuration NC (Naming Context) 悪用
  - gMSA (Group Managed Service Account) コンプロミズ
  - AD CS ESC5
  
- **External Domain Trust**:
  - Inbound / Outbound 信頼の悪用
  - SQL Database Linked Server を経由した横移動
  
- **SID Filtering / Selective Authentication**: 防御メカニズム

### 9. Group Managed Service Accounts (GMSA) セキュリティリスク

- **GMSA パスワード管理**:
  - GMSA のパスワードは AD により自動管理・変更される (実装: Windows 2012+)
  - `msDS-ManagedPassword` 属性に直近のパスワード格納
  - `PrincipalsAllowedToRetrieveManagedPassword` で明示的に委任
  
- **GMSA コンプロミズシナリオ**:
  - GMSA サービスをホストするコンピュータが侵害 → GMSA パスワードもコンプロミズ
  - GMSA パスワード取得権限を持つアカウント侵害 → GMSA コンプロミズ
  - GMSA 利用サービスの特権を活用して、他のシステムへのアクセス取得
  
- **検知 / 対策**:
  - `PrincipalsAllowedToRetrieveManagedPassword` へのアクセス権限を厳格に制御
  - GMSA を使用するコンピュータのセキュリティ強化が必須
  - GMSA のパスワード変更履歴を監視 (Event ID 4743 など)
  - GMSA 利用サービスの実行特権を最小限に制限

### 10. Foreign Security Principals (FSPs) & フォレスト間侵害

- **Foreign Security Principals (FSPs) とは**:
  - 別フォレスト/別ドメインのアカウントやグループが、現在のフォレストのグループに属する場合、その外部アカウント/グループを FSP として表現
  - 例: trdnet.local のドメイン管理者が trd.com の高権限グループに属する場合、そのアカウントは FSP として登録
  
- **FSP による侵害リスク**:
  - 別フォレストが侵害されると、その FSP を通じて現在のフォレストも侵害される可能性
  - 例: TRDNET フォレスト侵害 → TRD.COM フォレスト侵害 (FSP 経由)
  - フォレスト間の信頼は高権限アカウント共有への道
  
- **検知 / 対策**:
  - `Get-ADGroupMember -Recursive` で高権限グループを定期的に監査
  - FSP の必要性を検証し、不要な FSP を削除
  - 別フォレストからの FSP は信頼できるか厳密に確認
  - フォレスト間の信頼レベルを「Forest Trust」から「External Trust」への制限検討
  - PowerShell: [Invoke-FindPrivilegedFSPs.ps1](https://github.com/PyroTek3/Misc/blob/main/Invoke-FindPrivilegedFSPs.ps1) で自動検査

### 11. LDAP ベース攻撃 (オンホストインプラント)
- **LDAP 列挙 BOFs**: ユーザー / コンピュータ / グループ取得
- **LDAP 書き込み操作**:
  - オブジェクト作成 (add-user, add-computer, add-group)
  - パスワードリセット / グループメンバー変更
  - ACE 追加 / 削除

- **委任 / Roasting / Kerberos**:
  - S4U 拡張機能の設定
  - Kerberoastable / ASREProastable 化
  - RBCD の配置

### 12. ログ検知 & 監視

#### Windows イベントログ (Event IDs)
- **認証イベント**:
  - 4624: ログオン成功
  - 4625: ログオン失敗
  - 4768: Kerberos AS-REQ (TGT リクエスト)
  - 4769: Kerberos ST (Service Ticket)
  - 4776: NTLM 認証
  - 4771: Kerberos 事前認証失敗
  - 4776: NTLM Logon
  
- **Kerberos 攻撃の検知**:
  - 4768: 異常なユーザーからの TGT リクエスト
  - 4769: 大量の ST リクエスト (Kerberoasting)
  - 4771: 事前認証失敗の増加 (ASREProasting attempt)
  - 4776: RC4 で暗号化された TGS-REP の検知
  
- **権限昇格イベント**:
  - 4672: 特別な権限での操作
  - 4720-4726: ユーザー / グループ管理操作
  - 5136: AD オブジェクト変更
  - 4742 / 4738: コンピュータ / ユーザー属性変更
  
- **Pass-the-Hash / Pass-the-Ticket 検知**:
  - 4625: 異常なログオン失敗パターン
  - 4720-4738: 権限昇格のための属性変更
  - 4662: AD オブジェクトへのアクセス (DCSync 検知)
  
- **永続化操作**:
  - 5136: SID History 変更
  - 4742 / 4738: ユーザー属性 (DONT_REQ_PREAUTH など) の変更
  - 4733 / 4731: グループメンバーシップ変更

#### 検知クエリ例
- Kerberoasting の検知: 同一ユーザーによる多数の 4769 イベント
- 権限昇格パターン: 4672 の前に 4769 / 4771 がない場合の特異性
- SID History 注入: 5136 イベントで SID History 属性の予期しない変更
- Pass-the-Ticket: 同一プロセス内での複数トークン使用

### 13. 攻撃軽減 & 防御戦略
- **Domain Admin 制限**: DC へのログオンのみ許可
- **Service Account セキュリティ**: 高権限での実行回避
- **Temporal Privilege Elevation**: 一時的な権限昇格 (例: 20分制限)
- **欺瞞 (Deception)**:
  - Decoy ユーザー / コンピュータ配置
  - HoneypotBuster による検知
  - 不可疑な属性での予期しないアクセス検知
  
- **ATA Detection Bypass**: 検知システムの特性を理解
- **LAPS 導入**: ローカル管理者パスワードランダム化
- **Credential Guard / Device Guard**: Windows Defender の活用
- **監査ポリシー**: 詳細なイベントログ記録

## 使用シーン

**Copilot Chat での使用例:**
- `Active Directory で Kerberoasting 攻撃の検知方法を教えて`
- `ASREProast に対する Windows ログの検知クエリを作成して`
- `Pass-the-Hash 攻撃を検知するため Event ID 4624 / 4769 のパターンを説明して`
- `Domain Admin から子ドメインへの SID History 注入の検知方法は？`
- `Unconstrained Delegation の悪用をログから検知する手順を教えて`
- `Certificate Services (AD CS) の悪用検知クエリを提供して`
- `LDAP ベースの ACL 変更をイベントログから追跡する方法は？`
- `Diamond Ticket / Sapphire Ticket 攻撃の検知方法と Windows Event 4627 の見方を教えて`
- `Group Managed Service Accounts (GMSA) のセキュリティリスクと検知方法は？`
- `Foreign Security Principals (FSPs) が侵害経路になる仕組みを説明して`
- `Kerberos 委任の4つのタイプ (Unconstrained / Constrained / Protocol Transition / RBCD) の悪用検知クエリを作成`
- `Print Spooler (Petitpotam) 攻撃による DC 侵害の検知と対策は？`

## 参考リンク

### Palo Alto Networks - Unit 42
- [貴石のチケット: 詳解 次世代型Kerberos攻撃](https://unit42.paloaltonetworks.com/ja/next-gen-kerberos-attacks/) - Diamond Ticket & Sapphire Ticket 攻撃の詳細解説
- [CortexXDRによるBronze Bit脆弱性からの保護](https://www.paloaltonetworks.com/blog/security-operations/bronze-bit-vulnerability-xdr/?lang=ja) - Kerberos 委任脆弱性

### ADSecurity.org - Sean Metcalf
- [ADSecurity.org](https://adsecurity.org/) - Active Directory & Entra ID セキュリティ総合情報サイト
- [Active Directory Security Tip #14: Group Managed Service Accounts (GMSAs)](https://adsecurity.org/) - GMSA セキュリティリスク
- [Active Directory Security Tip #13: Reviewing Foreign Security Principals (FSPs)](https://adsecurity.org/) - FSP 監査と対策
- [Active Directory Security Tip #12: Kerberos Delegation](https://adsecurity.org/) - 4 つの委任タイプの詳細
- [Active Directory Security Tip #11: Print Service on Domain Controllers](https://adsecurity.org/) - Print Spooler の無効化
- [The History of Active Directory Security](https://adsecurity.org/) - AD 攻撃技術の20年以上の発展経歴
- [Detecting Kerberoasting Activity](https://adsecurity.org/) - Kerberoast 検知方法
- [Mimikatz DCSync Usage, Exploitation, and Detection](https://adsecurity.org/) - DCSync 悪用と検知

### HackTricks
- [Active Directory Methodology](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/index.html)
- [Kerberos Authentication](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/kerberos-authentication.html)
- [Kerberoast](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/kerberoast.html)
- [ASREProast](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/asreproast.html)
- [Password Spraying](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/password-spraying.html)
- [DCSync](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/dcsync.html)
- [Pass the Hash](https://book.hacktricks.wiki/ja/windows-hardening/ntlm/index.html#pass-the-hash)
- [Pass the Ticket](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/pass-the-ticket.html)
- [Constrained Delegation](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/constrained-delegation.html)
- [Unconstrained Delegation](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/unconstrained-delegation.html)
- [AD CS (Certificate Services)](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/ad-certificates/index.html)
- [Golden Ticket](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/golden-ticket.html)
- [Silver Ticket](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/silver-ticket.html)
- [Domain Trusts](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/index.html#forest-privilege-escalation---domain-trusts)
- [BloodHound](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/bloodhound.html)
- [LAPS](https://book.hacktricks.wiki/ja/windows-hardening/active-directory-methodology/laps.html)

### The Hacker Recipes
- [Kerberos](https://www.thehacker.recipes/ad/movement/kerberos/)
- [Pass the Key / Over Pass the Hash](https://www.thehacker.recipes/ad/movement/kerberos/ptk)
- [Pass the Ticket](https://www.thehacker.recipes/ad/movement/kerberos/ptt)
- [Relay](https://www.thehacker.recipes/ad/movement/kerberos/relay)
- [Delegations](https://www.thehacker.recipes/ad/movement/kerberos/delegations/)
- [Forged Tickets](https://www.thehacker.recipes/ad/movement/kerberos/forged-tickets/)
- [DACL Abuse](https://www.thehacker.recipes/ad/movement/dacl/)

### 用語・知識
- **Kerberos**: チケットベースの認証プロトコル
- **NTLM**: 従来の Windows 認証方式
- **SPN (Service Principal Name)**: サービスを識別する名称
- **SID (Security Identifier)**: Windows のセキュリティオブジェクト識別子
- **PAC (Privilege Attribute Certificate)**: チケットに含まれる権限情報
- **TGT (Ticket Granting Ticket)**: Domain Controller から発行される初期チケット
- **ST (Service Ticket)**: 特定のサービスへのアクセスを許可するチケット
- **RBCD (Resource-based Constrained Delegation)**: リソース側で委任を制御
- **DCSync**: Domain Controller Synchronization (ドメイン同期を悪用)
- **Forest Trust**: フォレスト間の信頼関係
- **SID Filtering**: フォレスト間の SID チェック
- **Diamond Ticket**: 正当な低特権 TGT の PAC を改ざんして権限昇格する攻撃
- **Sapphire Ticket**: U2U + S4U2Self で高特権 PAC を抽出し、低特権 TGT に統合する攻撃
- **GMSA (Group Managed Service Accounts)**: AD が自動管理するサービスアカウント (Windows 2012+)
- **msDS-ManagedPassword**: GMSA のパスワードを保持する属性
- **PrincipalsAllowedToRetrieveManagedPassword**: GMSA パスワード取得権限を持つセキュリティプリンシパル
- **FSP (Foreign Security Principal)**: 別フォレスト/別ドメインのアカウント/グループがローカルグループに属する際の表現
- **Print Spooler / Petitpotam**: RpcRemoteFindFirstPrinterChangeNotification を悪用した認証情報取得攻撃

## 注意事項

このスキルの情報は教育目的です。実際のセキュリティテストは以下を必ず遵守してください：

1. **合法性**: テスト対象システムへの明確な書面による許可を取得すること
2. **倫理**: 不正アクセスや無許可のテストは違法です
3. **機密性**: テスト結果は機密情報として厳格に管理してください
4. **ドキュメント**: すべてのテスト活動を記録し、レポートを提供してください

## 更新履歴

- **2025-01-02**: v1.2 - Palo Alto Networks & ADSecurity.org 情報を統合
  - Diamond Ticket / Sapphire Ticket 攻撃の検知方法を追加
  - GMSA (Group Managed Service Accounts) セキュリティリスク新規セクション
  - Foreign Security Principals (FSPs) フォレスト間侵害新規セクション
  - Kerberos 委任の4つのタイプを詳細化 (Unconstrained / Constrained / Protocol Transition / RBCD)
  - Print Spooler (Petitpotam) 攻撃の説明を追加
  - 参考リンクを Palo Alto Networks Unit 42 と ADSecurity.org で拡充
  - Copilot Chat 使用例を4つ追加 (Diamond/Sapphire, GMSA, FSP, Kerberos Delegation)
  
- **2025-12-30**: v1.1 - 初版作成
  - Active Directory 攻撃手法の包括的な概要
  - Kerberos プロトコルと関連攻撃
  - 権限昇格と横移動の方法
  - ドメイン間信頼悪用
  - ログ検知・監視ガイドライン
