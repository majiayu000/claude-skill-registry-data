---
name: configuring-image-optimization
description: Teach image optimization configuration changes in Next.js 16. Use when configuring images, troubleshooting image loading, or migrating image settings.
allowed-tools: Read, Write, Edit, Glob, Grep, TodoWrite
version: 1.0.0
---

# Image Optimization Configuration in Next.js 16

## Breaking Changes

### 1. Removed Configuration Options

**`domains` (removed)**
- Replaced by `remotePatterns`
- More secure with pattern matching instead of wildcard domain access

**`loader` (removed for 'default')**
- Custom loaders must now be specified explicitly
- No implicit fallback to default loader behavior

**`formats` array changes**
- AVIF format now enabled by default
- Order affects format preference during negotiation

### 2. Changed Default Values

**`minimumCacheTTL`**
- Old default: 60 seconds
- New default: 31536000 seconds (1 year)
- Requires manual override for shorter cache durations

**`deviceSizes`**
- Updated default breakpoints to match modern devices
- Old: `[640, 750, 828, 1080, 1200, 1920, 2048, 3840]`
- New: `[640, 750, 828, 1080, 1200, 1920, 2048, 3840, 4096]`

**`imageSizes`**
- Updated for modern layout shifts
- Old: `[16, 32, 48, 64, 96, 128, 256, 384]`
- New: `[16, 32, 48, 64, 96, 128, 256, 384, 512]`

### 3. Security Enhancements

**`dangerouslyAllowSVG`**
- Now requires explicit `contentDispositionType` setting
- Default changed to 'attachment' for security
- Inline SVG rendering requires opt-in configuration

**`unoptimized`**
- Stricter enforcement in production
- Warning logs for unoptimized images in development
- Performance metrics now track optimization bypass

## Core Configuration

### Basic Setup

```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        port: '',
        pathname: '/images/**',
      },
    ],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 31536000,
  },
}
```

### remotePatterns

Securely allow external image sources:

```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        hostname: '*.cloudinary.com',
        pathname: '/**',
      },
    ],
  },
}
```

**Pattern properties:**
- `protocol`: 'http' or 'https'
- `hostname`: exact match or wildcard (*.example.com)
- `port`: specific port number (optional)
- `pathname`: glob patterns using ** for nested paths

### minimumCacheTTL

Controls optimized image cache duration:

```javascript
module.exports = {
  images: {
    minimumCacheTTL: 60,
  },
}
```

**Common values:**
- `60`: Frequently changing images
- `3600`: Hourly updates (1 hour)
- `86400`: Daily updates (1 day)
- `31536000`: Static assets (1 year, default)

### imageSizes

Sizes for images with explicit `sizes` prop:

```javascript
module.exports = {
  images: {
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
}
```

**Usage:**
```jsx
<Image
  src="/avatar.jpg"
  sizes="(max-width: 768px) 64px, 128px"
  width={128}
  height={128}
  alt="Avatar"
/>
```

### deviceSizes

Viewport breakpoints for responsive images:

```javascript
module.exports = {
  images: {
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
  },
}
```

**Usage:**
```jsx
<Image
  src="/hero.jpg"
  fill
  sizes="100vw"
  alt="Hero"
/>
```

### localPatterns

Control local file optimization access:

```javascript
module.exports = {
  images: {
    localPatterns: [
      {
        pathname: '/public/uploads/**',
        search: '',
      },
    ],
  },
}
```

## Migration Patterns

### From domains to remotePatterns

**Before:**
```javascript
module.exports = {
  images: {
    domains: ['example.com', 'cdn.example.com'],
  },
}
```

**After:**
```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/**',
      },
    ],
  },
}
```

### Adjusting Cache for Dynamic Content

**Before (60s default):**
```javascript
module.exports = {
  images: {
    domains: ['api.example.com'],
  },
}
```

**After (explicit cache):**
```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'api.example.com',
        pathname: '/dynamic-images/**',
      },
    ],
    minimumCacheTTL: 300,
  },
}
```

### Restricting Image Sources

**Before:**
```javascript
module.exports = {
  images: {
    domains: ['*.cloudinary.com'],
  },
}
```

**After:**
```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
        pathname: '/my-account/image/upload/**',
      },
    ],
  },
}
```

## Common Configurations

### Production

```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.production.com',
        pathname: '/**',
      },
    ],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 31536000,
    dangerouslyAllowSVG: false,
  },
}
```

### Development

```javascript
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '3001',
        pathname: '/**',
      },
    ],
    minimumCacheTTL: 60,
  },
}
```

### Multi-Environment

```javascript
const isProd = process.env.NODE_ENV === 'production'

module.exports = {
  images: {
    remotePatterns: isProd
      ? [
          {
            protocol: 'https',
            hostname: 'cdn.production.com',
            pathname: '/**',
          },
        ]
      : [
          {
            protocol: 'http',
            hostname: 'localhost',
            port: '3001',
            pathname: '/**',
          },
        ],
    minimumCacheTTL: isProd ? 31536000 : 60,
  },
}
```

### Mobile-Optimized

```javascript
module.exports = {
  images: {
    deviceSizes: [375, 414, 640, 750, 828, 1080],
    imageSizes: [24, 32, 48, 64, 96],
  },
}
```

### SVG Support

```javascript
module.exports = {
  images: {
    dangerouslyAllowSVG: true,
    contentDispositionType: 'inline',
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
}
```

## Quick Troubleshooting

### Image Not Loading

Check pattern matches URL:

```javascript
remotePatterns: [
  {
    protocol: 'https',
    hostname: 'example.com',
    pathname: '/images/**',
  },
]
```

Verify:
- Protocol matches (https vs http)
- Hostname exact or wildcard match
- Pathname pattern includes image path

### Cache Not Updating

Override default TTL:

```javascript
module.exports = {
  images: {
    minimumCacheTTL: 3600,
  },
}
```

Clear build cache:

```bash
rm -rf .next
npm run build
```

### SVG Not Rendering

Enable with security:

```javascript
module.exports = {
  images: {
    dangerouslyAllowSVG: true,
    contentDispositionType: 'inline',
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },
}
```

### Performance Issues

Reduce size variants:

```javascript
module.exports = {
  images: {
    deviceSizes: [640, 828, 1200, 1920],
    imageSizes: [32, 64, 128, 256],
  },
}
```

## Detailed References

For comprehensive examples and advanced configurations, see the `references/` directory:

**`configuration-examples.md`**
- Complete configuration patterns
- E-commerce, CMS, social media setups
- Multi-CDN configurations
- Industry-specific examples

**`security-settings.md`**
- SVG security best practices
- Content Security Policy options
- Content Disposition configurations
- Security monitoring strategies

**`troubleshooting.md`**
- Advanced debugging techniques
- Edge cases and solutions
- Performance optimization
- Runtime error resolution

**`migration-guide.md`**
- Step-by-step migration from Next.js 15
- Complex migration scenarios
- Verification checklist
- Rollback strategies

## Related Skills

- Use `images-component` skill for Next.js Image component usage
- Use `images-responsive` skill for responsive image patterns
- Use `images-loaders` skill for custom image loader configuration
