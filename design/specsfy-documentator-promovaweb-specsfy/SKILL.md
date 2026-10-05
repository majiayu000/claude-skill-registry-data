---
name: specsfy-documentator
description: Construir ou reconstruir a documentação técnica completa de uma aplicação em docs/, a partir do código existente e das mudanças recém-implementadas. Use livremente quando o usuário pedir documentação, mapa técnico, arquitetura, UML, fluxos, banco, integrações, testes, frontend, Tailwind ou pacotes; use também obrigatoriamente depois de cada implementação conduzida por specsfy-07-implement. Funciona de forma independente, inclusive em projetos legados Laravel, Node, Next.js, React ou Astro, e preserva conteúdo humano fora dos blocos gerados.
---

# Documentar o sistema

1. Ler instruções locais, `PROJECT.md`, `.specsfy/STACK.md`,
   `.specsfy/RULES.md`, `.specsfy/DATABASE.md`, manifests e código existente.
2. Ler [o padrão documental](references/documentation-standard.md) antes de
   alterar a topologia publicada.
3. Construir toda a documentação, mesmo quando a skill for acionada sem uma
   spec ou implementação recente:

```bash
python3 -B scripts/build_documentation.py --project <raiz>
```

4. Inspecionar os arquivos gerados e corrigir manualmente somente inferências
   que o código não sustente. Não inventar decisões, relações ou integrações.
5. Executar `--check` para provar que a documentação representa o estado atual:

```bash
python3 -B scripts/build_documentation.py --project <raiz> --check
```

6. Preservar conteúdo humano fora dos blocos
   `specsfy:documentator`. Tratar o bloco como projeção reconstruível do código.
7. Registrar na evidência da tarefa o comando, resultado e arquivos atualizados.

## Cobertura obrigatória

Manter em `docs/`:

- portal e mapa de leitura;
- arquitetura, componentes e UML em Mermaid;
- inventário da aplicação e implementações existentes;
- banco e entidades com `erDiagram`;
- fluxos com `flowchart` e `sequenceDiagram`;
- guia e resumo dos testes;
- frontend, views, React e Tailwind;
- bibliotecas e pacotes nativos, de framework, integrados e terceiros, com
  versão, fonte e referência GitHub;
- integrações e variáveis de configuração sem valores sensíveis;
- decisões explícitas e suas fontes.

Para Laravel, mapear rotas, controllers, models, services, jobs, policies,
Blade, migrations e Pest/PHPUnit. Para Node, Next.js, React ou Astro, mapear
páginas, rotas de API, componentes, módulos, scripts e Vitest/Jest/Node Test.

## Limites

- Não copiar segredos, valores de `.env`, dados de produção ou código inteiro.
- Não apresentar heurística como decisão confirmada.
- Não substituir specs, `PROJECT.md` ou arquivos `.specsfy/`; referenciá-los
  como fontes.
- Não exigir rede para construir. Quando o repositório GitHub de um pacote não
  estiver declarado localmente nem for conhecido, publicar uma busca GitHub
  claramente rotulada, em vez de inventar uma URL.
