---
name: dx mysql pipe
description: when user asking mysql pipe to remote host, or pipe to a remote host, then use dx command to open a tunnel.
---

# Siteminder DX MySQL Pipe

## Instructions
- user can ask in any format will hit this skill:
  - "open db pipe to <remote_host>"
  - "mysql pipe to <remote_host>"
  - "pipe to <remote_host>"
  - "pipe to <nickname>"

- asking user to confirm the following details:
  - if no port is provided, provide a default port between 7000 to 7999, make sure the port is not in use in any other background process.
  - must asking user to choose a <local_port>.
  - remember which <local_port> is user choosed, next time when giving options, mention this port was chosen by user.
  - asking user to provide a <nickname> for the <remote_host> and remember it in cache and for future use.
  - if <remote_host> has a nickname already, then don't need ask user to provide <nickname>.
  - can provide a short nickname for user to choose in options.
  - once user provide a <nickname> to current <remote_host>, save it to cache and in future use.
- dx command is available in the global node_modules folder, add it to the path before executing dx-tunnel.js.
- if user dosn't have dx installed in global, use `npx @siteminder/dx` to execute the command instead of `dx`.
- with dx command installed in global:
```bash
dx infrastructure mysql-pipe -h <remote_host> -p <local_port>
```
- with npx @siteminder/dx installed in global:
```bash
npx @siteminder/dx infrastructure mysql-pipe -h <remote_host> -p <local_port>
```
- show the command will be executed to the user for approval.
- execute the command as a background process, should not block claude code main process.
- User can terminate the pipe process by asking to stop the process.


## Examples

user request without nickname:
- "open db pipe to platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com"
- "mysql pipe to platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com"
- "pipe to platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com"
- above examples all mean the same thing:
- <remote_host> is platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com
- <local_port> is not provided, then ask user to pick a port between 7000 to 7999, make sure the port is not in use in any other background process.

```bash
dx infrastructure mysql-pipe -h platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com -p 7111
```

user request with nickname:
- "open db pipe to platform-dev-ppay"
- "mysql pipe to platform-dev-ppay"
- "pipe to platform-dev-ppay"
- above examples all mean the same thing:
- <nickname> is platform-dev-ppay, and should use this nickname to get the real <remote_host> from cache.
  - example: platform-dev-ppay is pointing to platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com
- <local_port> is not provided, ask user to pick a port between 7000 to 7999, make sure the port is not in use in any other background process.

```bash
dx infrastructure mysql-pipe -h platform-dev-ppay-infrastructure.cluster-cfni24qvajia.us-west-2.rds.amazonaws.com -p 7111
```