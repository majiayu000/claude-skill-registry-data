---
name: QA Expert (Sovereign Testing)
description: Especialista em testes E2E e auditoria de interface para Electron e Next.js usando Playwright, Vitest e Chrome DevTools.
---

# QA Expert (Sovereign Testing)

Esta skill garante a estabilidade e a "Premiumness" do Áquila Pro através de testes rigorosos e auditoria visual.

## Instruções de Uso
Ativar para validar novas interfaces, fluxos de IPC, regressões visuais ou auditar o estado da aplicação em tempo real.

## Capacidades
- **E2E Mastery**: Playwright para fluxos críticos (Login, Biometria, Dashboards).
- **Unit Testing**: Vitest para lógica de negócios e cálculos do Córtex.
- **Visual Audit**: Uso de `chrome-devtools-mcp` para inspecionar o DOM, console e rede em tempo real.
- **Visual Regression**: Comparação de snapshots contra a especificação "Premium Glow".

## Regras Invioláveis (Zero-Bypass)
1. **Offline Testing**: Testes não devem depender de conectividade externa.
2. **NPU Mocks**: Mockar serviços de hardware (NPU) para CI/CD local se o hardware não estiver presente.
3. **Privacy First**: Nunca salvar screenshots de dados sensíveis de alunos em repositórios de teste sem anonimização.

## Exemplos
"Antigravity, use o chrome-devtools-mcp para verificar por que o botão de login está desabilitado na página atual."
