---
name: hippius-user
description: This skill should be used when the user asks to upload files to Hippius, has questions about Hippius decentralized storage (Bittensor Subnet 75), needs to query storage status, or wants to set up the Hippius CLI for IPFS or S3-compatible storage operations.
---

# Hippius User

## Overview

Hippius is a decentralized cloud storage platform on Bittensor (Subnet 75) offering IPFS-based permanent storage and S3-compatible object storage. This skill helps users interact with Hippius for uploading files, querying storage metrics, and managing their decentralized storage account.

## When to Use This Skill

Use this skill when the user:
- Asks to upload files to Hippius or IPFS via Hippius
- Has questions about Hippius features, pricing, or capabilities
- Needs to query their storage status (files, buckets, usage, credits)
- Wants to set up the Hippius CLI
- Needs help with Hippius authentication or environment configuration
- Asks about IPFS vs S3 storage options
- Needs to check account balance or storage credits

## Quick Start Decision Tree

```
User request about Hippius?
│
├─ "Set up Hippius CLI" or "Install Hippius"
│  └─→ Go to: CLI Installation Workflow
│
├─ "Upload file to Hippius" or "Pin to IPFS"
│  └─→ Go to: File Upload Workflow
│
├─ "Check my files" or "What's in my storage?"
│  └─→ Go to: Query Storage Workflow
│
├─ "How does Hippius work?" or "IPFS vs S3?"
│  └─→ Reference: references/storage_guide.md
│
├─ "Set up authentication" or "Configure credentials"
│  └─→ Reference: references/authentication.md
│
└─ "What API methods are available?"
   └─→ Reference: references/api_reference.md
```

## Core Workflows

### 1. CLI Installation Workflow

When the user needs to install or set up the Hippius CLI:

**Prerequisites Check:**
1. Verify Rust is installed (`rustc --version`)
2. Verify Docker is installed (`docker --version`)
3. If missing, reference `references/cli_commands.md` for installation links

**Installation:**
```bash
scripts/install_cli.sh
```

This automated script:
- Checks all prerequisites
- Clones the Hippius CLI repository
- Builds and installs the `hipc` binary
- Optionally copies to `/usr/local/bin`
- Guides environment configuration

**Post-Installation:**
1. Help user create `.env` file from template
2. Copy `assets/.env.template` to user's working directory
3. Guide user to fill in:
   - `SUBSTRATE_NODE_URL` (default: `ws://127.0.0.1:9944` or public node)
   - `SUBSTRATE_SEED_PHRASE` (their 12 or 24-word mnemonic)
4. Secure the file: `chmod 600 .env`
5. Test installation: `hipc wallet list`

**Reference:** See `references/cli_commands.md` for detailed command documentation.

### 2. File Upload Workflow

When the user wants to upload files to Hippius:

**Step 1: Determine Storage Type**

Ask the user (or infer from context):
- **IPFS**: For public, permanent, content-addressed storage
- **S3**: For private, mutable object storage

Reference `references/storage_guide.md` for detailed comparison if user is uncertain.

**Step 2: Upload to IPFS**

For IPFS uploads (recommended for permanent public content):

```bash
# Upload and pin (recommended)
scripts/upload_to_ipfs.sh /path/to/file.pdf --pin

# Upload without pinning (not recommended for permanent storage)
scripts/upload_to_ipfs.sh /path/to/file.pdf
```

The script:
- Validates file exists
- Checks environment configuration
- Uploads to IPFS via CLI
- Extracts and displays IPFS CID
- Provides gateway URLs for access
- Logs upload to `.hippius_uploads.log`

**Return to user:**
- IPFS CID (Content Identifier)
- Gateway URLs: `https://ipfs.io/ipfs/{CID}` and `https://gateway.pinata.cloud/ipfs/{CID}`
- Reminder to save the CID as permanent reference

**Step 3: Upload to S3 (Alternative)**

For S3-compatible storage:

1. Ensure user has S3 credentials (from `https://console.hippius.com → Settings → API Keys`)
2. Configure AWS SDK or CLI with Hippius endpoint
3. Use standard S3 operations

Example (Python):
```python
import boto3

s3_client = boto3.client(
    's3',
    endpoint_url='https://s3.hippius.com',
    aws_access_key_id='HIPPIUS_ACCESS_KEY_XXXXX',
    aws_secret_access_key='HIPPIUS_SECRET_XXXXXXXXXXXXX'
)

s3_client.upload_file('local_file.txt', 'my-bucket', 'remote_file.txt')
```

**Reference:** See `references/storage_guide.md` for comprehensive S3 usage examples.

### 3. Query Storage Workflow

When the user wants to check their storage status:

**Determine Query Type:**

Ask what they want to check (or query all):
- All information (default)
- Just files
- Just storage size
- Just buckets
- Just credit balance

**Execute Query:**

```bash
# Query all information
scripts/query_storage.py 5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY

# Query specific information
scripts/query_storage.py <account_address> --files
scripts/query_storage.py <account_address> --storage
scripts/query_storage.py <account_address> --buckets
scripts/query_storage.py <account_address> --credits
```

The script queries the Hippius RPC API and displays:
- **Files**: File hashes, names, sizes, pinning miners
- **Storage**: Total storage used in human-readable format
- **Buckets**: Bucket names and sizes
- **Credits**: Free credit balance

**Account Address:**
- User's SS58-formatted Hippius address
- Can be derived from their mnemonic via CLI
- Format: `5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY`

**Reference:** See `references/api_reference.md` for all available RPC methods.

### 4. Authentication Setup Workflow

When the user needs help with authentication or credentials:

**For CLI Authentication:**

1. User needs a mnemonic seed phrase (12 or 24 words)
2. If they don't have one:
   - Generate via console: `https://console.hippius.com → Create Account`
   - Generate via CLI: `hipc wallet create`
   - **Critical**: Mnemonic is shown only once - must write it down immediately
3. Configure environment:
   - Copy `assets/.env.template` to `.env`
   - Fill in `SUBSTRATE_SEED_PHRASE`
   - Fill in `SUBSTRATE_NODE_URL`
   - Secure: `chmod 600 .env`
4. Load environment: `source .env`

**For S3 Authentication:**

1. Log in to Hippius console: `https://console.hippius.com`
2. Navigate to Settings → API Keys
3. Generate new key pair
4. Save Access Key ID and Secret Access Key
5. Configure AWS SDK/CLI with these credentials

**Security Warnings:**

⚠️ **Always emphasize:**
- There is NO password recovery in Hippius
- Lost mnemonic = permanent account loss
- Never share mnemonic with anyone
- Store multiple backups in secure physical locations
- Never commit `.env` to version control

**Reference:** See `references/authentication.md` for comprehensive security best practices.

## Common User Requests and Responses

### "Upload this file to Hippius"

**Response:**
1. Check if CLI is installed (`which hipc`)
2. If not installed, run installation workflow
3. Verify environment is configured
4. Ask if file should be pinned (recommend yes for permanent storage)
5. Execute: `scripts/upload_to_ipfs.sh <file_path> --pin`
6. Provide CID and access URLs

### "What files do I have stored?"

**Response:**
1. Ask for their account address (or help them find it)
2. Execute: `scripts/query_storage.py <account_address> --files`
3. Display results with file names, sizes, and CIDs
4. Offer to query other information (storage size, credits)

### "How much storage am I using?"

**Response:**
1. Ask for their account address
2. Execute: `scripts/query_storage.py <account_address> --storage`
3. Display total storage in human-readable format
4. Optionally show credit balance and cost estimation

### "Set up Hippius for me"

**Response:**
1. Run full installation workflow
2. Execute: `scripts/install_cli.sh`
3. Help create `.env` file from template
4. Guide mnemonic setup (generate or import)
5. Test installation with `hipc wallet list`
6. Offer to do test upload

### "What's the difference between IPFS and S3?"

**Response:**
1. Reference `references/storage_guide.md`
2. Summarize key differences:
   - IPFS: Public, permanent, content-addressed, decentralized
   - S3: Private, mutable, key-based, hybrid architecture
3. Help user choose based on their use case
4. Provide code examples if needed

### "How do I check my credit balance?"

**Response:**
1. Option 1 (via script): `scripts/query_storage.py <account_address> --credits`
2. Option 2 (via CLI): `hipc credits check`
3. Option 3 (via console): `https://console.hippius.com`
4. Display balance and warn if low

## Direct CLI Usage

For users who prefer direct CLI commands instead of scripts:

### File Operations
```bash
# Pin file to IPFS
hipc storage pin /path/to/file.txt

# Upload to IPFS
hipc storage upload /path/to/file.txt

# Unpin file
hipc storage unpin QmYourIPFSHashHere
```

### Account Operations
```bash
# Check credits
hipc credits check

# List wallets
hipc wallet list

# Create new wallet
hipc wallet create
```

**Reference:** See `references/cli_commands.md` for complete command list.

## API Integration

For users who want to integrate Hippius into their applications:

### Python Example (RPC API)
```python
import requests

def get_user_files(account_id):
    response = requests.post(
        'http://api.hippius.io',
        json={
            "jsonrpc": "2.0",
            "method": "get_user_files",
            "params": [account_id],
            "id": 1
        }
    )
    return response.json()['result']

# Usage
files = get_user_files('5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY')
for file in files:
    print(f"{file['name']}: {file['hash']}")
```

### JavaScript Example (S3)
```javascript
const AWS = require('aws-sdk');

const s3 = new AWS.S3({
    endpoint: 'https://s3.hippius.com',
    accessKeyId: 'HIPPIUS_ACCESS_KEY_XXXXX',
    secretAccessKey: 'HIPPIUS_SECRET_XXXXXXXXXXXXX',
    s3ForcePathStyle: true
});

// Upload file
s3.upload({
    Bucket: 'my-bucket',
    Key: 'file.txt',
    Body: fileContent
}, (err, data) => {
    console.log('Upload complete:', data.Location);
});
```

**Reference:** See `references/api_reference.md` for all available RPC methods and `references/storage_guide.md` for S3 SDK examples.

## Troubleshooting

### Installation Issues

**Problem:** Rust not installed
- Direct user to: `https://rust-lang.org/tools/install`
- Command: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

**Problem:** Docker not running
- Check: `docker ps`
- Start Docker desktop application
- Note: Docker is required for some storage operations but not all

**Problem:** Build fails
- Check Rust version: `rustc --version`
- Update Rust: `rustup update`
- Check disk space
- Try clean build: `cargo clean && cargo install --path .`

### Upload Issues

**Problem:** Authentication failed
- Verify `SUBSTRATE_SEED_PHRASE` is set correctly
- Check mnemonic has exactly 12 or 24 words
- Ensure no extra spaces or special characters
- Load environment: `source .env`

**Problem:** File not accessible after upload
- Wait for pinning propagation (can take minutes)
- Verify CID is correct
- Try different IPFS gateway
- Check if enough miners have pinned (query via API)

**Problem:** Low credits
- Check balance: `scripts/query_storage.py <account> --credits`
- Add credits via console: `https://console.hippius.com`
- Consider referral program for earning credits

### Query Issues

**Problem:** API connection error
- Verify internet connection
- Check API status: `https://api.hippius.io`
- Try alternative endpoint if specified
- Check for network firewalls

**Problem:** Account address invalid
- Verify SS58 format
- Check for typos in address
- Derive address from mnemonic if unsure
- Use console to view address: `https://console.hippius.com`

## Resources

This skill includes comprehensive reference materials and automation scripts:

### scripts/

**install_cli.sh** - Automated Hippius CLI installation
- Checks prerequisites (Rust, Docker)
- Clones and builds the CLI
- Guides environment setup
- Validates installation

**upload_to_ipfs.sh** - Convenient file upload wrapper
- Validates file exists
- Handles pinning operations
- Extracts and displays CID
- Logs uploads to file
- Provides gateway URLs

**query_storage.py** - Storage metrics query tool
- Queries files, buckets, storage, credits
- Human-readable output formatting
- Flexible filtering options
- Direct RPC API integration

### references/

**api_reference.md** - Complete RPC API documentation
- 26+ RPC method descriptions
- Request/response formats
- Parameter specifications
- Usage examples

**cli_commands.md** - Full CLI command reference
- Installation instructions
- All available commands
- Usage examples
- Troubleshooting guide

**storage_guide.md** - Comprehensive storage documentation
- IPFS vs S3 comparison
- Best practices for each storage type
- Code examples (Python, AWS CLI, JavaScript)
- Pricing and cost management
- Troubleshooting common issues

**authentication.md** - Security and authentication guide
- Mnemonic generation and management
- Environment configuration
- S3 credentials setup
- Security best practices
- Account recovery information
- Critical security warnings

### assets/

**.env.template** - Environment configuration template
- Pre-configured with all required variables
- Security warnings and best practices
- Instructions for setup
- Optional S3 configuration
- Ready to copy and customize

## External Resources

- **Hippius Documentation**: [docs.hippius.com](https://docs.hippius.com)
- **Hippius Console**: [console.hippius.com](https://console.hippius.com)
- **Hippius API**: [api.hippius.io](http://api.hippius.io)
- **Hippius Community**: [community.hippius.com](https://community.hippius.com)
- **Hippius Stats**: [hipstats.com](https://hipstats.com)
- **Hippius CLI GitHub**: [github.com/thenervelab/hippius-cli](https://github.com/thenervelab/hippius-cli)
- **Hippius Docs GitHub**: [github.com/thenervelab/hippius-doc](https://github.com/thenervelab/hippius-doc)

## Important Notes

1. **Security First**: Always emphasize mnemonic security and backup practices
2. **No Recovery**: Repeatedly warn that lost mnemonics cannot be recovered
3. **Pinning for Permanence**: Recommend pinning for any content that should persist
4. **Cost Transparency**: Hippius uses pay-per-use model tracked on blockchain
5. **Public by Default**: IPFS content is public - use S3 for private files
6. **Gateway Propagation**: IPFS files may take time to propagate across gateways
7. **Environment Security**: Always secure `.env` files and add to `.gitignore`
8. **Credit Monitoring**: Help users check credits regularly to avoid service interruption
