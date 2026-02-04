---
name: zai-mcp-manager
description: Comprehensive management capabilities for Z.AI MCP servers, including quota tracking, health monitoring, configuration validation, and usage analytics for the Z.AI Lite Plan. Manages web-search-prime and web-reader MCP servers with intelligent monitoring and optimization.
---

# Z.AI MCP Manager Skill

This skill provides comprehensive management capabilities for Z.AI MCP servers, including quota tracking, health monitoring, configuration validation, and usage analytics for the Z.AI Lite Plan.

## Purpose

Manage Z.AI MCP servers (web-search-prime and web-reader) with intelligent monitoring, quota optimization, and best practice guidance. This skill ensures optimal usage of the FREE quotas (100 searches + 100 readers) while providing advanced analytics and error recovery.

## When to Use

Use this skill when you need to:

- Monitor Z.AI MCP server health and performance
- Track quota usage and prevent exhaustion
- Validate MCP configurations and API key accessibility
- Generate usage reports and analytics
- Troubleshoot MCP connectivity issues
- Optimize Z.AI MCP usage patterns
- Implement intelligent fallback strategies
- Set up monitoring and alerting for quota limits

## Configuration Validation

Check if your Z.AI MCP configuration is properly set up:

1. **Verify API Key Availability**:
   - Check `.env` file contains `ZAI_API_KEY`
   - Verify key format matches Z.AI requirements
   - Test key authentication with Z.AI endpoints

2. **Validate MCP Server Configuration**:
   - Check `.mcp.json` contains proper server definitions
   - Verify endpoints point to correct Z.AI URLs:
     - Web Search: `https://api.z.ai/api/mcp/web_search_prime/mcp`
     - Web Reader: `https://api.z.ai/api/mcp/web_reader/mcp`
   - Validate timeout and retry settings
   - Confirm authentication headers are properly configured

3. **Test Configuration**:
   - Run connection tests to each MCP endpoint
   - Verify response format and data structure
   - Check quota status and availability

## Quota Management

The Z.AI Lite Plan includes **100 searches + 100 readers** per month. Use these strategies:

### Quota Tracking

1. **Real-time Monitoring**:
   - Track daily/weekly/monthly usage
   - Monitor remaining quotas with warnings at 80% and 95%
   - Generate usage reports by date range

2. **Usage Patterns**:
   - Identify peak usage periods
   - Analyze search vs reader quota consumption
   - Track tool usage distribution

3. **Quota Optimization**:
   - Recommend batch processing to reduce quota usage
   - Suggest caching strategies for repeated queries
   - Plan usage around quota renewal cycles

### Quota Alerts

Set up automatic alerts when approaching limits:
- Warning at 80% usage: "Z.AI Search quota at 80% (80/100)"
- Critical at 95% usage: "Z.AI Search quota nearly exhausted (95/100)"
- Daily reports on quota status

## Health Monitoring

Monitor MCP server availability and performance:

### Connection Testing

1. **Endpoint Connectivity**:
   - Test each MCP endpoint with ping requests
   - Verify response times and availability
   - Check HTTP status codes and error responses

2. **Authentication Testing**:
   - Validate API key with authentication endpoint
   - Check for permission and authorization issues
   - Test with sample requests to verify access

3. **Response Validation**:
   - Verify response format matches expected schema
   - Check for data integrity and completeness
   - Validate error handling and recovery

### Performance Monitoring

1. **Response Time Tracking**:
   - Monitor average response times for search and reader operations
   - Track timeout rates and failures
   - Identify slow endpoints or degraded performance

2. **Success Rate Monitoring**:
   - Track success/failure rates for MCP operations
   - Monitor error rates and common failure patterns
   - Identify systematic issues requiring attention

## MCP Server Management

### Starting/Stopping Servers

Manage MCP server lifecycle:
- Start Z.AI MCP servers with proper configuration
- Stop servers gracefully to release resources
- Restart servers when health checks fail
- Monitor server status and availability

### Configuration Updates

1. **Dynamic Configuration**:
   - Update API keys without restarting servers
   - Modify timeout and retry settings
   - Adjust quota limits and warning thresholds

2. **Rollback Strategies**:
   - Backup working configurations
   - Test configurations before applying changes
   - Rollback to known-good configurations if issues occur

## Usage Analytics

Generate comprehensive reports on Z.AI MCP usage:

### Usage Reports

1. **Daily Reports**:
   - Search operations count and success rate
   - Reader operations count and success rate
   - Average response times and error rates
   - Peak usage times and patterns

2. **Weekly/Monthly Reports**:
   - Overall quota utilization
   - Usage trends and patterns
   - Cost savings from optimal usage
   - Performance improvements over time

### Optimization Insights

1. **Usage Optimization**:
   - Identify underutilized quota periods
   - Suggest batching strategies for efficiency
   - Recommend caching for repeated content

2. **Performance Optimization**:
   - Identify slow operations and bottlenecks
   - Suggest configuration improvements
   - Recommend infrastructure scaling

## Best Practices

### Quota Management

1. **Plan Usage**:
   - Prioritize critical operations within quota limits
   - Use search for research and fact-checking
   - Use reader only when content extraction is essential

2. **Monitor Continuously**:
   - Check quota status before starting large projects
   - Set up automated alerts for quota exhaustion
   - Plan quota renewal cycles around project deadlines

3. **Optimize Queries**:
   - Use specific, targeted search queries
   - Minimize unnecessary reader operations
   - Cache and reuse results where appropriate

### Error Handling

1. **Graceful Degradation**:
   - Fall back to alternative search methods when quotas exhausted
   - Retry failed operations with exponential backoff
   - Provide user-friendly error messages

2. **Recovery Strategies**:
   - Automatically retry failed operations
   - Switch to alternative endpoints if needed
   - Provide manual override options for critical operations

### Security Considerations

1. **API Key Management**:
   - Rotate API keys regularly
   - Monitor for unauthorized usage
   - Use environment variables for sensitive data

2. **Access Control**:
   - Limit API key access to authorized users
   - Log all MCP server access attempts
   - Monitor for unusual usage patterns

## Scripts and Tools

The Z.AI MCP Manager skill includes bundled scripts for common operations:

### Monitoring Scripts

1. **Quota Monitor**: Track real-time quota usage
2. **Health Checker**: Test MCP server connectivity
3. **Usage Reporter**: Generate usage analytics
4. **Configuration Validator**: Verify setup integrity

### Management Scripts

1. **Server Controller**: Start/stop MCP servers
2. **Config Manager**: Update configurations dynamically
3. **Backup Tool**: Create configuration backups
4. **Recovery Tool**: Restore working configurations

## Troubleshooting

### Common Issues

1. **Quota Exhausted**:
   - Monitor quota usage before starting operations
   - Use alternative search methods as fallback
   - Request quota increases if needed

2. **Authentication Failures**:
   - Verify API key format and validity
   - Check API key permissions and access
   - Test authentication with direct API calls

3. **Connection Issues**:
   - Verify network connectivity to Z.AI endpoints
   - Check firewall and proxy configurations
   - Test with different network configurations

### Diagnostic Tools

1. **Connection Diagnostics**:
   - Test connectivity to each MCP endpoint
   - Verify DNS resolution for Z.AI domains
   - Check SSL certificate validity

2. **API Diagnostics**:
   - Test API key with authentication endpoints
   - Verify request/response format compliance
   - Check for API rate limiting or restrictions

## Integration Examples

### Monitoring Integration

```python
# Monitor Z.AI MCP server health
from zai_mcp_manager import ZaiMCPManager

manager = ZaiMCPManager()
health_status = await manager.check_health()
quota_status = await manager.check_quotas()

if health_status.is_healthy:
    print(f"✅ All systems operational")
    print(f"📊 Quota Status: {quota_status}")
else:
    print(f"❌ Issues detected: {health_status.issues}")
```

### Usage Tracking

```python
# Track usage patterns
usage_data = await manager.get_usage_report(days=30)
print(f"Total searches: {usage_data.searches}")
print(f"Total readers: {usage_data.readers}")
print(f"Remaining quota: {usage_data.remaining}")
```

## Conclusion

The Z.AI MCP Manager skill provides comprehensive management capabilities for Z.AI MCP servers, ensuring optimal usage of the FREE quota while providing advanced monitoring and analytics. Use this skill to maintain reliable, efficient, and cost-effective Z.AI integration within your Mini-Agent workflows.
