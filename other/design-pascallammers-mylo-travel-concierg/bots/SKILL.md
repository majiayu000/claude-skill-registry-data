---
name: bots
description: Use when building Towns Protocol bots - covers SDK initialization, slash commands, message handlers, reactions, interactive forms, blockchain operations, and deployment
---

# Towns Protocol Bot SDK Reference

## Critical Rules

**MUST follow these rules - violations cause silent failures:**

1. **User IDs are Ethereum addresses** - Always `0x...` format, never usernames
2. **Mentions require BOTH** - `<@{userId}>` format in text AND `mentions` array in options
3. **Two-wallet architecture**:
   - `bot.viem.account.address` = Gas wallet (signs & pays fees) - **MUST fund with Base ETH**
   - `bot.appAddress` = Treasury (optional, for transfers)
4. **Slash commands DON'T trigger onMessage** - They're exclusive handlers
5. **Interactive forms use `type` property** - Not `case` (e.g., `type: 'form'`)
6. **Never trust txHash alone** - Verify `receipt.status === 'success'` before granting access

## Quick Reference

### Key Imports

```typescript
import { makeTownsBot, getSmartAccountFromUserId } from '@towns-protocol/bot'
import type { BotCommand, BotHandler } from '@towns-protocol/bot'
import { Permission } from '@towns-protocol/web3'
import { parseEther, formatEther, erc20Abi, zeroAddress } from 'viem'
import { readContract, waitForTransactionReceipt } from 'viem/actions'
import { execute } from 'viem/experimental/erc7821'
```

### Handler Methods

| Method | Signature | Notes |
|--------|-----------|-------|
| `sendMessage` | `(channelId, text, opts?) → { eventId }` | opts: `{ threadId?, replyId?, mentions?, attachments? }` |
| `editMessage` | `(channelId, eventId, text)` | Bot's own messages only |
| `removeEvent` | `(channelId, eventId)` | Bot's own messages only |
| `sendReaction` | `(channelId, messageId, emoji)` | |
| `sendInteractionRequest` | `(channelId, payload)` | Forms, transactions, signatures |
| `hasAdminPermission` | `(userId, spaceId) → boolean` | |
| `ban` / `unban` | `(userId, spaceId)` | Needs ModifyBanning permission |

### Bot Properties

| Property | Description |
|----------|-------------|
| `bot.viem` | Viem client for blockchain |
| `bot.viem.account.address` | Gas wallet - **MUST fund with Base ETH** |
| `bot.appAddress` | Treasury wallet (optional) |
| `bot.botId` | Bot identifier |

## Bot Setup

### Project Initialization

```bash
bunx towns-bot init my-bot
cd my-bot
bun install
```

### Environment Variables

```bash
APP_PRIVATE_DATA=<base64_credentials>   # From app.towns.com/developer
JWT_SECRET=<webhook_secret>              # Min 32 chars
PORT=3000
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/KEY  # Recommended
```

### Basic Bot Template

```typescript
import { makeTownsBot } from '@towns-protocol/bot'
import type { BotCommand } from '@towns-protocol/bot'

const commands = [
  { name: 'help', description: 'Show help' },
  { name: 'ping', description: 'Check if alive' }
] as const satisfies BotCommand[]

const bot = await makeTownsBot(
  process.env.APP_PRIVATE_DATA!,
  process.env.JWT_SECRET!,
  { commands }
)

bot.onSlashCommand('ping', async (handler, event) => {
  const latency = Date.now() - event.createdAt.getTime()
  await handler.sendMessage(event.channelId, 'Pong! ' + latency + 'ms')
})

export default bot.start()
```

### Config Validation

Validate environment on startup to fail fast:

```typescript
import { z } from 'zod'

const EnvSchema = z.object({
  APP_PRIVATE_DATA: z.string().min(1),
  JWT_SECRET: z.string().min(32),
  DATABASE_URL: z.string().url().optional()
})

const env = EnvSchema.safeParse(process.env)
if (!env.success) {
  console.error('Invalid config:', env.error.issues)
  process.exit(1)
}
```

## Event Handlers

### onMessage

Triggers on regular messages (NOT slash commands).

```typescript
bot.onMessage(async (handler, event) => {
  // event: { userId, spaceId, channelId, eventId, message, isMentioned, threadId?, replyId? }

  if (event.isMentioned) {
    await handler.sendMessage(event.channelId, 'You mentioned me!')
  }

  if (event.message.includes('hello')) {
    await handler.sendMessage(event.channelId, 'Hello there!')
  }
})
```

### onSlashCommand

Triggers on `/command`. Does NOT trigger onMessage.

```typescript
bot.onSlashCommand('weather', async (handler, { args, channelId }) => {
  // /weather San Francisco → args: ['San', 'Francisco']
  const location = args.join(' ')
  if (!location) {
    await handler.sendMessage(channelId, 'Usage: /weather <location>')
    return
  }
  // ... fetch weather
})
```

### onReaction

```typescript
bot.onReaction(async (handler, event) => {
  // event: { reaction, messageId, channelId }
  if (event.reaction === '👋') {
    await handler.sendMessage(event.channelId, 'I saw your wave!')
  }
})
```

### onTip

Requires "All Messages" mode in Developer Portal.

```typescript
bot.onTip(async (handler, event) => {
  // event: { senderAddress, receiverAddress, amount (bigint), currency }
  if (event.receiverAddress === bot.appAddress) {
    await handler.sendMessage(event.channelId,
      'Thanks for ' + formatEther(event.amount) + ' ETH!')
  }
})
```

### onInteractionResponse

```typescript
bot.onInteractionResponse(async (handler, event) => {
  switch (event.response.payload.content?.case) {
    case 'form':
      const form = event.response.payload.content.value
      for (const c of form.components) {
        if (c.component.case === 'button' && c.id === 'yes') {
          await handler.sendMessage(event.channelId, 'You clicked Yes!')
        }
      }
      break
    case 'transaction':
      const tx = event.response.payload.content.value
      if (tx.txHash) {
        await handler.sendMessage(event.channelId,
          'Success: https://basescan.org/tx/' + tx.txHash)
      }
      break
  }
})
```

### Event Context Validation

Always validate context before using - events can have missing fields:

```typescript
bot.onSlashCommand('cmd', async (handler, event) => {
  if (!event.spaceId || !event.channelId) {
    console.error('Missing context:', { userId: event.userId })
    return
  }
  // Safe to proceed
})
```

## Messaging API

### Send Message with Mention

**MUST include BOTH formatted text AND mentions array:**

```typescript
// Format: Hello <@0x...>!
const text = 'Hello <@' + userId + '>!'
await handler.sendMessage(channelId, text, {
  mentions: [{ userId, displayName: 'User' }]
})

// @channel
await handler.sendMessage(channelId, 'Attention!', {
  mentions: [{ atChannel: true }]
})
```

### Threads & Replies

```typescript
// Reply in thread
await handler.sendMessage(channelId, 'Thread reply', { threadId: event.eventId })

// Reply to specific message
await handler.sendMessage(channelId, 'Reply', { replyId: messageId })
```

### Attachments

```typescript
// Image
attachments: [{ type: 'image', url: 'https://...jpg', alt: 'Description' }]

// Miniapp
attachments: [{ type: 'miniapp', url: 'https://your-app.com/miniapp.html' }]

// Large file (chunked)
attachments: [{
  type: 'chunked',
  data: readFileSync('./video.mp4'),
  filename: 'video.mp4',
  mimetype: 'video/mp4'
}]
```

### Message Formatting

Towns has specific rendering behavior:
- **Use `\n\n`** (double newlines) between sections - single `\n` causes overlap
- **Never use `---`** as separator - renders as zero-height rule
- **Use middot** for inline data: `Value: $1.00 · P&L: $0.50`

```typescript
// Good - double newlines
const msg = ['**Header**', 'Line 1', 'Line 2'].join('\n\n')

// Bad - single newlines will collapse
const bad = lines.join('\n')
```

## Interactive Components

### Send Button Form

```typescript
await handler.sendInteractionRequest(channelId, {
  type: 'form',           // NOT 'case'
  id: 'my-form',
  components: [
    { id: 'yes', type: 'button', label: 'Yes' },
    { id: 'no', type: 'button', label: 'No' }
  ],
  recipient: event.userId  // Optional: private to this user
})
```

### Request Transaction

```typescript
import { encodeFunctionData, erc20Abi, parseUnits } from 'viem'

await handler.sendInteractionRequest(channelId, {
  type: 'transaction',
  id: 'payment',
  title: 'Send Tokens',
  subtitle: 'Transfer 50 USDC',
  tx: {
    chainId: '8453',
    to: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  // USDC
    value: '0',
    data: encodeFunctionData({
      abi: erc20Abi,
      functionName: 'transfer',
      args: [recipient, parseUnits('50', 6)]
    })
  },
  recipient: event.userId
})
```

## Blockchain Operations

### Read Contract

```typescript
const balance = await readContract(bot.viem, {
  address: tokenAddress,
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: [userAddress]
})
```

### Execute Transaction

```typescript
const hash = await execute(bot.viem, {
  address: bot.appAddress,
  account: bot.viem.account,
  calls: [{
    to: targetAddress,
    abi: contractAbi,
    functionName: 'transfer',
    args: [recipient, amount]
  }]
})

await waitForTransactionReceipt(bot.viem, { hash })
```

### Verify Transaction (Critical for Payments)

**Never grant access based on txHash alone.** Always verify on-chain:

```typescript
bot.onInteractionResponse(async (handler, event) => {
  if (event.response.payload.content?.case !== 'transaction') return
  const tx = event.response.payload.content.value

  if (tx.txHash) {
    const receipt = await waitForTransactionReceipt(bot.viem, {
      hash: tx.txHash
    })

    if (receipt.status !== 'success') {
      await handler.sendMessage(event.channelId, 'Transaction failed on-chain')
      return
    }

    // NOW safe to grant access
    await grantUserAccess(event.userId)
    await handler.sendMessage(event.channelId, 'Payment confirmed!')
  }
})
```

### Token Addresses (Base Mainnet)

```typescript
const TOKENS = {
  ETH: zeroAddress,
  USDC: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  TOWNS: '0x00000000A22C618fd6b4D7E9A335C4B96B189a38'
}
```

## Deployment

### Local Development

```bash
# Start bot (default port 5123)
bun run dev

# Expose webhook via Tailscale Funnel
tailscale funnel 5123
# Creates URL like: https://your-machine.taild8e1b0.ts.net/

# Alternative: ngrok
ngrok http 5123
```

**Setup webhook in Developer Portal:**
1. Go to https://app.towns.com/developer
2. Select your bot
3. Set Webhook URL to your tunnel URL + `/webhook`
   - Example: `https://your-machine.taild8e1b0.ts.net/webhook`
4. Save changes

**Testing checklist:**
- Bot server running (`bun run dev`)
- Tunnel active (Tailscale/ngrok)
- Webhook URL updated in Developer Portal
- Bot installed in a Space and added to a channel
- Check logs for incoming webhook events

### Render.com

1. Create Web Service from Git repo
2. Set environment variables (APP_PRIVATE_DATA, JWT_SECRET)
3. Set webhook URL in app.towns.com/developer

### Check Balances

```typescript
const gasBalance = await bot.viem.getBalance({ address: bot.viem.account.address })
const treasuryBalance = await bot.viem.getBalance({ address: bot.appAddress })
console.log('Gas: ' + formatEther(gasBalance) + ' ETH')
```

### Graceful Shutdown

Handle SIGTERM for clean shutdown (required for Render/Kubernetes):

```typescript
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing...')
  await pool.end()  // Close DB connections
  process.exit(0)
})
```

## Advanced Patterns

### Database Connection Pool

```typescript
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
})

// Health check on startup
await pool.query('SELECT 1')
```

### Thread Ownership (Race-Safe)

```typescript
// First writer wins
await pool.query(
  `INSERT INTO threads (thread_id, user_id)
   VALUES ($1, $2)
   ON CONFLICT (thread_id) DO NOTHING`,
  [threadId, userId]
)

// Check ownership
const result = await pool.query(
  'SELECT user_id FROM threads WHERE thread_id = $1',
  [threadId]
)
return result.rows[0]?.user_id === userId
```

## Debugging

### Handler Not Triggering

Most common issue. Check in order:

1. **Webhook URL correct?**
   ```bash
   # Your bot should log incoming requests
   curl -X POST https://your-webhook-url/webhook \
     -H "Content-Type: application/json" \
     -d '{"test": true}'
   ```

2. **Tunnel running?** (local dev)
   ```bash
   # Tailscale
   tailscale funnel status

   # ngrok
   curl http://127.0.0.1:4040/api/tunnels
   ```

3. **Bot added to channel?** Bot must be:
   - Installed in the Space (Settings → Integrations)
   - Added to the specific channel (Channel Settings → Integrations)

4. **Message forwarding mode?** In Developer Portal:
   - "Mentions Only" = only `@bot` messages
   - "All Messages" = everything (required for `onTip`)

5. **Slash command registered?** Must be in `commands` array passed to `makeTownsBot`

### Add Request Logging

```typescript
const bot = await makeTownsBot(
  process.env.APP_PRIVATE_DATA!,
  process.env.JWT_SECRET!,
  { commands }
)

// Log all incoming events
bot.onMessage(async (handler, event) => {
  console.log('[onMessage]', {
    userId: event.userId,
    channelId: event.channelId,
    message: event.message.slice(0, 100),
    isMentioned: event.isMentioned
  })
  // ... rest of handler
})

bot.onSlashCommand('*', async (handler, event) => {
  console.log('[onSlashCommand]', {
    command: event.command,
    args: event.args,
    userId: event.userId
  })
})
```

### Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `JWT verification failed` | Wrong JWT_SECRET | Match secret in Developer Portal |
| `insufficient funds for gas` | Empty gas wallet | Fund `bot.viem.account.address` |
| `Invalid APP_PRIVATE_DATA` | Malformed credentials | Re-copy from Developer Portal |
| `ECONNREFUSED` on RPC | Bad RPC URL or rate limited | Use dedicated RPC (Alchemy/Infura) |
| `nonce too low` | Concurrent transactions | Add transaction queue or retry logic |

### Verify Webhook Connectivity

```typescript
// Add health check endpoint
import { Hono } from 'hono'

const app = new Hono()

app.get('/health', (c) => c.json({
  status: 'ok',
  timestamp: new Date().toISOString(),
  gasWallet: bot.viem.account.address
}))

// Test from outside
// curl https://your-webhook-url/health
```

### Debug Transaction Failures

```typescript
import { waitForTransactionReceipt } from 'viem/actions'

try {
  const hash = await execute(bot.viem, { /* ... */ })
  console.log('TX submitted:', hash)

  const receipt = await waitForTransactionReceipt(bot.viem, { hash })
  console.log('TX result:', {
    status: receipt.status,
    gasUsed: receipt.gasUsed.toString(),
    blockNumber: receipt.blockNumber
  })

  if (receipt.status !== 'success') {
    console.error('TX reverted. Check on basescan:',
      'https://basescan.org/tx/' + hash)
  }
} catch (err) {
  console.error('TX failed:', err.message)
  // Common: insufficient funds, nonce issues, contract revert
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `insufficient funds for gas` | Fund `bot.viem.account.address` with Base ETH |
| Mention not highlighting | Include BOTH `<@userId>` in text AND `mentions` array |
| Slash command not working | Add to `commands` array in makeTownsBot |
| Handler not triggering | Check message forwarding mode in Developer Portal |
| `writeContract` failing | Use `execute()` for external contracts |
| Granting access on txHash | Verify `receipt.status === 'success'` first |
| Message lines overlapping | Use `\n\n` (double newlines), not `\n` |
| Missing event context | Validate `spaceId`/`channelId` before using |

## Resources

- **Developer Portal**: https://app.towns.com/developer
- **Documentation**: https://docs.towns.com/build/bots
- **SDK**: https://www.npmjs.com/package/@towns-protocol/bot
- **Chain ID**: 8453 (Base Mainnet)
