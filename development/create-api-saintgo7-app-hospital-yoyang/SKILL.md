---
name: create-api
description: CareMatch용 Next.js API 라우트 생성. 인증, 입력 검증, 에러 처리가 포함된 API 엔드포인트를 생성합니다. 사용법 - "API 만들어줘", "지원 API 생성"
allowed-tools: Read, Write, Glob
---

# Create API Skill

CareMatch V3용 Next.js API 라우트를 생성합니다.

## API 템플릿

```typescript
// pages/api/{path}.ts
import type { NextApiRequest, NextApiResponse } from 'next'
import { getServerSession } from 'next-auth'
import { authOptions } from '../auth/[...nextauth]'
import { supabase } from '@/lib/supabase'
import { z } from 'zod'

interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  error?: string
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ApiResponse>
) {
  const session = await getServerSession(req, res, authOptions)

  if (!session) {
    return res.status(401).json({
      success: false,
      error: '로그인이 필요합니다',
    })
  }

  switch (req.method) {
    case 'GET':
      return handleGet(req, res, session)
    case 'POST':
      return handlePost(req, res, session)
    default:
      res.setHeader('Allow', ['GET', 'POST'])
      return res.status(405).json({
        success: false,
        error: `${req.method} 메서드는 지원하지 않습니다`,
      })
  }
}
```

## 규칙

- 인증 체크 필수
- Zod로 입력 검증
- 한국어 에러 메시지
- 적절한 HTTP 상태 코드
