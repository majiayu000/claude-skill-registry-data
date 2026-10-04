---
name: pysam
description: "Kit de ferramentas para arquivos genômicos. Leia/escreva alinhamentos SAM/BAM/CRAM, variantes VCF/BCF, sequências FASTA/FASTQ, extraia regiões, calcule cobertura, para pipelines de processamento de dados NGS."
---

# Pysam

## Visão Geral

Pysam é um módulo Python para ler, manipular e escrever conjuntos de dados genômicos. Leia/escreva arquivos de alinhamento SAM/BAM/CRAM, arquivos de variantes VCF/BCF e sequências FASTA/FASTQ com uma interface Pythônica para htslib. Consulte arquivos indexados por tabix, execute análise de pileup para cobertura e execute comandos samtools/bcftools.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Trabalhar com arquivos de alinhamento de sequenciamento (BAM/CRAM)
- Analisar variantes genéticas (VCF/BCF)
- Extrair sequências de referência ou regiões de genes
- Processar dados de sequenciamento bruto (FASTQ)
- Calcular cobertura ou profundidade de leitura
- Implementar pipelines de análise bioinformática
- Controle de qualidade de dados de sequenciamento
- Workflows de chamada e anotação de variantes

## Início Rápido

### Instalação
```bash
uv pip install pysam
```

### Exemplos Básicos

**Leia arquivo de alinhamento:**
```python
import pysam

# Open BAM file and fetch reads in region
samfile = pysam.AlignmentFile("example.bam", "rb")
for read in samfile.fetch("chr1", 1000, 2000):
    print(f"{read.query_name}: {read.reference_start}")
samfile.close()
```

**Leia arquivo de variantes:**
```python
# Open VCF file and iterate variants
vcf = pysam.VariantFile("variants.vcf")
for variant in vcf:
    print(f"{variant.chrom}:{variant.pos} {variant.ref}>{variant.alts}")
vcf.close()
```

**Consulte sequência de referência:**
```python
# Open FASTA and extract sequence
fasta = pysam.FastaFile("reference.fasta")
sequence = fasta.fetch("chr1", 1000, 2000)
print(sequence)
fasta.close()
```

## Capacidades Principais

### 1. Operações com Arquivos de Alinhamento (SAM/BAM/CRAM)

Use a classe `AlignmentFile` para trabalhar com leituras de sequenciamento alinhadas. Isto é apropriado para analisar resultados de mapeamento, calcular cobertura, extrair leituras ou controle de qualidade.

**Operações comuns:**
- Abrir e ler arquivos BAM/SAM/CRAM
- Buscar leituras de regiões genômicas específicas
- Filtrar leituras por qualidade de mapeamento, flags ou outros critérios
- Escrever alinhamentos filtrados ou modificados
- Calcular estatísticas de cobertura
- Realizar análise de pileup (cobertura base a base)
- Acessar sequências de leitura, pontuações de qualidade e informações de alinhamento

**Referência:** Veja `references/alignment_files.md` para documentação detalhada sobre:
- Abrir e ler arquivos de alinhamento
- Atributos e métodos de AlignedSegment
- Busca baseada em região com `fetch()`
- Análise de pileup para cobertura
- Escrita e criação de arquivos BAM
- Sistemas de coordenadas e indexação
- Dicas de otimização de desempenho

### 2. Operações com Arquivos de Variantes (VCF/BCF)

Use a classe `VariantFile` para trabalhar com variantes genéticas de pipelines de chamada de variantes. Isto é apropriado para análise de variantes, filtragem, anotação ou genética de populações.

**Operações comuns:**
- Ler e escrever arquivos VCF/BCF
- Consultar variantes em regiões específicas
- Acessar informações de variantes (posição, alelos, qualidade)
- Extrair dados de genótipo para amostras
- Filtrar variantes por qualidade, frequência de alelo ou outros critérios
- Anotar variantes com informações adicionais
- Subconjuntar amostras ou regiões

**Referência:** Veja `references/variant_files.md` para documentação detalhada sobre:
- Abrir e ler arquivos de variantes
- Atributos e métodos de VariantRecord
- Acessar campos INFO e FORMAT
- Trabalhar com genótipos e amostras
- Criar e escrever arquivos VCF
- Filtrar e subconjuntar variantes
- Operações com VCF multi-amostra

### 3. Operações com Arquivos de Sequência (FASTA/FASTQ)

Use `FastaFile` para acesso aleatório a sequências de referência e `FastxFile` para ler dados de sequenciamento bruto. Isto é apropriado para extrair sequências de genes, validar variantes contra referência ou processar leituras brutas.

**Operações comuns:**
- Consultar sequências de referência por coordenadas genômicas
- Extrair sequências para genes ou regiões de interesse
- Ler arquivos FASTQ com pontuações de qualidade
- Validar alelos de referência de variantes
- Calcular estatísticas de sequência
- Filtrar leituras por qualidade ou comprimento
- Converter entre formatos FASTA e FASTQ

**Referência:** Veja `references/sequence_files.md` para documentação detalhada sobre:
- Acesso e indexação de arquivos FASTA
- Extração de sequências por região
- Manejo de complemento reverso para genes
- Leitura sequencial de arquivos FASTQ
- Conversão e filtragem de pontuação de qualidade
- Trabalho com arquivos indexados por tabix (BED, GTF, GFF)
- Padrões comuns de processamento de sequência

### 4. Workflows Bioinformáticos Integrados

Pysam é excelente em integrar múltiplos tipos de arquivo para análises genômicas abrangentes. Workflows comuns combinam arquivos de alinhamento, arquivos de variantes e sequências de referência.

**Workflows comuns:**
- Calcular estatísticas de cobertura para regiões específicas
- Validar variantes contra leituras alinhadas
- Anotar variantes com informações de cobertura
- Extrair sequências ao redor de posições de variantes
- Filtrar alinhamentos ou variantes com base em múltiplos critérios
- Gerar tracks de cobertura para visualização
- Controle de qualidade em múltiplos tipos de dados

**Referência:** Veja `references/common_workflows.md` para exemplos detalhados de:
- Workflows de controle de qualidade (estatísticas BAM, consistência de referência)
- Análise de cobertura (cobertura por base, detecção de baixa cobertura)
- Análise de variantes (anotação, filtragem por suporte de leitura)
- Extração de sequência (contextos de variantes, sequências de genes)
- Filtragem e subconjuntagem de leituras
- Padrões de integração (BAM+VCF, VCF+BED, etc.)
- Otimização de desempenho para workflows complexos

## Conceitos-Chave

### Sistemas de Coordenadas

**Crítico:** Pysam usa coordenadas **0-based, meio-abertas** (convenção Python):
- Posições iniciais são 0-based (primeira base é posição 0)
- Posições finais são exclusivas (não incluídas no intervalo)
- Região 1000-2000 inclui bases 1000-1999 (1000 bases no total)

**Exceção:** Strings de região em `fetch()` seguem convenção samtools (1-based):
```python
samfile.fetch("chr1", 999, 2000)      # 0-based: positions 999-1999
samfile.fetch("chr1:1000-2000")       # 1-based string: positions 1000-2000
```

**Arquivos VCF:** Usam coordenadas 1-based no formato de arquivo, mas `VariantRecord.start` é 0-based.

### Requisitos de Indexação

Acesso aleatório a regiões genômicas específicas requer arquivos de índice:
- **Arquivos BAM**: Requerem índice `.bai` (criar com `pysam.index()`)
- **Arquivos CRAM**: Requerem índice `.crai`
- **Arquivos FASTA**: Requerem índice `.fai` (criar com `pysam.faidx()`)
- **Arquivos VCF.gz**: Requerem índice tabix `.tbi` (criar com `pysam.tabix_index()`)
- **Arquivos BCF**: Requerem índice `.csi`

Sem um índice, use `fetch(until_eof=True)` para leitura sequencial.

### Modos de Arquivo

Especifique formato ao abrir arquivos:
- `"rb"` - Ler BAM (binário)
- `"r"` - Ler SAM (texto)
- `"rc"` - Ler CRAM
- `"wb"` - Escrever BAM
- `"w"` - Escrever SAM
- `"wc"` - Escrever CRAM

### Considerações de Desempenho

1. **Sempre use arquivos indexados** para operações de acesso aleatório
2. **Use `pileup()` para análise coluna a coluna** em vez de operações fetch repetidas
3. **Use `count()` para contagem** em vez de iterar e contar manualmente
4. **Processe regiões em paralelo** ao analisar regiões genômicas independentes
5. **Feche arquivos explicitamente** para liberar recursos
6. **Use `until_eof=True`** para processamento sequencial sem índice
7. **Evite múltiplos iteradores** a menos que necessário (use `multiple_iterators=True` se necessário)

## Armadilhas Comuns

1. **Confusão de coordenadas:** Lembre-se dos sistemas 0-based vs 1-based em diferentes contextos
2. **Índices ausentes:** Muitas operações requerem arquivos de índice—crie-os primeiro
3. **Sobreposições parciais:** `fetch()` retorna leituras que sobrepõem limites de região, não apenas aquelas totalmente contidas
4. **Escopo do iterador:** Mantenha referências do iterador pileup vivas para evitar erro "PileupProxy accessed after iterator finished"
5. **Edição de pontuação de qualidade:** Não pode modificar `query_qualities` no local após alterar `query_sequence`—crie uma cópia primeiro
6. **Limitações de stream:** Apenas stdin/stdout são suportados para streaming, não objetos de arquivo Python arbitrários
7. **Segurança de thread:** Enquanto a GIL é liberada durante I/O, a segurança abrangente de thread não foi totalmente validada

## Ferramentas de Linha de Comando

Pysam fornece acesso a comandos samtools e bcftools:

```python
# Sort BAM file
pysam.samtools.sort("-o", "sorted.bam", "input.bam")

# Index BAM
pysam.samtools.index("sorted.bam")

# View specific region
pysam.samtools.view("-b", "-o", "region.bam", "input.bam", "chr1:1000-2000")

# BCF tools
pysam.bcftools.view("-O", "z", "-o", "output.vcf.gz", "input.vcf")
```

**Tratamento de erros:**
```python
try:
    pysam.samtools.sort("-o", "output.bam", "input.bam")
except pysam.SamtoolsError as e:
    print(f"Error: {e}")
```

## Recursos

### references/

Documentação detalhada para cada capacidade principal:

- **alignment_files.md** - Guia completo para operações SAM/BAM/CRAM, incluindo classe AlignmentFile, atributos de AlignedSegment, operações fetch, análise de pileup e escrita de alinhamentos

- **variant_files.md** - Guia completo para operações VCF/BCF, incluindo classe VariantFile, atributos de VariantRecord, manejo de genótipo, campos INFO/FORMAT e operações multi-amostra

- **sequence_files.md** - Guia completo para operações FASTA/FASTQ, incluindo classes FastaFile e FastxFile, extração de sequência, manejo de pontuação de qualidade e acesso a arquivos indexados por tabix

- **common_workflows.md** - Exemplos práticos de workflows bioinformáticos integrados combinando múltiplos tipos de arquivo, incluindo controle de qualidade, análise de cobertura, validação de variantes e extração de sequência

## Obtendo Ajuda

Para informações detalhadas sobre operações específicas, consulte o documento de referência apropriado:

- Trabalhar com arquivos BAM ou calcular cobertura → `alignment_files.md`
- Analisar variantes ou genótipos → `variant_files.md`
- Extrair sequências ou processar FASTQ → `sequence_files.md`
- Workflows complexos integrando múltiplos tipos de arquivo → `common_workflows.md`

Documentação oficial: https://pysam.readthedocs.io/