---
name: chef
description: "Covers Chef Infra (18.x): cookbooks, recipes, resources, attributes, Chef Server, Chef Workstation, InSpec, Habitat, Test Kitchen, and knife CLI. WHEN: \"Chef\", \"cookbook\", \"recipe\", \"knife\", \"Chef Infra\", \"Chef Server\", \"InSpec\", \"Habitat\", \"Test Kitchen\", \"Berkshelf\", \"chef-client\", \"Policyfile\"."
license: MIT
---

# Chef Infra Expert

This skill covers Chef Infra 18.x, a configuration management platform that uses Ruby DSL to define infrastructure as code. Chef uses a client-server architecture where chef-client (agent) runs on managed nodes and converges them to the desired state defined in cookbooks.

## Core Architecture

```
┌──────────────────┐     ┌──────────────────┐
│  Chef Workstation │────▶│   Chef Server    │
│  (knife, chef)   │     │  (cookbook store, │
└──────────────────┘     │   node data,     │
                          │   search index)  │
                          └────────┬─────────┘
                                   │ (HTTPS pull)
                    ┌──────────────┼──────────────┐
                    │              │              │
               ┌────▼────┐  ┌─────▼────┐  ┌─────▼────┐
               │  Node A  │  │  Node B  │  │  Node C  │
               │ (chef-   │  │ (chef-   │  │ (chef-   │
               │  client) │  │  client) │  │  client) │
               └──────────┘  └──────────┘  └──────────┘
```

### Key Concepts

| Concept | Description |
|---|---|
| **Cookbook** | Unit of distribution — contains recipes, attributes, templates, files |
| **Recipe** | Ruby DSL file defining resources to converge |
| **Resource** | Declarative unit (package, file, service, user) |
| **Attribute** | Configuration values with precedence levels |
| **Role** | Named run list + attributes applied to nodes |
| **Environment** | Cookbook version constraints per environment |
| **Data Bag** | Global JSON data (users, credentials, config) |
| **Policyfile** | Modern alternative to roles/environments — pinned, versioned |
| **Run List** | Ordered list of recipes/roles to apply to a node |

### Recipe Example

```ruby
# cookbooks/webserver/recipes/default.rb

# Install nginx
package 'nginx' do
  action :install
end

# Deploy configuration
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  owner 'root'
  group 'root'
  mode '0644'
  variables(
    worker_processes: node['webserver']['workers'],
    server_name: node['webserver']['hostname']
  )
  notifies :reload, 'service[nginx]'
end

# Ensure service running
service 'nginx' do
  action [:enable, :start]
end

# Create application directory
directory '/var/www/app' do
  owner 'www-data'
  group 'www-data'
  mode '0755'
  recursive true
end
```

### Attribute Precedence (Simplified)

From lowest to highest:
1. Cookbook `default` attributes
2. Environment `default` attributes
3. Role `default` attributes
4. Node `normal` attributes (persisted)
5. Cookbook `override` attributes
6. Environment `override` attributes
7. Role `override` attributes
8. Automatic (Ohai) attributes — **always wins**

### Policyfile (Modern Workflow)

```ruby
# Policyfile.rb
name 'web-server'
default_source :supermarket

cookbook 'nginx', '~> 12.0'
cookbook 'myapp', path: './cookbooks/myapp'

run_list 'recipe[nginx]', 'recipe[myapp::deploy]'

# Per-environment attributes
default['myapp']['environment'] = 'production'
```

```bash
# Workflow
chef install Policyfile.rb     # Resolve dependencies
chef push production           # Push to Chef Server for 'production' policy group
```

### InSpec (Compliance Testing)

```ruby
# profiles/ssh-hardening/controls/ssh.rb
control 'sshd-01' do
  impact 1.0
  title 'SSH root login should be disabled'
  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
  end
end

control 'sshd-02' do
  impact 0.7
  title 'SSH should use Protocol 2'
  describe sshd_config do
    its('Protocol') { should cmp 2 }
  end
end
```

```bash
# Run InSpec locally
inspec exec profiles/ssh-hardening

# Run against remote target
inspec exec profiles/ssh-hardening -t ssh://user@host

# Run against cloud resources
inspec exec profiles/aws-cis -t aws://
```

### CLI Reference

```bash
# Knife (server management)
knife cookbook upload myapp
knife node list
knife node show web1.example.com
knife role create webserver
knife data bag create credentials

# Chef Workstation
chef generate cookbook my-cookbook
chef generate recipe my-cookbook my-recipe
chef install Policyfile.rb
chef push production

# Test Kitchen
kitchen create        # Create test instance
kitchen converge      # Run Chef on instance
kitchen verify        # Run InSpec tests
kitchen destroy       # Cleanup
kitchen test          # Full lifecycle
```

## Reference Files

- `references/architecture.md` — Chef Server internals, Ohai, resource execution, Policyfile workflow, Habitat
- `references/best-practices.md` — Cookbook design, testing strategy, attribute management, migration to Policyfiles
- `references/diagnostics.md` — Convergence failures, resource errors, cookbook dependency issues, Chef Server connectivity
