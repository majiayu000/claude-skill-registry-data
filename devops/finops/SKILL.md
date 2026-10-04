---
name: finops
description: Cloud financial management, cost optimization, cloud spending governance, and FinOps best practices. Use when optimizing cloud costs, implementing chargeback models, analyzing cloud spend, or managing cloud budgets.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# FinOps Skill

You are a FinOps practitioner responsible for cloud financial management, cost optimization, and implementing cloud cost governance. You bridge finance, engineering, and business teams to optimize cloud spending while maintaining performance.

## Core Responsibilities

1. **Cost Visibility**
   - Tagging strategy
   - Cost allocation
   - Showback/chargeback
   - Cost reporting

2. **Cost Optimization**
   - Rightsizing
   - Reserved capacity
   - Spot instances
   - Waste elimination

3. **Rate Optimization**
   - Savings Plans/Reserved Instances
   - Enterprise discounts
   - Negotiations

4. **Usage Optimization**
   - Autoscaling
   - Scheduling
   - Resource quotas

5. **Governance**
   - Budgets and alerts
   - Policy enforcement
   - Cost reviews

## FinOps Principles

| Principle | Description |
|-----------|-------------|
| **Teams** | Teams must take ownership of cloud costs |
| **Decentralize** | Decision making moves to engineering edges |
| **Visibility** | Centralize cloud cost visibility |
| **Optimize** | Take advantage of variable cost model |
| **Govern** | Continuously govern cloud spend |

## Cost Allocation Strategy

### Tagging Policy

```yaml
# tagging-policy.yml
required_tags:
  - key: Environment
    values: [production, staging, development, testing]
    apply_to: all_resources
    mandatory: true

  - key: CostCenter
    description: "Finance department code"
    pattern: "^[0-9]{4}$"
    mandatory: true

  - key: Project
    description: "Project or application name"
    mandatory: true

  - key: Owner
    description: "Team email or individual"
    pattern: ".*@company.com"
    mandatory: true

  - key: Team
    description: "Engineering team name"
    mandatory: true

  - key: DataClassification
    values: [public, internal, confidential, restricted]
    mandatory: true

optional_tags:
  - key: Schedule
    description: "Auto-shutdown schedule"
    example: "8-18-mon-fri"

  - key: AutoStart
    values: ["true", "false"]
    description: "Whether resource auto-starts"

governance:
  enforcement:
    method: aws_config_rules
    action: notify_and_tag

  exceptions:
    process: finops-ticket
    approvers: [finops-team]
```

### Account Structure

```yaml
# account-structure.yml
aws_organization:
  root:
    - production:
        purpose: "Live customer workloads"
        cost_allocation: chargeback
        billing_alerts:
          - threshold: 80%
            action: notify_team
          - threshold: 100%
            action: notify_management

    - staging:
        purpose: "Pre-production testing"
        cost_allocation: shared
        optimization:
          - scheduled_shutdown: 19:00-07:00
          - spot_instances: true

    - development:
        purpose: "Developer environments"
        cost_allocation: shared
        budgets:
          - monthly_limit: 5000
          - per_user_limit: 500

    - shared_services:
        purpose: "Common infrastructure"
        services:
          - monitoring
          - logging
          - ci_cd
          - security
        cost_allocation: percentage_split

azure_management_groups:
  structure:
    - root:
        children:
          - production
          - non-production
          - sandbox

  policies:
    - budget_enforcement: enabled
    - tag_requirements: mandatory
    - resource_limits: per_subscription
```

## Cost Optimization Techniques

### Compute Optimization

```python
# rightsizing-analysis.py
import boto3
from datetime import datetime, timedelta

class RightsizingAnalyzer:
    """Analyze resources for rightsizing opportunities."""

    def __init__(self):
        self.ce = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')

    def analyze_ec2_rightsizing(self):
        """Find EC2 instances that can be downsized."""
        recommendations = []

        # Get EC2 cost and usage
        response = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                'End': datetime.now().strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['BlendedCost', 'UsageQuantity'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'INSTANCE_TYPE'},
                {'Type': 'TAG', 'Key': 'Name'}
            ]
        )

        for result in response['ResultsByTime']:
            for group in result['Groups']:
                instance_type = group['Keys'][0]
                metrics = group['Metrics']
                avg_cpu = self._get_avg_cpu(group['Keys'][1])

                if avg_cpu < 20:
                    recommendations.append({
                        'resource': group['Keys'][1],
                        'current_type': instance_type,
                        'suggested_type': self._get_smaller_instance(instance_type),
                        'avg_cpu': avg_cpu,
                        'potential_savings': self._calculate_savings(
                            instance_type,
                            self._get_smaller_instance(instance_type)
                        )
                    })

        return recommendations

    def _get_avg_cpu(self, instance_name):
        """Get average CPU utilization."""
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_name}],
            StartTime=datetime.now() - timedelta(days=7),
            EndTime=datetime.now(),
            Period=3600,
            Statistics=['Average']
        )

        if response['Datapoints']:
            return sum(d['Average'] for d in response['Datapoints']) / len(response['Datapoints'])
        return 0

    def _get_smaller_instance(self, current_type):
        """Get next smaller instance type."""
        size_mapping = {
            'xlarge': 'large',
            'large': 'medium',
            'medium': 'small',
            'small': 'micro'
        }

        for large, small in size_mapping.items():
            if large in current_type:
                return current_type.replace(large, small)
        return current_type

    def _calculate_savings(self, current, suggested):
        """Calculate monthly savings."""
        # Simplified - would use actual pricing API
        pricing = {
            't3.large': 0.0832,
            't3.medium': 0.0416,
            't3.small': 0.0208,
        }
        return (pricing.get(current, 0) - pricing.get(suggested, 0)) * 730
```

### Reserved Capacity Strategy

```yaml
# ri-strategy.yml
reserved_instance_strategy:
  analysis_period: 30_days
  coverage_target: 70%

  compute:
    instance_families:
      - m6i: general_purpose
      - c6i: compute_optimized
      - r6i: memory_optimized

    purchase_criteria:
      - stable_usage: 30_days
      - utilization: >60%
      - commit_duration: 1_year

    savings_plans:
      type: compute
      coverage: 80%
      term: 1_year
      payment: partial_upfront

  databases:
    rds:
      instances:
        - prod-db-primary
        - prod-db-replica
      term: 1_year
      class: convertible

  waste_detection:
    underutilized_ris:
      threshold: 40%
      action: alert
    overprovisioned:
      threshold: 80%
      action: modify_or_exchange
```

### Spot Instance Usage

```python
# spot-instance-manager.py
import boto3

class SpotInstanceManager:
    """Manage spot instances for cost savings."""

    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.autoscaling = boto3.client('autoscaling')

    def create_spot_fleet(self, launch_specs):
        """Create diversified spot fleet."""
        response = self.ec2.request_spot_fleet(
            SpotFleetRequestConfig={
                'IamFleetRole': 'arn:aws:iam::account:role/aws-ec2-spot-fleet-tagging-role',
                'TargetCapacity': 10,
                'SpotPrice': '0.05',
                'AllocationStrategy': 'capacityOptimized',
                'LaunchSpecifications': launch_specs,
                'InstanceInterruptionBehavior': 'terminate'
            }
        )
        return response['SpotFleetRequestId']

    def get_spot_recommendations(self):
        """Get spot instance recommendations."""
        # Find workloads suitable for spot
        suitable_workloads = [
            'batch_processing',
            'ci_cd_runners',
            'stateless_web_servers',
            'data_processing',
            'ml_training'
        ]

        savings = {
            'm5.large': 0.096,      # On-demand price
            'm5.large_spot': 0.038,  # Typical spot price
            'savings': 60%
        }

        return suitable_workloads

    def create_mixed_asg(self):
        """Create Auto Scaling Group with mixed instances."""
        return {
            'AutoScalingGroupName': 'mixed-asg',
            'MixedInstancesPolicy': {
                'LaunchTemplate': {
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': 'app-template',
                        'Version': '$Latest'
                    },
                    'Overrides': [
                        {'InstanceType': 'm5.large'},
                        {'InstanceType': 'm5a.large'},
                        {'InstanceType': 'm6i.large'},
                    ]
                },
                'InstancesDistribution': {
                    'OnDemandAllocationStrategy': 'prioritized',
                    'OnDemandBaseCapacity': 2,
                    'OnDemandPercentageAboveBaseCapacity': 30,
                    'SpotAllocationStrategy': 'capacity-optimized'
                }
            },
            'MinSize': 2,
            'MaxSize': 20,
            'DesiredCapacity': 5
        }
```

## Cost Governance

### Budgets and Alerts

```yaml
# budget-config.yml
budgets:
  company_wide:
    monthly_limit: 500000
    alerts:
      - threshold: 80%
        email: [finops@company.com, cfo@company.com]
      - threshold: 100%
        email: [executives@company.com]
        action: freeze_non_critical

  per_team:
    template:
      monthly_limit: varies
      alerts:
        - threshold: 75%
          email: [team-lead, team-channel]
        - threshold: 90%
          email: [director]
          action: require_approval

  per_environment:
    production:
      monthly_limit: 300000
      tolerance: high
    staging:
      monthly_limit: 50000
      schedule: business_hours_only
    development:
      monthly_limit: 10000
      per_user_limit: 500

anomaly_detection:
  enabled: true
  sensitivity: medium
  minimum_spend: 100
  alert_channels:
    - slack: #finops-alerts
    - email: finops@company.com

forecasting:
  method: ml_based
  horizon: 30_days
  accuracy_target: 90%
  monthly_review: true
```

### Policy as Code

```python
# cost-policies.py
import json

class CostPolicies:
    """Cost governance policies."""

    @staticmethod
    def instance_size_policy():
        """Restrict instance sizes to prevent overspending."""
        return {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Deny",
                "Action": "ec2:RunInstances",
                "Resource": "arn:aws:ec2:*:*:instance/*",
                "Condition": {
                    "ForAnyValue:StringNotLike": {
                        "ec2:InstanceType": [
                            "t3.micro",
                            "t3.small",
                            "t3.medium",
                            "t3.large",
                            "m5.large",
                            "m5.xlarge",
                            "c5.large",
                            "c5.xlarge"
                        ]
                    }
                }
            }]
        }

    @staticmethod
    def region_restriction_policy():
        """Restrict to approved regions."""
        return {
            "Version": "2012-10-17",
            "Statement": [{
                "Sid": "DenyUnapprovedRegions",
                "Effect": "Deny",
                "Action": "*",
                "Resource": "*",
                "Condition": {
                    "StringNotEquals": {
                        "aws:RequestedRegion": [
                            "us-east-1",
                            "us-west-2",
                            "eu-west-1"
                        ]
                    }
                }
            }]
        }

    @staticmethod
    def s3_storage_class_policy():
        """Enforce lifecycle policies on S3."""
        return {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Deny",
                "Action": "s3:PutBucketLifecycleConfiguration",
                "Resource": "*",
                "Condition": {
                    "Null": {
                        "s3:LifecycleConfiguration": "true"
                    }
                }
            }]
        }
```

## Cost Reporting

### Monthly Cost Report

```python
# cost-reporting.py
import boto3
import pandas as pd
from datetime import datetime, timedelta

class CostReporter:
    """Generate cost reports."""

    def __init__(self):
        self.ce = boto3.client('ce')

    def generate_monthly_report(self, month=None):
        """Generate comprehensive monthly report."""
        if month is None:
            month = (datetime.now() - timedelta(days=30)).strftime('%Y-%m')

        report = {
            'month': month,
            'summary': self._get_summary(month),
            'by_service': self._get_service_breakdown(month),
            'by_team': self._get_team_breakdown(month),
            'trends': self._get_trends(month),
            'optimization_opportunities': self._find_opportunities(month)
        }

        return report

    def _get_summary(self, month):
        """Get high-level summary."""
        response = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': f'{month}-01',
                'End': f'{month}-31'
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost', 'UnblendedCost', 'UsageQuantity']
        )

        total = response['ResultsByTime'][0]['Total']
        return {
            'total_cost': float(total['BlendedCost']['Amount']),
            'currency': total['BlendedCost']['Unit'],
            'vs_previous_month': self._calculate_delta(month)
        }

    def _get_service_breakdown(self, month):
        """Breakdown by AWS service."""
        response = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': f'{month}-01',
                'End': f'{month}-31'
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )

        services = []
        for group in response['ResultsByTime'][0]['Groups']:
            services.append({
                'service': group['Keys'][0],
                'cost': float(group['Metrics']['BlendedCost']['Amount'])
            })

        return sorted(services, key=lambda x: x['cost'], reverse=True)

    def _find_opportunities(self, month):
        """Identify cost optimization opportunities."""
        opportunities = []

        # Check for unattached volumes
        orphaned_volumes = self._find_orphaned_volumes()
        if orphaned_volumes:
            opportunities.append({
                'type': 'orphaned_resources',
                'resource': 'EBS volumes',
                'count': len(orphaned_volumes),
                'estimated_monthly_savings': len(orphaned_volumes) * 100
            })

        # Check for idle instances
        idle_instances = self._find_idle_instances()
        if idle_instances:
            opportunities.append({
                'type': 'rightsizing',
                'resource': 'EC2 instances',
                'count': len(idle_instances),
                'estimated_monthly_savings': len(idle_instances) * 200
            })

        return opportunities

    def generate_executive_dashboard(self):
        """Generate executive summary."""
        return {
            'total_monthly_spend': self._get_current_spend(),
            'ytd_spend': self._get_ytd_spend(),
            'forecast': self._get_forecast(),
            'top_3_cost_drivers': self._get_top_cost_drivers(),
            'optimization_savings_potential': self._get_savings_potential()
        }
```

## Multi-Cloud Cost Comparison

```yaml
# cloud-cost-comparison.yml
compute_pricing:
  aws:
    t3.medium:
      on_demand: 0.0416
      reserved_1yr: 0.0262
      spot: 0.0166

  azure:
    b2s:
      pay_as_you_go: 0.0416
      reserved_1yr: 0.0249
      spot: 0.0083

  gcp:
    n1-standard-2:
      on_demand: 0.0760
      committed_1yr: 0.0479
      spot: 0.0150

storage_pricing:
  aws_s3_standard:
    storage_per_gb: 0.023
    requests_per_1000: 0.005

  azure_blob_hot:
    storage_per_gb: 0.0184
    operations_per_10000: 0.005

  gcp_standard:
    storage_per_gb: 0.020
    operations_per_1000: 0.005

network_pricing:
  aws:
    data_transfer_out: 0.09
    data_transfer_in: 0.00

  azure:
    data_transfer_out: 0.087
    data_transfer_in: 0.00

  gcp:
    data_transfer_out: 0.12
    data_transfer_in: 0.00
```

## FinOps Team Structure

```yaml
# finops-team.yml
organizational_structure:
  finops_practitioners:
    - cloud_analysts:
        responsibilities:
          - cost_reporting
          - trend_analysis
          - invoice_validation
        skills: [excel, sql, cloud_billing]

    - engineers:
        responsibilities:
          - automation
          - tooling
          - data_pipelines
        skills: [python, sql, cloud_apis]

    - analysts:
        responsibilities:
          - rightsizing
          - rate_optimization
          - commitment_planning
        skills: [cloud_platforms, finance]

  embedded_engineers:
    - placement: one_per_engineering_team
    - responsibilities:
        - cost_awareness
        - optimization_recommendations
        - budget_tracking
    - allocation: 20%_finops_80%_engineering

  governance_committee:
    members:
      - finops_lead
      - finance_representative
      - engineering_lead
      - product_lead
    meetings: monthly
    agenda:
      - budget_review
      - optimization_opportunities
      - policy_changes

processes:
  monthly_review:
    attendees: [team_leads, finops]
    duration: 1_hour
    agenda:
      - previous_month_spend_review
      - variance_analysis
      - optimization_wins
      - action_items

  quarterly_planning:
    attendees: [executives, finops, engineering]
    duration: half_day
    agenda:
      - forecast_review
      - budget_adjustments
      - major_optimizations
      - policy_updates
```
