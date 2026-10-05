---
name: ncpgr-data-manage
description: |
  集群数据管理 Skill —— 涵盖数据使用规范、压缩优化、数据共享（ACL）、文件扫描与清理、文件完整性校验、genozip 基因组压缩等全流程。Use when the user asks about: managing data on the HPC cluster, compressing genomic files (fq/bam/vcf), sharing data between users/groups, scanning for large files or cleaning up disk space, checking file integrity (md5/gzip/bam), using genozip, checking disk quota, or any data lifecycle management task on the NCPGR HPC cluster.
metadata:
  version: "1.0.0"
---

# NCPGR 集群数据管理 Skill

## 适用场景

当用户需要执行以下任何操作时使用本 Skill：
- 了解集群数据使用规范和最佳实践
- 压缩基因组数据（fq/bam/vcf 等）以节省存储空间
- 与其他用户或用户组共享数据（ACL 权限管理）
- 扫描大文件、清理不需要的数据、释放存储空间
- 校验文件完整性（md5、gzip、bam、双端测序）
- 使用 genozip 进行高效基因组数据压缩
- 查看存储配额使用情况

## 一、数据使用规范

以下是集群数据管理的核心原则，在回答用户问题时应始终遵循：

### 压缩优先原则
- **fq.gz 不要解压**：常用比对软件（bwa、bowtie2 等）及 seqkit 等工具均支持直接使用 fq.gz 压缩文件
- **sra 转 fq.gz 后删除 sra**：下载完 sra 文件后直接转成 fq.gz，然后删掉 sra 文件
- **比对输出 bam 而非 sam**：利用管道组合 samtools 直接输出 bam，相比 sam 可节省约 60% 存储空间
- **bam 可进一步转 cram**：gatk、sentieon 等支持 cram，可再节省 30%-50% 空间
- **大文本文件压缩成 gz**：linux 命令和各编程语言均支持直接处理 gz 文件
- **使用 pigz 多线程加速**：pigz 支持多线程，可替代 gzip 加速压缩解压

### 长期存储策略
- **文章发表后删除原始 fq**：原始数据已上传 NCBI 等数据库，后续需要时可重新下载
- **群体数据用 genozip 压缩**：fq/bam/vcf 均可压缩，相比 gzip 可节省至少 50% 以上空间
- **大量 vcf 用 bgzip + tabix**：bgzip 压缩后可用 tabix 建索引，方便操作大 vcf 文件
- **公共数据库用集群已有版本**：nr、nt、interproscan 等大型数据库不要自己下载

### 安全与清理
- **集群存储不支持数据恢复**：重要数据及时本地备份
- **大量小文件及时删除**：如 maker、Trinity 的中间文件、软件源码等，会影响集群性能
- **定期查看存储配额**：使用 `diskquota` 命令查看使用情况，超过配额无法写入数据
- **大量文件拷贝用 rsync**：方便校验完整性，避免重复拷贝
- **数据传输后做 md5 校验**：确保传输完整性
- **禁止 chmod 777 共享数据**：使用 ACL 精确控制权限（详见第三节）

## 二、存储配额管理

### 查看配额
```bash
# 查看当前账号的存储配额使用情况
diskquota
```

### 查看目录占用
```bash
# 查看当前目录各子目录的大小
du -sh */

# 查看指定目录的总大小
du -sh /path/to/directory

# 按大小排序列出子目录
du -sm */ | sort -rn | head -20
```

## 三、数据共享（ACL 权限管理）

### 核心原则
- 每个账号 home 目录默认权限为 700（仅本人可读写）
- **严禁将 home 目录设置为 777**（任何用户都可删除文件，极度不安全）
- **禁止将共享数据拷贝到自己目录下**（浪费存储空间）
- 使用 Linux ACL 权限精确控制共享访问

### 组内数据共享（同课题组）
```bash
# 开放本账号 home 目录的读权限给本组用户
chmod 750 ~
```
开放后本组其他用户可以访问、拷贝本账号内的数据。除非特殊情况，不建议开放写权限。

### 组间数据共享（跨课题组 —— 使用 ACL）

#### 向用户组开放目录权限
```bash
# 添加权限：将 user1 的 home 目录对 GROUP2 组开放读权限
setfacl -m g:GROUP2:rx /public/home/user1

# 查看权限
getfacl /public/home/user1

# 课题合作结束后删除权限
setfacl -x g:GROUP2 /public/home/user1
```

#### 向单个用户开放目录权限
```bash
# 添加权限：将 user1 的 home 目录对 user2 开放读权限
setfacl -m u:user2:rx /public/home/user1

# 查看权限
getfacl /public/home/user1

# 课题合作结束后删除权限
setfacl -x u:user2 /public/home/user1
```

### ACL 注意事项
- **路径上所有目录都需要开放权限**：如共享 `/public/home/user1/data`，需先对 `/public/home/user1` 开放权限，再对 data 目录开放
- 正确做法：先 `setfacl -m u:user2:rx /public/home/user1`，然后测试 user2 能否访问目标目录
- 不再需要共享时，及时删除共享权限

## 四、文件扫描与清理

### 扫描大文本文件并压缩
扫描当前账号下大于 100M 的文本文件（fq、fa、sam、vcf、bed 等）：

```bash
# 扫描大文本文件
bsub -n 5 -J scan -o filescan.out -e filescan.err \
  "ls -d ~/* |xargs -I[] -P 5 find [] -size +100M -type f -exec sh ASCII.sh {} \; >filetxt_$(whoami)_$(date +%y%m%d)"
```

其中 `ASCII.sh` 脚本内容：
```bash
#!/bin/sh
na=$1
ty=`file -b $1|xargs echo -n|cut -d" " -f 1`
si=`du -sm $1`
if [ $ty == ASCII ];then
  echo $si
fi
```

从扫描结果中剔除需要保留的文件后，批量 gzip 压缩：
```bash
bsub -n 5 -J gzip -o filegzip.out -e filesgzip.err \
  "cat filetxt_$(whoami)_$(date +%y%m%d)|awk '{print \$2}'|xargs -P 5 -i sh gzip.sh {} > filegzip_$(whoami)_$(date +%y%m%d) 2>&1"
```

其中 `gzip.sh` 脚本内容：
```bash
#!/bin/sh
file=$1
if [ -f $file ];then
  echo $file
  gzip $file
fi
```

**清理建议**：
- sam 文件建议排序并转成 bam 或 cram 存放，已有对应 bam 则直接删除 sam
- fq 的 rawdata 和 cleandata 只保留其中一份

### 扫描所有大文件
```bash
# 扫描所有大于 100M 的文件
bsub -n 5 -J scan -o filescan.out -e filescan.err \
  "ls -d ~/* |xargs -I[] -P 5 find [] -size +100M -type f |xargs du -sm >fileall_$(whoami)_$(date +%y%m%d)"

# 扫描大于 100M 且修改时间超过 90 天的文件
bsub -n 5 -J scan -o filescan.out -e filescan.err \
  "ls -d ~/* |xargs -I[] -P 5 find [] -mtime +90 -size +100M -type f |xargs du -sm >fileall_$(whoami)_$(date +%y%m%d)"
```

### 文件数扫描
```bash
# 进入交互节点，查看当前目录下每个子目录的文件数
find . -maxdepth 1 -type d -print0 | xargs -P 10 -0 -I{} sh -c 'printf "%s\t%s\n" "{}" "$(find "{}" -type f -print | wc -l)"'
```

## 五、文件完整性检查

### MD5 校验（通用方式）
```bash
# 生成 md5 校验文件（同时对 5 个文件并行计算）
ls *gz|xargs -i -P 5 md5sum {} > md5.txt

# 查看生成的校验文件
cat md5.txt

# 利用 md5 校验文件验证数据完整性
md5sum -c md5.txt
```

### gzip 文件完整性检查
适用于没有原始 md5 校验文件的 gzip 文件：
```bash
# 批量并行检查（无输出则表示文件完整）
ls|xargs -i -P 5 gzip -t {}

# 单文件检查 — 出现如下报错则说明文件不完整
gzip -t file.fastq.gz
# 报错示例：gzip: file.fastq.gz: unexpected end of file
```
如有 pigz，使用 pigz 替代 gzip 速度更快。

### seqkit 校验 fq 文件完整性
```bash
# -j 10 多线程，-e 跳过错误继续
seqkit stats -j 10 *.fq.gz -e
```
文件有问题时会输出 WARN，正常则输出统计信息。

### bam 文件完整性检查
```bash
# 批量检查 bam 文件（cram 文件同样适用）
for i in *.bam; do (samtools quickcheck $i && echo "ok" || echo $i error); done
```

**建议在以下场景检查 bam 完整性**：
- 大量群体样本比对完成后
- 大量 bam 转 cram 之后
- 大量 bam 保存备份之前

### 双端测序校验（pecheck）
```bash
# 校验双端测序文件配对完整性
pecheck -i sample_R1.fq.gz -I sample_R2.fq.gz -j sample.json
```
输出 result 为 "passed" 则表示配对完整。

## 六、Genozip 基因组数据压缩

### 概述
Genozip 是专为基因组数据设计的高效压缩工具，相比 gzip 可节省至少 50% 以上空间。

**支持格式**：FASTQ、BAM、CRAM、VCF、FASTA 等
**关键特性**：
- 高压缩率（通常为原始大小的 10%-20%）
- 多线程压缩/解压
- 支持随机访问和部分解压
- 支持数据加密
- 支持压缩目录
- 压缩后自动校验数据一致性

**注意**：压缩和解压建议使用相同版本的 genozip。

### 加载与 License
```bash
# 载入 genozip 模块
module load genozip/15.0.4

# 将 license 拷到自己的 home 目录（执行一次即可）
cp $LIC ~

# 或使用 --licfile 参数指定 license 位置
genozip --licfile $LIC
```

### 压缩/解压 FASTQ 文件
```bash
# 压缩单个 fq.gz 文件
# -@4 使用 4 个线程
# --reference 使用参考基因组压缩（首次使用会生成 .genozip 索引文件）
genozip -@4 sample.fq.gz --reference ref.fa

# 解压（需指定参考基因组，若路径未变可省略 --reference）
genounzip -@4 sample.fq.genozip

# 使用 --REFERENCE（大写），输出文件中包含部分参考基因组，解压时不需要基因组
genozip -@4 sample.fq.gz --REFERENCE ref.fa
genounzip -@4 sample.fq.genozip

# 双端 fq 合并压缩（可获得更高压缩率）
genozip -@4 --reference ref.fa --pair sample_1.fq.gz sample_2.fq.gz

# 解压双端合并文件
genounzip -@4 --reference ref.fa sample_1+2.clean.fq.genozip
```

### 压缩/解压 BAM 文件
```bash
genozip -@4 sample_sorted.bam
genounzip -@4 sample_sorted.bam.genozip
```

### FQ + BAM 联合压缩（--deep 模式）
fq 和 bam 联合压缩后，bam 文件大小几乎可以不计：
```bash
genozip -@4 --deep --reference ref.fa sample_sorted.bam sample_1.fq.gz sample_2.fq.gz
genounzip sample_sorted.deep.genozip
```

### 压缩/解压 VCF 文件
```bash
genozip -@4 sample.vcf.gz
genounzip -@4 sample.vcf.gz.genozip
```

### 数据一致性说明
genozip 压缩过程分 2 步：压缩和校验。压缩完成后会自动将压缩文件在内存中解压并与原始文件比较，校验通过才算压缩完成。压缩成功后输出类似：
```
testing: genounzip sample.R1.fq.gz : verified as identical to the original FASTQ
```

**注意**：原始 gz 文件与 genozip 解压后的 gz 文件的 md5 值不一致，只有两者都解压成文本文件后的 md5 才一致：
```bash
# 验证方式
zcat file.fastq.gz | md5sum
```

### 压缩效果参考

| 物种 | 文件类型 | 原始大小 | genozip 大小 | 压缩率 |
|------|---------|---------|-------------|--------|
| 水稻 | fq.gz (R1) | 4.6G | 1.1G | ~76% |
| 棉花 | fq.gz (R1) | 15G | 3.2G | ~79% |
| 玉米 | fq.gz (R1) | 9.4G | 3.0G | ~68% |
| 水稻 | bam | 7.0G | 2.3G | ~67% |
| 棉花 | bam | 52G | 16G | ~69% |
| 水稻 | fq+fq+bam | 16.4G | 2.5G | ~85% |
| 水稻 | vcf.gz | 18M | 7.5M | ~58% |

### Genozip 用于下游分析（interleaved 格式）

genozip 将双端 fq 合并压缩后，文件格式为 interleaved（序列条目交替存储）。部分比对软件支持 interleaved 输入，可直接使用 genozip 文件而无需解压。

#### BWA / BWA-MEM2
```bash
genocat sample_1+2.fq.genozip | bwa mem $ref - -p -t 20 -T 0 \
  -R "@RG\tID:id\tSM:sample\tPL:Illumina" | samtools sort -@20 -o sample_sorted.bam
```

#### Bowtie2
Bowtie2 的 `--interleaved` 选项支持 interleaved 格式输入。

### 常见问题
- **Out of memory 报错**：减少 genozip 使用的线程数（`-@` 参数）
- **`genozip --deep` 压缩人的 fq+bam 时报错**：目前暂无法解决，建议分开压缩

## 七、常用操作速查

| 操作 | 命令 |
|------|------|
| 查看存储配额 | `diskquota` |
| 多线程压缩文件 | `pigz file.txt` |
| 多线程解压文件 | `pigz -d file.txt.gz` |
| 大文件远程拷贝 | `rsync -avP src/ dest/` |
| 生成 md5 校验 | `ls *gz\|xargs -i -P 5 md5sum {} > md5.txt` |
| 验证 md5 校验 | `md5sum -c md5.txt` |
| gzip 完整性检查 | `gzip -t file.gz` |
| bam 完整性检查 | `samtools quickcheck file.bam` |
| 双端 fq 校验 | `pecheck -i R1.fq.gz -I R2.fq.gz` |
| genozip 压缩 fq | `genozip -@4 file.fq.gz --reference ref.fa` |
| genozip 解压 | `genounzip -@4 file.genozip` |
| 共享给组 | `setfacl -m g:GROUP:rx /path` |
| 共享给用户 | `setfacl -m u:user:rx /path` |
| 删除共享权限 | `setfacl -x g:GROUP /path` |
| 查看 ACL 权限 | `getfacl /path` |
| 扫描大文本文件 | `find ~ -size +100M -type f -exec file {} \;` |
| 统计子目录文件数 | `find . -maxdepth 1 -type d \| xargs -I{} sh -c 'echo $(find "{}" -type f \| wc -l) {}'` |

## 八、最佳实践工作流

### 新数据接收流程
1. 接收原始 fq.gz 数据后，**立即做 md5 校验**
2. 记录 md5 值到文件备查
3. 开始分析前确认数据完整性

### 分析过程数据管理
1. 比对输出 bam/cram，不要输出 sam
2. 定期清理中间文件（如 sort 后的临时文件）
3. 定期用 `diskquota` 检查配额

### 项目结题归档
1. 清理所有中间文件和临时文件
2. 保留的 fq/bam/vcf 用 genozip 压缩归档
3. 已发表文章的原始数据如已上传 NCBI，可删除本地副本
4. 使用 rsync 备份重要数据到本地

### 跨组合作数据共享
1. 使用 ACL 精确控制权限（不要用 chmod 777）
2. 仅开放读权限，不开放写权限
3. 合作结束后及时删除 ACL 权限
