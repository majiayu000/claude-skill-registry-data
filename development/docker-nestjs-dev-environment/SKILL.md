---
name: "Docker + NestJS Dev Environment"
description: "Configure e otimize ambientes de desenvolvimento Docker para projetos NestJS com hot-reload, persistência de dados, health checks e debugging eficiente."
---

# Docker + NestJS Development Environment Skill

Esta Skill orienta a configuração de ambientes Docker otimizados para desenvolvimento de aplicações NestJS, com foco em produtividade, hot-reload, debugging e boas práticas de containerização.

## Objetivo

Configurar e manter ambientes Docker eficientes para desenvolvimento NestJS, garantindo:
- Hot-reload automático de código TypeScript
- Persistência adequada de dados de desenvolvimento
- Integração com ferramentas de debug
- Performance otimizada para ciclos rápidos de desenvolvimento
- Separação clara entre ambientes dev, test e CI

## Quando usar

Ative esta Skill quando o usuário:
- Solicitar configuração de Docker para ambiente de desenvolvimento NestJS
- Pedir otimização de performance em ambiente Docker local
- Questionar sobre hot-reload, volumes ou debugging em containers
- Precisar configurar docker-compose para desenvolvimento
- Mencionar problemas de performance ou lentidão em Docker dev
- Solicitar integração com bancos de dados, Redis, RabbitMQ em desenvolvimento

**NÃO use esta Skill para**:
- Configuração de ambientes de produção (use práticas de multi-stage build específicas)
- Deploy em cloud ou orquestradores (Kubernetes, ECS, etc.)
- Otimização de imagens para produção

## Entradas esperadas

- `tipo_projeto`: NestJS (versão, dependências principais)
- `servicos_externos`: Lista de serviços necessários (PostgreSQL, MySQL, Redis, RabbitMQ, etc.)
- `estrutura_atual`: Arquivos Docker existentes (se houver) e estrutura do projeto
- `problemas_atuais`: Descrição de problemas de performance ou configuração (opcional)

## Saídas esperadas

- Dockerfile otimizado para desenvolvimento
- docker-compose.yaml configurado para desenvolvimento local
- docker-compose.dev.yaml com overrides para persistência
- Script de inicialização (.docker/start.sh)
- Arquivo .dockerignore completo
- Instruções de uso e comandos úteis
- Explicação das decisões arquiteturais

## Passo a passo do fluxo

### 1. Análise do Projeto

Analise a estrutura do projeto NestJS:
- Leia package.json para identificar dependências
- Verifique estrutura de diretórios (src/, test/, etc.)
- Identifique variáveis de ambiente necessárias
- Liste serviços externos requeridos (databases, message queues, caches)

### 2. Criação do Dockerfile de Desenvolvimento

Crie um Dockerfile otimizado para desenvolvimento com as seguintes características:

**Princípios obrigatórios**:
- Use imagem `node:20.5.1-slim` (ou versão apropriada do projeto)
- Instale `@nestjs/cli` globalmente para comandos nest
- Defina `USER node` para segurança
- Use `WORKDIR /home/node/app`
- Não faça build no Dockerfile de dev (use volume mounts)
- Use `CMD` que mantém container ativo (tail -f /dev/null ou npm run start:dev)

**Template base**:
```dockerfile
FROM node:20.5.1-slim

# Instalar NestJS CLI globalmente
RUN npm install -g @nestjs/cli@10.1.17

# Segurança: usuário não-root
USER node

# Diretório de trabalho
WORKDIR /home/node/app

# Manter container ativo para desenvolvimento
CMD ["tail", "-f", "/dev/null"]
```

**Explique ao usuário**:
- Por quê usar imagem slim (redução de 80% no tamanho)
- Importância de USER node para segurança
- Por quê não instalar dependências no Dockerfile de dev (volume mount faz isso)

### 3. Criação do docker-compose.yaml Base

Configure docker-compose.yaml com:

**Serviço da Aplicação**:
```yaml
services:
  app:
    build: .
    command: ./.docker/start.sh
    ports:
      - "3000:3000"
    volumes:
      - .:/home/node/app                    # Hot-reload
      - /home/node/app/node_modules         # Volume anônimo (performance)
      - '/etc/timezone:/etc/timezone:ro'
      - '/etc/localtime:/etc/localtime:ro'
    extra_hosts:
      - "host.docker.internal:host-gateway" # Acesso ao host
    env_file:
      - ./envs/.env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
```

**Decisões críticas a explicar**:

1. **Volume anônimo para node_modules**:
   ```yaml
   volumes:
     - .:/home/node/app
     - /home/node/app/node_modules  # ✅ CRUCIAL
   ```
   - **Por quê**: Evita conflito entre node_modules do host e do container
   - **Problema sem isso**: npm install no container seria sobrescrito pelo volume mount
   - **Ganho de performance**: node_modules fica em filesystem Docker (mais rápido)

2. **host.docker.internal**:
   ```yaml
   extra_hosts:
     - "host.docker.internal:host-gateway"
   ```
   - **Por quê**: Permite app no container acessar serviços no host
   - **Use case**: Debugger na IDE, serviços locais não containerizados

3. **Timezone sync**:
   ```yaml
   volumes:
     - '/etc/timezone:/etc/timezone:ro'
     - '/etc/localtime:/etc/localtime:ro'
   ```
   - **Por quê**: Logs com timestamp correto, agendamentos consistentes

### 4. Configuração de Serviços Externos

Para cada serviço externo necessário, configure com health checks:

**PostgreSQL**:
```yaml
db:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: ${DB_DATABASE:-dev_db}
    POSTGRES_USER: ${DB_USER:-dev_user}
    POSTGRES_PASSWORD: ${DB_PASSWORD:-dev_pass}
  ports:
    - "${DB_PORT:-5432}:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-dev_user}"]
    interval: 5s
    timeout: 3s
    retries: 10
    start_period: 30s
  networks:
    - backend
```

**MySQL**:
```yaml
db:
  image: mysql:8.0.30-debian
  environment:
    MYSQL_DATABASE: ${DB_DATABASE:-dev_db}
    MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:-dev_pass}
  ports:
    - "${DB_PORT:-3306}:3306"
  volumes:
    - mysql_data:/var/lib/mysql
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u$$MYSQL_USER", "-p$$MYSQL_ROOT_PASSWORD"]
    interval: 5s
    timeout: 3s
    retries: 10
    start_period: 30s
  networks:
    - backend
```

**Redis**:
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "${REDIS_PORT:-6379}:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s
    timeout: 3s
    retries: 10
  networks:
    - backend
```

**RabbitMQ**:
```yaml
rabbitmq:
  image: rabbitmq:3-management-alpine
  environment:
    RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER:-dev_user}
    RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS:-dev_pass}
  ports:
    - "${RABBITMQ_PORT:-5672}:5672"
    - "${RABBITMQ_MGMT_PORT:-15672}:15672"
  healthcheck:
    test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
    interval: 5s
    timeout: 3s
    retries: 10
  networks:
    - backend
```

**Explique ao usuário**:
- **Health checks são OBRIGATÓRIOS**: Garante que app só inicia após DB estar pronto
- **Volumes nomeados**: Persistência de dados entre restarts
- **Portas expostas**: Permite acesso direto do host para debugging
- **Variáveis com defaults**: Facilita setup inicial

### 5. Criação do Script de Inicialização

Crie `.docker/start.sh`:

```bash
#!/bin/bash

# Verifica se node_modules existe e se package.json foi modificado
if [ ! -d "node_modules" ] || [ package.json -nt node_modules ]; then
  echo "📦 Instalando dependências..."
  npm ci
fi

echo "🚀 Iniciando aplicação em modo desenvolvimento..."
npm run start:dev
```

**Torne o script executável**:
```bash
chmod +x .docker/start.sh
```

**Explique ao usuário**:
- **npm ci vs npm install**:
  - `npm ci` é mais rápido e determinístico
  - Usa versões exatas do package-lock.json
  - Limpa node_modules antes de instalar
- **Verificação de package.json**:
  - Evita reinstalar dependências desnecessariamente
  - Melhora tempo de startup em 80-90%

### 6. Criação do Override de Desenvolvimento

Crie `docker-compose.dev.yaml` para ajustes específicos de desenvolvimento:

```yaml
version: '3.8'

services:
  app:
    environment:
      NODE_ENV: development
      DEBUG: '*'  # Habilita debug logs
    stdin_open: true  # Para debugging interativo
    tty: true

  # Override para persistência em dev
  db:
    volumes:
      - ./.docker/dbdata:/var/lib/postgresql/data:delegated
```

**Uso**:
```bash
# Desenvolvimento local com persistência
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up
```

### 7. Criação do .dockerignore

Crie `.dockerignore` completo para otimizar COPY:

```
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/

# Tests
coverage/
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore
.github/

# Docker
.docker/dbdata/
.docker/logs/
docker-compose*.yaml
Dockerfile*
.dockerignore

# Environment
.env
.env.*
envs/

# Documentation
*.md
docs/

# OS
.DS_Store
Thumbs.db

# Misc
.history/
tmp/
temp/
```

**Explique ao usuário**:
- **node_modules**: CRUCIAL - reduz build de minutos para segundos
- **dist/**: Build artifacts não devem ser copiados (serão gerados no container)
- **.git/**: Histórico não é necessário no runtime
- **Ganho médio**: 80-95% de redução no contexto de build

### 8. Configuração de Variáveis de Ambiente

Estruture `envs/` com templates:

**envs/.env.example**:
```bash
# Application
NODE_ENV=development
APP_PORT=3000

# Database
DB_HOST=db
DB_PORT=5432
DB_DATABASE=dev_db
DB_USER=dev_user
DB_PASSWORD=dev_pass

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=dev_user
RABBITMQ_PASS=dev_pass
```

**Instruções ao usuário**:
```bash
# Setup inicial
cp envs/.env.example envs/.env

# Edite .env com valores locais
nano envs/.env
```

### 9. Debugging no VSCode

Configure `.vscode/launch.json` para debug remoto:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Docker: Attach to Node",
      "remoteRoot": "/home/node/app",
      "localRoot": "${workspaceFolder}",
      "protocol": "inspector",
      "port": 9229,
      "restart": true,
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

**Modifique docker-compose.dev.yaml**:
```yaml
services:
  app:
    command: npm run start:debug  # Em vez de start:dev
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
```

**Adicione script em package.json**:
```json
{
  "scripts": {
    "start:debug": "nest start --debug 0.0.0.0:9229 --watch"
  }
}
```

### 10. Comandos Úteis de Desenvolvimento

Forneça ao usuário esta lista de comandos:

**Iniciar ambiente**:
```bash
# Primeira vez (build)
docker-compose up --build

# Starts subsequentes (mais rápido)
docker-compose up

# Background
docker-compose up -d

# Com override de dev
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up
```

**Executar comandos no container**:
```bash
# Shell interativo
docker-compose exec app bash

# Executar comando único
docker-compose exec app npm run test
docker-compose exec app npm run lint
docker-compose exec app npx nest g module users

# Como root (se necessário)
docker-compose exec -u root app bash
```

**Logs e debugging**:
```bash
# Ver logs
docker-compose logs -f app

# Ver logs de todos os serviços
docker-compose logs -f

# Últimas 100 linhas
docker-compose logs --tail=100 app
```

**Limpeza**:
```bash
# Parar containers
docker-compose down

# Parar e remover volumes (⚠️ perde dados)
docker-compose down -v

# Remover imagens
docker-compose down --rmi all

# Limpeza completa do sistema
docker system prune -a --volumes
```

**Resetar banco de dados**:
```bash
# Parar, remover volumes e reiniciar
docker-compose down -v
docker-compose up -d db
docker-compose exec app npm run migrate
```

### 11. Otimizações de Performance

**Cache de node_modules (melhor abordagem)**:

Se performance for crítica, use esta estratégia:

```yaml
services:
  app:
    volumes:
      - .:/home/node/app
      - node_modules:/home/node/app/node_modules  # Volume nomeado
      - '/etc/timezone:/etc/timezone:ro'
      - '/etc/localtime:/etc/localtime:ro'

volumes:
  node_modules:  # Volume nomeado (mais rápido que anônimo)
```

**Ganho**: 50-70% mais rápido que volume mount normal

**Delegated/Cached mount modes (macOS)**:
```yaml
volumes:
  - .:/home/node/app:delegated  # Prioriza performance do container
```

**Trade-off**: Pequeno delay entre salvamento no host e detecção no container

**Usar tmpfs para dados temporários**:
```yaml
services:
  db:
    tmpfs:
      - /tmp
      - /var/run/postgresql  # Unix sockets em RAM
```

### 12. Troubleshooting Comum

**Problema: Hot-reload não funciona**

Diagnóstico:
```bash
# Verificar se volumes estão corretos
docker-compose config

# Verificar se start:dev está configurado
docker-compose exec app npm run start:dev
```

Soluções:
1. Verificar que volume mount está correto (`.:/home/node/app`)
2. Garantir que `start:dev` usa `--watch` flag
3. Em macOS, adicionar `:delegated` ao volume
4. Verificar que .dockerignore não exclui src/

**Problema: Permissões negadas**

Diagnóstico:
```bash
# Verificar usuário do processo
docker-compose exec app whoami  # Deve ser 'node'

# Verificar ownership dos arquivos
docker-compose exec app ls -la
```

Soluções:
1. Garantir `USER node` no Dockerfile
2. Ajustar ownership no host: `sudo chown -R $USER:$USER .`
3. Em Linux, verificar que UID/GID do node user (1000:1000) corresponde ao user do host

**Problema: Database connection refused**

Diagnóstico:
```bash
# Verificar se DB está healthy
docker-compose ps

# Testar conexão manualmente
docker-compose exec app nc -zv db 5432
```

Soluções:
1. Adicionar health check no serviço DB
2. Usar `depends_on` com `condition: service_healthy`
3. Verificar que `DB_HOST` aponta para nome do serviço ('db', não 'localhost')
4. Aguardar 30s-60s no primeiro start (inicialização do DB)

**Problema: Container sai imediatamente**

Diagnóstico:
```bash
# Ver logs de erro
docker-compose logs app

# Verificar exit code
docker-compose ps
```

Soluções:
1. Verificar se start.sh tem `#!/bin/bash` na primeira linha
2. Garantir que start.sh é executável: `chmod +x .docker/start.sh`
3. Verificar se CMD no Dockerfile está correto
4. Adicionar `tail -f /dev/null` temporariamente para debugging

## Restrições e limites

### Contexto de Desenvolvimento

Esta Skill é focada EXCLUSIVAMENTE em ambientes de desenvolvimento. NÃO use estas configurações para:

❌ **Produção**:
- Não usa multi-stage builds
- Não otimiza tamanho de imagem
- Inclui ferramentas de desenvolvimento
- Expõe portas de debugging

❌ **CI/CD**:
- Não usa tmpfs para databases (CI usa isso)
- Persistência pode impactar testes idempotentes
- Não otimizado para builds rápidos

### Segurança em Desenvolvimento

Mesmo em desenvolvimento, mantenha boas práticas:

✅ **Faça**:
- Use variáveis de ambiente para senhas
- Não commite arquivos .env
- Use senhas fracas APENAS localmente
- Mantenha .dockerignore completo

❌ **Nunca**:
- Hardcode senhas em docker-compose.yaml
- Commite .env com credenciais reais
- Use mesmas senhas de produção em dev
- Exponha portas sensíveis publicamente

### Performance Trade-offs

Decisões desta Skill priorizam velocidade de desenvolvimento:

**Prioridade ALTA**:
- Hot-reload rápido (< 2s)
- Tempo de startup aceitável (< 30s)
- Debugging sem friction

**Prioridade BAIXA**:
- Tamanho de imagem (pode chegar a 800MB)
- Uso de RAM (volumes podem consumir muito)
- Otimização de layers (não relevante em dev)

## Validação de Qualidade

Após aplicar esta Skill, valide:

### Checklist de Funcionalidades

- [ ] Hot-reload funciona ao editar arquivos .ts
- [ ] Container inicia em menos de 60 segundos
- [ ] Dependências são instaladas corretamente no primeiro start
- [ ] Serviços externos (DB, Redis, etc.) são acessíveis
- [ ] Logs aparecem no console com `docker-compose logs -f`
- [ ] Debug remoto conecta (se configurado)
- [ ] Variáveis de ambiente são carregadas corretamente

### Checklist de Performance

- [ ] Hot-reload leva menos de 3 segundos
- [ ] `docker-compose up` subsequente leva menos de 30s
- [ ] node_modules não é copiado do host para container
- [ ] Volumes nomeados ou anônimos estão configurados para node_modules

### Checklist de Qualidade

- [ ] .dockerignore exclui node_modules, dist, .git
- [ ] Health checks estão configurados para todos os serviços externos
- [ ] Dockerfile usa USER node
- [ ] docker-compose.yaml tem networks definidas
- [ ] Todos os serviços usam depends_on com service_healthy

## Exemplos de uso

### Exemplo 1: Setup inicial de projeto NestJS

**Entrada do usuário**:
"Configure Docker para meu projeto NestJS com PostgreSQL e Redis."

**Ações esperadas**:
1. Analisar package.json e estrutura do projeto
2. Criar Dockerfile otimizado para desenvolvimento
3. Criar docker-compose.yaml com app, PostgreSQL e Redis
4. Configurar health checks em todos os serviços
5. Criar .docker/start.sh com verificação de dependências
6. Gerar .dockerignore completo
7. Criar envs/.env.example com templates
8. Fornecer comandos de uso e troubleshooting

**Saída esperada**:
- Arquivos criados e explicações detalhadas
- Instruções de primeiro uso
- Lista de comandos úteis

### Exemplo 2: Otimização de performance

**Entrada do usuário**:
"Hot-reload está lento, demora 10 segundos para refletir mudanças."

**Ações esperadas**:
1. Diagnosticar configuração atual de volumes
2. Verificar se node_modules está em volume anônimo
3. Sugerir mount mode delegated (macOS)
4. Verificar configuração de start:dev
5. Propor uso de volume nomeado para node_modules
6. Recomendar ajustes em tsconfig.json se necessário

**Saída esperada**:
- Análise do problema
- Soluções priorizadas por impacto
- Patches para docker-compose.yaml

### Exemplo 3: Adicionar debugging

**Entrada do usuário**:
"Como fazer debug remoto do NestJS rodando no Docker?"

**Ações esperadas**:
1. Criar configuração .vscode/launch.json
2. Adicionar script start:debug em package.json
3. Modificar docker-compose.dev.yaml para expor porta 9229
4. Fornecer instruções de uso do debugger
5. Explicar como definir breakpoints e inspecionar variáveis

### Exemplo 4: Migração de projeto existente

**Entrada do usuário**:
"Tenho um projeto NestJS sem Docker, quero containerizar para desenvolvimento."

**Ações esperadas**:
1. Analisar dependências e serviços necessários
2. Criar toda estrutura Docker do zero
3. Migrar variáveis de ambiente para envs/
4. Configurar serviços externos baseado em configuração atual
5. Fornecer plano de migração gradual
6. Documentar diferenças de workflow (npm → docker-compose exec)

## Dependências

Esta Skill assume:

**No host**:
- Docker Engine 20.10+ ou Docker Desktop
- Docker Compose 2.0+ (plugin format)
- Node.js 18+ (para desenvolvimento fora do container, opcional)

**No projeto**:
- NestJS 9+ ou 10+
- package.json válido com scripts (start:dev, build, test)
- TypeScript configurado

**Ferramentas opcionais**:
- VSCode (para debugging remoto)
- Colima (alternativa ao Docker Desktop no macOS)

## Versão

**Versão**: 1.0.0
**Data**: 2025-11-18
**Autor**: SuperClaude Framework
**Compatibilidade**: NestJS 9+, Docker Compose 2.0+

## Changelog

### v1.0.0 (2025-11-18)
- Versão inicial
- Suporte completo para PostgreSQL, MySQL, Redis, RabbitMQ
- Otimizações de performance para macOS e Linux
- Debugging remoto com VSCode
- Troubleshooting para problemas comuns
