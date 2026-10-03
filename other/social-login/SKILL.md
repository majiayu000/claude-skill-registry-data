---
name: social-login
description: >
  Social Login Implementation Guide. 소셜 로그인(Google, Apple, Kakao, Naver) 구현 가이드.
  React Native(Expo), Swift, Kotlin, Web 환경. 소셜 로그인, social login, 카카오/네이버/구글/애플
  로그인, KOE205, DEVELOPER_ERROR, keyHash 문제와 실전 gotcha 요청에 사용한다.
---

# Social Login Implementation Guide

소셜 로그인 구현 종합 가이드. Google, Apple, Kakao, Naver 4사를
React Native(Expo), Swift(iOS), Kotlin/Java(Android), Web 환경에서 구현합니다.
실제 프로덕션 삽질 경험에서 추출한 gotcha + 체크리스트 포함.

## Trigger

다음 키워드에 자동 활성화:
- "소셜 로그인", "social login", "OAuth 로그인"
- "카카오 로그인", "네이버 로그인", "구글 로그인", "애플 로그인"
- "kakao login", "naver login", "google sign-in", "apple sign-in"
- "DEVELOPER_ERROR", "KOE205", "keyHash validation"

## 핵심 개념: "프론트만 값을 가지고 있으면 안 되는 거구나?"

> 이것이 소셜 로그인에서 가장 많이 하는 실수입니다.

```
[사용자] → [프론트엔드] → [소셜 프로바이더] → [프론트엔드] → [백엔드] → [DB]
           ① SDK로 로그인    ② 토큰 발급         ③ 토큰 전달    ④ 토큰 검증
```

| 단계 | 프론트엔드 | 백엔드 |
|------|-----------|--------|
| ① 로그인 요청 | SDK로 소셜 로그인 UI 호출 | - |
| ② 토큰 획득 | `idToken` 또는 `accessToken` 받음 | - |
| ③ 토큰 전달 | 백엔드 `/auth/social` API 호출 | - |
| ④ 토큰 검증 | - | 소셜 서버에 직접 확인 (위조 방지) |
| ⑤ JWT 발급 | 우리 앱 JWT 저장 | 사용자 생성/조회 + JWT 생성 |

**왜 백엔드도 키가 필요한가?**
프론트에서 "카카오로 로그인했어요"라고만 하면 누구나 가짜 토큰을 보낼 수 있다.
백엔드가 카카오/구글 서버에 직접 물어봐서 진짜인지 확인해야 한다.

### 프로바이더별 백엔드 검증 방식

| 프로바이더 | 프론트가 보내는 것 | 백엔드 검증 방식 |
|-----------|-------------------|-----------------|
| **Google** | `idToken` (JWT) | JWT의 `aud`(Client ID)가 우리 앱인지 검증 |
| **Apple** | iOS: `idToken` / Android: `authorizationCode` | JWT 서명 검증 (JWKS) / code 교환 |
| **Kakao** | `accessToken` | 카카오 API로 사용자 정보 조회 |
| **Naver** | `accessToken` | 네이버 API로 사용자 정보 조회 |

---

## 플랫폼 × 프로바이더 매트릭스

각 조합마다 설정 방식이 **완전히 다릅니다**.

| | React Native (Expo) | Swift (iOS) | Kotlin (Android) | Web |
|---|---|---|---|---|
| **Google** | `@react-native-google-signin` + `google-services.json` | `GoogleSignIn` pod | `credentials-manager` + `google-services.json` | `gsi/client` JS SDK |
| **Apple** | iOS: `expo-apple-authentication` (네이티브) / Android: 웹 OAuth | `AuthenticationServices` (네이티브) | 웹 OAuth (Service ID 필요) | JS SDK + Service ID |
| **Kakao** | `@react-native-seoul/kakao-login` | `KakaoSDK` pod | `kakao-sdk` gradle | Kakao JS SDK |
| **Naver** | `@react-native-seoul/naver-login` | `NaverThirdPartyLogin` pod | `naver-sdk` gradle | Naver JS SDK |

### iOS vs Android 핵심 차이 (가장 혼란스러운 부분)

```
iOS:  대부분 네이티브 SDK → 설정이 비교적 단순
Android: 서명 키(keystore) 기반 인증 → SHA-1, keyHash 등록 필수
```

| 항목 | iOS | Android |
|------|-----|---------|
| **Google** | `GoogleService-Info.plist` | `google-services.json` + **SHA-1 등록** |
| **Apple** | 네이티브 (자동) | **웹 OAuth** (Service ID + Return URL 필요) |
| **Kakao** | Bundle ID 등록 | **keyHash 등록** (debug/release 각각) |
| **Naver** | URL Scheme 등록 | Package Name + **서명 인증서** |
| **서명 키** | 자동 관리 (Xcode) | **debug.keystore ≠ release.jks** (SHA-1/keyHash 다름!) |

> **초보자 함정**: "iOS에서 되는데 Android에서 안 돼요"는 90% 서명 키 문제입니다.

---

## Provider별 구현 가이드

### 1. Google

#### 개발자 콘솔 설정

1. [Firebase Console](https://console.firebase.google.com/) → 프로젝트 생성
2. Android 앱 추가 → **SHA-1 등록** (debug + release 둘 다!)
3. iOS 앱 추가 → Bundle ID 입력
4. `google-services.json` / `GoogleService-Info.plist` 다운로드
5. [Google Cloud Console](https://console.cloud.google.com/) → API 및 서비스 → 사용자 인증 정보
   - Web Client ID (백엔드 검증용)
   - Android Client ID (SHA-1별로)
   - iOS Client ID

#### SHA-1 확인 방법

```bash
# debug keystore (로컬 개발)
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android

# release keystore (프로덕션)
keytool -list -v -keystore your-release.jks -alias your-alias

# EAS 빌드 keystore
eas credentials  # → Android → Keystore → SHA-1 확인
```

> **GOTCHA**: Firebase에 SHA-1 등록 후 **반드시 `google-services.json`을 다시 다운로드**해야 합니다.
> 안 하면 `oauth_client` 섹션이 비어있어 `DEVELOPER_ERROR`가 납니다.

#### DEVELOPER_ERROR 디버깅 체크리스트

`DEVELOPER_ERROR`는 "설정이 뭔가 안 맞다"는 포괄적 에러입니다. 4곳을 전부 확인하세요:

- [ ] Firebase Console에 SHA-1 등록했나? (debug + release)
- [ ] `google-services.json`을 SHA-1 등록 **후에** 다시 다운로드했나?
- [ ] Google Cloud Console → OAuth 클라이언트에 Android SHA-1이 있나?
- [ ] 코드에서 `webClientId`가 실제로 전달되고 있나? (`console.log`로 확인)

#### 플랫폼별 코드

<details>
<summary>React Native (Expo)</summary>

```typescript
// 설치: npx expo install @react-native-google-signin/google-signin
import { GoogleSignin } from '@react-native-google-signin/google-signin';

GoogleSignin.configure({
  webClientId: 'YOUR_WEB_CLIENT_ID.apps.googleusercontent.com', // 상수 권장
  offlineAccess: true,
});

const googleLogin = async () => {
  await GoogleSignin.hasPlayServices();
  const { data } = await GoogleSignin.signIn();
  const idToken = data?.idToken;
  // → 백엔드로 idToken 전송
  await api.post('/auth/social', { provider: 'google', token: idToken });
};
```

> **GOTCHA**: `process.env.EXPO_PUBLIC_*`는 EAS 클라우드 빌드에서만 주입됩니다.
> 로컬 Gradle 빌드(`expo run:android`)에서는 빈 값! **상수 fallback 필수**.
> ```typescript
> const WEB_CLIENT_ID = process.env.EXPO_PUBLIC_GOOGLE_WEB_CLIENT_ID
>   || 'fallback-value.apps.googleusercontent.com';
> ```

</details>

<details>
<summary>Swift (iOS)</summary>

```swift
// GoogleSignIn pod 설치
import GoogleSignIn

func googleLogin() {
    // iOS 15+: UIApplication.shared.windows는 deprecated — connectedScenes 경유
    guard let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene,
          let presentingVC = scene.keyWindow?.rootViewController else { return }

    GIDSignIn.sharedInstance.signIn(withPresenting: presentingVC) { result, error in
        guard let idToken = result?.user.idToken?.tokenString else { return }
        // → 백엔드로 idToken 전송
        AuthAPI.socialLogin(provider: "google", token: idToken)
    }
}
```

`Info.plist`에 URL Scheme 추가:
```xml
<key>GIDClientID</key>
<string>YOUR_IOS_CLIENT_ID.apps.googleusercontent.com</string>
```

</details>

<details>
<summary>Kotlin (Android)</summary>

```kotlin
// build.gradle: implementation("com.google.android.libraries.identity.googleid:googleid:1.1.1")
// build.gradle: implementation("androidx.credentials:credentials:1.3.0")

val googleIdOption = GetGoogleIdOption.Builder()
    .setFilterByAuthorizedAccounts(false)
    .setServerClientId("YOUR_WEB_CLIENT_ID")
    .build()

val request = GetCredentialRequest.Builder()
    .addCredentialOption(googleIdOption)
    .build()

val credentialManager = CredentialManager.create(context)
val result = credentialManager.getCredential(context, request)
val idToken = (result.credential as GoogleIdTokenCredential).idToken
// → 백엔드로 idToken 전송
```

> `google-services.json`이 `app/` 디렉토리에 있는지 확인.

</details>

<details>
<summary>Web (JavaScript)</summary>

```html
<script src="https://accounts.google.com/gsi/client" async></script>
<div id="g_id_onload"
     data-client_id="YOUR_WEB_CLIENT_ID"
     data-callback="handleGoogleLogin">
</div>
```

```javascript
function handleGoogleLogin(response) {
  const idToken = response.credential;
  fetch('/auth/social', {
    method: 'POST',
    body: JSON.stringify({ provider: 'google', token: idToken }),
  });
}
```

</details>

<details>
<summary>백엔드 (Spring Boot)</summary>

```java
// Google idToken 검증
GoogleIdTokenVerifier verifier = new GoogleIdTokenVerifier.Builder(transport, jsonFactory)
    .setAudience(Arrays.asList(webClientId, androidClientId, iosClientId))
    .build();

GoogleIdToken idToken = verifier.verify(tokenString);
if (idToken != null) {
    GoogleIdToken.Payload payload = idToken.getPayload();
    String email = payload.getEmail();
    String name = (String) payload.get("name");
}
```

> **GOTCHA**: `setAudience`에 **Web + Android + iOS Client ID 전부** 넣어야 합니다.
> 하나라도 빠지면 해당 플랫폼에서 검증 실패.

</details>

---

### 2. Apple

#### 핵심: iOS와 Android는 완전히 다른 흐름

```
iOS:     네이티브 SDK → idToken(JWT) 직접 반환 → 백엔드에서 JWKS 검증
Android: 웹 OAuth → authorization_code 반환 → 백엔드에서 Apple 서버에 code 교환
Web:     JS SDK → authorization_code 또는 idToken → 백엔드 처리
```

> **GOTCHA**: Android에서 받은 `authorization_code`를 `idToken` 필드로 보내면 JWT 파싱 실패 → 401.
> 두 필드를 **반드시 분리**하세요.

#### 개발자 콘솔 설정

1. [Apple Developer](https://developer.apple.com/) → Certificates, Identifiers & Profiles
2. **App ID** 생성 → Sign in with Apple 활성화
3. **Service ID** 생성 (Android/Web용) → Configure:
   - Domains: `yourdomain.com`
   - Return URLs: `https://yourdomain.com/auth/apple/callback`
4. **Keys** 생성 → APNs + Sign in with Apple 체크 → `.p8` 파일 다운로드

> **GOTCHA**: Apple Developer License Agreement에 동의 안 하면 콘솔 기능 전체가 잠깁니다.
> 작업 시작 전 콘솔 접속부터 확인하세요. 연 1회 갱신 필요.

> **GOTCHA**: `.p8` 파일은 **딱 1번만** 다운로드 가능합니다. 분실하면 새 Key 생성 필수.

#### 플랫폼별 코드

<details>
<summary>React Native (Expo)</summary>

```typescript
import * as AppleAuthentication from 'expo-apple-authentication';
import * as WebBrowser from 'expo-web-browser';
import { Platform } from 'react-native';

const appleLogin = async () => {
  if (Platform.OS === 'ios') {
    // iOS: 네이티브
    const credential = await AppleAuthentication.signInAsync({
      requestedScopes: [
        AppleAuthentication.AppleAuthenticationScope.EMAIL,
        AppleAuthentication.AppleAuthenticationScope.FULL_NAME,
      ],
    });
    await api.post('/auth/social', {
      provider: 'apple',
      idToken: credential.identityToken,  // JWT
    });
  } else {
    // Android: 웹 OAuth (Expo Auth Proxy 또는 직접 구현)
    const result = await WebBrowser.openAuthSessionAsync(
      `https://appleid.apple.com/auth/authorize?` +
      `client_id=${SERVICE_ID}&` +
      `redirect_uri=${encodeURIComponent(RETURN_URL)}&` +
      `response_type=code&` +
      `scope=name email&` +
      `response_mode=form_post`,
      RETURN_URL
    );
    if (result.type === 'success') {
      const code = extractCodeFromUrl(result.url);
      await api.post('/auth/social', {
        provider: 'apple',
        authorizationCode: code,  // code ≠ idToken!
      });
    }
  }
};
```

</details>

<details>
<summary>Swift (iOS)</summary>

```swift
import AuthenticationServices

class AppleSignInDelegate: NSObject, ASAuthorizationControllerDelegate {
    func authorizationController(controller: ASAuthorizationController,
                                didCompleteWithAuthorization authorization: ASAuthorization) {
        if let appleIDCredential = authorization.credential as? ASAuthorizationAppleIDCredential,
           let identityToken = appleIDCredential.identityToken,
           let tokenString = String(data: identityToken, encoding: .utf8) {
            // → 백엔드로 idToken 전송
            AuthAPI.socialLogin(provider: "apple", idToken: tokenString)
        }
    }
}

// 로그인 요청
let provider = ASAuthorizationAppleIDProvider()
let request = provider.createRequest()
request.requestedScopes = [.fullName, .email]
let controller = ASAuthorizationController(authorizationRequests: [request])
controller.delegate = self
controller.performRequests()
```

> Apple은 이름/이메일을 **최초 1회만** 줍니다. 놓치면 앱 삭제 후 재설치해야 다시 받을 수 있습니다.

</details>

<details>
<summary>Kotlin (Android) — 웹 OAuth</summary>

```kotlin
// Android에서 Apple 로그인 = 웹 OAuth
val authUrl = "https://appleid.apple.com/auth/authorize?" +
    "client_id=$SERVICE_ID&" +
    "redirect_uri=${URLEncoder.encode(RETURN_URL, "UTF-8")}&" +
    "response_type=code&" +
    "scope=name email&" +
    "response_mode=form_post"

// Custom Tab 또는 WebView로 열기
val intent = CustomTabsIntent.Builder().build()
intent.launchUrl(context, Uri.parse(authUrl))

// redirect 수신 → authorization_code 추출 → 백엔드 전송
```

</details>

<details>
<summary>백엔드 (Spring Boot)</summary>

```java
// iOS: idToken(JWT) 검증
public AppleUser verifyIdToken(String idToken) {
    // Apple JWKS 엔드포인트에서 공개키 가져오기
    String jwksUrl = "https://appleid.apple.com/auth/keys";
    // JWT 서명 검증 + claims 추출
    Claims claims = Jwts.parserBuilder()
        .setSigningKey(applePublicKey)
        .build()
        .parseClaimsJws(idToken)
        .getBody();
    return new AppleUser(claims.getSubject(), claims.get("email", String.class));
}

// Android/Web: authorization_code → 토큰 교환
public AppleTokenResponse exchangeCode(String code) {
    // Apple 토큰 엔드포인트에 POST
    // client_secret은 JWT로 직접 생성 (team_id + key_id + .p8)
    RestTemplate rest = new RestTemplate();
    MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
    params.add("client_id", serviceId);
    params.add("client_secret", generateClientSecret()); // .p8로 JWT 서명
    params.add("code", code);
    params.add("grant_type", "authorization_code");
    return rest.postForObject("https://appleid.apple.com/auth/token", params, AppleTokenResponse.class);
}
```

> **GOTCHA**: Apple `client_secret`은 고정 문자열이 아니라 **`.p8` 키로 서명한 JWT**입니다.
> 만료 6개월. 갱신 로직 필요.

</details>

#### App Store 심사 필수 요구사항

Apple 로그인을 제공하면 **계정 삭제(revoke) 기능이 필수**입니다:

```java
// 백엔드: Apple 토큰 revoke
public void revokeAppleToken(String refreshToken) {
    MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
    params.add("client_id", serviceId);
    params.add("client_secret", generateClientSecret());
    params.add("token", refreshToken);
    params.add("token_type_hint", "refresh_token");
    restTemplate.postForObject("https://appleid.apple.com/auth/revoke", params, Void.class);
}
```

---

### 3. Kakao

#### 개발자 콘솔 설정

1. [카카오 개발자센터](https://developers.kakao.com/) → 내 애플리케이션
2. 앱 생성 → 앱 키 확인:
   - **Native App Key** (모바일 SDK용)
   - **REST API Key** (백엔드 검증용)
3. 플랫폼 등록:
   - Android: 패키지명 + **keyHash** (debug/release 각각)
   - iOS: Bundle ID
   - Web: 도메인
4. **카카오 로그인** 활성화 + **동의항목** 설정 (이메일, 프로필)

#### keyHash 등록

```bash
# debug keyHash (Mac/Linux)
keytool -exportcert -alias androiddebugkey -keystore ~/.android/debug.keystore \
  | openssl dgst -sha1 -binary | openssl base64

# release keyHash
keytool -exportcert -alias your-alias -keystore your-release.jks \
  | openssl dgst -sha1 -binary | openssl base64
```

> **GOTCHA**: `keyHash validation failed`가 나와도 **실제 keyHash 문제가 아닐 수 있습니다**.
> Native App Key가 빈 값이어도 카카오 SDK는 `keyHash validation failed`를 리턴합니다.
> 런타임에 실제 값을 확인하세요:
> ```typescript
> import { getKeyHashAndroid } from '@react-native-seoul/kakao-login';
> const hash = await getKeyHashAndroid();
> Alert.alert('KeyHash', hash); // 이 값을 카카오 콘솔에 등록
> ```

> **GOTCHA (KOE205)**: "잘못된 요청" 에러는 **동의항목 미설정**입니다.
> 카카오 개발자센터 → 동의항목 → 이메일(선택), 프로필(필수) 활성화 필수.

#### 플랫폼별 코드

<details>
<summary>React Native (Expo)</summary>

```typescript
// 설치: npm install @react-native-seoul/kakao-login
// expo prebuild 필요 (네이티브 모듈)
import { login, getProfile } from '@react-native-seoul/kakao-login';

const kakaoLogin = async () => {
  const result = await login();
  // result.accessToken → 백엔드 전송
  await api.post('/auth/social', {
    provider: 'kakao',
    token: result.accessToken,
  });
};
```

`app.json`:
```json
{
  "expo": {
    "plugins": [
      ["@react-native-seoul/kakao-login", {
        "nativeAppKey": "YOUR_NATIVE_APP_KEY"
      }]
    ]
  }
}
```

> **GOTCHA**: fallback 로직(`login()` 실패 시 `login({ useKakaoAccountLogin: true })`)을 넣으면
> 카카오톡 앱 로그인 성공 후 웹 로그인이 또 실행되어 **동의 화면 2번 + 앱 프리징**.
> fallback 없이 하나만 사용하세요.

</details>

<details>
<summary>Swift (iOS)</summary>

```swift
import KakaoSDKAuth
import KakaoSDKUser

// 카카오톡 앱 로그인 가능 여부 확인
if UserApi.isKakaoTalkLoginAvailable() {
    UserApi.shared.loginWithKakaoTalk { (oauthToken, error) in
        guard let accessToken = oauthToken?.accessToken else { return }
        AuthAPI.socialLogin(provider: "kakao", token: accessToken)
    }
} else {
    UserApi.shared.loginWithKakaoAccount { (oauthToken, error) in
        guard let accessToken = oauthToken?.accessToken else { return }
        AuthAPI.socialLogin(provider: "kakao", token: accessToken)
    }
}
```

`Info.plist`:
```xml
<key>LSApplicationQueriesSchemes</key>
<array><string>kakaokompassauth</string><string>kakaolink</string></array>
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array><string>kakao{NATIVE_APP_KEY}</string></array>
  </dict>
</array>
```

</details>

<details>
<summary>Kotlin (Android)</summary>

```kotlin
// build.gradle: implementation("com.kakao.sdk:v2-user:2.20.6")
import com.kakao.sdk.user.UserApiClient

if (UserApiClient.instance.isKakaoTalkLoginAvailable(context)) {
    UserApiClient.instance.loginWithKakaoTalk(context) { token, error ->
        token?.accessToken?.let { sendToBackend("kakao", it) }
    }
} else {
    UserApiClient.instance.loginWithKakaoAccount(context) { token, error ->
        token?.accessToken?.let { sendToBackend("kakao", it) }
    }
}
```

`AndroidManifest.xml`:
```xml
<meta-data android:name="com.kakao.sdk.AppKey" android:value="YOUR_NATIVE_APP_KEY"/>
```

</details>

<details>
<summary>Web (JavaScript)</summary>

```javascript
// <script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.4/kakao.min.js"></script>
Kakao.init('YOUR_JAVASCRIPT_KEY');

Kakao.Auth.authorize({
  redirectUri: 'https://yourdomain.com/auth/kakao/callback',
  scope: 'profile_nickname,account_email',
});

// 콜백 페이지에서 authorization code 추출 → 백엔드 전송
```

</details>

<details>
<summary>백엔드 (Spring Boot)</summary>

```java
// Kakao accessToken으로 사용자 정보 조회
public KakaoUser getKakaoUser(String accessToken) {
    HttpHeaders headers = new HttpHeaders();
    headers.setBearerAuth(accessToken);
    HttpEntity<?> entity = new HttpEntity<>(headers);

    ResponseEntity<Map> response = restTemplate.exchange(
        "https://kapi.kakao.com/v2/user/me",
        HttpMethod.GET, entity, Map.class);

    Map<String, Object> kakaoAccount = (Map) response.getBody().get("kakao_account");
    String email = (String) kakaoAccount.get("email");
    Map<String, Object> profile = (Map) kakaoAccount.get("profile");
    String nickname = (String) profile.get("nickname");
    return new KakaoUser(email, nickname);
}
```

</details>

---

### 4. Naver

#### 개발자 콘솔 설정

1. [네이버 개발자센터](https://developers.naver.com/) → Application → 등록
2. 사용 API: **네아로(네이버 로그인)** 선택
3. 환경 추가:
   - Android: 패키지명 + 다운로드 URL
   - iOS: URL Scheme + Bundle ID
   - Web: 서비스 URL + 콜백 URL
4. **Client ID** + **Client Secret** 확인

> **GOTCHA**: 앱이 "개발 중" 상태이면 **등록된 테스터만 로그인 가능**합니다.
> "한 기기에서 되고 다른 기기에서 안 된다"면 이전 세션 캐시 때문일 수 있습니다.
> 양쪽 모두 로그아웃 후 깨끗한 상태에서 테스트하세요.
>
> **해결**: 네이버 개발자센터 → 멤버관리 → 테스터 ID 추가, 또는 검수 요청.

#### 플랫폼별 코드

<details>
<summary>React Native (Expo)</summary>

```typescript
// 설치: npm install @react-native-seoul/naver-login
import { NaverLogin } from '@react-native-seoul/naver-login';

const naverLogin = async () => {
  const { successResponse } = await NaverLogin.login({
    appName: 'YourApp',
    consumerKey: 'YOUR_CLIENT_ID',
    consumerSecret: 'YOUR_CLIENT_SECRET',
    serviceUrlScheme: 'yourapp',
  });
  if (successResponse) {
    await api.post('/auth/social', {
      provider: 'naver',
      token: successResponse.accessToken,
    });
  }
};
```

</details>

<details>
<summary>Swift (iOS)</summary>

```swift
import NaverThirdPartyLogin

let loginInstance = NaverThirdPartyLoginConnection.getSharedInstance()
loginInstance?.delegate = self
loginInstance?.requestThirdPartyLogin()

// NaverThirdPartyLoginConnectionDelegate
func oauth20ConnectionDidFinishRequestACTokenWithAuthCode() {
    guard let accessToken = loginInstance?.accessToken else { return }
    AuthAPI.socialLogin(provider: "naver", token: accessToken)
}
```

</details>

<details>
<summary>Kotlin (Android)</summary>

```kotlin
// build.gradle: implementation("com.navercorp.nid:oauth:5.10.0")
NaverIdLoginSDK.initialize(context, CLIENT_ID, CLIENT_SECRET, APP_NAME)

val launcher = registerForActivityResult(NaverIdLoginSDK.getContract()) { result ->
    when (result) {
        is NaverIdLoginResult.Success -> {
            val accessToken = NaverIdLoginSDK.getAccessToken()
            sendToBackend("naver", accessToken!!)
        }
        is NaverIdLoginResult.Failure -> { /* 에러 처리 */ }
    }
}
launcher.launch(Unit)
```

</details>

<details>
<summary>Web (JavaScript)</summary>

```javascript
// 네이버 로그인 버튼 생성
var naverLogin = new naver.LoginWithNaverId({
    clientId: "YOUR_CLIENT_ID",
    callbackUrl: "https://yourdomain.com/auth/naver/callback",
    isPopup: false,
    loginButton: { color: "green", type: 3, height: 60 }
});
naverLogin.init();

// 콜백에서 access_token 추출 → 백엔드 전송
```

</details>

<details>
<summary>백엔드 (Spring Boot)</summary>

```java
// Naver accessToken으로 사용자 정보 조회
public NaverUser getNaverUser(String accessToken) {
    HttpHeaders headers = new HttpHeaders();
    headers.setBearerAuth(accessToken);
    HttpEntity<?> entity = new HttpEntity<>(headers);

    ResponseEntity<Map> response = restTemplate.exchange(
        "https://openapi.naver.com/v1/nid/me",
        HttpMethod.GET, entity, Map.class);

    Map<String, Object> naverResponse = (Map) response.getBody().get("response");
    String email = (String) naverResponse.get("email");
    String name = (String) naverResponse.get("name");
    return new NaverUser(email, name);
}
```

</details>

---

## 종합 설정 체크리스트

소셜 로그인 키를 변경하거나 새로 설정할 때, **3곳을 반드시 동시에 확인**하세요.

### 프론트엔드

- [ ] Google: `webClientId` 설정 (상수 fallback 권장)
- [ ] Apple: Service ID (Android/Web용)
- [ ] Kakao: Native App Key
- [ ] Naver: Client ID + Client Secret

### 백엔드

- [ ] Google: Web Client ID + Android Client ID + iOS Client ID
- [ ] Apple: Team ID + Key ID + `.p8` 파일 경로 + Service ID
- [ ] Kakao: REST API Key
- [ ] Naver: Client ID + Client Secret

### 개발자 콘솔

- [ ] Google: Firebase SHA-1 (debug+release) → `google-services.json` 재다운로드
- [ ] Apple: Service ID → Return URL 등록, Keys → `.p8` 발급
- [ ] Kakao: 플랫폼(Android keyHash, iOS Bundle ID) + 동의항목 + 앱 활성화
- [ ] Naver: 환경(Android/iOS/Web) + 콜백 URL + 테스터 등록(개발 중이면)

---

## 실전 디버깅 가이드

### "모든 소셜 로그인이 안 돼요"

→ **공통 원인**부터 확인:
1. 백엔드가 살아있나? (`curl` 확인)
2. 앱 → 백엔드 네트워크 연결 가능한가? (HTTP/HTTPS, cleartext 설정)
3. **프론트-백엔드 키 값이 일치하나?** (가장 흔한 원인)
4. 환경변수가 실제로 주입되고 있나? (`console.log` 또는 `Alert`으로 확인)

### 에러별 빠른 진단

| 에러 | 프로바이더 | 원인 | 해결 |
|------|-----------|------|------|
| `DEVELOPER_ERROR` | Google | SHA-1 미등록 또는 `webClientId` null | SHA-1 등록 + google-services.json 재다운 |
| `KOE205` | Kakao | 동의항목 미설정 | 카카오 콘솔 → 동의항목 활성화 |
| `keyHash validation failed` | Kakao | keyHash 미등록 **또는** Native App Key 빈 값 | 런타임 Alert으로 실제 값 확인 |
| `401 Unauthorized` | Apple (Android) | `authorizationCode`를 `idToken`으로 전송 | 필드 분리 (code ≠ idToken) |
| "개발 중 상태" | Naver | 앱 미검수 + 테스터 미등록 | 테스터 등록 또는 검수 요청 |
| `Network Error` | 전체 | 백엔드 URL 또는 네트워크 | cleartext 허용 + URL 확인 |

### 디버깅 꿀팁: 런타임 값 확인

설정 문제의 90%는 **"내가 넣은 값이 실제로 들어갔는지"** 확인하면 풀립니다:

```typescript
// 임시 디버깅 코드 (해결 후 반드시 삭제)
Alert.alert('Debug', JSON.stringify({
  googleWebClientId: GOOGLE_WEB_CLIENT_ID,
  kakaoAppKey: KAKAO_NATIVE_APP_KEY,
  naverClientId: NAVER_CLIENT_ID,
}, null, 2));
```

---

## 도메인/서버 변경 시 업데이트 포인트

서버 도메인이 바뀌면 (예: `api.example.com` → `api.newdomain.com`):

| 위치 | 변경 항목 |
|------|----------|
| Google Cloud Console | 승인된 JavaScript 출처, 리디렉션 URI |
| Apple Developer | Service ID → Return URL, Domains |
| Kakao 개발자센터 | Web 플랫폼 도메인 |
| Naver 개발자센터 | 서비스 URL, 콜백 URL |
| 백엔드 | `application.yml` redirect URI |
| 프론트엔드 | API base URL |
| Firebase | Authorized domains |

---

## 탈퇴(회원 삭제) 시 소셜 연결 해제

App Store/Play Store 심사에서 **계정 삭제 기능**이 필수입니다.
삭제 시 소셜 연결도 해제해야 합니다:

| 프로바이더 | API | 필수 여부 |
|-----------|-----|----------|
| Google | `https://oauth2.googleapis.com/revoke?token={token}` | 권장 |
| Apple | `https://appleid.apple.com/auth/revoke` (POST) | **필수** (심사 요건) |
| Kakao | `https://kapi.kakao.com/v1/user/unlink` | 권장 |
| Naver | `https://nid.naver.com/oauth2.0/token?grant_type=delete` | 권장 |

---

## 참고: 이 스킬이 만들어진 배경

이 스킬은 멜라토닌 앱 프로젝트(Expo + Spring Boot)에서 2026년 2~3월,
약 한 달간 4개 소셜 로그인을 구현하며 겪은 실전 삽질 경험에서 만들어졌습니다.

초보자가 실제로 물어본 질문들:
- "백엔드도 변경해야 하는구나? 프론트만 값을 가지고 있으면 안되는거구나?"
- "파이어베이스도 내 걸로 해도 되겠지?" → 개발/테스트 단계에서는 OK
- "소셜로그인이 이렇게 어려웠던가?" → 공식문서는 쉬워 보이지만, 4사 × 다중 플랫폼 조합이 복잡도를 폭발시킴
- "iOS에서 되는데 Android에서 안 돼" → 서명 키, 캐시된 세션, 개발 상태 차이

모든 gotcha는 실제 발생한 에러에서 추출했습니다.
