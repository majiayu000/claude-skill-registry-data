---
name: libavutil
description: "Skill for the Libavutil area of iVista-Client-Application. 24 symbols across 8 files."
---

# Libavutil

24 symbols | 8 files | Cohesion: 100%

## When to Use

- Working with code in `V3SClient/`
- Understanding how av_refstruct_alloc_ext_c, av_log2, av_strerror work
- Modifying libavutil-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/ffmpeg/include/libavutil/refstruct.h` | av_refstruct_alloc_ext_c, av_refstruct_alloc_ext, av_refstruct_allocz, av_refstruct_unref, av_refstruct_pool_uninit (+2) |
| `V3SClient/ffmpeg/include/libavutil/common.h` | av_log2, av_ceil_log2_c, av_zero_extend_c, av_mod_uintp2_c |
| `V3SClient/ffmpeg/include/libavutil/avstring.h` | av_isdigit, av_tolower, av_isxdigit |
| `V3SClient/ffmpeg/include/libavutil/bswap.h` | av_bswap32, av_bswap64 |
| `V3SClient/ffmpeg/include/libavutil/error.h` | av_strerror, av_make_error_string |
| `V3SClient/ffmpeg/include/libavutil/frame.h` | av_frame_side_data_get_c, av_frame_side_data_get |
| `V3SClient/ffmpeg/include/libavutil/imgutils.h` | av_image_copy, av_image_copy2 |
| `V3SClient/ffmpeg/include/libavutil/timestamp.h` | av_ts_make_time_string2, av_ts_make_time_string |

## Entry Points

Start here when exploring this area:

- **`av_refstruct_alloc_ext_c`** (Function) — `V3SClient/ffmpeg/include/libavutil/refstruct.h:83`
- **`av_log2`** (Function) — `V3SClient/ffmpeg/include/libavutil/common.h:163`
- **`av_strerror`** (Function) — `V3SClient/ffmpeg/include/libavutil/error.h:99`
- **`av_frame_side_data_get_c`** (Function) — `V3SClient/ffmpeg/include/libavutil/frame.h:1181`
- **`av_image_copy`** (Function) — `V3SClient/ffmpeg/include/libavutil/imgutils.h:172`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `av_refstruct_alloc_ext_c` | Function | `V3SClient/ffmpeg/include/libavutil/refstruct.h` | 83 |
| `av_log2` | Function | `V3SClient/ffmpeg/include/libavutil/common.h` | 163 |
| `av_strerror` | Function | `V3SClient/ffmpeg/include/libavutil/error.h` | 99 |
| `av_frame_side_data_get_c` | Function | `V3SClient/ffmpeg/include/libavutil/frame.h` | 1181 |
| `av_image_copy` | Function | `V3SClient/ffmpeg/include/libavutil/imgutils.h` | 172 |
| `av_refstruct_unref` | Function | `V3SClient/ffmpeg/include/libavutil/refstruct.h` | 118 |
| `av_refstruct_pool_alloc_ext_c` | Function | `V3SClient/ffmpeg/include/libavutil/refstruct.h` | 243 |
| `av_ts_make_time_string2` | Function | `V3SClient/ffmpeg/include/libavutil/timestamp.h` | 64 |
| `av_isdigit` | Function | `V3SClient/ffmpeg/include/libavutil/avstring.h` | 201 |
| `av_tolower` | Function | `V3SClient/ffmpeg/include/libavutil/avstring.h` | 236 |
| `av_isxdigit` | Function | `V3SClient/ffmpeg/include/libavutil/avstring.h` | 246 |
| `av_refstruct_alloc_ext` | Function | `V3SClient/ffmpeg/include/libavutil/refstruct.h` | 92 |
| `av_refstruct_allocz` | Function | `V3SClient/ffmpeg/include/libavutil/refstruct.h` | 103 |
| `av_bswap32` | Function | `V3SClient/ffmpeg/include/libavutil/bswap.h` | 61 |
| `av_ceil_log2_c` | Function | `V3SClient/ffmpeg/include/libavutil/common.h` | 435 |
| `av_zero_extend_c` | Function | `V3SClient/ffmpeg/include/libavutil/common.h` | 291 |
| `av_mod_uintp2_c` | Function | `V3SClient/ffmpeg/include/libavutil/common.h` | 303 |
| `av_make_error_string` | Function | `V3SClient/ffmpeg/include/libavutil/error.h` | 111 |
| `av_frame_side_data_get` | Function | `V3SClient/ffmpeg/include/libavutil/frame.h` | 1191 |
| `av_image_copy2` | Function | `V3SClient/ffmpeg/include/libavutil/imgutils.h` | 182 |

## How to Explore

1. `context({name: "av_refstruct_alloc_ext_c"})` — see callers and callees
2. `query({search_query: "libavutil"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
