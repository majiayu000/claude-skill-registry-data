---
name: fapi
description: FAPI（Financial-grade API）機能の開発・修正を行う際に使用。FAPI 1.0 Baseline/Advanced, FAPI CIBA, mTLS, PAR, JARM実装時に役立つ。
---

# FAPI（Financial-grade API）開発ガイド

## ドキュメント

- `documentation/docs/content_06_developer-guide/04-implementation-guides/oauth-oidc/fapi.md` - FAPI実装ガイド
- `documentation/docs/content_03_concepts/03-authentication-authorization/concept-06-fapi.md` - FAPI概念
- `documentation/docs/content_10_ai_developer/ai-32-extension-fapi.md` - AI開発者向けFAPIガイド

## 機能概要

FAPIは、金融グレードのセキュリティを実現するOIDC/OAuth 2.0プロファイル。
- **FAPI 1.0 Baseline Profile**: 基本的なセキュリティ要件
- **FAPI 1.0 Advanced Profile**: 高度なセキュリティ要件（PAR, JARM, mTLS必須）
- **FAPI CIBA Profile**: CIBAとFAPIの組み合わせ
- **Sender-constrained Access Token**: mTLSバインディング

## モジュール構成

```
libs/
├── idp-server-core-extension-fapi/          # FAPI拡張モジュール
│   └── .../extension/fapi/
│       ├── FapiBaselineVerifier.java       # FAPI Baseline検証
│       ├── FapiAdvanceVerifier.java        # FAPI Advanced検証
│       ├── FapiProfileValidator.java       # FAPIプロファイル検証
│       ├── TlsClientAuthAuthenticator.java # mTLSクライアント認証
│       └── SelfSignedTlsClientAuthAuthenticator.java
│
├── idp-server-core-extension-fapi-ciba/     # FAPI-CIBA拡張
│   └── .../extension/fapi/ciba/
│       └── FapiCibaVerifier.java
│
├── idp-server-core/                         # コア（PAR, JARM実装）
│   └── .../oauth/
│       ├── request/
│       │   └── OAuthPushedRequestParameters.java  # PAR
│       ├── response/
│       │   └── JarmCreatable.java                 # JARM
│       ├── io/
│       │   ├── OAuthPushedRequest.java
│       │   └── OAuthPushedRequestResponse.java
│       └── verifier/extension/
│           └── JarmVerifier.java
│
└── idp-server-control-plane/               # 管理API
    └── .../management/fapi/
        └── FapiConfigManagementApi.java
```

## FAPI Baseline検証

`idp-server-core-extension-fapi/` モジュール内:

```java
public class FapiBaselineVerifier {
    public void verify(
        AuthorizationRequest request,
        Client client
    ) {
        // 1. response_type=code only
        if (!request.responseType().isCode()) {
            throw new InvalidRequestException(
                "fapi_baseline_requires_code_flow"
            );
        }

        // 2. PKCE必須（S256のみ）
        if (!request.hasCodeChallenge()) {
            throw new InvalidRequestException(
                "code_challenge_required"
            );
        }

        if (request.codeChallengeMethod() != CodeChallengeMethod.S256) {
            throw new InvalidRequestException(
                "code_challenge_method_must_be_s256"
            );
        }

        // 3. state必須
        if (!request.hasState()) {
            throw new InvalidRequestException("state_required");
        }

        // 4. nonce必須（OpenID Connect時）
        if (request.scope().contains("openid") &&
            !request.hasNonce()) {
            throw new InvalidRequestException("nonce_required");
        }
    }
}
```

## FAPI Advanced検証

```java
public class FapiAdvanceVerifier {
    public void verify(
        AuthorizationRequest request,
        Client client
    ) {
        // Baseline要件チェック
        fapiBaselineVerifier.verify(request, client);

        // 1. PAR必須
        if (!request.isPushedAuthorizationRequest()) {
            throw new InvalidRequestException(
                "par_required_for_fapi_advanced"
            );
        }

        // 2. JARM必須
        if (!request.hasResponseMode() ||
            !request.responseMode().isJwt()) {
            throw new InvalidRequestException(
                "jarm_required_for_fapi_advanced"
            );
        }

        // 3. mTLS必須
        if (!request.hasMtlsCertificate()) {
            throw new InvalidRequestException(
                "mtls_required_for_fapi_advanced"
            );
        }
    }
}
```

## PAR（Pushed Authorization Requests）

`idp-server-core/oauth/request/` および `oauth/io/` 内:

PAR実装は以下のクラスで構成:
- `OAuthPushedRequestParameters` - PAR処理
- `OAuthPushedRequest` - リクエスト表現
- `OAuthPushedRequestResponse` - レスポンス表現

## JARM（JWT-secured Authorization Response Mode）

`idp-server-core/oauth/response/` 内:

JARM実装は以下のクラスで構成:
- `JarmCreatable` - JARM生成インターフェース
- `JarmVerifier` - JARM検証

## mTLS（Mutual TLS）

`idp-server-core-extension-fapi/` 内:

mTLS実装は以下のクラスで構成:
- `TlsClientAuthAuthenticator` - tls_client_auth方式
- `SelfSignedTlsClientAuthAuthenticator` - self_signed_tls_client_auth方式

## E2Eテスト

```
e2e/src/tests/
├── spec/
│   ├── fapi_baseline.test.js                # FAPI Baseline仕様
│   ├── fapi_advance.test.js                 # FAPI Advanced仕様
│   ├── fapi_ciba.test.js                    # FAPI CIBA仕様
│   ├── rfc9126_par.test.js                  # PAR (RFC 9126)
│   └── jarm.test.js                         # JARM仕様
│
├── usecase/financial-grade/
│   ├── financial-grade-01-transfer-flow.test.js
│   └── financial-grade-02-authentication-device-rule.test.js
│
└── security/
    └── (FAPI関連セキュリティテスト)
```

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-extension-fapi:compileJava
./gradlew :libs:idp-server-core-extension-fapi-ciba:compileJava

# テスト
cd e2e && npm test -- spec/fapi_baseline.test.js
cd e2e && npm test -- spec/fapi_advance.test.js
cd e2e && npm test -- spec/rfc9126_par.test.js
cd e2e && npm test -- usecase/financial-grade/
```

## トラブルシューティング

### PKCE S256エラー
- `code_challenge_method=S256`のみ許可（plainは不可）
- FAPI Baselineでは必須

### PAR request_uri無効
- request_uriの有効期限（90秒）を確認
- 使用済みrequest_uriは再利用不可

### mTLS証明書検証失敗
- クライアント証明書が正しく送信されているか確認
- `TlsClientAuthAuthenticator` の設定を確認

### JARM署名検証失敗
- Authorization Serverの署名鍵（JWK）を確認
- `response`パラメータのJWT形式を確認
