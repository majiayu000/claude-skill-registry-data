---
name: pypi-simple_gh_aws_creds
description: "Use the simple_gh_aws_creds Python library (v0.2.0): give a GitHub repository its own AWS IAM user and store the user's access key as GitHub Actions secrets, then update its permissions, rotate the key, or tear it all down. Covers SetupGitHubRepo (setup_all, s12_put_iam_policy, s31_rotate_access_key, teardown_all), the simple-gh-aws-creds CLI (setup, update_policy, rotate_key, teardown), and an end-to-end check of the credentials."
---

# simple_gh_aws_creds

Written for version 0.2.0. Install: `pip install simple-gh-aws-creds`, or run the CLI with `uvx simple-gh-aws-creds`.

## Purpose

Creates one IAM user per GitHub repository, with one inline policy (plus optional existing managed policies), one access key saved to a local JSON file, and three GitHub Actions secrets (region, key ID, secret key). Every step is idempotent and makes AWS and GitHub match the config. The key is long-lived: suited to open source CI and test accounts; prefer OIDC for production.

## Import

```python
from simple_gh_aws_creds.api import SetupGitHubRepo
import simple_gh_aws_creds.api as simple_gh_aws_creds     # then simple_gh_aws_creds.SetupGitHubRepo
```

## Public API

`SetupGitHubRepo` (dataclass). Fields:

- `boto_ses: boto3.Session`: can manage IAM users in the target account
- `aws_region: str`: written to the region secret; part of the inline policy name
- `iam_user_name: str`
- `tags: dict[str, str]`
- `policy_document: dict`: the user's inline IAM policy
- `attached_policy_arn_list: list[str]`: existing managed policies to attach
- `path_access_key_json: Path`: local key file, the only copy of the secret; keep it out of git
- `github_user_name: str`, `github_repo_name: str`
- `github_token: str`: can write the repo's Actions secrets
- `github_secret_name_aws_default_region: str = "AWS_DEFAULT_REGION"`
- `github_secret_name_aws_access_key_id: str = "AWS_ACCESS_KEY_ID"`
- `github_secret_name_aws_secret_access_key: str = "AWS_SECRET_ACCESS_KEY"`

Workflows:

- `setup_all() -> None`: create user, policies, key, and secrets (s11 to s14); safe to re-run
- `s12_put_iam_policy() -> None`: make the user's policies exactly match the config (hot update)
- `s31_rotate_access_key() -> None`: replace the key, save it locally, update the secrets
- `teardown_all() -> None`: delete secrets, keys, policies, and the user (s21 to s24)

Steps and helpers:

- `s11_create_iam_user() -> None`, `s13_create_or_get_access_key(verbose: bool = True) -> tuple[str, str]`, `s14_setup_github_secrets() -> None`
- `s21_delete_github_secrets() -> None`, `s22_delete_access_key() -> None`, `s23_delete_iam_policy() -> None`, `s24_delete_iam_user() -> None`
- `print_github_workflow_example() -> None`: print a workflow snippet that uses the secrets
- Properties: `policy_document_name: str`, `iam_user_console_url: str`, `github_secrets_url: str`, `iam_client`

```python
setup = SetupGitHubRepo(
    boto_ses=boto3.Session(profile_name="my-aws-profile"),
    aws_region="us-east-1",
    iam_user_name="pypi-my_package",
    tags={},
    policy_document={"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": "*"}]},
    attached_policy_arn_list=[],
    path_access_key_json=Path("my_access_key.json"),
    github_user_name="my-user",
    github_repo_name="my-repo",
    github_token=os.environ["GITHUB_TOKEN"],
)
setup.setup_all()
```

Errors: `s13` raises `RuntimeError` when the user has a key whose secret is not in the local file (fix: `s31_rotate_access_key()`); `s31` raises `RuntimeError` when the user does not exist; GitHub failures are raised as PyGithub reports them.

## CLI

`simple-gh-aws-creds` (or `.venv/bin/simple-gh-aws-creds`, or `uvx simple-gh-aws-creds`) runs the same workflows from a JSON config file holding the same values as the fields above, minus `boto_ses` and `github_token`. AWS credentials come from `--aws_profile` or the boto3 credential chain; the GitHub token from an environment variable named by `--github_token_env_name` (default `GITHUB_TOKEN`), never from an argument. `simple-gh-aws-creds --help` lists the commands. Commands return nothing, so no secret is printed.

## Verify a setup end to end

After setup or a key rotation, check the key locally from the key file (caller identity, an allowed and a denied call), then run a GitHub Actions workflow that maps the three secrets to `AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and runs `aws sts get-caller-identity`. Never print the key file. Recipe: `ref/cli.md`, "Verify end to end".

## More detail

For full API docs see `ref/public-api.md`. For full CLI args and the end-to-end check see `ref/cli.md`.
