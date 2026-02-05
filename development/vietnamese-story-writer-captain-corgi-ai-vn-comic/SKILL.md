---
name: vietnamese-story-writer
description: Tạo và viết truyện tranh bằng tiếng Việt với các thể loại đa dạng. Use when you need to create engaging stories, fables, or narratives in Vietnamese language for different audiences and purposes.
---

# Vietnamese Story Writer

## Mô tả
Kỹ năng này giúp bạn tạo ra những câu chuyện hấp dẫn bằng tiếng Việt với nhiều thể loại khác nhau như truyện cổ tích, ngụ ngôn, truyện ngắn, hay truyện thiếu nhi. Công cụ hỗ trợ phát triển ý tưởng, cấu trúc câu chuyện, và tạo ra nội dung chất lượng cao.

## Sử dụng khi nào
- Cần viết truyện cổ tích or ngụ ngôn cho trẻ em
- Tạo truyện ngắn với chủ đề cụ thể
- Phát triển nội dung giáo dục giải trí
- Viết truyện với bài học đạo đức hoặc giá trị nhân văn
- Tạo nội dung cho các nền tảng giải trí

## Công cụ có sẵn

### 1. Story Generator (Python)
**Đường dẫn:** `scripts/story_generator.py`
**Mô tả:** Tạo câu chuyện tự động dựa trên thể loại và chủ đề được chọn

**Cách sử dụng:**
```bash
# Tạo truyện cổ tích
python scripts/story_generator.py --genre fairytale --theme friendship --output story.md

# Tạo truyện ngụ ngôn 
python scripts/story_generator.py --genre fable --theme honesty --output fable.md

# Tạo truyện thiếu nhi
python scripts/story_generator.py --genre children --theme adventure --output kids_story.md
```

### 2. Character Development (Python)
**Đường dẫn:** `scripts/character_generator.py`
**Mô tả:** Phát triển nhân vật với tính cách, ngoại hình và đặc điểm riêng

**Cách sử dụng:**
```bash
# Tạo nhân vật chính
python scripts/character_generator.py --role protagonist --type human --name Nguyen

# Tạo nhân vật phản diện
python scripts/character_generator.py --role antagonist --type magical --name EvilDragon
```

### 3. Story Structure Helper (Python)
**Đường dẫn:** `scripts/structure_helper.py`
**Mô tả:** Xây dựng cấu trúc câu chuyện theo các mô hình phổ biến

**Cách sử dụng:**
```bash
# Cấu trúc 3 hồi
python scripts/structure_helper.py --model three_act --genre fairytale

# Cấu trúc anh hùng
python scripts/structure_helper.py --model hero_journey --theme adventure
```

### 4. Vietnamese Language Validator (Python)
**Đường dẫn:** `scripts/vietnamese_validator.py`
**Mô tả:** Kiểm tra và cải thiện chất lượng tiếng Việt trong câu chuyện

**Cách sử dụng:**
```bash
# Kiểm tra ngữ pháp và từ vựng
python scripts/vietnamese_validator.py --input story.md --check grammar,vocabulary

# Gợi ý cải thiện
python scripts/vietnamese_validator.py --input story.md --suggestions
```

## Quy trình làm việc

### Workflow 1: Tạo truyện cổ tích cho trẻ em

**Mục tiêu:** Tạo một câu chuyện cổ tích dễ hiểu với bài học đạo đức

**Các bước:**
1. **[Lựa chọn chủ đề]** - Xác định bài học đạo đức muốn truyền tải (ví dụ: lòng tốt, sự trung thực, tình bạn)
2. **[Phát triển nhân vật]** - Sử dụng character_generator.py tạo nhân vật chính và phụ
3. **[Xây dựng cấu trúc]** - Dùng structure_helper.py với model three_act
4. **[Viết nội dung]** - Sử dụng story_generator.py tạo bản nháp
5. **[Kiểm tra chất lượng]** - Dùng vietnamese_validator.py kiểm tra ngôn ngữ
6. **[Chỉnh sửa hoàn thiện]** - Tinh chỉnh câu chuyện cho phù hợp độ tuổi

**Kết quả mong đợi:** Truyện cổ tích hoàn chỉnh 500-1000 từ, ngôn ngữ đơn giản, có bài học rõ ràng

**Thời gian dự kiến:** 15-20 phút

**Ví dụ:**
```bash
python scripts/story_generator.py --genre fairytale --theme honesty --output honest_woodcutter.md
python scripts/character_generator.py --role protagonist --type human --name Woodcutter
python scripts/vietnamese_validator.py --input honest_woodcutter.md --suggestions
```

### Workflow 2: Tạo truyện ngụ ngôn moral

**Mục tiêu:** Viết truyện ngụ ngôn với động vật hóa thân và bài học sâu sắc

**Các bước:**
1. **[Chọn loài vật]** - Xác định con vật đại diện cho các đặc tính cần mô tả
2. **[Tạo nhân vật]** - Phát triển tính cách và vai trò cho từng nhân vật động vật
3. **[Xây dựng câu chuyện]** - Tạo tình huống thể hiện đặc tính và dạy bài học
4. **[Viết và tinh chỉnh]** - Hoàn thiện với ngôn ngữ giàu hình ảnh
5. **[Thêm thông điệp]** - Rút ra bài học rõ ràng ở cuối câu chuyện

**Kết quả mong đợi:** Truyện ngụ ngôn 300-600 từ, có thông điệp đạo đức rõ ràng

**Thời gian dự kiến:** 10-15 phút

**Ví dụ:**
```bash
python scripts/character_generator.py --role protagonist --type animal --species ant
python scripts/character_generator.py --role antagonist --type animal --species grasshopper
python scripts/story_generator.py --genre fable --theme diligence --output ant_grasshopper.md
```

### Workflow 3: Tạo truyện phiêu lưu thiếu nhi

**Mục tiêu:** Viết câu chuyện phiêu lưu hấp dẫn cho độ tuổi 7-12

**Các bước:**
1. **[Lên kịch bản]** - Xác định thế giới giả tưởng và sứ mệnh của nhân vật
2. **[Phát triển nhân vật]** - Tạo anh hùng, người bạn đồng hành và nhân vật phản diện
3. **[Xây dựng cốt truyện]** - Sử dụng hero_journey structure
4. **[Thêm yếu tố kỳ ảo]** - Thêm phép thuật, sinh vật thần bí
5. **[Viết theo từng chương]** - Phát triển từng phần của phiêu lưu
6. **[Hoàn thiện]** - Kiểm tra tính hợp lý và hấp dẫn

**Kết quả mong đợi:** Truyện phiêu lưu 1000-2000 từ, nhiều tình tiết hấp dẫn

**Thời gian dự kiến:** 25-30 phút

**Ví dụ:**
```bash
python scripts/structure_helper.py --model hero_journey --theme adventure --output adventure_structure.md
python scripts/story_generator.py --genre children --theme quest --output magical_journey.md
```

## Định dạng.story_generator.py

**Thể loại hỗ trợ:**
- `fairytale` - Truyện cổ tích truyền thống
- `fable` - Truyện ngụ ngôn với bài học đạo đức  
- `children` - Truyện thiếu nhi hiện đại
- `adventure` - Truyện phiêu lưu mạo hiểm
- `mystery` - Truyện bí ẩn

**Chủ đề phổ biến:**
- `friendship` - Tình bạn thủy chung
- `honesty` - Sự trung thực
- `courage` - Lòng dũng cảm
- `kindness` - Lòng tốt bụng
- `perseverance` - Sự kiên trì
- `wisdom` - Trí tuệ
- `love` - Tình yêu thương

**Tùy chọn output:**
- `--format markdown` - Xuất định dạng Markdown (mặc định)
- `--format plain` - Xuất văn bản thuần
- `--format illustrated` - Thêm gợi ý hình ảnh minh họa

## Tham khảo

### Mẫu cấu trúc truyện
Xem thêm tại `references/story_structures.md` để tìm hiểu các mẫu cấu trúc phổ biến trong văn học Việt Nam và quốc tế.

### From điển hình truyện Việt
Tham khảo `references/vietnamese_folktales.md` để hiểu các mẫu truyện cổ tích đậm chất Việt Nam.

### Lưu ý về văn hóa
- Sử dụng tên và địa điểm có tính Việt Nam khi phù hợp
- Tôn trọng giá trị văn hóa và đạo đức truyền thống
- Tránh các nội dung không phù hợp với văn hóa Việt

## Chất lượng và kiểm soát

### Tiêu chí chất lượng
- Ngôn ngữ tự nhiên, phù hợp với đối tượng độc giả
- Cấu trúc câu chuyện rõ ràng, logic
- Bài học đạo đức tích cực, phù hợp
- Tính sáng tạo và hấp dẫn

### Kiểm tra nội dung
Sử dụng `vietnamese_validator.py` để đảm bảo:
- Ngữ pháp chính xác
- Từ vựng phù hợp độ tuổi
- Câu văn mạch lạc
- Không có nội dung nhạy cảm

---

**Phiên bản:** 1.0.0  
**Ngày tạo:** 2025-11-20  
**Tác giả:** Vietnamese Story Writer Skill  
**Mục đích:** Hỗ trợ sáng tác truyện tiếng Việt chất lượng cao
