---
name: final-checklist
description: Comprehensive pre-launch verification checklist. Use as the last step before deploying. Triggers on "final check", "pre-launch", "ready to deploy", "launch checklist".
---

# Final Checklist

Comprehensive verification before website launch.

## Content

- [ ] All pages have unique title tags (50-60 chars)
- [ ] All pages have unique meta descriptions (150-160 chars)
- [ ] All H1s contain primary keywords
- [ ] Only ONE H1 per page
- [ ] All images have alt text
- [ ] No placeholder text ("Lorem ipsum")
- [ ] No broken links
- [ ] Contact info is correct

## Technical SEO

- [ ] sitemap.xml accessible at /sitemap.xml
- [ ] robots.txt allows crawling
- [ ] Schema.org JSON-LD added
- [ ] Open Graph tags on all pages
- [ ] Twitter cards configured
- [ ] Canonical URLs set

## Legal

- [ ] Impressum page exists and accessible
- [ ] Datenschutz page exists and accessible
- [ ] Cookie consent (if analytics used)
- [ ] All required legal info present

## Design

- [ ] Favicon displays correctly
- [ ] 404 page works
- [ ] Mobile responsive (test all breakpoints)
- [ ] No horizontal scroll
- [ ] Dark mode works (if applicable)

## Performance

- [ ] Lighthouse score > 90
- [ ] Page load < 3 seconds
- [ ] Images optimized (WebP)
- [ ] No console errors
- [ ] No console warnings

## i18n

- [ ] DE translations complete
- [ ] EN translations complete
- [ ] Language switcher works
- [ ] URLs use correct locale prefix

## Forms

- [ ] Contact form submits correctly
- [ ] Form validation works
- [ ] Success/error messages display
- [ ] Email delivery tested

## Final Steps

1. Run `pnpm build` - verify no build errors
2. Test production build locally
3. Verify all environment variables set
4. Deploy to staging first
5. Full QA on staging
6. Deploy to production

## Launch Readiness

```
[ ] All checklist items passed
[ ] Client approval received
[ ] DNS configured correctly
[ ] SSL certificate active
[ ] Analytics tracking verified
```
