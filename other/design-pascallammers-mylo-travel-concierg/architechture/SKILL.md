---
name: architechture
description: 本项目里面的各种架构设计, 设计中用到的各种概念例如 system, action, view-function, action-function, action-handler, base, component 等的解释
---

## base vs component
这是 polylith 工具里面的概念, base 是一个可以 deploy 的 artifact, 例如 webapp, cli, tui 等.
component 是 base 的 building block, component 会提供一个 interface namespace, 其他 base / component 只能直接 require interface, 不能 require component 里面的其他 namespace.

interface 需要用 defn 的方式暴露函数, 不能用 def 的方式, 并且需要有 docstring.
interface 用 cljc, 同时兼顾前后端

运行
```shell
clj -M:poly info
```
可以检查所有错误.

## system

前后端都使用 integrant 管理 stateful component.
integrant init 返回的整个 map 就叫作 system.
```clojure
(def config {...})
(def system (ig/init config))
```

当一些函数需要使用 python-env 或者 数据库连接 或者 websocket channel 之类的 stateful component 时, 就可以接收 system 作为第一个参数. 然后从 system 中 destruct 需要用的到部分.

## view-function
输入 state 返回 hiccup 数据的函数, 叫作 view-function. 

## action
pure data, 例如
```clojure
[[:event/prevent-default]
 [:table-filter/add-filter {:field field
                            :operator selected-operator
                            :from-value :event/form-data}]]
```
这个例子中有两个 action, 每个 action 都是一个 list, 第一个元素是 action 的类型, 后面是 0 或 n 个 arguments.
其中有一些特殊的值例如这个例子中的 :event/form-data 是个 placeholder. 
placeholder 由 interpolate 函数转换成实际的 value

```clojure
(defn make-interpolate
  "Creates an interpolation function for handling event data with optional extensions.
   
   Parameters:
   - extension-fns: Optional functions to extend the interpolation behavior.
                    Each function should take (event case-key) and return a value if handled, nil otherwise.
   
   Returns: An interpolation function that can be used to process event data"
  [& extension-fns]
  (fn [event data]
    (walk/postwalk
     (fn [x]
       (let [result (or
                     (some #(when-let [result (% event x)]
                              result)
                           extension-fns)
                     (case x
                       :event/target.value (.. event -target -value)
                       :event/target.int-value (parse-int (.. event -target -value))
                       :event/target.checked (.. event -target -checked)
                       :event/clipboard-data (.getData (.. event -clipboardData) "text")
                       :event/target (.. event -target)
                       :event/form-data (some-> event .-target gather-form-data)
                       :event/event event
                       :event/file (or (when-let [files (.-files (.-target event))]
                                         (aget files 0))
                                       :event/file)
                       :query/result event
                       nil))]
         (if (some? result)
           result
           x)))
     data)))
```

因此, action 是 pure 的, 只描述了想要做什么, 和需要什么样的数据.

## action-function
返回多个 actions 的函数, 一般是 hiccup 里面的 :on attribute 里面使用.

## action-handler
view 和 action 都是 pure data. 他们没有任何 effect, 因此需要 action-handler 执行 effect 的部分.
action-handler 的参数是当前的 system 和 interpolate 后的 action.
handler 可以根据 action 的数据修改 store, 或者使用 system 中的其他 stateful effect.
当 store 修改后, replicant 会负责获取新的 state, 然后调用 view-function 渲染更新后的 UI.

## websocket

WebSocket 通信使用 extension function 模式, 允许各个模块定义自己的事件处理函数, 最后在 base 中统一注册.

### 模块定义 WebSocket Extension Function

各个 component 可以在自己的 interface namespace 中定义 WebSocket 事件处理函数:

**后端 (Clojure)**:
```clojure
(defn ws-event-handler
  "WebSocket event handler for component.
   Accepts [system event-msg] and returns non-nil if handled, nil otherwise."
  [system event-msg]
  (let [{:keys [id ?data uid ?reply-fn]} event-msg]
    (case id
      :component/custom-event
      (do
        ;; 处理事件逻辑
        (when ?reply-fn
          (?reply-fn [:component/response "ok"]))
        true)  ; 返回 truthy 表示已处理
      nil)))  ; 返回 nil 表示未处理
```

**前端 (ClojureScript)**:
```clojure
(defn ws-event-handler-frontend
  "Frontend WebSocket event handler for component.
   Accepts [system event-msg] and returns non-nil if handled, nil otherwise."
  [system event-msg]
  (let [{:keys [id ?data]} event-msg
        store (:replicant/store system)]
    (case id
      :component/state-update
      (do
        (swap! store assoc :component/state ?data)
        true)  ; 返回 truthy 表示已处理
      nil)))  ; 返回 nil 表示未处理
```

### 在 Base 中注册 Extension Functions

**后端注册** (`bases/web-app/src/com/zihao/web_app/api.clj`):
```clojure
(defn ws-event-handler [system event-msg]
  (or (xiangqi/ws-event-handler system event-msg)
      (language-learn/ws-event-handler system event-msg)
      ;; 更多模块的 handler...
      ))

(def config
  {:ws/ws-server true
   :ws/event-handler []
   :ws/ws-handler {:ws-server (ig/ref :ws/ws-server)
                   :ws-event-handler (ig/ref :ws/event-handler)}})

(defmethod ig/init-key :ws/event-handler [_ _]
  (fn [event-msg]
    (ws-event-handler nil event-msg)))

(defmethod ig/init-key :ws/ws-handler [_ {:keys [ws-server ws-event-handler]}]
  (when ws-server
    (let [stop-ch (async/chan)
          handler (jm/make-ws-handler-with-extensions ws-event-handler)]
      (handler stop-ch ws-server)
      stop-ch)))
```

**前端注册** (`bases/web-app/src/com/zihao/web_app/main.cljs`):
```clojure
(def config
  {:ws/ws-client true
   :ws/event-handlers [xiangqi/ws-event-handler-frontend
                       language-learn/ws-event-handler-frontend]
   :ws/ws-handler {:ws-client (ig/ref :ws/ws-client)
                   :ws-event-handlers (ig/ref :ws/event-handlers)
                   :store (ig/ref :replicant/store)}})

(defmethod ig/init-key :ws/event-handlers [_ handlers]
  handlers)

(defmethod ig/init-key :ws/ws-handler [_ {:keys [store ws-client ws-event-handlers]}] 
  (when ws-client
    (let [stop-ch (async/chan)
          handler (apply rm1/make-ws-handler-with-extensions ws-event-handlers)]
      (handler stop-ch (assoc ws-client :system {:replicant/store store}))
      {:stop-ch stop-ch})))
```

### 发送 WebSocket 消息

发送 WebSocket 消息需要从 system 中获取 `:ws/ws-server` (后端) 或 `:ws/ws-client` (前端), 它们都包含 `:chsk-send!` 这个 key.

**后端发送** (需要指定 user id):
```clojure
(let [ws-server (:ws/ws-server system)
      send-fn (:chsk-send! ws-server)]
  (send-fn
   "uid"                    ; user id
   [:subscribe/event 1]     ; Event [id data]
   8000))                   ; Timeout (ms)
```

**前端发送** (支持回调):
```clojure
(let [ws-client (:ws/ws-client system)
      send-fn (:chsk-send! ws-client)]
  (send-fn
   [:test/echo {:name "Rich Hickey" :type "Awesome"}]  ; Event [id data]
   8000                                                  ; Timeout (ms)
   (fn [reply]                                           ; Callback function
     (when (sente/cb-success? reply)
       (println reply)))))
```

注意: 后端和前端 `chsk-send!` 的签名不同:
- **后端**: `(chsk-send! uid event timeout)`
- **前端**: `(chsk-send! event timeout callback-fn)`