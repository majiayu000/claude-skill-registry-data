---
name: gmaps-phase-1
description: Fase 1 do gmaps-leads — Parsear parametros e expandir termos de busca
user-invocable: false
---

# Fase 1 — Parsear + Expandir Termos

Leia os argumentos: $ARGUMENTS

## 1.1 Parsear parametros

Extraia:
- `--nicho "X"` → nicho (obrigatorio)
- `--local "X"` → local: bairro, cidade (obrigatorio)
- `--sem-site` → flag: apenas sem website
- `--nota-min N` → nota minima Google
- `--min-reviews N` → minimo avaliacoes
- `--max-reviews N` → maximo avaliacoes
- `--com-telefone` → flag: apenas com telefone
- `--subdividir` → flag: buscar por bairros
- `--enrich-cnpj` → flag: enriquecer com CNPJ
- `--limite N` → max resultados por query (default: 60)
- `--target N` → parar apos encontrar N leads
- `--force` → ignorar cache

## 1.2 Expandir termos de busca (PASSO CRITICO)

PENSE como um empresario desse nicho se apresenta no Google Maps.
Gere TODOS os subtipos, sinonimos e variacoes.

Exemplos de expansao:
- "escola esportiva" → escola de futebol, escola de natacao, escola de surf, escola de tenis, escola de judo, escolinha de volei, escola de ginastica, escola de artes marciais, escola de danca, academia infantil
- "restaurante" → pizzaria, hamburgueria, churrascaria, sushi, comida japonesa, comida italiana, restaurante vegano, marmitaria, self-service, bistrô, gastropub, food truck
- "clinica" → clinica medica, clinica popular, consultorio, centro medico, clinica de fisioterapia, clinica dermatologica
- "salao" → salao de beleza, barbearia, studio de beleza, cabeleireiro, hair studio
- "dentista" → dentista, odontologia, clinica odontologica, consultorio dentario, ortodontia, implante dentario

Gere pelo menos 5-10 termos extras para o nicho solicitado.

## 1.3 Montar comando

Monte o comando final:
```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python gmaps_leads.py --nicho "{nicho}" --local "{local}" --keywords-extra "termo1,termo2,termo3" [filtros]
```

## 1.4 Verificar dependencias

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/pip install playwright playwright-stealth 2>/dev/null
.venv/bin/python -m playwright install chromium 2>/dev/null
```

## 1.5 Salvar no state

Salve: nicho, local, filtros, keywords_extra, comando montado.

Mostre ao usuario:
```
Nicho: [nicho]
Local: [local]
Keywords expandidas: [lista]
Filtros: [ativos]
Queries estimadas: ~[N]
```

## CRITERIO DE CONCLUSAO
- Params parseados
- Termos expandidos (5+ extras)
- Comando montado
- Dependencias verificadas
- State file atualizado
