---
name: lead-phase-3
description: Fase 3 do lead-finder — Login no Instagram via Playwright
user-invocable: false
---

# Fase 3 — Login Playwright no Instagram

**FERRAMENTAS:** APENAS Playwright MCP. NUNCA claude-in-chrome. NUNCA instagrapi.

## 3.1 Verificar se ja esta logado

```
browser_navigate: https://www.instagram.com/
```

Espere carregar. Depois:

```
browser_take_screenshot
```

Analise o screenshot:
- Se ve o feed (posts, stories no topo) → JA ESTA LOGADO → pule para 3.4
- Se ve tela de login (campos username/password) → precisa logar → va para 3.2
- Se ve "Accept cookies" → aceite primeiro, depois verifique

## 3.2 Fazer login

As credenciais da conta secundaria sao as mesmas usadas no MCP instagram-lead-mcp.
Pergunte ao usuario se nao souber.

```
browser_click: campo de username (input[name="username"])
browser_type: {username}
```

```
browser_click: campo de password (input[name="password"])  
browser_type: {password}
```

```
browser_click: botao "Log in" / "Entrar"
```

Espere 5 segundos para o login processar.

```
browser_take_screenshot
```

## 3.3 Tratar desafios pos-login

Analise o screenshot apos login:

**Se "Save Your Login Info?" / "Salvar informacoes de login?":**
```
browser_click: "Save Info" / "Salvar informacoes"
```

**Se "Turn on Notifications?" / "Ativar notificacoes?":**
```
browser_click: "Not Now" / "Agora nao"
```

**Se "Security Check" / "Challenge":**
- PARE imediatamente
- Avise o usuario: "Instagram pediu verificacao de seguranca. Resolva no celular e tente novamente."
- Marque no state: login_failed = true

**Se "Suspicious Login Attempt":**
- PARE
- Avise: "Instagram detectou login suspeito. Aguarde e tente novamente."

## 3.4 Confirmar sessao

Navegue para um perfil publico conhecido para confirmar que a sessao funciona:
```
browser_navigate: https://www.instagram.com/instagram/
```

```
browser_take_screenshot
```

Se ve o perfil do @instagram com foto, bio, grid → sessao OK.
Se ve tela de login → sessao falhou, voltar para 3.2.

## 3.5 Salvar no state

Atualize: logged_in = true (ou false se falhou).

## DELAYS NATURAIS

Entre CADA acao no browser, espere 2-3 segundos.
Um humano nao clica instantaneamente. O Playwright pode ser rapido demais.

Use `browser_evaluate` com setTimeout se necessario:
```javascript
browser_evaluate: (() => { return new Promise(r => setTimeout(r, 3000)); })()
```

## CRITERIO DE CONCLUSAO
- Sessao ativa no Instagram via Playwright
- Screenshot confirmando login
- Se falhou: motivo registrado, usuario avisado
