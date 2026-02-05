---
name: hydro-forecast
description: 
---

# 1 运行环境说明

- 在Julia中运行

- 在julia中首先加载包，`using HydroTools`

- 若没有包加载出错，则安装之，`using Pkg; Pkg.add("HydroTools")`


## 说明

先不要立即执行该skills，提醒用户输入的数据的格式。用户需要整理好的数据路径即可。

```

```

`model`模型选择

+ MarrMot
+ XAJ
+ TCN
+ LSTM
+ KAN

如果复杂、参数比较多的模型：要求用户输入模型参数`json`文件。
按照如下示例

```json
{
    "clumping_index": 0.62,
    "LAI_max_o": 4.5,
    "LAI_max_u": 2.4,
    "z00": 1.33,
    "mass_overstory": 35,
    "mass_understory": 10,
    "root_depth": 0.6,
    "α_canopy_vis": 0.035,
    "α_canopy_nir": 0.23,
    "r_root_decay": 0.95,
    "minimum_stomatal_resistance": 150,
    "z_canopy_o": 20,
    "z_canopy_u": 3,
    "g1_w": 8,
    "VCmax25": 62.5,
    "leaf_resp_co": 0.0015,
    "stem_resp_co": 0.0020,
    "root_resp_co": 0.0020,
    "fine_root_resp_co": 0.003,
    "N_leaf": 4.45,
    "slope_Vc": 0.33152
}
```

## 1.1 任务说明

### 1.1.1 `framework`：

```julia

function hydro_forecast(f; model, outdir)
  res = ...

  fwrite(res.output, ...)
  fwrite(res.gof, ...)
  fwrite(res.info_flood, ...)
  fwrite(res.dat_flood, ...)
  fwrite(res.evaluation, ...)
end

function hydro_forecast(X::AbstractArray, Y::AbstractArray; model::Function, outdir = "OUTPUT")
  mkpath(outdir)
  res; # return a NamedTuple
end
```

**输入**：X, Y, model

**输出**：Qsim, GOF, Pass_rate

  + `output`: 三类数据集的输出，A DataFrame with columns of `date`, `Qsim`, 
  + `gof`: 三类数据的拟合优度
  + `info_flood`: 洪水场次信息，`id`, `time_beg`, `time_end`, `duration`, `Q_peak`, `Q_min`
  + `dat_flood`：洪水场次的驱动数据，
  + `evaluation`: 每个洪水场次上的模拟优度, csv

**绘图**：

  + 交给他绘图的函数，数据

**总结**：

  + `evaluation`总结模型预报精度 （`AI执行`）


**内部模块设计**：

  + `flood_division`: 采用R语言，划分洪水场次

  + `划分数据集`：train, test, valid

  + `loss`: 根据拟合优度指标去设计loss，例如KGE, NSE, RMSE，注意loss越小越优。根据loss去优选模型参数。
 
  + `evaluation`: 在三种数据集，train, test, valid。每个洪水场次的洪峰、峰现时间合格率。


### 1.1.2 `model`：水文模型、LSTM、TCN、KAN

  ```julia
  Ysim = Model(X, Y; params, state) # Lux的设计哲学
  ```

### 1.1.3 文件保存

文件保存采用Julia包`DataFrames`，`RTableTools`

```julia
using RTableTools
fwrite(df, "out.csv") # df is a DataFrame
```
