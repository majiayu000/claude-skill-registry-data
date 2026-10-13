---
name: keycloak-docs-index
description: |
  Keycloak Documentation Index. Use this skill whenever the user asks about Keycloak features, configuration, deployment, security, monitoring, or any other Keycloak-related topic. This skill provides a structured index of official Keycloak documentation with direct links to complete guides, allowing agents to quickly navigate and access the full documentation context needed for any Keycloak task. Always refer to this index when helping with Keycloak setup, configuration, troubleshooting, or best practices - even if the user doesn't explicitly mention "documentation" or "guide".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Keycloak Documentation Index

This is a reference guide to the official Keycloak documentation. Use this to find and access the appropriate documentation modules for any Keycloak-related task.

## How to Use This Skill

1. **Identify the category** relevant to the user's question (e.g., deployment, security, monitoring)
2. **Select the module** that matches the specific need
3. **Access the full documentation** by navigating to the provided link for complete context and step-by-step instructions
4. **Read the full guide** before providing solutions to ensure accuracy and completeness

---

## Documentation Categories & Modules

### Getting Started

Quick-start guides for deploying Keycloak in different environments.

| Module         | Description                                                | Link                                                                                                                                                       |
| -------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenJDK**    | Get started with Keycloak on a physical or virtual server. | [https://www.keycloak.org/getting-started/getting-started-zip](https://www.keycloak.org/getting-started/getting-started-zip)                               |
| **Docker**     | Get started with Keycloak on Docker.                       | [https://www.keycloak.org/getting-started/getting-started-docker](https://www.keycloak.org/getting-started/getting-started-docker)                         |
| **Podman**     | Get started with Keycloak on Podman.                       | [https://www.keycloak.org/getting-started/getting-started-podman](https://www.keycloak.org/getting-started/getting-started-podman)                         |
| **Kubernetes** | Get started with Keycloak on Kubernetes.                   | [https://www.keycloak.org/getting-started/getting-started-kube](https://www.keycloak.org/getting-started/getting-started-kube)                             |
| **OpenShift**  | Get started with Keycloak on OpenShift.                    | [https://www.keycloak.org/getting-started/getting-started-openshift](https://www.keycloak.org/getting-started/getting-started-openshift)                   |
| **Scaling**    | Scale and tune your Keycloak installation.                 | [https://www.keycloak.org/getting-started/getting-started-scaling-and-tuning](https://www.keycloak.org/getting-started/getting-started-scaling-and-tuning) |

### Server Configuration & Administration

Server setup, configuration, deployment, and operational tasks.

| Module                         | Description                                                                                      | Link                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Configuring Keycloak**       | Configure and start Keycloak.                                                                    | [https://www.keycloak.org/server/configuration](https://www.keycloak.org/server/configuration)                       |
| **Supported Configurations**   | Overview of supported platforms, Java versions, databases, and system requirements for Keycloak. | [https://www.keycloak.org/server/supported-configurations](https://www.keycloak.org/server/supported-configurations) |
| **Configuring for Production** | Prepare Keycloak for use in production.                                                          | [https://www.keycloak.org/server/configuration-production](https://www.keycloak.org/server/configuration-production) |
| **Bootstrap & Admin Recovery** | Bootstrap Keycloak and recover access by creating a temporary admin account.                     | [https://www.keycloak.org/server/bootstrap-admin-recovery](https://www.keycloak.org/server/bootstrap-admin-recovery) |
| **Directory Structure**        | Understand the purpose of the directories under the installation root.                           | [https://www.keycloak.org/server/directory-structure](https://www.keycloak.org/server/directory-structure)           |
| **Running in Container**       | Run Keycloak from a container image.                                                             | [https://www.keycloak.org/server/containers](https://www.keycloak.org/server/containers)                             |
| **Configuring TLS**            | Configure Keycloak's HTTPS certificates for ingoing and outgoing requests.                       | [https://www.keycloak.org/server/enabletls](https://www.keycloak.org/server/enabletls)                               |
| **Configuring Hostname**       | Configure the frontend and backchannel endpoints exposed by Keycloak.                            | [https://www.keycloak.org/server/hostname](https://www.keycloak.org/server/hostname)                                 |
| **Reverse Proxy**              | Configure Keycloak with a reverse proxy, API gateway, or load balancer.                          | [https://www.keycloak.org/server/reverseproxy](https://www.keycloak.org/server/reverseproxy)                         |
| **Database Configuration**     | Configure a relational database for Keycloak to store user, client, and realm data.              | [https://www.keycloak.org/server/db](https://www.keycloak.org/server/db)                                             |
| **Distributed Caches**         | Configure the caching layer to cluster multiple Keycloak instances and increase performance.     | [https://www.keycloak.org/server/caching](https://www.keycloak.org/server/caching)                                   |
| **Outgoing HTTP Requests**     | Configure the client used for outgoing HTTP requests.                                            | [https://www.keycloak.org/server/outgoinghttp](https://www.keycloak.org/server/outgoinghttp)                         |
| **Trusted Certificates**       | Configure the Keycloak Truststore to communicate through TLS.                                    | [https://www.keycloak.org/server/keycloak-truststore](https://www.keycloak.org/server/keycloak-truststore)           |
| **mTLS Configuration**         | Configure Mutual TLS to verify clients that are connecting to Keycloak.                          | [https://www.keycloak.org/server/mutual-tls](https://www.keycloak.org/server/mutual-tls)                             |
| **Features**                   | Configure Keycloak to use optional features.                                                     | [https://www.keycloak.org/server/features](https://www.keycloak.org/server/features)                                 |
| **Providers**                  | Configure providers for Keycloak.                                                                | [https://www.keycloak.org/server/configuration-provider](https://www.keycloak.org/server/configuration-provider)     |
| **Logging**                    | Configure logging for Keycloak.                                                                  | [https://www.keycloak.org/server/logging](https://www.keycloak.org/server/logging)                                   |
| **FIPS 140-2**                 | Configure Keycloak server for FIPS compliance.                                                   | [https://www.keycloak.org/server/fips](https://www.keycloak.org/server/fips)                                         |
| **Management Interface**       | Configure Keycloak's management interface for endpoints such as metrics and health checks.       | [https://www.keycloak.org/server/management-interface](https://www.keycloak.org/server/management-interface)         |
| **Realm Import/Export**        | Import and export realms as JSON files.                                                          | [https://www.keycloak.org/server/importExport](https://www.keycloak.org/server/importExport)                         |
| **Vault**                      | Configure and use a vault in Keycloak.                                                           | [https://www.keycloak.org/server/vault](https://www.keycloak.org/server/vault)                                       |
| **All Configuration**          | Review build options and configuration for Keycloak.                                             | [https://www.keycloak.org/server/all-config](https://www.keycloak.org/server/all-config)                             |
| **Provider Configuration**     | Review provider configuration options.                                                           | [https://www.keycloak.org/server/all-provider-config](https://www.keycloak.org/server/all-provider-config)           |
| **Update Compatibility**       | Execute the update compatibility command to check if Keycloak supports a rolling update.         | [https://www.keycloak.org/server/update-compatibility](https://www.keycloak.org/server/update-compatibility)         |
| **Windows Service**            | Install and run Keycloak as a Windows service using Apache Commons Daemon.                       | [https://www.keycloak.org/server/windows-service](https://www.keycloak.org/server/windows-service)                   |

### Operator (Kubernetes/OpenShift)

Deploy and manage Keycloak using Kubernetes Operators.

| Module                     | Description                                                                            | Link                                                                                                                 |
| -------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Operator Installation**  | Install the Keycloak Operator on Kubernetes and OpenShift.                             | [https://www.keycloak.org/operator/installation](https://www.keycloak.org/operator/installation)                     |
| **Basic Deployment**       | Install Keycloak using the Operator.                                                   | [https://www.keycloak.org/operator/basic-deployment](https://www.keycloak.org/operator/basic-deployment)             |
| **Realm Import**           | Automate a realm import using the Operator.                                            | [https://www.keycloak.org/operator/realm-import](https://www.keycloak.org/operator/realm-import)                     |
| **Advanced Configuration** | Tune advanced aspects of the Keycloak CR.                                              | [https://www.keycloak.org/operator/advanced-configuration](https://www.keycloak.org/operator/advanced-configuration) |
| **Rolling Updates**        | Avoid downtime when changing themes, providers, or configurations in optimized images. | [https://www.keycloak.org/operator/rolling-updates](https://www.keycloak.org/operator/rolling-updates)               |
| **Custom Images**          | Customize and optimize the Keycloak container.                                         | [https://www.keycloak.org/operator/customizing-keycloak](https://www.keycloak.org/operator/customizing-keycloak)     |

### Observability & Monitoring

Monitor, observe, and troubleshoot Keycloak deployments.

| Module                           | Description                                                                                                                       | Link                                                                                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **OpenTelemetry Integration**    | Learn about OpenTelemetry integration for centralized observability and telemetry data.                                           | [https://www.keycloak.org/observability/telemetry](https://www.keycloak.org/observability/telemetry)                                                 |
| **Health Checks**                | Check if an instance has finished its start up and is ready to serve requests by calling its health REST endpoints.               | [https://www.keycloak.org/observability/health](https://www.keycloak.org/observability/health)                                                       |
| **Metrics Configuration**        | Collect metrics to gain insights about state and activities of a running instance of Keycloak.                                    | [https://www.keycloak.org/observability/configuration-metrics](https://www.keycloak.org/observability/configuration-metrics)                         |
| **Event Metrics**                | Event metrics provide an aggregated view of user activities in a Keycloak instance.                                               | [https://www.keycloak.org/observability/event-metrics](https://www.keycloak.org/observability/event-metrics)                                         |
| **Service Level Indicators**     | Track performance and reliability as perceived by users with Service Level Indicators (SLIs) and Service Level Objectives (SLOs). | [https://www.keycloak.org/observability/keycloak-service-level-indicators](https://www.keycloak.org/observability/keycloak-service-level-indicators) |
| **Troubleshooting with Metrics** | Use metrics for troubleshooting errors and performance issues.                                                                    | [https://www.keycloak.org/observability/metrics-for-troubleshooting](https://www.keycloak.org/observability/metrics-for-troubleshooting)             |
| **Tracing**                      | Record information during the request lifecycle with OpenTelemetry tracing to identify root causes for latencies and errors.      | [https://www.keycloak.org/observability/tracing](https://www.keycloak.org/observability/tracing)                                                     |
| **Grafana Dashboards**           | Install the Keycloak Grafana dashboards to visualize the metrics captured.                                                        | [https://www.keycloak.org/observability/grafana-dashboards](https://www.keycloak.org/observability/grafana-dashboards)                               |
| **Exemplars**                    | Use exemplars to connect a metric to a recorded trace to analyze the root cause of errors or latencies.                           | [https://www.keycloak.org/observability/exemplars](https://www.keycloak.org/observability/exemplars)                                                 |

### Securing Applications

Secure applications and services using Keycloak.

| Module                                     | Description                                                                         | Link                                                                                                                                                                                       |
| ------------------------------------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Security Overview**                      | Understand basic concepts for securing applications.                                | [https://www.keycloak.org/securing-apps/overview](https://www.keycloak.org/securing-apps/overview)                                                                                         |
| **OpenID Connect**                         | Use OpenID Connect with Keycloak to secure applications and services.               | [https://www.keycloak.org/securing-apps/oidc-layers](https://www.keycloak.org/securing-apps/oidc-layers)                                                                                   |
| **JavaScript Adapter**                     | Client-side JavaScript library that can be used to secure web applications.         | [https://www.keycloak.org/securing-apps/javascript-adapter](https://www.keycloak.org/securing-apps/javascript-adapter)                                                                     |
| **Node.js Adapter**                        | Node.js adapter to protect server-side JavaScript apps.                             | [https://www.keycloak.org/securing-apps/nodejs-adapter](https://www.keycloak.org/securing-apps/nodejs-adapter)                                                                             |
| **Apache HTTPD Module (mod_auth_openidc)** | Configure the mod_auth_openidc Apache module with Keycloak.                         | [https://www.keycloak.org/securing-apps/mod-auth-openidc](https://www.keycloak.org/securing-apps/mod-auth-openidc)                                                                         |
| **SAML Galleon Feature Pack**              | Using Keycloak SAML Galleon feature pack to secure applications in WildFly and EAP. | [https://www.keycloak.org/securing-apps/saml-galleon-layers](https://www.keycloak.org/securing-apps/saml-galleon-layers)                                                                   |
| **Apache mod_auth_mellon Module**          | Configure the mod_auth_mellon Apache module with Keycloak.                          | [https://www.keycloak.org/securing-apps/mod-auth-mellon](https://www.keycloak.org/securing-apps/mod-auth-mellon)                                                                           |
| **Distribution Registry**                  | Configure a Distribution Registry to use Keycloak.                                  | [https://www.keycloak.org/securing-apps/distribution-registry](https://www.keycloak.org/securing-apps/distribution-registry)                                                               |
| **Client Registration**                    | Use the client registration service.                                                | [https://www.keycloak.org/securing-apps/client-registration](https://www.keycloak.org/securing-apps/client-registration)                                                                   |
| **Client Registration CLI**                | Use the CLI to automate client registration.                                        | [https://www.keycloak.org/securing-apps/client-registration-cli](https://www.keycloak.org/securing-apps/client-registration-cli)                                                           |
| **Model Context Protocol (MCP)**           | Using Keycloak as an authorization server for Model Context Protocol (MCP) servers. | [https://www.keycloak.org/securing-apps/mcp-authz-server](https://www.keycloak.org/securing-apps/mcp-authz-server)                                                                         |
| **Token Exchange**                         | Configure and use token exchange for Keycloak.                                      | [https://www.keycloak.org/securing-apps/token-exchange](https://www.keycloak.org/securing-apps/token-exchange)                                                                             |
| **JWT Authorization Grant**                | Guide for the JWT Authorization Grant specification RFC 7521 / 7523.                | [https://www.keycloak.org/securing-apps/jwt-authorization-grant](https://www.keycloak.org/securing-apps/jwt-authorization-grant)                                                           |
| **OAuth Identity Chaining**                | Guide for OAuth Identity and Authorization Chaining Across Domains.                 | [https://www.keycloak.org/securing-apps/oauth-identity-authorization-chaining-across-domains](https://www.keycloak.org/securing-apps/oauth-identity-authorization-chaining-across-domains) |
| **DPoP (Proof-of-Possession)**             | Guide for securing applications with DPoP using Keycloak.                           | [https://www.keycloak.org/securing-apps/dpop](https://www.keycloak.org/securing-apps/dpop)                                                                                                 |
| **Specifications Implemented**             | List of specifications and standards implemented by Keycloak.                       | [https://www.keycloak.org/securing-apps/specifications](https://www.keycloak.org/securing-apps/specifications)                                                                             |
| **Admin Client**                           | Using the Keycloak admin client to access the Keycloak Admin REST API.              | [https://www.keycloak.org/securing-apps/admin-client](https://www.keycloak.org/securing-apps/admin-client)                                                                                 |
| **Authorization Client**                   | Using the Keycloak authz client to administer and check permissions.                | [https://www.keycloak.org/securing-apps/authz-client](https://www.keycloak.org/securing-apps/authz-client)                                                                                 |
| **Policy Enforcer**                        | Using the Keycloak policy enforcer in Java applications.                            | [https://www.keycloak.org/securing-apps/policy-enforcer](https://www.keycloak.org/securing-apps/policy-enforcer)                                                                           |
| **Upgrading Client Libraries**             | How to upgrade the Keycloak Client Libraries.                                       | [https://www.keycloak.org/securing-apps/upgrading](https://www.keycloak.org/securing-apps/upgrading)                                                                                       |

### Framework & Platform Integrations

Integrate Keycloak with popular frameworks and platforms.

| Module            | Description                                                                             | Link                                                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Apache APISIX** | Integrate Keycloak for Authentication with Apache APISIX.                               | [https://apisix.apache.org/blog/2021/12/10/integrate-keycloak-auth-in-apisix](https://apisix.apache.org/blog/2021/12/10/integrate-keycloak-auth-in-apisix)                                     |
| **KrakenD**       | Secure APIs with an API Gateway.                                                        | [https://www.krakend.io/docs/authorization/keycloak/](https://www.krakend.io/docs/authorization/keycloak/)                                                                                     |
| **Quarkus**       | Using OpenID Connect and Keycloak to secure your Quarkus applications.                  | [https://quarkus.io/guides/security-keycloak-authorization](https://quarkus.io/guides/security-keycloak-authorization)                                                                         |
| **Traefik Hub**   | Use Keycloak as an identity provider or identity broker for Traefik Hub API management. | [https://doc.traefik.io/traefik-hub/authentication-authorization/idp/keycloak](https://doc.traefik.io/traefik-hub/authentication-authorization/idp/keycloak)                                   |
| **WildFly**       | Secure WildFly Applications with Keycloak.                                              | [https://wildfly-security.github.io/wildfly-elytron/blog/securing-wildfly-apps-openid-connect/](https://wildfly-security.github.io/wildfly-elytron/blog/securing-wildfly-apps-openid-connect/) |

### High Availability & Clustering

Deploy Keycloak in highly available configurations.

| Module                         | Description                                                                      | Link                                                                                                                                             |
| ------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **High Availability Overview** | Explore the different Keycloak high-availability architectures.                  | [https://www.keycloak.org/high-availability/introduction](https://www.keycloak.org/high-availability/introduction)                               |
| **Single-Cluster Deployments** | Deploy a single Keycloak cluster, optionally across multiple availability-zones. | [https://www.keycloak.org/high-availability/single-cluster/introduction](https://www.keycloak.org/high-availability/single-cluster/introduction) |
| **Multi-Cluster Deployments**  | Connect multiple Keycloak deployments in independent Kubernetes clusters.        | [https://www.keycloak.org/high-availability/multi-cluster/introduction](https://www.keycloak.org/high-availability/multi-cluster/introduction)   |

### UI Customization

Customize and theme the Keycloak user interfaces.

| Module                        | Description                                                                         | Link                                                                                                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Introduction**              | Learn how to customize the user interfaces.                                         | [https://www.keycloak.org/ui-customization/introduction](https://www.keycloak.org/ui-customization/introduction)                           |
| **Themes**                    | Understand how to create and configure themes.                                      | [https://www.keycloak.org/ui-customization/themes](https://www.keycloak.org/ui-customization/themes)                                       |
| **Quick Theme**               | Learn how to customize the consoles and login screens with the Quick Theme utility. | [https://www.keycloak.org/ui-customization/quick-theme](https://www.keycloak.org/ui-customization/quick-theme)                             |
| **Localization**              | Learn how to localize strings in the UIs.                                           | [https://www.keycloak.org/ui-customization/localization](https://www.keycloak.org/ui-customization/localization)                           |
| **Avatars**                   | Use avatars in the Admin console and Account console.                               | [https://www.keycloak.org/ui-customization/avatars](https://www.keycloak.org/ui-customization/avatars)                                     |
| **Welcome Theme**             | Learn how to customize the welcome theme.                                           | [https://www.keycloak.org/ui-customization/welcome-theme](https://www.keycloak.org/ui-customization/welcome-theme)                         |
| **Creating Your Own Console** | Learn to create your own version of Admin Console or Account Console.               | [https://www.keycloak.org/ui-customization/creating-your-own-console](https://www.keycloak.org/ui-customization/creating-your-own-console) |
| **Using npm UI Packages**     | Learn how to use UI modules in your own application.                                | [https://www.keycloak.org/ui-customization/themes-react](https://www.keycloak.org/ui-customization/themes-react)                           |

### Migration

Upgrade and migrate to new Keycloak versions.

| Module                                | Description                                                                   | Link                                                                                                               |
| ------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Migrating to Quarkus Distribution** | Migrate to the new Quarkus distribution from the legacy WildFly distribution. | [https://www.keycloak.org/migration/migrating-to-quarkus](https://www.keycloak.org/migration/migrating-to-quarkus) |

---

## Quick Reference

### By Use Case

**I want to deploy Keycloak:**

- Getting Started (OpenJDK, Docker, Kubernetes, etc.)
- Server Configuration → Configuring for Production

**I want to secure my application:**

- Securing Applications → Security Overview & OpenID Connect
- Securing Applications → Framework-specific adapters (JavaScript, Node.js, etc.)

**I want to monitor or troubleshoot:**

- Observability & Monitoring (all modules)

**I want to customize the UI:**

- UI Customization (Themes, Quick Theme, Localization)

**I want high availability:**

- High Availability & Clustering (all modules)

**I need to configure advanced features:**

- Server Configuration & Administration (specific modules)

---

## Using This Index Effectively

1. **Find your category** - Scan the categories above to find what matches your task
2. **Select the module** - Each module has a clear title and description
3. **Access the documentation** - Click the link to read the complete guide on keycloak.org
4. **Follow the guide** - They provide step-by-step instructions for your specific task

This skill should be used to provide quick, accurate navigation to the official documentation whenever a Keycloak-related question arises.
