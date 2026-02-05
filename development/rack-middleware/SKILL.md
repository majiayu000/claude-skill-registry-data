---
name: rack-middleware
description: Rack middleware development, configuration, and integration patterns. Use when working with middleware stacks or creating custom middleware.
---

# Rack Middleware Skill

## Tier 1: Quick Reference - Middleware Basics

### Middleware Structure

```ruby
class MyMiddleware
  def initialize(app, options = {})
    @app = app
    @options = options
  end

  def call(env)
    # Before request
    # Modify env if needed

    # Call next middleware
    status, headers, body = @app.call(env)

    # After request
    # Modify response if needed

    [status, headers, body]
  end
end

# Usage
use MyMiddleware, option: 'value'
```

### Common Middleware

```ruby
# Session management
use Rack::Session::Cookie, secret: ENV['SESSION_SECRET']

# Security
use Rack::Protection

# Compression
use Rack::Deflater

# Logging
use Rack::CommonLogger

# Static files
use Rack::Static, urls: ['/css', '/js'], root: 'public'
```

### Middleware Ordering

```ruby
# config.ru - Correct order
use Rack::Deflater           # 1. Compression
use Rack::Static             # 2. Static files
use Rack::CommonLogger       # 3. Logging
use Rack::Session::Cookie    # 4. Sessions
use Rack::Protection          # 5. Security
use CustomAuth               # 6. Authentication
run Application              # 7. Application
```

### Request/Response Access

```ruby
class SimpleMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    # Access request via env hash
    method = env['REQUEST_METHOD']
    path = env['PATH_INFO']
    query = env['QUERY_STRING']

    # Or use Rack::Request
    request = Rack::Request.new(env)
    params = request.params

    # Process request
    status, headers, body = @app.call(env)

    # Modify response
    headers['X-Custom-Header'] = 'value'

    [status, headers, body]
  end
end
```

---

## Tier 2: Detailed Instructions - Advanced Middleware

### Custom Middleware Development

**Request Logging Middleware:**
```ruby
require 'logger'

class RequestLogger
  def initialize(app, options = {})
    @app = app
    @logger = options[:logger] || Logger.new(STDOUT)
    @skip_paths = options[:skip_paths] || []
  end

  def call(env)
    return @app.call(env) if skip_logging?(env)

    start_time = Time.now
    request = Rack::Request.new(env)

    log_request_start(request)

    status, headers, body = @app.call(env)

    duration = Time.now - start_time
    log_request_end(request, status, duration)

    [status, headers, body]
  rescue StandardError => e
    log_error(request, e)
    raise
  end

  private

  def skip_logging?(env)
    path = env['PATH_INFO']
    @skip_paths.any? { |skip| path.start_with?(skip) }
  end

  def log_request_start(request)
    @logger.info({
      event: 'request.start',
      method: request.request_method,
      path: request.path,
      ip: request.ip,
      user_agent: request.user_agent
    }.to_json)
  end

  def log_request_end(request, status, duration)
    @logger.info({
      event: 'request.end',
      method: request.request_method,
      path: request.path,
      status: status,
      duration: duration.round(3)
    }.to_json)
  end

  def log_error(request, error)
    @logger.error({
      event: 'request.error',
      method: request.request_method,
      path: request.path,
      error: error.class.name,
      message: error.message,
      backtrace: error.backtrace[0..5]
    }.to_json)
  end
end

# Usage
use RequestLogger, skip_paths: ['/health', '/metrics']
```

**Authentication Middleware:**
```ruby
class TokenAuthentication
  def initialize(app, options = {})
    @app = app
    @token_header = options[:header] || 'HTTP_AUTHORIZATION'
    @skip_paths = options[:skip_paths] || []
    @realm = options[:realm] || 'Application'
  end

  def call(env)
    return @app.call(env) if skip_authentication?(env)

    token = extract_token(env)

    if valid_token?(token)
      user = find_user_by_token(token)
      env['current_user'] = user
      @app.call(env)
    else
      unauthorized_response
    end
  end

  private

  def skip_authentication?(env)
    path = env['PATH_INFO']
    method = env['REQUEST_METHOD']

    # Skip for public paths
    @skip_paths.any? { |skip| path.start_with?(skip) } ||
      # Skip for OPTIONS (CORS preflight)
      method == 'OPTIONS'
  end

  def extract_token(env)
    auth_header = env[@token_header]
    return nil unless auth_header

    # Support "Bearer TOKEN" format
    if auth_header.start_with?('Bearer ')
      auth_header.split(' ', 2).last
    else
      auth_header
    end
  end

  def valid_token?(token)
    return false unless token

    # Implement your token validation logic
    # This is a placeholder
    token.length >= 32
  end

  def find_user_by_token(token)
    # Implement your user lookup logic
    # This is a placeholder
    { id: 1, email: 'user@example.com' }
  end

  def unauthorized_response
    [
      401,
      {
        'Content-Type' => 'application/json',
        'WWW-Authenticate' => "Bearer realm=\"#{@realm}\""
      },
      ['{"error": "Unauthorized"}']
    ]
  end
end

# Usage
use TokenAuthentication,
  skip_paths: ['/login', '/register', '/public']
```

**Caching Middleware:**
```ruby
require 'digest/md5'

class SimpleCache
  def initialize(app, options = {})
    @app = app
    @cache = {}
    @ttl = options[:ttl] || 300  # 5 minutes
    @cache_methods = options[:methods] || ['GET']
  end

  def call(env)
    request = Rack::Request.new(env)

    return @app.call(env) unless cacheable?(request)

    cache_key = generate_cache_key(env)

    if cached_response = get_from_cache(cache_key)
      return cached_response
    end

    status, headers, body = @app.call(env)

    if cacheable_response?(status)
      cache_response(cache_key, [status, headers, body])
    end

    [status, headers, body]
  end

  private

  def cacheable?(request)
    @cache_methods.include?(request.request_method)
  end

  def cacheable_response?(status)
    status == 200
  end

  def generate_cache_key(env)
    # Include method, path, and query string
    Digest::MD5.hexdigest([
      env['REQUEST_METHOD'],
      env['PATH_INFO'],
      env['QUERY_STRING']
    ].join('|'))
  end

  def get_from_cache(key)
    entry = @cache[key]
    return nil unless entry

    # Check if cache entry is still valid
    if Time.now - entry[:cached_at] <= @ttl
      entry[:response]
    else
      @cache.delete(key)
      nil
    end
  end

  def cache_response(key, response)
    @cache[key] = {
      response: response,
      cached_at: Time.now
    }
  end
end

# Usage with Redis for distributed caching
class RedisCache
  def initialize(app, options = {})
    @app = app
    @redis = Redis.new(url: options[:redis_url])
    @ttl = options[:ttl] || 300
    @namespace = options[:namespace] || 'cache'
  end

  def call(env)
    request = Rack::Request.new(env)

    return @app.call(env) unless request.get?

    cache_key = generate_cache_key(env)

    if cached = @redis.get(cache_key)
      return Marshal.load(cached)
    end

    status, headers, body = @app.call(env)

    if status == 200
      @redis.setex(cache_key, @ttl, Marshal.dump([status, headers, body]))
    end

    [status, headers, body]
  end

  private

  def generate_cache_key(env)
    "#{@namespace}:#{Digest::MD5.hexdigest(env['PATH_INFO'] + env['QUERY_STRING'])}"
  end
end
```

**Request Transformation Middleware:**
```ruby
class JSONBodyParser
  def initialize(app)
    @app = app
  end

  def call(env)
    if json_request?(env)
      body = env['rack.input'].read
      env['rack.input'].rewind

      begin
        parsed = JSON.parse(body)
        env['rack.request.form_hash'] = parsed
        env['parsed_json'] = parsed
      rescue JSON::ParserError => e
        return error_response('Invalid JSON', 400)
      end
    end

    @app.call(env)
  end

  private

  def json_request?(env)
    content_type = env['CONTENT_TYPE']
    content_type && content_type.include?('application/json')
  end

  def error_response(message, status)
    [
      status,
      { 'Content-Type' => 'application/json' },
      [{ error: message }.to_json]
    ]
  end
end

# XML Parser
class XMLBodyParser
  def initialize(app)
    @app = app
  end

  def call(env)
    if xml_request?(env)
      body = env['rack.input'].read
      env['rack.input'].rewind

      begin
        parsed = Hash.from_xml(body)
        env['rack.request.form_hash'] = parsed
        env['parsed_xml'] = parsed
      rescue StandardError => e
        return error_response('Invalid XML', 400)
      end
    end

    @app.call(env)
  end

  private

  def xml_request?(env)
    content_type = env['CONTENT_TYPE']
    content_type && (content_type.include?('application/xml') ||
                     content_type.include?('text/xml'))
  end

  def error_response(message, status)
    [
      status,
      { 'Content-Type' => 'application/json' },
      [{ error: message }.to_json]
    ]
  end
end
```

### Middleware Ordering Patterns

**Security-First Stack:**
```ruby
# config.ru
# 1. SSL redirect (production only)
use Rack::SSL if ENV['RACK_ENV'] == 'production'

# 2. Rate limiting (before everything else)
use Rack::Attack

# 3. Security headers
use SecurityHeaders

# 4. CORS (for API applications)
use Rack::Cors do
  allow do
    origins '*'
    resource '*', headers: :any, methods: [:get, :post, :put, :delete, :options]
  end
end

# 5. Compression
use Rack::Deflater

# 6. Static files
use Rack::Static, urls: ['/public'], root: 'public'

# 7. Logging
use Rack::CommonLogger

# 8. Request parsing
use JSONBodyParser

# 9. Sessions
use Rack::Session::Cookie,
  secret: ENV['SESSION_SECRET'],
  same_site: :strict,
  httponly: true,
  secure: ENV['RACK_ENV'] == 'production'

# 10. Protection (CSRF, etc.)
use Rack::Protection

# 11. Authentication
use TokenAuthentication, skip_paths: ['/login', '/public']

# 12. Performance monitoring
use PerformanceMonitor

# 13. Application
run Application
```

**API-Focused Stack:**
```ruby
# config.ru for API
# 1. CORS first for preflight
use Rack::Cors do
  allow do
    origins ENV.fetch('ALLOWED_ORIGINS', '*').split(',')
    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options],
      credentials: true,
      max_age: 86400
  end
end

# 2. Rate limiting
use Rack::Attack

# 3. Compression
use Rack::Deflater

# 4. Logging (structured JSON logs)
use RequestLogger

# 5. Request parsing
use JSONBodyParser

# 6. Authentication
use TokenAuthentication, skip_paths: ['/auth']

# 7. Caching
use RedisCache, ttl: 300

# 8. Application
run API
```

### Conditional Middleware

**Environment-Based:**
```ruby
class ConditionalMiddleware
  def initialize(app, condition, middleware, *args)
    @app = if condition.call
      middleware.new(app, *args)
    else
      app
    end
  end

  def call(env)
    @app.call(env)
  end
end

# Usage
use ConditionalMiddleware,
  -> { ENV['RACK_ENV'] == 'development' },
  Rack::ShowExceptions

use ConditionalMiddleware,
  -> { ENV['ENABLE_PROFILING'] == 'true' },
  RackMiniProfiler
```

**Path-Based:**
```ruby
class PathBasedMiddleware
  def initialize(app, pattern, middleware, *args)
    @app = app
    @pattern = pattern
    @middleware = middleware.new(app, *args)
  end

  def call(env)
    if env['PATH_INFO'].match?(@pattern)
      @middleware.call(env)
    else
      @app.call(env)
    end
  end
end

# Usage
use PathBasedMiddleware, %r{^/api}, CacheMiddleware, ttl: 300
use PathBasedMiddleware, %r{^/admin}, AdminAuth
```

### Error Handling Middleware

```ruby
class ErrorHandler
  def initialize(app, options = {})
    @app = app
    @logger = options[:logger] || Logger.new(STDOUT)
    @error_handlers = options[:handlers] || {}
  end

  def call(env)
    @app.call(env)
  rescue StandardError => e
    handle_error(env, e)
  end

  private

  def handle_error(env, error)
    request = Rack::Request.new(env)

    # Log error
    @logger.error({
      error: error.class.name,
      message: error.message,
      path: request.path,
      method: request.request_method,
      backtrace: error.backtrace[0..10]
    }.to_json)

    # Custom handler for specific error types
    if handler = @error_handlers[error.class]
      return handler.call(error)
    end

    # Default error response
    status = status_for_error(error)
    [
      status,
      { 'Content-Type' => 'application/json' },
      [{ error: error.message, type: error.class.name }.to_json]
    ]
  end

  def status_for_error(error)
    case error
    when ArgumentError, ValidationError
      400
    when NotFoundError
      404
    when AuthorizationError
      403
    when AuthenticationError
      401
    else
      500
    end
  end
end

# Usage
use ErrorHandler,
  handlers: {
    ValidationError => ->(e) {
      [422, { 'Content-Type' => 'application/json' },
       [{ error: e.message, details: e.details }.to_json]]
    }
  }
```

---

## Tier 3: Resources & Examples

### Complete Middleware Examples

**Performance Monitoring:**
```ruby
class PerformanceMonitor
  def initialize(app, options = {})
    @app = app
    @threshold = options[:threshold] || 1.0  # 1 second
    @logger = options[:logger] || Logger.new(STDOUT)
  end

  def call(env)
    start_time = Time.now
    memory_before = memory_usage

    status, headers, body = @app.call(env)

    duration = Time.now - start_time
    memory_after = memory_usage
    memory_delta = memory_after - memory_before

    # Add performance headers
    headers['X-Runtime'] = duration.to_s
    headers['X-Memory-Delta'] = memory_delta.to_s

    # Log slow requests
    if duration > @threshold
      log_slow_request(env, duration, memory_delta)
    end

    [status, headers, body]
  end

  private

  def memory_usage
    `ps -o rss= -p #{Process.pid}`.to_i / 1024.0  # MB
  end

  def log_slow_request(env, duration, memory)
    @logger.warn({
      event: 'slow_request',
      method: env['REQUEST_METHOD'],
      path: env['PATH_INFO'],
      duration: duration.round(3),
      memory_delta: memory.round(2)
    }.to_json)
  end
end
```

**Request ID Tracking:**
```ruby
class RequestID
  def initialize(app, options = {})
    @app = app
    @header = options[:header] || 'X-Request-ID'
  end

  def call(env)
    request_id = env["HTTP_#{@header.upcase.tr('-', '_')}"] || generate_id
    env['request.id'] = request_id

    status, headers, body = @app.call(env)

    headers[@header] = request_id

    [status, headers, body]
  end

  private

  def generate_id
    SecureRandom.uuid
  end
end
```

**Response Modification:**
```ruby
class ResponseTransformer
  def initialize(app, &block)
    @app = app
    @transformer = block
  end

  def call(env)
    status, headers, body = @app.call(env)

    if should_transform?(headers)
      body = transform_body(body)
    end

    [status, headers, body]
  end

  private

  def should_transform?(headers)
    headers['Content-Type']&.include?('application/json')
  end

  def transform_body(body)
    content = body.is_a?(Array) ? body.join : body.read
    transformed = @transformer.call(content)
    [transformed]
  end
end

# Usage
use ResponseTransformer do |body|
  data = JSON.parse(body)
  data['timestamp'] = Time.now.to_i
  data.to_json
end
```

### Testing Middleware

```ruby
RSpec.describe RequestLogger do
  let(:app) { ->(env) { [200, {}, ['OK']] } }
  let(:logger) { double('Logger', info: nil, error: nil) }
  let(:middleware) { RequestLogger.new(app, logger: logger) }
  let(:request) { Rack::MockRequest.new(middleware) }

  describe 'request logging' do
    it 'logs request start' do
      expect(logger).to receive(:info).with(hash_including(event: 'request.start'))
      request.get('/')
    end

    it 'logs request end with duration' do
      expect(logger).to receive(:info).with(hash_including(
        event: 'request.end',
        duration: kind_of(Numeric)
      ))
      request.get('/')
    end

    it 'includes request details' do
      expect(logger).to receive(:info).with(hash_including(
        method: 'GET',
        path: '/test'
      ))
      request.get('/test')
    end
  end

  describe 'error logging' do
    let(:app) { ->(env) { raise StandardError, 'Test error' } }

    it 'logs errors' do
      expect(logger).to receive(:error).with(hash_including(
        event: 'request.error',
        error: 'StandardError'
      ))

      expect { request.get('/') }.to raise_error(StandardError)
    end
  end

  describe 'skip paths' do
    let(:middleware) { RequestLogger.new(app, logger: logger, skip_paths: ['/health']) }

    it 'skips logging for configured paths' do
      expect(logger).not_to receive(:info)
      request.get('/health')
    end
  end
end
```

### Additional Resources

- **Middleware Template:** `assets/middleware-template.rb` - Boilerplate for new middleware
- **Middleware Examples:** `assets/middleware-examples/` - Collection of useful middleware
- **Configuration Guide:** `assets/configuration-guide.md` - Best practices for middleware configuration
- **Performance Guide:** `references/performance-optimization.md` - Optimizing middleware performance
- **Testing Guide:** `references/middleware-testing.md` - Comprehensive testing strategies
