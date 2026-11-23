---
name: code-standards
description: Padrões mínimos de código, testes e segurança para o projeto.
---

# Skill: code-standards

Padrões mínimos. O projeto pode estender em `.agents/AGENTS.md`.

## Código
- Nomes claros; funções curtas com uma responsabilidade.
- Sem código morto, sem comentários que repetem o código.
- Tratamento de erro explícito; nunca engolir exceções.

## Testes
- Toda regra de negócio tem teste.
- Testes rodam com um único comando documentado no handoff.
- Bug corrigido ganha teste que reproduz.

## Segurança
- Validar toda entrada externa.
- Sem segredos no repositório; use variáveis de ambiente.
- Consultas parametrizadas; escapar saída em HTML.

## Git
- Commits pequenos, mensagem no imperativo explicando o porquê.
