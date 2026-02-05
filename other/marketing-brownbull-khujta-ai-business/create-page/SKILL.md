---
name: create-page
description: CareMatch용 Next.js 페이지 생성. Pages Router 기반 페이지를 생성하며 SEO, 인증, 레이아웃이 자동 적용됩니다. 사용법 - "페이지 만들어줘", "간병인 대시보드 페이지 생성"
allowed-tools: Read, Write, Glob
---

# Create Page Skill

CareMatch V3용 Next.js 페이지를 생성합니다.

## 페이지 템플릿

```typescript
// pages/{path}.tsx
import { type NextPage, type GetServerSideProps } from 'next'
import { getServerSession } from 'next-auth'
import Head from 'next/head'
import { Layout } from '@/components/layout/Layout'
import { authOptions } from '@/pages/api/auth/[...nextauth]'

interface PageProps {
  // props 정의
}

const Page: NextPage<PageProps> = (props) => {
  return (
    <>
      <Head>
        <title>페이지 제목 | CareMatch</title>
        <meta name="description" content="페이지 설명" />
      </Head>

      <Layout>
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold mb-8">
            페이지 제목
          </h1>
          {/* 내용 */}
        </div>
      </Layout>
    </>
  )
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const session = await getServerSession(context.req, context.res, authOptions)

  if (!session) {
    return {
      redirect: { destination: '/auth/login', permanent: false },
    }
  }

  return { props: {} }
}

export default Page
```

## 페이지 구조

| 경로 | 설명 |
|------|------|
| pages/auth/ | 인증 관련 |
| pages/caregiver/ | 간병인 전용 |
| pages/guardian/ | 보호자 전용 |
| pages/chat/ | 채팅 |
