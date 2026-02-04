---
name: strix-halo-setup
description: Complete setup for AMD Strix Halo (Ryzen AI MAX+ 395) PyTorch environments. Handles ROCm installation verification, PyTorch community builds (official wheels don't work with gfx1151), GTT memory configuration, and environment setup. Creates ready-to-use ML workspaces for running 30B parameter models.
license: MIT
metadata:
  hardware: AMD Strix Halo (gfx1151)
  supported_rocm: "6.4.4+"
  tested_date: "2025-10-25"
  skill_version: "1.0.0"
---

# Strix Halo Setup

Set up a new PyTorch project optimized for AMD Strix Halo (Ryzen AI MAX+ 395, gfx1151).

## When Claude Should Use This Skill

This skill should be invoked when:
- Setting up PyTorch on AMD Strix Halo (Ryzen AI MAX+ 395, gfx1151) hardware
- User reports "HIP error: invalid device function" with PyTorch on AMD APU
- Configuring environments for running LLMs on AMD integrated graphics
- User mentions needing GTT memory configuration for ML workloads
- Creating a new ML project specifically for Strix Halo hardware
- User asks about running 30B parameter models on AMD Ryzen AI MAX+

## What This Skill Does

1. Verifies system configuration (ROCm, GTT, user groups)
2. Creates a conda environment with working PyTorch for gfx1151
3. Sets up proper environment variables
4. Creates test scripts to verify GPU functionality
5. Provides a complete project template with best practices

## Critical Information

**PyTorch Installation**: Official PyTorch wheels from pytorch.org **DO NOT WORK** with gfx1151. They detect the GPU but fail on compute with "HIP error: invalid device function". This skill installs community builds that actually work.

**ROCm Installation Note**: For Strix Halo APUs, ROCm should be installed with `--no-dkms` flag to use the inbox kernel driver. If you have amdgpu-dkms installed, it may cause issues when upgrading kernels.

## Prerequisites Check

Before running setup, verify the system with:

```bash
./scripts/verify_system.sh
```

This checks:
- ROCm installation (6.4.4+ or 7.0.2 required)
- User in `render` and `video` groups
- GTT memory configuration
- Python/Conda availability

If any checks fail, see `.claude/skills/strix-halo-setup/docs/TROUBLESHOOTING.md` for detailed fix instructions.

## Setup Process

### Step 1: System Verification

Run the verification script:

```bash
cd .claude/skills/strix-halo-setup
./scripts/verify_system.sh
```

Expected output:
- ✓ AMD GPU detected
- ✓ ROCm installed
- ✓ User in render/video groups
- ✓ GTT configured (or warning if not)

If issues found, follow the script's instructions to fix them.

### Step 2: Determine Project Name and Backend

Ask the user for:
1. **Project name**: If not specified, use `strix-ml-project`
2. **Backend choice**: PyTorch (training/custom code) or Vulkan (inference only)

Use the AskUserQuestion tool:

**Question 1**: "What would you like to name your project?"
**Question 2**: "Which backend do you want to set up?"
- **PyTorch with ROCm**: For training, custom code, full ML framework (supports transformers, etc.)
- **Vulkan**: For inference only (llama.cpp, Ollama) - simpler setup, often faster

If PyTorch is chosen, continue with steps below. If Vulkan, skip to Vulkan setup section at the end.

### Step 3: Create Environment

**Using Conda (Recommended)**:
```bash
# Create new environment with Python 3.14 (or 3.13)
conda create -n {project_name} python=3.14 -y
conda activate {project_name}
```

**Using uv (Alternative)**:
```bash
# Create new environment with Python 3.14 (or 3.13)
uv venv {project_name} --python 3.14
source {project_name}/bin/activate
```

### Step 4: Install PyTorch (Community Build)

**CRITICAL**: Must use community builds, not official wheels.

**Option 1: AMD Nightlies (Recommended)**
```bash
pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch torchvision torchaudio
```

**Option 2: scottt's Stable Builds (Fallback)**
If nightlies fail, use pre-built wheels from:
https://github.com/scottt/rocm-TheRock/releases

Download and install with `pip install <wheel_file>`.

**Verify Installation**:
```bash
python -c "import torch; print('PyTorch:', torch.__version__); print('HIP:', torch.version.hip)"
```

Should show PyTorch 2.7+ and HIP 6.5+.

### Step 5: Configure Environment Variables

Create activation script in the conda environment:

```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d

cat > $CONDA_PREFIX/etc/conda/activate.d/strix_halo_env.sh << 'EOF'
#!/bin/bash

# Core ROCm settings for Strix Halo (gfx1151)
export HSA_OVERRIDE_GFX_VERSION=11.5.1
export PYTORCH_ROCM_ARCH=gfx1151

# Unified Memory Configuration - CRITICAL for accessing full memory
export HSA_XNACK=1
export HSA_FORCE_FINE_GRAIN_PCIE=1

# Memory allocation settings
export GPU_MAX_HEAP_SIZE=100
export GPU_MAX_ALLOC_PERCENT=100

# Device visibility
export ROCR_VISIBLE_DEVICES=0
export HIP_VISIBLE_DEVICES=0

# Performance optimizations
export ROCBLAS_USE_HIPBLASLT=1
export AMD_LOG_LEVEL=0
export HSA_CU_MASK=0xffffffffffffffff

echo "✓ Strix Halo environment variables set"
EOF

chmod +x $CONDA_PREFIX/etc/conda/activate.d/strix_halo_env.sh
```

Create deactivation script:

```bash
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

cat > $CONDA_PREFIX/etc/conda/deactivate.d/strix_halo_env.sh << 'EOF'
#!/bin/bash

unset HSA_OVERRIDE_GFX_VERSION PYTORCH_ROCM_ARCH HSA_XNACK HSA_FORCE_FINE_GRAIN_PCIE
unset GPU_MAX_HEAP_SIZE GPU_MAX_ALLOC_PERCENT ROCR_VISIBLE_DEVICES HIP_VISIBLE_DEVICES
unset ROCBLAS_USE_HIPBLASLT AMD_LOG_LEVEL HSA_CU_MASK
EOF

chmod +x $CONDA_PREFIX/etc/conda/deactivate.d/strix_halo_env.sh
```

### Step 7: Create Project Structure

```bash
mkdir -p {project_name}/{scripts,notebooks,data,models,tests}
cd {project_name}
```

### Step 8: Copy Test Scripts

Copy the test scripts from the skill directory:

```bash
cp .claude/skills/strix-halo-setup/scripts/*.py scripts/
chmod +x scripts/*.py
```

### Step 9: Create Project README

Create a README with project-specific information:

```bash
cat > README.md << 'EOF'
# {Project Name}

PyTorch project optimized for AMD Strix Halo (gfx1151).

## Environment

- **Hardware**: AMD Strix Halo (gfx1151)
- **ROCm**: 6.4.2+
- **PyTorch**: Community build for gfx1151
- **Python**: 3.12

## Setup

```bash
# Activate environment
conda activate {project_name}

# Verify GPU
python scripts/test_gpu_simple.py

# Test memory capacity
python scripts/test_memory.py
```

## Hardware Capabilities

- **Compute**: ~7 TFLOPS FP32, ~12 TFLOPS BF16
- **Memory**: Up to 113GB GPU-accessible (with GTT configuration)
- **Model Capacity**: 30B parameter models in FP16

## Best Practices

1. **Use BF16** for 1.6x speedup over FP32
2. **Keep batch size small** (1-4) for inference
3. **Data in VRAM is faster** than GTT memory
4. **Monitor memory**: `rocm-smi --showmeminfo gtt`

## Troubleshooting

If compute fails with "HIP error: invalid device function":
- You're using official PyTorch wheels (don't work with gfx1151)
- Reinstall: `pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch`

For more help, see `.claude/skills/strix-halo-setup/docs/COMPLETE_GUIDE.md`

Created: {date}
EOF
```

### Step 10: Verify Installation

Reactivate the environment to load variables:

```bash
conda deactivate
conda activate {project_name}

# Should see: "✓ Strix Halo environment variables set"
```

Run verification:

```bash
python scripts/test_gpu_simple.py
```

**Expected output:**
```
============================================================
STRIX HALO GPU TEST
============================================================
✓ GPU detected: AMD Radeon Graphics
  Memory: 113.2 GB
  Compute test successful
✓ ALL TESTS PASSED
============================================================
```

### Step 11: Final Summary

Tell the user:

```
✓ Setup complete! Your Strix Halo environment is ready.

Project: {project_name}
Location: {full_path}

Next steps:
  1. Test GPU: python scripts/test_gpu_simple.py
  2. Test memory: python scripts/test_memory.py
  3. Try a model: See docs/COMPLETE_GUIDE.md for examples

Hardware capabilities:
  - 7-12 TFLOPS compute (FP32/BF16)
  - 113 GB GPU-accessible memory
  - Can run 30B parameter models in FP16

Activate anytime with: conda activate {project_name}
```

## Success Criteria

All of these should pass:
- ✓ PyTorch detects GPU
- ✓ Compute operations succeed (no HIP errors)
- ✓ Can allocate 30GB+ memory
- ✓ BF16 operations work

## Common Issues

### Issue: "HIP error: invalid device function"

**Cause**: Using official PyTorch wheels (don't work with gfx1151)

**Solution**:
```bash
pip uninstall torch torchvision torchaudio
pip install --index-url https://rocm.nightlies.amd.com/v2/gfx1151/ --pre torch torchvision torchaudio
```

**Verify it worked**:
```bash
python -c "import torch; a=torch.tensor([1.0]).cuda(); print('✓ Works:', (a+1).item())"
```

### Issue: Out of memory below 30GB

**Cause**: GTT not configured (limited to ~33GB)

**Solution 1**: Upgrade to kernel 6.16.9+ (no configuration needed)

**Solution 2**: For older kernels, configure GTT:
```bash
.claude/skills/strix-halo-setup/scripts/configure_gtt.sh
```

This adds kernel parameters to GRUB for GPU to access more system RAM.

### Issue: GPU not detected

**Cause**: User not in render/video groups

**Solution**:
```bash
sudo usermod -aG render,video $USER
# Log out and back in (or reboot)
groups | grep -E "render|video"  # Verify
```

## References

- **Complete Guide**: `.claude/skills/strix-halo-setup/docs/STRIX_HALO_COMPLETE_GUIDE.md`
- **Troubleshooting**: `.claude/skills/strix-halo-setup/docs/TROUBLESHOOTING.md`
- **GTT Configuration**: `.claude/skills/strix-halo-setup/docs/GTT_MEMORY_FIX.md`
- **Community PyTorch**: https://github.com/scottt/rocm-TheRock/releases

---

## Vulkan Setup (Alternative to PyTorch)

If the user chose Vulkan for inference-only workloads:

### Step V1: Install Vulkan Drivers

```bash
sudo apt install mesa-vulkan-drivers vulkan-tools
```

### Step V2: Verify Vulkan

```bash
vulkaninfo | grep "deviceName"
# Should show: AMD Radeon Graphics or similar
```

### Step V3: Install Inference Tools

**For llama.cpp**:
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make LLAMA_VULKAN=1
```

**For Ollama**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step V4: Test Vulkan

```bash
# With llama.cpp
./llama-cli -m /path/to/model.gguf -ngl 99 --gpu-backend vulkan

# With Ollama
ollama run llama2
```

### Vulkan Summary

Tell the user:
```
✓ Vulkan setup complete!

Backend: Vulkan (inference only)
Use with: llama.cpp, Ollama, other Vulkan-enabled tools

Note: Vulkan often provides better performance for inference than ROCm/HIP.
For training or custom PyTorch code, set up PyTorch instead.
```

---

## References

- **Troubleshooting**: `.claude/skills/strix-halo-setup/docs/TROUBLESHOOTING.md`
- **GTT Configuration**: `.claude/skills/strix-halo-setup/docs/GTT_MEMORY_FIX.md`
- **Community PyTorch**: https://github.com/scottt/rocm-TheRock/releases

## Notes

- GTT configuration needed for 30B+ models on kernels before 6.16.9 (kernel 6.16.9+ has automatic UMA support)
- Vulkan backend often provides better performance for inference
- Use BF16 precision in PyTorch for better performance
