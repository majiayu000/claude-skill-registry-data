---
name: justfile-syntax
description: Justfile 편집 시 인덴트/문법 규칙을 제공합니다. justfile, Justfile, 레시피 편집 시 자동으로 사용하세요.
---

# Justfile 문법 가이드

Justfile 편집 시 인덴트 규칙과 heredoc 문법을 안내합니다.

## 핵심 규칙

### 1. 기본 인덴트

레시피 본문은 **4칸 공백** (또는 탭)으로 시작합니다.

```justfile
recipe-name:
    #!/usr/bin/env bash
    echo "hello"
    if [ -f file ]; then
        cat file
    fi
```

### 2. Heredoc 규칙 (중요!)

**heredoc 내용은 인덴트 없음** - 첫 칸(column 0)부터 시작해야 합니다.

```justfile
generate-file:
    #!/usr/bin/env bash
    cat > output.txt << 'EOF'
line 1
line 2
line 3
EOF
```

**EOF 마커도 인덴트 없음** - 첫 칸에 위치해야 합니다.

### 3. 변수 치환 heredoc

변수 치환이 필요하면 따옴표 없이 EOF 사용:

```justfile
generate-config:
    #!/usr/bin/env bash
    VALUE="test"
    cat > config.txt << EOF
value=$VALUE
another=static
EOF
```

변수 치환 방지하려면 따옴표 사용:

```justfile
generate-script:
    #!/usr/bin/env bash
    cat > script.sh << 'EOF'
echo $HOME  # 이 $HOME은 치환되지 않음
EOF
```

### 4. <<- 사용 시 (탭 인덴트)

`<<-` 사용 시 **탭**으로만 인덴트 가능 (공백 불가):

```justfile
generate-file:
    #!/usr/bin/env bash
    cat > output.txt <<- 'EOF'
	line 1
	line 2
	EOF
```

> 주의: 위 예시에서 인덴트는 반드시 탭 문자여야 함

## 안티패턴

### 잘못된 예 1: heredoc 내용에 공백 인덴트

```justfile
# ❌ 잘못됨 - 공백이 파일에 포함됨
recipe:
    cat > file << 'EOF'
    line 1
    line 2
    EOF
```

### 잘못된 예 2: EOF에 인덴트

```justfile
# ❌ 잘못됨 - EOF를 찾지 못함
recipe:
    cat > file << 'EOF'
line 1
    EOF
```

### 올바른 예

```justfile
# ✅ 올바름
recipe:
    cat > file << 'EOF'
line 1
line 2
EOF
```

## 편집 체크리스트

Justfile 수정 전 확인:
- [ ] 레시피 본문: 4칸 공백 인덴트
- [ ] heredoc 내용: 인덴트 없음 (첫 칸 시작)
- [ ] EOF 마커: 인덴트 없음 (첫 칸)
- [ ] 변수 치환: 필요하면 `<< EOF`, 방지하면 `<< 'EOF'`

## 참고

- Just 공식 문서: https://github.com/casey/just
- Bash heredoc: https://tldp.org/LDP/abs/html/here-docs.html
