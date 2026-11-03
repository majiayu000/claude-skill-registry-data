---
name: REA Reverse Engineering (Binary, Electron, SQLite & Web X-Ray)
description: Especialista em engenharia reversa e auditoria profunda de aplicativos Electron/JS, bancos SQLite, capturas de rede Web (HAR/SAZ -> API Surface) e binários nativos usando morluto/rea (rea-agents).
---

# REA — Reverse Engineer Anything (`morluto/rea` v6.7.0)

Habilidade soberana para inspeção profunda, auditoria de segurança, reconstrução de grafos semânticos, validação de bancos SQLite e engenharia reversa de portais web (bancos de questões, imagens e ERPs escolares como Activesoft).

## 🚀 Capacidades Principais no Áquila Pro

1. **Auditoria de Código, Segurança & Infraestrutura Electron (`analyze-javascript-application` / `trace-javascript-semantics`)**
   - Mapeia o grafo estrutural e semântico completo (`apps/electron/dist` e `dist-renderer`).
   - Rastreia fronteiras de segurança Electron (`contextBridge`, `ipcMain`, `ipcRenderer`, `node:child_process`, timers, EventEmitters e fronteiras de parse/validação).
   - Marca automaticamente conteúdo não confiável (`provenance: { untrusted_content: true }`) contra prompt-injection.

2. **Auditoria de Bancos de Dados SQLite (`inspect-sqlite-database`)**
   - Inspeciona snapshots de `pedagogical_scaffolding.db` e `aquila.db` (`--schema-scope database`), verificando tabelas, índices, triggers, views e integridade WAL sem executar SQL arbitrário.

3. **Engenharia Reversa de Portais Web, Bancos de Questões e Imagens (`inspect-web-network-capture` + `api-surface`)**
   - Analisa capturas `.har` (geradas pelo Playwright / Chrome DevTools) ou `.saz` (Fiddler).
   - Extrai automaticamente a superfície de API (`view: { kind: "api-surface" }`), agrupando rotas REST/GraphQL, templates de URL e sidecars binários (imagens de questões, diagramas, PDFs de provas e boletins do Activesoft).
   - Redige automaticamente credenciais e tokens sensíveis (`--sensitive-value`).

4. **Inspeção de Binários Nativos, .NET, Go, Rust e WebAssembly**
   - `inspect-managed-artifact`, `inspect-go-binary`, `inspect-rust-binary`, `inspect-wasm-artifact`.

## 🛠️ Comandos CLI (`rea` / `rea-agents`)

```powershell
# 1. Verificar capacidades instaladas no host
rea capabilities --json

# 2. Analisar o bundle Electron/JS do Áquila Pro e gerar Evidence JSON
rea analyze-javascript-application "c:/aquila/apps/electron/dist" --json > aquila-electron-evidence.json

# 3. Inspecionar bancos SQLite do Áquila Pro (Inventário Completo + Amostra Segura)
rea inspect-sqlite-database "c:/aquila/apps/electron/src/database/pedagogical_scaffolding.db" --schema-scope database --json
rea inspect-sqlite-database "c:/aquila/apps/electron/src/database/pedagogical_scaffolding.db" --table practice_questions --row-limit 10 --json

# 4. Engenharia Reversa de Portais Web (Activesoft / Portais de Vestibulares ENEM, UFG, UEG, UniRV, UFMG, UnB)
rea inspect-web-network-capture "c:/aquila/logs/portal_session.har" har --json > capture-evidence.json
```

## 🔗 Pipeline Integrado: Playwright HAR ➔ REA (`api-surface`) ➔ `api-anything` / SQLite
Para absorver bancos de questões, imagens e dados de portais externos:
1. Capturar tráfego da navegação com Playwright (`recordHar`).
2. Processar o `.har` com `rea inspect-web-network-capture` para descobrir endpoints ocultos, payloads JSON e hashes SHA-256 de imagens/anexos.
3. Registrar as rotas descobertas no `api-anything` (`Tier 1`) e sincronizar questões/imagens diretamente no `pedagogical_scaffolding.db`.
