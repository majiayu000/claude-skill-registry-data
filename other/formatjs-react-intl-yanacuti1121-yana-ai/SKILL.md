---
name: formatjs--react-intl
description: "i18n cho React apps — react-intl, FormatJS. Dùng khi implement đa ngôn ngữ, format số/ngày/tiền tệ chuẩn theo locale."
allowed-tools: Bash, Read, Write
user-invocable: true
---

FormatJS / react-intl là monorepo i18n chuẩn cho React. Format messages, dates, numbers, currencies theo locale.

## Install

```bash
npm install react-intl
```

## Basic setup

```tsx
import { IntlProvider, FormattedMessage } from 'react-intl'

const messages = {
  'app.greeting': 'Hello, {name}!',
}

<IntlProvider locale="en" messages={messages}>
  <FormattedMessage id="app.greeting" values={{ name: 'Tâm' }} />
</IntlProvider>
```

## Format patterns

```tsx
// Number / currency
<FormattedNumber value={1000} style="currency" currency="VND" />
// → ₫1.000

// Date
<FormattedDate value={new Date()} year="numeric" month="long" day="2-digit" />

// Relative time
<FormattedRelativeTime value={-1} unit="day" />
// → yesterday
```

## Extract & compile messages

```bash
# Extract from source
npx formatjs extract 'src/**/*.tsx' --out-file messages/en.json

# Compile for production
npx formatjs compile messages/vi.json --out-file compiled/vi.json
```

## Source

https://github.com/formatjs/formatjs · ⭐14.7K
