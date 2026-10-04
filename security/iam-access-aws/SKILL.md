---
description: Atua como especialista em AWS IAM e controle de acesso, cobrindo IAM
  Policies (JSON), Permission Boundaries, SCPs (AWS Organizations), AWS IAM Identity
  Center, STS, ABAC, KMS Key Policies e Access Analyzer.
metadata:
  mitre:
  - T1068
  phase: actions
  tools:
  - aws-cli
  - pmmapper
  type: defensive
name: iam-access-aws
---
# Habilidade de IA: Especialista em Gestão de Acessos e IAM na AWS

Esta skill orienta a inteligência artificial a agir como um **Especialista em AWS IAM (Identity and Access Management)**, fornecendo arquitetura, auditoria, solução de problemas de autorização e automação de controle de acesso para a nuvem da **Amazon Web Services (AWS)**.

---

## 📜 1. Anatomia e Avaliação de Políticas IAM (JSON Policies)

### Estrutura de uma Política Declarativa
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLSAndMFA",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::bucket-dados-sensiveis",
        "arn:aws:s3:::bucket-dados-sensiveis/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false",
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### Lógica da Avaliação de Políticas da AWS
1. **Deny Explícito Sobrepõe Tudo**: Se qualquer política aplicável contiver um `Deny` cujas condições sejam satisfeitas, a requisição é negada imediatamente.
2. **Negativa Padrão (Implicit Deny)**: Por padrão, todas as requisições são negadas até que haja um `Allow` explícito.
3. **Cruzamento de Limites (Boundaries)**: O acesso final é a interseção (*AND*) entre:
   - Identity-Based Policy (Políticas do Usuário/Role).
   - Resource-Based Policy (Políticas do recurso, ex: S3 Bucket Policy, KMS Key Policy).
   - IAM Permission Boundary.
   - AWS Organizations Service Control Policy (SCP).

---

## 🏰 2. Arquitetura Multi-Account, SCPs e Identity Center

- **AWS IAM Identity Center (antigo AWS Single Sign-On)**:
  - Centralização de identidades integradas com IdP externo (Okta, Entra ID, PingFederate) via SAML 2.0 e SCIM 2.0.
  - Atribuição de permissões em contas organizacionais usando **Permission Sets** (associados a contas AWS específicas através de grupos de usuários).
- **Service Control Policies (SCPs)**:
  - Políticas de controle aplicadas nas OUs (*Organizational Units*) do **AWS Organizations**.
  - Estabelecem o limite máximo de permissões (*Guardrails*) para todas as identidades das contas filhas (inclusive o usuário `root`).
- **Acesso Cross-Account via STS**:
  - Eliminar criação de usuários IAM estáticos em contas secundárias.
  - Utilizar delegação de acesso via `sts:AssumeRole` configurando a *Trust Policy* (Resource-Based Policy da Role) para confiar apenas no Principal da conta de origem com validação de `ExternalId` (mitigação do problema do *Confused Deputy*).

---

## 🔑 3. Credenciais Temporárias, EKS e Workloads

- **AWS STS (Security Token Service)**:
  - Emissão de tokens de acesso temporários efêmeros (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) via `AssumeRole`, `AssumeRoleWithWebIdentity` ou `GetSessionToken`.
- **IAM Roles para Workloads EC2, Lambda e ECS**:
  - Utilização de **Instance Profiles** (EC2) e **Execution Roles** (Lambda/ECS) eliminando chaves de acesso gravadas em código ou arquivos de configuração.
- **IRSA (IAM Roles for Service Accounts) & Pod Identity no EKS**:
  - Associação de IAM Roles diretamente a Service Accounts de Kubernetes no Amazon EKS via OpenID Connect (OIDC) ou AWS EKS Pod Identity.

---

## 🏷️ 4. Controle de Acesso Baseado em Atributos (ABAC)

- **Tags como Condição de Autorização**:
  - Criação de políticas escaláveis que autorizam ações dinamicamente se as tags da identidade e do recurso coincidirem:
```json
{
  "Effect": "Allow",
  "Action": ["ec2:StartInstances", "ec2:StopInstances"],
  "Resource": "arn:aws:ec2:*:*:instance/*",
  "Condition": {
    "StringEquals": {
      "aws:ResourceTag/Environment": "${aws:PrincipalTag/Environment}"
    }
  }
}
```

---

## 🔐 5. Políticas de Chaves KMS (KMS Key Policies)

- As chaves de encriptação do **AWS KMS** exigem permissão explícita na **Key Policy** da própria chave.
- Garantir que a Key Policy delegue o controle ao IAM da conta ou especifique os Principais autorizados para ações de decapagem/encriptação (`kms:Decrypt`, `kms:GenerateDataKey`).

---

## 🔍 6. Auditoria, Zero Trust e Troubleshooting

- **IAM Access Analyzer**: Análise matemática automatizada baseada em raciocínio automatizado (*Automated Reasoning*) para identificar recursos expostos publicamente ou para fora da organização.
- **AWS CloudTrail & IAM Access Advisor**:
  - Análise das últimas ações utilizadas por uma IAM Role para redução de permissões não utilizadas (*Role Sizing / Least Privilege*).
- **Ferramentas CLI para Troubleshooting**:
  ```bash
  # Simular avaliação de políticas para uma ação específica
  aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:role/DevRole \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::meu-bucket/objeto.txt

  # Inspecionar credenciais ativas da sessão
  aws sts get-caller-identity
  ```

---

## ⚙️ Protocolo de Decisão do Engenheiro IAM AWS

1. **Bloqueie o Uso de Access Keys Estáticas**: Exija o uso do IAM Identity Center e credenciais temporárias do STS.
2. **Imponha Deny em Tráfego Não Criptografado**: Toda Bucket Policy ou recurso deve negar explicitamente requisições onde `aws:SecureTransport` for `false`.
3. **Utilize SCPs para Bloquear Regiões Desativadas**: Configure SCPs para impedir a criação de recursos fora das regiões AWS homologadas pela empresa.

---

## 🔗 Integração com Outras Skills

- Para integrar IAM com segurança de transporte e encriptação S3/KMS, consulte a skill [cryptography-pqc-standards](../../crypto-pki/cryptography-pqc-standards/SKILL.md).
- Para diretrizes gerais de controle de acesso e federação, consulte a skill [iam-access-management](../iam-access-management/SKILL.md).
- Para alinhar o IAM AWS aos frameworks de compliance e segurança de nuvem, consulte a skill [csa-cloud-security](../csa-cloud-security/SKILL.md).
