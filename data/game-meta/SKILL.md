---
name: game-meta工具
description: 使用game-meta进行策划表相关的操作，包括导出csv文件、更新game-meta工具
---

# game-meta工具

## 介绍
game-meta是公司内部使用的转表工具，现针对于gforge core2 项目使用。游戏运行所需的csv文件都需要使用game-meta工具导出。
### game-meta使用时需要指定多个参数，重点关注-b和--meta.tag参数
### game-meta在导出csv文件的同时会生成一个meta文件夹干扰git操作
### 默认在d:\work\gamemeta\目录下使用game-meta工具，除非用户明确要求使用其他目录
### 如无明确要求使用我的手机号
### 如无明确要求使用1.1.55版本号，一旦发现用户使用过其他版本号则提示用户更新版本号
### 公司办公普通办公环境无法连接服务器，需要在沙箱中才能成功导出csv文件，如果遇到game-meta连接超时或其他网络相关错误提醒用户在沙箱环境中执行

## 使用示例
windows下载game-meta
```powershell
wget -OutFile game-meta.exe http://gforge-editors.iwgame.com:8081/repository/gforge-editor-tools/game-meta-tool/win/latest/game-meta.exe
```
git bash下载game-meta
```powershell
wget -OutFile game-meta.exe http://gforge-editors.iwgame.com:8081/repository/gforge-editor-tools/game-meta-tool/linux/latest/game-meta.exe
```
导出csv文件
```bat
game-meta.exe serialize -p u01 -b {手机号} --meta.tag f02+{策划表版本号}
```

## 手机号对应关系
15201770947 我
