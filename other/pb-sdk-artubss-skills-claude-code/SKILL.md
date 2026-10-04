---
name: "PocketBase SDK"
description: "Uso do SDK JavaScript para aplicações cliente PocketBase. Use ao chamar PocketBase a partir do frontend ou Node.js, autenticar usuários, subscrever a eventos em tempo real, fazer upload de arquivos, ou trabalhar com o SDK PocketBase JS/TS. Cobre operações CRUD, fluxos de autenticação, authStore, SSE em tempo real, manipulação de arquivos, operações em lote e sintaxe de query."
---

# SDK JavaScript PocketBase

## Instalação e Setup

```bash
npm install pocketbase
# ou
yarn add pocketbase
# ou
<script src="https://cdn.jsdelivr.net/npm/pocketbase@0.36.6/dist/pocketbase.umd.js"></script>
```

```js
import PocketBase from 'pocketbase'

const pb = new PocketBase('http://127.0.0.1:8090')
```

## Operações CRUD

### Listar registros

```js
const records = await pb.collection('posts').getList(1, 20, {
    filter: 'status = "active" && created > "2024-01-01"',
    sort: '-created,title',
    expand: 'author,tags',
    fields: 'id,title,author,created',  // partial response
    skipTotal: true,  // skip COUNT query for better performance
})

// records.page, records.perPage, records.totalItems, records.totalPages, records.items
```

### Obter lista completa (auto-paginação)

```js
const allRecords = await pb.collection('posts').getFullList({
    filter: 'status = "active"',
    sort: '-created',
    batch: 200,  // records per request (default: 200)
})
```

### Visualizar um registro único

```js
const record = await pb.collection('posts').getOne('RECORD_ID', {
    expand: 'author',
})
```

### Obter primeiro registro correspondente

```js
const record = await pb.collection('posts').getFirstListItem('slug = "my-post"', {
    expand: 'author',
})
```

### Criar registro

```js
const record = await pb.collection('posts').create({
    title: 'My Post',
    body: 'Content here',
    author: 'USER_ID',
    status: 'draft',
})
```

### Atualizar registro

```js
const record = await pb.collection('posts').update('RECORD_ID', {
    title: 'Updated Title',
    status: 'published',
})
```

### Deletar registro

```js
await pb.collection('posts').delete('RECORD_ID')
```

## Parâmetros de Query

### Sintaxe de filtro

Igual à sintaxe de filtro das regras da API. Padrões comuns:

```js
// Igualdade
filter: 'status = "active"'

// Contém (LIKE)
filter: 'title ~ "hello"'

// Multi-relação contém
filter: 'tags ?= "TAG_ID"'

// Comparação de data
filter: 'created > "2024-01-01 00:00:00"'

// Datas relativas
filter: 'created > @now - 7d'

// Operadores lógicos
filter: 'status = "active" && author = "USER_ID"'
filter: '(type = "a" || type = "b") && active = true'

// Verificação de nulo
filter: 'parent = null'
filter: 'parent != null'
```

### Sintaxe de ordenação

```js
sort: '-created'          // descendente por created
sort: 'title'             // ascendente por title
sort: '-created,title'    // ordenação multi-campo
sort: '@random'           // ordem aleatória
```

### Expandir relações

```js
expand: 'author'                    // relação única
expand: 'author,tags'               // múltiplas relações
expand: 'author.team'               // expand aninhado (team do author)
expand: 'comments_via_post'         // back-relação (comments que referenciam este post)
expand: 'comments_via_post.author'  // expand de back-relação aninhada
```

### Campos (resposta parcial)

```js
fields: 'id,title,created'
fields: 'id,expand.author.name'     // incluir campo expandido
fields: '*,expand.author.name'      // todos os campos + expand específico
```

## Autenticação

### Email/senha

```js
const authData = await pb.collection('users').authWithPassword('user@example.com', 'password123')
// authData.token, authData.record
```

### OAuth2 (tudo-em-um)

```js
// Abre popup/redirect para provedor OAuth2
const authData = await pb.collection('users').authWithOAuth2({ provider: 'google' })
// ou com redirect
const authData = await pb.collection('users').authWithOAuth2({
    provider: 'google',
    urlCallback: (url) => { window.location.href = url }
})
```

### OTP (one-time password)

```js
// Etapa 1: Solicitar OTP
const result = await pb.collection('users').requestOTP('user@example.com')
// result.otpId

// Etapa 2: Verificar OTP
const authData = await pb.collection('users').authWithOTP(result.otpId, '123456')
```

### MFA (autenticação multifator)

MFA é acionado automaticamente quando ativado. Após autenticação primária retorna um `mfaId`:

```js
try {
    await pb.collection('users').authWithPassword('user@example.com', 'password')
} catch (err) {
    if (err.response?.mfaId) {
        // Precisa de segundo fator — por ex., OTP
        const otpResult = await pb.collection('users').requestOTP('user@example.com')
        await pb.collection('users').authWithOTP(otpResult.otpId, '123456', {
            mfaId: err.response.mfaId
        })
    }
}
```

### Auth store

```js
pb.authStore.token       // token JWT atual
pb.authStore.record      // registro de autenticação atual
pb.authStore.isValid     // token não expirado
pb.authStore.isAdmin     // descontinuado — verificar record.collectionName === '_superusers'
pb.authStore.isSuperuser // verificar se é superuser

// Ouvir mudanças de autenticação
pb.authStore.onChange((token, record) => {
    console.log('Auth changed:', record?.id)
})

// Limpar autenticação
pb.authStore.clear()

// Renovar autenticação (obter token fresco + registro)
await pb.collection('users').authRefresh()
```

### Redefinição de senha

```js
// Solicitar email de reset
await pb.collection('users').requestPasswordReset('user@example.com')

// Confirmar reset (geralmente através de link no email)
await pb.collection('users').confirmPasswordReset(token, newPassword, newPasswordConfirm)
```

### Verificação de email

```js
await pb.collection('users').requestVerification('user@example.com')
await pb.collection('users').confirmVerification(token)
```

### Mudança de email

```js
await pb.collection('users').requestEmailChange('new@example.com')
await pb.collection('users').confirmEmailChange(token, password)
```

## Tempo Real (SSE)

### Subscrever a mudanças de registro

```js
// Subscrever a todas as mudanças em uma coleção
pb.collection('posts').subscribe('*', function(e) {
    // e.action: 'create' | 'update' | 'delete'
    // e.record: o registro afetado
    console.log(e.action, e.record.id)
}, {
    expand: 'author',  // expandir relações em eventos em tempo real
    filter: 'status = "active"',  // receber apenas registros correspondentes
})

// Subscrever a um registro específico
pb.collection('posts').subscribe('RECORD_ID', function(e) {
    console.log('Record changed:', e.record)
})

// Desinscrever
pb.collection('posts').unsubscribe('*')        // de tópico específico
pb.collection('posts').unsubscribe('RECORD_ID')
pb.collection('posts').unsubscribe()            // de todos os tópicos de coleção
pb.realtime.unsubscribe()                       // de tudo
```

### Gerenciamento de conexão

```js
// O SDK reconecta automaticamente ao desconectar
// Você pode ouvir connect/disconnect:
pb.realtime.onConnect = function() {
    console.log('Connected')
}
pb.realtime.onDisconnect = function() {
    console.log('Disconnected')
}
```

## Upload e Download de Arquivos

### Fazer upload de arquivos

```js
// Via FormData (browser)
const formData = new FormData()
formData.append('title', 'My Post')
formData.append('document', fileInput.files[0])
formData.append('images', fileInput1.files[0])  // multi-file
formData.append('images', fileInput2.files[0])

const record = await pb.collection('posts').create(formData)

// Via objeto (Node.js ou quando você tem o arquivo como Blob/File)
const record = await pb.collection('posts').create({
    title: 'My Post',
    document: new File([blob], 'file.pdf'),
})
```

### Deletar um arquivo

```js
// Definir campo como vazio para deletar
await pb.collection('posts').update('RECORD_ID', {
    document: null,  // deletes the file
})

// Para multi-arquivo: remover arquivo específico
await pb.collection('posts').update('RECORD_ID', {
    'images-': ['filename_to_remove.jpg'],  // minus suffix removes
})
```

### Obter URL de arquivo

```js
const url = pb.files.getURL(record, record.document)
// https://example.com/api/files/COLLECTION_ID/RECORD_ID/filename.pdf

// Com thumbnail (para campos de imagem)
const thumb = pb.files.getURL(record, record.cover, { thumb: '100x100' })
// Suportados: WxH, WxHt (top), WxHb (bottom), WxHf (fit), 0xH, Wx0
```

### Arquivos protegidos

Para arquivos em coleções com regras de visualização, incluir o token de autenticação:

```js
const url = pb.files.getURL(record, record.document, { token: pb.authStore.token })
```

## Operações em Lote

Enviar múltiplos create/update/delete em uma única requisição (transacional):

```js
const batch = pb.createBatch()

batch.collection('posts').create({ title: 'Post 1' })
batch.collection('posts').create({ title: 'Post 2' })
batch.collection('posts').update('RECORD_ID', { title: 'Updated' })
batch.collection('comments').delete('COMMENT_ID')

const results = await batch.send()
// results[0], results[1], ... correspondem a cada operação
```

## Tratamento de Erros

```js
try {
    const record = await pb.collection('posts').create(data)
} catch (err) {
    // err.status — código de status HTTP
    // err.response — resposta de erro completa
    // err.response.message — mensagem de erro
    // err.response.data — erros de validação de nível de campo
    //   ex., { title: { code: "validation_required", message: "Missing required value." } }
    // err.isAbort — true se a requisição foi cancelada

    if (err.status === 400) {
        // Erro de validação
        for (const [field, error] of Object.entries(err.response.data)) {
            console.log(`${field}: ${error.message}`)
        }
    }
}
```

## Avançado

### Auto-cancelamento

Por padrão, requisições duplicadas pendentes para o mesmo endpoint são auto-canceladas. Desabilitar por requisição:

```js
await pb.collection('posts').getList(1, 20, {
    requestKey: null,  // disable auto-cancel for this request
})

// Ou usar uma chave customizada para agrupar cancelamentos
await pb.collection('posts').getList(1, 20, {
    requestKey: 'my-custom-key',
})
```

### Headers customizados

```js
// Por requisição
await pb.collection('posts').getList(1, 20, {
    headers: { 'X-Custom': 'value' }
})

// Global (todas as requisições)
pb.beforeSend = function(url, options) {
    options.headers['X-Custom'] = 'value'
    return { url, options }
}

// Interceptar resposta
pb.afterSend = function(response, data) {
    // modify data if needed
    return data
}
```

### SSR / Lado do servidor

```js
// Carregar autenticação a partir de cookie (ex., em Next.js/SvelteKit)
pb.authStore.loadFromCookie(request.headers.get('cookie') || '')

// Exportar autenticação para cookie
const cookie = pb.authStore.exportToCookie({ httpOnly: false })
response.headers.set('set-cookie', cookie)
```

### Enviando como superuser

```js
const pb = new PocketBase('http://127.0.0.1:8090')
await pb.collection('_superusers').authWithPassword('admin@example.com', 'password')
// Agora todas as requisições são autenticadas como superuser
```