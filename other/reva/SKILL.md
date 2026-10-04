---
name: reva
description: Complete Reva wallet management - passwordless authentication, PayID name claiming, multi-chain crypto transfers to PayIDs or wallet addresses, balance tracking across networks, account details information, and deposit management
homepage: https://revapay.ai
user-invocable: true
dependencies:
  - jq
  - curl
---

# Reva

**Passwordless authentication and wallet management for Reva users.**

Reva provides a simple way to authenticate users, claim unique PayID names, and manage cryptocurrency balances. All authentication is passwordless using email-based OTP verification.

## Authentication

Reva uses a passwordless authentication flow. Users receive a one-time password (OTP) via email, verify it, and receive an access token for subsequent operations.

### Login/Register Flow

There is no difference between registration and login - both use the same passwordless flow:

1. User provides their email address
2. System sends OTP to the email
3. User provides the OTP code
4. System verifies OTP and returns access token
5. Access token is stored securely for future operations

**The access token MUST be stored securely after verification and reused for all protected operations.**

## Available Commands

### 1. Login or Register

**Triggers:** When user wants to login, register, sign in, sign up, authenticate, or access Reva

**Process:**

1. Ask user for their email address if not provided
2. Call the authentication script to send OTP: `{baseDir}/scripts/send-otp.sh <email>`
3. Inform user that OTP has been sent to their email
4. Ask user to provide the OTP code they received
5. Call the verification script: `{baseDir}/scripts/verify-otp.sh <email> <otp>`
6. If successful, inform user they are now authenticated
7. The access token is automatically stored for future use

### 2. Claim PayID

**Triggers:** When user wants to claim a PayID, get a PayID name, register a PayID, or set their PayID

**Requirements:** User must be authenticated first (have valid access token)

**Process:**

1. Check if user is authenticated by calling: `{baseDir}/scripts/check-auth.sh`
2. If not authenticated, prompt user to login first
3. Ask user for their desired PayID name if not provided
4. Call the claim script: `{baseDir}/scripts/claim-payid.sh <desired_payid>`
5. Handle response:
   - Success: Inform user their PayID was claimed successfully
   - Already taken: Inform user the PayID is taken and ask for another choice
   - Invalid format: Explain format requirements and ask again
   - Unauthorized: Token expired, ask user to login again

### 3. View Balance

**Triggers:** When user wants to check balance, see wallet balance, view funds, or check how much money they have

**Requirements:** User must be authenticated first (have valid access token)

**Process:**

1. Check if user is authenticated by calling: `{baseDir}/scripts/check-auth.sh`
2. If not authenticated, prompt user to login first
3. Call the balance script: `{baseDir}/scripts/get-balance.sh`
4. Display the balance to user in a friendly format showing each token with its amount, symbol, and chain (network)
5. If unauthorized error, token expired - ask user to login again

**Display Format Example:**

```
Your current balance:
- 0.001016 ETH on Base
- 1.97 USDC on Base
- 1.21 USDT on BNB Smart Chain
- 0.80 USDC on BNB Smart Chain
- 0.00088 BNB on BNB Smart Chain
```

### 4. Get User Information

**Triggers:** When user asks about their account details, PayID, wallet address, email, referral code, cashback points, connected Twitter, avatar, or wants to deposit funds

**Requirements:** User must be authenticated first (have valid access token)

**Process:**

1. Check if user is authenticated by calling: `{baseDir}/scripts/check-auth.sh`
2. If not authenticated, prompt user to login first
3. Call the user info script: `{baseDir}/scripts/get-user-info.sh`
4. Extract and display the relevant information the user asked for:
   - **PayID**: Show from `payId` field
   - **Wallet Address**: Show from `walletAddress` field
   - **Email**: Show from `email` field
   - **Referral Code**: Show from `referralCode` field
   - **Cashback Points**: Show from `cashbackPoints` field
   - **Connected Twitter**: Show from `twitter` field
   - **Avatar**: Show from `avatarUrl` field
   - **Transaction Limit**: Show `transactionLimit` and `transactionUsed`
5. If user wants to deposit funds, provide their wallet address and instruct them to send funds to it

**Important for Deposits:** When user asks to deposit, simply provide their wallet address from the `/api/users/me` response and tell them to send funds to that address.

### 5. Send Funds

**Triggers:** When user wants to send money, send funds, send crypto, transfer tokens, or pay someone

**Requirements:** User must be authenticated first (have valid access token)

**Process:**

**CRITICAL: You must parse the user's message and extract all required information to construct a proper transfer payload. Continue asking follow-up questions until ALL required fields are provided.**

1. Check if user is authenticated by calling: `{baseDir}/scripts/check-auth.sh`
2. If not authenticated, prompt user to login first
3. Extract the following information from user's message:
   - **Token Symbol**: USDT, USDC, ETH, BNB, POL, or USD_STABLECOIN (these are the ONLY supported tokens)
   - **Chain Symbol**: ETH, POL, OP, BNB, or BASE (null for USD_STABLECOIN)
   - **Recipient**: PayID name, Twitter username (starts with @), or wallet address
   - **Amount**: Numeric value
4. If ANY field is missing, ask the user a follow-up question to get the missing information
5. Once ALL fields are collected, call: `{baseDir}/scripts/send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>`
6. Display the success message or error to the user

**Recipient Type Detection:**

- **Twitter Username**: If recipient starts with `@`, remove the @ and use as `recipientTwitterUsername`
  - Example: `@aminedd4` → `recipientTwitterUsername: "aminedd4"`
- **Wallet Address**: If recipient starts with `0x`, use as `recipientWalletAddress`
  - Example: `0x1234...` → `recipientWalletAddress: "0x1234..."`
- **PayID Name**: Otherwise, use as `recipientPayid`
  - Example: `aldo` → `recipientPayid: "aldo"`

**USD/Dollar Handling (IMPORTANT):**

When user mentions 'USD', 'dollar', 'dollars', or '$':

- Set `tokenSymbol` to `USD_STABLECOIN` (this is a special marker)
- Set `chainSymbol` to `null` - the system automatically selects the network with the highest USD stablecoin balance
- **DO NOT** ask for network when USD/dollar is mentioned - the system handles this automatically

**Supported Tokens (EXACT ENUMS):**

- `USDT` - Tether
- `USDC` - USD Coin
- `ETH` - Ethereum
- `BNB` - Binance Coin
- `POL` - Polygon
- `USD_STABLECOIN` - For USD/dollar requests (chainSymbol must be null)

**Supported Chains (EXACT ENUMS):**

- `ETH` - Ethereum
- `POL` - Polygon
- `OP` - Optimism
- `BNB` - BNB Chain
- `BASE` - Base
- `null` - Only when tokenSymbol is USD_STABLECOIN

**Parsing Examples:**

Example 1: "send 5 usdt on base to aldo"

```
tokenSymbol: USDT
chainSymbol: BASE
recipientPayid: aldo
recipientTwitterUsername: null
recipientWalletAddress: null
amount: 5
```

Example 2: "transfer 0.3 BNB on bnb to @aminedd4"

```
tokenSymbol: BNB
chainSymbol: BNB
recipientPayid: null
recipientTwitterUsername: aminedd4
recipientWalletAddress: null
amount: 0.3
```

Example 3: "send $10 to chris"

```
tokenSymbol: USD_STABLECOIN
chainSymbol: null
recipientPayid: chris
recipientTwitterUsername: null
recipientWalletAddress: null
amount: 10
```

Example 4: "send 1 eth on ethereum to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

```
tokenSymbol: ETH
chainSymbol: ETH
recipientPayid: null
recipientTwitterUsername: null
recipientWalletAddress: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
amount: 1
```

**Follow-up Question Examples:**

- User: "send some usdt to aldo"
  → Missing: amount, chain
  → Ask: "How much USDT would you like to send, and on which network? (ETH, POL, OP, BNB, or BASE)"

- User: "send 5 usdt to aldo"
  → Missing: chain
  → Ask: "Which network would you like to use? (ETH, POL, OP, BNB, or BASE)"

- User: "send 5 usdt on base"
  → Missing: recipient
  → Ask: "Who would you like to send it to? (PayID name, Twitter handle, or wallet address)"

- User: "send $20 to aldo"
  → Nothing missing (USD doesn't need chain)
  → Execute transfer immediately

**Important Notes:**

- Only supported tokens are: USDT, USDC, ETH, BNB, POL, USD_STABLECOIN
- Token symbols and chain symbols must match the EXACT enums (case-sensitive)
- USD_STABLECOIN is ONLY used for USD/dollar requests
- Continue asking questions until all required fields are provided
- Do NOT make assumptions - always ask the user for missing information

## Error Handling

### Token Expiration

If any protected operation returns an unauthorized error, the access token has expired. Inform the user and ask them to login again.

### Rate Limiting

If OTP request fails due to rate limiting, inform user to wait before trying again.

### Network Errors

If scripts fail due to network issues, inform user and suggest trying again.

### Invalid Input

Validate email format before sending requests. PayID format should be alphanumeric with optional underscores/hyphens.

## Security Notes

**User Authentication and Control:**

- **All operations require explicit user authentication** - users must complete passwordless OTP verification before any protected operations
- **Transfers are NEVER autonomous** - every transfer requires the user to explicitly provide: token, chain, recipient, and amount
- The skill cannot initiate transfers on its own; it only executes transfers when the user explicitly requests them with all required parameters
- Users maintain full control over their wallet operations at all times

**Token Storage:**

- Access tokens are stored locally in `~/.openclaw/payid/auth.json` with restricted file permissions (chmod 600)
- This is a standard OAuth/JWT token pattern - tokens are stored locally for session persistence
- Users can clear their token at any time by deleting the auth file or using the skill's logout functionality
- Tokens expire and require re-authentication when invalid

**Data Security:**

- Never log or display access tokens to the user
- OTP codes are only entered once and never stored
- All API requests use HTTPS encryption (enforced in scripts)
- All JSON payloads are constructed using `jq` to prevent injection attacks
- The skill communicates only with the official Reva API (https://api.revapay.ai)

**External API:**

- This skill integrates with Reva (https://revapay.ai), a legitimate cryptocurrency wallet service
- The API endpoint (https://api.revapay.ai) is the official production API for Reva
- All transfers are executed through user-authenticated API calls, not autonomous actions

## Script Reference

All scripts are located in `{baseDir}/scripts/`:

- `send-otp.sh <email>` - Send OTP to email
- `verify-otp.sh <email> <otp>` - Verify OTP and get access token
- `claim-payid.sh <payid>` - Claim a PayID name
- `get-balance.sh` - Get wallet balance with all tokens across chains
- `get-user-info.sh` - Get current logged user information
- `send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>` - Transfer funds to a recipient
- `check-auth.sh` - Check if user is authenticated

## Common Workflows

### First Time User

1. User asks to login or register
2. User provides email
3. System sends OTP
4. User provides OTP code
5. User is authenticated
6. User can now claim PayID or check balance

### Claim PayID

1. User asks to claim a PayID
2. Check authentication status
3. User provides desired payid name
4. System attempts to claim
5. Success or ask for alternative if taken

### Check Balance

1. User asks for balance
2. Check authentication status
3. Display current balance

### Get Account Info

1. User asks about their PayID, wallet address, referral code, etc.
2. Check authentication status
3. Fetch user info from `/api/users/me`
4. Display the requested information

### Deposit Funds

1. User asks how to deposit
2. Check authentication status
3. Get wallet address from user info
4. Provide wallet address for deposits

### Send Funds (Simple)

1. User: "send 0.01 usdt on bnb to aldo"
2. Forward message to Reva AI
3. Reva AI processes and sends funds
4. Display transaction confirmation with links

### Send Funds (Multi-Step)

1. User: "send some funds to aldo"
2. Forward to Reva AI
3. Reva AI: "which network?"
4. User: "bnb"
5. Forward to Reva AI (same room)
6. Reva AI: "which token?"
7. User: "0.01 usdt"
8. Forward to Reva AI (same room)
9. Transaction complete with confirmation

## API Endpoints

### Login (Send OTP)

- **Method**: POST
- **Path**: `/api/openclaw/login`
- **Body**: `{"email": "user@example.com"}`
- **Response**: `{"success": true, "message": "OTP sent to your email"}`

### Verify OTP

- **Method**: POST
- **Path**: `/api/openclaw/verify`
- **Body**: `{"email": "user@example.com", "otp": "123456"}`
- **Response**: `{"success": true, "token": "jwt_token", "user": {...}}`

### Get Balance

- **Method**: GET
- **Path**: `/api/wallet?isForceUpdateWallet=true`
- **Header**: `openclaw-token: <token>`
- **Response**: `{"success": true, "tokens": [{"name": "...", "symbol": "...", "balance": ..., "chain": "..."}]}`

### Claim PayID

- **Method**: POST
- **Path**: `/api/payid/register`
- **Header**: `openclaw-token: <token>`
- **Body**: `{"payIdName": "payid_name"}`
- **Response**: `{"success": true, "data": {...}}`

### Get User Info

- **Method**: GET
- **Path**: `/api/users/me`
- **Header**: `openclaw-token: <token>`
- **Response**: `{"user": {"id": "...", "email": "...", "payId": "...", "walletAddress": "...", "referralCode": "...", "cashbackPoints": ..., "twitter": "...", ...}}`

### Transfer Funds

- **Method**: POST
- **Path**: `/api/message/transfer-funds`
- **Header**: `openclaw-token: <token>`
- **Body**:

```json
{
  "tokenSymbol": "USDT" | "USDC" | "ETH" | "BNB" | "POL" | "USD_STABLECOIN",
  "chainSymbol": "ETH" | "POL" | "OP" | "BNB" | "BASE" | null,
  "recipientPayid": string | null,
  "recipientTwitterUsername": string | null,
  "recipientWalletAddress": string | null,
  "amount": number
}
```

- **Success Response (200)**: `{"success": true, "data": {"message": "...", "recipientPayId": "...", "usdAmountToSend": ...}, "meta": {"message": "Transaction completed successfully"}}`
- **Error Response (400/500)**: `{"success": false, "error": {"code": "...", "message": "...", "details": [...]}}`

## Tips

- Always check authentication before performing protected operations
- Display all token balances with their respective chains for clarity
- For deposits, simply provide the user's wallet address from `/api/users/me`
- **CRITICAL for sending funds**: Parse user's message to extract token, chain, recipient, and amount - ask follow-up questions for missing information
- USD/dollar requests use `USD_STABLECOIN` token with `null` chain - do NOT ask for network
- Only supported tokens are: USDT, USDC, ETH, BNB, POL, USD_STABLECOIN (case-sensitive)
- When user asks about account details (PayID, wallet, referral code, etc.), fetch from `/api/users/me`
- Provide clear error messages based on API responses
- Guide users through the authentication flow step-by-step
- Suggest alternative PayIDs if the desired one is taken
- Display transaction success messages from API responses
