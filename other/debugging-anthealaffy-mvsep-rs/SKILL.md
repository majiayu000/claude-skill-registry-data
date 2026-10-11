---
name: debugging
description: >
  调试工具阶梯：print/logging、gdb/lldb/pdb、rr 反向调试、strace/dtruss 与 bpftrace、tcpdump/mitmproxy、
  ASan/TSan/MSan/UBSan 与 Valgrind、AI 辅助调试。Use when the user asks to debug a crash, segfault,
  memory error, flaky test, or race condition. 触发于「帮我调试/排查崩溃/段错误/内存错误/偶发失败」。
---

# 调试

主线：代码做的不是你以为的事，而是你叫它做的事——调试就是弥合这个差距。工具按信号成本排阶梯：能 print 就不用 gdb，能 strace 就不上 bpftrace。本 skill 只做 MIT 讲义的科学面（原理与具体工具）；与工程策略（艺术面）混合的版本见 dsh 的 `debugging-and-profiling` 与 `diagnosing-bugs`。

## Printf 与 Logging

- print 迭代法：在怀疑处加 print，反复跑直到信息足够定位。有效，但每次都改代码重跑。
- logging = 「更讲究的 print」：框架自带日志路由（定向到别处）、级别过滤（INFO/DEBUG/WARN/ERROR）、结构化日志（数据事后好提取）。写代码时就主动埋日志——需要的数据可能已经在。
- 修完 bug 后，把诊断用的 print 转成正式 log 再删——下次同类问题不用再改代码。
- 现成程序的日志：很多程序支持 `-v`/`--verbose`（重复加更详细）；服务日志看 `/var/log/` 或 `journalctl -u <service>`；第三方库查它是否支持 debug 日志（环境变量/配置）。

## 调试器（gdb）

- 什么时候上调试器：不知道该看什么信息、bug 只在难复现条件下出现、改代码重启太贵（长启动时间、复杂状态）。
- 调试器能：某一行停下、逐指令单步、崩溃后看变量、条件成立才停。
- 通用调试器 gdb/lldb 可调试任意原生二进制；语言专属（Python pdb、Java jdb）与运行时集成更紧。
- gdb 常用：`run`；`b {函数}` 或 `b {文件}:{行}` 断点；`c` 继续；`step`/`next`/`finish` 进/过/出；`p {变量}` 打印值；`bt` 调用栈；`watch {表达式}` 值变化即停。
- 要有意义的栈：用 `-g` 编译（DWARF 调试信息）；性能工具再加 `-fno-omit-frame-pointer` 让栈更可靠。TUI 模式 `gdb -tui`（或内部 Ctrl-x a）分屏看源码。

## Record-Replay（rr）

- Heisenbug（一观察就消失：竞态、时序、环境依赖）用传统调试器无效——print 拖慢代码后竞态可能不再发生。
- rr 记录执行、确定性重放，还能倒着走：`reverse-continue`（rc）反向继续、`reverse-step`（rs）反向单步、`reverse-next`（rn）反向跳过函数、`reverse-finish` 反向出当前函数。
- 崩溃排查套路：跑到崩溃 → 看被破坏的变量 → `watch` 它 → `reverse-continue` 精确找到被写坏的那一行。
- 适用：偶发失败测试、竞态与多线程、难复现崩溃、一切「想回到过去」的 bug。
- 注意：rr 仅 Linux、需要硬件性能计数器（多数 AWS EC2 虚拟机不行、不支持 GPU）；rr 序列化线程调度，依赖时序的竞态可能不复现，要多录几次。macOS 看 Warpspeed。

## 系统调用追踪

- strace 观察程序与内核的每次交互（打开文件、分配内存、建进程……）：程序卡在哪、想访问什么文件、时间花在等什么。
- 常用：`strace ./prog`；`-e trace=file` 只看文件调用；`-f` 跟子进程；`-p <PID>` 追运行中的进程；`-T` 显示耗时。macOS/BSD 用 dtruss（包装 dtrace）。
- bpftrace/eBPF：在内核里跑沙箱程序，awk 式语法但表达力极强——按系统调用名聚合计数/延迟、看调用参数。strace 胜在零门槛；bpftrace 胜在低开销、可看内核函数、可聚合。要 root、默认监控整个内核：按 `comm == "bash"` 过滤，或 `-c 'ls -la'` 从启动开始追一个命令（cpid 即其 PID）。

## 网络调试

- tcpdump：`sudo tcpdump -i any port 80` 抓包；`-w capture.pcap` 存文件给 Wireshark 分析。
- HTTPS 有加密：mitmproxy 做中间人代理看加密流量；Web 应用最省事的是浏览器 DevTools 的 Network tab（解密后的请求/响应、头、耗时都在）。

## 内存调试

- 内存 bug（越界、use-after-free、泄漏）常不立刻崩，而是很久以后才发作。
- Sanitizers 是编译期插桩：AddressSanitizer 查越界/UAF/泄漏（`-fsanitize=address`）；ThreadSanitizer 查数据竞争（`-fsanitize=thread`）；MemorySanitizer 查未初始化内存读（`-fsanitize=memory`）；UBSan 查未定义行为如整数溢出（`-fsanitize=undefined`）。要重编译，但快到能进 CI 与日常开发。
- 不能重编译（无源码、第三方库）用 Valgrind：类虚拟机运行、更慢——`valgrind --leak-check=full ./prog`。

## AI 辅助调试

- 擅长：解释天书级报错（C++ 模板、Rust borrow checker）；跨语言/抽象边界（FFI、构建系统、「我怀疑是依赖的 bug」）；把模糊症状关联到根因（「功能正常但内存多用了 10 倍」）；分析崩溃转储与栈。
- 局限：会一本正经胡说；可能给出掩蔽 bug 而非修复 bug 的建议；永远用真调试工具验证它的话——AI 是理解的补充，不是替代。

## 练习

学习材料在 `exercises.md`。

> 改编自 MIT The Missing Semester 课程 Lecture 4: Debugging and Profiling（讲义 + 口播稿，CC BY-NC-SA 4.0）：https://creativecommons.org/licenses/by-nc-sa/4.0/ · 课程站点：https://missing.csail.mit.edu/ · 讲座视频：https://www.youtube.com/watch?v=8VYT9TcUmKs
