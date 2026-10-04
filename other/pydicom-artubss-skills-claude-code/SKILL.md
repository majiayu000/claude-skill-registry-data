---
name: pydicom
description: Biblioteca Python para trabalhar com arquivos DICOM (Digital Imaging and Communications in Medicine). Use essa skill ao ler, escrever ou modificar dados de imagens médicas em formato DICOM, extrair dados de pixel de imagens médicas (TC, RM, Raio-X, ultrassom), anonimizar arquivos DICOM, trabalhar com metadados e tags DICOM, converter imagens DICOM para outros formatos, processar dados DICOM comprimidos ou processar conjuntos de dados de imagens médicas. Aplica-se a tarefas envolvendo análise de imagens médicas, sistemas PACS, fluxos de trabalho de radiologia e aplicações de imagem médica.
---

# Pydicom

## Visão Geral

Pydicom é um pacote Python puro para trabalhar com arquivos DICOM, o formato padrão para dados de imagens médicas. Essa skill oferece orientação sobre leitura, escrita e manipulação de arquivos DICOM, incluindo trabalho com dados de pixel, metadados e vários formatos de compressão.

## Quando Usar Essa Skill

Use essa skill ao trabalhar com:
- Arquivos de imagens médicas (TC, RM, Raio-X, ultrassom, PET, etc.)
- Conjuntos de dados DICOM que requerem extração ou modificação de metadados
- Extração de dados de pixel e processamento de imagem a partir de exames médicos
- Anonimização de DICOM para pesquisa ou compartilhamento de dados
- Conversão de arquivos DICOM para formatos de imagem padrão
- Dados DICOM comprimidos que requerem descompressão
- Sequências DICOM e relatórios estruturados
- Reconstrução de volume multi-slice
- Integração com PACS (Picture Archiving and Communication System)

## Instalação

Instale pydicom e dependências comuns:

```bash
uv pip install pydicom
uv pip install pillow  # Para conversão de formato de imagem
uv pip install numpy   # Para manipulação de array de pixel
uv pip install matplotlib  # Para visualização
```

Para lidar com arquivos DICOM comprimidos, pacotes adicionais podem ser necessários:

```bash
uv pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg  # Compressão JPEG
uv pip install python-gdcm  # Manipulador de compressão alternativo
```

## Fluxos de Trabalho Principais

### Leitura de Arquivos DICOM

Leia um arquivo DICOM usando `pydicom.dcmread()`:

```python
import pydicom

# Ler um arquivo DICOM
ds = pydicom.dcmread('path/to/file.dcm')

# Acessar metadados
print(f"Patient Name: {ds.PatientName}")
print(f"Study Date: {ds.StudyDate}")
print(f"Modality: {ds.Modality}")

# Exibir todos os elementos
print(ds)
```

**Pontos-chave:**
- `dcmread()` retorna um objeto `Dataset`
- Acesse elementos de dados usando notação de atributo (ex: `ds.PatientName`) ou notação de tag (ex: `ds[0x0010, 0x0010]`)
- Use `ds.file_meta` para acessar metadados de arquivo como Transfer Syntax UID
- Trate atributos ausentes com `getattr(ds, 'AttributeName', default_value)` ou `hasattr(ds, 'AttributeName')`

### Trabalhando com Dados de Pixel

Extraia e manipule dados de imagem a partir de arquivos DICOM:

```python
import pydicom
import numpy as np
import matplotlib.pyplot as plt

# Ler arquivo DICOM
ds = pydicom.dcmread('image.dcm')

# Obter array de pixel (requer numpy)
pixel_array = ds.pixel_array

# Informações de imagem
print(f"Shape: {pixel_array.shape}")
print(f"Data type: {pixel_array.dtype}")
print(f"Rows: {ds.Rows}, Columns: {ds.Columns}")

# Aplicar janelamento para exibição (TC/RM)
if hasattr(ds, 'WindowCenter') and hasattr(ds, 'WindowWidth'):
    from pydicom.pixel_data_handlers.util import apply_voi_lut
    windowed_image = apply_voi_lut(pixel_array, ds)
else:
    windowed_image = pixel_array

# Exibir imagem
plt.imshow(windowed_image, cmap='gray')
plt.title(f"{ds.Modality} - {ds.StudyDescription}")
plt.axis('off')
plt.show()
```

**Trabalhando com imagens coloridas:**

```python
# Imagens RGB têm shape (rows, columns, 3)
if ds.PhotometricInterpretation == 'RGB':
    rgb_image = ds.pixel_array
    plt.imshow(rgb_image)
elif ds.PhotometricInterpretation == 'YBR_FULL':
    from pydicom.pixel_data_handlers.util import convert_color_space
    rgb_image = convert_color_space(ds.pixel_array, 'YBR_FULL', 'RGB')
    plt.imshow(rgb_image)
```

**Imagens multi-frame (vídeos/séries):**

```python
# Para arquivos DICOM multi-frame
if hasattr(ds, 'NumberOfFrames') and ds.NumberOfFrames > 1:
    frames = ds.pixel_array  # Shape: (num_frames, rows, columns)
    print(f"Number of frames: {frames.shape[0]}")

    # Exibir frame específico
    plt.imshow(frames[0], cmap='gray')
```

### Convertendo DICOM para Formatos de Imagem

Use o script fornecido `dicom_to_image.py` ou converta manualmente:

```python
from PIL import Image
import pydicom
import numpy as np

ds = pydicom.dcmread('input.dcm')
pixel_array = ds.pixel_array

# Normalizar para intervalo 0-255
if pixel_array.dtype != np.uint8:
    pixel_array = ((pixel_array - pixel_array.min()) /
                   (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)

# Salvar como PNG
image = Image.fromarray(pixel_array)
image.save('output.png')
```

Use o script: `python scripts/dicom_to_image.py input.dcm output.png`

### Modificando Metadados

Modifique elementos de dados DICOM:

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# Modificar elementos existentes
ds.PatientName = "Doe^John"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyDescription = "Modified Study"

# Adicionar novos elementos
ds.SeriesNumber = 1
ds.SeriesDescription = "New Series"

# Remover elementos
if hasattr(ds, 'PatientComments'):
    delattr(ds, 'PatientComments')
# Ou usando del
if 'PatientComments' in ds:
    del ds.PatientComments

# Salvar arquivo modificado
ds.save_as('modified.dcm')
```

### Anonimizando Arquivos DICOM

Remova ou substitua informações de identificação pessoal do paciente:

```python
import pydicom
from datetime import datetime

ds = pydicom.dcmread('input.dcm')

# Tags que comumente contêm PHI (Protected Health Information)
tags_to_anonymize = [
    'PatientName', 'PatientID', 'PatientBirthDate',
    'PatientSex', 'PatientAge', 'PatientAddress',
    'InstitutionName', 'InstitutionAddress',
    'ReferringPhysicianName', 'PerformingPhysicianName',
    'OperatorsName', 'StudyDescription', 'SeriesDescription',
]

# Remover ou substituir dados sensíveis
for tag in tags_to_anonymize:
    if hasattr(ds, tag):
        if tag in ['PatientName', 'PatientID']:
            setattr(ds, tag, 'ANONYMOUS')
        elif tag == 'PatientBirthDate':
            setattr(ds, tag, '19000101')
        else:
            delattr(ds, tag)

# Atualizar datas para manter relações temporais
if hasattr(ds, 'StudyDate'):
    # Deslocar datas por um offset aleatório
    ds.StudyDate = '20000101'

# Manter dados de pixel intactos
ds.save_as('anonymized.dcm')
```

Use o script fornecido: `python scripts/anonymize_dicom.py input.dcm output.dcm`

### Escrevendo Arquivos DICOM

Crie arquivos DICOM do zero:

```python
import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
import numpy as np

# Criar informações de meta arquivo
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = pydicom.uid.generate_uid()
file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

# Criar a instância FileDataset
ds = FileDataset('new_dicom.dcm', {}, file_meta=file_meta, preamble=b"\0" * 128)

# Adicionar elementos DICOM obrigatórios
ds.PatientName = "Test^Patient"
ds.PatientID = "123456"
ds.Modality = "CT"
ds.StudyDate = datetime.now().strftime('%Y%m%d')
ds.StudyTime = datetime.now().strftime('%H%M%S')
ds.ContentDate = ds.StudyDate
ds.ContentTime = ds.StudyTime

# Adicionar elementos específicos de imagem
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.Rows = 512
ds.Columns = 512
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 0

# Criar dados de pixel
pixel_array = np.random.randint(0, 4096, (512, 512), dtype=np.uint16)
ds.PixelData = pixel_array.tobytes()

# Adicionar UIDs obrigatórios
ds.SOPClassUID = pydicom.uid.CTImageStorage
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.SeriesInstanceUID = pydicom.uid.generate_uid()
ds.StudyInstanceUID = pydicom.uid.generate_uid()

# Salvar arquivo
ds.save_as('new_dicom.dcm')
```

### Compressão e Descompressão

Lide com arquivos DICOM comprimidos:

```python
import pydicom

# Ler arquivo DICOM comprimido
ds = pydicom.dcmread('compressed.dcm')

# Verificar syntax de transferência
print(f"Transfer Syntax: {ds.file_meta.TransferSyntaxUID}")
print(f"Transfer Syntax Name: {ds.file_meta.TransferSyntaxUID.name}")

# Descomprimir e salvar como descomprimido
ds.decompress()
ds.save_as('uncompressed.dcm', write_like_original=False)

# Ou comprimir ao salvar (requer codificador apropriado)
ds_uncompressed = pydicom.dcmread('uncompressed.dcm')
ds_uncompressed.compress(pydicom.uid.JPEGBaseline8Bit)
ds_uncompressed.save_as('compressed_jpeg.dcm')
```

**Syntaxes de transferência comuns:**
- `ExplicitVRLittleEndian` - Descomprimido, mais comum
- `JPEGBaseline8Bit` - Compressão JPEG com perda
- `JPEGLossless` - Compressão JPEG sem perda
- `JPEG2000Lossless` - JPEG 2000 sem perda
- `RLELossless` - Codificação Run-Length sem perda

Veja `references/transfer_syntaxes.md` para lista completa.

### Trabalhando com Sequências DICOM

Lide com estruturas de dados aninhadas:

```python
import pydicom

ds = pydicom.dcmread('file.dcm')

# Acessar sequências
if 'ReferencedStudySequence' in ds:
    for item in ds.ReferencedStudySequence:
        print(f"Referenced SOP Instance UID: {item.ReferencedSOPInstanceUID}")

# Criar uma sequência
from pydicom.sequence import Sequence

sequence_item = Dataset()
sequence_item.ReferencedSOPClassUID = pydicom.uid.CTImageStorage
sequence_item.ReferencedSOPInstanceUID = pydicom.uid.generate_uid()

ds.ReferencedImageSequence = Sequence([sequence_item])
```

### Processando Séries DICOM

Trabalhe com múltiplos arquivos DICOM relacionados:

```python
import pydicom
import numpy as np
from pathlib import Path

# Ler todos os arquivos DICOM em um diretório
dicom_dir = Path('dicom_series/')
slices = []

for file_path in dicom_dir.glob('*.dcm'):
    ds = pydicom.dcmread(file_path)
    slices.append(ds)

# Ordenar por localização de slice ou número de instância
slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
# Ou: slices.sort(key=lambda x: int(x.InstanceNumber))

# Criar volume 3D
volume = np.stack([s.pixel_array for s in slices])
print(f"Volume shape: {volume.shape}")  # (num_slices, rows, columns)

# Obter informações de espaçamento para escala apropriada
pixel_spacing = slices[0].PixelSpacing  # [row_spacing, col_spacing]
slice_thickness = slices[0].SliceThickness
print(f"Voxel size: {pixel_spacing[0]}x{pixel_spacing[1]}x{slice_thickness} mm")
```

## Scripts Auxiliares

Essa skill inclui scripts utilitários no diretório `scripts/`:

### anonymize_dicom.py
Anonimize arquivos DICOM removendo ou substituindo Protected Health Information (PHI).

```bash
python scripts/anonymize_dicom.py input.dcm output.dcm
```

### dicom_to_image.py
Converta arquivos DICOM para formatos de imagem comuns (PNG, JPEG, TIFF).

```bash
python scripts/dicom_to_image.py input.dcm output.png
python scripts/dicom_to_image.py input.dcm output.jpg --format JPEG
```

### extract_metadata.py
Extraia e exiba metadados DICOM em formato legível.

```bash
python scripts/extract_metadata.py file.dcm
python scripts/extract_metadata.py file.dcm --output metadata.txt
```

## Materiais de Referência

Informações de referência detalhadas estão disponíveis no diretório `references/`:

- **common_tags.md**: Lista abrangente de tags DICOM comumente usadas organizadas por categoria (Paciente, Estudo, Série, Imagem, etc.)
- **transfer_syntaxes.md**: Referência completa de syntaxes de transferência DICOM e formatos de compressão

## Problemas Comuns e Soluções

**Problema: "Unable to decode pixel data"**
- Solução: Instale manipuladores de compressão adicionais: `uv pip install pylibjpeg pylibjpeg-libjpeg python-gdcm`

**Problema: "AttributeError" ao acessar tags**
- Solução: Verifique se atributo existe com `hasattr(ds, 'AttributeName')` ou use `ds.get('AttributeName', default)`

**Problema: Exibição de imagem incorreta (muito escura/clara)**
- Solução: Aplique janelamento VOI LUT: `apply_voi_lut(pixel_array, ds)` ou ajuste manualmente com `WindowCenter` e `WindowWidth`

**Problema: Problemas de memória com séries grandes**
- Solução: Processe arquivos iterativamente, use arrays memory-mapped ou faça downsample de imagens

## Melhores Práticas

1. **Sempre verifique atributos obrigatórios** antes de acessá-los usando `hasattr()` ou `get()`
2. **Preserve metadados de arquivo** ao modificar arquivos usando `save_as()` com `write_like_original=True`
3. **Use Transfer Syntax UIDs** para entender formato de compressão antes de processar dados de pixel
4. **Trate exceções** ao ler arquivos de fontes não confiáveis
5. **Aplique janelamento apropriado** (VOI LUT) para visualização de imagens médicas
6. **Mantenha informações espaciais** (espaçamento de pixel, espessura de slice) ao processar volumes 3D
7. **Verifique anonimização** completamente antes de compartilhar dados médicos
8. **Use UIDs corretamente** - gere novos UIDs ao criar novas instâncias, preserve-os ao modificar

## Documentação

Documentação oficial do pydicom: https://pydicom.github.io/pydicom/dev/
- Guia do Usuário: https://pydicom.github.io/pydicom/dev/guides/user/index.html
- Tutoriais: https://pydicom.github.io/pydicom/dev/tutorials/index.html
- Referência de API: https://pydicom.github.io/pydicom/dev/reference/index.html
- Exemplos: https://pydicom.github.io/pydicom/dev/auto_examples/index.html