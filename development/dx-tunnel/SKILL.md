---
name: dx tunnel
description: use to open a tunnel to a remote host using the dx command
---

# Siteminder DX Tunnel

## Instructions
- user can ask in any format will hit this skill:
  - "open tunnel to <target_host>"
  - "tunnel to <target_host>"
  - "tunnel <target_host>"
  - "connect to <target_host>"
- asking user to provide the following details
  - allways asking user to provider the <target_port>, default value is 80.
  - allways asking user to provider the <local_port>, default value pick between 8000 to 8999, make sure the port is not in use in any other background process.
- required arguments: <target_host>, <target_port>, <local_port>
- while executing bash script, make sure make it as a background process, should not block claude code main process.
- dx command is available in the global node_modules folder, add it to the path before executing dx-tunnel.js.
- if user dosn't have dx installed in global, use `npx @siteminder/dx` to execute the command instead of `dx`.
- command for executing the script:
```bash
dx infrastructure tunnel --target_host <target_host> --target_port <target_port> --local_port <local_port>
```
- if error catched from stdout or stderr, then return the error message to the user.
- once user asking to stop the tunnel process, then stop the process and return the result to the user.

## Examples

#### Example for first time open tunnel and no nickname.
- user request: "open tunnel to demand-manager-api.platform-dev"
- meaning: 
  - <target_host> is demand-manager-api.platform-dev
  - <target_port> is not provided, default is 80
  - <local_port> is not provided, should be selected between 8000 to 8999, make sure the port is not in used in any other background process.
- command:
```bash
dx infrastructure tunnel --target_host demand-manager-api.platform-dev --target_port 80 --local_port 8080
```

#### Example for first time and second time open tunnel with nickname.
- user request: "open tunnel to demand-manager-api.platform-dev"
- meaning:
  - <target_host> is demand-manager-api.platform-dev, because nickname is pointing to this host.
  - <target_port> is not provided, default is 80
  - <local_port> is not provided, usinng this plugin default to select a port between 8000 to 8999, make sure the port is not in use.
- then command:
```bash
   dx infrastructure tunnel --target_host demand-manager-api.platform-dev --target_port 80 --local_port 8080
```

#### Example for user who dosn't have dx installed in global
- user request: "open tunnel to demand-manager-api.platform-dev"
- meaning:
  - <target_host> is demand-manager-api.platform-dev
  - <target_port> is not provided, default is 80
  - <local_port> is not provided, usinng this plugin default to select a port between 8000 to 8999, make sure the port is not in use.
- before executing,because user doesn't have `dx` installed in global, so this will fall back to use `npx @siteminder/dx` to execute the command instead of `dx`.
- then the command should be:
```bash
npx @siteminder/dx infrastructure tunnel --target_host demand-manager-api.platform-dev --target_port 80 --local_port 8080
```

#### Example for stop the tunnel process.
- user request: "stop demand-manager-api.platform-dev"
- then stop that background process and return the result to the user.