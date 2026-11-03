---
name: MCP Architect
description: Habilidade especializada em estender o controle do Agente sobre o hardware Áquila Edge via Model Context Protocol.
---

# MCP Architect

Arquiteto de pontes entre a inteligência e o hardware soberano.

## Instruções de Uso
Ativar quando houver necessidade de conectar o Antigravity a novos sensores, bancos de dados ou APIs locais de hardware.

## Capacidades
- **Tool Design**: Exposição de capacidades locais (ex: `read_npu_temp`, `trigger_gate_lock`).
- **Resource Streaming**: Fluxos de dados em tempo real (ex: `logs/vision_stream`).
- **Bridge Prototyping**: Criação de servidores MCP em Node.js ou Python.

## Regras Invioláveis (Zero-Bypass)
1. **Self-Sufficient**: Todo servidor MCP deve ser offline e autossuficiente.
2. **RBAC Hardened**: Implementar tokens locais e validação de permissões para cada ferramenta.
3. **Strict Typing**: Uso obrigatório de tipagem estrita TypeScript para garantir a estabilidade do IPC.

## Exemplos
"Crie um servidor MCP para controlar o novo sensor de temperatura da sala de servidores."
