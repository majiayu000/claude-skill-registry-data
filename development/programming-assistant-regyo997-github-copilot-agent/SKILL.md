---
name: programming-assistant
description: 協助開發者進行程式開發，包含公司 API 設計規範指引和 Spring Boot 專案快速建立。用於：(1) 開發新的 API 端點時、(2) 規劃和設計 API 時、(3) 需要快速建立新的 Spring Boot 專案時、(4) Code Review 時驗證 API 是否符合公司規範時
---

# 程式開發助手技能

## 關於此技能

此技能協助開發者進行程式開發工作，特別是在需要遵循公司標準的場景。提供 API 設計規範指引和 Spring Boot 專案快速建立能力，確保開發過程中的一致性和規範性。

## 此技能提供

1. **API 設計規範** - 公司強制遵循的 API 設計標準，涵蓋命名、結構、錯誤處理、安全性等完整指引
2. **Spring Boot 專案初始化** - 快速建立符合標準結構的 Spring Boot 專案
3. **開發工作流** - 確保團隊所有成員遵循統一的開發標準

## 可用資源

### references/REFERENCE.md - API 設計規範（必讀・強制遵循）

包含「API 設計規範」的完整詳細指引。**這是公司的 API 設計標準，所有 API 開發必須遵循**。

**何時使用：**
- 開發新的 API 端點時
- API 規劃和設計階段
- Code Review 時驗證 API 是否符合規範
- 團隊新成員需要學習公司 API 設計標準時

**包含內容：**
- API 命名慣例、結構規則和設計模式
- 錯誤處理、狀態碼和回應格式的標準定義
- 文檔、版本控制和相容性管理規範
- 安全性、驗證和授權的實作標準

**重要：任何不符合此規範的 API 不予接受。務必在開發前充分理解並遵循本規範。**

### scripts/create_springboot_project.py - Spring Boot 專案建立腳本

提供 Spring Boot 專案自動建立腳本，支援快速初始化項目結構。

**何時使用：**
- 需要開始一個新的 Spring Boot 專案時
- 快速建立微服務或新模組時
- 需要以標準結構初始化多個相關專案時

**功能特性：**
- 自動從 Spring Initializr 下載並解壓縮專案
- 支援批次建立多個 Spring Boot 微服務專案
- 預設建立在 `./project/java` 資料夾下

## 使用指南

1. **API 開發** - 務必先閱讀 REFERENCE.md，確保理解公司 API 規範
2. **建立SpringBoot新專案** - 使用 scripts/create_springboot_project.py 快速初始化 Spring Boot 專案
3. **目錄約定** - Spring Boot 專案建立在 `./project/java` 資料夾，Python 專案建立在 `./project/py` 資料夾
```
