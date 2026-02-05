---
name: sinatra-patterns
description: Common Sinatra patterns, routing strategies, error handling, and application organization. Use when building Sinatra applications or designing routes.
---

# Sinatra Patterns Skill

## Tier 1: Quick Reference

### Common Routing Patterns

**Basic Routes:**
```ruby
get '/' do
  'Hello World'
end

post '/users' do
  # Create user
end

put '/users/:id' do
  # Update user
end

delete '/users/:id' do
  # Delete user
end
```

**Route Parameters:**
```ruby
# Named parameters
get '/users/:id' do
  User.find(params[:id])
end

# Parameter constraints
get '/users/:id', :id => /\d+/ do
  # Only matches numeric IDs
end

# Wildcard
get '/files/*.*' do
  # params['splat'] contains matched segments
end
```

**Query Parameters:**
```ruby
get '/search' do
  query = params[:q]
  page = params[:page] || 1
  results = search(query, page: page)
end
```

### Basic Middleware

```ruby
# Session middleware
use Rack::Session::Cookie, secret: ENV['SESSION_SECRET']

# Security middleware
use Rack::Protection

# Logging
use Rack::CommonLogger

# Compression
use Rack::Deflater
```

### Simple Error Handling

```ruby
not_found do
  'Page not found'
end

error do
  'Internal server error'
end

error 401 do
  'Unauthorized'
end
```

### Helpers

```ruby
helpers do
  def logged_in?
    !session[:user_id].nil?
  end

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end
end
```

---

## Tier 2: Detailed Instructions

### Advanced Routing

**Modular Applications:**
```ruby
# app/controllers/base_controller.rb
class BaseController < Sinatra::Base
  configure do
    set :views, Proc.new { File.join(root, '../views') }
    set :public_folder, Proc.new { File.join(root, '../public') }
  end

  helpers do
    def json_response(data, status = 200)
      content_type :json
      halt status, data.to_json
    end
  end
end

# app/controllers/users_controller.rb
class UsersController < BaseController
  get '/' do
    users = User.all
    json_response(users.map(&:to_hash))
  end

  get '/:id' do
    user = User.find(params[:id]) || halt(404)
    json_response(user.to_hash)
  end

  post '/' do
    user = User.create(params[:user])
    if user.persisted?
      json_response(user.to_hash, 201)
    else
      json_response({ errors: user.errors }, 422)
    end
  end
end

# config.ru
map '/users' do
  run UsersController
end
```

**Namespaces:**
```ruby
require 'sinatra/namespace'

class App < Sinatra::Base
  register Sinatra::Namespace

  namespace '/api' do
    namespace '/v1' do
      get '/users' do
        # GET /api/v1/users
      end

      namespace '/admin' do
        before do
          authenticate_admin!
        end

        get '/stats' do
          # GET /api/v1/admin/stats
        end
      end
    end
  end
end
```

**Route Conditions:**
```ruby
# User agent condition
get '/', :agent => /iPhone/ do
  # Mobile version
end

# Custom conditions
set(:auth) do |role|
  condition do
    unless current_user && current_user.has_role?(role)
      halt 403
    end
  end
end

get '/admin', :auth => :admin do
  # Only accessible to admins
end

# Host-based routing
get '/', :host => 'admin.example.com' do
  # Admin subdomain
end
```

**Content Negotiation:**
```ruby
get '/users/:id', :provides => [:json, :xml, :html] do
  user = User.find(params[:id])

  case request.accept.first.to_s
  when 'application/json'
    json user.to_json
  when 'application/xml'
    xml user.to_xml
  else
    erb :user, locals: { user: user }
  end
end

# Or using provides helper
get '/users/:id' do
  user = User.find(params[:id])

  respond_to do |format|
    format.json { json user.to_json }
    format.xml { xml user.to_xml }
    format.html { erb :user, locals: { user: user } }
  end
end
```

### Middleware Composition

**Custom Middleware:**
```ruby
class RequestLogger
  def initialize(app)
    @app = app
  end

  def call(env)
    start_time = Time.now
    status, headers, body = @app.call(env)
    duration = Time.now - start_time

    puts "#{env['REQUEST_METHOD']} #{env['PATH_INFO']} - #{status} (#{duration}s)"

    [status, headers, body]
  end
end

use RequestLogger
```

**Middleware Ordering:**
```ruby
# config.ru
use Rack::Deflater                    # Compression first
use Rack::Static                       # Static files
use Rack::CommonLogger                 # Logging
use Rack::Session::Cookie             # Sessions
use Rack::Protection                   # Security
use CustomAuthentication              # Auth
run Application
```

### Template Integration

**ERB Templates:**
```ruby
# views/layout.erb
<!DOCTYPE html>
<html>
<head>
  <title><%= @title || 'My App' %></title>
</head>
<body>
  <%= yield %>
</body>
</html>

# views/users/index.erb
<h1>Users</h1>
<ul>
  <% @users.each do |user| %>
    <li><%= user.name %></li>
  <% end %>
</ul>

# Controller
get '/users' do
  @users = User.all
  @title = 'User List'
  erb :'users/index'
end
```

**Inline Templates:**
```ruby
get '/' do
  erb :index
end

__END__

@@layout
<!DOCTYPE html>
<html>
  <body><%= yield %></body>
</html>

@@index
<h1>Welcome</h1>
```

**Template Engines:**
```ruby
# Haml
get '/' do
  haml :index
end

# Slim
get '/' do
  slim :index
end

# Liquid (safe for user content)
get '/' do
  liquid :index, locals: { user: current_user }
end
```

### Error Handling Patterns

**Comprehensive Error Handling:**
```ruby
class Application < Sinatra::Base
  # Development configuration
  configure :development do
    set :show_exceptions, :after_handler
    set :dump_errors, true
  end

  # Production configuration
  configure :production do
    set :show_exceptions, false
    set :dump_errors, false
  end

  # Specific exception handlers
  error ActiveRecord::RecordNotFound do
    status 404
    json({ error: 'Resource not found' })
  end

  error ActiveRecord::RecordInvalid do
    status 422
    json({ error: 'Validation failed', details: env['sinatra.error'].message })
  end

  error Sequel::NoMatchingRow do
    status 404
    json({ error: 'Not found' })
  end

  # HTTP status handlers
  not_found do
    json({ error: 'Endpoint not found' })
  end

  error 401 do
    json({ error: 'Unauthorized' })
  end

  error 403 do
    json({ error: 'Forbidden' })
  end

  error 422 do
    json({ error: 'Unprocessable entity' })
  end

  # Catch-all error handler
  error do
    error = env['sinatra.error']
    logger.error("Error: #{error.message}")
    logger.error(error.backtrace.join("\n"))

    status 500
    json({ error: 'Internal server error' })
  end
end
```

### Before/After Filters

**Request Filters:**
```ruby
# Global before filter
before do
  content_type :json
end

# Path-specific filters
before '/admin/*' do
  authenticate_admin!
end

# Conditional filters
before do
  pass unless request.path.start_with?('/api')
  authenticate_api_user!
end

# After filters
after do
  # Add CORS headers
  headers 'Access-Control-Allow-Origin' => '*'
end

# Modify response
after do
  response.body = response.body.map(&:upcase) if params[:uppercase]
end
```

### Session Management

**Cookie Sessions:**
```ruby
use Rack::Session::Cookie,
  key: 'app.session',
  secret: ENV['SESSION_SECRET'],
  expire_after: 86400,  # 1 day
  secure: production?,
  httponly: true,
  same_site: :strict

helpers do
  def login(user)
    session[:user_id] = user.id
    session[:logged_in_at] = Time.now.to_i
  end

  def logout
    session.clear
  end

  def current_user
    return nil unless session[:user_id]
    @current_user ||= User.find_by(id: session[:user_id])
  end
end
```

---

## Tier 3: Resources & Examples

### Full Application Example

See `assets/modular-app-template/` for complete modular application structure.

### Performance Patterns

**Caching:**
```ruby
# HTTP caching
get '/public/data' do
  cache_control :public, max_age: 3600
  etag calculate_etag
  last_modified last_update_time

  json PublicData.all.map(&:to_hash)
end

# Fragment caching with Redis
require 'redis'

helpers do
  def cache_fetch(key, expires_in: 300, &block)
    cached = REDIS.get(key)
    return JSON.parse(cached) if cached

    data = block.call
    REDIS.setex(key, expires_in, data.to_json)
    data
  end
end

get '/expensive-data' do
  data = cache_fetch('expensive-data', expires_in: 600) do
    perform_expensive_query
  end

  json data
end
```

**Streaming Responses:**
```ruby
# Stream large responses
get '/large-export' do
  stream do |out|
    User.find_each do |user|
      out << user.to_csv_row
    end
  end
end

# Server-Sent Events
get '/events', provides: 'text/event-stream' do
  stream :keep_open do |out|
    EventSource.subscribe do |event|
      out << "data: #{event.to_json}\n\n"
    end
  end
end
```

### Production Configuration

**Complete config.ru:**
```ruby
# config.ru
require_relative 'config/environment'

# Production middleware
if ENV['RACK_ENV'] == 'production'
  use Rack::SSL
  use Rack::Deflater
end

# Static files
use Rack::Static,
  urls: ['/css', '/js', '/images'],
  root: 'public',
  header_rules: [
    [:all, {'Cache-Control' => 'public, max-age=31536000'}]
  ]

# Logging
use Rack::CommonLogger

# Sessions
use Rack::Session::Cookie,
  secret: ENV['SESSION_SECRET'],
  same_site: :strict,
  httponly: true,
  secure: ENV['RACK_ENV'] == 'production'

# Security
use Rack::Protection,
  except: [:session_hijacking],
  use: :all

# Rate limiting (production)
if ENV['RACK_ENV'] == 'production'
  require 'rack/attack'
  use Rack::Attack
end

# Mount applications
map '/api/v1' do
  run ApiV1::Application
end

map '/' do
  run WebApplication
end
```

**Rack::Attack Configuration:**
```ruby
# config/rack_attack.rb
class Rack::Attack
  # Throttle login attempts
  throttle('login/ip', limit: 5, period: 60) do |req|
    req.ip if req.path == '/login' && req.post?
  end

  # Throttle API requests
  throttle('api/ip', limit: 100, period: 60) do |req|
    req.ip if req.path.start_with?('/api')
  end

  # Block suspicious requests
  blocklist('block bad user agents') do |req|
    req.user_agent =~ /bad_bot/i
  end
end
```

### Testing Patterns

See `references/testing-examples.rb` for comprehensive test patterns.

### Project Structure

**Recommended modular structure:**
```
app/
  controllers/
    base_controller.rb
    api_controller.rb
    users_controller.rb
    posts_controller.rb
  models/
    user.rb
    post.rb
  services/
    user_service.rb
    authentication_service.rb
  helpers/
    application_helpers.rb
    view_helpers.rb
config/
  environment.rb
  database.yml
  puma.rb
db/
  migrations/
lib/
  middleware/
    custom_auth.rb
  tasks/
public/
  css/
  js/
  images/
views/
  layout.erb
  users/
    index.erb
    show.erb
spec/
  controllers/
  models/
  spec_helper.rb
config.ru
Gemfile
Rakefile
README.md
```

### Additional Resources

- **Routing Examples:** `assets/routing-examples.rb`
- **Middleware Patterns:** `assets/middleware-patterns.rb`
- **Modular App Template:** `assets/modular-app-template/`
- **Production Config:** `references/production-config.rb`
- **Testing Guide:** `references/testing-examples.rb`
