---
name: runtime_migration
description: 将用户合法拥有或已获授权的 CUDA 应用中的 Runtime 层迁移到 CANN Runtime，包括 API、类型、错误码、初始化、内存、stream、event、IPC、构建配置和兼容层适配。仅在处理 Runtime 层迁移或可行性分析时使用；不迁移 CUDA kernel、device helper 或任何算子实现。
---
# CUDA Runtime 迁移到 CANN Runtime 指南

## 授权与使用边界

本技能仅用于帮助用户将其自身合法拥有或已获授权的代码资产延伸与适配至 CANN 计算架构。用户应确保对被适配代码享有合法权利，或已取得相应授权。

本技能不用于、也不鼓励在未获授权的情况下复制、翻译或转换第三方代码。若用户明确表示代码属于第三方且未取得授权，或请求规避许可证、版权声明、访问控制、商业限制等，应拒绝执行迁移，并建议用户先取得权利人的许可或授权。

## 概述

在满足上述授权与使用边界的前提下，本技能只负责将 CUDA 应用程序的 Runtime 层迁移到华为昇腾 NPU 的 CANN Runtime。基于 `assets/src` 目录下的兼容层源码，提供两种迁移方式：

1. **兼容层方式**：替换头文件并链接兼容库，最小代码修改
   说明：默认使用兼容层方式,除非用户明确要求“直接迁移方式、直接改成 CANN API”， 并遵守以下约束：
    - **尽量保持用户源码不变**：优先只替换 include、构建配置和 CUDA 编译器专用语法；不要无故重写控制流、变量名、输出文本、错误处理风格。
    - **不要主动引入新风格**：原代码没有 `CUDA_CHECK`、RAII、异常、封装类、`std::vector` 改写时，不要为了“更规范”而加入。
    - **CANN 细节不泄漏到业务源码**：兼容层方式下，业务源码不应直接 include `acl/acl.h`、`aclnnop/*.h`，也不应自己创建/销毁 `aclTensor`、`aclScalar`、workspace。
    - **缺失能力补兼容层，不堆到样例里**：遇到 `cann_runtime_compat.h` 没覆盖的能力，优先在 `assets/src` 下补兼容 API/适配函数，再让业务代码调用该 compat 接口。
    - **严格限定 Runtime 边界**：`cudaMalloc/cudaMemcpy/cudaFree` 等 Runtime API 可由兼容层映射；CUDA kernel、device helper 和算子实现不属于本技能，不得在本技能内部迁移或调用其他算子迁移 skill。
    - **Kernel 启动默认 Host fallback**：当源代码包含 `kernel<<<...>>>` 时，将 kernel body 的等价 CPU 实现隔离为独立函数，并默认通过 `cudaCompatLaunchHostKernel()` 调用。必须在代码注释、README 或迁移报告中明确记录：该路径在 Host/CPU 上执行，仅用于维持流程和验证 Runtime 层，不是 NPU kernel 执行，也不能用于 NPU kernel 性能或设备侧正确性结论。
    - **每次迁移都要编译并运行最小验证**：不能只改代码不验证；如机器有坏卡或需指定设备，用环境变量如 `ASCEND_RT_VISIBLE_DEVICES` 限制可见设备。

2. **直接迁移方式**：将 CUDA API 调用改写为 CANN Runtime API, 
  说明： 直接迁移方式适用于需要深度适配或优化的场景，或应用使用部分不支持 API 需自定义实现的情况。直接迁移方式下，程序需要将 CUDA API 调用改写为 CANN Runtime API 调用，并处理参数差异、错误码映射等细节。直接迁移方式的改写步骤包括：
   - API 映射对照：参考 `references ` 中的 API 支持状态表、接口文档等文件，了解哪些 CUDA API 有对应的 CANN API 支持，不支持的接口如何处理，并查看 `assets/src` 中的实现示例。
   - 类型映射：了解 CUDA 类型与 CANN 类型的映射关系，如 `cudaStream_t` 映射为 `aclrtStream`。
   - 错误码转换：参考 `references/error_mapping.md` 进行错误码映射，将 CANN 错误码转换为 CUDA 错误码。  
   - 初始化/清理：CANN 需要显式初始化和清理，改写代码时需要添加 `aclInit` 和 `aclFinalize` 调用。
   - 必要时联网查询 CANN API 文档，了解最新的接口变更和使用建议。


## 迁移流程

按照以下步骤执行迁移：

### Step 1: 使用边界检查

用户应确保对所转换的代码享有合法权利，或已取得相应授权。一般情况下，不因授权状态重复询问用户，按正常迁移流程继续。

当用户表示代码可能属于第三方、请求处理闭源/受限材料，或上下文出现明显疑似侵权、许可不明、访问受限等风险信号时，应先简短询问权利来源或授权情况；在用户确认具备合法权利或授权后，方可继续迁移。

当用户明确表示代码属于第三方且未取得授权，或请求规避许可证、版权声明、访问控制、商业限制，或要求移除、弱化、隐藏版权/许可证/NOTICE/作者署名等归属信息时，应拒绝执行相关迁移或改写，并建议用户先取得权利人的许可或授权。

迁移过程中不得移除、弱化、隐藏或规避原代码中的版权、许可证、NOTICE、作者署名或其他归属信息。

### Step 2: 迁移可行性分析

分析应用程序使用的 CUDA API 是否有对应的 CANN 接口支持。

#### 2.1 识别 CUDA API 使用情况

使用以下方法扫描用户代码：

```bash
# 扫描 CUDA Runtime API 调用
grep -E "cuda[A-Z][a-zA-Z]+\(" --include="*.c" --include="*.cpp" --include="*.cu"

# 扫描 CUDA Driver API 调用
grep -E "cu[A-Z][a-zA-Z]+\(" --include="*.c" --include="*.cpp" --include="*.cu"

# 扫描头文件依赖
grep -E "#include.*cuda(_runtime|\.h)" --include="*.c" --include="*.cpp" --include="*.cu"
```

#### 2.2 API 支持状态检查

对照以下支持状态表判断可行性：


| API 类别            |  支持状态  | 说明                                                      |
| ------------------- | :---------: | --------------------------------------------------------- |
| **设备管理**        | ✅ 完全支持 | cudaGetDeviceCount, cudaSetDevice 等 16 个 API            |
| **内存管理**        | ✅ 基本支持 | cudaMalloc, cudaMemcpy, cudaHostAlloc, cudaMemcpyToSymbol 等 API；Managed Memory 基础接口按 CANN UVM 产品能力条件支持 |
| **流管理**          | ✅ 完全支持 | cudaStreamCreate, cudaStreamSynchronize, capture info 等 API |
| **事件管理**        | ✅ 完全支持 | cudaEventCreate, cudaEventRecord, cudaEventRecordWithFlags 等 API |
| **IPC**             | ✅ 完全支持 | cudaIpcGetMemHandle 等 5 个 API (注意 key/opaque handle 约束) |
| **库/模块管理**     | ✅ 完全支持 | cudaLibraryLoadFromFile、cuModuleLoad、cuModuleGetFunction 等 API |
| **内存池/UVM**        | ⚠️ 部分支持 | CUDA Managed Memory 基础分配、advise、prefetch、range attribute 查询按 CANN UVM 产品能力条件支持；CUDA SOMA 和 discard batch 类 UVM 扩展仍返回 cudaErrorNotSupported |
| **Occupancy/Cooperative/高级 Graph/Driver JIT/Green Context/Multicast/Tensor Map** | ⚠️ 不支持 | 返回 cudaErrorNotSupported 或 CUDA_ERROR_NOT_SUPPORTED |
| **Texture/Surface** |  ❌ 不支持  | 需额外适配层                                              |
| **Driver VMM/Context** | ✅ 完全支持 | cuMemCreate, cuMemMap, cuCtxGetCurrent, cuCtxSetCurrent 等 API |

具体 API 映射和支持状态以 `references/api_support_table.md` 为准；需要核对接口语义时，继续查阅 `references/cuda_api_common.md` 和 `references/cann_api_common.md`。Graph/Stream capture 相关能力基于 CANN Model RI，部分接口为试验特性，不应承诺生产可用或长期 ABI 稳定。`cudaGraphAddNode` 仅支持 `cudaGraphNodeTypeConditional` 特例并映射到 `aclmdlRIAddCondTask`，其他 node type 仍按不支持处理；`cudaGraphNodeGetDependencies`、`cudaStreamUpdateCaptureDependencies` 当前不支持。CUDA SOMA/UVM 不得误标为完整支持；Managed Memory 基础接口只能按 CANN UVM 产品能力条件支持并允许明确 `SKIP`，内存池、异步分配和 discard batch 类 UVM 扩展保持 not supported，且不进入转测验收。

#### 2.3 输出可行性分析报告

报告包含：

- 使用到的 CUDA API 清单
- API 支持状态（支持/不支持/Mock）
- 不支持 API 的替代方案建议
- 迁移可行性结论

---

### Step 3: 迁移方式选择

根据分析结果，推荐或让用户选择迁移方式。

如果代码中存在 CUDA Kernel 启动语法 `kernel<<<...>>>(...)`，不要迁移 kernel 或依赖其他算子迁移 skill。默认采用 Host fallback：将 kernel body 的等价 CPU 实现隔离成函数，通过 `cudaCompatLaunchHostKernel()` 调用，并在迁移报告中醒目标注“Host/CPU fallback，不是 NPU kernel 执行”。如果用户需要 NPU 设备侧算子实现或性能验证，将该需求列为本技能范围外的后续工作，由独立的算子 skill 处理。

#### 3.1 兼容层方式（推荐）

**适用场景**：

- 应用主要使用已支持的 CUDA Runtime API
- 希望最小化代码修改
- 快速验证迁移可行性

**优点**：

- Drop-in replacement，仅替换头文件
- 无需修改业务逻辑代码
- 自动初始化/清理（constructor/destructor）

**修改点**：

```c
// 原代码
#include <cuda_runtime.h>

// 迁移后
#include "cann_runtime_compat.h"
```

**编译链接**：

```bash
# 编译兼容层库（在 assets/src 目录）
cd assets/src
mkdir -p build && cd build
cmake .. && make

# 编译并链接用户应用
cd your_app_dir
gcc -I/path/to/runtime_migration/assets/src \
    your_code.c \
    -L/path/to/runtime_migration/assets/src/build -lcudacompat \
    -L~/Ascend/cann/lib64 -lacl_rt -lc_sec \
    -o your_app
```

#### 3.2 直接迁移方式

**适用场景**：

- 需要深度适配或优化
- 应用使用部分不支持 API，需自定义实现
- 希望直接使用 CANN Runtime 特性

**修改点**：

```c
// 原代码
cudaMalloc(&ptr, size);
cudaMemcpy(dst, src, size, cudaMemcpyHostToDevice);

// 迁移后
aclrtMalloc(&ptr, size, ACL_MEM_MALLOC_HUGE_FIRST);
aclrtMemcpy(dst, size, src, size, ACL_MEMCPY_HOST_TO_DEVICE);
```

#### 3.3 混合方式

部分代码使用兼容层，部分代码直接调用 CANN API，不推荐此方式。

---

### Step 4: 应用代码改写迁移

根据选择的迁移方式执行代码改写。

#### 4.1 兼容层方式改写步骤

##### 4.1.1 头文件替换

```c
// 替换 CUDA 头文件
// 原：#include <cuda_runtime.h>
// 原：#include <cuda.h>
// 新：#include "cann_runtime_compat.h"
```

##### 4.1.2 初始化适配

兼容层自动初始化，但静态链接需添加：

```c
#include "cann_runtime_compat.h"

int main() {
    CUDA_COMPAT_FORCE_LINK();  // 仅静态链接时需要
    // ... 业务代码 ...
}
```

内存、Host register、stream/event 等依赖 CANN Runtime context 的 API 应确保有当前 device。兼容层会在内存类 API 首次调用时尝试补齐默认 `aclrtSetDevice(0)`，以贴近 CUDA Runtime 的隐式默认设备行为；迁移独立验证程序或样例时仍建议在 `main` 开始显式调用 `cudaSetDevice(0)` 或按用户指定设备调用 `cudaSetDevice(device)`，这样坏卡、多卡可见性和 `ASCEND_RT_VISIBLE_DEVICES` 场景更容易定位。

##### 4.1.3 错误处理适配

```c
// 使用 CUDA_CHECK 宏
CUDA_CHECK(cudaMalloc(&ptr, size));

// 或使用原有 CUDA 错误检查逻辑（兼容层返回 cudaError_t）
cudaError_t err = cudaMalloc(&ptr, size);
if (err != cudaSuccess) {
    printf("Error: %s\n", cudaGetErrorString(err));
}
```

##### 4.1.4 Kernel 启动适配

CUDA Kernel 启动语法需要单独处理：

```c
// 原 CUDA Kernel 启动
kernel<<<grid, block, shared_mem, stream>>>(args);

// 不能由普通 C++ 兼容头直接保留；本技能默认改写为 Host fallback。
```

**使用 Host fallback 验证 Runtime 兼容性**

当源代码包含 CUDA Kernel 启动语法时：

- 不要把 fallback 计算直接散落在主流程里
- 将 CUDA kernel body 的等价 Host fallback 隔离成独立函数
- 通过 `cudaCompatLaunchHostKernel()` 调用该 fallback，保留主流程中的“launch”语义
- 对 `cudaLaunchKernel(func, grid, block, args, ...)` 的 host fallback，按 CUDA 参数数组语义解析 `args`：`args[i]` 是第 i 个实参的地址，不能把 `args` 或 `args[i]` 本身直接当成设备指针写入。
- 如果源代码对已迁移为 Host fallback 的 CUDA kernel 调用 `cudaFuncGetAttributes`，改为调用 `cudaCompatFuncGetHostFallbackAttributes(&attrs)`；不要把 Host fallback 函数指针强行传给 `aclrtGetFunctionAttribute`。
- `cudaFuncGetName`、`cudaFuncGetParamCount`、`cudaFuncGetParamInfo`、`cudaLaunchKernelEx`、`cudaOccupancyAvailableDynamicSMemPerBlock` 的 CANN 成功路径必须使用 CANN Runtime 可识别的真实 `aclrtFuncHandle`，例如由 CANN binary/module 加载流程取得的 handle。迁移验证用例不得用 `reinterpret_cast<void *>(0x1)`、普通 host 函数指针、CUDA `__global__` 函数指针或 Host fallback 函数指针探测这些接口的成功路径；无真实 handle 时只保留空指针、非法配置等错误路径，并把成功路径写成明确 `SKIP - requires a real CANN aclrtFuncHandle`。
- 在调用处添加注释，并在 README 或迁移报告中明确说明该路径在 Host/CPU 上执行，不是 NPU kernel 执行
- 不使用 Host fallback 的结果声称已完成 NPU kernel 迁移、设备侧正确性验证或性能验证
- 如需 NPU 设备侧实现，将其记录为本技能范围外事项，交由独立算子 skill 处理；本技能不得内部依赖或调用该 skill

当只验证 CUDA 版本升级引入的少量 Runtime API 签名、返回码或参数约束时，不要把完整 `apiRuntimeCoverage_cuda.cu` 直接作为 CANN 转测产物。应按本轮接口范围生成最小 CANN smoke，只保留目标 API 的基本成功/错误路径和数据校验；`cudaLaunchKernelEx`、`cudaFuncGet*`、`cudaLaunchHostFunc*` 等依赖真实 CANN function handle 或 host callback 同步/销毁语义的专项路径，除非本轮目标正是验证这些能力，否则不要混入 batch copy、managed memory、capture info 等接口的基本场景验收，避免无关挂死遮蔽真正结论。若目标正是验证 function handle 类 API，也必须先准备真实 CANN binary/function handle；没有真实 handle 时，生成的 CANN 用例只能验证错误路径和条件 `SKIP`，不能伪造 handle。

##### 4.1.5 Device Symbol / PTX Module Host Fallback

CUDA `__device__` symbol 和 PTX 文本都属于 CUDA 设备侧资产，不能在 Runtime skill 中伪装成 NPU kernel 或 CANN binary。兼容层方式迁移时按以下规则处理：

- 源代码中的 `__device__ T symbol` 在迁移产物中改为普通 Host 变量 `T symbol`，保留变量名，便于 `cudaMemcpyToSymbol(symbol, ...)` 和 `cudaGetSymbolAddress(..., symbol)` 继续按 CUDA 写法编译。
- `cudaMemcpyToSymbol(symbol, src, count, ...)`、`cudaGetSymbolAddress(&ptr, symbol)`、`cudaMemcpyFromSymbol(dst, symbol, ...)` 由兼容层 C++ 重载提供 device backing；这是 Host fallback 语义，用于验证 Runtime symbol API 流程，不代表完成 CANN 设备侧全局变量迁移。
- 如果源代码内嵌 PTX 字符串或把 PTX 写入临时文件后调用 `cuModuleLoadData/cuModuleLoad/cuModuleGetFunction/cuModuleUnload`，兼容层识别 PTX 文本并创建 host fallback module handle，保持 Driver module API 流程可运行；真实 CANN ELF/二进制仍走 `aclrtBinaryLoadFromData/aclrtBinaryLoadFromFile`。
- 不得把 PTX 文本直接传给 CANN binary loader 作为验收成功路径；如果用户要求真实 NPU kernel 执行，需要另行提供 CANN 可加载二进制或交由算子迁移流程处理。

##### 4.1.6 Conditional Graph / Model RI 适配

迁移 CUDA conditional graph 时使用兼容层实现，不要把 CANN RI 细节散落到业务代码中。规则如下：

- `cudaGraphConditionalHandleCreate` 映射到 `aclmdlRICondHandleCreate`，要求 graph 来自 active stream capture 或兼容层可识别的 Model RI。
- `cudaGraphAddNode` 只有 `cudaGraphNodeTypeConditional` 特例映射到 `aclmdlRIAddCondTask`；`cudaGraphCondTypeIf/While/Switch` 分别映射到 `ACL_MODEL_RI_COND_TYPE_IF/WHILE/SWITCH`。非 conditional node type 不得宣称支持。
- `cudaStreamBeginCaptureToGraph` 映射到 `aclmdlRICaptureToModelRIBegin`，用于捕获 conditional node 输出的 body graph；不能用空 capture 作为能力验收。
- `cudaStreamGetCaptureInfo` / `cudaStreamGetCaptureInfo_v3` 映射到 `aclmdlRICaptureGetInfo`，并由兼容层记录 graph 与 capture stream 的关联。
- CUDA 侧 `cudaGraphSetConditional` 是 device-side 函数；迁移到 CANN Runtime 兼容层时，通过 `aclmdlRICondHandleGetCondPtr` 获取条件指针，再用 runtime 写入操作在 body capture 内更新条件值。验收用例必须通过输出结果证明 conditional body 真正执行。
- `cudaGraphNodeGetDependencies`、`cudaStreamUpdateCaptureDependencies`、`cudaStreamUpdateCaptureDependencies_v2` 当前没有 CANN 对标，迁移代码不能依赖这些接口完成验收；如输入依赖这些接口，应报告 not supported 或重构为不依赖 dependency update 的 capture 流程。

##### 4.1.7 Host Register / Zero-Copy 适配

迁移包含 `cudaHostRegister`、`cudaHostGetDevicePointer`、`cudaHostUnregister` 或 CUDA Samples `simpleZeroCopy` 的用例时，按以下规则处理：

- `cudaHostRegister` 映射到 `aclrtHostRegisterV2`，`cudaHostGetDevicePointer` 映射到 `aclrtHostGetDevicePointer`，`cudaHostUnregister` 映射到 `aclrtHostUnregister`；调用前保留 CUDA 侧空指针、zero size 和 flags 校验。
- `cudaHostRegisterMapped` 需要转换为 `ACL_HOST_REG_MAPPED | ACL_HOST_REG_PINNED`；若源内存已由 `cudaMallocHost` / `aclrtMallocHost` 得到，可只做 mapped 注册验证；若源内存来自 `malloc`/`posix_memalign`，仍按 CUDA 原语义注册为 pinned+mapped。
- CANN Host register/get pointer 依赖当前 device/context。兼容层内存入口会自动补默认 device，但生成独立样例时应优先在 `main` 入口显式 `cudaSetDevice(0)`，并允许用户通过 `ASCEND_RT_VISIBLE_DEVICES` 控制实际设备。
- `simpleZeroCopy.cu` 的 `vectorAddGPU<<<...>>>` 不属于 Runtime API 迁移范围。迁移该样例用于验证 Host register 能力时，应把 kernel 结果校验改为独立 Host fallback，并明确记录它只验证 Runtime wrapper、不是 NPU kernel 执行。

##### 4.1.8 Device Limit / Atomic Capability 适配

迁移包含 `cudaDeviceSetLimit`、`cudaDeviceGetLimit`、`cudaDeviceGetHostAtomicCapabilities`、`cudaDeviceGetP2PAtomicCapabilities` 的用例时，按以下规则处理：

- `cudaDeviceSetLimit` 映射到 `aclrtDeviceSetLimit`，`cudaDeviceGetLimit` 映射到 `aclrtDeviceGetLimit`。当前只把 `cudaLimitStackSize` 转换为 `ACL_RT_DEV_LIMIT_SIMD_STACK_SIZE`，把 `cudaLimitPrintfFifoSize` 转换为 `ACL_RT_DEV_LIMIT_SIMD_PRINTF_FIFO_SIZE_PER_CORE`。
- `cudaLimitMallocHeapSize`、`cudaLimitDevRuntimeSyncDepth`、`cudaLimitDevRuntimePendingLaunchCount`、`cudaLimitMaxL2FetchGranularity`、`cudaLimitPersistingL2CacheSize` 当前没有等价 CANN Runtime limit，兼容层返回 `cudaErrorUnsupportedLimit`；迁移用例不能把这些 limit 写成成功验收。
- `cudaDeviceGetLimit` 的输出指针为空时必须先返回 `cudaErrorInvalidValue`，不能把空指针透传给 ACL。
- `cudaDeviceGetHostAtomicCapabilities` 映射到 `aclrtDeviceGetHostAtomicCapabilities`，`cudaDeviceGetP2PAtomicCapabilities` 映射到 `aclrtDeviceGetP2PAtomicCapabilities`。CUDA operation 0-12 与 CANN SIMT atomic operation 数值一致，可逐项转换；非法 operation 返回 `cudaErrorInvalidValue`。
- CUDA atomic capability bit 与 CANN bit 不完全一致。迁移时必须将 `ACL_RT_ATOMIC_CAPABILITY_SIGNED/UNSIGNED/REDUCTION/SCALAR32/SCALAR64/SCALAR128/VECTOR32X4` 转换为对应 CUDA bit；CANN 独有 `SCALAR8/SCALAR16` 不向上暴露为 CUDA bit。
- `cudaDeviceGetP2PAtomicCapabilities` 的 src/dst 设备相同应按 CUDA 语义返回 `cudaErrorInvalidDevice`。跨设备正向查询需要至少 2 张可见设备；单卡环境用例应 `SKIP` 跨设备成功路径，但仍验证同设备错误路径。
- CUDA Samples `1_Utilities/apiRuntimeCoverage` 可用于 `cudaDeviceSetLimit` / `cudaDeviceGetLimit` 的 stack limit 直转验收；本地 CUDA Samples 不包含 atomic capability 两个接口时，应使用自研 `apiRuntimeCoverage_cuda.cu::CheckAtomicCapabilityApis` 补充验收。

##### 4.1.9 IPC 适配注意事项

CANN IPC 使用 key/opaque handle 数据而非 POSIX fd：

```c
// 跨进程传递 IPC handle/key 数据必须使用共享内存
// 不能使用 UNIX socket 传递文件描述符

// Producer
cudaIpcMemHandle_t handle;
cudaIpcGetMemHandle(&handle, d_ptr);

// 通过 shm_open/mmap 传递 handle/key 数据
int shm_fd = shm_open("/ipc_shm", O_CREAT|O_RDWR, 0666);
ftruncate(shm_fd, sizeof(cudaIpcMemHandle_t));
void* shm_ptr = mmap(NULL, sizeof(cudaIpcMemHandle_t), 
                     PROT_READ|PROT_WRITE, MAP_SHARED, shm_fd, 0);
memcpy(shm_ptr, &handle, sizeof(cudaIpcMemHandle_t));

// Consumer
cudaIpcMemHandle_t handle;
memcpy(&handle, shm_ptr, sizeof(cudaIpcMemHandle_t));
cudaIpcOpenMemHandle(&d_ptr, handle, cudaIpcMemLazyEnablePeerAccess);
```

##### 4.1.10 P2P / cudaMemcpyPeerAsync 适配注意事项

迁移包含 `cudaMemcpyPeerAsync`、`cudaMemcpyPeer`、`cudaDeviceCanAccessPeer`、`cudaDeviceEnablePeerAccess` 的 CUDA 用例或应用时，不能只做头文件替换后沿用 CUDA 原始双卡顺序。CANN 跨 Device P2P 复制对 enable 方向、内存分配策略和 stream 所属 Device 更敏感，转换后的 CANN 兼容层用例必须按以下流程生成：

- 先用 `cudaDeviceCanAccessPeer(&canAccessPeer, srcDevice, dstDevice)` 查询能力；若返回 0，跨 Device copy 成功路径应 `SKIP`，不能继续当作失败。
- 在任何 P2P device 内存分配前，分别切到两张卡开启双向 peer access：`cudaSetDevice(srcDevice); cudaDeviceEnablePeerAccess(dstDevice, 0);`，再 `cudaSetDevice(dstDevice); cudaDeviceEnablePeerAccess(srcDevice, 0);`。只开启单向访问容易在 `cudaStreamSynchronize` 暴露 `cudaErrorSystemDriverMismatch`。
- 设置 `CUDA_COMPAT_DEVICE_MALLOC_POLICY=p2p`，让兼容层 `cudaMalloc` 使用 `ACL_MEM_MALLOC_HUGE_FIRST_P2P`；P2P 源、目的 device buffer 必须在 peer access 开启之后再分配。
- Device 0 到 Device 1 的最小验证流程：切到 Device 0 分配并写入源 buffer；切到 Device 1 分配目的 buffer、创建属于 Device 1 的 stream；调用 `cudaMemcpyPeerAsync(dstOn1, 1, srcOn0, 0, bytes, streamOn1)`；随后同步同一个 Device 1 stream 并把目的 buffer 拷回 Host 校验数据。
- 如果转换产物里同时有同设备 `cudaMemcpyPeerAsync(dst, 0, src, 0, ...)` 和跨设备 `0->1`，同设备路径可作为单卡基础验证；跨设备路径必须按上述 CANN P2P 流程生成，不能复用单卡 stream 或在分配内存后才 enable peer access。
- 清理时分别切回对应 Device 释放各自 buffer 和 stream，并尽量关闭两端 peer access；关闭失败可按环境限制记录为 `SKIP`，不要影响已完成的数据校验结论。

##### 4.1.11 3D Pitched Memory 验证注意事项

迁移 `cudaMemcpy3D*`、`cudaMemset3D*` 或 3D batch/attributes copy 用例时，数据断言必须按 CUDA extent 语义生成：

- `extent.width` 是每行有效字节数，`pitch - extent.width` 是 padding；3D copy/memset 不保证改写 padding，不能把整段 `pitch * height * depth` 缓冲区直接与期望值比较。
- 数据校验应逐 `z`、逐 `y` 比较每行前 `extent.width` 字节；只有在源、目的 padding 都已显式初始化为同一值时，才允许整缓冲区比较。
- `cudaMemset3D` / `cudaMemset3DAsync` 成功后必须回读并检查有效 extent 内的值，不能只检查返回码或回读调用是否成功。
- `cudaMemcpy3DBatchOp` 的 `rowLength`、`layerHeight` 和 location hint 必须与源用例保持一致，避免测试因错误推断 Host/Device 位置而走到不同复制路径。

##### 4.1.12 转换覆盖与环境跳过

- 报告把 CUDA 版本别名、重载或 `_v2` 符号分别计入覆盖数时，转换用例必须存在对应的真实调用路径；只打印多个 `COVER` 标签、却重复调用同一个重载，不能作为多 spelling 覆盖证据。若 CUDA 公共头文件只暴露非版本化名称，应在 CANN 产物中验证该包装函数确实委托到版本化实现，并在报告中说明两者关系。
- `cudaGetDeviceCount` 返回 `cudaSuccess` 但 count 为 0 时，应输出 `SKIP - no visible CANN device (count=0)` 等准确原因；不要用 `cudaGetErrorString(cudaSuccess)` 生成 `SKIP - no error`。该状态只证明程序可启动，不得写成设备用例已运行通过。

#### 4.2 直接迁移方式改写步骤

##### 4.2.1 API 映射对照


| CUDA API                | CANN API                      | 参数映射                             |
| ----------------------- | ----------------------------- | ------------------------------------ |
| `cudaMalloc`            | `aclrtMalloc`                 | size, 添加 ACL_MEM_MALLOC_HUGE_FIRST |
| `cudaFree`              | `aclrtFree`                   | 直接映射                             |
| `cudaMemcpy`            | `aclrtMemcpy`                 | 增加 count 参数（dstSize, srcSize）  |
| `cudaMemcpyAsync`       | `aclrtMemcpyAsync`            | 同上 + stream                        |
| `cudaStreamCreate`      | `aclrtCreateStream`           | 直接映射                             |
| `cudaStreamSetAttribute` / `cudaStreamGetAttribute` | `aclrtSetStreamAttribute` / `aclrtGetStreamAttribute` | 兼容层按 CANN stream attr/value 直通 |
| `cudaEventCreate`       | `aclrtCreateEvent`            | 直接映射                             |
| `cudaLaunchKernel`      | `aclrtLaunchKernelWithArgsArray` / `aclrtLaunchKernelWithHostArgs` / SIMT Launch 系列 | 根据参数组织方式选择 |
| `cudaLaunchKernelEx`    | `aclrtLaunchKernelWithHostArgs` | 查询 CANN function 参数布局后打包 HostArgs |
| `cudaFuncGetName` / `cudaFuncGetParamCount` / `cudaFuncGetParamInfo` | `aclrtGetFunctionName` / `aclrtFunctionGetParamCount` / `aclrtFunctionGetParamInfo` | CANN function handle 查询 |
| `cudaGraphDebugDotPrint` | `aclmdlRIDebugJsonPrint`     | Graph 调试信息导出                   |
| `cudaGraphExecDestroy`  | `aclmdlRIDestroy`             | 销毁 Graph/RI 实例                   |
| `cudaGraphLaunch`       | `aclmdlRIExecuteAsync`        | 异步执行 Graph/RI                    |
| `cudaRuntimeGetVersion` | `aclsysGetVersionNum`         | 查询 runtime 包版本号                |
| `cudaSetDevice`         | `aclrtSetDevice`              | 直接映射                             |
| `cudaDeviceSynchronize` | `aclrtSynchronizeDevice`      | 直接映射                             |

##### 4.2.2 类型映射


| CUDA 类型        | CANN 类型         |
| ---------------- | ----------------- |
| `cudaStream_t`   | `aclrtStream`     |
| `cudaEvent_t`    | `aclrtEvent`      |
| `cudaError_t`    | `aclError`        |
| `cudaMemcpyKind` | `aclrtMemcpyKind` |

##### 4.2.3 错误码转换

参考 `references/error_mapping.md` 进行错误码映射。

##### 4.2.4 初始化/清理

```c
// CANN 需显式初始化
aclInit(NULL);  // 或指定配置文件路径

// 业务代码...

// 清理
aclFinalize();
```

#### 4.3 编译配置改写

##### 4.3.1 CMake 改写示例

```cmake
# 原 CUDA 项目
find_package(CUDA REQUIRED)
include_directories(${CUDA_INCLUDE_DIRS})
target_link_libraries(your_target ${CUDA_LIBRARIES})

# 迁移后（兼容层方式）
# 设置兼容层源码路径（指向 runtime_migration/assets/src）
set(RUNTIME_MIGRATION_DIR /path/to/runtime_migration/assets/src)
include_directories(${RUNTIME_MIGRATION_DIR})

# 编译兼容层库（在 assets/src 目录）
# cd assets/src && mkdir -p build && cd build && cmake .. && make
# 编译产物：libcudacompat.so, libcudacompat.a

find_library(CUDACOMPAT libcudacompat.so 
    PATHS ${RUNTIME_MIGRATION_DIR}/build)
target_link_libraries(your_target ${CUDACOMPAT} acl_rt c_sec)
```

##### 4.3.2 Makefile 改写示例

```makefile
# 原 CUDA 项目
CFLAGS += -I/usr/local/cuda/include
LDFLAGS += -L/usr/local/cuda/lib64 -lcudart

# 迁移后（兼容层方式）
# 设置兼容层源码路径（指向 runtime_migration/assets/src）
RUNTIME_MIGRATION_DIR = /path/to/runtime_migration/assets/src
CFLAGS += -I$(RUNTIME_MIGRATION_DIR)
LDFLAGS += -L$(RUNTIME_MIGRATION_DIR)/build -lcudacompat
LDFLAGS += -L~/Ascend/cann/lib64 -lacl_rt -lc_sec
```

说明：兼容层头文件在 CANN 环境提供 `securec.h` 时会使用 `memcpy_s` 等安全函数，独立迁移样例或应用链接时需同时链接 `libc_sec`。

##### 4.3.3 独立编译兼容层库

兼容层支持在 `assets/src` 目录独立编译：

```bash
# 在 assets/src 目录独立编译
cd assets/src
mkdir -p build && cd build
cmake .. && make

# 编译产物
# libcudacompat.so - 共享库
# libcudacompat.a  - 静态库

# Debug 模式编译
cmake .. -DCUDA_COMPAT_DEBUG=ON && make
```

---

### Step 5: 编译测试验证

#### 5.1 编译步骤

```bash
# 编译兼容层库
cd assets/src
mkdir -p build && cd build
cmake .. && make

# 编译产物位置
# assets/src/build/libcudacompat.so
# assets/src/build/libcudacompat.a

# 编译迁移后的应用
cd your_app_dir
gcc -I/path/to/runtime_migration/assets/src \
    your_app.c \
    -L/path/to/runtime_migration/assets/src/build -lcudacompat \
    -L~/Ascend/cann/lib64 -lacl_rt -lc_sec \
    -o your_app
```

#### 5.2 运行测试

```bash
# 设置环境变量（可选）
export CUDA_COMPAT_INIT_FILE_PATH=/path/to/acl.ini

# 运行应用
./your_app
```

#### 5.3 Debug 模式排查

如果遇到问题，启用 Debug 模式：

```bash
# 编译兼容层 Debug 版本
cd assets/src/build
cmake .. -DCUDA_COMPAT_DEBUG=ON && make

# 运行应用查看详细错误信息
./your_app
# 输出：[CUDA_COMPAT_DEBUG] cann_compat.c:34: aclInit failed with ACL error: 107000
```

#### 5.4 常见问题处理


| 问题                           | 原因               | 解决方案                        |
| ------------------------------ | ------------------ | ------------------------------- |
| 初始化失败                     | aclInit 配置错误   | 检查 CUDA_COMPAT_INIT_FILE_PATH |
| 内存分配失败                   | 设备内存不足       | 减小分配大小或检查设备状态      |
| API 返回 cudaErrorNotSupported | 使用了不支持 API   | 查阅支持表，使用替代方案        |
| IPC 传递失败                   | 使用 UNIX socket   | 改用共享内存传递 opaque handle  |
| CUDA Kernel 启动语法无法编译   | `kernel<<<...>>>` 不能由普通 C++ 兼容头保留 | 改为 `cudaCompatLaunchHostKernel()` Host fallback，并明确记录这不是 NPU kernel 执行 |

---

## 参考资源

本技能依赖以下参考文件，按需加载：

- `references/cuda_api_common.md` - 常用 CUDA API 参考
- `references/cann_api_common.md` - 常用 CANN API 参考
- `references/error_mapping.md` - 错误码映射表
- `references/api_support_table.md` - API 支持状态表
- `references/p2p_migration_patterns.md` - P2P / peer copy 迁移验证模板

### 项目代码参考

`assets/src` 目录提供了 CUDA API 到 CANN Runtime API 的完整实现，可作为迁移代码参考：

#### 头文件（API 声明）


| 文件路径                            | 功能说明               | 参考用途                                       |
| ----------------------------------- | ---------------------- | ---------------------------------------------- |
| `assets/src/cann_runtime_compat.h`  | 主头文件，整合所有 API | 查看支持的完整 API 列表                        |
| `assets/src/cann_compat_types.h`    | CUDA 类型定义          | 了解类型映射（cudaStream_t → aclrtStream 等） |
| `assets/src/cann_compat_cu_types.h` | CUDA Driver 类型定义   | Driver API 类型映射                            |
| `assets/src/cann_compat_device.h`   | 设备管理 API           | cudaGetDeviceCount 等实现参考                  |
| `assets/src/cann_compat_memory.h`   | 内存管理 API           | cudaMalloc, cudaMemcpy 等实现参考              |
| `assets/src/cann_compat_stream.h`   | 流管理 API             | cudaStreamCreate 等实现参考                    |
| `assets/src/cann_compat_event.h`    | 事件管理 API           | cudaEventCreate 等实现参考                     |
| `assets/src/cann_compat_ipc.h`      | IPC API                | cudaIpcGetMemHandle 等实现参考                 |
| `assets/src/cann_compat_library.h`  | 库管理 API             | cudaLibraryLoad 等实现参考                     |
| `assets/src/cann_compat_exec.h`     | 执行配置 API           | 执行配置相关宏定义                             |
| `assets/src/cann_compat_mempool.h`  | 内存池 API             | CUDA SOMA API 编译兼容面，当前返回 cudaErrorNotSupported |
| `assets/src/cann_compat_cu_vmm.h`   | VMM API                | cuMemCreate 等 Driver VMM 实现                 |

#### 源文件（API 实现）


| 文件路径                           | 功能说明   | 参考用途                            |
| ---------------------------------- | ---------- | ----------------------------------- |
| `assets/src/cann_compat.c`         | 主实现文件 | 查看所有 Runtime API 的完整实现逻辑 |
| `assets/src/cann_compat_ipc.c`     | IPC 实现   | 了解 IPC 跨进程通信的实现细节       |
| `assets/src/cann_compat_library.c` | 库管理实现 | 了解库加载和 Kernel 执行的实现      |

#### 编译配置


| 文件路径                    | 功能说明                                      |
| --------------------------- | --------------------------------------------- |
| `assets/src/CMakeLists.txt` | 独立的 CMake 配置，支持独立编译 cudacompat 库 |

#### 使用方式

迁移时，可按以下方式参考项目代码：

1. **查看 API 映射实现**：阅读 `assets/src/cann_compat.c` 中对应函数，了解 CUDA API 如何转换为 CANN API 调用
2. **理解参数转换**：查看函数内部如何处理参数差异（如 cudaMemcpyKind → aclrtMemcpyKind）
3. **错误处理模式**：学习如何将 CANN 错误码映射为 CUDA 错误码
4. **特殊场景处理**：如 IPC 的 opaque handle 处理、Stream 配置等

示例 - 查看 cudaMalloc 实现：

```bash
# 在 cann_compat.c 中搜索 cudaMalloc 实现
grep -A 20 "cudaError_t cudaMalloc" assets/src/cann_compat.c
```

独立编译（可选）：

```bash
# 在 assets/src 目录独立编译 cudacompat 库
cd assets/src
mkdir -p build && cd build
cmake .. && make
# 生成 libcudacompat.so 和 libcudacompat.a
```

本地头文件路径：

- CUDA 类型定义: `assets/src/cann_compat_types.h`
- CANN 头文件: `~/Ascend/cann/include/acl/acl_rt.h`

---

## 示例

### 示例 1: 简单内存拷贝程序迁移

**原 CUDA 代码**：

```c
#include <cuda_runtime.h>

int main() {
    float *d_data;
    cudaMalloc(&d_data, 1024 * sizeof(float));
  
    float h_data[1024];
    cudaMemcpy(d_data, h_data, 1024 * sizeof(float), cudaMemcpyHostToDevice);
  
    cudaFree(d_data);
    return 0;
}
```

**迁移后（兼容层方式）**：

```c
#include "cann_runtime_compat.h"

int main() {
    CUDA_COMPAT_FORCE_LINK();
  
    float *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, 1024 * sizeof(float)));
  
    float h_data[1024];
    CUDA_CHECK(cudaMemcpy(d_data, h_data, 1024 * sizeof(float), cudaMemcpyHostToDevice));
  
    CUDA_CHECK(cudaFree(d_data));
    return 0;
}
```

**迁移后（直接迁移方式）**：

```c
#include <acl/acl.h>

int main() {
    aclInit(NULL);
  
    float *d_data;
    aclrtMalloc(&d_data, 1024 * sizeof(float), ACL_MEM_MALLOC_HUGE_FIRST);
  
    float h_data[1024];
    aclrtMemcpy(d_data, 1024 * sizeof(float), h_data, 1024 * sizeof(float), ACL_MEMCPY_HOST_TO_DEVICE);
  
    aclrtFree(d_data);
    aclFinalize();
    return 0;
}
```

### 示例 2: 多流并发程序迁移

**原 CUDA 代码**：

```c
cudaStream_t stream1, stream2;
cudaStreamCreate(&stream1);
cudaStreamCreate(&stream2);

cudaMemcpyAsync(d1, h1, size, cudaMemcpyHostToDevice, stream1);
cudaMemcpyAsync(d2, h2, size, cudaMemcpyHostToDevice, stream2);

cudaStreamSynchronize(stream1);
cudaStreamSynchronize(stream2);

cudaStreamDestroy(stream1);
cudaStreamDestroy(stream2);
```

**迁移后（兼容层方式）**：

```c
// API 调用完全相同，仅替换头文件
#include "cann_runtime_compat.h"
// ... 同原代码 ...
```

---

## 输出格式

完成迁移后，输出以下内容：

1. **迁移可行性分析报告**
2. **迁移方式推荐**
3. **改写后的代码**
4. **编译命令**
5. **测试验证步骤**

如果源代码包含 CUDA Kernel 启动语法，输出还必须包含 Host fallback 清单，并逐项声明其在 Host/CPU 上执行、不是 NPU kernel 执行。NPU 算子迁移需求仅作为范围外后续事项记录，不在本技能内实现或调用其他 skill。
