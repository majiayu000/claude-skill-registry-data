---
name: drupal-planner.search
description: "Plan Drupal search — Search API, Solr/Elasticsearch, faceted search, indexing strategies."
---

# Drupal Search Planner

## Overview

drupal-planner.search designs Drupal search and discovery architectures before implementation. It produces specifications for Search API server and index configuration, field mapping, processor selection, Facets module setup, Views search page configuration, autocomplete, zero-result handling, and content discovery patterns — all expressed in Drupal Search API terms.

This is a focused sub-planner of `/drupal-planner`. Use it when the planning scope is specifically about search and content discovery rather than a full feature implementation.

## Use_When

- User says "plan the search", "design search architecture", "configure Search API"
- User needs to choose a search backend (Solr, Elasticsearch, Database)
- User is designing faceted search with the Facets module
- User is planning Search API index configuration, field mapping, or processors
- User needs to design Views-based search pages, autocomplete, or zero-result handling
- User has search-discovery-critic REVISE findings to address

## Do_Not_Use_When

- User needs full feature planning — use `/drupal-planner`
- User wants to review existing search — use `search-discovery-critic`
- User is focused on taxonomy design — use `/drupal-planner.taxonomy`
- User is focused on content model — use `/drupal-planner.content-model`

## Companion_Skills

- `drupal-planner`: Full Drupal implementation planning
- `search-discovery-critic`: Review the search architecture after design
- `drupal-critic`: Review the implementation after coding
- `drupal-planner.taxonomy`: Taxonomy design (taxonomies power faceted search)
- `drupal-planner.content-model`: Content model design (determines what's indexed)

## Steps

1. **Identify scope**: What search/discovery architecture is being designed?
2. **Detect context**: Drupal version, existing search setup, Search API modules, backend (Solr/Elasticsearch/DB)
3. **Route to agent**: Delegate to the drupal-search-planner agent
   - `Agent(subagent_type="drupal-planner", model="opus", prompt=<search_planning_prompt>)`
4. **Return the plan**: Present search architecture specification

## Tool_Usage

- Use Read to examine existing Search API config, Views search pages, Facets configuration
- Use Grep to find search_api index definitions, facet configurations, Views display settings
- Use Bash to check composer.json for search_api_solr, elasticsearch_connector, facets modules
- Write the plan to `docs/plans/`
