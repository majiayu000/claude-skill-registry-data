---
name: gen-voice
description: สร้างเสียงพูดจากข้อความด้วย bunx TTS CLI
argument-hint: "[text]"
related:
  - gen-subtitle-video
  - gen-media
---

## Goal

สร้างไฟล์เสียงพูดจากข้อความด้วย TTS CLI

## Scope

- ใช้ `bunx` CLI สำหรับ text-to-speech
- รองรับหลายภาษาและ voices
- รองรับ output `.mp3`, `.wav`, `.ogg`

## Execute

### 1. Prepare Text

> Goal: มีข้อความทีชัดเจน

1. รับ text จาก user หรือ file
2. ถ้า text ยาวเกินไป → แบ่งเป็นหลาย chunk
3. ระบุภาษา (default auto-detect)
4. ระบุ voice, speed, output format

### 2. Choose CLI

> Goal: เลือก TTS tool

1. Primary: `bunx @pollinations/cli gen audio "<text>" --voice nova --output speech.mp3`
   - ไม่ต้อง API key
   - รองรับหลาย voices
2. Fallback: `bunx talk-tts "<text>" -o out.wav`
   - ใช้ Kokoro, offline หลัง download
   - รองรับ 150+ voices
3. Fallback: `bunx tts-cli "<text>" --save speech.mp3`
   - ใช้ Microsoft Edge TTS
   - ต้องการ internet
4. Fallback: `bunx @illyism/transcribe` ไม่ใช่ TTS (skip)

### 3. Generate Voice

> Goal: สร้างไฟล์เสียง

1. รันคำสั่งพร้อม text, voice, output
2. รอจนกระทั่งเสร็จ
3. ตรวจสอบไฟล์ output มีขนาด > 0
4. ถ้าผิดภาษา → ระบุ `--lang` แล้วรันใหม่

### 4. Validate

> Goal: ตรวจสอบเสียง

1. ใช้ `ffprobe` หรือ `file` ตรวจ type
2. ถ้าเปิดได้ → รายงาน duration
3. รายงาน path, voice, format

## Rules

### 1. Language

- ใช้ auto-detect ถ้าไม่ระบุ
- ถ้า text มีหลายภาษา → แบ่ง chunk หรือเลือก voice ทีรองรับ

### 2. Chunks

- ถ้า text ยาว → แบ่งเป็นหลายไฟล์แล้ว concat ด้วย ffmpeg
- ไม่ส่ง text ยาวเกิน provider limit

### 3. No Leaks

- ไม่ hardcode API key
- ใช้ environment variable หรือถาม user

- ใช้ /gen-subtitle-video ถ้าจำเป็น
- ใช้ /gen-media-ai-videos ถ้าจำเป็น

## Expected Outcome

- ไฟล์เสียงจากข้อความ
- รายงาน path, voice, duration, tool ทีใช้
- ถ้า fail มีแนวทาง fallback
