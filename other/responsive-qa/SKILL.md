---
name: responsive-qa
description: Run a responsive QA pass on a FixNow page or component across desktop, tablet, and mobile Chrome viewports. Verifies no horizontal scroll, touch targets, Vietnamese diacritics, layout shifts, and Lighthouse mobile score. Use when user says "kiem tra responsive", "test trang X", "check tren mobile/tablet", "qa giao dien".
---

# responsive-qa

Kiem tra responsive cho FixNow tren 3 viewport Chrome: desktop, tablet, mobile.

## Truoc khi chay

Hoi user:
1. Trang nao can kiem tra? (URL day du hoac component path)
2. Co bug cu the dang nghi khong? (de focus check)

## Viewports chuan (Chrome DevTools)

| Profile | Viewport | Mau thiet bi |
|---------|----------|--------------|
| Mobile  | 375 x 667 | iPhone SE |
| Tablet  | 768 x 1024 | iPad Mini |
| Desktop | 1280 x 800 | MacBook 13" |
| Desktop large | 1920 x 1080 | Full HD |

## Workflow

### 1. Khoi dong dev server

    npm run dev

Mo Chrome -> F12 -> Toggle device toolbar (Ctrl+Shift+M).

### 2. Doi qua tung viewport va chay checklist

Bao user thuc hien tung viewport mot. KHONG bao "done" khi chua test du 3.

### Checklist chung (cho moi viewport)

#### Layout
- [ ] Khong horizontal scroll (kiem tra scroll trai-phai).
- [ ] Khong content tran ra ngoai container.
- [ ] Hinh anh fit container (w-full hoac max-w-full).
- [ ] Text khong bi cat off, khong overflow.

#### Tieng Viet
- [ ] Chu co dau hien thi dung (UTF-8 OK, khong mojibake).
- [ ] Font ho tro Vietnamese subset (Inter subset 'vietnamese').

#### Performance
- [ ] Khong console error (mau do).
- [ ] Khong hydration mismatch warning.
- [ ] Page load < 3s tren throttle "Fast 4G" (DevTools Network).

### Checklist mobile (375px)

- [ ] Touch target >= 44px (button h-11/h-12, icon button p-3).
- [ ] Form input co text-base (16px) -- KHONG dung text-sm (iOS zoom).
- [ ] Submit button w-full.
- [ ] Mobile hamburger menu mo/dong, khong trap focus.
- [ ] Floating contact (hotline + Zalo) o goc duoi phai, khong che footer.
- [ ] Khoang cach giua interactive elements >= 8px.

### Checklist tablet (768px)

- [ ] Grid 1 cot -> 2 cot (vd: `md:grid-cols-2`).
- [ ] Navbar inline links hien thi (an hamburger).
- [ ] Floating contact con phu hop khong, hoac switch sang inline.
- [ ] Form max-w-md mx-auto (khong full width chay rang).
- [ ] Sidebar / drawer behavior dung.

### Checklist desktop (1280px+)

- [ ] Grid 2 -> 3 hoac 4 cot tuy noi dung (`lg:grid-cols-3`).
- [ ] Container max-width hop ly (khong tran full-screen text).
- [ ] Hero section can chinh, khong qua cao (`min-h-[60vh]`).
- [ ] Footer co structure cot (vd: 3-4 cot).
- [ ] Floating contact thuong AN o desktop (`md:hidden`).

### Checklist orientation

- [ ] Xoay mobile sang landscape (667x375): navbar khong qua cao, modal van fit.
- [ ] Tablet landscape (1024x768): layout hop ly nhu desktop nho.

### Checklist interaction

- [ ] Click button -> action xay ra (submit, nav, modal).
- [ ] Form validate inline.
- [ ] Toast notification hien.
- [ ] Back button browser dieu huong dung.
- [ ] Keyboard tab order hop ly (a11y).
- [ ] Focus visible (ring-2 ring-primary).

### Lighthouse audit (optional but recommended)

Mobile audit:
- Performance >= 70 (acceptable cho dev).
- Accessibility >= 90.
- Best Practices >= 90.
- SEO >= 90.

Lenh CLI:

    npx lighthouse http://localhost:3000/<path> --view --form-factor=mobile

## Bao cao

Format output:

    # Responsive QA -- <page name>

    ## Mobile (375px) -- PASSED / FAILED
    - [ok / fail: path:line] item

    ## Tablet (768px) -- PASSED / FAILED
    ...

    ## Desktop (1280px) -- PASSED / FAILED
    ...

    ## Issues to fix
    1. [priority] file:line -- mo ta + de xuat sua

    ## Needs user attention
    - <thu can user verify thu cong>

## Lien ket

- Loi UI tim duoc -> spawn agent **fixnow-ui-builder** de sua.
- Spec compliance -> spawn agent **fixnow-spec-reviewer**.
- Performance issues -> tham khao skill **next-best-practices** (image, font, bundling).

## Toolkit

- Chrome DevTools Device Mode.
- Lighthouse mobile audit.
- React DevTools Profiler neu nghi render issue.
- `npx @next/bundle-analyzer` neu bundle qua lon.
