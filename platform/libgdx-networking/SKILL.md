---
name: libgdx-networking
description: Use when writing libGDX Java/Kotlin code involving HTTP requests, TCP sockets, or Gdx.net. Use when debugging cross-platform networking, response threading issues, or choosing between libGDX Net and third-party HTTP libraries.
---

# libGDX Networking

Quick reference for `com.badlogic.gdx.Net` and `com.badlogic.gdx.net.*`. Covers HTTP requests, TCP sockets, HttpRequestBuilder, and platform differences.

## Net Interface

Access via `Gdx.net`. Two capabilities: HTTP requests and TCP sockets.

```java
// HTTP
Gdx.net.sendHttpRequest(request, listener);    // async — response via listener
Gdx.net.cancelHttpRequest(request);            // void
Gdx.net.isHttpRequestPending(request);         // boolean

// TCP Sockets
Gdx.net.newServerSocket(Net.Protocol.TCP, port, hints);           // ServerSocket
Gdx.net.newServerSocket(Net.Protocol.TCP, hostname, port, hints); // overload with bind address
Gdx.net.newClientSocket(Net.Protocol.TCP, host, port, hints);     // Socket

// Browser
Gdx.net.openURI("https://example.com");       // opens system browser, returns boolean
```

`Net.Protocol` is an enum with **only `TCP`** — no UDP support.

## HTTP Requests

### Net.HttpRequest

```java
Net.HttpRequest request = new Net.HttpRequest(Net.HttpMethods.GET);
request.setUrl("https://api.example.com/data");
request.setHeader("Accept", "application/json");
request.setTimeOut(5000);                      // millis — NOTE: capital O in TimeOut
request.setFollowRedirects(true);              // default: true
request.setIncludeCredentials(false);          // for GWT CORS cookies

// POST with string body
Net.HttpRequest post = new Net.HttpRequest(Net.HttpMethods.POST);
post.setUrl("https://api.example.com/submit");
post.setHeader("Content-Type", "application/json");
post.setContent("{\"key\": \"value\"}");

// POST with stream body
post.setContent(inputStream, contentLength);   // InputStream + long
```

**Gotchas:**
- Spelling is `setTimeOut` (capital O), **NOT** `setTimeout`. The getter is `getTimeOut()`.
- There is no `setBody()` — the method is `setContent()`.
- There is no `setMethod()` on HttpRequest for changing method after construction — wait, there IS: `setMethod(String)` exists, but prefer the constructor.
- `HttpRequest` implements `Poolable` with a `reset()` method for object pool reuse.

### Net.HttpMethods Constants

`Net.HttpMethods` is an interface used as a constant holder (not an enum):

| Constant | Value |
|---|---|
| `GET` | `"GET"` |
| `POST` | `"POST"` |
| `PUT` | `"PUT"` |
| `DELETE` | `"DELETE"` |
| `PATCH` | `"PATCH"` |
| `HEAD` | `"HEAD"` |

**Always use these constants.** On Desktop/Android/iOS, `HttpURLConnection.setRequestMethod()` is case-sensitive and requires uppercase. Passing `"get"` throws `ProtocolException`.

### Sending and Handling Responses

```java
Gdx.net.sendHttpRequest(request, new Net.HttpResponseListener() {
    @Override
    public void handleHttpResponse(Net.HttpResponse httpResponse) {
        int status = httpResponse.getStatus().getStatusCode();
        String body = httpResponse.getResultAsString();

        // CRITICAL: This callback is NOT on the GL thread!
        Gdx.app.postRunnable(() -> {
            label.setText(body);  // safe to touch Scene2D/GL here
        });
    }

    @Override
    public void failed(Throwable t) {
        Gdx.app.postRunnable(() -> {
            Gdx.app.error("Net", "Request failed", t);
        });
    }

    @Override
    public void cancelled() {
        // Request was cancelled via cancelHttpRequest()
    }
});
```

### CRITICAL: Callback Threading

On Desktop, Android, and iOS, **response callbacks run on a background thread** (the internal `NetThread` pool), NOT the GL/render thread. Any code that touches OpenGL state, SpriteBatch, Scene2D actors, or game state **must** be wrapped in `Gdx.app.postRunnable()`.

On GWT, callbacks run on the main JS event loop (which is the render thread), but write code as if they don't — always use `postRunnable()` for cross-platform safety.

### Net.HttpResponse

```java
String body    = response.getResultAsString();  // String
byte[] bytes   = response.getResult();          // byte[] — NOTE: NOT getResultAsBytes()
InputStream is = response.getResultAsStream();  // InputStream

HttpStatus status = response.getStatus();
int code = status.getStatusCode();              // e.g. 200

String header = response.getHeader("Content-Type");            // single header
Map<String, List<String>> all = response.getHeaders();         // all headers
```

**Gotchas:**
- The byte[] method is `getResult()`, **NOT** `getResultAsBytes()` — this does not exist.
- `getResult()` and `getResultAsString()` may only be called **once** per response (documented limitation).
- `HttpStatus` is `com.badlogic.gdx.net.HttpStatus` (standalone class), not an inner class of `Net`. It has standard constants like `HttpStatus.SC_OK` (200), `HttpStatus.SC_NOT_FOUND` (404), etc.
- The listener parameter on `sendHttpRequest` is `@Null` — passing null is allowed (fire-and-forget).

## HttpRequestBuilder

Fluent builder for constructing `Net.HttpRequest`. Located in `com.badlogic.gdx.net`.

```java
// Static configuration (set once, affects all subsequent builds)
HttpRequestBuilder.baseUrl = "https://api.example.com";  // prepended to all URLs
HttpRequestBuilder.defaultTimeout = 5000;                 // millis, default: 1000

HttpRequestBuilder builder = new HttpRequestBuilder();

// GET request
Net.HttpRequest get = builder.newRequest()
    .method(Net.HttpMethods.GET)
    .url("/users/123")              // becomes "https://api.example.com/users/123"
    .timeout(3000)
    .header("Accept", "application/json")
    .build();

// POST with JSON body
Net.HttpRequest post = builder.newRequest()
    .method(Net.HttpMethods.POST)
    .url("/users")
    .jsonContent(myObject)          // sets Content-Type: application/json, serializes via Json
    .build();

// POST with form data
Map<String, String> params = new HashMap<>();
params.put("username", "alice");
params.put("password", "secret");
Net.HttpRequest form = builder.newRequest()
    .method(Net.HttpMethods.POST)
    .url("/login")
    .formEncodedContent(params)     // sets Content-Type: application/x-www-form-urlencoded
    .build();

// Basic authentication
Net.HttpRequest auth = builder.newRequest()
    .method(Net.HttpMethods.GET)
    .url("/protected")
    .basicAuthentication("user", "pass")  // sets Authorization: Basic header
    .build();
```

### Builder Methods

| Method | Notes |
|---|---|
| `newRequest()` | Must call first. Throws `IllegalStateException` if called twice without `build()`. Applies `defaultTimeout`. |
| `method(String)` | Use `Net.HttpMethods` constants |
| `url(String)` | **Prepends `baseUrl`** — set `baseUrl = ""` to disable |
| `timeout(int millis)` | |
| `header(String name, String value)` | |
| `content(String)` | Raw string body |
| `content(InputStream, long)` | Stream body |
| `jsonContent(Object)` | Serializes via `com.badlogic.gdx.utils.Json`, sets Content-Type header |
| `formEncodedContent(Map<String, String>)` | URL-encodes params, sets Content-Type header |
| `basicAuthentication(String user, String pass)` | Base64-encoded Authorization header |
| `followRedirects(boolean)` | |
| `includeCredentials(boolean)` | For GWT CORS |
| `build()` | Returns `Net.HttpRequest`, resets builder |

**Gotchas:**
- `url()` silently prepends `baseUrl`. If `baseUrl` is non-empty and you pass a full URL, you get a mangled URL.
- `jsonContent()` uses a static `Json` instance — configure it via `HttpRequestBuilder.json` if you need custom serialization.
- `newRequest()` must be called before each request. Calling it twice without `build()` throws.

## TCP Sockets

Socket I/O is **blocking** — never use on the render thread.

```java
// Server
ServerSocketHints serverHints = new ServerSocketHints();
serverHints.acceptTimeout = 0;   // 0 = block forever; default: 5000ms
ServerSocket server = Gdx.net.newServerSocket(Net.Protocol.TCP, 9090, serverHints);

// Accept clients on a background thread
new Thread(() -> {
    while (running) {
        SocketHints clientHints = new SocketHints();
        Socket client = server.accept(clientHints);  // blocks until connection
        handleClient(client);
    }
}).start();

// Client
SocketHints hints = new SocketHints();
hints.connectTimeout = 5000;     // default: 5000ms
hints.tcpNoDelay = true;         // default: true
hints.keepAlive = true;          // default: true
Socket socket = Gdx.net.newClientSocket(Net.Protocol.TCP, "example.com", 9090, hints);

InputStream in  = socket.getInputStream();
OutputStream out = socket.getOutputStream();
String remote   = socket.getRemoteAddress();
boolean alive   = socket.isConnected();

socket.dispose();   // MUST dispose — Socket extends Disposable
server.dispose();   // ServerSocket also extends Disposable
```

### SocketHints Fields

| Field | Type | Default |
|---|---|---|
| `connectTimeout` | int | 5000 |
| `keepAlive` | boolean | true |
| `tcpNoDelay` | boolean | true |
| `socketTimeout` | int | 0 (no read timeout) |
| `sendBufferSize` | int | 4096 |
| `receiveBufferSize` | int | 4096 |
| `linger` | boolean | false |
| `lingerDuration` | int | 0 |
| `trafficClass` | int | 0x14 |
| `performancePrefConnectionTime` | int | 0 |
| `performancePrefLatency` | int | 1 |
| `performancePrefBandwidth` | int | 0 |

### ServerSocketHints Fields

| Field | Type | Default |
|---|---|---|
| `acceptTimeout` | int | 5000 |
| `backlog` | int | 16 |
| `reuseAddress` | boolean | true |
| `receiveBufferSize` | int | 4096 |
| `performancePrefConnectionTime` | int | 0 |
| `performancePrefLatency` | int | 1 |
| `performancePrefBandwidth` | int | 0 |

## openURI

```java
boolean opened = Gdx.net.openURI("https://example.com");
```

Opens the URL in the platform's default browser/handler. Returns `false` if known to have failed.

## Pixmap.downloadFromUrl

Convenience method for downloading images — uses Net internally:

```java
Pixmap.downloadFromUrl("https://example.com/image.png", new Pixmap.DownloadPixmapResponseListener() {
    @Override
    public void downloadComplete(Pixmap pixmap) {
        // Already on GL thread (internally posted via postRunnable) — safe to use directly
        texture = new Texture(pixmap);
    }

    @Override
    public void downloadFailed(Throwable t) {
        // Called on background thread — use postRunnable for GL/UI operations
        Gdx.app.postRunnable(() -> Gdx.app.log("Download", "Failed", t));
    }
});
```

## Platform Differences

| Feature | Desktop (LWJGL3) | Android | iOS (RoboVM) | GWT/HTML5 |
|---|---|---|---|---|
| HTTP requests | Yes | Yes | Yes | Yes (XMLHttpRequest) |
| TCP sockets | Yes | Yes | Yes | **No** (throws) |
| `getResult()` (bytes) | Yes | Yes | Yes | **No** (throws) |
| `getResultAsStream()` | Yes | Yes | Yes | **No** (throws) |
| `getResultAsString()` | Yes | Yes | Yes | Yes |
| Callback thread | Background | Background | Background | Main (JS event loop) |
| INTERNET permission | N/A | **Required** in AndroidManifest.xml | N/A | N/A |
| CORS restrictions | N/A | N/A | N/A | **Yes** — same-origin policy |
| HTTPS required | No | No | **Effectively yes** (ATS) | Depends on page |
| `setFollowRedirects(false)` | Yes | Yes | Yes | **Throws** `IllegalArgumentException` |

**Android:** Add `<uses-permission android:name="android.permission.INTERNET"/>` to `AndroidManifest.xml`.

**iOS:** App Transport Security (ATS) blocks plain HTTP by default. Use HTTPS or configure ATS exceptions in `Info.plist`.

**GWT:** Only `getResultAsString()` works. `getResult()` and `getResultAsStream()` throw `GdxRuntimeException`. Sockets throw `UnsupportedOperationException`. Use `setIncludeCredentials(true)` for cross-origin requests needing cookies.

## When to Use libGDX Net vs Third-Party

| | libGDX Net | OkHttp / Retrofit |
|---|---|---|
| **Cross-platform** | All backends including GWT | Desktop + Android only |
| **Features** | Basic HTTP, TCP sockets | Connection pooling, interceptors, streaming, WebSocket |
| **Complexity** | Simple | Full-featured |
| **Recommendation** | Simple REST calls, cross-platform games | Complex networking, Desktop/Android-only projects |

For JSON parsing of responses, use libGDX's `com.badlogic.gdx.utils.Json` class. `HttpRequestBuilder.jsonContent()` already uses it for serialization.

**DO NOT use** `java.net.HttpURLConnection` or `java.net.URL` directly — these are not available on GWT and bypass libGDX's threading model.

## Common Mistakes

1. **Processing response data off the GL thread** — `handleHttpResponse` runs on a background thread (Desktop/Android/iOS). Touching SpriteBatch, Scene2D, or game state without `Gdx.app.postRunnable()` causes crashes or silent corruption.
2. **Using `setTimeout` (lowercase o)** — The method is `setTimeOut` (capital O). `setTimeout` does not exist and will not compile.
3. **Calling `getResultAsBytes()`** — This method does not exist. The byte[] method is `getResult()`. The string method is `getResultAsString()`.
4. **Inventing `Gdx.net.httpGet(url)` or synchronous helpers** — No convenience methods exist. You must construct `Net.HttpRequest` and use an async listener.
5. **Using sockets on GWT** — `newServerSocket` and `newClientSocket` throw `UnsupportedOperationException` on GWT. Design socket-dependent features with a platform check.
6. **Forgetting INTERNET permission on Android** — Network calls silently fail or throw without `<uses-permission android:name="android.permission.INTERNET"/>` in AndroidManifest.xml.
7. **Passing lowercase HTTP methods** — `new Net.HttpRequest("get")` throws `ProtocolException` on Desktop/Android/iOS. Always use `Net.HttpMethods.GET` etc.
8. **Forgetting to dispose sockets** — Both `Socket` and `ServerSocket` extend `Disposable`. Leaking them leaks OS file descriptors.
9. **Calling `getResultAsString()` twice on the same response** — May only be called once per response. Store the result in a variable.
10. **Socket I/O on the render thread** — Socket reads/writes are blocking. Use a dedicated thread or the application freezes.
11. **Ignoring `baseUrl` in HttpRequestBuilder** — `url()` prepends `HttpRequestBuilder.baseUrl` to every URL. Passing a full URL when `baseUrl` is set produces a mangled URL. Set `baseUrl = ""` to disable.
12. **Using `java.net.HttpURLConnection` directly** — Not cross-platform (fails on GWT), bypasses libGDX's thread pool, and requires manual thread management. Use `Gdx.net` for portable networking.
