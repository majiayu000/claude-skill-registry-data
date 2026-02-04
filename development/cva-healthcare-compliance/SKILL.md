---
name: cva-healthcare-compliance
description: Brazilian healthcare compliance for regulated medical and psychological content. Includes LGPD data protection, CFM/CRP/ANVISA regulatory requirements, scientific research validation, and data sanitization. Use when developing healthcare applications, ensuring LGPD compliance, validating medical content, implementing data protection, or creating regulated healthcare systems in Brazil.
allowed-tools: Read,Bash,Edit,Write
---

# Healthcare Compliance for Brazil

> **⚠️ COMPLIANCE WARNING:** This skill covers regulated healthcare content in Brazil
> **Regulations:** LGPD, CFM (Conselho Federal de Medicina), CRP (Conselho Regional de Psicologia), ANVISA
> **Last Updated:** 2025-10-29

## 🎯 Overview

Healthcare content in Brazil is subject to strict regulatory oversight from multiple authorities. This skill provides comprehensive compliance frameworks for:

- **LGPD Compliance**: Data protection for sensitive health information
- **CFM/CRP Regulations**: Professional council requirements for medical and psychological content
- **ANVISA Standards**: Health surveillance requirements for medications and procedures
- **Scientific Validation**: Evidence-based content requirements and research protocols
- **Data Sanitization**: Technical implementation of privacy protection

## 🔒 LGPD Data Protection Requirements

### Sensitive Health Data Categories (Art. 5º, II, LGPD)

```clojure
(ns lab.compliance.lgpd.health-data
  "LGPD-compliant health data classification and handling")

(def sensitive-data-categories
  {:category-1-clinical-direct
   {:level :critical
    :types [:diagnoses :lab-results :imaging :prescriptions
            :treatment-history :allergies :adverse-reactions]
    :retention-days 90
    :encryption-required true}

   :category-2-biometric
   {:level :critical
    :types [:fingerprints :facial-recognition :iris :voice
            :unique-physical-characteristics]
    :retention-days 30
    :encryption-required true}

   :category-3-genetic
   {:level :critical
    :types [:genetic-sequencing :paternity-tests
            :genetic-predispositions :hereditary-info]
    :retention-days 180
    :encryption-required true}

   :category-4-behavioral
   {:level :high
    :types [:eating-habits :substance-use :physical-activity
            :sleep-patterns :mental-health]
    :retention-days 60
    :encryption-required true}

   :category-5-indirect-identification
   {:level :medium
    :types [:appointment-locations :visit-frequency
            :family-relationships :insurance-plans :payment-history]
    :retention-days 30
    :encryption-required false}})

(defn classify-data-sensitivity
  "Classify health data by sensitivity level and compliance requirements"
  [data-type]
  (some (fn [[category config]]
          (when (some #{data-type} (:types config))
            (assoc config :category category)))
        sensitive-data-categories))

(defn requires-encryption?
  "Check if data type requires encryption under LGPD"
  [data-type]
  (:encryption-required (classify-data-sensitivity data-type)))
```

### Legal Bases for Health Data Processing

```clojure
(def lgpd-legal-bases
  {:life-protection
   {:article "Art. 7º, III"
    :description "Protection of life or physical safety"
    :requires-consent false
    :use-cases [:emergency-care :critical-interventions]}

   :health-protection
   {:article "Art. 11, II, a"
    :description "Health protection in procedures by health professionals"
    :requires-consent false
    :use-cases [:medical-diagnosis :treatment :health-services]}

   :public-interest
   {:article "Art. 7º, III"
    :description "Public interest for public health policy execution"
    :requires-consent false
    :use-cases [:epidemiology :public-health :health-surveillance]}

   :specific-consent
   {:article "Art. 11, I"
    :description "Specific and highlighted consent"
    :requires-consent true
    :use-cases [:research :marketing :data-sharing]}})

(defn validate-legal-basis
  "Validate if operation has proper legal basis under LGPD"
  [operation-type context]
  (let [basis (get lgpd-legal-bases operation-type)]
    {:valid? (not (nil? basis))
     :requires-consent? (:requires-consent basis)
     :article (:article basis)
     :applicable-use-cases (:use-cases basis)}))
```

### Data Subject Rights Implementation

```clojure
(ns lab.compliance.lgpd.subject-rights
  "Implementation of LGPD data subject rights")

(def subject-rights
  {:access
   {:deadline-days 15
    :description "Access to personal data"
    :implementation-required [:data-export :readable-format]}

   :correction
   {:deadline-days 10
    :description "Correction of incomplete, inaccurate, or outdated data"
    :implementation-required [:update-interface :validation :audit-trail]}

   :deletion
   {:deadline-days 15
    :description "Deletion of unnecessary or excessive data"
    :implementation-required [:soft-delete :anonymization :retention-policies]}

   :portability
   {:deadline-days 20
    :description "Data portability to another service provider"
    :implementation-required [:structured-export :machine-readable :common-formats]}

   :information
   {:deadline-days 15
    :description "Information about data sharing with public and private entities"
    :implementation-required [:sharing-log :third-party-tracking :consent-records]}})

(defn handle-subject-request
  "Process data subject rights request according to LGPD requirements"
  [request-type patient-id]
  (let [right (get subject-rights request-type)
        deadline (java.time.LocalDate/now)
        deadline (.plusDays deadline (:deadline-days right))]
    {:request-type request-type
     :patient-id patient-id
     :deadline deadline
     :required-actions (:implementation-required right)
     :status :pending}))
```

### Data Sanitization and Anonymization

```clojure
(ns lab.compliance.lgpd.sanitization
  "Data sanitization and anonymization utilities")

(def pii-patterns
  {:cpf #"\d{3}\.\d{3}\.\d{3}-\d{2}"
   :cpf-unformatted #"\d{11}"
   :rg #"\d{1,2}\.\d{3}\.\d{3}-[\dXx]"
   :phone #"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
   :email #"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
   :cep #"\d{5}-?\d{3}"
   :full-name #"\b[A-Z][a-z]+\s+([A-Z][a-z]+\s+)*[A-Z][a-z]+\b"
   :date-birth #"\d{2}/\d{2}/\d{4}"
   :medical-record #"(?i)prontu[aá]rio\s*:?\s*\d+"})

(defn sanitize-text
  "Remove or mask PII from text content"
  [text mask-char]
  (reduce (fn [sanitized [type pattern]]
            (clojure.string/replace sanitized pattern
              (fn [match]
                (case type
                  :cpf "***.***.***-**"
                  :email (str (subs match 0 2) "***@***"
                             (subs match (clojure.string/last-index-of match ".")))
                  :phone "(XX) XXXXX-XXXX"
                  (apply str (repeat (count match) mask-char))))))
          text
          pii-patterns))

(defn anonymize-patient-data
  "Anonymize patient data for research or analytics"
  [patient-data]
  {:patient-id (generate-anonymous-id (:patient-id patient-data))
   :age-range (age-to-range (:age patient-data))
   :gender (:gender patient-data)
   :region (location-to-region (:location patient-data))
   :condition-category (generalize-condition (:diagnosis patient-data))
   :treatment-type (generalize-treatment (:treatment patient-data))})

(defn validate-anonymization
  "Validate that anonymized data cannot be re-identified"
  [anonymized-data original-count]
  (let [k-anonymity-threshold 5
        unique-combinations (count-unique-combinations anonymized-data)]
    {:k-anonymity (/ original-count unique-combinations)
     :meets-threshold? (>= (/ original-count unique-combinations)
                           k-anonymity-threshold)
     :risk-level (if (< unique-combinations 5) :high :acceptable)}))
```

### LGPD Compliance Checklist

```clojure
(ns lab.compliance.lgpd.checklist
  "LGPD compliance validation checklist")

(def compliance-requirements
  {:technical-security-measures
   [{:id "SEC-001"
     :requirement "Implement encryption for sensitive health data at rest"
     :regulation "Art. 46, LGPD"
     :severity :critical
     :validation-fn #(check-encryption-at-rest %)}

    {:id "SEC-002"
     :requirement "Implement encryption for data in transit (TLS 1.2+)"
     :regulation "Art. 46, LGPD"
     :severity :critical
     :validation-fn #(check-tls-version %)}

    {:id "SEC-003"
     :requirement "Implement access control and authentication"
     :regulation "Art. 46, LGPD"
     :severity :critical
     :validation-fn #(check-access-control %)}

    {:id "SEC-004"
     :requirement "Implement audit logging for data access"
     :regulation "Art. 37, LGPD"
     :severity :high
     :validation-fn #(check-audit-logs %)}]

   :administrative-measures
   [{:id "ADM-001"
     :requirement "Maintain processing activity records"
     :regulation "Art. 37, LGPD"
     :severity :high
     :validation-fn #(check-processing-records %)}

    {:id "ADM-002"
     :requirement "Conduct privacy impact assessment (DPIA)"
     :regulation "Art. 38, LGPD"
     :severity :high
     :validation-fn #(check-dpia-exists %)}

    {:id "ADM-003"
     :requirement "Designate Data Protection Officer (DPO) if required"
     :regulation "Art. 41, LGPD"
     :severity :medium
     :validation-fn #(check-dpo-designation %)}]

   :incident-response
   [{:id "INC-001"
     :requirement "Notify ANPD of data breaches within 72 hours"
     :regulation "Art. 48, LGPD"
     :severity :critical
     :validation-fn #(check-notification-procedure %)}

    {:id "INC-002"
     :requirement "Notify affected data subjects of breaches"
     :regulation "Art. 48, II, LGPD"
     :severity :critical
     :validation-fn #(check-subject-notification-procedure %)}]

   :subject-rights
   [{:id "SUB-001"
     :requirement "Implement data access request mechanism"
     :regulation "Art. 18, LGPD"
     :severity :high
     :validation-fn #(check-access-mechanism %)}

    {:id "SUB-002"
     :requirement "Implement data deletion mechanism"
     :regulation "Art. 18, VI, LGPD"
     :severity :high
     :validation-fn #(check-deletion-mechanism %)}

    {:id "SUB-003"
     :requirement "Implement data portability mechanism"
     :regulation "Art. 18, V, LGPD"
     :severity :medium
     :validation-fn #(check-portability-mechanism %)}]})

(defn validate-compliance
  "Validate system against LGPD requirements"
  [system-config]
  (let [all-checks (flatten (vals compliance-requirements))
        results (map (fn [check]
                      (assoc check :result
                        ((:validation-fn check) system-config)))
                  all-checks)]
    {:total-checks (count results)
     :passed (count (filter #(:result %) results))
     :critical-failures (filter #(and (= :critical (:severity %))
                                     (not (:result %)))
                                results)
     :all-results results}))
```

## 🏥 CFM/CRP Professional Council Requirements

### Mandatory Disclaimers

```clojure
(ns lab.compliance.councils.disclaimers
  "CFM and CRP required disclaimers for healthcare content")

(def disclaimer-templates
  {:cfm-general
   {:urgency :critical
    :applies-to [:diagnoses :medications :invasive-procedures :contraindications]
    :text "As informações apresentadas não substituem a consulta médica. Sempre procure um profissional médico qualificado para diagnóstico e tratamento adequados."
    :placement :top
    :visual-style :warning}

   :cfm-specialized
   {:urgency :high
    :applies-to [:specialist-content :treatment-efficacy :medical-procedures]
    :text "Este conteúdo é de caráter informativo e não substitui a avaliação médica especializada. O diagnóstico e tratamento devem ser realizados por médico especialista na área."
    :placement :top
    :visual-style :info}

   :cfm-procedures
   {:urgency :critical
    :applies-to [:surgical-procedures :invasive-treatments :medical-devices]
    :text "Os procedimentos médicos mencionados possuem riscos e benefícios que devem ser avaliados individualmente. Consulte sempre um médico especializado."
    :placement :top-and-bottom
    :visual-style :warning}

   :crp-general
   {:urgency :high
    :applies-to [:mental-health :psychological-assessment :therapy-approaches]
    :text "As informações sobre saúde mental são de caráter educativo e não substituem a avaliação psicológica profissional. Procure um psicólogo registrado no CRP."
    :placement :top
    :visual-style :info}

   :crp-therapeutic
   {:urgency :high
    :applies-to [:therapy-techniques :psychological-interventions :self-help]
    :text "As abordagens terapêuticas mencionadas devem ser conduzidas por profissionais qualificados. Não pratique auto-terapia baseada nestas informações."
    :placement :top-and-bottom
    :visual-style :warning}

   :anvisa-medications
   {:urgency :critical
    :applies-to [:medication-info :drug-recommendations :prescription-drugs]
    :text "As informações sobre medicamentos são de caráter educativo. Não utilize medicamentos sem prescrição e orientação médica."
    :placement :top
    :visual-style :danger}

   :anvisa-procedures
   {:urgency :high
    :applies-to [:aesthetic-procedures :therapeutic-procedures :medical-devices]
    :text "Procedimentos estéticos e terapêuticos devem ser realizados por profissionais habilitados em estabelecimentos regularizados pela ANVISA."
    :placement :bottom
    :visual-style :info}

   :emergency-warning
   {:urgency :critical
    :applies-to [:all-medical-content]
    :text "Em caso de emergência médica, procure imediatamente um pronto-socorro ou ligue para o SAMU (192). Este conteúdo não oferece orientações para situações de urgência ou emergência médica."
    :placement :bottom
    :visual-style :danger}

   :results-disclaimer
   {:urgency :medium
    :applies-to [:treatment-outcomes :success-rates :before-after]
    :text "Os resultados podem variar individualmente e dependem de diversos fatores incluindo histórico médico, idade, estilo de vida e adesão ao tratamento. Não há garantia de resultados específicos."
    :placement :bottom
    :visual-style :info}})

(defn select-required-disclaimers
  "Select required disclaimers based on content type"
  [content-metadata]
  (let [content-type (:type content-metadata)
        topics (:topics content-metadata)]
    (filter (fn [[key config]]
              (some (set (:applies-to config)) topics))
            disclaimer-templates)))

(defn format-disclaimer-html
  "Format disclaimer as HTML with proper styling"
  [disclaimer-key config]
  (let [styles {:warning "background: #fff3cd; border-left: 4px solid #ffc107;"
                :danger "background: #f8d7da; border-left: 4px solid #dc3545;"
                :info "background: #e7f3ff; border: 1px solid #bee5eb;"}
        style (get styles (:visual-style config))]
    (str "<div class=\"disclaimer-" (name disclaimer-key) "\" "
         "style=\"" style " padding: 15px; margin: 20px 0; border-radius: 4px;\">"
         "<h4>⚠️ Informações Importantes</h4>"
         "<p>" (:text config) "</p>"
         "</div>")))
```

### Professional Credentials Validation

```clojure
(ns lab.compliance.councils.credentials
  "Validation of professional credentials (CRM, CRP, etc.)")

(def professional-registries
  {:crm {:name "Conselho Regional de Medicina"
         :pattern #"CRM/[A-Z]{2}\s+\d{4,6}"
         :validation-url "https://portal.cfm.org.br/busca-medicos/"
         :required-for [:medical-content :prescriptions :diagnoses]}

   :crp {:name "Conselho Regional de Psicologia"
         :pattern #"CRP\s+\d{2}/\d{5,6}"
         :validation-url "https://cadastro.cfp.org.br/"
         :required-for [:psychological-content :therapy :mental-health]}

   :crn {:name "Conselho Regional de Nutrição"
         :pattern #"CRN-\d+\s+\d{4,6}"
         :validation-url "http://www.cfn.org.br/index.php/consulta-de-nutricionistas/"
         :required-for [:nutrition-content :diet-plans :nutritional-advice]}

   :crefito {:name "Conselho Regional de Fisioterapia e Terapia Ocupacional"
             :pattern #"CREFITO-\d+\s+\d{5,6}"
             :validation-url "https://www.coffito.gov.br/"
             :required-for [:physical-therapy :rehabilitation :occupational-therapy]}})

(defn validate-credential-format
  "Validate professional credential format"
  [credential-type credential-number]
  (let [registry (get professional-registries credential-type)
        pattern (:pattern registry)]
    {:valid-format? (boolean (re-matches pattern credential-number))
     :registry-name (:name registry)
     :validation-url (:validation-url registry)
     :requires-online-verification true}))

(defn extract-professional-data
  "Extract and validate professional data from content"
  [content]
  {:professionals-mentioned
   (extract-professional-mentions content)

   :credentials-found
   (extract-credentials content)

   :validation-required
   (identify-validation-needs content)

   :compliance-status
   (check-credential-compliance content)})
```

## 🔬 Scientific Research Validation

### Evidence-Based Content Requirements

```clojure
(ns lab.compliance.research.validation
  "Scientific research validation protocols")

(def evidence-hierarchy
  {:level-1-meta-analysis
   {:strength :highest
    :description "Meta-analyses and systematic reviews"
    :minimum-studies 5
    :peer-review-required true
    :recency-years 5}

   :level-2-rct
   {:strength :high
    :description "Randomized controlled trials"
    :minimum-sample-size 50
    :peer-review-required true
    :recency-years 10}

   :level-3-cohort
   {:strength :moderate-high
    :description "Cohort studies"
    :minimum-sample-size 100
    :peer-review-required true
    :recency-years 10}

   :level-4-case-control
   {:strength :moderate
    :description "Case-control studies"
    :minimum-sample-size 50
    :peer-review-required true
    :recency-years 10}

   :level-5-case-series
   {:strength :low-moderate
    :description "Case series"
    :minimum-cases 10
    :peer-review-required true
    :recency-years 15}

   :level-6-case-report
   {:strength :low
    :description "Case reports"
    :minimum-cases 1
    :peer-review-required true
    :recency-years 15}})

(def research-databases
  {:primary
   [{:name "PubMed/MEDLINE"
     :url "https://pubmed.ncbi.nlm.nih.gov/"
     :specialty :general-medicine
     :priority :high}

    {:name "Cochrane Library"
     :url "https://www.cochranelibrary.com/"
     :specialty :systematic-reviews
     :priority :highest}

    {:name "Embase"
     :url "https://www.embase.com/"
     :specialty :biomedicine-pharmacology
     :priority :high}

    {:name "PsycINFO"
     :url "https://www.apa.org/pubs/databases/psycinfo"
     :specialty :psychology-psychiatry
     :priority :high}]

   :secondary
   [{:name "SciELO"
     :url "https://scielo.org/"
     :specialty :latin-american-research
     :priority :medium}

    {:name "LILACS"
     :url "https://lilacs.bvsalud.org/"
     :specialty :latin-american-health
     :priority :medium}

    {:name "Google Scholar"
     :url "https://scholar.google.com/"
     :specialty :broad-access
     :priority :low}]})

(defn build-search-query
  "Build advanced search query for scientific validation"
  [claim-type main-concept keywords]
  (case claim-type
    :treatment-efficacy
    {:structure "[TREATMENT] AND [CONDITION] AND [OUTCOME]"
     :example (str "\"" (:treatment keywords) "\" AND \""
                  (:condition keywords) "\" AND (\"improvement\" OR \"reduction\")")
     :filters ["Clinical trials" "Systematic reviews" "Meta-analyses"]
     :timeframe-years 10}

    :health-statistics
    {:structure "[CONDITION] AND [POPULATION] AND (\"prevalence\" OR \"incidence\" OR \"epidemiology\")"
     :example (str "\"" (:condition keywords) "\" AND \""
                  (:population keywords) "\" AND \"prevalence\"")
     :filters ["Population studies" "Cross-sectional studies"]
     :timeframe-years 5}

    :side-effects
    {:structure "[TREATMENT] AND (\"side effects\" OR \"adverse events\" OR \"complications\")"
     :example (str "\"" (:treatment keywords) "\" AND (\"side effects\" OR \"adverse events\")")
     :filters ["Case reports" "Adverse event studies"]
     :timeframe-years :all}

    :contraindications
    {:structure "[TREATMENT] AND (\"contraindications\" OR \"precautions\" OR \"warnings\")"
     :example (str "\"" (:treatment keywords) "\" AND (\"contraindications\" OR \"precautions\")")
     :filters ["Clinical guidelines" "Safety reports"]
     :timeframe-years 15}))

(defn validate-scientific-claim
  "Validate medical claim against scientific evidence"
  [claim search-results]
  (let [evidence-levels (map :evidence-level search-results)
        highest-evidence (first (sort-by :strength > evidence-levels))
        study-count (count search-results)
        recent-studies (filter #(within-recency? %) search-results)]
    {:claim claim
     :evidence-found (> study-count 0)
     :highest-evidence-level highest-evidence
     :total-studies study-count
     :recent-studies (count recent-studies)
     :validation-status (determine-validation-status
                          study-count highest-evidence recent-studies)
     :confidence-level (calculate-confidence-level
                         study-count highest-evidence recent-studies)}))
```

## 💻 Technical Implementation Utilities

### Content Validation Pipeline

```clojure
(ns lab.compliance.pipeline
  "Complete compliance validation pipeline"
  (:require [lab.compliance.lgpd.health-data :as lgpd-data]
            [lab.compliance.lgpd.sanitization :as sanitization]
            [lab.compliance.councils.disclaimers :as disclaimers]
            [lab.compliance.councils.credentials :as credentials]
            [lab.compliance.research.validation :as research]))

(defn validate-healthcare-content
  "Complete healthcare content compliance validation"
  [content metadata]
  (let [;; LGPD Data Protection
        sensitive-data (lgpd-data/identify-sensitive-data content)
        sanitized-content (if (seq sensitive-data)
                           (sanitization/sanitize-text content "*")
                           content)

        ;; Professional Credentials
        credentials-check (credentials/extract-professional-data content)

        ;; Required Disclaimers
        required-disclaimers (disclaimers/select-required-disclaimers metadata)

        ;; Scientific Validation
        claims (extract-medical-claims content)
        validated-claims (map research/validate-scientific-claim claims)

        ;; Overall Compliance
        compliance-score (calculate-compliance-score
                          {:lgpd-compliant? (empty? sensitive-data)
                           :credentials-valid? (:all-valid? credentials-check)
                           :disclaimers-present? (seq required-disclaimers)
                           :claims-validated? (all-claims-validated? validated-claims)})]

    {:sanitized-content sanitized-content
     :sensitive-data-found sensitive-data
     :credentials credentials-check
     :required-disclaimers required-disclaimers
     :validated-claims validated-claims
     :compliance-score compliance-score
     :approved? (>= compliance-score 0.95)
     :issues (collect-compliance-issues
              sensitive-data credentials-check validated-claims)}))

(defn generate-compliance-report
  "Generate detailed compliance report"
  [validation-result]
  {:timestamp (java.time.Instant/now)
   :overall-status (if (:approved? validation-result) :approved :needs-review)
   :compliance-score (:compliance-score validation-result)
   :critical-issues (filter #(= :critical (:severity %)) (:issues validation-result))
   :warnings (filter #(= :warning (:severity %)) (:issues validation-result))
   :recommendations (generate-recommendations validation-result)
   :next-steps (generate-next-steps validation-result)})
```

## 📋 Validation Checklist

### Pre-Publication Checklist

- [ ] **LGPD Compliance**
  - [ ] All sensitive health data identified and classified
  - [ ] Proper legal basis established for data processing
  - [ ] Data sanitization applied where required
  - [ ] Patient consent obtained and documented (when required)
  - [ ] Data retention policies defined and implemented
  - [ ] Encryption enabled for sensitive data (at rest and in transit)

- [ ] **Professional Credentials**
  - [ ] All participating professionals identified
  - [ ] Professional registrations validated (CRM/CRP/CRN/etc.)
  - [ ] Credentials displayed properly in content
  - [ ] Scope of practice verified against content type

- [ ] **Required Disclaimers**
  - [ ] CFM disclaimer added for medical content
  - [ ] CRP disclaimer added for psychological content
  - [ ] ANVISA disclaimer added for medications/procedures
  - [ ] Emergency warning disclaimer included
  - [ ] Results disclaimer included (when applicable)
  - [ ] Disclaimers properly positioned (top and/or bottom)

- [ ] **Scientific Validation**
  - [ ] All medical claims identified and documented
  - [ ] Scientific research conducted for each claim
  - [ ] Evidence hierarchy assessed (meta-analyses > RCTs > cohort studies)
  - [ ] Minimum evidence threshold met (5+ studies for high-impact claims)
  - [ ] References properly cited in standard format
  - [ ] Study quality assessed (peer review, impact factor, methodology)

- [ ] **Content Quality**
  - [ ] Language is professional but accessible
  - [ ] No absolute claims without strong evidence
  - [ ] Risks and benefits presented balanced
  - [ ] Patient action encouraged toward professional consultation
  - [ ] No guarantee of specific results

- [ ] **Technical Security**
  - [ ] TLS 1.2+ for data transmission
  - [ ] Access controls implemented
  - [ ] Audit logging enabled
  - [ ] Incident response procedures documented

### Post-Publication Monitoring

- [ ] Monitor for ANPD compliance updates
- [ ] Track CFM/CRP regulatory changes
- [ ] Review scientific literature for updates
- [ ] Update disclaimers as regulations evolve
- [ ] Conduct quarterly compliance audits

## 🔗 Related Skills

- [`cva-healthcare-pipeline`](../cva-healthcare-pipeline/SKILL.md) - Full healthcare content pipeline with integrated compliance
- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - Agent type selection for healthcare applications
- [`cva-overview`](../cva-overview/SKILL.md) - Clojure Vertex AI ADK overview
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Google Cloud Vertex AI setup

## 📘 Official Regulatory Documentation

### LGPD Resources
- **Lei Geral de Proteção de Dados**: [LGPD Official Text](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- **ANPD (Autoridade Nacional de Proteção de Dados)**: [https://www.gov.br/anpd/](https://www.gov.br/anpd/)
- **LGPD Guide for Healthcare**: [ANPD Healthcare Guidance](https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia-lgpd-saude)

### Medical Council Resources
- **CFM (Conselho Federal de Medicina)**: [https://portal.cfm.org.br/](https://portal.cfm.org.br/)
- **CFM Resolution 1974/2011**: Medical advertising regulations
- **CFM Resolution 2217/2018**: Medical code of ethics
- **CRM Professional Registry Search**: [CFM Registry Lookup](https://portal.cfm.org.br/busca-medicos/)

### Psychology Council Resources
- **CRP (Conselho Regional de Psicologia)**: [https://crp.org.br/](https://crp.org.br/)
- **CFP (Conselho Federal de Psicologia)**: [https://site.cfp.org.br/](https://site.cfp.org.br/)
- **Resolution CFP 011/2018**: Ethical guidelines for psychologist communication
- **CRP Professional Registry Search**: [CFP Registry Lookup](https://cadastro.cfp.org.br/)

### ANVISA Resources
- **ANVISA**: [https://www.gov.br/anvisa/](https://www.gov.br/anvisa/)
- **Medication Database**: [ANVISA Bulário Eletrônico](https://consultas.anvisa.gov.br/#/bulario/)
- **RDC 44/2009**: Regulations for health services advertising

### Scientific Databases
- **PubMed**: [https://pubmed.ncbi.nlm.nih.gov/](https://pubmed.ncbi.nlm.nih.gov/)
- **Cochrane Library**: [https://www.cochranelibrary.com/](https://www.cochranelibrary.com/)
- **SciELO**: [https://scielo.org/](https://scielo.org/)
- **LILACS**: [https://lilacs.bvsalud.org/](https://lilacs.bvsalud.org/)

## 🚨 Critical Warnings

1. **Never skip disclaimers** - CFM/CRP violations can result in professional license suspension
2. **Always validate credentials** - Impersonation of healthcare professionals is a criminal offense
3. **Protect patient data** - LGPD violations carry fines up to R$ 50 million
4. **Document consent** - Explicit consent required for sensitive health data processing
5. **Report breaches within 72 hours** - ANPD notification is mandatory
6. **Never guarantee results** - Medical outcome guarantees violate CFM ethics code
