---
name: basjoofan
description:
  "Use when user needs to run api test, performance test, load test, stress test, http test etc.
  当用户需要运行接口测试、性能测试、负载测试、压力测试、HTTP测试等时使用。
  触发词: 接口测试、API测试、性能测试、负载测试、压力测试、HTTP测试"
license: MIT, Apache-2.0
metadata:
  {
    "openclaw":
      {
        "emoji": "🍀",
        "requires": { "bins": ["basjoofan"] },
        "install":
          [
            {
              "id": "get-latest-version",
              "kind": "script",
              "script": 'node -e "const https = require(''https''); https.get(''https://api.github.com/repos/basjoofan/core/releases/latest'', {headers: {''User-Agent'': ''node.js''}}, (res) => {let data = ''''; res.on(''data'', chunk => data += chunk); res.on(''end'', () => {const release = JSON.parse(data); const version = release.tag_name.replace(/^v/, ''''); console.log(version);})}).on(''error'', (err) => {console.error(''Error:'', err.message); process.exit(1);});"',
              "env":
                {
                  "VERSION": "${VERSION}",
                  "ARCH": "${process.arch === 'arm64' ? 'aarch64' : 'x86_64'}",
                  "OS": "${process.platform === 'darwin' ? 'apple-darwin' : process.platform === 'win32' ? 'pc-windows-msvc.exe' : 'unknown-linux-gnu'}",
                },
            },
            {
              "id": "download",
              "kind": "download",
              "url": "https://github.com/basjoofan/core/releases/download/v${VERSION}/basjoofan-${VERSION}-${ARCH}-${OS}",
              "bins": ["basjoofan"],
              "label": "Install basjoofan v${VERSION}",
            },
          ],
      },
  }
---

# API test

通过 `basjoofan test [OPTIONS] [NAME]` 来运行测试脚本。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--tasks, -t` | 并发数量 | 否 | 1 |
| `--duration, -d` | 测试时长（秒）或分钟（例如：60s, 1m） | 否 | - |
| `--number, -n` | 测试次数 | 否 | 1 |
| `--path, -p` | 测试脚本路径 | 否 | 当前路径 |
| `--record, -r` | 是否记录测试结果 | 否 | - |
| `--stat, -s` | 是否输出统计信息 | 否 | false |

## 命令选择决策树

```
用户想运行测试脚本
├─ 接口测试 → basjoofan test name 测试方法名为name的接口测试
├─ 性能测试 → basjoofan test name -t 100 -d 1m 测试方法名为name的接口测试，并发数量为100，测试时长为1分钟
```

## 使用示例
让我们开始一个简单的接口测试，测试方法名为get，这是一个GET请求。
```bash
let host = "httpbin.org";

rq get`
  GET https://{host}/get
`[status == 200]

test get {
  let response = get->;
  response.status
}
```
这个脚本保存为.fan为后缀名的文件，例如get.fan。
如果用户想运行测试脚本
├─ 接口测试 → basjoofan test get 测试方法名为get的接口测试
├─ 性能测试 → basjoofan test get -t 100 -d 1m -s 测试方法名为get的接口测试，并发数量为100，测试时长为1分钟，输出统计信息

这是一个POST请求
```bash
let host = "httpbin.org";

rq post`
  POST https://{host}/post
`[status == 200]

test post {
  let response = post->;
  response.status
}
```
这是一个POST请求，请求体为application/x-www-form-urlencoded格式。
```bash
let host = "httpbin.org";

rq post`
  POST https://{host}/post
Content-Type: application/x-www-form-urlencoded

key: value
`[status == 200]

test post {
  let response = post->;
  response.status
}
```
这是一个POST请求，请求体为multipart/form-data格式。
```bash
let host = "httpbin.org";

rq post`
  POST https://{host}/post
  Content-Type: multipart/form-data

  key: value
  file: @path/to/file
`[status == 200]

test post {
  let response = post->;
  response.status
}
```

这是一个POST请求，请求体为application/json格式。
```bash
let host = "httpbin.org";

rq post`
  POST https://{host}/post
  Content-Type: application/json

  {
    "name": "Gauss",
    "age": 6,
    "address": {
      "street": "19 Hear Sea Street",
      "city": "DaLian"
    },
    "phones": [
      "+86 13098767890",
      "+86 15876567890"
    ]
  }
`[status == 200]

test post {
  let response = post->;
  response.status
}
```