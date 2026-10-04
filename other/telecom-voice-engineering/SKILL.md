---
name: "telecom-voice-engineering"
description: "Fornece padrões de arquitetura, engenharia e segurança em telefonia e redes de voz. Cobre protocolos VoIP (SIP, SDP, RTP, SRTP), Session Border Controllers (SBC), rede legada (PSTN, E1/T1, ISDN, SS7), WebRTC, codecs de áudio (G.711, G.729, Opus), Softswitches (Kamailio, OpenSIPS, FreeSWITCH, Asterisk), QoS (DSCP EF), STIR/SHAKEN e prevenção a fraudes de telefonia."
---

# Habilidade de IA: Engenharia de Voz e Telefonia (Telecom & Voice Specialist)

Esta skill orienta a inteligência artificial a atuar como **Especialista em Engenharia de Voz, Telefonia e Comunicações em Tempo Real**, abrangendo desde redes legadas de telefonia comutada (**PSTN**) até arquiteturas avançadas de **VoIP (Voice over IP)**, **SBC (Session Border Controllers)**, **WebRTC** e segurança de telecomunicações.

---

## 🧭 Arquitetura de Redes de Telefonia e Protocolos de Voz

### 1. Sinalização e Transporte VoIP
- **SIP (Session Initiation Protocol - RFC 3261)**:
  - Métodos fundamentais: `INVITE`, `ACK`, `BYE`, `CANCEL`, `REGISTER`, `OPTIONS`, `INFO`, `SUBSCRIBE`, `NOTIFY`.
  - Códigos de Resposta: `1xx` (Informativo - 180 Ringing, 183 Session Progress), `2xx` (Sucesso - 200 OK), `3xx` (Redirecionamento), `4xx` (Erro do Cliente - 404 Not Found, 486 Busy, 488 Not Acceptable), `5xx` (Erro do Servidor), `6xx` (Falha Global).
  - **SDP (Session Description Protocol - RFC 4566)**: Negociação de mídias, endereços IP, portas UDP e codecs suportados durante o handshake SIP.
- **RTP / RTCP / SRTP**:
  - **RTP (Real-time Transport Protocol - RFC 3550)**: Transporte de pacotes de voz sobre UDP.
  - **RTCP (RTP Control Protocol)**: Monitoramento de métricas de qualidade da transmissão (jitter, perda de pacotes, RTT).
  - **SRTP (Secure Real-time Transport Protocol - RFC 3711)**: Criptografia de mídia via AES-128/256 negociada por SDES ou DTLS-SRTP.

### 2. Telefonia Tradicional e Interconexão PSTN
- **PSTN (Public Switched Telephone Network) & TDM**:
  - Troncos E1 (30 canais 64kbps / 2.048 Mbps) e T1 (24 canais / 1.544 Mbps) usando sinalização **ISDN PRI** (Q.931) ou CAS (R2/Digital).
  - **SS7 (Signaling System No. 7)**: Protocolo out-of-band de sinalização entre centrais telefônicas da rede pública (ISUP, TCAP, MAP).
  - Interfaces analógicas: **FXS** (fornece tom de discagem e voltagem de campainha) e **FXO** (conecta à linha telefônica da operadora).

---

## 🛠️ Session Border Controllers (SBC) & Proxies SIP

O **SBC** atua como a fronteira de segurança, roteamento e normalização entre redes VoIP internas, operadoras (Sip Trunks) e a internet:

### 1. Funções Essenciais de um SBC
- **B2BUA (Back-to-Back User Agent)**: Separação total de sessões entre a perna de entrada (*ingress*) e de saída (*egress*), ocultando a topologia interna da rede (*Topology Hiding*).
- **NAT Traversal**: Resolução de endereços IP privados/públicos em pacotes SIP e fluxos RTP utilizando algoritmos de ancoragem de mídia (*Media Anchoring*), STUN, TURN e ICE.
- **HMR / HPL (Header Manipulation Rules)**: Reescrita e sanitização dinâmica de cabeçalhos SIP (`From`, `To`, `Contact`, `P-Asserted-Identity`, `Diversion`).
- **Controle de Admissão de Chamadas (CAC)**: Limitação de taxa de chamadas por segundo (CPS) e chamadas simultâneas para prevenção de sobrecarga e mitigação de ataques DoS/DDoS SIP.

### 2. Tecnologias de Mercado
- **SBCs de Operadora / Enterprise**: Oracle Acme Packet, Ribbon (Sonus), AudioCodes Mediant.
- **Softswitches e Proxies SIP Open Source**:
  - **Kamailio / OpenSIPS**: Proxies SIP de ultra-alta performance para roteamento de milhões de chamadas, balanceamento de carga e registradores estáticos/dinâmicos.
  - **FreeSWITCH / Asterisk**: Servidores de mídia B2BUA, URA (IVR), gravação de chamadas e transcodificação.

---

## 🔊 Codecs de Áudio, QoS e WebRTC

### 1. Seleção e Comparativo de Codecs
| Codec | Taxa de Bits (Bitrate) | Tipo de Banda | Uso Típico |
| :--- | :--- | :--- | :--- |
| **G.711 (PCMU / PCMA)** | 64 kbps | Narrowband (8 kHz) | Padrão PSTN/VoIP tradicional sem perda por compressão. |
| **G.729a/b** | 8 kbps | Narrowband (8 kHz) | Compressão alta (CS-ACELP) para troncos de baixa largura de banda. |
| **Opus** | 6 a 510 kbps (dinâmico) | Fullband / Superwideband (48 kHz) | Padrão ouro do WebRTC; adaptação dinâmica à oscilação de rede. |
| **AMR-WB (G.722.2)** | 6.6 a 23.85 kbps | Wideband (16 kHz) | Padrão HD Voice em redes móveis (VoLTE / VoNR). |

### 2. Qualidade de Serviço (QoS) e Métricas
- **Marcação DiffServ (DSCP)**:
  - Pacotes de Mídia RTP: Marcação obrigatória **DSCP EF (Expedited Forwarding - 46 / 0xb8)**.
  - Pacotes de Sinalização SIP: Marcação **DSCP AF31 (26)** ou **CS3 (24)**.
- **Métricas Alvo em Produção**:
  - **Latência (Unidirecional)**: < 150 ms (RTT < 300 ms).
  - **Jitter**: < 30 ms.
  - **Perda de Pacotes (Packet Loss)**: < 1%.
  - **MOS (Mean Opinion Score)**: > 4.0 em uma escala de 1 a 5.

### 3. WebRTC e Telefonia na Web
- Sinalização sobre WebSockets cifrados (`wss://`).
- Negociação DTLS-SRTP para criptografia obrigatória de mídia sem chaves em texto claro no SDP.
- Requisitos de codec: Suporte mandatório a Opus e G.711.

---

## 🔒 Segurança em Voz, STIR/SHAKEN e Mitigação de Fraudes

### 1. Hardening e Proteção da Infraestrutura VoIP
- **SIPS (SIP over TLS)**: Criptografia da sinalização SIP na porta `5061` com validação mTLS de certificados da operadora.
- **Prevenção de Toll Fraud**:
  - Restrição rigorosa de planos de discagem para destinos internacionais de alto custo.
  - Autenticação obrigatória para todas as requisições `INVITE` originadas internamente.
  - Bloqueio imediato de varredura por `REGISTER` sem senha (ferramentas como SIPP, Friendly-Scanner, Svwar).

### 2. Autenticação de Chamadas com STIR/SHAKEN
- **STIR (Secure Telephony Identity Revisited - RFC 8224)**: Assinatura criptográfica X.509 no cabeçalho SIP `Identity` para atestar a autenticidade do número de origem (*Caller ID*).
- **SHAKEN (Signature-based Handling of Asserted information using tokens)**: Framework operacional para atribuição de níveis de atestado (A, B, C) pelas operadoras para eliminação de falsificação de número (*Caller ID Spoofing*).

---

## 🔗 Integração com Outras Skills

- Para segurança de voz em dispositivos de assistência por voz, STT/TTS e IVR, consulte [ai-voice-stt-tts-security](../../security/ai-security/ai-voice-stt-tts-security/SKILL.md).
- Para desenvolvimento de APIs de controle de chamadas (Twilio, Asterisk AGI/ARI, FreeSWITCH ESL), consulte [backend-developer](../../roles/backend-developer/SKILL.md) e [lang-python](../../languages/lang-python/SKILL.md).
- Para segurança de rede on-premises e nuvem (firewalls, microsegmentação de voz), consulte [network-security-onprem-cloud](../../security/grc-compliance/network-security-onprem-cloud/SKILL.md) e [auth-protocols-mfa](../../security/ops-architecture/auth-protocols-mfa/SKILL.md).
