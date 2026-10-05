---
name: specsfy-specialist-laravel
description: Implementar, revisar e operar aplicações Laravel com domínio, HTTP, Eloquent, filas, autorização, migrations e testes. Use quando o projeto contém artisan ou laravel/framework e a tarefa toca rotas, controllers, models, policies, jobs, commands, eventos, cache, banco, Pest ou PHPUnit; não use para PHP sem Laravel.
---

# Laravel

## Fluxo

1. Ler as instruções, a spec ativa e os manifests do projeto consumidor.
2. Descobrir versões e extensões em `composer.json` e `composer.lock`.
3. Mapear a requisição até domínio, persistência, efeitos assíncronos e resposta.
4. Localizar convenções em arquivos irmãos e testes existentes.
5. Definir autorização, validação, transação, idempotência e falhas antes do código.
6. Materializar o teste focal, implementar a menor fatia e refatorar.
7. Executar testes, análise estática, formatter e verificação operacional disponíveis.

## Padrões

- Manter controllers finos e regras de negócio no boundary já adotado.
- Usar Form Requests, policies, resources e bindings quando forem contratos locais.
- Tratar Eloquent como acesso a dados, sem esconder consultas caras ou N+1.
- Projetar jobs idempotentes, com timeout, tentativas, backoff e tratamento de falha.
- Preparar migrations compatíveis com o volume, lock esperado, rollback e deploy misto.
- Nunca confiar em validação do cliente nem autorizar somente na interface.
- Não criar abstração, pacote ou evento sem consumidor e benefício verificável.

## Validação

- Cobrir caminho feliz, autorização, validação, efeitos e falhas relevantes.
- Inspecionar queries quando cardinalidade ou latência importar.
- Verificar queues, scheduler, cache, config e variáveis no ambiente alvo.
- Registrar riscos de dados e comandos operacionais sem executá-los sem autorização.

Leia [references/standards.md](references/standards.md) para padrões detalhados e
fontes oficiais conforme a área alterada.
