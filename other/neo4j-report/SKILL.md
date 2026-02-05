---
name: neo4j-report
description: Query SEC filings (8-K, 10-K, 10-Q), extracted sections, exhibits, and financial statements from Neo4j. Use when fetching report/filing data.
---

# Neo4j Report Queries

Queries for Report nodes and related content (sections, exhibits, financial statements).

## Report Content Labels
| Label | Count | Key properties | Relationship |
|-------|-------|----------------|--------------|
| **ExtractedSectionContent** | 157,841 | `content`, `section_name`, `filing_id` | Report-[:HAS_SECTION]-> |
| **ExhibitContent** | 30,812 | `content`, `exhibit_number`, `filing_id` | Report-[:HAS_EXHIBIT]-> |
| **FinancialStatementContent** | 31,312 | `value`, `statement_type`, `filing_id` | Report-[:HAS_FINANCIAL_STATEMENT]-> |
| **FilingTextContent** | 1,908 | `content`, `filing_id` | Report-[:HAS_FILING_TEXT]-> |
| **AdminReport** | 16 | `id` | Report-[:IN_CATEGORY]-> |

## Basic Report Queries

### Latest report for company
```cypher
MATCH (c:Company {ticker: $ticker})<-[:PRIMARY_FILER]-(r:Report)
RETURN r ORDER BY r.created DESC LIMIT 1
```

### Reports by form type
```cypher
MATCH (r:Report {formType: $form_type})-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
RETURN r.id, r.accessionNo, r.created, r.periodOfReport
ORDER BY r.created DESC
LIMIT 10
```

### Reports in date range
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.created >= $start_date AND r.created < $end_date
RETURN r.id, r.formType, r.created, r.items
ORDER BY r.created DESC
```

## 8-K Earnings Filings

### 8-K Item 2.02 filings for company
```cypher
MATCH (r:Report {formType: '8-K'})-[pf:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.items CONTAINS 'Item 2.02'
RETURN r.id, r.created, r.market_session,
       pf.daily_stock, pf.daily_macro,
       round((pf.daily_stock - pf.daily_macro) * 100) / 100 AS daily_adj
ORDER BY r.created DESC
```

### Top earnings movers in date range
```cypher
MATCH (r:Report {formType: '8-K'})-[pf:PRIMARY_FILER]->(c:Company)
WHERE r.items CONTAINS 'Item 2.02'
  AND r.created >= $start_date AND r.created < $end_date
  AND pf.daily_stock IS NOT NULL AND NOT isNaN(pf.daily_stock)
RETURN c.ticker, r.id, r.created,
       round((pf.daily_stock - pf.daily_macro) * 100) / 100 AS daily_adj
ORDER BY abs(pf.daily_stock - pf.daily_macro) DESC
LIMIT 10
```

### 8-K with specific item
```cypher
MATCH (r:Report {formType: '8-K'})-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.items CONTAINS $item_code  // e.g., 'Item 1.01', 'Item 5.02'
RETURN r.id, r.created, r.items
ORDER BY r.created DESC
```

## Report Content

### Press release (Exhibit EX-99.1)
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_EXHIBIT]->(e:ExhibitContent)
WHERE e.exhibit_number = 'EX-99.1'
RETURN e.content
```

### All exhibits for report
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_EXHIBIT]->(e:ExhibitContent)
RETURN e.exhibit_number, substring(e.content, 0, 500) AS preview
ORDER BY e.exhibit_number
```

### Extracted sections (narrative)
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_SECTION]->(s:ExtractedSectionContent)
RETURN s.section_name, s.content
```

### Financial statement content
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_FINANCIAL_STATEMENT]->(fs:FinancialStatementContent)
RETURN fs.statement_type, fs.value
```

### Filing text content
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_FILING_TEXT]->(ft:FilingTextContent)
RETURN ft.form_type, ft.content
```

## 10-K/10-Q Section Queries

### Financial Statements (Narrative)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name IN ['FinancialStatements', 'FinancialStatementsandSupplementaryData']
RETURN c.ticker, r.formType, substring(esc.content, 0, 2000) as financial_text,
       size(esc.content) as content_size
ORDER BY r.created DESC
LIMIT 10
```

### Management Discussion & Analysis (MD&A)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name IN ['ManagementDiscussionandAnalysisofFinancialConditionandResultsofOperations',
                           'Management\'sDiscussionandAnalysisofFinancialConditionandResultsofOperations']
RETURN c.ticker, r.formType, substring(esc.content, 0, 3000) as mda_text
ORDER BY r.created DESC
LIMIT 10
```

### Risk Factors
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'RiskFactors'
RETURN c.ticker, r.formType, substring(esc.content, 0, 3000) as risk_factors
ORDER BY r.created DESC
LIMIT 10
```

### Cybersecurity Disclosures (Item 1C)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'Cybersecurity'
RETURN c.ticker, r.formType, substring(esc.content, 0, 2000) as cyber_disclosure
ORDER BY r.created DESC
LIMIT 10
```

### Business Description (10-K)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '10-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'Business'
RETURN c.ticker, substring(esc.content, 0, 3000) as business_description
ORDER BY r.created DESC
LIMIT 10
```

### Properties
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'Properties'
RETURN c.ticker, r.formType, substring(esc.content, 0, 1500) as properties_info
ORDER BY r.created DESC
LIMIT 10
```

### Legal Proceedings
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'LegalProceedings'
RETURN c.ticker, r.formType, substring(esc.content, 0, 2000) as legal_matters
ORDER BY r.created DESC
LIMIT 20
```

### Controls and Procedures
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'ControlsandProcedures'
RETURN c.ticker, r.formType, substring(esc.content, 0, 1500) as controls_info
ORDER BY r.created DESC
LIMIT 10
```

### Executive Compensation
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'ExecutiveCompensation'
RETURN c.ticker, r.formType, substring(esc.content, 0, 2000) as compensation_info
ORDER BY r.created DESC
LIMIT 10
```

### Directors and Corporate Governance
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'Directors,ExecutiveOfficersandCorporateGovernance'
RETURN c.ticker, r.formType, substring(esc.content, 0, 1500) as governance_info
ORDER BY r.created DESC
LIMIT 10
```

## ExhibitContent Queries

### Press Releases (EX-99.1)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_EXHIBIT]->(ec:ExhibitContent)
WHERE ec.exhibit_number = 'EX-99.1'
RETURN c.ticker, r.formType, substring(ec.content, 0, 2000) as press_release, r.created
ORDER BY r.created DESC
LIMIT 20
```

### Material Contracts (EX-10.x)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_EXHIBIT]->(ec:ExhibitContent)
WHERE ec.exhibit_number STARTS WITH 'EX-10.'
RETURN c.ticker, r.formType, ec.exhibit_number,
       substring(ec.content, 0, 1500) as contract_excerpt, r.created
ORDER BY r.created DESC
LIMIT 20
```

### Presentations (EX-99.2)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_EXHIBIT]->(ec:ExhibitContent)
WHERE ec.exhibit_number = 'EX-99.2'
RETURN c.ticker, r.formType, substring(ec.content, 0, 1500) as presentation_content, r.created
ORDER BY r.created DESC
LIMIT 20
```

### Search Within Exhibits (Fulltext)
```cypher
CALL db.index.fulltext.queryNodes('exhibit_content_ft', $search_term)
YIELD node, score
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {id: node.filing_id})
RETURN c.ticker, r.formType, node.exhibit_number,
       substring(node.content, 0, 1000) as matching_excerpt, r.created, score
ORDER BY score DESC
LIMIT 20
```

## Data Inventory Query

Run first to know what data exists for a company in a date range:

```cypher
MATCH (c:Company {ticker: $ticker})
OPTIONAL MATCH (r:Report {formType: '8-K'})-[:PRIMARY_FILER]->(c)
  WHERE r.items CONTAINS 'Item 2.02' AND r.created >= $start_date AND r.created <= $end_date
OPTIONAL MATCH (n:News)-[:INFLUENCES]->(c)
  WHERE n.created >= $start_date AND n.created <= $end_date
OPTIONAL MATCH (t:Transcript)-[:INFLUENCES]->(c)
  WHERE t.conference_datetime >= $start_date AND t.conference_datetime <= $end_date
OPTIONAL MATCH (xr:Report)-[:PRIMARY_FILER]->(c)
  WHERE xr.formType IN ['10-K', '10-Q']
OPTIONAL MATCH (c)-[:DECLARED_DIVIDEND]->(div:Dividend)
  WHERE div.declaration_date >= $start_date AND div.declaration_date <= $end_date
OPTIONAL MATCH (c)-[:DECLARED_SPLIT]->(sp:Split)
  WHERE sp.execution_date >= $start_date AND sp.execution_date <= $end_date
RETURN c.ticker, c.name,
       count(DISTINCT r) AS reports_8k,
       count(DISTINCT n) AS news_count,
       count(DISTINCT t) AS transcript_count,
       count(DISTINCT xr) AS xbrl_reports,
       count(DISTINCT div) AS dividends,
       count(DISTINCT sp) AS splits
```

## Fulltext Search

### Search extracted sections
```cypher
CALL db.index.fulltext.queryNodes('extracted_section_content_ft', $query)
YIELD node, score
RETURN node.section_name, node.filing_id, substring(node.content, 0, 300), score
ORDER BY score DESC
LIMIT 20
```

### Search exhibits
```cypher
CALL db.index.fulltext.queryNodes('exhibit_content_ft', $query)
YIELD node, score
RETURN node.exhibit_number, node.filing_id, substring(node.content, 0, 300), score
ORDER BY score DESC
LIMIT 20
```

## SEC Item Codes (8-K)

`Report.items` contains SEC Item codes. Common codes:

| Item | Name | Data Location | Notes |
|------|------|---------------|-------|
| 2.02 | Results of Operations | **EX-99.1** (94%) | Earnings - real data in exhibit |
| 7.01 | Regulation FD | **EX-99.1** (85%) | Disclosure materials |
| 1.01 | Material Agreement | **EX-10.x** (69%) | Contracts in exhibit |
| 8.01 | Other Events | Check both (64%) | Varies |
| 5.02 | Personnel Changes | Check both (57%) | Officer appointments |
| 5.07 | Voting Results | **Section** (79%) | Data in section itself |
| 2.06 | Material Impairments | **Section** (64%) | Data in section itself |

**Key insight**: Sections are often pointers (1.4KB avg) → Exhibits have real data (49KB avg).

## 8-K Content Structure

### Content Distribution (23,836 8-K reports)
- **67% have BOTH section + exhibit**: Section is a pointer → Exhibit has real data
- **33% have section only**: Data embedded directly in section
- **2% fallback**: FilingTextContent (690KB avg) when parsing fails

### Exhibit Types
| Type | % | Purpose | Used With |
|------|---|---------|-----------|
| **EX-99.x** | 84% | Press releases, presentations | Item 2.02, 7.01, 8.01 |
| **EX-10.x** | 16% | Material contracts, agreements | Item 1.01, 5.02 |

### Section Name → Item Code Mapping
The `section_name` field stores SEC section names without spaces. Map to Item codes:

| section_name | Item | % of 8-Ks |
|--------------|------|-----------|
| `FinancialStatementsandExhibits` | 9.01 | 79% |
| `ResultsofOperationsandFinancialCondition` | 2.02 | 36% |
| `RegulationFDDisclosure` | 7.01 | 24% |
| `DepartureofDirectorsorCertainOfficers...` | 5.02 | 21% |
| `OtherEvents` | 8.01 | 20% |
| `EntryintoaMaterialDefinitiveAgreement` | 1.01 | 11% |
| `SubmissionofMatterstoaVoteofSecurityHolders` | 5.07 | 10% |
| `CreationofaDirectFinancialObligation...` | 2.03 | 6% |
| `MaterialImpairments` | 2.06 | 0.2% |
| `MaterialCybersecurityIncidents` | 1.05 | 0.1% |

### Extraction Strategy by Item
```
EXHIBIT-FIRST (check EX-99.1/EX-10.x first):
  Item 2.02 (94%), Item 7.01 (85%), Item 1.01 (69%)

CHECK BOTH (data may be in either):
  Item 8.01 (64% exhibit), Item 5.02 (57% exhibit)

SECTION-FIRST (data usually in section itself):
  Item 5.07 (79% section), Item 2.06 (64% section)
```

## Data Analysis

### Return data coverage in PRIMARY_FILER
```cypher
MATCH ()-[pf:PRIMARY_FILER]->()
WITH COUNT(*) as total,
     COUNT(pf.daily_stock) as has_daily_stock,
     COUNT(pf.hourly_stock) as has_hourly_stock,
     COUNT(pf.session_stock) as has_session_stock
RETURN total,
       ROUND(100.0 * has_daily_stock / total) as daily_coverage,
       ROUND(100.0 * has_hourly_stock / total) as hourly_coverage,
       ROUND(100.0 * has_session_stock / total) as session_coverage
```

### 10-Q filings with negative market reactions
```cypher
MATCH (c:Company)<-[pf:PRIMARY_FILER]-(r:Report)
WHERE r.formType = '10-Q' AND pf.daily_stock < -2.0
  AND datetime(r.created) > datetime() - duration('P90D')
RETURN c.ticker, r.created, r.formType, pf.daily_stock, pf.daily_industry, pf.daily_sector, pf.daily_macro
ORDER BY pf.daily_stock LIMIT 20
```

### Find amended reports
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)
WHERE r.isAmendment = true
RETURN c.ticker, r.formType, r.created, r.description
ORDER BY r.created DESC LIMIT 20
```

### Amended reports with descriptions
```cypher
MATCH (r:Report)
WHERE r.isAmendment = true AND r.description IS NOT NULL
RETURN r.accessionNo, r.formType, r.description, r.created
ORDER BY r.created DESC LIMIT 20
```

### Companies with recent 10-K filings
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)
WHERE r.formType = '10-K' AND datetime(r.created) > datetime() - duration('P120D')
RETURN c.ticker, r.created, r.accessionNo
ORDER BY r.created DESC LIMIT 20
```

### Recent 10-K reports and stock impact
```cypher
MATCH (c:Company)<-[pf:PRIMARY_FILER]-(r:Report)
WHERE r.formType = '10-K' AND datetime(r.created) > datetime() - duration('P180D')
  AND pf.daily_stock IS NOT NULL
RETURN c.ticker, r.created, r.accessionNo,
       pf.daily_stock as daily_return, pf.daily_macro as market_return,
       pf.daily_stock - pf.daily_macro as excess_return
ORDER BY r.created DESC LIMIT 20
```

### Reports filed in last 30 days
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)
WHERE datetime(r.created) > datetime() - duration('P30D')
RETURN c.ticker, r.formType, r.created
ORDER BY r.created DESC LIMIT 50
```

### Reports with complete return data
```cypher
MATCH (c:Company)<-[pf:PRIMARY_FILER]-(r:Report)
WHERE pf.daily_stock IS NOT NULL AND pf.daily_industry IS NOT NULL
  AND pf.daily_sector IS NOT NULL AND pf.daily_macro IS NOT NULL
  AND pf.hourly_stock IS NOT NULL AND pf.session_stock IS NOT NULL
RETURN c.ticker, r.formType, r.created,
       pf.daily_stock, pf.daily_industry, pf.daily_sector, pf.daily_macro
LIMIT 20
```

### Reports with completed XBRL processing
```cypher
MATCH (r:Report)
WHERE r.xbrl_status = 'COMPLETED' AND datetime(r.created) > datetime() - duration('P30D')
RETURN r.formType, r.accessionNo, r.created, r.xbrl_status
ORDER BY r.created DESC LIMIT 20
```

## FinancialStatementContent Queries (JSON)

### Balance Sheets
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FINANCIAL_STATEMENT]->(fsc:FinancialStatementContent)
WHERE fsc.statement_type = 'BalanceSheets'
RETURN c.ticker, r.formType,
       substring(fsc.value, 0, 1000) as balance_sheet_json,
       size(fsc.value) as json_size
ORDER BY r.created DESC
LIMIT 10
```

### Income Statements
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FINANCIAL_STATEMENT]->(fsc:FinancialStatementContent)
WHERE fsc.statement_type = 'StatementsOfIncome'
RETURN c.ticker, r.formType,
       substring(fsc.value, 0, 1000) as income_statement_json
ORDER BY r.created DESC
LIMIT 10
```

### Cash Flow Statements
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FINANCIAL_STATEMENT]->(fsc:FinancialStatementContent)
WHERE fsc.statement_type = 'StatementsOfCashFlows'
RETURN c.ticker, r.formType,
       substring(fsc.value, 0, 1000) as cash_flow_json
ORDER BY r.created DESC
LIMIT 10
```

### Shareholders Equity Statements
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FINANCIAL_STATEMENT]->(fsc:FinancialStatementContent)
WHERE fsc.statement_type = 'StatementsOfShareholdersEquity'
RETURN c.ticker, r.formType,
       substring(fsc.value, 0, 1000) as equity_statement_json
ORDER BY r.created DESC
LIMIT 10
```

## FilingTextContent Queries

### Proxy Solicitations (425 filings)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FILING_TEXT]->(ftc:FilingTextContent)
WHERE ftc.form_type = '425'
RETURN c.ticker, substring(ftc.content, 0, 2000) as proxy_text, r.created
ORDER BY r.created DESC
LIMIT 20
```

### Schedule 13D/A (Activist/Ownership)
```cypher
MATCH (c:Company)<-[:REFERENCED_IN]-(r:Report)-[:HAS_FILING_TEXT]->(ftc:FilingTextContent)
WHERE ftc.form_type CONTAINS 'SCHEDULE 13D'
RETURN c.ticker, ftc.form_type,
       substring(ftc.content, 0, 1500) as ownership_disclosure, r.created
ORDER BY r.created DESC
LIMIT 20
```

### Foreign Private Issuer (6-K)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)-[:HAS_FILING_TEXT]->(ftc:FilingTextContent)
WHERE ftc.form_type = '6-K'
RETURN c.ticker, substring(ftc.content, 0, 1500) as foreign_issuer_content, r.created
ORDER BY r.created DESC
LIMIT 20
```

## Additional 8-K Event Sections

### Results of Operations (Item 2.02 - Section)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'ResultsofOperationsandFinancialCondition'
RETURN c.ticker, r.created, substring(esc.content, 0, 2000) as earnings_announcement
ORDER BY r.created DESC
LIMIT 20
```

### Other Events (Item 8.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'OtherEvents'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as other_event
ORDER BY r.created DESC
LIMIT 20
```

### Shareholder Voting Results (Item 5.07)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'SubmissionofMatterstoaVoteofSecurityHolders'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as voting_results
ORDER BY r.created DESC
LIMIT 20
```

### Financial Statements and Exhibits (Item 9.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'FinancialStatementsandExhibits'
RETURN c.ticker, r.created, substring(esc.content, 0, 1000) as exhibit_info
ORDER BY r.created DESC
LIMIT 20
```

### Debt/Financial Obligations (Item 2.03)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'CreationofaDirectFinancialObligationoranObligationunderanOff-BalanceSheetArrangementofaRegistrant'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as debt_details
ORDER BY r.created DESC
LIMIT 20
```

### Acquisitions/Dispositions (Item 2.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'CompletionofAcquisitionorDispositionofAssets'
RETURN c.ticker, r.created, substring(esc.content, 0, 2000) as transaction_details
ORDER BY r.created DESC
LIMIT 20
```

### Material Impairments (Item 2.06)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'MaterialImpairments'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as impairment_details
ORDER BY r.created DESC
LIMIT 20
```

### Bankruptcy/Receivership (Item 1.03)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'BankruptcyorReceivership'
RETURN c.ticker, r.created, substring(esc.content, 0, 2000) as bankruptcy_info
ORDER BY r.created DESC
LIMIT 20
```

### Delisting Notices (Item 3.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'NoticeofDelistingorFailuretoSatisfyaContinuedListingRuleorStandard;TransferofListing'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as delisting_notice
ORDER BY r.created DESC
LIMIT 20
```

### Executive Changes (Item 5.02)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'DepartureofDirectorsorCertainOfficers;ElectionofDirectors;AppointmentofCertainOfficers:CompensatoryArrangementsofCertainOfficers'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as executive_change
ORDER BY r.created DESC
LIMIT 20
```

### Regulation FD Disclosure (Item 7.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'RegulationFDDisclosure'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as fd_disclosure
ORDER BY r.created DESC
LIMIT 20
```

### Material Agreements (Item 1.01)
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report {formType: '8-K'})-[:HAS_SECTION]->(esc:ExtractedSectionContent)
WHERE esc.section_name = 'EntryintoaMaterialDefinitiveAgreement'
RETURN c.ticker, r.created, substring(esc.content, 0, 1500) as agreement_details
ORDER BY r.created DESC
LIMIT 20
```

## Get All Content for a Report
```cypher
MATCH (c:Company {ticker: $ticker})<-[:PRIMARY_FILER]-(r:Report)
WHERE r.created > datetime() - duration('P30D')
OPTIONAL MATCH (r)-[:HAS_SECTION]->(esc:ExtractedSectionContent)
OPTIONAL MATCH (r)-[:HAS_EXHIBIT]->(ec:ExhibitContent)
OPTIONAL MATCH (r)-[:HAS_FINANCIAL_STATEMENT]->(fsc:FinancialStatementContent)
OPTIONAL MATCH (r)-[:HAS_FILING_TEXT]->(ftc:FilingTextContent)
RETURN c.ticker, r.formType, r.created,
       COUNT(DISTINCT esc) as section_count,
       COUNT(DISTINCT ec) as exhibit_count,
       COUNT(DISTINCT fsc) as financial_statement_count,
       COUNT(DISTINCT ftc) as filing_text_count,
       COLLECT(DISTINCT esc.section_name)[0..5] as sample_sections,
       COLLECT(DISTINCT ec.exhibit_number)[0..5] as sample_exhibits
ORDER BY r.created DESC
LIMIT 10
```

## Notes
- `Report.items` is a JSON string. Use `CONTAINS` for item matching. Example: `["Item 2.02", "Item 9.01"]`.
- `Report.created` is ISO string with timezone. Example: `2023-01-04T13:48:33-05:00`.
- Returns (daily_stock, daily_macro) live on `PRIMARY_FILER` relationship, not Report node.
- `market_session` indicates pre/post/regular market timing.
- For Item 2.02 (earnings), check EX-99.1 exhibit first - section usually just references it.
- `FinancialStatementContent.statement_type` values: `BalanceSheets`, `StatementsOfIncome`, `StatementsOfCashFlows`, `StatementsOfShareholdersEquity`.
- `FilingTextContent.form_type` values include: `425`, `8-K`, `SCHEDULE 13D/A`, `6-K`, etc.
- Key 10-K/10-Q `section_name` values: `Business`, `RiskFactors`, `ManagementDiscussionandAnalysisofFinancialConditionandResultsofOperations`, `LegalProceedings`, `ExecutiveCompensation`, `Properties`, `ControlsandProcedures`, `Cybersecurity`.
- Key 8-K `section_name` values: `ResultsofOperationsandFinancialCondition` (2.02), `OtherEvents` (8.01), `RegulationFDDisclosure` (7.01), `FinancialStatementsandExhibits` (9.01).

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|
| 2026-01-11 | Missing exhibit content for some 8-K filings | Report:0000048465-25-000042 has 0 exhibits despite Item 9.01 listing EX-99 | Check exhibit_count before querying; use News/Transcript for key figures |

---
*Version 2.1 | 2026-01-11 | Added self-improvement protocol*
