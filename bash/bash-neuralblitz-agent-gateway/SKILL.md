---
name: bash
description: Bash shell scripting for automation, system administration, and command-line productivity
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: scripting
---
## What I do
- Write bash scripts for automation
- Process text with awk and sed
- Use find and xargs effectively
- Handle command-line arguments
- Manage environment variables
- Implement error handling
- Create utility functions

## When to use me
When automating tasks, building CLI tools, or managing systems.

## Basics
```bash
#!/bin/bash

# Variables
name="World"
echo "Hello, $name!"

# Command substitution
current_date=$(date +%Y-%m-%d)
files=$(ls)

# Arrays
colors=("red" "green" "blue")
echo "${colors[0]}"
echo "${colors[@]}"

# Dictionaries (bash 4+)
declare -A config
config[host]="localhost"
config[port]="8080"
echo "${config[host]}"
```

## Conditionals
```bash
# If statement
if [ "$name" == "admin" ]; then
    echo "Welcome admin"
elif [ "$age" -ge 18 ]; then
    echo "Adult"
else
    echo "Minor"
fi

# File tests
if [ -f "$file" ]; then
    echo "Regular file"
fi
if [ -d "$dir" ]; then
    echo "Directory"
fi
if [ -z "$var" ]; then
    echo "Empty"
fi

# String comparison
if [[ "$str" == *"pattern"* ]]; then
    echo "Contains pattern"
fi
```

## Loops
```bash
# For loop
for i in {1..5}; do
    echo "Number: $i"
done

for file in *.txt; do
    echo "Processing $file"
done

# While loop
while read line; do
    echo "$line"
done < file.txt

# Iterate over array
for color in "${colors[@]}"; do
    echo "$color"
done
```

## Functions
```bash
function greet() {
    local name="$1"  # local variable
    echo "Hello, $name!"
}

greet "World"

# Return value
function get_sum() {
    local a=$1
    local b=$2
    echo $((a + b))
}

result=$(get_sum 5 10)
```

## Arguments
```bash
#!/bin/bash

# $@ = all arguments
# $# = argument count
# $0 = script name
# $1, $2, ... = arguments

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            help=true
            ;;
        -n|--name)
            name="$2"
            shift 2
            ;;
        -v|--verbose)
            verbose=true
            shift
            ;;
        *)
            echo "Unknown: $1"
            shift
            ;;
    esac
done
```

## Error Handling
```bash
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Pipeline fails on error

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Check command success
if ! command -v git &> /dev/null; then
    echo "Git not found"
    exit 1
fi
```

## Text Processing
```bash
# Awk
awk -F',' '{print $1, $3}' file.csv
awk 'NR>1 {sum+=$2} END {print sum}' file.txt

# Sed
sed 's/old/new/g' file.txt
sed -i 's/old/new/g' file.txt  # in-place
sed '/pattern/d' file.txt  # delete lines with pattern

# Find
find . -name "*.txt" -type f
find . -mtime -7  # modified in last 7 days
find . -size +1M  # larger than 1MB

# xargs
find . -name "*.log" -type f | xargs rm
find . -name "*.txt" | xargs -I {} mv {} ./backup/
```

## Useful Patterns
```bash
# Check if command exists
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }

# Heredoc
cat << EOF > config.txt
name=$name
value=$value
EOF

# Parallel execution
cat hosts | xargs -P 10 -I {} ssh {} 'uptime'

# Progress bar
for i in {1..100}; do
    echo -ne "Progress: $i%\r"
    sleep 0.1
done
```
