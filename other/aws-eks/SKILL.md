---
name: aws-eks
description: Amazon Elastic Kubernetes Service (EKS) for running Kubernetes on AWS. Use for container orchestration, deploying applications, managing clusters, and Kubernetes workloads on AWS.
---

# Aws-Eks Skill

Comprehensive assistance with aws-eks development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with aws-eks
- Asking about aws-eks features or APIs
- Implementing aws-eks solutions
- Debugging aws-eks code
- Learning aws-eks best practices

## Quick Reference

### Common Patterns

**Pattern 1:** Determine the name and version of the add-on you want to download attributions for. Update the following command with the name and version: curl -O https://amazon-eks-docs.s3.amazonaws.com/attributions/<add-on-name>/<add-on-version>/attributions.zip For example: curl -O https://amazon-eks-docs.s3.amazonaws.com/attributions/kube-state-metrics/v2.14.0-eksbuild.1/attributions.zip Use the command to download the file.

```
curl -O https://amazon-eks-docs.s3.amazonaws.com/attributions/<add-on-name>/<add-on-version>/attributions.zip
```

**Pattern 2:** For example:

```
curl -O https://amazon-eks-docs.s3.amazonaws.com/attributions/kube-state-metrics/v2.14.0-eksbuild.1/attributions.zip
```

**Pattern 3:** Create a Kubernetes namespace called game-2048 with the --save-config flag. kubectl create namespace game-2048 --save-config You should see the following response output: namespace/game-2048 created Deploy the 2048 Game Sample application. kubectl apply -n game-2048 -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml This manifest sets up a Kubernetes Deployment, Service, and Ingress for the game-2048 namespace, creating the necessary resources to deploy and expose the game-2048 application within the cluster. It includes the creation of a service named service-2048 that exposes the deployment on port 80, and an Ingress resource named ingress-2048 that defines routing rules for incoming HTTP traffic and annotations for an internet-facing Application Load Balancer (ALB). You should see the following response output: namespace/game-2048 configured deployment.apps/deployment-2048 created service/service-2048 created ingress.networking.k8s.io/ingress-2048 created Run the following command to get the Ingress resource for the game-2048 namespace. kubectl get ingress -n game-2048 You should see the following response output: NAME CLASS HOSTS ADDRESS PORTS AGE ingress-2048 alb * k8s-game2048-ingress2-eb379a0f83-378466616.region-code.elb.amazonaws.com 80 31s You’ll need to wait several minutes for the Application Load Balancer (ALB) to provision before you begin the following steps. Open a web browser and enter the ADDRESS from the previous step to access the web application. For example: k8s-game2048-ingress2-eb379a0f83-378466616.region-code.elb.amazonaws.com You should see the 2048 game in your browser. Play!

```
game-2048
```

**Pattern 4:** Open a web browser and enter the ADDRESS from the previous step to access the web application. For example:

```
ADDRESS
```

**Pattern 5:** If you want to specify one or more security groups that Amazon EKS assigns to the network interfaces that it creates, specify the securityGroup option. Whether you choose any security groups or not, Amazon EKS creates a security group that enables communication between your cluster and your VPC. Amazon EKS associates this security group, and any that you choose, to the network interfaces that it creates. For more information about the cluster security group that Amazon EKS creates, see View Amazon EKS security group requirements for clusters. You can modify the rules in the cluster security group that Amazon EKS creates. If you want to specify which IPv4 Classless Inter-domain Routing (CIDR) block Kubernetes assigns service IP addresses from, specify the serviceIPv4CIDR option. Specifying your own range can help prevent conflicts between Kubernetes services and other networks peered or connected to your VPC. Enter a range in CIDR notation. For example: 10.2.0.0/16. The CIDR block must meet the following requirements: Be within one of the following ranges: 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16. Have a minimum size of /24 and a maximum size of /12. Not overlap with the range of the VPC for your Amazon EKS resources. You can only specify this option when using the IPv4 address family and only at cluster creation. If you don’t specify this, then Kubernetes assigns service IP addresses from either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks. If you’re creating cluster and want the cluster to assign IPv6 addresses to Pods and services instead of IPv4 addresses, specify the ipFamily option. Kubernetes assigns IPv4 addresses to Pods and services, by default. Before deciding to use the IPv6 family, make sure that you’re familiar with all of the considerations and requirements in the VPC requirements and considerations, Subnet requirements and considerations, View Amazon EKS security group requirements for clusters, and Learn about IPv6 addresses to clusters, Pods, and services topics. If you choose the IPv6 family, you can’t specify an address range for Kubernetes to assign IPv6 service addresses from like you can for the IPv4 family. Kubernetes assigns service addresses from the unique local address range (fc00::/7).

```
IPv4
```

**Pattern 6:** Specifying your own range can help prevent conflicts between Kubernetes services and other networks peered or connected to your VPC. Enter a range in CIDR notation. For example: 10.2.0.0/16.

```
10.2.0.0/16
```

**Pattern 7:** accessConfig The access configuration for the cluster. Type: CreateAccessConfigRequest object Required: No bootstrapSelfManagedAddons If you set this value to False when creating a cluster, the default networking add-ons will not be installed. The default networking add-ons include vpc-cni, coredns, and kube-proxy. Use this option when you plan to install third-party alternative add-ons or self-manage the default networking add-ons. Type: Boolean Required: No clientRequestToken A unique, case-sensitive identifier that you provide to ensure the idempotency of the request. Type: String Required: No computeConfig Enable or disable the compute capability of EKS Auto Mode when creating your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account Type: ComputeConfigRequest object Required: No deletionProtection Indicates whether to enable deletion protection for the cluster. When enabled, the cluster cannot be deleted unless deletion protection is first disabled. This helps prevent accidental cluster deletion. Default value is false. Type: Boolean Required: No encryptionConfig The encryption configuration for the cluster. Type: Array of EncryptionConfig objects Array Members: Maximum number of 1 item. Required: No kubernetesNetworkConfig The Kubernetes network configuration for the cluster. Type: KubernetesNetworkConfigRequest object Required: No logging Enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs . By default, cluster control plane logs aren't exported to CloudWatch Logs . For more information, see Amazon EKS Cluster control plane logs in the Amazon EKS User Guide . NoteCloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see CloudWatch Pricing. Type: Logging object Required: No name The unique name to give to your cluster. The name can contain only alphanumeric characters (case-sensitive), hyphens, and underscores. It must start with an alphanumeric character and can't be longer than 100 characters. The name must be unique within the AWS Region and AWS account that you're creating the cluster in. Type: String Length Constraints: Minimum length of 1. Maximum length of 100. Pattern: ^[0-9A-Za-z][A-Za-z0-9\-_]* Required: Yes outpostConfig An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. Before creating a local cluster on an Outpost, review Local clusters for Amazon EKS on AWS Outposts in the Amazon EKS User Guide. This object isn't available for creating Amazon EKS clusters on the AWS cloud. Type: OutpostConfigRequest object Required: No remoteNetworkConfig The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created. Type: RemoteNetworkConfigRequest object Required: No resourcesVpcConfig The VPC configuration that's used by the cluster control plane. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see Cluster VPC Considerations and Cluster Security Group Considerations in the Amazon EKS User Guide. You must specify at least two subnets. You can specify up to five security groups. However, we recommend that you use a dedicated security group for your cluster control plane. Type: VpcConfigRequest object Required: Yes roleArn The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. For more information, see Amazon EKS Service IAM Role in the Amazon EKS User Guide . Type: String Required: Yes storageConfig Enable or disable the block storage capability of EKS Auto Mode when creating your EKS Auto Mode cluster. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account. Type: StorageConfigRequest object Required: No tags Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources. Type: String to string map Map Entries: Maximum number of 50 items. Key Length Constraints: Minimum length of 1. Maximum length of 128. Value Length Constraints: Maximum length of 256. Required: No upgradePolicy New clusters, by default, have extended support enabled. You can disable extended support when creating a cluster by setting this value to STANDARD. Type: UpgradePolicyRequest object Required: No version The desired Kubernetes version for your cluster. If you don't specify a value here, the default version available in Amazon EKS is used. NoteThe default version might not be the latest version available. Type: String Required: No zonalShiftConfig Enable or disable ARC zonal shift for the cluster. If zonal shift is enabled, AWS configures zonal autoshift for the cluster. Zonal shift is a feature of Amazon Application Recovery Controller (ARC). ARC zonal shift is designed to be a temporary measure that allows you to move traffic for a resource away from an impaired AZ until the zonal shift expires or you cancel it. You can extend the zonal shift if necessary. You can start a zonal shift for an Amazon EKS cluster, or you can allow AWS to do it for you by enabling zonal autoshift. This shift updates the flow of east-to-west network traffic in your cluster to only consider network endpoints for Pods running on worker nodes in healthy AZs. Additionally, any ALB or NLB handling ingress traffic for applications in your Amazon EKS cluster will automatically route traffic to targets in the healthy AZs. For more information about zonal shift in EKS, see Learn about Amazon Application Recovery Controller (ARC) Zonal Shift in Amazon EKS in the Amazon EKS User Guide . Type: ZonalShiftConfigRequest object Required: No

```
False
```

**Pattern 8:** Pattern: ^[0-9A-Za-z][A-Za-z0-9\-_]*

```
^[0-9A-Za-z][A-Za-z0-9\-_]*
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **addons.md** - Addons documentation
- **cluster_management.md** - Cluster Management documentation
- **deployment.md** - Deployment documentation
- **getting_started.md** - Getting Started documentation
- **networking.md** - Networking documentation
- **nodes.md** - Nodes documentation
- **other.md** - Other documentation
- **security.md** - Security documentation

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
