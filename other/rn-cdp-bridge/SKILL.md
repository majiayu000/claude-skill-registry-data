---
name: rn-cdp-bridge
description: >
  React Native 0.77+에서 제거된 Metro 로그 포워딩을 CDP WebSocket으로 대체하는 런북.
  console.log 출력 복구, 네트워크 요청 모니터링, InspectorProxy 타겟 디스커버리,
  브릿지 스크립트를 통한 터미널 스트리밍을 다룬다.
  release 빌드 크래시(Hermes minify로 스택이 안 풀릴 때)를 debug+Metro로 전환해
  CDP/LogBox로 정확한 에러를 잡는 셋업(디버그 빌드·adb reverse·권한 우회·타겟 선택)도 포함.
  "console.log가 안 보여", "Metro 로그가 안 나와", "RN 로그가 안 찍혀",
  "RN console.log not showing", "Metro logs missing", "CDP 연결",
  "DevTools 연결 안 됨", "RN network debugging", "RN 디버깅 런북",
  "RN 크래시 원인 분석", "release 크래시가 안 잡혀", "debug 빌드로 에러 확인",
  "RedBox 에러 캡처", "화면 진입하면 죽어"
  등에서 트리거.
---

# RN Metro CDP

RN 0.77+에서 Metro console.log 스트리밍이 제거되었다. CDP WebSocket을 통해 console 출력과 네트워크 요청을 터미널로 브릿지하는 런북.

> **공식 근거**: "log forwarding via Metro, originally deprecated in 0.76, is removed in 0.77. We are moving exclusively to the Chrome DevTools Protocol (CDP)." — [React Native 0.77 Blog](https://reactnative.dev/blog/2025/01/21/version-0.77)

## 언제 이 스킬을 쓰는가

| 증상 | 이 스킬? | 대안 |
|------|----------|------|
| console.log가 Metro 터미널에 안 보임 (RN 0.77+) | **O** | — |
| 네트워크 요청을 터미널에서 모니터링하고 싶음 | **O** | — |
| release 빌드에서만 크래시, 스택이 minify돼 안 풀림 | **O** (debug+Metro 전환) | — |
| 화면 진입/네비게이션이 silent하게 무동작 (크래시 아님) | **O** (CDP가 console.error 캡처) | — |
| DevTools GUI로 디버깅하고 싶음 | X | `j` 키 → React Native DevTools |
| VS Code에서 인라인 로그 보고 싶음 | X | Expo Tools / Radon IDE 확장 |
| Expo CLI 프로젝트 | △ | Expo CLI 자체 로그 스트리밍 있음, 네트워크는 이 스킬 유용 |

## 워크플로우

### 0. 디버그 빌드를 Metro에 연결 (타겟이 없거나 release 크래시 추적 시)

release(Hermes + minify) 크래시는 Metro packager sourcemap으로 역매핑되지 않는다 — 크래시 스택의 `index.bundle:1:<col>`은 Hermes 바이트코드 오프셋이라 JS 바이트 오프셋과 안 맞아 `metro-symbolicate`/`source-map`이 `null`을 뱉는다. 정확한 에러 메시지 + 소스 스택은 **debug 빌드 + Metro**에서만 나온다(RedBox/LogBox 화면 + CDP 스트림). 그래서 "release에서만 죽는다"면 먼저 debug로 전환한다.

```bash
yarn start                                            # Metro (백그라운드)
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
adb reverse tcp:8081 tcp:8081                         # 실기기: device→Metro (USB 재연결 시 사라짐)
adb shell monkey -p <pkg> -c android.intent.category.LAUNCHER 1   # 실행 (am start는 BAL로 막힐 수 있음)
```

- **debug appId suffix 주의**: `applicationIdSuffix ".dev"` 등이면 debug는 release와 **별개 패키지**로 설치된다. 타겟/실행/권한 부여 모두 그 `.dev` 패키지로.
- **권한 게이트 우회**: 디버그할 화면이 권한 동의 화면 뒤에 있으면 시스템 다이얼로그를 누르는 대신 `adb shell pm grant <pkg> android.permission.CAMERA`(등 필요한 dangerous 권한)로 미리 부여하면 통과한다. (`requestMultiple`이 전부 granted면 바로 진행.)
- 그 후 debug 앱을 실행하면 `/json/list`에 타겟이 뜬다.

### 1. Target 확인

```bash
curl -s http://localhost:8081/json/list | jq .
```

Metro 포트: RN CLI 기본 `8081`, Expo SDK 50+도 `8081` 고정 (SDK 49 이하는 `19000`–`19002`). Metro 시작 로그에서 확인.

응답에서 `webSocketDebuggerUrl`이 CDP 연결 주소다. 상세 포맷은 `references/inspector-proxy.md` 참조.

**Page 구분**: Page 번호보다 `title`의 "Bridgeless" 키워드나 `reactNative.capabilities.nativePageReloads`로 판별하는 것이 안정적이다 (bridge 스크립트도 이 방식 사용). 일반적으로 Bridgeless page = 메인 RN Bridge (console.log가 여기로 옴), Reanimated UI runtime은 별도 page.

### 2. Bridge 실행

```bash
node "${SKILL_DIR}/scripts/cdp-console.mjs"
node "${SKILL_DIR}/scripts/cdp-console.mjs" --network              # 네트워크 포함
node "${SKILL_DIR}/scripts/cdp-console.mjs" --port 19000 --target iPhone  # Expo + 디바이스 지정
```

스크립트가 target 탐색 → Bridgeless/Hermes 우선 선택 → WebSocket 연결 → 이벤트 스트리밍을 자동 처리한다. 연결 끊김 시 exponential backoff로 재연결.

`SKILL_DIR`이 없으면 스크립트의 절대 경로를 직접 사용. Node 18+에서 동작하며, Node 22 미만에서는 `ws` 패키지가 필요하다.

**스크립트 없이 수동 연결:**

```bash
WS_URL=$(curl -s http://localhost:8081/json/list | jq -r '.[0].webSocketDebuggerUrl')
echo '{"id":1,"method":"Runtime.enable"}' | websocat "$WS_URL"
```

### 3. 공식 GUI 대안

- **React Native DevTools**: Metro에서 `j` 키, 또는 `http://localhost:8081/open-debugger`
- **VS Code**: [Expo Tools](https://github.com/expo/vscode-expo) / [Radon IDE](https://ide.swmansion.com/)

## Gotchas

- **Hermes CDP에서 async/await 불가**: `Runtime.evaluate`로 JS 실행 시 `async/await` 구문을 쓸 수 없다. Promise 체인(`.then()`)으로 작성하고, `awaitPromise: true` 옵션으로 결과를 받을 것.
- **`require`, `global` 없음**: Hermes CDP 컨텍스트에서는 `globalThis`를 사용. Metro의 require는 `globalThis.__r`로 접근 가능하나 불안정.
- **DevTools 동시 연결 경고**: React Native DevTools가 열려 있는 상태에서 bridge를 연결하면 "unsupported debugging client" 경고가 뜨지만 기능은 동작한다.
- **`chrome://inspect` 미지원**: RN 0.76+부터 작동하지 않는다. `j` 키 또는 `/open-debugger` 사용.
- **Flipper가 WebSocket 선점**: Flipper 실행 중이면 CDP 연결 실패. Flipper 종료 후 재시도.
- **Hermes 전용**: JSC(JavaScriptCore) 사용 시 이 워크플로우 불가.
- **Legacy target CDP 제한**: `reactNative.capabilities`가 없는 Legacy target에서는 일부 이벤트 누락 가능.
- **`Network.getResponseBody`는 experimental**: 응답 body 누락될 수 있다.
- **기기에 RN 타겟이 여러 개**: release+debug 동시 설치거나 다른 RN 앱이 떠 있으면 `/json/list`에 타겟이 여럿 잡혀 엉뚱한 앱에 붙는다. `--target <substring>`(deviceName 또는 title=패키지명 부분매칭)으로 우리 앱을 고정.
- **크래시·네비게이션 에러도 CDP로 온다**: console.log뿐 아니라 `console.error`(React 컴포넌트 크래시는 `isComponentError: true` + componentStack)와 `Runtime.exceptionThrown`이 흐른다. React Navigation `The action 'NAVIGATE'/'RESET' ... was not handled` 같은 **silent 무동작**(화면이 안 열림)도 여기서 잡힌다. dev에선 같은 내용이 LogBox(빨간/노란 토스트)·RedBox로도 뜬다 — "화면 진입하면 죽어/안 열려"의 정확한 원인을 CDP/LogBox에서 확인.
- **deprecation 노이즈 필터**: 라이브러리 deprecation 경고(예: Firebase namespaced API)가 `{ name: 'Stack' }` stack 덤프로 스트림을 도배한다. 실제 에러를 찾을 땐 `grep -viE 'deprecated|rnfirebase'`처럼 걸러라.

## 참조

- `references/inspector-proxy.md` — `/json/list` 응답 파싱이나 WebSocket URL 직접 구성 시 참조
- `references/cdp-domains.md` — `consoleAPICalled` args 파싱이나 `Runtime.evaluate` 사용 시 참조
