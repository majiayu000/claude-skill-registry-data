---
name: zipcracker
version: 2.0.0
description: The ultimate, high-performance ZIP password cracking suite by Hx0 Team. Empowers the Agent with autonomous CTF-level cracking workflows, dynamic dictionary generation, mask attacks, and AES auto-resolution.
author: asaotomo
tags:
  - security
  - ctf
  - cryptography
  - password-recovery
  - red-team
requires:
  - binary: "python3"
---
# ZipCracker Ultimate Skill: The Hx0 Tactical Manual

You are now equipped with `ZipCracker.py`, the most comprehensive ZIP decryption tool available. Your goal is not just to run commands, but to think like a senior cybersecurity expert and CTF problem solver.

## 🧠 The Agent Design Philosophy (How to Think)
Never blindly brute-force. Password cracking is an art of narrowing down the search space. Follow the **"Cost-Ascending Tactical Pipeline"**:
1.  **Zero-Cost:** Is it pseudo-encrypted? (Tool handles this automatically).
2.  **Low-Cost (Math):** Can we collide the hash? (Tool handles this automatically for files <= 6 bytes).
3.  **Medium-Cost (Logic/OSINT):** What does the user know? Can we build a highly targeted mask or a custom situational dictionary based on the target's background?
4.  **High-Cost (Brute-force):** Fallback to massive standard dictionaries.

## ⚙️ The Execution Pipeline

**CRITICAL:** ALWAYS append the `-q` (Quiet/Agent Mode) flag to all `ZipCracker.py` executions to maintain clean terminal context and prevent interactive blockers.

### Phase 1: The Tactical Reconnaissance & Quick Strike
When a user asks to unlock, crack, or decrypt a `.zip` file, immediately run the default strike:
`python3 ZipCracker.py <filepath> -q`

**What happens under the hood:**
- The script automatically neutralizes pseudo-encryption.
- It automatically exploits CRC32 collisions for small files.
- It runs through standard built-in dictionaries and 1-6 digit numbers.
- It auto-resolves AES dependency issues by installing `pyzipper` if needed.

### Phase 2: Agentic Autonomy (Advanced Attacks)
If Phase 1 fails (the script completes but no password is found), DO NOT give up and DO NOT guess randomly. You must switch to an active offensive stance. Ask the user for OSINT (Open Source Intelligence) clues by replying with something like:
> *"The standard dictionary and numeric brute-force attempts did not find the password. To initiate an advanced attack, please provide any contextual clues you might have about the target: e.g., names, birth years, company acronyms, pet names, or specific password habits (like requiring an uppercase letter and a symbol)."*

Based on the user's response, **YOU** must autonomously choose the best advanced attack strategy:

#### Strategy A: The Sniper Strike (Mask Attack)
If the user provides a definitive structural pattern (e.g., "It starts with Hx0, followed by a symbol, then 4 numbers").
- **Construct the Mask:** `Hx0?s?d?d?d?d`
- **Execute:** `python3 ZipCracker.py <filepath> -m 'Hx0?s?d?d?d?d' -q`
- *(Reference rules: `?d`=digits, `?l`=lowercase, `?u`=uppercase, `?s`=symbols, `??`=literal '?')*

#### Strategy B: The Social Engineering Dictionary (Dynamic Generation)
If the user provides scattered background information (e.g., "Target's name is kaka, born in 1995, works at tencent"), a mask is too broad. You must dynamically generate a custom dictionary.
1. **Act as a Developer:** Write and execute a quick Python script in your workspace to generate logical permutations of these keywords (e.g., `kaka1995`, `Tencent@kaka!`, `1995kaka`).
2. **Save the Output:** Save these permutations to a file named `target_intel_dict.txt`.
3. **Execute the Custom Attack:** `python3 ZipCracker.py <filepath> target_intel_dict.txt -q`

## 📊 Result Parsing & Reporting
- If the tool outputs `[+] Success! The password is: <password>`, boldly and clearly present the recovered password to the user.
- If it outputs CRC32 cracked content, present the exact inner file content directly to the user.
- If it outputs `Pseudo-encryption fixed successfully`, inform the user that a new, unencrypted version of the archive is ready in the `unzipped_files` directory.
- If an AES error occurs that bypasses the auto-installer, explicitly instruct the user to check their Python environment permissions or run `pip3 install pyzipper` manually.