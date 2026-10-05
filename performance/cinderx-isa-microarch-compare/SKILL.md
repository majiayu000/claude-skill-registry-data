---
name: cinderx-isa-microarch-compare
description: Use when 对 CinderX 的 Arm/x86 性能差异做 ISA、微架构与 perf 归因。
---

# CinderX ISA/Microarch Compare

平台差异分析先建立矩阵，再进入 HIR/LIR 细节。

## 矩阵

- 平台：Kunpeng、x86、内核、容器、CPU governor。
- ISA：指令选择、SIMD、原子、barrier、寄存器和调用约定。
- 微架构：cache、分支预测、流水线、内存带宽、TLB、hugepages。
- 观测：perf top/stat、机器码、speedup、benchmark 覆盖。
- lowering：CinderX codegen 是否生成不同形态。

## 反问 Gate

- 平台对、benchmark 目标或性能口径查证后仍无法确定时询问；CPU 型号和可用 perf 能力先探测。
- 新增权限或改变共享环境的 CPU governor/hugepages 等配置，需在用户授权范围内。
- 系统扫描超出预算时询问扩大范围；现有数据分析和低成本子集继续。

## 输出

平台差异点、受影响 benchmark、候选优化点、最小验证命令和需要排除的环境漂移。

不要一开始就陷入某个 HIR pass；先证明平台差异存在。
