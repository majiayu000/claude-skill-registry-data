---
name: program-moodle
description: "Atua como especialista sênior em Moodle LMS, cobrindo desenvolvimento e ciclo de vida de plugins (Frankenstyle), APIs principais (DB, Form, Page, Output), modelagem XMLDB e tuning de banco de dados, design de temas (Mustache/SCSS), infraestrutura em larga escala (OPcache, MUC Redis/Memcached) e segurança."
---

# 🎓 Especialista Integral em Moodle LMS (program-moodle)

Esta skill fornece diretrizes rigorosas, padrões de arquitetura e boas práticas de engenharia de software para todo o ecossistema Moodle LMS (Learning Management System).

---

## 🏛️ 1. Arquitetura Frankenstyle & Ciclo de Vida de Plugins

O Moodle utiliza a convenção de nomenclatura **Frankenstyle** (`[plugintype]_[pluginname]`):

```
moodle/
├── mod/               # Módulos de atividades (ex: mod_quiz, mod_assign)
├── block/             # Blocos laterais (ex: block_myoverview)
├── local/             # Plugins locais de customização (ex: local_custom_reports)
├── theme/             # Temas visuais (ex: theme_boost)
└── enrol/             # Métodos de inscrição (ex: enrol_manual)
```

- **Estrutura Padrão de um Plugin**:
  - `version.php`: Declara `$plugin->version`, `$plugin->requires` e `$plugin->component`.
  - `lib.php`: Funções de extensão, callbacks e hooks.
  - `db/`: `install.xml` (definições de tabelas XMLDB), `upgrade.php`, `access.php` (capabilities).
  - `lang/en/` e `lang/pt_br/`: Strings de internacionalização.
  - `settings.php`: Árvore de configurações administrativas.

---

## 🗄️ 2. Banco de Dados, XMLDB e Otimização DBA

- **Modelagem XMLDB**: Toda tabela do Moodle deve ser definida via XMLDB Editor (`db/install.xml`) com convenções rigorosas:
  - Campos primários sempre nomeados como `id (int 10, not null, auto-increment)`.
  - Chaves estrangeiras com índices explícitos para evitar *Full Table Scans*.
- **Transações Delegadas Seguras**:
```php
$transaction = $DB->start_delegated_transaction();
try {
    $DB->insert_record('custom_table', $record1);
    $DB->update_record('other_table', $record2);
    $transaction->allow_commit();
} catch (Exception $e) {
    $transaction->rollback($e);
}
```

---

## 🎨 3. Design de Interfaces, Temas e Acessibilidade (UI/UX)

- **Mustache Templates**: Separação estrita entre lógica de renderização e apresentação (`templates/component.mustache`).
- **Estilização SCSS**: Customização no arquivo `scss/preset/default.scss` estendendo o tema `theme_boost` e respeitando padrões WCAG 2.1 AA.

---

## 🌐 4. Infraestrutura, Performance e MUC (Moodle Universal Cache)

- **PHP OPcache**: Habilitar `opcache.enable=1`, `opcache.memory_consumption=512`, `opcache.max_accelerated_files=20000`.
- **MUC (Moodle Universal Cache)**: Configurar Redis ou Memcached para caches de Aplicação e Sessão, desacelerando consultas ao banco de dados.
- **Cron em Lote**: Executar `admin/cli/cron.php` via processo de background desacoplado do servidor web.
