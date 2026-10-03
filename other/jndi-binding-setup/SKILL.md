---
name: jndi-binding-setup
description: Use when deploying a Java web application (such as CEU Mass Mediator)
  that requires access to an internal or external database and the application server
  provides JNDI as the connection pooling and naming mechanism.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - javax.faces-2.2.12.jar
  - CEU Mass Mediator
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00720
  title: CEU Mass Mediator 3.0
evidence_spans:
- 'The next library is needed in the app server: javax.faces-2.2.12.jar'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ceu_mass_mediator_3_0_cq
    doi: 10.1021/acs.jproteome.8b00720
    title: CEU Mass Mediator 3.0
  dedup_kept_from: coll_ceu_mass_mediator_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00720
  all_source_dois:
  - 10.1021/acs.jproteome.8b00720
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JNDI Binding Setup

## Summary

Configure a JNDI (Java Naming and Directory Interface) data-source binding on an application server to enable database connectivity for Java web applications. This skill is essential when deploying tools that require managed database access through a standard Java naming service.

## When to use

Apply this skill when deploying a Java web application (such as CEU Mass Mediator) that requires access to an internal or external database and the application server provides JNDI as the connection pooling and naming mechanism. Use this when you have obtained database credentials and need to establish a named reference (JNDI binding) that the application can look up at runtime.

## When NOT to use

- If the application uses direct JDBC connections rather than JNDI lookup — skip JNDI binding and configure the connection string directly in application properties.
- If database credentials have not been obtained or access has not been granted — JNDI binding configuration will fail at connection test; resolve access first.
- If the application server does not support JNDI or you are deploying to a containerized/cloud environment with alternative connection management (e.g., Kubernetes secrets, environment variables) — use the platform-specific binding method instead.

## Inputs

- Database credentials (username, password, connection URL)
- Application server configuration directory path
- Database driver class name and JDBC URL format
- Application server type (Tomcat, JBoss, GlassFish, etc.)

## Outputs

- JNDI data-source configuration file (XML or equivalent)
- Deployment manifest documenting JNDI binding name and connection parameters
- Active data-source registered on the application server
- Connection pool ready for application lookup

## How to apply

Obtain database credentials from the appropriate database administrator (in the CEU Mass Mediator case, contact [redacted-email]). Create a data-source configuration file appropriate to your application server (e.g., datasource XML for JBoss, context.xml for Tomcat) that specifies the database connection parameters (URL, username, password, driver class). Define the JNDI binding name (e.g., 'java:/datasources/CEUMassMediator') that your application will reference. Deploy the configuration file to the application server's configuration directory. Verify the data-source is active by checking the application server's admin console or logs for successful connection pool initialization. Document the JNDI binding name in a deployment manifest so that developers can correctly reference the resource in the application code.

## Related tools

- **javax.faces-2.2.12.jar** (Required library dependency installed on the application server alongside the data-source configuration to enable JSF (JavaServer Faces) web application support)
- **CEU Mass Mediator** (Metabolite annotation application that requires JNDI data-source binding to access the CEU internal database at runtime) — https://github.com/albertogilf/ceuMassMediator

## Evaluation signals

- Data-source configuration file is syntactically valid for the target application server format (XML schema compliance).
- Application server logs show successful data-source deployment and connection pool initialization (look for 'datasource deployed' or 'connection pool created' messages).
- Application server admin console lists the configured JNDI binding name as active and ready.
- Test database query through the JNDI binding succeeds (application can retrieve a connection and execute a simple SELECT).
- Deployment manifest correctly documents the JNDI binding name, database URL, and username so that developers can reference it in application code (e.g., @Resource(lookup='java:/datasources/...') in Java).

## Limitations

- JNDI binding setup is specific to the application server type and version; configuration syntax differs between Tomcat, JBoss, GlassFish, and others.
- Database credentials obtained from the administrator (e.g., [redacted-email]) must remain confidential; do not commit them to version control; use server-side environment variables or secure vaults where possible.
- Connection pool performance depends on pool size settings; improper tuning may cause connection exhaustion or slow application startup.
- Database driver JAR (not documented in the source material but implied by JDBC setup) must also be present on the application server classpath for the JNDI binding to function.

## Evidence

- [readme] Database access request step: "It is necessary to access an internal database of CEU. Request access to [redacted-email]."
- [readme] Data-source configuration requirement: "it is needed a data-source from the app server used with the credentials provided"
- [other] Deployment configuration documentation: "Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README."
