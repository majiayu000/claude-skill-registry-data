---
name: aws-sagemaker
description: Amazon SageMaker for building, training, and deploying machine learning models. Use for SageMaker AI endpoints, model training, inference, MLOps, and AWS machine learning services.
---

# Aws-Sagemaker Skill

Comprehensive assistance with aws-sagemaker development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with aws-sagemaker
- Asking about aws-sagemaker features or APIs
- Implementing aws-sagemaker solutions
- Debugging aws-sagemaker code
- Learning aws-sagemaker best practices

## Quick Reference

### Common Patterns

**Pattern 1:** DomainId The ID of the associated Domain. Type: String Length Constraints: Minimum length of 0. Maximum length of 63. Pattern: d-(-*[a-z0-9]){1,61} Required: Yes SingleSignOnUserIdentifier A specifier for the type of value specified in SingleSignOnUserValue. Currently, the only supported value is "UserName". If the Domain's AuthMode is IAM Identity Center, this field is required. If the Domain's AuthMode is not IAM Identity Center, this field cannot be specified. Type: String Pattern: UserName Required: No SingleSignOnUserValue The username of the associated AWS Single Sign-On User for this UserProfile. If the Domain's AuthMode is IAM Identity Center, this field is required, and must match a valid username of a user in your directory. If the Domain's AuthMode is not IAM Identity Center, this field cannot be specified. Type: String Length Constraints: Minimum length of 0. Maximum length of 256. Required: No Tags Each tag consists of a key and an optional value. Tag keys must be unique per resource. Tags that you specify for the User Profile are also added to all Apps that the User Profile launches. Type: Array of Tag objects Array Members: Minimum number of 0 items. Maximum number of 50 items. Required: No UserProfileName A name for the UserProfile. This value is not case sensitive. Type: String Length Constraints: Minimum length of 0. Maximum length of 63. Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62} Required: Yes UserSettings A collection of settings. Type: UserSettings object Required: No

```
d-(-*[a-z0-9]){1,61}
```

**Pattern 2:** Pattern: UserName

```
UserName
```

**Pattern 3:** Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}

```
[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
```

**Pattern 4:** UserProfileArn The user profile Amazon Resource Name (ARN). Type: String Length Constraints: Minimum length of 0. Maximum length of 256. Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:user-profile/.*

```
arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:user-profile/.*
```

**Pattern 5:** At inference time, you can request predictions for targets with cat values that are combinations of the cat values observed in the training data, for example:

```
cat
```

**Pattern 6:** MetricData A list of raw metric values to put. Type: Array of RawMetricData objects Array Members: Minimum number of 1 item. Maximum number of 10 items. Required: Yes TrialComponentName The name of the Trial Component to associate with the metrics. The Trial Component name must be entirely lowercase. Type: String Length Constraints: Minimum length of 1. Maximum length of 120. Pattern: ^[a-z0-9](-*[a-z0-9]){0,119} Required: Yes

```
^[a-z0-9](-*[a-z0-9]){0,119}
```

**Pattern 7:** AppSpecification Configuration to run a processing job in a specified container image. Type: AppSpecification object Required: No AutoMLJobArn The Amazon Resource Name (ARN) of the AutoML job associated with this processing job. Type: String Length Constraints: Minimum length of 1. Maximum length of 256. Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:automl-job/.* Required: No CreationTime The time the processing job was created. Type: Timestamp Required: No Environment Sets the environment variables in the Docker container. Type: String to string map Map Entries: Minimum number of 0 items. Maximum number of 100 items. Key Length Constraints: Minimum length of 0. Maximum length of 256. Key Pattern: [a-zA-Z_][a-zA-Z0-9_]* Value Length Constraints: Minimum length of 0. Maximum length of 256. Value Pattern: [\S\s]* Required: No ExitMessage A string, up to one KB in size, that contains metadata from the processing container when the processing job exits. Type: String Length Constraints: Minimum length of 0. Maximum length of 1024. Pattern: [\S\s]* Required: No ExperimentConfig Associates a SageMaker job as a trial component with an experiment and trial. Specified when you call the following APIs: CreateProcessingJob CreateTrainingJob CreateTransformJob Type: ExperimentConfig object Required: No FailureReason A string, up to one KB in size, that contains the reason a processing job failed, if it failed. Type: String Length Constraints: Minimum length of 0. Maximum length of 1024. Required: No LastModifiedTime The time the processing job was last modified. Type: Timestamp Required: No MonitoringScheduleArn The ARN of a monitoring schedule for an endpoint associated with this processing job. Type: String Length Constraints: Minimum length of 0. Maximum length of 256. Pattern: .* Required: No NetworkConfig Networking options for a job, such as network traffic encryption between containers, whether to allow inbound and outbound network calls to and from containers, and the VPC subnets and security groups to use for VPC-enabled jobs. Type: NetworkConfig object Required: No ProcessingEndTime The time that the processing job ended. Type: Timestamp Required: No ProcessingInputs List of input configurations for the processing job. Type: Array of ProcessingInput objects Array Members: Minimum number of 0 items. Maximum number of 10 items. Required: No ProcessingJobArn The ARN of the processing job. Type: String Length Constraints: Minimum length of 0. Maximum length of 256. Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:processing-job/[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62} Required: No ProcessingJobName The name of the processing job. Type: String Length Constraints: Minimum length of 1. Maximum length of 63. Pattern: [a-zA-Z0-9](-*[a-zA-Z0-9]){0,62} Required: No ProcessingJobStatus The status of the processing job. Type: String Valid Values: InProgress | Completed | Failed | Stopping | Stopped Required: No ProcessingOutputConfig Configuration for uploading output from the processing container. Type: ProcessingOutputConfig object Required: No ProcessingResources Identifies the resources, ML compute instances, and ML storage volumes to deploy for a processing job. In distributed training, you specify more than one instance. Type: ProcessingResources object Required: No ProcessingStartTime The time that the processing job started. Type: Timestamp Required: No RoleArn The ARN of the role used to create the processing job. Type: String Length Constraints: Minimum length of 20. Maximum length of 2048. Pattern: arn:aws[a-z\-]*:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+ Required: No StoppingCondition Configures conditions under which the processing job should be stopped, such as how long the processing job has been running. After the condition is met, the processing job is stopped. Type: ProcessingStoppingCondition object Required: No Tags An array of key-value pairs. For more information, see Using Cost Allocation Tags in the AWS Billing and Cost Management User Guide. Type: Array of Tag objects Array Members: Minimum number of 0 items. Maximum number of 50 items. Required: No TrainingJobArn The ARN of the training job associated with this processing job. Type: String Length Constraints: Minimum length of 0. Maximum length of 256. Pattern: arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:training-job/[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62} Required: No

```
arn:aws[a-z\-]*:sagemaker:[a-z0-9\-]*:[0-9]{12}:automl-job/.*
```

**Pattern 8:** Key Pattern: [a-zA-Z_][a-zA-Z0-9_]*

```
[a-zA-Z_][a-zA-Z0-9_]*
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **endpoints.md** - Endpoints documentation
- **getting_started.md** - Getting Started documentation
- **inference.md** - Inference documentation
- **models.md** - Models documentation
- **other.md** - Other documentation
- **studio.md** - Studio documentation
- **training.md** - Training documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
