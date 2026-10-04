---
name: nginx
description: Nginx web server, reverse proxy, and load balancer configuration
license: MIT
compatibility: opencode
metadata:
  audience: devops
  category: web-servers
---
## What I do
- Configure Nginx as web server
- Set up reverse proxies
- Implement load balancing
- Configure SSL/TLS
- Set up caching
- Handle rate limiting
- Configure gzip compression

## When to use me
When deploying web applications or setting up API gateways.

## Basic Configuration
```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## SSL/TLS
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.crt;
    ssl_certificate_key /etc/ssl/private/example.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # SSL session caching
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
}
```

## Load Balancing
```nginx
upstream backend {
    least_conn;  # or ip_hash, hash $request_uri
    
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080;
    server backend3.example.com:8080 backup;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Caching
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 
    keys_zone=api_cache:10m 
    max_size=1g 
    inactive=60m;

server {
    location /api {
        proxy_cache api_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        add_header X-Cache-Status $upstream_cache_status;
        
        proxy_pass http://backend;
    }
}
```

## Rate Limiting
```nginx
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=1r/s;

    server {
        location /api {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://backend;
        }
        
        location /login {
            limit_req zone=login_limit burst=5 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

## Gzip Compression
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript 
    text/xml application/xml application/xml+rss text/javascript;
gzip_proxied any;
```

## Static Files
```nginx
server {
    location /static {
        alias /var/www/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public";
    }
}
```
