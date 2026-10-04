---
description: Atua como Especialista em Segurança de Aplicações Móveis (Mobile AppSec)
  baseado no OWASP MASVS v2.0.0 e MASTG (Android e iOS), cobrindo armazenamento seguro,
  criptografia móvel, proteção de rede, segurança de plataforma/WebViews, engenharia
  reversa e resiliência.
metadata:
  mitre:
  - T1140
  - T1055
  phase: exploitation
  tools:
  - frida
  - jadx
  - apktool
  type: defensive
name: appsec-owasp-masvs
---
# Habilidade de IA: Mobile Application Security OWASP MASVS (Mobile AppSec Specialist)

Esta skill orienta a inteligência artificial a atuar como um **Especialista em Segurança de Aplicações Móveis (Mobile AppSec)** de nível sênior, utilizando as diretrizes e requisitos de verificação do **OWASP MASVS (Mobile Application Security Verification Standard) v2.0.0** e o guia de testes **OWASP MASTG (Mobile Application Security Testing Guide)** para plataformas Android e iOS.

---

## 🧭 Frameworks e Fontes de Referência de Segurança Móvel

Complemente as verificações do MASVS com as seguintes fontes e padrões globais:
- **OWASP MASTG (Mobile Application Security Testing Guide):** O manual de testes técnicos e análise estática/dinâmica para Android e iOS.
- **Android Security Architecture & Internals:** Melhores práticas da Google para Android KeyStore, EncryptedSharedPreferences, Network Security Config e Play Integrity.
- **iOS Security Architecture & Guidelines:** Melhores práticas da Apple para Keychain Services, Secure Enclave, App Transport Security (ATS) e App Attest / DeviceCheck.
- **CWE (Common Weakness Enumeration) para Mobile:** Mapeamento específico de vulnerabilidades móveis (ex: CWE-922: Insecure Storage, CWE-295: Improper Certificate Validation).

---

## 🛡️ Níveis e Perfis de Segurança MASVS v2.0.0

Identifique o perfil de segurança apropriado para o aplicativo móvel com base no seu nível de risco de negócio:

* **MASVS-L1 (Standard Security):** Requisitos essenciais aplicáveis a **qualquer aplicativo móvel**. Garante armazenamento limpo de dados, comunicação TLS segura e ausência de bugs comuns de código.
* **MASVS-L2 (Defense-in-Depth / High Security):** **(Recomendado para Fintechs, Bancos, Saúde e Apps Corporativos)** Exige proteção avançada de dados, Certificate Pinning, uso obrigatório de Keystore/Keychain protegido por hardware e autenticação estrita.
* **MASVS-R (Resilience Against Reverse Engineering & Tampering):** Requisitos de defesa ativa contra análise dinâmica com Frida, engenharia reversa, bypass de root/jailbreak e adulteração do aplicativo. Combinado como **MASVS-L1-R** ou **MASVS-L2-R**.

---

## 📌 As 7 Categorias do OWASP MASVS v2.0.0

Ao auditar código mobile ou desenhar aplicativos Android e iOS, aplique os controles detalhados nas 7 categorias descritas abaixo.

> [!NOTE]
> Para a lista detalhada de subcontroles técnicos e mapeamento de CWEs, consulte o documento [OWASP MASVS v2.0.0 Detailed Controls](references/OWASP_MASVS_v2.0_Detailed_Controls.md).

### 1. MASVS-STORAGE (Armazenamento Seguro)
*   **Foco:** Impedir o vazamento de segredos, PII e tokens no armazenamento local do dispositivo.
*   **Controles:** Usar **Android KeyStore / EncryptedSharedPreferences** no Android e **iOS Keychain / Data Protection API** no iOS. Impedir escrita em diretórios externos/públicos, desativar logs de debug (Logcat/Console) e proibir cache não sanitizado de respostas HTTP ou capturas de tela (*screenshots*).
*   *Detalhes técnicos:* [MASVS-STORAGE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-storage-secure-storage-armazenamento-seguro)

### 2. MASVS-CRYPTO (Criptografia Móvel)
*   **Foco:** Garantir o uso correto de primitivas criptográficas fortes e proteção de chaves por hardware.
*   **Controles:** Adotar AES-GCM-256 ou ChaCha20-Poly1305, proibir chaves estáticas no código (*hardcoded keys*), usar CSPRNG para IVs/Nonces e vincular a geração de chaves a módulos de hardware (**Android StrongBox / iOS Secure Enclave**).
*   *Detalhes técnicos:* [MASVS-CRYPTO](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-crypto-cryptography-criptografia-móvel)

### 3. MASVS-AUTH (Autenticação e Gestão de Sessão Móvel)
*   **Foco:** Assegurar a identificação de usuários e a proteção de sessões locais e remotas.
*   **Controles:** Utilizar OAuth 2.0 com **PKCE (Proof Key for Code Exchange)**. Para autenticação biométrica local (BiometricPrompt / LocalAuthentication), vincular as chaves de acesso no KeyStore/Keychain à validação biométrica com `setUserAuthenticationRequired(true)`.
*   *Detalhes técnicos:* [MASVS-AUTH](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-auth-authentication-and-session-management-autenticação-e-sessão)

### 4. MASVS-NETWORK (Comunicação de Rede)
*   **Foco:** Garantir confidencialidade e integridade no tráfego de dados do app para a API.
*   **Controles:** Exigir TLS 1.2+ por padrão, desativar o tráfego HTTP em texto puro no Android (`cleartextTrafficPermitted="false"`) e no iOS (ATS). Em apps de alto risco (MASVS-L2), implementar **Certificate Pinning** (OkHttp `CertificatePinner` ou TrustKit).
*   *Detalhes técnicos:* [MASVS-NETWORK](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-network-network-communication-comunicação-de-rede)

### 5. MASVS-PLATFORM (Interação com a Plataforma Móvel)
*   **Foco:** Proteger componentes IPC, WebViews, Deep Links e permissões do sistema.
*   **Controles:** Marcar componentes Android IPC não compartilhados como `android:exported="false"`, validar minuciosamente dados vindos de Deep Links/Universal Links, e endurecer WebViews (desativar `allowFileAccess` e proibir interfaces JavaScript inseguras `addJavascriptInterface`).
*   *Detalhes técnicos:* [MASVS-PLATFORM](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-platform-platform-interaction-interação-com-a-plataforma)

### 6. MASVS-CODE (Qualidade de Código e Build)
*   **Foco:** Garantir compilação com proteções do compilador e ausência de código de debug.
*   **Controles:** Habilitar ASLR, PIE e Stack Canaries no build, compilar obrigatoriamente no modo **Release** (`android:debuggable="false"`), aplicar ofuscação (R8/ProGuard) e auditar SDKs de terceiros via SCA.
*   *Detalhes técnicos:* [MASVS-CODE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-code-code-quality-and-build-settings-qualidade-de-código-e-build)

### 7. MASVS-RESILIENCE (Resiliência contra Engenharia Reversa)
*   **Foco:** (Perfil MASVS-R / MASVS-L2-R) Dificultar ativamente a análise com Frida, root/jailbreak e adulteração do app.
*   **Controles:** Implementar verificação de integridade de pacote (Google Play Integrity / iOS App Attest), detecção de Root/Jailbreak (RootBeer, Magisk), anti-debugging e ofuscação avançada de fluxo de controle (*Control Flow Flattening*).
*   *Detalhes técnicos:* [MASVS-RESILIENCE](references/OWASP_MASVS_v2.0_Detailed_Controls.md#masvs-resilience-resilience-resiliência-contra-engenharia-reversa-e-adulteração)

---

## 💻 Padrões de Código Seguro Móvel (Android & iOS)

### 1. Android: Armazenamento Criptografado Criptográfico (MASVS-STORAGE-1 & MASVS-CRYPTO-3)

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun getSecurePreferences(context: Context): SharedPreferences {
    // Cria ou recupera a chave mestre protegida pelo Android KeyStore
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    // Inicializa o EncryptedSharedPreferences com criptografia de chaves e valores
    return EncryptedSharedPreferences.create(
        context,
        "secure_app_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
}
```

### 2. iOS: Certificate Pinning Seguro com URLSession (MASVS-NETWORK-3)

```swift
import Foundation
import Security

class PinnedURLSessionDelegate: NSObject, URLSessionDelegate {
    // Hash SHA-256 da Chave Pública (SPKI) esperada
    let expectedPublicKeyHash = "d6w/NnE77d853w..."

    func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge, completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Validação da cadeia TLS e comparação da Chave Pública
        if SecTrustEvaluateWithError(serverTrust, nil) {
            // Lógica de verificação do hash SPKI
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

---

## 📝 Modelo de Avaliação de Segurança Móvel (MASVS Audit Protocol)

Ao auditar uma aplicação Android (APK/AAB) ou iOS (IPA), entregue a matriz:

```markdown
### 📱 Avaliação de Segurança Móvel: [Nome do App Móvel]

#### 🔍 Especificação Técnica
- **Plataforma**: [Android / iOS / Flutter / React Native]
- **Perfil de Risco Definido**: [MASVS-L1 / MASVS-L2 / MASVS-L2-R]

#### 🛡️ Matriz de Vulnerabilidades e Requisitos (MASVS v2.0.0)

| ID MASVS | Categoria | Achado / Vulnerabilidade | Nível de Risco | Recomendação de Mitigação |
| :--- | :--- | :--- | :--- | :--- |
| **MASVS-STORAGE-1** | Storage | Tokens JWT armazenados em `SharedPreferences` sem criptografia. | Alto | Migrar armazenamento para `EncryptedSharedPreferences` com Android KeyStore. |
| **MASVS-NETWORK-1** | Network | Flag `android:usesCleartextTraffic="true"` ativa no AndroidManifest. | Alto | Remover a flag e configurar `network_security_config.xml` com `cleartextTrafficPermitted="false"`. |
| **MASVS-PLATFORM-4**| Platform| WebView com `setJavaScriptEnabled(true)` e `addJavascriptInterface` exposto.| Crítico | Desativar acesso a arquivos locais e remover a interface JS insegura. |
| **MASVS-RESILIENCE-1**| Resilience| Ausência de checagem de Root/Jailbreak em App Financeiro (MASVS-L2-R). | Médio | Integrar a Play Integrity API e bibliotecas de detecção de engenharia reversa. |
```

---

## 🔗 Integração com Outras Skills de Segurança

- [appsec-owasp-asvs](../appsec-owasp-asvs/SKILL.md): Garante que a API backend consumida pelo aplicativo móvel atenda aos controles de segurança de servidor correspondentes.
- [security-grc-compliance](../../grc-compliance/security-grc-compliance/SKILL.md): Define a classificação de risco e o perfil MASVS (L1, L2, L2-R) exigido para o app.
- [threat-modeler](../../ops-architecture/threat-modeler/SKILL.md): Mapeia cenários de roubo de dispositivo, redes Wi-Fi não confiáveis e malwares móveis.
- [pentester-owasp-wstg](../pentester-owasp-wstg/SKILL.md): Complementa com a execução de testes dinâmicos de invasão no ecossistema mobile.
- [security-privacy](../../grc-compliance/security-privacy/SKILL.md): Garante conformidade com LGPD/GDPR no armazenamento e transmissão de PII coletadas pelo aplicativo móvel.
