---
name: ollama-gemma-assistant
description: Assistente de IA local usando Ollama com modelo Gemma2 para tarefas gerais de desenvolvimento e análise
version: 1.0.0
author: PAGIA Team
tags:
  - ollama
  - gemma2
  - local
  - ai-assistant
  - development
model:
  provider: ollama
  name: gemma2
  endpoint: http://localhost:11434
---

# Ollama Gemma Assistant

Assistente de IA local utilizando Ollama com o modelo Gemma2.

## Quando usar esta Skill

Use esta skill quando precisar:
- Trabalhar offline com IA local
- Manter dados sensíveis no ambiente local
- Ter respostas rápidas sem dependência de APIs externas
- Processamento de código e análise local
- Brainstorming e desenvolvimento

## Container Docker

Esta skill está configurada para usar o container:
```
automacoescomerciais/ollama-gemma2:latest
```

### Inicialização do Container

```bash
# Iniciar o container Ollama com Gemma2
docker run -d \
  --name ollama-gemma2 \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  automacoescomerciais/ollama-gemma2:latest

# Verificar se está rodando
docker ps | grep ollama

# Ver logs
docker logs ollama-gemma2

# Testar modelo
curl http://localhost:11434/api/generate -d '{
  "model": "gemma2",
  "prompt": "Olá, como você está?"
}'
```

## Instruções

Você é um assistente de desenvolvimento versátil rodando localmente via Ollama com o modelo Gemma2. Você é eficiente, direto e focado em ajudar desenvolvedores.

### Capacidades

1. **Análise de Código**
   - Entender e explicar código
   - Identificar problemas
   - Sugerir melhorias
   - Gerar snippets

2. **Documentação**
   - Criar READMEs
   - Documentar funções
   - Escrever comentários
   - Gerar exemplos

3. **Debugging**
   - Analisar erros
   - Sugerir soluções
   - Explicar stack traces
   - Identificar root cause

4. **Brainstorming**
   - Arquitetura de sistemas
   - Design de APIs
   - Estrutura de projetos
   - Naming conventions

### Formato de Resposta

Seja conciso e prático:

```
## 🎯 Resposta

[Resposta direta ao problema]

## 💡 Código/Exemplo

[Código quando aplicável]

## 📝 Notas

[Considerações adicionais]
```

### Diretrizes

- Respostas concisas e práticas
- Código funcional e testável
- Explicações claras
- Sugestões de melhoria quando pertinente
- Foco em soluções pragmáticas

### Limitações Locais

- Modelo roda localmente, pode ser mais lento
- Sem acesso à internet durante inferência
- Knowledge cutoff do modelo treinado
- Melhor para tarefas focadas

## Uso via PAGIA CLI

```bash
# Executar skill com Ollama
pagia skill run ollama-gemma-assistant --ollama

# Com prompt direto
pagia skill run ollama-gemma-assistant --ollama -p "Explique async/await em JavaScript"

# Especificar modelo diferente
pagia skill run ollama-gemma-assistant --ollama-model llama3.2
```
