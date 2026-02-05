---
name: generate-apis
description: 基于 yapi mcp 返回的数据生成对应的 API 文件
---

这项技能专注于生成 APIs 文件，包含 request 函数、对应的出入参类型，不同的文件需要放在指定的文件夹下，并且生成的类型文件需要继承或者复用公共的基础类型

用户提供对应的 yapi 文档地址

## 使用指南

- 接口数据使用 `yapi-auto-mcp` 获取，如果遇到没有权限则通知用户配置
- API 请求放在 `packages/services/src` 目录下，使用 `@repo/services` 包能拿到对应的函数，需要按照项目放到对应的文件内
- 类型文件放在 `packages/types/src` 目录下，使用 `@repo/types` 包能拿到对应的函数，需要按照项目放到对应的文件内
- API 格式参考 `examples/fn.ts` 文件
- type 格式参考 `examples/types.ts` 文件

## 公共文件

- 公共 type 文件地址 `packages/types/src/common.ts`

## 关键词

yapi,YAPI,API,接口
