---
name: julia-hydrotools
description: 计算短波辐射、长波辐射、潜在蒸散发、日出日落时间、湿度的基本变量处理。
---

# 1 运行环境说明

- 在Julia中运行

- 在julia中首先加载包，`using HydroTools`

- 若没有包加载出错，则安装之，`using Pkg; Pkg.add("HydroTools")`


## 1.1 函数说明

- `cal_Rsi_toa(lat, J)`: daily extraterrestrial radiation in MJ m-2 day-1
  + `lat`: latitude in deg
  + `J`: doy of year
  > 注意lat和J是scalar
  > 如果是vector，按照Julia的语法，采用`cal_Rsi_toa.(lat, J)`调用
  + 默认返回单位是`MJ d-1`，若想转为`W m-2`，需要调用[MJ2W]函数，告诉用户返回的数字单位


## 1.2 文件保存

文件保存采用Julia包`DataFrames`，`RTableTools`

```julia
using RTableTools
fwrite(df, "out.csv") # df is a DataFrame
```
