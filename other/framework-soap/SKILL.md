---
name: "framework-soap"
description: "Fornece padrões de engenharia e integração de serviços web baseados nos padrões W3C SOAP 1.1/1.2 e WSDL 1.1/2.0. Cobre estrutura do XML Envelope, segurança de mensagens com WS-Security (WSS), assinatura digital (XML-Signature), validação por XSD e integração corporativa."
---

# Habilidade de IA: Engenharia e Integração de Serviços SOAP (framework-soap)

Esta skill orienta a inteligência artificial a atuar como especialista nos protocolos de comunicação orientados a mensagens **SOAP (Simple Object Access Protocol)** e definições de serviço **WSDL (Web Services Description Language)**, alinhada às recomendações do W3C ([w3.org/TR/soap/](https://www.w3.org/TR/soap/)) e especificações WS-*. Cobre integrações corporativas legadas, bancos, governança de esquemas XML e padrões de segurança de mensagens.

---

## 🧭 Estrutura da Mensagem SOAP e Contrato WSDL

### 1. Estrutura do Envelope SOAP (1.1 / 1.2)
Toda mensagem SOAP deve ser um documento XML válido estruturado em um `Envelope`, um `Header` opcional (usado para credenciais e WS-Addressing) e um `Body` contendo os dados do método ou o erro (`Fault`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://services.empresa.com/banking">
   <soapenv:Header>
      <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
         <wsse:UsernameToken>
            <wsse:Username>usuario_api</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">senha_segura</wsse:Password>
         </wsse:UsernameToken>
      </wsse:Security>
   </soapenv:Header>
   <soapenv:Body>
      <web:ConsultarSaldoRequest>
         <web:NumeroConta>123456-7</web:NumeroConta>
      </web:ConsultarSaldoRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

### 2. Desenvolvimento Contract-First (WSDL & XSD)
- Desenvolva contratos estritos em **WSDL** definindo `types`, `message`, `portType` (ou `interface`), `binding` e `service`.
- Defina tipos de dados complexos em schemas **XSD (XML Schema Definition)** separados para reaproveitamento e validação forte no parser XML antes da execução da lógica de negócios.

---

## 🔒 Segurança de Mensagens Corporativas (WS-Security)

Diferente do REST/gRPC que dependem prioritariamente de TLS no transporte, o SOAP suporta criptografia e assinatura de segurança no **nível de mensagem** (WS-Security):

- **UsernameToken Profile**: Autenticação de usuário e hash digest de senha no `Header`.
- **X.509 Certificate Token Profile**: Uso de chaves assimétricas para assinatura digital (`XML-Signature`) de partes específicas do `Body` para não-repúdio.
- **XML Encryption**: Criptografia de nós específicos da mensagem para tráfego seguro por múltiplos proxies intermediários (ESBs).

---

## 🚨 Tratamento de Erros com SOAP Fault

Erros durante o processamento devem retornar a estrutura padronizada `<soapenv:Fault>` dentro do `<soapenv:Body>`:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <soapenv:Fault>
         <faultcode>soapenv:Client</faultcode>
         <faultstring>Número de conta inválido ou não encontrado</faultstring>
         <faultactor>http://services.empresa.com/banking</faultactor>
         <detail>
            <err:ErrorDetail xmlns:err="http://services.empresa.com/errors">
               <err:ErrorCode>ACCOUNT_NOT_FOUND</err:ErrorCode>
            </err:ErrorDetail>
         </detail>
      </soapenv:Fault>
   </soapenv:Body>
</soapenv:Envelope>
```

---

## 🔗 Integração com Outras Skills

- Para arquitetura de integração corporativa (ESB, sistemas legados e bancários), consulte [backend-developer](../../roles/backend-developer/SKILL.md), [financial-transaction-processing](../../domains/financial-transaction-processing/SKILL.md) e [software-architect](../../roles/software-architect/SKILL.md).
- Para auditoria de vulnerabilidades em serviços SOAP e XML (XXE, XML Bomb, WS-Security bypass), consulte [pentester-owasp-wstg](../../security/appsec/pentester-owasp-wstg/SKILL.md) e [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
