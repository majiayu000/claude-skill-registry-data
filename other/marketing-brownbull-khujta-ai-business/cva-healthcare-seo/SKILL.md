---
name: cva-healthcare-seo
description: Healthcare SEO strategy for Brazilian medical and wellness professionals. Includes specialized keyword research (dermatology, psychology, nutrition), professional content templates, local SEO optimization, and regulatory-compliant content structures. Use when optimizing healthcare websites, creating medical practice content, implementing local SEO for health professionals, or building patient acquisition funnels.
allowed-tools: Read,Bash,Edit,Write
---

# Healthcare SEO for Brazil

> **⚠️ COMPLIANCE WARNING:** All SEO content must comply with CFM/CRP/ANVISA regulations
> **Required Skills:** Must be used with [`cva-healthcare-compliance`](../cva-healthcare-compliance/SKILL.md)
> **Last Updated:** 2025-10-29

## 🎯 Overview

Healthcare SEO in Brazil requires balancing search optimization with strict regulatory compliance. This skill provides:

- **Specialized Keywords**: Medical specialty-specific keyword research and strategies
- **Professional Templates**: Regulatory-compliant content structures for healthcare
- **Local SEO**: Geographic optimization for medical practices and clinics
- **Conversion Optimization**: Patient acquisition strategies within ethical guidelines
- **Compliance-First Approach**: SEO that respects CFM/CRP/ANVISA regulations

## 🔍 Specialized Keyword Research

### Keyword Classification Framework

```clojure
(ns lab.seo.healthcare.keywords
  "Healthcare-specific keyword research and classification")

(def keyword-intent-types
  {:informational
   {:description "Learning about conditions, symptoms, treatments"
    :conversion-potential :low
    :volume :high
    :examples ["o que é melasma" "sintomas de ansiedade" "como tratar acne"]}

   :navigational
   {:description "Looking for specific professional or clinic"
    :conversion-potential :medium
    :volume :medium
    :examples ["dr joão silva dermatologista" "clínica abc são paulo"]}

   :commercial
   {:description "Comparing treatments, researching before consultation"
    :conversion-potential :high
    :volume :medium
    :examples ["melhor tratamento para acne" "laser co2 ou fraxel" "quanto custa terapia"]}

   :transactional
   {:description "Ready to book consultation or treatment"
    :conversion-potential :highest
    :volume :low
    :examples ["agendar consulta dermatologista" "marcar terapia hoje" "dermato próximo"]}})

(def specialty-keywords
  {:dermatology
   {:primary
    {:keywords ["dermatologista" "tratamento acne" "laser CO2"
                "melasma tratamento" "rosácea dermatologia"]
     :monthly-volume-range [1000 10000]
     :competition :high
     :cpc-range [5.00 15.00]}

    :secondary
    {:keywords ["clínica dermatológica" "procedimentos estéticos"
                "consulta dermatológica" "dermatologia estética"
                "tratamento manchas pele"]
     :monthly-volume-range [500 5000]
     :competition :medium
     :cpc-range [3.00 10.00]}

    :long-tail
    {:keywords ["melhor dermatologista para acne [CIDADE]"
                "tratamento laser CO2 [BAIRRO]"
                "como tratar melasma [CIDADE]"
                "dermatologista convênio [CONVENIO]"
                "dermatologista especialista em [CONDICAO]"]
     :monthly-volume-range [10 500]
     :competition :low
     :cpc-range [2.00 8.00]}

    :conditions
    {:keywords ["acne" "melasma" "rosácea" "psoríase" "dermatite"
                "manchas na pele" "queda de cabelo" "unhas frágeis"
                "envelhecimento da pele" "cicatrizes de acne"]
     :monthly-volume-range [1000 50000]
     :competition :medium
     :intent :informational}

    :procedures
    {:keywords ["peeling químico" "laser fracionado" "microagulhamento"
                "preenchimento facial" "toxina botulínica"
                "radiofrequência" "luz pulsada" "criolipólise"]
     :monthly-volume-range [500 10000]
     :competition :high
     :intent :commercial}}

   :psychology
   {:primary
    {:keywords ["psicólogo" "terapia ansiedade" "psicoterapia"
                "consulta psicológica" "tratamento depressão"]
     :monthly-volume-range [5000 50000]
     :competition :medium
     :cpc-range [3.00 12.00]}

    :secondary
    {:keywords ["psicólogo clínico" "terapia cognitivo comportamental"
                "psicólogo adulto" "consultório psicológico"
                "sessão psicoterapia"]
     :monthly-volume-range [1000 10000]
     :competition :medium
     :cpc-range [2.50 10.00]}

    :long-tail
    {:keywords ["melhor psicólogo para ansiedade [CIDADE]"
                "terapia para depressão [BAIRRO]"
                "psicólogo convênio [CONVENIO]"
                "quanto custa sessão psicólogo [CIDADE]"
                "psicólogo online para ansiedade"]
     :monthly-volume-range [10 1000]
     :competition :low
     :cpc-range [2.00 8.00]}

    :conditions
    {:keywords ["ansiedade" "depressão" "estresse" "burnout" "pânico"
                "fobia" "TOC" "trauma" "luto" "relacionamento"
                "autoestima" "insônia" "transtorno alimentar"]
     :monthly-volume-range [5000 100000]
     :competition :medium
     :intent :informational}

    :approaches
    {:keywords ["TCC" "psicanálise" "terapia de casal" "terapia familiar"
                "EMDR" "ACT" "gestalt-terapia" "terapia humanista"]
     :monthly-volume-range [100 5000]
     :competition :low
     :intent :commercial}}

   :nutrition
   {:primary
    {:keywords ["nutricionista" "dieta emagrecimento"
                "consulta nutricional" "plano alimentar"
                "nutrição esportiva"]
     :monthly-volume-range [5000 50000]
     :competition :medium
     :cpc-range [3.00 10.00]}

    :secondary
    {:keywords ["nutricionista clínico" "reeducação alimentar"
                "dieta personalizada" "nutrição funcional"
                "consultório nutrição"]
     :monthly-volume-range [1000 10000]
     :competition :medium
     :cpc-range [2.50 8.00]}

    :long-tail
    {:keywords ["nutricionista para diabetes [CIDADE]"
                "dieta para perder peso [BAIRRO]"
                "nutricionista convênio [CONVENIO]"
                "consulta nutricional online"
                "nutricionista especialista em [CONDICAO]"]
     :monthly-volume-range [10 1000]
     :competition :low
     :cpc-range [2.00 7.00]}

    :conditions
    {:keywords ["diabetes" "obesidade" "hipertensão" "colesterol alto"
                "intestino preso" "ganho de massa" "emagrecimento"
                "nutrição na gestação" "nutrição infantil"]
     :monthly-volume-range [1000 50000]
     :competition :medium
     :intent :informational}

    :goals
    {:keywords ["perder peso" "ganhar massa muscular" "dieta detox"
                "alimentação saudável" "cardápio fitness"
                "dieta low carb" "jejum intermitente" "dieta cetogênica"]
     :monthly-volume-range [5000 100000]
     :competition :high
     :intent :commercial}}})

(def geographic-modifiers
  {:city
   {:type :primary
    :importance :critical
    :examples ["São Paulo" "Rio de Janeiro" "Brasília" "Salvador"
               "Belo Horizonte" "Curitiba" "Porto Alegre" "Recife"]
    :pattern "[KEYWORD] [CIDADE]"}

   :neighborhood
   {:type :secondary
    :importance :high
    :examples ["Ipanema" "Vila Madalena" "Asa Norte" "Barra"
               "Savassi" "Batel" "Moinhos de Vento" "Boa Viagem"]
    :pattern "[KEYWORD] [BAIRRO]"}

   :region
   {:type :tertiary
    :importance :medium
    :examples ["Zona Sul" "Zona Oeste" "Grande São Paulo"
               "Região Metropolitana" "Centro"]
    :pattern "[KEYWORD] [REGIAO]"}

   :proximity
   {:type :long-tail
    :importance :medium
    :examples ["próximo a" "perto de" "região de" "nas proximidades"]
    :pattern "[KEYWORD] próximo [LANDMARK]"}})

(def temporal-modifiers
  {:urgency
   {:keywords ["urgente" "emergência" "hoje" "agora" "imediato"
               "rápido" "disponível agora"]
    :conversion-boost 2.5
    :compliance-warning "Must include emergency disclaimers"}

   :flexibility
   {:keywords ["fim de semana" "sábado" "domingo" "feriado"
               "noite" "horário estendido" "madrugada"]
    :conversion-boost 1.8
    :competitive-advantage :high}

   :scheduling
   {:keywords ["agendar" "marcar" "consulta" "horário disponível"
               "próxima vaga" "encaixe"]
    :conversion-boost 2.0
    :intent :transactional}})

(def convenience-modifiers
  {:digital
   {:keywords ["online" "telemedicina" "teleconsulta" "virtual"
               "remoto" "por vídeo" "via internet"]
    :growth-trend :increasing
    :post-pandemic-boost :significant}

   :accessibility
   {:keywords ["acessível" "cadeirante" "rampa" "elevador"
               "estacionamento" "fácil acesso"]
    :differentiation :strong
    :ethical-importance :high}

   :comfort
   {:keywords ["domiciliar" "em casa" "home care" "mobile"
               "atendimento a domicílio"]
    :premium-positioning true
    :price-sensitivity :low}})

(def price-modifiers
  {:cost-inquiry
   {:keywords ["preço" "valor" "custo" "quanto custa"
               "tabela de preços" "orçamento"]
    :intent :commercial
    :compliance-note "Cannot guarantee prices without evaluation"}

   :value-positioning
   {:keywords ["barato" "acessível" "em conta" "promoção"
               "desconto" "preço justo" "bom preço"]
    :competitive-risk :high
    :cfm-warning "Avoid competing on price alone - violates medical ethics"}

   :insurance
   {:keywords ["convênio" "plano de saúde" "aceita convênio"
               "Unimed" "Amil" "SulAmérica" "Bradesco Saúde"]
    :conversion-critical true
    :search-volume :very-high}

   :payment
   {:keywords ["particular" "privado" "cartão" "parcelado"
               "boleto" "PIX" "formas de pagamento"]
    :practical-importance :high
    :transparency-value :high}})

(defn generate-keyword-combinations
  "Generate keyword combinations for healthcare SEO"
  [specialty location options]
  (let [base-keywords (get-in specialty-keywords [specialty :primary :keywords])
        geo-modifier (get geographic-modifiers (:geo-type options))
        temporal (when (:include-temporal? options)
                   (get temporal-modifiers :urgency))
        convenience (when (:include-convenience? options)
                     (get convenience-modifiers :digital))]
    (for [keyword base-keywords
          :let [combinations [(str keyword " " location)]
                with-temporal (when temporal
                               (map #(str keyword " " % " " location)
                                    (:keywords temporal)))
                with-convenience (when convenience
                                  (map #(str keyword " " % " " location)
                                       (:keywords convenience)))]]
      (concat combinations with-temporal with-convenience))))

(defn calculate-keyword-priority
  "Calculate keyword priority score based on multiple factors"
  [keyword-data]
  (let [volume-score (normalize-volume (:search-volume keyword-data))
        competition-score (- 1.0 (:competition-level keyword-data))
        intent-score (get {:transactional 1.0
                          :commercial 0.8
                          :navigational 0.6
                          :informational 0.4}
                         (:intent keyword-data))
        conversion-score (or (:conversion-boost keyword-data) 1.0)]
    (* volume-score competition-score intent-score conversion-score)))
```

## 📝 Professional Content Templates

### Template 1: Educational Article (Artigo Educativo)

```clojure
(ns lab.seo.healthcare.templates.article
  "SEO-optimized educational article template")

(def article-structure
  {:metadata
   {:title-format "[CONDITION/TREATMENT]: [BENEFIT] - [SPECIALTY] [CITY]"
    :title-length [50 60]
    :meta-description-format "[HOOK]. [CREDENTIAL]. [CTA]. [CITY]."
    :meta-description-length [150 160]
    :url-format "/blog/[specialty]/[condition-slug]"
    :canonical true
    :schema-type "MedicalWebPage"}

   :hero-section
   {:h1-title {:format "[PRIMARY_KEYWORD]: O Que Você Precisa Saber"
               :length [40 60]
               :keyword-placement :beginning}
    :hook {:word-count [100 150]
           :elements [:emotional-connection :problem-identification
                      :solution-preview :credibility-signal]}
    :featured-image {:alt-text-format "[KEYWORD] - [SPECIALTY] em [CITY]"
                     :dimensions [1200 630]
                     :schema-required true}}

   :introduction
   {:word-count [150 200]
    :components
    [{:element :attention-hook
      :purpose "Capture reader interest immediately"
      :example "Você sabia que 85% das pessoas com acne podem alcançar pele limpa com tratamento adequado?"}

     {:element :problem-statement
      :purpose "Identify reader's pain point"
      :example "A acne não é apenas uma questão estética - afeta autoestima, relacionamentos e qualidade de vida."}

     {:element :solution-introduction
      :purpose "Present solution overview"
      :example "Felizmente, avanços em dermatologia oferecem tratamentos eficazes e personalizados."}

     {:element :credibility-establishment
      :purpose "Build trust with credentials"
      :example "Como dermatologista há 15 anos e membro da Sociedade Brasileira de Dermatologia, tenho ajudado centenas de pacientes a superar este desafio."}]}

   :main-content
   {:structure
    [{:section-type :what-is-condition
      :h2-format "O Que É [CONDITION]?"
      :word-count [200 300]
      :includes [:definition :causes :types :prevalence]
      :keyword-density 0.02
      :internal-links 2}

     {:section-type :symptoms
      :h2-format "Sintomas e Sinais de [CONDITION]"
      :word-count [200 250]
      :format :bullet-list
      :includes [:common-symptoms :warning-signs :when-to-seek-help]
      :keyword-variants [:secondary]}

     {:section-type :diagnosis
      :h2-format "Como É Feito o Diagnóstico"
      :word-count [150 200]
      :includes [:examination-process :diagnostic-tests :professional-role]
      :credibility-boosters [:clinical-experience :scientific-approach]}

     {:section-type :treatment-options
      :h2-format "Opções de Tratamento para [CONDITION]"
      :word-count [400 500]
      :subsections
      [{:h3-format "Tratamento [OPTION_1]"
        :word-count [100 150]
        :includes [:how-it-works :benefits :considerations :evidence]}
       {:h3-format "Tratamento [OPTION_2]"
        :word-count [100 150]
        :includes [:how-it-works :benefits :considerations :evidence]}
       {:h3-format "Tratamento [OPTION_3]"
        :word-count [100 150]
        :includes [:how-it-works :benefits :considerations :evidence]}]
      :scientific-references 3}

     {:section-type :prevention
      :h2-format "Prevenção e Cuidados"
      :word-count [150 200]
      :format :numbered-list
      :actionable true
      :practical-tips 5}

     {:section-type :professional-role
      :h2-format "A Importância do Acompanhamento [SPECIALTY]"
      :word-count [150 200]
      :cta-preparation true
      :benefits-of-consultation 4}]}

   :faq-section
   {:h2-title "Perguntas Frequentes sobre [CONDITION]"
    :schema-type "FAQPage"
    :question-count [5 7]
    :question-format
    [{:question "Qual o melhor tratamento para [CONDITION]?"
      :answer-length [80 120]
      :keyword-rich true
      :cta-soft true}

     {:question "Quanto tempo dura o tratamento de [CONDITION]?"
      :answer-length [80 120]
      :realistic-expectations true}

     {:question "O tratamento para [CONDITION] é coberto pelo convênio?"
      :answer-length [60 100]
      :practical-information true}

     {:question "[CONDITION] tem cura?"
      :answer-length [100 150]
      :scientific-accuracy :critical
      :manage-expectations true}

     {:question "Quando devo procurar um [SPECIALTY]?"
      :answer-length [80 120]
      :urgency-indicators true
      :cta-natural true}]}

   :about-author
   {:h2-title "Sobre o [SPECIALTY]"
    :word-count [200 300]
    :components
    [{:element :name-and-credentials
      :format "[DR/DRA NAME] - [CREDENTIALS]"}
     {:element :qualifications
      :items [:education :certifications :memberships]}
     {:element :experience
      :years-practicing true
      :specializations true
      :patient-testimonial-count true}
     {:element :differentiators
      :unique-approaches 3}
     {:element :professional-registration
      :format "CRM/CRP [NUMBER]"
      :compliance-required true}]}

   :conclusion-cta
   {:h2-title "Próximos Passos"
    :word-count [150 200]
    :components
    [{:element :summary
      :key-points 3}
     {:element :action-encouragement
      :tone :professional-but-warm}
     {:element :contact-methods
      :options [:phone :whatsapp :online-booking :email]
      :visibility :prominent}
     {:element :location-mention
      :format "Atendimento em [NEIGHBORHOOD], [CITY]"}
     {:element :insurance-mention
      :if-applicable true}]}

   :disclaimers
   {:position :top-and-bottom
    :required
    [{:type :cfm-general
      :condition (fn [content] (medical-content? content))}
     {:type :crp-general
      :condition (fn [content] (psychological-content? content))}
     {:type :emergency-warning
      :condition (fn [_] true)}
     {:type :results-disclaimer
      :condition (fn [content] (mentions-outcomes? content))}]}

   :seo-elements
   {:keyword-density
    {:primary 0.02
     :secondary 0.015
     :related 0.01}

    :internal-linking
    {:minimum 3
     :types [:related-conditions :treatment-pages :about-page]}

    :external-linking
    {:scientific-references {:minimum 3 :sources [:pubmed :scielo :cochrane]}
     :authority-sites {:minimum 1 :sources [:medical-societies :government]}}

    :multimedia
    {:images {:minimum 3
              :alt-text-keyword-rich true
              :file-naming-seo true}
     :infographics {:recommended 1
                    :original-content-value :high}
     :videos {:optional true
              :youtube-embed-optimized true}}

    :schema-markup
    {:required [:MedicalWebPage :Article :Person :FAQPage]
     :recommended [:BreadcrumbList :Organization]}}})

(defn generate-article
  "Generate SEO-optimized healthcare article from template"
  [topic specialty location credentials]
  (let [keyword-research (research-keywords topic specialty location)
        content-outline (build-outline article-structure keyword-research)
        seo-metadata (generate-metadata topic specialty location)
        compliance-elements (select-disclaimers topic specialty)]
    {:metadata seo-metadata
     :outline content-outline
     :keywords keyword-research
     :disclaimers compliance-elements
     :schema-markup (generate-schema topic specialty credentials location)
     :word-count-target (calculate-target-word-count topic)
     :internal-links (suggest-internal-links topic)
     :external-references (find-scientific-references topic)}))
```

### Template 2: Service Page (Página de Serviço)

```clojure
(ns lab.seo.healthcare.templates.service
  "SEO-optimized service/treatment page template")

(def service-page-structure
  {:metadata
   {:title-format "[TREATMENT/SERVICE] em [CITY] - [DR NAME] [SPECIALTY]"
    :title-length [50 60]
    :meta-description-format "[TREATMENT]: [BENEFIT]. [CREDENTIAL]. Agende: [PHONE]. [CITY]."
    :meta-description-length [150 160]
    :url-format "/servicos/[service-slug]"
    :schema-type "MedicalProcedure"}

   :hero-section
   {:h1-title {:format "[TREATMENT/SERVICE] em [CITY]"
               :length [40 60]
               :primary-keyword true}
    :subtitle {:format "Com [DR NAME], [SPECIALTY] [CREDENTIALS]"
               :credibility-focus true}
    :hero-image {:type :professional-or-treatment
                 :alt-format "[TREATMENT] - [SPECIALTY] em [CITY]"
                 :dimensions [1920 1080]}
    :primary-cta {:text "Agendar Consulta"
                  :prominence :maximum
                  :above-fold true
                  :tracking :conversion-primary}}

   :value-proposition
   {:word-count [150 200]
    :components
    [{:element :main-benefit
      :emphasis :strong
      :example "Recupere a saúde da sua pele com tratamento personalizado e baseado em evidências científicas."}

     {:element :differentiators
      :format :bullet-list
      :count 4
      :examples ["15 anos de experiência em dermatologia"
                 "Equipamentos de última geração"
                 "Protocolos individualizados"
                 "Acompanhamento contínuo"]}

     {:element :social-proof
      :types [:patient-count :experience-years :certifications]
      :example "Mais de 1.000 pacientes atendidos"}]}

   :about-treatment
   {:h2-title "O Que É [TREATMENT]"
    :word-count [200 300]
    :components
    [{:subsection :definition
      :h3-title "Entenda o [TREATMENT]"
      :word-count [100 150]
      :accessibility :layman-terms
      :keyword-density 0.025}

     {:subsection :how-it-works
      :h3-title "Como Funciona"
      :word-count [150 200]
      :include-diagram true
      :step-by-step true}

     {:subsection :benefits
      :h3-title "Benefícios do [TREATMENT]"
      :format :numbered-list
      :count [5 7]
      :evidence-based true
      :realistic-expectations true}

     {:subsection :ideal-candidates
      :h3-title "Para Quem É Indicado"
      :word-count [100 150]
      :inclusion-criteria true
      :qualification-cta true}]}

   :treatment-process
   {:h2-title "Como É o Processo de Tratamento"
    :word-count [300 400]
    :visual :timeline-or-steps
    :steps
    [{:step 1
      :title "Consulta Inicial"
      :description [100 150]
      :includes [:evaluation :medical-history :expectations :treatment-plan]}

     {:step 2
      :title "Preparação"
      :description [80 120]
      :includes [:pre-treatment-care :medications :skincare-routine]}

     {:step 3
      :title "Procedimento"
      :description [100 150]
      :includes [:duration :comfort-measures :what-to-expect]}

     {:step 4
      :title "Pós-Tratamento"
      :description [100 150]
      :includes [:immediate-care :restrictions :normal-reactions]}

     {:step 5
      :title "Acompanhamento"
      :description [80 120]
      :includes [:follow-up-schedule :progress-evaluation :adjustments]}]
    :conversion-element {:position :after-steps
                        :cta "Agende Sua Consulta Inicial"}}

   :expected-results
   {:h2-title "Resultados Esperados"
    :word-count [200 300]
    :components
    [{:element :timeline
      :format :visual-timeline
      :milestones ["Imediato" "1 semana" "1 mês" "3 meses" "6 meses"]}

     {:element :realistic-outcomes
      :emphasis :managing-expectations
      :scientific-backing true}

     {:element :individual-variation
      :disclaimer-integrated true
      :factors [:age :condition-severity :adherence :lifestyle]}

     {:element :before-after
      :if-allowed-by-regulation true
      :anonymized true
      :disclaimer-prominent true}]}

   :professional-section
   {:h2-title "Sobre [DR NAME]"
    :word-count [250 350]
    :components
    [{:element :credentials
      :format :highlight-box
      :items [:name :title :registration-number :specialties]}

     {:element :qualifications
      :subsections
      [{:h3 "Formação Acadêmica"
        :institutions-degrees true}
       {:h3 "Especializações"
        :certifications-fellowships true}
       {:h3 "Sociedades Profissionais"
        :memberships true}]}

     {:element :experience
      :metrics [:years-practicing :patients-treated
                :procedures-performed :research-publications]}

     {:element :philosophy
      :word-count [100 150]
      :humanization true
      :patient-centered-approach true}

     {:element :photo
      :professional-headshot true
      :alt-text "[DR NAME] - [SPECIALTY] em [CITY]"}]}

   :faq-section
   {:h2-title "Perguntas Frequentes"
    :schema "FAQPage"
    :questions [5 7]
    :categories
    [{:category :practical
      :questions
      ["Quanto tempo dura o [TREATMENT]?"
       "O [TREATMENT] dói?"
       "Quantas sessões são necessárias?"
       "Qual o valor do [TREATMENT]?"]}

     {:category :safety
      :questions
      ["O [TREATMENT] é seguro?"
       "Quais os efeitos colaterais?"
       "Existe contraindicação?"
       "Como é a recuperação?"]}

     {:category :results
      :questions
      ["Quando vou ver resultados?"
       "Os resultados são permanentes?"
       "O que fazer para manter os resultados?"]}

     {:category :logistics
      :questions
      ["Preciso me preparar para o [TREATMENT]?"
       "Posso voltar ao trabalho no mesmo dia?"
       "O convênio cobre?"
       "Como agendar?"]}]}

   :location-section
   {:h2-title "Localização e Atendimento"
    :components
    [{:element :address
      :format :structured
      :schema "MedicalClinic"
      :includes [:street :neighborhood :city :state :zip :country]}

     {:element :map
      :type :google-maps-embed
      :optimized-for-local-seo true}

     {:element :access-info
      :parking true
      :public-transport true
      :accessibility-features true}

     {:element :hours
      :format :table
      :schema "OpeningHoursSpecification"}

     {:element :coverage-area
      :neighborhoods-served true
      :cities-served true
      :keyword-rich true}]}

   :final-cta
   {:h2-title "Agende Sua Consulta"
    :word-count [100 150]
    :urgency-elements
    [{:type :limited-availability
      :ethical-constraint :must-be-true}
     {:type :next-available-date
      :real-time-integration-recommended true}]

    :contact-options
    [{:method :phone
      :prominence :primary
      :click-to-call true}
     {:method :whatsapp
      :prominence :primary
      :direct-link true}
     {:method :online-booking
      :prominence :secondary
      :integration-required true}
     {:method :email
      :prominence :tertiary}]

    :social-proof
    {:patient-testimonials {:count [2 3]
                           :schema "Review"
                           :authentic true}
     :ratings {:if-available true
              :schema "AggregateRating"}}}

   :disclaimers
   {:required-disclaimers
    [:cfm-procedures :anvisa-procedures :results-disclaimer :emergency-warning]
    :position :top-and-bottom
    :visual-prominence :high}

   :seo-optimization
   {:keyword-placement
    {:h1 1
     :h2 [2 3]
     :h3 [1 2]
     :first-paragraph 1
     :last-paragraph 1
     :alt-texts :all-images}

    :schema-markup
    {:required [:MedicalProcedure :MedicalClinic :Physician]
     :recommended [:FAQPage :Review :AggregateRating :BreadcrumbList]}

    :internal-links
    {:minimum 5
     :targets [:related-treatments :conditions-treated :blog-posts :about-page]}

    :conversion-optimization
    {:cta-count [3 5]
     :cta-positions [:hero :after-value-prop :after-process
                     :after-faq :final-section]
     :cta-variety [:phone :whatsapp :form :booking]}}})

(defn generate-service-page
  "Generate SEO-optimized service page"
  [service-name specialty location doctor-profile]
  {:metadata (build-service-metadata service-name specialty location)
   :content (populate-service-template service-page-structure
                                       service-name
                                       specialty
                                       location
                                       doctor-profile)
   :schema (generate-service-schema service-name specialty location doctor-profile)
   :local-seo (optimize-local-seo location doctor-profile)
   :conversion-tracking (setup-conversion-tracking service-name)})
```

## 🌍 Local SEO Optimization

### Google Business Profile Optimization

```clojure
(ns lab.seo.healthcare.local
  "Local SEO optimization for healthcare professionals")

(def google-business-profile-optimization
  {:basic-information
   {:business-name {:format "[DR NAME] - [SPECIALTY]"
                    :avoid-keyword-stuffing true
                    :cfm-compliant true}
    :categories {:primary "[SPECIALTY] Category"
                 :secondary ["Medical Clinic" "Health Professional"]
                 :maximum 3}
    :description {:word-count [250 750]
                  :includes [:credentials :specialties :unique-value
                            :location :insurance :languages]
                  :keyword-natural true
                  :cta-soft true}}

   :contact-information
   {:phone {:type :local-number
            :availability true
            :verified true}
    :website {:https-required true
              :mobile-optimized true
              :fast-loading true}
    :address {:complete true
              :verified true
              :accessible-location true}}

   :hours-of-operation
   {:regular-hours {:accurate true
                    :updated-regularly true}
    :special-hours {:holidays true
                    :closures true
                    :extended-hours-highlighted true}}

   :photos
   {:profile-photo {:professional-headshot true
                    :high-quality true
                    :updated-annually true}
    :cover-photo {:brand-representative true
                  :dimensions [1024 576]}
    :interior {:clinic-photos 5
               :modern-clean-professional true}
    :exterior {:building-entrance true
               :parking-access true}
    :team {:if-applicable true
           :permissions-obtained true}
    :before-after {:if-regulation-allows true
                   :anonymized-properly true
                   :disclaimer-included true}}

   :services
   {:list-all-services true
    :detailed-descriptions true
    :keyword-rich true
    :treatment-specific true
    :condition-specific true}

   :attributes
   {:accessibility ["Wheelchair accessible"
                    "Accessible parking"
                    "Accessible entrance"]
    :amenities ["Free parking"
                "Wi-Fi"
                "Air conditioning"
                "Waiting area"]
    :languages ["Portuguese" "English" "Spanish"]
    :payment ["Credit cards"
              "Debit cards"
              "Insurance"
              "PIX"]
    :appointment ["Online appointments"
                  "Same-day appointments"
                  "Appointment required"]}

   :posts
   {:frequency :weekly
    :types [:update :event :offer :product]
    :content
    [{:type :educational
      :example "Você sabia? [Health Tip]"
      :frequency :weekly}
     {:type :service-highlight
      :example "Conheça nosso tratamento de [PROCEDURE]"
      :frequency :bi-weekly}
     {:type :patient-success
      :example "Como [Treatment] transformou a vida de nossos pacientes"
      :frequency :monthly
      :anonymized true}
     {:type :availability
      :example "Horários disponíveis esta semana"
      :frequency :weekly}]}

   :reviews
   {:strategy
    [{:action :request-reviews
      :timing :after-positive-outcome
      :method [:email :sms :in-person]
      :frequency :every-satisfied-patient}

     {:action :respond-all-reviews
      :timing :within-24-hours
      :tone :professional-grateful
      :address-concerns true}

     {:action :handle-negative-reviews
      :approach [:acknowledge :apologize :offer-resolution :take-offline]
      :cfm-compliance :maintain-patient-privacy}

     {:action :showcase-reviews
      :minimum-rating 4.5
      :review-count-target 50
      :schema-markup "AggregateRating"}]}

   :q-and-a
   {:monitor-questions true
    :respond-promptly true
    :add-faqs-proactively true
    :keyword-opportunities true}

   :insights-monitoring
   {:metrics
    [:search-queries :discovery-searches :direct-searches
     :views-maps :views-search :actions-website-clicks
     :actions-phone-calls :actions-direction-requests]
    :frequency :weekly
    :optimization-based-on-data true}})

(defn optimize-google-business-profile
  "Complete Google Business Profile optimization"
  [practice-data]
  {:profile-setup (setup-gbp-profile practice-data)
   :content-strategy (create-gbp-content-strategy practice-data)
   :review-management (implement-review-strategy practice-data)
   :performance-tracking (setup-gbp-tracking practice-data)
   :local-seo-boost (calculate-local-seo-score practice-data)})
```

### Local Citation Building

```clojure
(def local-citation-sources
  {:healthcare-specific
   [{:site "Doctoralia"
     :url "https://www.doctoralia.com.br/"
     :importance :critical
     :patient-reviews true
     :online-booking true}

    {:site "Consulta do Bem"
     :url "https://consultadobem.com.br/"
     :importance :high
     :social-impact true}

    {:site "ZocDoc (Doctoralia)"
     :url "https://www.zocdoc.com/"
     :importance :high
     :appointment-booking true}

    {:site "BoaConsulta"
     :url "https://www.boaconsulta.com/"
     :importance :high
     :telemedicine-integration true}]

   :general-directories
   [{:site "Google Business Profile"
     :importance :critical
     :primary-listing true}

    {:site "Facebook Business"
     :importance :high
     :social-proof true
     :patient-engagement true}

    {:site "Instagram Business"
     :importance :high
     :visual-content true
     :younger-demographic true}

    {:site "LinkedIn"
     :importance :medium
     :professional-networking true
     :credibility-building true}]

   :local-directories
   [{:site "Guia Mais"
     :importance :medium
     :local-search true}

    {:site "Apontador"
     :importance :medium
     :map-integration true}

    {:site "TeleListas"
     :importance :low
     :traditional-directory true}]

   :specialty-specific
   {:dermatology
    [{:site "Sociedade Brasileira de Dermatologia"
      :url "https://www.sbd.org.br/"
      :member-directory true
      :credibility :highest}]

    :psychology
    [{:site "Conselho Federal de Psicologia"
      :url "https://site.cfp.org.br/"
      :professional-registry true
      :credibility :highest}

     {:site "e-Psi"
      :url "http://epsi.cfp.org.br/"
      :online-therapy-directory true}]

    :nutrition
    [{:site "Conselho Federal de Nutricionistas"
      :url "http://www.cfn.org.br/"
      :professional-registry true
      :credibility :highest}]}}

(defn build-local-citations
  "Build and manage local citations"
  [practice-info specialty]
  (let [core-citations (get local-citation-sources :healthcare-specific)
        specialty-citations (get-in local-citation-sources
                                   [:specialty-specific specialty])
        general-citations (get local-citation-sources :general-directories)]
    {:priority-citations (concat core-citations specialty-citations)
     :secondary-citations general-citations
     :nap-consistency (validate-nap-consistency practice-info)
     :citation-audit (audit-existing-citations practice-info)
     :opportunities (identify-citation-opportunities specialty)}))
```

## 📊 Compliance-First SEO Strategy

### Ethical Content Marketing

```clojure
(ns lab.seo.healthcare.ethics
  "Ethical content marketing within regulatory constraints")

(def ethical-content-guidelines
  {:cfm-restrictions
   {:prohibited
    ["Guarantees of results"
     "Superlative claims (best, number one, etc.)"
     "Comparison with other professionals"
     "Before/after photos without context"
     "Promotional pricing"
     "Sensationalism"
     "Self-promotion beyond credentials"]

    :allowed
    ["Educational content"
     "Credential disclosure"
     "Treatment explanations"
     "Scientific information"
     "Patient testimonials (with consent)"
     "Professional experience"
     "Specialization areas"]}

   :crp-restrictions
   {:prohibited
    ["Promises of cure"
     "Guaranteed outcomes"
     "Diagnostic claims online"
     "Therapy without formal relationship"
     "Patient case details (without consent)"
     "Comparison of therapeutic approaches"]

    :allowed
    ["Psychoeducational content"
     "Mental health awareness"
     "When to seek help"
     "Treatment approach explanations"
     "Professional qualifications"
     "Therapy process overview"]}

   :anvisa-restrictions
   {:prohibited
    ["Medication recommendations without prescription"
     "Off-label use suggestions"
     "Product guarantees"
     "Medical device claims beyond approved"
     "Supplement medical claims"]

    :allowed
    ["Educational medication information"
     "Approved indications"
     "General safety information"
     "When to consult professional"]}})

(defn validate-content-ethics
  "Validate content against ethical guidelines"
  [content specialty]
  (let [restrictions (get ethical-content-guidelines
                         (specialty-to-council specialty))
        prohibited-patterns (:prohibited restrictions)
        violations (detect-violations content prohibited-patterns)]
    {:compliant? (empty? violations)
     :violations violations
     :recommendations (generate-ethical-alternatives violations)
     :approval-status (if (empty? violations) :approved :needs-revision)}))
```

## 🔗 Related Skills

- [`cva-healthcare-compliance`](../cva-healthcare-compliance/SKILL.md) - LGPD and regulatory compliance (USE THIS FIRST)
- [`cva-concepts-agent-types`](../cva-concepts-agent-types/SKILL.md) - Agent type selection for SEO workflows
- [`cva-overview`](../cva-overview/SKILL.md) - Clojure Vertex AI ADK overview
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Google Cloud Vertex AI setup

## 📘 SEO and Marketing Resources

### Healthcare Marketing Regulations
- **CFM Resolution 1974/2011**: Medical advertising and online presence guidelines
- **CRP Resolution 11/2018**: Psychology professional online communication ethics
- **ANVISA RDC 96/2008**: Regulations for health services advertising

### SEO Tools for Healthcare
- **Google Search Console**: [https://search.google.com/search-console](https://search.google.com/search-console)
- **Google Business Profile**: [https://business.google.com/](https://business.google.com/)
- **Google Keyword Planner**: Keyword research for healthcare terms
- **SEMrush / Ahrefs**: Competitive analysis and keyword tracking
- **Schema.org Medical Schemas**: [https://schema.org/MedicalEntity](https://schema.org/MedicalEntity)

### Local SEO Resources
- **Moz Local SEO Guide**: Best practices for local search optimization
- **BrightLocal**: Local citation and review management
- **Whitespark**: Local citation building and tracking

## ⚠️ Critical Compliance Notes

1. **Always use with compliance skill** - Never implement SEO without checking [`cva-healthcare-compliance`](../cva-healthcare-compliance/SKILL.md) first
2. **No guarantee claims** - Never promise specific results or use superlatives
3. **Credential verification** - Always validate professional registrations before publication
4. **Disclaimer integration** - SEO content must include all required disclaimers
5. **Scientific backing** - All claims must be supported by evidence
6. **Patient privacy** - Testimonials and case studies require explicit consent and anonymization
7. **Ethical pricing** - Avoid competing on price alone - focus on value and expertise
