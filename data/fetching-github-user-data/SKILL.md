---
name: fetching-github-user-data
description: Fetch comprehensive GitHub user data including profile, repositories, contributions, pull requests, issues, and statistics. Use when the user asks to fetch, download, or analyze GitHub user data.
---

# Fetching GitHub User Data

Fetch comprehensive data about any GitHub user through the GitHub API, including profile information, repositories, contributions, social connections, and detailed statistics.

## Quick start

### Basic usage (without token)

Fetch public data for any GitHub user:

```bash
python scripts/fetch.py \
  --username "torvalds" \
  --output "./github_data"
```

### With Personal Access Token (recommended)

Use a GitHub Personal Access Token to access more data and higher rate limits:

```bash
python scripts/fetch.py \
  --username "torvalds" \
  --token "ghp_YOUR_TOKEN_HERE" \
  --output "./github_data"
```

Or use environment variable:

```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"
python scripts/fetch.py --username "torvalds"
```

## What data is fetched

### Basic data
- ✅ User profile (name, bio, location, email, etc.)
- ✅ All public repositories with details
- ✅ Gists
- ✅ Starred repositories

### Social data
- ✅ Followers
- ✅ Following
- ✅ Organizations
- ✅ Subscribed repositories

### Activity data
- ✅ Public events (last 30 days)
- ✅ Pull requests created
- ✅ Issues created

### Statistics (computed)
- ✅ Programming language distribution
- ✅ Repository statistics (total stars, forks)
- ✅ Contribution calendar (requires token)

## Output structure

Data is organized in a clean directory structure:

```
github_data/
└── {username}/
    ├── profile.json                    # User basic info
    ├── repositories/
    │   ├── list.json                   # Repository summary
    │   └── details/{repo}.json         # Each repository details
    ├── gists/
    │   ├── list.json
    │   └── details/{gist_id}.json
    ├── starred/repositories.json
    ├── social/
    │   ├── followers.json
    │   └── following.json
    ├── organizations.json
    ├── events/public_events.json
    ├── subscriptions.json
    ├── contributions/calendar.json     # Requires token
    ├── pull_requests/created.json
    ├── issues/created.json
    ├── statistics/
    │   ├── languages.json              # Language distribution
    │   └── repositories.json           # Repo stats
    └── metadata.json                   # Fetch metadata
```

## Configuration

### Getting a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `read:user`, `repo` (for private repos if needed)
4. Copy the token and use it with `--token` or set as `GITHUB_TOKEN` environment variable

### Why use a token?

- **Higher rate limits**: 5,000 requests/hour vs 60 without token
- **Contribution calendar**: Only available with authentication
- **More complete data**: Access to some endpoints requires authentication

## Advanced usage

### Specify custom output directory

```bash
python scripts/fetch.py \
  --username "octocat" \
  --output "./my_custom_folder"
```

### Using GitHub CLI token

If you have GitHub CLI (`gh`) installed and authenticated:

```bash
# The script will automatically detect gh CLI authentication
python scripts/fetch.py --username "username"
```

## Use cases

### Evaluating engineer capabilities

The fetched data provides comprehensive insights for evaluating:
- **Technical breadth**: Programming language distribution
- **Project experience**: Repository count and quality
- **Open source contribution**: PRs, issues, starred repos
- **Community influence**: Followers, stars, forks
- **Coding activity**: Contribution calendar (with token)
- **Collaboration**: PRs and issues created

### Research and analysis

- Analyze GitHub user behavior patterns
- Study programming language trends
- Track developer activity over time
- Build developer profiles for recruitment

### Personal archival

- Backup your GitHub profile data
- Track your own progress over time
- Generate portfolio data

## Examples

### Example 1: Fetch data for Linux creator

```bash
python scripts/fetch.py \
  --username "torvalds" \
  --output "./linux_creator_data"
```

### Example 2: Analyze your own data with token

```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN"
python scripts/fetch.py \
  --username "yourusername" \
  --output "./my_github_data"
```

### Example 3: Batch fetch multiple users

```bash
for user in "torvalds" "gvanrossum" "dhh"; do
  python scripts/fetch.py --username "$user" --output "./github_users"
done
```

## Error handling

The script handles common errors gracefully:
- **Rate limit exceeded**: Shows clear error message
- **User not found**: Reports invalid username
- **Network errors**: Retries with exponential backoff
- **Missing token**: Continues with public data only
- **API errors**: Logs errors but continues fetching other data

## Statistics summary

After fetching, the script displays:
- Total API requests made
- Data items fetched for each category
- Total stars and forks
- Programming languages detected
- Any errors encountered

## Performance

- Typical fetch time: 30-120 seconds (depending on user data volume)
- API requests: 15-50 requests (varies by user)
- Storage: 1-50 MB per user (depending on repo count)

## Limitations

- Public events limited to last 300 events (30 days)
- Contribution calendar requires Personal Access Token
- Repository statistics limited for repos with 10,000+ commits
- Search results limited to 100 items per query

## Troubleshooting

### "Rate limit exceeded"
Solution: Use a Personal Access Token for higher limits

### "GraphQL request failed"
Solution: Ensure you have a valid Personal Access Token for contribution calendar

### "No data fetched"
Solution: Check username spelling and network connection

## See also

- [AUTHENTICATION.md](AUTHENTICATION.md) - Detailed authentication guide
- [EXAMPLES.md](EXAMPLES.md) - More usage examples
- [DATA_ANALYSIS.md](DATA_ANALYSIS.md) - How to analyze fetched data
