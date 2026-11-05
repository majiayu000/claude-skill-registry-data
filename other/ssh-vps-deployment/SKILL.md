---
name: ssh-vps-deployment
description: Deep knowledge about deploying applications to Baremetal servers or Virtual Private Servers (VPS) using SSH, SCP, Rsync, and PM2/Systemd.
type: transform
tier: library
domain: deploy
trigger: "when deploying to a VPS via SSH"
---

## Context
Deploying {{project_name}} ({{project_type}}) to a VPS via SSH.
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Ensure the SSH key is correctly configured (`~/.ssh/id_rsa` or another identity file).
2. For automated agents, ensure the SSH key string is written to a file, its permissions are restricted (`chmod 600`), and it is used correctly with the `ssh -i` command.
3. Test connectivity by running `ssh -i <path-to-key> -o StrictHostKeyChecking=no <user>@<host> "echo Authentication successful"`. If this fails, abort the deployment.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. If this is a Node.js or static frontend application, run `npm run build` or `yarn build` locally to generate the `dist/` or `build/` directory.
3. If this is a compiled language (Go, Rust), run the appropriate build command (e.g., `go build -o app main.go`) ensuring the target architecture matches the VPS (e.g., `GOOS=linux GOARCH=amd64`).

### Phase 3: Install / Provisioning
1. Ensure the target directory structure exists on the VPS. For example: `ssh -i <key> <user>@<host> "mkdir -p /var/www/{{project_name}}"`.
2. Ensure necessary dependencies (e.g., Node.js, Python, PM2, Nginx) are installed on the server. Do not automatically install these unless explicitly required by the project configuration.
3. Stop the existing application process (e.g., `pm2 stop {{project_name}}` or `sudo systemctl stop {{project_name}}`) to prevent file lock issues during deployment.

### Phase 4: Deploy
1. Ship the artifact to the VPS.
2. Use `rsync` (preferred for speed and reliability) or `scp` to copy the necessary files to the VPS. Example: `rsync -avz -e "ssh -i <key> -o StrictHostKeyChecking=no" dist/ package.json <user>@<host>:/var/www/{{project_name}}/`.
3. SSH into the VPS and install production dependencies if necessary: `ssh -i <key> <user>@<host> "cd /var/www/{{project_name}} && npm ci --production"`.
4. Start the application process. E.g., `pm2 start {{project_name}}` or `sudo systemctl start {{project_name}}`.

### Phase 5: Checking
1. Verify the deployment was successful.
2. SSH into the VPS and check the application status: `ssh -i <key> <user>@<host> "pm2 status {{project_name}}"`.
3. Check the application logs for any startup errors: `ssh -i <key> <user>@<host> "pm2 logs {{project_name}} --lines 50 --nostream"`.
4. Curl the application's public URL or local port to check for an HTTP 200 OK status. E.g., `curl -sSf http://<host>` or `ssh -i <key> <user>@<host> "curl -sSf http://localhost:<port>"`.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. If using a rollback script, execute it. Otherwise, manually copy the backup files (if created during Phase 3/4) back into the deployment directory.
3. Restart the application process using the old codebase (`pm2 restart {{project_name}}`).
4. Note the failure in the progress log.

## Validation
- [ ] SSH authentication succeeds.
- [ ] Local build succeeds.
- [ ] Files are transferred successfully.
- [ ] Remote installation/start succeeds.
- [ ] Health check (curl) returns 200 OK.
