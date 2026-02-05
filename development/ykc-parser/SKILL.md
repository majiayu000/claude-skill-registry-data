---
name: ykc-parser
description: 解析云快充充电桩通信协议报文,支持CRC16校验、多种帧类型解析、错误诊断,返回标准JSON格式。用于处理云快充协议V1.6的报文数据。
---

# 云快充报文解析器

解析云快充充电桩通信协议报文,将十六进制报文转换为结构化的JSON数据。

## 技能用途

本技能用于解析云快充充电平台协议V1.6的报文数据,提供:
- 完整的报文结构解析(起始标志、数据长度、序列号、加密标志、帧类型、消息体、CRC校验)
- CRC16校验(Modbus算法),即使校验失败也继续解析
- 多种帧类型的消息体解析(登录认证、实时数据、心跳包等)
- 数据类型转换(BCD码、BIN码、ASCII码)
- 错误诊断和容错处理
- 标准JSON格式输出

## 何时使用此技能

当用户需要:
- 解析云快充协议的十六进制报文
- 诊断云快充通信问题
- 验证报文的CRC校验码
- 查看报文的详细字段内容
- 开发或调试云快充充电桩通信程序

## 使用方法

### 基本解析流程

1. **接收报文**: 用户提供十六进制格式的云快充报文(可带空格)
2. **调用解析脚本**: 使用 `scripts/parse_ykc.py` 脚本解析报文
3. **返回结果**: 输出标准JSON格式的解析结果

### 执行解析

使用Python脚本解析报文:

```bash
python "$SKILL_DIR"/scripts/parse_ykc.py "<hex_string>"
```

示例:
```bash
python "$SKILL_DIR"/scripts/parse_ykc.py "68 22 0000 00 01 55031412782305 00 02 0F 56342E312E353000 01 01010101010101010101 04 675A"
```

### 解析脚本说明

- **scripts/parse_ykc.py**: 主解析脚本
  - 解析报文基本结构
  - 调用CRC16验证
  - 根据帧类型解析消息体
  - 返回标准JSON格式
  - 处理各种错误情况

- **scripts/crc16.py**: CRC16校验模块
  - 实现Modbus CRC16算法
  - 使用查表法计算CRC
  - 支持CRC验证和计算

### 返回格式

#### 成功解析
```json
{
  "code": 200,
  "msg": "解析成功",
  "start_flag": "0x68",
  "data_length": 34,
  "sequence_number": 0,
  "encrypt_flag": "0x00",
  "is_encrypted": false,
  "frame_type": "0x01",
  "frame_type_name": "充电桩登录认证",
  "body_length": 28,
  "body_hex": "...",
  "crc16_received": "0x675A",
  "crc16_calculated": "0x675A",
  "crc16_valid": true,
  "body_data": {
    "pile_code": "55031412782305",
    "pile_type": "直流桩",
    "gun_count": 2,
    "protocol_version": "v1.5",
    "program_version": "v4.1.50",
    "network_type": "LAN",
    "sim_card": "01010101010101010101",
    "operator": "其他"
  }
}
```

#### 解析失败
```json
{
  "code": 500,
  "msg": "解析失败: 错误描述",
  "errors": [
    "具体错误信息1",
    "具体错误信息2"
  ],
  "warnings": [
    "CRC16校验失败: 期望0x675A, 计算0x675B"
  ],
  "partial_data": {
    "frame_type": "0x01",
    "frame_type_name": "登录认证"
  }
}
```

### 支持的帧类型

当前实现详细解析的帧类型:
- **0x01**: 充电桩登录认证
- **0x02**: 登录认证应答
- **0x12**: 读取实时监测数据
- **0x13**: 上传实时监测数据

其他帧类型会返回帧类型名称和原始十六进制数据,但不进行详细字段解析。

### 参考文档

#### 快速参考文档
如需了解协议概要,查阅以下快速参考:
- **references/protocol_structure.md**: 报文结构和解析流程
- **references/data_formats.md**: 数据类型定义和转换规则
- **references/frame_types.md**: 所有帧类型定义表

#### 完整协议文档
技能包含云快充协议V1.6的完整文档,位于 `references/docs/` 目录:

**协议基础**:
- `references/docs/02-协议基础/01-通信协议结构.md`
- `references/docs/02-协议基础/02-应用层报文帧格式.md`
- `references/docs/02-协议基础/03-数据格式定义.md`
- `references/docs/02-协议基础/05-帧类型定义表.md`

**业务流程**:
- `references/docs/04-注册心跳/01-登录认证.md`: 登录认证流程和报文格式
- `references/docs/04-注册心跳/02-心跳包.md`: 心跳包协议
- `references/docs/05-实时数据/01-实时监测数据.md`: 实时数据上报
- `references/docs/06-运营交互/01-充电启动.md`: 充电启动流程
- `references/docs/06-运营交互/02-充电停止.md`: 充电停止流程
- `references/docs/07-平台设置/`: 平台配置相关
- `references/docs/09-远程维护/`: 远程维护命令
- `references/docs/10-并充模式/`: 双枪并充模式

**附录**:
- `references/docs/11-附录/01-充电停止原因代码表.md`
- `references/docs/11-附录/02-CRC16校验计算方法.md`
- `references/docs/11-附录/03-协议需知.md`

**文档索引**:
- `references/docs/INDEX.md`: 完整的文档目录索引
- `references/docs/README.md`: 协议文档总览

#### 使用Grep搜索
搜索特定内容示例:
- 搜索特定帧类型: `grep -i "0x13" "$SKILL_DIR"/references/frame_types.md`
- 搜索数据格式: `grep -i "BCD" "$SKILL_DIR"/references/data_formats.md`
- 搜索完整文档: `grep -r "登录认证" "$SKILL_DIR"/references/docs/`
- 搜索流程说明: `grep -r "充电启动" "$SKILL_DIR"/references/docs/`

## 常见问题处理

### 1. CRC校验失败
- 报文会标注 `"crc16_valid": false`
- 在warnings中说明期望值和计算值
- **继续解析报文内容**(不中断)

### 2. 报文长度不匹配
- 在errors中说明期望长度和实际长度
- 尽可能解析已有字段
- 返回部分解析结果

### 3. 数据类型错误
- ASCII字段包含非ASCII字符时发出警告
- BCD码无效时返回"无效BCD"
- 在warnings中标注错误位置

### 4. 未知帧类型
- 返回帧类型十六进制值
- 标注为"未知帧类型"
- 返回消息体原始十六进制数据

## 扩展解析

如需添加新帧类型的详细解析:
1. 在 `parse_ykc.py` 的 `_parse_body` 方法中添加新的条件分支
2. 实现对应的 `_parse_<frame_name>` 方法
3. 参考 `_parse_login` 和 `_parse_realtime_data` 的实现方式
4. 使用 `_bcd_to_str`、`_ascii_to_str` 等辅助方法处理数据类型

## 示例用法

### 示例1: 解析登录认证报文
```
用户: 帮我解析这个云快充报文:
68 22 0000 00 01 55031412782305 00 02 0F 56342E312E353000 01 01010101010101010101 04 675A

Claude: 执行解析脚本并返回结果,说明这是一个登录认证报文,桩编码为55031412782305,直流桩,2个充电枪,协议版本v1.5等
```

### 示例2: 解析实时数据报文
```
用户: 这个报文有什么问题?
68 40 1A03 00 13 ... 9DAC

Claude: 执行解析脚本,发现CRC校验失败,但继续解析,返回完整的实时数据(电压、电流、SOC、充电度数等),并标注CRC错误
```

### 示例3: 处理格式错误
```
用户: 解析报文 68 22 00

Claude: 执行解析脚本,返回错误信息"报文长度过短: 3字节,最少需要8字节"
```

## 技术细节

### CRC16计算
- 使用Modbus CRC16算法(多项式0x180D)
- 校验范围: 序列号域到消息体结束
- 字节序: 小端序(低字节在前,高字节在后)
- 初始值: 0xFFFF
- 使用查表法提高计算效率

### 数据类型转换
- **BCD码**: 每字节表示两位十进制数,直接转十六进制字符串
- **BIN小端**: 使用 `int.from_bytes(byteorder='little')` 转换
- **ASCII码**: 使用 `decode('ascii')` 转换,移除尾部0x00

### 精度处理
- 电压/电流: 精确到0.1,除以10
- 电量/金额: 精确到0.0001,除以10000
- 温度: 整数偏移-50℃

## 注意事项

- 报文十六进制字符串可以包含空格,会自动清理
- CRC校验失败时会继续解析,不会中断流程
- 未实现详细解析的帧类型会返回原始十六进制数据
- 对于错误报文,返回尽可能多的部分解析结果
- 所有错误和警告都会在结果中列出
