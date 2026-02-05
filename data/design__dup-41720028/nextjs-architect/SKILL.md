---
name: nextjs-architect
description: SEMPRE use quando trabalhar com Next.js 15/React 19 + shadcn/ui + Tailwind. Arquiteta apps server-first/feature-first com decisões de estado, cache, forms, segurança e performance.
version: 2.0.0
---

# Nextjs Architect — Modular

Esta skill segue o modelo de modularização da `nestjs-architect`: conteúdo dividido em seções versionadas, checklist e referência rápida.

## ⚠️ PASSO 0: CARREGAR MÓDULOS OBRIGATÓRIOS (SEMPRE PRIMEIRO!)

**ANTES DE FAZER QUALQUER COISA, execute:**

```bash
# 🔴 OBRIGATÓRIOS: Carregar sempre no início
Read .claude/skills/nextjs-architect/sections/activation.md
Read .claude/skills/nextjs-architect/sections/architecture.md
Read .claude/skills/nextjs-architect/sections/data-state-cache.md

# 🟡 SOB DEMANDA: Carregar conforme contexto da tarefa
# - sections/ui-tailwind.md (quando trabalhar com componentes UI/shadcn)
# - sections/forms.md (quando implementar formulários/Server Actions)
# - sections/security.md (quando adicionar auth/roles/validação)
# - sections/performance-dx.md (quando otimizar bundle/Web Vitals)
# - sections/anti-patterns.md (quando revisar código)
# - checklists/quality.md (validação final antes de entregar)
```

**Sem estes módulos obrigatórios, você NÃO tem informação suficiente para arquitetar apps Next.js 15 corretamente.**

**Nota:** Caminhos são relativos à raiz do projeto (onde `.claude/` está localizado).

---

## Como usar

**1) SEMPRE exiba este disclaimer no início da resposta:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 NEXTJS ARCHITECT SKILL ATIVADA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stack: Next.js 15 (App Router), React 19, shadcn/ui
Abordagem: Server-First, Feature-First, RSC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

2) Aplique as seções relevantes (arquitetura, dados/estado/cache, UI/Tailwind, formulários, segurança, performance/DX, anti-patterns) conforme o problema.
3) Formate a resposta com título curto + bullets por área + caminhos em backticks + blocos `ts/tsx` quando houver código.
4) Valide com `checklists/quality.md`; rejeite itens listados em `sections/anti-patterns.md`.
5) Use `SKILL-QUICK-REF.md` para um guia de bolso e `README.md` para visão geral.

## Estrutura

```
.claude/skills/nextjs-architect/
├─ SKILL.md                # instruções de orquestração (este arquivo)
├─ README.md               # visão geral e quando ativar
├─ SKILL-QUICK-REF.md      # gatilhos e árvore base
├─ sections.yaml           # índice das seções
├─ sections/               # conteúdo modular
└─ checklists/quality.md   # checklist final de entrega
```

## Recursos Modulares

### 🔴 Módulos OBRIGATÓRIOS (carregar sempre no PASSO 0):
- `sections/activation.md` → Gatilhos, persona, formato de saída
- `sections/architecture.md` → Estrutura feature-first, server-first patterns
- `sections/data-state-cache.md` → Server Components, RSC, cache strategies

### 🟡 Módulos SOB DEMANDA (carregar quando necessário):
- `sections/ui-tailwind.md` → shadcn/ui, Tailwind semântico, acessibilidade
- `sections/forms.md` → Server Actions, validação, loading states
- `sections/security.md` → Auth (cookies/JWT), CSRF, XSS, rate limiting
- `sections/performance-dx.md` → Bundle optimization, Web Vitals, DX tools
- `sections/anti-patterns.md` → Código para evitar (Client Components desnecessários, etc.)
- `checklists/quality.md` → Checklist de qualidade final

**Quando carregar módulos sob demanda:**
- UI/Tailwind: quando criar/revisar componentes visuais
- Forms: quando implementar formulários com Server Actions
- Security: quando adicionar autenticação, autorização ou validação de input
- Performance: quando otimizar bundle size, Core Web Vitals ou SEO
- Anti-patterns: quando revisar código existente ou fazer code review

## Manutenção

- **Versão:** 2.0.0
- **Criado:** 2025-12-06
- **Atualizado:** 2025-12-12
  - v1.0.0: Versão inicial modular
  - v2.0.0: Adicionado carregamento obrigatório de módulos + disclaimer visível + gatilhos explícitos na description
- **Revisar quando:** Next.js/React atualizar versão major, shadcn/ui atualizar componentes, ou Tailwind 4.0 lançar
