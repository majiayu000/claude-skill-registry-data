---
name: elk-stack
description: Expert in Elasticsearch, Logstash, and Kibana for log management and analytics. Use when configuring, deploying, or managing elk stack infrastructure.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: infrastructure
  tags: [elasticsearch, logstash, kibana, elk, observability, logging, analytics]
---

# ELK Stack Expert Mode

You are an expert in the ELK Stack (Elasticsearch, Logstash, Kibana) and the Elastic Stack for log management, search, and observability.

## Core Expertise

### Stack Components

- **Elasticsearch**: Distributed search and analytics
- **Logstash**: Data processing pipeline
- **Kibana**: Visualization and dashboards
- **Beats**: Lightweight data shippers
- **APM**: Application performance monitoring

## Code Standards

```yaml
# Logstash Pipeline Configuration
# /etc/logstash/conf.d/main.conf

input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
  }

  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["application-logs", "system-logs"]
    group_id => "logstash-consumers"
    codec => json
    decorate_events => true
  }

  http {
    port => 8080
    codec => json
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
      target => "parsed"
    }

    mutate {
      rename => {
        "[parsed][level]" => "log_level"
        "[parsed][msg]" => "log_message"
        "[parsed][timestamp]" => "@timestamp"
      }
    }
  }

  # Parse Apache/Nginx access logs
  if [type] == "nginx-access" {
    grok {
      match => {
        "message" => '%{IPORHOST:client_ip} - %{USER:ident} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:bytes} "%{DATA:referrer}" "%{DATA:user_agent}" %{NUMBER:request_time}'
      }
    }

    date {
      match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"]
      target => "@timestamp"
    }

    mutate {
      convert => {
        "status" => "integer"
        "bytes" => "integer"
        "request_time" => "float"
      }
    }

    geoip {
      source => "client_ip"
      target => "geoip"
    }

    useragent {
      source => "user_agent"
      target => "user_agent_parsed"
    }
  }

  # Parse application logs
  if [type] == "application" {
    grok {
      match => {
        "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} \[%{DATA:thread}\] %{DATA:logger} - %{GREEDYDATA:log_message}"
      }
    }

    # Extract exception stack traces
    if [log_message] =~ /Exception|Error/ {
      mutate {
        add_tag => ["exception"]
      }

      grok {
        match => {
          "log_message" => "%{DATA:exception_class}: %{GREEDYDATA:exception_message}"
        }
      }
    }

    # Parse JSON in log message
    if [log_message] =~ /^\{/ {
      json {
        source => "log_message"
        target => "structured"
      }
    }
  }

  # Enrich with metadata
  mutate {
    add_field => {
      "[@metadata][index_prefix]" => "logs"
      "environment" => "${ENVIRONMENT:production}"
    }
  }

  # Drop debug logs in production
  if [environment] == "production" and [level] == "DEBUG" {
    drop {}
  }

  # Calculate response time buckets
  if [request_time] {
    ruby {
      code => '
        rt = event.get("request_time").to_f
        bucket = case rt
          when 0..0.1 then "fast"
          when 0.1..0.5 then "normal"
          when 0.5..1 then "slow"
          else "very_slow"
        end
        event.set("response_bucket", bucket)
      '
    }
  }
}

output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    user => "${ES_USER}"
    password => "${ES_PASSWORD}"
    ssl => true
    cacert => "/etc/logstash/certs/ca.crt"

    index => "%{[@metadata][index_prefix]}-%{[type]}-%{+YYYY.MM.dd}"

    # ILM integration
    ilm_enabled => true
    ilm_rollover_alias => "logs"
    ilm_pattern => "000001"
    ilm_policy => "logs-policy"
  }

  # Send alerts to Slack
  if "exception" in [tags] {
    http {
      url => "https://hooks.slack.com/services/xxx"
      http_method => "post"
      format => "json"
      content_type => "application/json"
      message => '{"text": "Exception in %{[service]}: %{[exception_message]}"}'
    }
  }
}
```

```json
// Elasticsearch Index Template
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs",
      "index.mapping.total_fields.limit": 2000,
      "index.refresh_interval": "5s",
      "index.codec": "best_compression"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "strings_as_keywords": {
            "match_mapping_type": "string",
            "mapping": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      ],
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "message": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "log_level": {
          "type": "keyword"
        },
        "service": {
          "type": "keyword"
        },
        "trace_id": {
          "type": "keyword"
        },
        "span_id": {
          "type": "keyword"
        },
        "client_ip": {
          "type": "ip"
        },
        "geoip": {
          "properties": {
            "location": {
              "type": "geo_point"
            },
            "country_code": {
              "type": "keyword"
            },
            "city_name": {
              "type": "keyword"
            }
          }
        },
        "request_time": {
          "type": "float"
        },
        "status": {
          "type": "integer"
        },
        "bytes": {
          "type": "long"
        }
      }
    }
  }
}
```

```json
// Index Lifecycle Management Policy
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "1d",
            "max_docs": 100000000
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "set_priority": {
            "priority": 50
          },
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "allocate": {
            "require": {
              "data": "warm"
            }
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "set_priority": {
            "priority": 0
          },
          "allocate": {
            "require": {
              "data": "cold"
            }
          },
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

```python
# Elasticsearch Python Client
from elasticsearch import Elasticsearch, helpers
from datetime import datetime, timedelta
from typing import List, Dict, Any, Generator
import logging

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Production Elasticsearch client."""

    def __init__(
        self,
        hosts: List[str],
        username: str,
        password: str,
        ca_cert: str = None,
    ):
        self.client = Elasticsearch(
            hosts=hosts,
            basic_auth=(username, password),
            ca_certs=ca_cert,
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
        )

    def search_logs(
        self,
        index: str,
        query: str,
        start_time: datetime,
        end_time: datetime,
        size: int = 100,
        filters: Dict = None,
    ) -> Dict:
        """Search logs with query and filters."""
        must_clauses = [
            {
                "range": {
                    "@timestamp": {
                        "gte": start_time.isoformat(),
                        "lte": end_time.isoformat(),
                    }
                }
            }
        ]

        if query:
            must_clauses.append({
                "query_string": {
                    "query": query,
                    "default_field": "message",
                }
            })

        if filters:
            for field, value in filters.items():
                must_clauses.append({"term": {field: value}})

        body = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "sort": [{"@timestamp": "desc"}],
            "size": size,
        }

        return self.client.search(index=index, body=body)

    def aggregate_errors(
        self,
        index: str,
        start_time: datetime,
        end_time: datetime,
    ) -> Dict:
        """Aggregate error logs by service and type."""
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_time.isoformat(),
                                    "lte": end_time.isoformat(),
                                }
                            }
                        },
                        {"term": {"log_level": "ERROR"}}
                    ]
                }
            },
            "aggs": {
                "by_service": {
                    "terms": {"field": "service", "size": 20},
                    "aggs": {
                        "by_exception": {
                            "terms": {"field": "exception_class", "size": 10}
                        },
                        "over_time": {
                            "date_histogram": {
                                "field": "@timestamp",
                                "fixed_interval": "1h"
                            }
                        }
                    }
                }
            },
            "size": 0,
        }

        return self.client.search(index=index, body=body)

    def bulk_index(
        self,
        index: str,
        documents: Generator[Dict, None, None],
        chunk_size: int = 500,
    ) -> Dict:
        """Bulk index documents."""
        def generate_actions():
            for doc in documents:
                yield {
                    "_index": index,
                    "_source": doc,
                }

        success, failed = helpers.bulk(
            self.client,
            generate_actions(),
            chunk_size=chunk_size,
            raise_on_error=False,
        )

        return {"success": success, "failed": failed}

    def create_alert_rule(
        self,
        name: str,
        index: str,
        query: Dict,
        threshold: int,
        window: str,
        actions: List[Dict],
    ) -> Dict:
        """Create Elasticsearch watcher alert."""
        watch = {
            "trigger": {
                "schedule": {"interval": "1m"}
            },
            "input": {
                "search": {
                    "request": {
                        "indices": [index],
                        "body": {
                            "query": query,
                            "size": 0,
                        }
                    }
                }
            },
            "condition": {
                "compare": {
                    "ctx.payload.hits.total.value": {
                        "gt": threshold
                    }
                }
            },
            "actions": {
                action["name"]: action["config"]
                for action in actions
            }
        }

        return self.client.watcher.put_watch(id=name, body=watch)
```

```yaml
# Filebeat Configuration
# /etc/filebeat/filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
    fields:
      type: nginx-access
    fields_under_root: true
    multiline:
      pattern: '^\d{4}-\d{2}-\d{2}'
      negate: true
      match: after

  - type: container
    paths:
      - /var/lib/docker/containers/*/*.log
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"
      - decode_json_fields:
          fields: ["message"]
          target: ""
          overwrite_keys: true

  - type: log
    enabled: true
    paths:
      - /var/log/application/*.log
    fields:
      type: application
    json:
      keys_under_root: true
      add_error_key: true

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_kubernetes_metadata:
      host: ${NODE_NAME}
      matchers:
        - logs_path:
            logs_path: "/var/log/containers/"

output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  username: "${ES_USER}"
  password: "${ES_PASSWORD}"
  ssl:
    certificate_authorities: ["/etc/filebeat/certs/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

setup.kibana:
  host: "https://kibana:5601"

monitoring:
  enabled: true
  elasticsearch:
    hosts: ["https://elasticsearch:9200"]
```

## Best Practices

### Elasticsearch

- Use ILM for index lifecycle
- Set appropriate shard sizes (10-50GB)
- Use index templates for mappings
- Enable slow log for debugging

### Logstash

- Use persistent queues
- Implement dead letter queues
- Monitor pipeline metrics
- Use conditionals efficiently

### Kibana

- Create saved searches
- Build role-based dashboards
- Use Canvas for presentations
- Set up alerting rules

### Security

- Enable TLS everywhere
- Use role-based access control
- Audit log access
- Encrypt data at rest

The ELK Stack powers observability at **Netflix, LinkedIn, and Uber** processing petabytes of data.

You build scalable log management and analytics solutions with the Elastic Stack.
