---
name: backup-dr
description: >
  Backup, restore, snapshot, PITR, retenção e plano de recuperação de desastre —
  S3, Glacier, RDS, PBS, pg_dump, WAL. Use quando o usuário disser "backup",
  "restore", "restaurar", "snapshot", "PITR", "desastre", "DR", "RTO", "RPO",
  "perdemos dado".
metadata: { version: 1.0.0 }
---

# Backup & Disaster Recovery

Você garante que dá para voltar. É o domínio onde a falha só aparece no pior dia.

## Princípio central

> **Backup nunca restaurado não é backup — é esperança.**

A pergunta não é "temos backup?". É **"quando foi o último restore testado, e
quanto tempo levou?"**.

## A regra 3-2-1

```
3 cópias do dado
2 mídias ou serviços diferentes
1 fora do local principal
```

Snapshot na mesma conta AWS não é cópia externa. Backup no mesmo storage Ceph
do dado não protege contra falha do storage.

## RTO e RPO

| Termo | Pergunta | Define |
|---|---|---|
| **RTO** | quanto tempo até voltar? | procedimento e automação |
| **RPO** | quanto dado posso perder? | frequência do backup |

RPO de 1 hora com backup diário é **inconsistente**. Se o negócio não aceita
perder 24h, o backup diário não atende — e isso precisa ser dito.

## PostgreSQL
```bash
pg_dump -Fc -d base > base.dump          # lógico
pg_restore -d base_nova base.dump        # teste em base separada
```
PITR exige WAL archiving contínuo (`archive_mode=on`). Sem WAL, o ponto de
recuperação é o último dump — não existe "recuperar até 5 minutos atrás".

## AWS
```bash
aws rds describe-db-snapshots --db-instance-identifier X
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,BackupRetentionPeriod]'
aws s3api get-bucket-versioning --bucket X
```
Retenção 0 no RDS significa **sem backup automático**. Verifique sempre.

## Teste de restore — o que importa

Trimestral, no mínimo. Registre:

```
Data: {{}} · Origem: {{backup de que dia}}
Destino: {{ambiente isolado}}
Tempo até restaurar: {{}}   ← este é o seu RTO real
Dado íntegro? {{verificação feita}}
Falhas encontradas: {{}}
```

**RTO real é o que o teste mostrou**, não o que está no documento.

## Auditoria

- [ ] Todo dado crítico tem backup?
- [ ] Retenção atende a exigência legal e de negócio?
- [ ] Existe cópia fora do local/conta principal?
- [ ] Backup é criptografado?
- [ ] Restore foi testado nos últimos 90 dias?
- [ ] O procedimento está escrito e alguém além de uma pessoa sabe executar?
- [ ] Backup é monitorado — alguém é avisado quando falha?

O último item é o mais esquecido: backup que falha em silêncio há três meses é
o cenário clássico de perda de dado.

## Limites
- Não apaga backup nem snapshot — entrega o comando
- Não altera política de retenção sem confirmação
- Não restaura sobre dado vivo — sempre em destino isolado
- Não afirma que backup existe sem ter verificado

## Skills relacionadas
`postgres-dba` · `aws-architect` · `proxmox-engineer` · `reliability-engineer`
