---
name: ansible-validate
description: Validate Ansible playbook syntax and run ansible-lint
allowed-tools: Bash(source ~/.ansible-venv/bin/activate*), Bash(ansible*), Read, Grep, Glob
---

Validate Ansible syntax and lint for this project.

## Steps

1. Activate the project venv and run syntax check:
   ```bash
   source ~/.ansible-venv/bin/activate && ansible-playbook -vv -i tests/inventory tests/test.yml --syntax-check
   ```

2. Run ansible-lint on the target scope:
   - If `$ARGUMENTS` is empty, lint the full playbook:
     ```bash
     source ~/.ansible-venv/bin/activate && ansible-lint site.yml
     ```
   - If `$ARGUMENTS` specifies a role name (e.g., `vagrant`), lint that role:
     ```bash
     source ~/.ansible-venv/bin/activate && ansible-lint local-roles/<role_name>/
     ```
   - If `$ARGUMENTS` specifies a file path, lint that file:
     ```bash
     source ~/.ansible-venv/bin/activate && ansible-lint <file_path>
     ```

3. Report results clearly:
   - If both pass: confirm success
   - If either fails: show the errors and suggest fixes based on the project's `.ansible-lint` config (production profile, see skip_list for tolerated rules)

## Notes

- The venv is at `~/.ansible-venv`
- The lint config is in `.ansible-lint` (production profile)
- External roles in `roles/` are excluded from linting
- All working paths are relative to the project root
