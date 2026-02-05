---
name: serverless-aws
description: Patterns for AWS Lambda, DynamoDB, SQS, and Secrets Manager. Use when working on serverless AWS projects.
---

# Serverless AWS Skill

Patterns for AWS Lambda, DynamoDB, SQS, and Secrets Manager.

## When to Use

Apply when working on serverless AWS projects using Lambda functions.

## Lambda Handler Structure

```typescript
export async function handle(event: AWSLambda.APIGatewayProxyEvent) {
    try {
        return await handleInternal(event);
    } catch (error) {
        await trace.error(error, { headers: event.headers, body: event.body });
        return createErrorResponse(error);
    }
}

async function handleInternal(event: AWSLambda.APIGatewayProxyEvent) {
    const isAuthenticated = await authenticateRequest(event);
    if (!isAuthenticated) return unauthorizedResponse();

    const body = JSON.parse(event.body);
    assert(isValidInput(body), 'Invalid request body');
    return processRequest(body);
}
```

## Cold Start Optimization

Initialize clients outside handler:

```typescript
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

const dynamoClient = new DynamoDBClient({ region: 'us-east-1' });

let configCache: Config;

export async function handle(event: any) {
    if (!configCache) configCache = await loadConfig();
    return process(event, configCache);
}
```

## SQS Processing

```typescript
export async function handle(event: SQSEvent) {
    assert(event.Records.length === 1, 'Expected single record');
    
    const record = event.Records[0];
    const message = JSON.parse(record.body);
    const type = record.messageAttributes?.type?.stringValue;

    switch (type) {
        case 'ORDER_UPDATE': return handleOrderUpdate(message);
        case 'CUSTOMER_SYNC': return handleCustomerSync(message);
        default: console.warn('Unknown message type', type);
    }
}
```

## External API Calls

```typescript
export async function callExternalAPI(endpoint: string, data: any) {
    const config = await getServiceConfig();
    
    try {
        const response = await fetch(`${config.base_url}${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${config.api_key}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new StatusCodeError(response.status, await response.text());
        }
        
        return response.json();
    } catch (error) {
        await trace.error('External API call failed', { endpoint, error });
        throw error;
    }
}
```

## Deduplication

```typescript
const processedEvents = new Map<string, number>();

function isDuplicate(eventId: string): boolean {
    const now = Date.now();
    const fiveMinutesAgo = now - (5 * 60 * 1000);
    
    // Clean old entries
    for (const [id, timestamp] of processedEvents.entries()) {
        if (timestamp < fiveMinutesAgo) {
            processedEvents.delete(id);
        }
    }
    
    if (processedEvents.has(eventId)) return true;
    
    processedEvents.set(eventId, now);
    return false;
}
```
