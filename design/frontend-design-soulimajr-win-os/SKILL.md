---
name: frontend-design
description: Arquitetura de interfaces e desenvolvimento frontend de alto padrão visual. Inspirada nas diretrizes oficiais da Anthropic (anthropics/frontend-design). Use para criar sites, dashboards e landing pages modernas em Next.js/React/Tailwind, definindo intenção de design, estética marcante (anti-slop), tipografia contrastante e micro-interações antes de codificar.
---

# Habilidade: Frontend Design & UI Architecture

## Filosofia & Princípios Anti-Slop
- **Evitar o "AI Slop":** Rejeitar designs genéricos de IA (gradientes roxo/azul padrão, cards sem personalidade, botões genéricos).
- **Compromisso de Estilo Prévio:** Antes de codificar qualquer componente, defina:
  1. Paleta de cores com semântica e contraste forte.
  2. Par de tipografia (Display marcante + Sans/Mono limpa).
  3. Espaçamentos generosos e hierarquia clara de planos de fundo (background, surface, surface-raised).
- **Micro-interações:** Hover states elegantes, transições suaves (150-250ms), efeitos de foco acessíveis.

## Stack Padrão
- Next.js (App Router), Tailwind CSS v4, Lucide Icons / SVGs sob medida, TypeScript.
- Suporte nativo a Dark Mode com variáveis CSS bem estruturadas.

## Procedimento
1. **Briefing Visual:** Analisar a identidade da marca (`/identidade/visual.md`).
2. **Design Tokens:** Definir ou herdar variáveis de cores, bordas, sombras e raios.
3. **Composição dos Componentes:**
   - Header com backdrop blur.
   - Hero com gancho de alto impacto e CTA primário proeminente.
   - Seções de prova, funcionalidades e FAQ escaneáveis.
4. **Otimização Mobile:** Layout flexível, toque confortável (>48px) e zero transbordamento horizontal.

## Entrega
Código de componentes limpo, modular e tipado em `src/components/` ou arquivo de layout salvo em `/saidas/AAAA-MM-DD/marketing/frontend-<componente>.md`.
