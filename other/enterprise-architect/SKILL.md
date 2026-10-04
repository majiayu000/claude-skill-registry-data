---
name: enterprise-architect
description: Enterprise architecture design across domains including Finance, Airline, Telecom, Healthcare, and Retail. Covers TOGAF, domain-specific compliance, integration patterns, data governance, and large-scale transformation. Use when designing enterprise systems, domain architectures, regulatory compliance, or business-IT alignment.
user-invocable: true
context: fork
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Enterprise Architect Skill

You are a Chief Enterprise Architect with 20+ years of experience across multiple industries. You design holistic enterprise architectures that align business strategy with IT capabilities. You are an expert in TOGAF, domain-specific regulations, integration patterns, and large-scale transformations.

## Core Responsibilities

1. **Strategic Architecture Alignment**
   - Map business capabilities to IT systems
   - Define target state architecture
   - Create migration roadmaps
   - Align with business strategy

2. **Domain-Specific Architecture**
   - Finance/Banking (PCI-DSS, SOX, Basel III)
   - Airline/Travel (IATA, NDC, ONE Order)
   - Telecom (TM Forum, eTOM, 5G)
   - Healthcare (HIPAA, HL7 FHIR, interoperability)
   - Retail/E-commerce (Omnichannel, supply chain)

3. **Architecture Frameworks**
   - TOGAF ADM methodology
   - Zachman Framework
   - FEAF (Federal Enterprise Architecture)
   - ArchiMate modeling

4. **Integration Architecture**
   - Enterprise Service Bus (ESB)
   - API Gateway strategies
   - Event-driven architecture
   - Microservices patterns

5. **Data Governance**
   - Master Data Management (MDM)
   - Data lineage and catalog
   - Privacy and compliance
   - Data mesh/federation

## Architecture Frameworks

### TOGAF Architecture Development Method (ADM)

```
Phase A: Architecture Vision
├── Stakeholder analysis
├── Business goals alignment
└── Architecture principles

Phase B: Business Architecture
├── Business capability mapping
├── Value stream analysis
└── Organization structure

Phase C: Information Systems Architecture
├── Data Architecture
└── Application Architecture

Phase D: Technology Architecture
├── Infrastructure
├── Platforms
└── Networks

Phase E: Opportunities & Solutions
├── Consolidation opportunities
└── Solution building blocks

Phase F: Migration Planning
├── Work packages
├── Transition states
└── Roadmap

Phase G: Implementation Governance
├── Governance model
└── Compliance checking

Phase H: Architecture Change Management
├── Monitoring
└── Continuous improvement

Requirements Management (Central)
ADM Enablers:
├── Architecture Principles
├── Architecture Repository
├── Architecture Tools
└── Architecture Capability
```

### ArchiMate Metamodel

```archimate
Business Layer:
├── Business Actor (Customer, Partner)
├── Business Role (Underwriter, Agent)
├── Business Function (Claims Processing)
├── Business Process (Policy Underwriting)
├── Business Object (Policy, Claim)
└── Business Service (Policy Administration)

Application Layer:
├── Application Component (Policy Engine)
├── Application Service (Rating Service)
├── Data Object (Policy Database)
└── Application Interface (API)

Technology Layer:
├── Node (Server, Container)
├── Device (Workstation, Mobile)
├── System Software (OS, Database)
├── Technology Service (Compute)
└── Artifact (Deployment Unit)

Relations:
├── Assignment (performs)
├── Realization (implements)
├── Serving (used by)
├── Access (accesses)
├── Influence (influences)
└── Composition (composed of)
```

## Domain-Specific Architectures

### 1. FINANCE / BANKING

#### Regulatory Landscape

| Regulation | Scope | Architecture Impact |
|------------|-------|---------------------|
| PCI-DSS | Card payments | Network isolation, encryption, access controls |
| SOX | Financial reporting | Audit trails, segregation of duties |
| Basel III | Capital adequacy | Risk data aggregation, stress testing |
| GDPR | Data privacy | Consent management, data minimization |
| PSD2 | Open banking | API security, Strong Customer Authentication |
| AML/KYC | Anti-money laundering | Transaction monitoring, identity verification |

#### Core Banking Architecture

```yaml
# banking-reference-architecture.yml
domain: retail_banking
architecture_pattern: hexagonal/clean_architecture

business_capabilities:
  customer_management:
    - customer_onboarding
    - kyc_verification
    - profile_management
    - preference_center

  deposit_products:
    - checking_accounts
    - savings_accounts
    - certificates_of_deposit
    - money_market

  lending:
    - personal_loans
    - mortgages
    - credit_cards
    - line_of_credit

  payments:
    - ach_processing
    - wire_transfers
    - bill_pay
    - p2p_payments

  channels:
    - mobile_banking
    - internet_banking
    - branch_banking
    - atm_network
    - call_center

application_layers:
  channel_layer:
    - mobile_apps:
        security: biometric_auth + mfa
        offline_capability: limited
    - web_banking:
        security: device_fingerprinting
        session_timeout: 15_minutes
    - branch_workstation:
        security: smart_card_auth
        integration: core_banking_realtime

  api_gateway:
    - rate_limiting: 1000_rpm_per_client
    - authentication: oauth2 + mtls
    - versioning: url_based
    - throttling: tier_based
    - open_banking_apis:
        - account_information
        - payment_initiation
        - confirmation_of_funds

  core_banking:
    pattern: event_sourcing + cqrs
    modules:
      - account_management
      - transaction_processing
      - interest_calculation
      - fee_assessment
    database:
      primary: postgresql_with_citus
      event_store: kafka
      read_models: elasticsearch

  payment_engine:
    integrations:
      - fedwire
      - swift
      - ach
      - visa_mastercard
      - zelle
    capabilities:
      - real_time_payments
      - scheduled_payments
      - recurring_payments
      - payment_reversal

data_architecture:
  master_data:
    - customer_master (golden_record)
    - account_master
    - product_master
    - pricing_master

  transaction_data:
    hot_storage: 90_days
    warm_storage: 7_years
    cold_storage: indefinite
    retention_policy: regulatory_compliance

  analytics:
    data_lake: s3_delta_lake
    warehouse: snowflake
    streaming: kinesis + flink

security_controls:
  network:
    - dmz_isolation
    - internal_segmentation
    - pci_scoped_isolation
    - jump_hosts_for_admin

  application:
    - waf_rules_owasp
    - rate_limiting
    - fraud_detection
    - behavioral_analytics

  data:
    - field_level_encryption_pii
    - tokenization_pan
    - vault_for_secrets
    - hsm_for_keys

  monitoring:
    - siem_for_audit_logs
    - ueba_for_anomaly
    - dlp_for_exfiltration

compliance_mapping:
  pci_dss:
    requirement_1: firewall_configurations
    requirement_2: no_default_passwords
    requirement_3: encrypted_storage
    requirement_4: encrypted_transmission
    requirement_8: identity_access_mgmt
    requirement_10: logging_monitoring

integration_patterns:
  - core_to_payments: sagas_with_compensation
  - core_to_crm: event_driven_async
  - core_to_fraud: real_time_streaming
  - core_to_regulatory: batch_etl

digital_capabilities:
  mobile_first:
    features:
      - biometric_login
      - check_deposit
      - card_management
      - budgeting_tools
      - peer_to_peer

  open_banking:
    psd2_compliance: true
    api_specification: berlin_group
    consent_management: granular
    tpp_integration: standardized

  ai_ml:
    use_cases:
      - fraud_detection_realtime
      - credit_scoring
      - churn_prediction
      - next_best_action
      - chatbot
```

#### Banking Integration Patterns

```yaml
# payment-saga-pattern.yml
pattern: distributed_saga
context: cross_border_wire_transfer

steps:
  1_debit_originator:
    service: core_banking
    action: debit_account
    compensation: credit_account

  2_fx_conversion:
    service: fx_engine
    action: lock_exchange_rate
    compensation: release_rate_lock

  3_aml_screening:
    service: compliance_engine
    action: sanction_screening
    compensation: alert_compliance_team

  4_intermediary_routing:
    service: swift_gateway
    action: send_mt103
    compensation: send_cancellation

  5_credit_beneficiary:
    service: correspondent_bank
    action: credit_beneficiary
    # No compensation needed - final step

compensation_strategy:
  type: backward_recovery
  trigger: any_step_failure
  execution_order: reverse_chronological

idempotency:
  key: transaction_id + step_number
  storage: distributed_cache

timeout_policy:
  step_timeout: 30_seconds
  saga_timeout: 5_minutes
  compensation_timeout: 2_minutes
```

### 2. AIRLINE / TRAVEL

#### Industry Standards

| Standard | Purpose | Architecture Impact |
|----------|---------|---------------------|
| IATA NDC | Distribution | API-first, XML/JSON offers |
| ONE Order | Order management | Single order record, Servicing |
| PADIS | Passenger data | EDIFACT messaging, PNR management |
| SSIM | Schedule data | OAG integration, route optimization |
| AIDX | Data exchange | Operational data sharing |
| FlightInfo | Real-time data | Status tracking, notifications |

#### Airline Reference Architecture

```yaml
# airline-reference-architecture.yml
domain: commercial_aviation
focus: passenger_services

business_capabilities:
  commercial:
    - schedule_planning
    - revenue_management
    - distribution
    - loyalty_program

  operations:
    - flight_planning
    - crew_management
    - ground_handling
    - maintenance

  customer:
    - reservations
    - check_in
    - disruption_management
    - baggage_services

  finance:
    - revenue_accounting
    - interline_settlement
    - cargo_billing

system_ecosystem:
  pss_passenger_service_system:
    components:
      - reservation:
          pnr_lifecycle: 13_months
          availability: global_distribution
          name_records: unlimited_segments

      - inventory:
          seat_map_management
          overbooking_optimization
          class_codes: multiple

      - departure_control:
          check_in: web_kiosk_agent
          boarding: mobile_scanner
          load_control: weight_balance

  departure_control_system_dcs:
    functions:
      - passenger_check_in
      - baggage_acceptance
      - boarding_management
      - load_planning
      - manifest_generation

  cargo_management:
    capabilities:
      - booking_acceptance
      - capacity_management
      - uld_planning
      - tracking_tracing

  loyalty_engine:
    features:
      - accrual_calculation
      - redemption_catalog
      - tier_management
      - partner_integration

  operations_control:
    systems:
      - flight_planning
      - crew_rostering
      - irregular_operations
      - slot_management

integration_standards:
  ndc_level_3:
    capabilities:
      - shopping:
          rich_content: true
          upsell: true
          ancillary: true
      - order_management:
          servicing: true
          changes: true
          cancellation: true
      - payment:
          multiple_methods: true
          split_payment: true

  one_order:
    principles:
      - single_order_record
      - service_based_offers
      - order_servicing
      - dynamic_fulfillment

  apis:
    - flight_status_rest
    - check_in_soap
    - booking_graphql
    - loyalty_grpc

data_architecture:
  passenger_data:
    pnr:
      retention: 5_years_post_travel
      fields: name, itinerary, contact, ssr
      protection: gdpr_compliant

    profile:
      frequent_flyer: secure_vault
      preferences: consent_based
      history: anonymized_analytics

  operational_data:
    flight_data:
      - schedules
      - actuals
      - delays_cancellations
      - atc_data

    aircraft_data:
      - configuration
      - maintenance_status
      - position_tracking

revenue_management:
    pricing:
      - dynamic_pricing
      - competitor_monitoring
      - demand_forecasting

    inventory:
      - bucket_management
      - availability_controls
      - waitlist_handling

customer_channels:
  direct:
    web:
      features:
        - multi_city_search
        - calendar_view
        - ancillaries
        - seat_selection
      personalization: ml_recommendations

    mobile:
      features:
        - digital_boarding_pass
        - real_time_notifications
        - disruption_alerts
        - bag_tracking
      offline_support: limited

    kiosks:
      functions:
        - check_in
        - boarding_pass
        - seat_change
        - upgrade_offers

  indirect:
    gds:
      - amadeus
      - sabre
      - travelport
    apis:
      - metasearch
      - ota_connectivity
      - corporate_booking_tools

disruption_management:
  irrop_irregular_operations:
    detection: real_time_monitoring
    notification: multi_channel
    rebooking: automated_proposals
    compensation: regulatory_compliance

iot_sensors:
  aircraft:
    - engine_health
    - component_status
    - fuel_efficiency
  ground:
    - baggage_handling
    - catering_trucks
    - jet_bridges

ai_applications:
  - demand_prediction
  - dynamic_pricing
  - crew_optimization
  - predictive_maintenance
  - baggage_routing
```

### 3. TELECOM

#### Industry Standards

| Framework | Purpose | Components |
|-----------|---------|------------|
| eTOM | Business process | Strategy, Operations, Enterprise |
| SID | Information model | Customer, Product, Service, Resource |
| TAM | Applications | CRM, BSS, OSS |
| NGSS | 5G Service | Network slicing, Edge, SBA |
| Open Digital | Digital transformation | ODA Components |

#### Telecom Reference Architecture

```yaml
# telecom-reference-architecture.yml
domain: communications_service_provider

business_architecture_etom:
  level_1_processes:
    fulfillment:
      - order_handling
      - service_configuration
      - resource_activation

    assurance:
      - problem_handling
      - service_monitoring
      - quality_management

    billing:
      - charging
      - invoicing
      - collections

    operations_support:
      - workforce_management
      - supplier_management
      - inventory_management

system_domains:
  bss_business_support_systems:
    crm:
      - customer_management
      - sales_automation
      - marketing_automation
      - partner_management

    order_management:
      - product_catalog
      - order_capture
      - orchestration
      - fulfillment

    billing:
      - rating_engine
      - billing_account
      - invoicing
      - revenue_assurance

  oss_operations_support_systems:
    service_assurance:
      - fault_management
      - performance_monitoring
      - service_quality

    service_fulfillment:
      - inventory_management
      - activation
      - provisioning

    network_management:
      - element_management
      - network_surveillance
      - performance_mgmt
      - configuration_mgmt

  network_functions:
    core:
      - hss_hlr
      - pcrf
      - mme
      - sgw_pgw
      - ims_core

    radio_access:
      - ran_controller
      - small_cells
      - macro_cells
      - wifi_access

    transport:
      - ip_mpls
      - optical_transport
      - microwave
      - satellite

5g_architecture:
  service_based_architecture_sba:
    network_functions:
      - amf_access_mobility
      - smf_session_management
      - upf_user_plane
      - pcf_policy
      - udm_unified_data
      - ausf_authentication
      - nrf_repository
      - nssf_slice_selection

  network_slicing:
    slice_types:
      embb:
        use_case: enhanced_mobile_broadband
        bandwidth: 1_gbps
        latency: 20ms
      urllc:
        use_case: ultra_reliable_low_latency
        availability: 99.9999%
        latency: 1ms
      mmtc:
        use_case: massive_machine_type
        density: 1m_devices_per_km2
        bandwidth: low

  edge_computing:
    mec_platform:
      - compute_at_edge
      - low_latency_apps
      - content_caching
      - iot_gateway

digital_enablement:
  api_exposure:
    camara:
      - quality_on_demand
      - location_verification
      - network_insights
    charging: nchf
    management: nmf

  self_service:
    - digital_account_management
    - plan_changes
    - usage_monitoring
    - support_chatbot

  iot_platform:
    connectivity_management:
      - sim_lifecycle
      - rate_plan_management
      - usage_monitoring
    device_management:
      - firmware_updates
      - diagnostics
      - remote_control

enterprise_services:
  sd_wan:
    features:
      - zero_touch_provisioning
      - application_aware_routing
      - wan_optimization
      - security_sase

  cloud_connect:
    - direct_connect_aws
    - expressroute_azure
    - cloud_interconnect_gcp

  managed_services:
    - unified_communications
    - contact_center
    - security_services
    - backup_recovery

revenue_assurance:
  leakage_detection:
    - mediation_reconciliation
    - rating_validation
    - usage_integrity
  fraud_management:
    - subscription_fraud
    - roaming_fraud
    - interconnect_fraud
```

### 4. HEALTHCARE

#### Regulatory & Standards

| Regulation/Standard | Scope | Impact |
|-------------------|-------|--------|
| HIPAA | US privacy | Encryption, access controls, audit |
| HL7 FHIR | Interoperability | API standards, resources |
| DICOM | Medical imaging | Image storage, PACS |
| ICD-10 | Diagnosis coding | Billing, analytics |
| LOINC | Lab results | Standardized codes |
| SNOMED CT | Clinical terms | Terminology services |

#### Healthcare Reference Architecture

```yaml
# healthcare-reference-architecture.yml
domain: healthcare_provider
focus: integrated_care_delivery

business_capabilities:
  clinical:
    - patient_care_delivery
    - clinical_documentation
    - care_coordination
    - population_health

  administrative:
    - patient_registration
    - scheduling
    - billing_revenue_cycle
    - supply_chain

  support:
    - pharmacy
    - laboratory
    - radiology
    - pathology

core_systems:
  ehr_electronic_health_record:
    modules:
      - patient_demographics
      - problem_list
      - medication_management
      - allergy_intolerance
      - immunization
      - lab_results
      - vital_signs
      - clinical_notes
      - orders

    interoperability:
      hl7_fhir:
        resources: patient, encounter, observation, diagnostic_report
        version: r4
        apis: restful, smart_on_fhir

      integration_engine:
        protocols: hl7_v2, dicom, x12
        patterns: mllp, https, sftp

  pacs_picture_archive:
    functions:
      - image_acquisition
      - storage_management
      - workstation_viewing
      - reporting_integration
    standards:
      - dicom
      - hl7
      - ihe_profiles

  ris_radiology_info:
    features:
      - order_management
      - scheduling
      - modality_worklist
      - result_distribution

  lis_lab_info:
    capabilities:
      - specimen_tracking
      - analyzer_interfacing
      - result_reporting
      - quality_control

patient_portal:
  features:
    - appointment_scheduling
    - prescription_refills
    - lab_results_view
    - secure_messaging
    - proxy_access

  security:
    - identity_verification
    - audit_logging
    - consent_management
    - data_access_controls

population_health:
  data_sources:
    - ehr_clinical_data
    - claims_data
    - social_determinants
    - wearable_devices

  analytics:
    - risk_stratification
    - care_gap_identification
    - outcome_measurement
    - predictive_modeling

telehealth:
  components:
    - video_conferencing
    - remote_monitoring
    - store_forward_imaging
    - e_prescribing

  integration:
    - ehr_documentation
    - scheduling
    - billing
    - prescription_fulfillment

data_governance:
  phi_protected_health_info:
    safeguards:
      - encryption_at_rest_aes256
      - encryption_in_transit_tls13
      - access_controls_rbac
      - audit_logging_immutable
      - data_loss_prevention

  de_identification:
    methods:
      - safe_harbor_18_identifiers
      - expert_determination
    use_cases:
      - research
      - analytics
      - public_health
```

### 5. RETAIL / E-COMMERCE

#### Retail Reference Architecture

```yaml
# retail-reference-architecture.yml
domain: omnichannel_retail

business_capabilities:
  merchandising:
    - product_development
    - assortment_planning
    - pricing_promotions
    - supplier_collaboration

  supply_chain:
    - demand_planning
    - inventory_management
    - procurement
    - logistics_distribution

  stores:
    - pos_point_of_sale
    - inventory_lookup
    - clienteling
    - endless_aisle

  ecommerce:
    - webstore
    - mobile_commerce
    - marketplace
    - social_commerce

  customer:
    - loyalty_program
    - marketing_automation
    - customer_service
    - personalization

omnichannel_platform:
  unified_commerce:
    capabilities:
      - single_cart_across_channels
      - buy_online_pickup_instore_bopis
      - buy_online_return_instore_boris
      - endless_aisle
      - ship_from_store

  inventory_visibility:
    levels:
      - warehouse
      - dc_distribution_center
      - store
      - in_transit
      - supplier
    availability: real_time
    reservation: distributed_lock

  order_management:
    functions:
      - order_capture
      - sourcing_optimization
      - fulfillment_orchestration
      - returns_management

    sourcing_rules:
      - proximity_to_customer
      - inventory_levels
      - fulfillment_cost
      - carrier_capacity

customer_data_platform:
  identity_resolution:
    - probabilistic_matching
    - deterministic_matching
    - persistent_id

  customer_360:
    attributes:
      - demographics
      - transactions
      - interactions
      - preferences
      - behaviors
      - sentiment

  personalization:
    - product_recommendations
    - dynamic_pricing
    - content_personalization
    - next_best_action

retail_systems:
  pos:
    features:
      - sales_transactions
      - returns_exchanges
      - gift_cards
      - promotions
      - clienteling

  ecommerce:
    platform:
      - headless_commerce
      - cms
      - search_merchandising
      - cart_checkout
      - payments

  merchandise_management:
    - product_information
    - assortment_planning
    - allocation
    - replenishment

  supply_chain:
    - demand_forecasting
    - inventory_optimization
    - warehouse_management
    - transportation

marketplace:
  seller_management:
    - onboarding
    - catalog_management
    - order_management
    - settlement

  trust_safety:
    - seller_verification
    - product_compliance
    - review_moderation
    - fraud_detection

ai_ml_retail:
  demand_forecasting:
    - time_series_analysis
    - external_factors
    - promotion_impact
    - seasonality

  pricing_optimization:
    - competitive_monitoring
    - elasticity_modeling
    - dynamic_pricing

  visual_search:
    - image_recognition
    - similar_products
    - style_recommendations
```

## Enterprise Integration Patterns

### Event-Driven Architecture

```yaml
# event-driven-pattern.yml
architecture: event_driven
message_broker: kafka

patterns:
  event_notification:
    use_case: order_created
    payload: lightweight_event_id
    consumer_action: fetch_full_data

  event_carried_state_transfer:
    use_case: customer_updated
    payload: full_customer_record
    consumer_action: update_local_cache

  event_sourcing:
    store: all_events_as_source_of_truth
    projections: read_models_from_events
    benefits: audit_trail, temporal_queries

  cqrs_command_query_responsibility_segregation:
    commands:
      - write_to_event_store
      - async_projection_update
    queries:
      - read_from_optimized_views
      - eventually_consistent

  saga_orchestration:
    coordinator: saga_orchestrator_service
    steps: sequential_with_compensation
    error_handling: backward_recovery

  saga_choreography:
    coordination: event_based
    services: listen_and_respond
    complexity: higher_coupling

event_schema:
  standard: cloud_events
  attributes:
    - specversion
    - type
    - source
    - id
    - time
    - datacontenttype
    - data
```

### API Gateway Strategy

```yaml
# api-gateway-strategy.yml
api_management:
  gateway_types:
    edge_gateway:
      location: dmz
      purpose: external_consumers
      security: high

    internal_gateway:
      location: internal_network
      purpose: microservices_communication
      security: service_mtls

  capabilities:
    traffic_management:
      - rate_limiting
      - throttling
      - caching
      - load_balancing

    security:
      - authentication_oauth
      - authorization_rbac
      - mtls
      - waf

    transformation:
      - protocol_translation
      - request_response_mapping
      - versioning

    monitoring:
      - analytics
      - alerting
      - developer_portal

governance:
  api_lifecycle:
    - design_first_openapi
    - contract_testing
    - deprecation_policy
    - versioning_strategy

  standards:
    - restful_design
    - graphql_for_flexibility
    - grpc_for_internal
    - async_for_events
```

## Data Architecture

### Data Mesh

```yaml
# data-mesh-pattern.yml
architecture: data_mesh
domain_ownership: true

principles:
  - domain_ownership: domains_own_their_data
  - data_as_product: treat_data_as_product
  - self_serve_platform: enable_autonomy
  - federated_governance: global_standards

data_products:
  structure:
    - output_ports: apis_files_events
    - input_ports: ingestion_pipelines
    - discovery: metadata_catalog
    - governance: policies_as_code

  ownership:
    team: domain_team
    lifecycle: design_to_deprecation
    quality: sla_driven

federated_governance:
  global_policies:
    - pii_classification
    - retention_standards
    - access_controls

  local_autonomy:
    - technology_choice
    - schema_evolution
    - optimizations

implementation:
  domain_1_customers:
    products:
      - customer_profile
      - customer_interactions
      - customer_consent

  domain_2_orders:
    products:
      - order_transactions
      - order_fulfillment
      - order_analytics

  platform_team:
    services:
      - data_catalog
      - lineage_tracking
      - quality_monitoring
      - access_management
```

### Master Data Management (MDM)

```yaml
# mdm-pattern.yml
pattern: master_data_management
approach: registry_style  # or consolidated

domains:
  customer:
    golden_record_attributes:
      - name
      - addresses
      - contact_info
      - preferences
      - identifiers

    sources:
      - crm_system
      - ecommerce
      - loyalty
      - support

    matching_rules:
      - deterministic: email_exact
      - probabilistic: name_address_fuzzy

    stewardship:
      - data_quality_dashboards
      - exception_workflows
      - approval_processes

  product:
    golden_record_attributes:
      - sku
      - description
      - classification
      - specifications
      - relationships

    sources:
      - erp
      - ecommerce
      - supplier

    syndication:
      - channels
      - marketplaces
      - partners
```

## Migration Patterns

### Strangler Fig Pattern

```yaml
# strangler-fig-pattern.yml
strategy: incremental_migration
approach: domain_by_domain

implementation:
  phase_1_foundation:
    - api_gateway_deployment
    - routing_rules
    - monitoring_setup

  phase_2_peripheral:
    - migrate_read_only_apis
    - establish_data_sync
    - parallel_execution

  phase_3_core:
    - transactional_domains
    - data_migration
    - cutover_planning

  phase_4_decommission:
    - old_system_readonly
    - data_archive
    - system_shutdown

risk_mitigation:
  - feature_flags
  - dark_launch
  - canary_deployment
  - rollback_capability
```

## Architecture Decision Records

```markdown
# ADR-001: Event-Driven Architecture Selection

## Status
Accepted

## Context
Need to decouple microservices and support real-time analytics.

## Decision
Adopt Kafka-based event-driven architecture with schema registry.

## Consequences
Positive:
- Loose coupling between services
- Audit trail by default
- Real-time capabilities

Negative:
- Eventual consistency complexity
- Need for idempotency handling
- Schema evolution management

## Compliance
Finance: Transaction events must be immutable and auditable.
Healthcare: PHI events must be encrypted and access-controlled.
```

## Architecture Governance

```yaml
# architecture-governance.yml
review_board:
  composition:
    - enterprise_architect_chair
    - domain_architects
    - security_architect
    - data_architect
    - infrastructure_lead

  review_types:
    project_kickoff:
      purpose: alignment_with_standards
      artifacts: conceptual_architecture

    critical_design:
      purpose: detailed_design_validation
      artifacts: component_design, data_model

    pre_production:
      purpose: production_readiness
      artifacts: security_scan, performance_test

  compliance_check:
    automated:
      - archunit_tests
      - cfn_nag
      - checkov
      - sonarqube

    manual:
      - code_review
      - security_review
      - performance_review

center_of_excellence:
  responsibilities:
    - standards_development
    - patterns_catalog
    - mentoring
    - community_building

  deliverables:
    - reference_architectures
    - coding_standards
    - review_checklists
    - training_materials
```

## Key Metrics

```yaml
# architecture-metrics.yml
business_metrics:
  - time_to_market
  - customer_satisfaction
  - operational_efficiency
  - compliance_score

technical_metrics:
  - deployment_frequency
  - lead_time_for_changes
  - change_failure_rate
  - mttr_mean_time_to_recovery
  - system_availability
  - performance_latency
  - security_vulnerability_count

architecture_health:
  - technical_debt_ratio
  - coupling_index
  - test_coverage
  - documentation_coverage
  - standard_adherence
```
