---
name: cloud-architect
description: >
  Diseña infraestructura cloud como código — Terraform, AWS, GCP, Azure.
  Arquitecturas serverless, VPC, bases de datos administradas y cost optimization.
  Trigger: Cuando hay que levantar infraestructura en cloud, elegir proveedor, diseñar arquitectura o escribir Terraform.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: cloud-architect

Infraestructura como código en serio. Nada de consolear.

## Trigger

- Necesitás levantar una base de datos, un bucket o un servidor
- Hay que elegir entre AWS, GCP o Azure
- Vas a deployar una app web y necesitás DNS + CDN + SSL
- Querés infraestructura reproducible (Terraform)
- Hay que auditar costos y recursos olvidados

## Workflow LEND

```
1. ANALIZAR
   ├── Tipo de carga: web app, batch processing, API serverless
   ├── Escala esperada: users/día, storage, bandwidth
   ├── Presupuesto: free tier, startup, enterprise
   ├── ¿Ya hay cuenta en algún proveedor?
   └── Requisitos de compliance (GDPR, datos locales)

2. OFRECER (Menú del Senior)
   ├── A) Serverless: Lambda/Cloud Functions + API Gateway + DynamoDB/Firestore
   ├── B) Containerizado: ECS/GKE/AKS + RDS/Cloud SQL + ALB
   └── C) VM clásica: EC2/GCE/VM + managed DB + Load Balancer

3. ELEGIR → el usuario confirma

4. HACER
   ├── Terraform HCL (o OpenTofu): main.tf, variables.tf, outputs.tf
   ├── Remote state en S3/GCS + DynamoDB/Bigtable locking
   ├── Resource tagging consistente (Project, Env, ManagedBy)
   ├── Security groups / firewall rules (mínimo privilegio)
   └── Cost estimation con infracost o similar

5. VERIFICAR
   ├── terraform plan pasa sin errores
   ├── Los recursos son los mínimos necesarios
   └── No hay secretos en los outputs
```

## Patrones

- **Estado remoto**: siempre S3/GCS + locking, nunca local
- **Tagging**: `Project`, `Environment`, `ManagedBy`, `CostCenter`
- **Naming**: `{project}-{env}-{resource}-{region}-{xxx}`
- **Mínimo privilegio**: IAM roles, security groups, service accounts
- **Cost tags**: marcar recursos para trackear gasto
- **Módulos**: reutilizar módulos de Terraform Registry

## Anti-patrones

- Terraform state en local (se pierde, no se comparte)
- Recursos sin tags (no se puede rastrear el costo)
- Puertos abiertos a `0.0.0.0/0` en security groups
- Hardcodear region, cuenta ID o access keys
- Aprobar `terraform apply` sin revisar `terraform plan`
