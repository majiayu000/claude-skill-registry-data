---
name: message-dispatcher
description: 이메일 및 카카오톡 알림톡 통합 발송 관리
version: 2.0.0
trigger: "메시지 발송"
updated: 2025-12-30
---

# Message Dispatcher 스킬

## 🎯 역할

생성된 콘텐츠를 소원이에게 발송:
1. **이메일 발송**: SendGrid 연동
2. **카카오톡 발송**: Solapi 알림톡
3. **스케줄링**: 예약 발송 관리

## 📥 입력

```json
{
  "recipient": {
    "name": "소원이 이름",
    "phone": "010-0000-0000",
    "email": "sowoni@example.com"
  },
  "channel": "kakao|email|both",
  "content": {
    "type": "message|pdf|magic-link",
    "body": "메시지 내용",
    "attachments": []
  },
  "schedule": "2025-12-22T09:00:00+09:00"
}
```

## 📤 출력

```json
{
  "success": true,
  "messageId": "msg_123456",
  "channel": "kakao",
  "sentAt": "2025-12-22T09:00:01+09:00",
  "status": "delivered"
}
```

## 📡 발송 채널

### 카카오톡 (Solapi) ✅ 구현 완료

**구현 파일**: `services/solapiService.js`

**채널 정보**:
- 채널명: 하루하루의 기적
- 채널 ID: @dailymiracles
- URL: http://pf.kakao.com/_xfxhcWn

**API 함수**:
```javascript
// 알림톡 발송
sendKakaoAlimtalk(to, templateId, variables)

// SMS 발송 (fallback)
sendSMS(to, text)

// 소원 ACK 발송 (통합)
sendWishAck(phone, wishData)

// RED 신호 긴급 알림
sendRedAlert(wishData)
```

**환경변수**:
```env
SOLAPI_API_KEY=       # Solapi API 키
SOLAPI_API_SECRET=    # Solapi API 시크릿
SOLAPI_PFID=          # 카카오 채널 ID
SENDER_PHONE=18996117 # 발신번호
SOLAPI_TEMPLATE_WISH_ACK=  # 소원 ACK 템플릿 ID (승인 후)
CRO_PHONE=            # RED 알림 수신자 (재미)
```

**메시지 템플릿**: `config/messageTemplates.js`
- `generateWishAckMessage()` - 소원 접수 ACK
- `generateRedAlertMessage()` - RED 신호 긴급 알림

### 이메일 (SendGrid)
- HTML 템플릿
- PDF 첨부 가능
- 열람 추적

## ⚡ 속도 기준

- 목표: 3초
- 최대: 5초

## 🔗 의존

← wish-writer (메시지)
← roadmap-generator (PDF)
→ comi-orchestrator (발송 로그)
