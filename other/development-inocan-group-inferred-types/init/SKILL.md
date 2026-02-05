---
name: init
description: 코드베이스를 분석하여 CLAUDE.md 초기화. 프로젝트 문서화, 아키텍처 개요, 코딩 표준 생성
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Initialize CLAUDE.md

## Instructions
1. 전체 코드베이스 구조 스캔
2. 기술 스택 및 프레임워크 식별
3. 프로젝트 아키텍처 문서화
4. 기존 문서 추출 및 통합
5. 종합적인 CLAUDE.md 생성:
   - Project Overview
   - Architecture (ASCII 다이어그램)
   - Tech Stack
   - Coding Standards
   - Key Files and Directories
   - Development Workflow
   - Sub-agents

## Output
.claude/CLAUDE.md 파일 생성 또는 업데이트
