---
name: debug-protocol
description: >
  Evidence-first debugging in 5 stages — REPRODUCE, EVIDENCE, DIAGNOSE, FIX,
  PROVE. Never touch code before the root cause is stated with evidence; fix
  the source, not the symptom; hand dead-end investigations to the
  root-cause-debugger agent. Use for any bug, error, crash, regression,
  unexpected behavior, or /toh-fix work.
user-invocable: false  # internal — model-invoked via toh-* commands, not a user /command
---
# 🔧 Debug Protocol Skill

> **Purpose:** Evidence-first debugging — หา root cause ด้วยหลักฐาน ไม่เดา ไม่กดอาการ
> **Version:** 2.0.0
> **Updated:** 2026-07-14

---

## 🎯 Core Idea

```
❌ Guess & retry loop
undefined → ใส่ ?.  →  พังที่อื่น  →  ใส่ ?. อีก  →  วนไม่จบ
(กดอาการ ไม่เคยถามว่า "ทำไมข้อมูลถึง undefined")

✅ Evidence-first
REPRODUCE → EVIDENCE → DIAGNOSE → FIX → PROVE
(เก็บหลักฐานจริง → วินิจฉัย → แก้ต้นตอ → พิสูจน์)
```

**กฎเหล็ก:** อย่าแตะโค้ดจนกว่าจะบอก root cause ได้พร้อมหลักฐาน
ถ้าร่องรอยตัน → ส่งงานสืบสวนให้ agent `root-cause-debugger`

---

## Protocol — 5 Stages

### 1. REPRODUCE — ทำให้พังซ้ำก่อน
ทำให้ bug เกิดบนเจตนา ก่อนคิดแก้. รู้ path / action / ข้อมูลที่ทำให้พัง แล้วเห็นมันพังจริง
**ทำซ้ำไม่ได้ = แก้ไม่ได้** → บอกตรงๆ แล้วขอ steps / env / data เพิ่ม

### 2. EVIDENCE — เก็บหลักฐาน (ห้ามเดา)
- อ่าน **error + stack trace เต็มๆ** — ไฟล์/บรรทัด/call chain
- `git log` / `git diff` — อะไรเพิ่งเปลี่ยน (bug ใหม่ = โค้ดใหม่ ~80%)
- ตาม **data flow** ด้วย log/debugger จริง — ค่ามาจากไหน หายที่จุดไหน

### 3. DIAGNOSE — differential diagnosis
สมมุติฐาน 2–3 ข้อ + หลักฐานสนับสนุน/หักล้างแต่ละข้อ → เลือกข้อที่หลักฐานชี้ ไม่ใช่ข้อที่แก้ง่ายสุด
ถาม "ทำไม" ต่อจนถึงต้นตอ

### 4. FIX — แก้ที่ต้นตอ
แก้ root cause จุดเดียว. defensive guard ตรงจุดอาการเสริมได้ **แต่ guard ≠ การแก้** — ต้นตอต้องหาย

### 5. PROVE — พิสูจน์ว่าหาย
รันเส้นทางเดิมที่พังซ้ำ + เส้นทางข้างเคียง แล้วค่อยรายงาน

---

## 🛠 Technique: Targeted Logging

log ค่า **ตรงจุดก่อนพัง** และ log **shape จริง** ของข้อมูล — อย่าเดาว่าหน้าตาเป็นยังไง

```js
// ก่อนบรรทัดที่พัง: ค่าจริงตอนนั้นคืออะไร
console.log('[render] products =', products, 'isArray:', Array.isArray(products));

// API response: ดู shape จริง ไม่ใช่ที่ "คิดว่าได้"
const data = await res.json();
console.log('[api] typeof:', typeof data, 'keys:', Object.keys(data ?? {}), data);
```

ถามให้ตรง: ตอน render มีข้อมูลไหม? เป็น array จริงไหม? key ที่โค้ดอ้างถึงมีอยู่จริงไหม?

---

## 🛠 Technique: git bisect — หา commit ที่ทำพัง

Bug ใหม่ = โค้ดใหม่. binary search หา commit ต้นเหตุ:

```bash
git bisect start
git bisect bad                 # commit ปัจจุบัน (พัง)
git bisect good v1.7.0         # commit/tag ที่รู้ว่ายังดี
# git checkout ให้อัตโนมัติทีละครึ่ง → ทดสอบ → บอกผล:
git bisect good                # commit นี้ยังดี
git bisect bad                 # commit นี้พังแล้ว
# ...จนได้ commit แรกที่ทำพัง
git bisect reset
```

Manual bisect (ถ้าไม่มี tag good): `git log --oneline` → checkout กลางๆ → ทดสอบ → ขยับ
เจาะลึก commit ต้องสงสัย: `git log -p <file>` / `git diff <commit>~..<commit> -- <file>`

---

## 🛠 Technique: Differential Diagnosis

เขียน hypothesis แข่งกัน แล้วใช้หลักฐาน **ตัดทิ้ง** ทีละข้อ:

```
Bug: dashboard พัง "Cannot read property map of undefined"

H1: API ตอบช้า → render ก่อนได้ data
    ✔ for: พังตอนโหลดครั้งแรก, refresh แล้วบางทีหาย
    ✘ against: ถ้า cache อยู่ควรไม่พัง — ตรวจ: มี loading guard ไหม? → ไม่มี
H2: API response shape เปลี่ยน (products ย้ายไป data.items)
    ✔ for: backend เพิ่ง deploy (git log ฝั่ง API)
    ✘ against: log แล้ว data.products ยังมีอยู่ → ตัดทิ้ง
H3: race condition หลาย fetch เขียนทับ state
    ✘ against: มี fetch เดียว → ตัดทิ้ง

→ หลักฐานชี้ H1 (ไม่มี loading state) = root cause จริง
```

หลักฐานเป็นตัวเลือก hypothesis ไม่ใช่ความง่ายในการแก้

---

## 🎨 Debug Patterns: CSS / Layout

Symptom → สืบหาสาเหตุ → พิสูจน์ (ไม่ใช่แปะ fix สำเร็จรูป)

### Scroll เกิน / white space ด้านล่าง
- **สืบ:** parent มี fixed height + child มี padding/margin ไหม? มี element ไหน overflow?
- **พิสูจน์:** DevTools → เลื่อน inspect หา element ที่สูงเกิน viewport จริง → ค่อยแก้ที่ตัวนั้น
- สาเหตุพบบ่อย: `h-screen` + padding พร้อมกัน, flex item ขาด `min-h-0`, `position: fixed` หลุด flow

### Element ไม่อยู่ที่ที่คาด
- **สืบ:** เป็น flow / flex / grid / absolute? parent เป็น positioning context ไหม?
- **พิสูจน์:** ใส่ outline ชั่วคราว (`outline: 1px solid red`) กับ element + parent เพื่อเห็น box จริง

---

## ⚙️ Debug Patterns: JavaScript / Async

### Function เหมือนไม่ทำงาน
- **สืบ:** ถูกเรียกจริงไหม? args ที่เข้ามาคืออะไร? state ก่อน/หลังต่างไหม?
- **พิสูจน์:** `console.log` ต้นฟังก์ชัน — ถ้าไม่ขึ้น = ปัญหาอยู่ที่ "การเรียก" (event binding: `onClick={fn()}` vs `onClick={fn}`) ไม่ใช่ในฟังก์ชัน

### ค่าไม่อัพเดท / เป็น undefined
- **สืบ:** await ครบไหม? Promise reject เงียบไหม? useEffect dependency ตรงไหม?
- **พิสูจน์:** log ค่าที่ทุก step ของ chain — หาจุด **แรก** ที่ค่าผิด นั่นคือต้นตอ ไม่ใช่จุดที่ throw

---

## 🚫 Anti-Patterns

```
❌ กดอาการ: undefined → ใส่ ?. โดยไม่ถามว่าทำไม undefined
❌ เดาแล้วแก้: เปลี่ยนโค้ดก่อนมีหลักฐาน
❌ แก้หลายจุดพร้อมกัน: พังแล้วไม่รู้จุดไหนช่วย
❌ รายงานก่อนพิสูจน์: "น่าจะได้แล้ว" โดยไม่รันซ้ำ
❌ ยอมแพ้เร็ว: ลองไม่กี่รอบแล้วลบเขียนใหม่ทั้งที่ยังไม่รู้สาเหตุ
```

---

## 🔗 Integration

| Skill | ใช้ร่วมกันยังไง |
|-------|----------------|
| `error-handling` | debug สำหรับ error ที่ auto-fix ไม่ได้ |
| `engineer-harness` | รายงานผล: Problem → Root cause → Fix → Proof → Prevention |
| agent `root-cause-debugger` | delegate การสืบสวนเมื่อร่องรอยตัน |

---

## 💡 When to Use

```
USE:  แก้ไม่หายสักที · error เดิมกลับมา · "ทำไมถึงเป็นแบบนี้" · bug ที่ยังไม่รู้สาเหตุ
SKIP: typo ชัดๆ · error ที่ fix ชัดเจน · feature request (ไม่ใช่ bug)
```
