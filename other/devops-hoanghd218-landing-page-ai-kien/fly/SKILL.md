---
name: fly
description: Deploy and manage the photography portfolio backend on fly.io. Use when deploying the app, checking logs, checking status, scaling machines, or managing the fly.io deployment.
allowed-tools: Bash
---

# Fly.io Management

This skill helps manage the photography portfolio backend deployment on fly.io.

## App Information

- **App name**: `photography-portfolio-solitary-fire-836`
- **Region**: sjc (San Jose, California)
- **Backend directory**: `backend/`

## Common Commands

### Deploy

Deploy the backend to fly.io:

```bash
cd backend && fly deploy
```

For a faster deployment without building (if image is already pushed):
```bash
cd backend && fly deploy --no-cache
```

### View Logs

Get real-time logs from the deployed app:

```bash
fly logs -a photography-portfolio-solitary-fire-836
```

Tail logs continuously:
```bash
fly logs -a photography-portfolio-solitary-fire-836 -f
```

### Check Status

Check app status and running machines:

```bash
fly status -a photography-portfolio-solitary-fire-836
```

List all machines:
```bash
fly machines list -a photography-portfolio-solitary-fire-836
```

### SSH into Machine

Open SSH session to the running machine:

```bash
fly ssh console -a photography-portfolio-solitary-fire-836
```

Execute a single command:
```bash
fly ssh console -a photography-portfolio-solitary-fire-836 -C "command here"
```

### Scaling

Scale memory:
```bash
fly scale memory 512 -a photography-portfolio-solitary-fire-836
```

Scale VM count:
```bash
fly scale count 1 -a photography-portfolio-solitary-fire-836
```

### Secrets Management

List secrets:
```bash
fly secrets list -a photography-portfolio-solitary-fire-836
```

Set a secret:
```bash
fly secrets set SECRET_NAME=value -a photography-portfolio-solitary-fire-836
```

### Troubleshooting

Check recent events:
```bash
fly logs -a photography-portfolio-solitary-fire-836 --tail 100
```

Restart the app:
```bash
fly apps restart photography-portfolio-solitary-fire-836
```

Get machine details:
```bash
fly machine status <machine-id> -a photography-portfolio-solitary-fire-836
```

## Deployment Checklist

When deploying:

1. Ensure you're in the `backend/` directory
2. Check that all secrets are set (if needed)
3. Run `fly deploy`
4. Monitor logs with `fly logs -f` to verify successful startup
5. Check status with `fly status` to confirm machines are running

## Notes

- The app uses auto-stop/auto-start machines (min_machines_running = 0)
- Backend runs on port 5001
- Uses CDN mode (USE_CDN = 'true')
- Photos directory is `/app/photos`
