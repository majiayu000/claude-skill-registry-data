---
name: apk-reverse
description: "分析 APK、DEX、Smali、Android 组件与 JNI 边界时使用。"
---

# Android APK 逆向

## 何时使用

分析 APK、DEX、Smali、Android 组件与 JNI 边界。

## 执行要点

- 建立包名、版本、签名、ABI、SDK 和组件清单，识别 native 库与二次载荷。
- 关联 Java/Smali 调用与 JNI 注册；区别客户端判断、native 逻辑和服务器响应。
- 重建副本时同步检查 provider authority、资源引用和签名；先校验再安装到测试设备。
- 用实际页面或业务输入验证结论，记录 adb 设备与复现条件；首页能进入不等于业务通过。

## 交付与验收

调用链、资源/权限清单、修改差异、设备验证证据。每个结论注明对应输入、版本与证据；运行条件不满足时说明已确认范围与未验证部分。
