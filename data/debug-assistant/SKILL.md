---
name: debug-assistant
description: Assistência em debugging e troubleshooting de aplicações PHP/Laravel incluindo análise de stack traces, logs, erros de banco de dados, problemas de performance, memory leaks, e issues de configuração. Usar para diagnosticar erros, interpretar mensagens de exceção, identificar causas raiz, e propor soluções.
---

# Debug Assistant

Skill para diagnóstico e resolução de problemas em aplicações PHP/Laravel.

## Análise de Stack Traces

### Anatomia de um Stack Trace Laravel

```
[2024-01-15 10:30:45] production.ERROR: SQLSTATE[23000]: Integrity constraint violation: 
1062 Duplicate entry 'john@email.com' for key 'users.users_email_unique' 
(Connection: mysql, SQL: insert into `users` (`name`, `email`, `password`, `updated_at`, `created_at`) 
values (John, john@email.com, $2y$12$xxx, 2024-01-15 10:30:45, 2024-01-15 10:30:45))

#0 /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connection.php(801): 
   Illuminate\Database\Connection->runQueryCallback()
#1 /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connection.php(567): 
   Illuminate\Database\Connection->run()
#2 /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Eloquent/Builder.php(1716): 
   Illuminate\Database\Query\Builder->insert()
#3 /var/www/html/app/Services/UserService.php(45): 
   App\Models\User::create()                    ← PONTO DE ORIGEM
#4 /var/www/html/app/Http/Controllers/UserController.php(28): 
   App\Services\UserService->register()         ← CHAMADOR
```

### Checklist de Análise

```markdown
1. [ ] Identificar tipo do erro (Exception class)
2. [ ] Localizar mensagem principal
3. [ ] Encontrar arquivo/linha de origem (primeiro arquivo app/)
4. [ ] Verificar parâmetros/dados envolvidos
5. [ ] Checar contexto (request, user, etc)
```

## Erros Comuns e Soluções

### Database Errors

```php
// ERRO: SQLSTATE[23000] Duplicate entry
// CAUSA: Violação de unique constraint
// SOLUÇÃO:
try {
    User::create($data);
} catch (\Illuminate\Database\UniqueConstraintViolationException $e) {
    // Laravel 10+
    return back()->withErrors(['email' => 'Email já cadastrado']);
}
// OU usar firstOrCreate/updateOrCreate
User::firstOrCreate(['email' => $email], $data);

// ERRO: SQLSTATE[42S22] Column not found
// CAUSA: Coluna não existe ou typo
// VERIFICAR:
php artisan tinker
>>> Schema::hasColumn('users', 'nome')  // false = coluna não existe
>>> Schema::getColumnListing('users')    // listar colunas

// ERRO: SQLSTATE[HY000] [2002] Connection refused
// CAUSA: MySQL não está rodando ou configuração errada
// VERIFICAR:
// 1. MySQL running: sudo systemctl status mysql
// 2. .env: DB_HOST, DB_PORT, DB_DATABASE, DB_USERNAME, DB_PASSWORD
// 3. Docker: verificar se container está up e network correta
```

### Class/Method Not Found

```php
// ERRO: Class 'App\Services\UserService' not found
// CAUSA: Autoload desatualizado ou namespace errado
// SOLUÇÃO:
composer dump-autoload
// Verificar namespace no arquivo corresponde ao path

// ERRO: Method App\Models\User::contracts does not exist
// CAUSA: Método não definido ou typo
// VERIFICAR: O método existe no Model? Está usando trait correto?

// ERRO: Target class [UserController] does not exist
// CAUSA: Controller não registrado ou namespace errado em routes
// SOLUÇÃO Laravel 8+:
// routes/web.php
use App\Http\Controllers\UserController;
Route::get('/users', [UserController::class, 'index']);
```

### Memory/Performance

```php
// ERRO: Allowed memory size of X bytes exhausted
// CAUSA: Loop infinito, query sem limit, processamento em massa
// SOLUÇÕES:

// 1. Chunking para grandes volumes
User::chunk(1000, function ($users) {
    foreach ($users as $user) {
        // processar
    }
});

// 2. Cursor para economia de memória
foreach (User::cursor() as $user) {
    // processar um por vez
}

// 3. Lazy collections
User::lazy()->each(function ($user) {
    // processar
});

// 4. Aumentar limite temporariamente (não recomendado como fix permanente)
ini_set('memory_limit', '512M');
```

### N+1 Query Problem

```php
// PROBLEMA: Query executada para cada item do loop
// SINTOMA: Lentidão, muitas queries no debugbar

// ❌ RUIM - N+1
$contracts = Contract::all();
foreach ($contracts as $contract) {
    echo $contract->client->name; // Query para cada contract!
}

// ✅ BOM - Eager Loading
$contracts = Contract::with('client')->get();
foreach ($contracts as $contract) {
    echo $contract->client->name; // Sem queries adicionais
}

// DETECTAR N+1
// .env
QUERY_LOG=true
// Ou usar Laravel Debugbar / Telescope
```

## Ferramentas de Debug

### Laravel Telescope

```bash
composer require laravel/telescope --dev
php artisan telescope:install
php artisan migrate
# Acessar: /telescope
```

### Laravel Debugbar

```bash
composer require barryvdh/laravel-debugbar --dev
# Automático em ambiente local
```

### Logging Estratégico

```php
use Illuminate\Support\Facades\Log;

// Níveis de log
Log::emergency($message);  // Sistema inutilizável
Log::alert($message);      // Ação imediata necessária
Log::critical($message);   // Condições críticas
Log::error($message);      // Erros
Log::warning($message);    // Avisos
Log::notice($message);     // Eventos normais mas significativos
Log::info($message);       // Informações
Log::debug($message);      // Debug detalhado

// Com contexto
Log::error('Falha no pagamento', [
    'contract_id' => $contract->id,
    'amount' => $amount,
    'gateway_response' => $response,
    'user_id' => auth()->id(),
]);

// Channel específico
Log::channel('payments')->info('Pagamento processado', [...]);
```

### Dump & Die

```php
// Dump e continuar
dump($variable);

// Dump e parar (die)
dd($variable);

// Dump SQL de query
Contract::where('status', 'active')->dd();
// ou
Contract::where('status', 'active')->toSql();

// Com bindings
$query = Contract::where('status', 'active');
dump($query->toSql(), $query->getBindings());
```

## Checklist de Troubleshooting

```markdown
## Erro em Produção
1. [ ] Verificar logs: storage/logs/laravel.log
2. [ ] Verificar .env: APP_DEBUG=false, APP_ENV=production
3. [ ] Cache limpo: php artisan optimize:clear
4. [ ] Permissões: storage/ e bootstrap/cache/ com 775

## Erro de Database
1. [ ] Conexão OK: php artisan db
2. [ ] Migrations rodaram: php artisan migrate:status
3. [ ] Índices existem: SHOW INDEX FROM table_name
4. [ ] Query correta: Log::debug(DB::getQueryLog())

## Erro de Performance
1. [ ] N+1 queries: debugbar ou telescope
2. [ ] Cache ativo: php artisan cache:table
3. [ ] Queue funcionando: php artisan queue:work
4. [ ] Índices no DB: EXPLAIN SELECT...

## Erro de Autenticação
1. [ ] Session driver: config/session.php
2. [ ] Guards configurados: config/auth.php
3. [ ] Middleware aplicado: route:list
4. [ ] Token válido (Sanctum/Passport)
```

## Comandos de Diagnóstico

```bash
# Status geral
php artisan about

# Listar rotas
php artisan route:list --columns=uri,method,action

# Verificar config
php artisan config:show database

# Testar conexão DB
php artisan db

# Verificar migrations
php artisan migrate:status

# Limpar tudo
php artisan optimize:clear

# Logs em tempo real
tail -f storage/logs/laravel.log

# Verificar queue
php artisan queue:monitor redis:default
```
