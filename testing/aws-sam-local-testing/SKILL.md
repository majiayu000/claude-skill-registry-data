---
name: aws-sam-local-testing
description: "Wraps AWS SAM (Serverless Application Model) Local CLI for testing Lambda functions locally: `sam local invoke` (single invocation with event payload), `sam local start-api` (local API Gateway emulator), `sam local start-lambda` (local Lambda invoke endpoint for AWS SDK clients), and event-payload generation (`sam local generate-event`). For C#/.NET Lambdas, references/dotnet.md covers handler-direct testing with Amazon.Lambda.TestUtilities (TestLambdaContext, TestLambdaLogger) and the dotnet-lambda CLI. Use when testing Lambda + API Gateway + integrated AWS services locally."
---

# aws-sam-local-testing

## Overview

AWS SAM Local is the canonical local-testing toolchain for AWS
Lambda. Per
[docs.aws.amazon.com/serverless-application-model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-test.html),
it runs Lambdas in Docker containers locally with images that
mirror the Lambda runtime - same Linux, same Node/Python/Java
binaries, same handler-invocation contract.

## When to use

- Local unit + integration tests for Lambda handlers.
- Testing API Gateway + Lambda routing locally.
- Reproducing prod Lambda behaviour without deploying.
- Event-payload-driven tests (S3 event, SQS message, API GW
  request).

## Authoring

### Install

```bash
brew install aws-sam-cli
sam --version            # 1.x or higher
docker --version         # Required for sam local
```

### Project structure

A SAM project has `template.yaml` declaring Lambda functions:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.handler
      Runtime: python3.12
      Timeout: 10
      MemorySize: 512
      Events:
        Api:
          Type: Api
          Properties:
            Path: /hello
            Method: GET
```

### Generate an event payload

Per SAM docs:

```bash
sam local generate-event apigateway aws-proxy --path /hello --method GET > event.json
sam local generate-event s3 put --bucket mybucket --key file.txt > s3-event.json
sam local generate-event sqs receive-message > sqs-event.json
```

### Single invocation

```bash
sam local invoke HelloFunction --event event.json
```

Output: handler's return value, plus the simulated Lambda runtime
log lines.

### Local API Gateway

```bash
sam local start-api --port 3000
```

Now `curl http://localhost:3000/hello` exercises the full
API Gateway → Lambda routing.

### Local Lambda invoke endpoint

```bash
sam local start-lambda --port 3001
```

Then point AWS SDK clients at `http://localhost:3001`:

```python
import boto3
lambda_client = boto3.client('lambda', endpoint_url='http://localhost:3001', region_name='us-east-1')
lambda_client.invoke(FunctionName='HelloFunction', Payload=b'{}')
```

Useful for testing **Lambda → Lambda** invocations end-to-end.

### .NET Lambdas - handler-direct testing

For C#/.NET Lambda handlers, prefer in-process handler-direct invocation
with `Amazon.Lambda.TestUtilities` (`TestLambdaContext`,
`TestLambdaLogger`) over per-test `sam local invoke` spawns - setup,
worked tests, and the dotnet-lambda CLI are in
[references/dotnet.md](references/dotnet.md).

### Integration with pytest

```python
import subprocess, json

def invoke_lambda(name, event):
    proc = subprocess.run(
        ["sam", "local", "invoke", name, "--event", "-"],
        input=json.dumps(event), text=True, capture_output=True,
    )
    return json.loads(proc.stdout)

def test_hello():
    result = invoke_lambda("HelloFunction", {"name": "world"})
    assert result["statusCode"] == 200
    assert "Hello, world" in result["body"]
```

## Running

```bash
sam build                # Package Lambdas
sam local invoke HelloFunction --event event.json
```

For watch-mode:

```bash
sam build --use-container --watch
```

## CI integration

```yaml
jobs:
  sam-local-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: aws-actions/setup-sam@v2
      - run: sam build --use-container
      - run: pytest tests/lambda/
```

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Skip `sam build` between code changes | Stale package; old code runs | `sam build` (or watch mode) |
| `sam local invoke` for full-suite | Spawn cost per invocation; slow | `sam local start-lambda` once, invoke many |
| Compare local timing to prod | Docker overhead; cold-start model differs per `cold-start-budget-reference` | Test correctness locally; latency in prod |
| No event-payload generation | Hand-rolled events miss fields | `sam local generate-event` |
| Mock AWS SDK calls locally | Tests pass but prod IAM / endpoints fail | Use LocalStack or test against real low-cost AWS account |
| Skip API Gateway routing test | Lambda alone passes; API GW integration breaks | `sam local start-api` |
| Hardcoded path in test | OS-specific | Use generated events |

## Limitations

- **Docker overhead.** Cold starts in SAM Local are 5-15s
  (Docker container spin-up); not representative of prod
  cold-start budgets per `cold-start-budget-reference`.
- **Doesn't test IAM.** Local invocations run with your AWS
  CLI credentials, not the Lambda's role.
- **Doesn't test event-source mapping.** SQS / DynamoDB Streams /
  EventBridge bindings are SAM-template-only locally.
- **VPC + private endpoints can't be simulated.** Local Lambdas
  reach internet directly.
- **Pair with LocalStack** for fuller AWS-service emulation
  ([localstack.cloud](https://localstack.cloud/)).

## References

- AWS SAM docs:
  [docs.aws.amazon.com/serverless-application-model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/).
- SAM Local testing:
  [docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-test.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-test.html).
- `sam local generate-event`:
  [docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-generate-event.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-generate-event.html).
- .NET handler-direct testing:
  [references/dotnet.md](references/dotnet.md).
- Companion catalog:
  `cold-start-budget-reference` (cold-start + timeout budgets).
- Sibling tools:
  `cloudflare-workers-miniflare`,
  `azure-functions-tests`.
- Builder:
  `serverless-integration-test-builder`.
