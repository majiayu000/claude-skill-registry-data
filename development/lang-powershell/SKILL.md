---
name: "lang-powershell"
description: "Fornece padrões de engenharia de software em PowerShell (Windows PowerShell 5.1 e PowerShell 7+ Core). Cobre automação, gestão de pipeline de objetos, modularização (módulos de script/manifestos), tratamento de erros defensivo (Try/Catch/Finally, ErrorActionPreference), tipagem forte, PSCustomObject e boas práticas de segurança (ExecutionPolicy, remoting e credenciais)."
---

# Habilidade de IA: Engenharia de PowerShell (PowerShell Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista no ecossistema **PowerShell** (suportando tanto Windows PowerShell 5.1 quanto PowerShell 7+ Cross-Platform), com foco em scripts robustos, modulares, testáveis e com alto desempenho em automação de infraestrutura e sistemas.

---

## 🧭 Diretrizes de Desenvolvimento em PowerShell

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Orientação a Objetos e Uso do Pipeline
- **Retorne Objetos, Não Texto**: Evite formatar saídas como texto cru ou usar `Write-Host` para dados estruturados. Em vez disso, emita objetos usando `[PSCustomObject]` ou `Write-Output`.
- **`Write-Host` vs `Write-Information` / `Write-Verbose`**: Use `Write-Verbose` para logs detalhados, `Write-Warning` para alertas e `Write-Error` para falhas. Evite `Write-Host` a menos que esteja criando uma interface interativa específica no console.
- **Pipeline-Awareness**: Projete funções avançadas para aceitar entrada via pipeline (`ValueFromPipeline` ou `ValueFromPipelineByPropertyName`).

### 2. Tratamento de Erros e Execução Defensiva
- **Parada em Erros**: Utilize `$ErrorActionPreference = 'Stop'` no topo dos scripts ou use `-ErrorAction Stop` em cmdlets específicos para garantir que erros não críticos (*non-terminating errors*) sejam convertidos em exceções capturáveis.
- **Blocos Try / Catch / Finally**: Sempre envolva chamadas a APIs nativas do .NET ou operações de E/S em blocos `Try/Catch` tipados:
  ```powershell
  try {
      [System.IO.File]::ReadAllText($filePath)
  } catch [System.IO.FileNotFoundException] {
      Write-Error "Arquivo não encontrado: $filePath"
  } catch {
      Write-Error "Erro inesperado: $_"
  }
  ```

### 3. Funções Avançadas e CmdletBinding
- **Uso de `[CmdletBinding()]`**: Todas as funções reutilizáveis devem declarar `[CmdletBinding()]` para suportar parâmetros comuns como `-Verbose`, `-Debug`, `-ErrorAction` e `-WhatIf` / `-Confirm` (quando houver suporte a `SupportsShouldProcess`).
- **Validação Estrita de Parâmetros**: Adicione atributos de validação como `[ValidateNotNullOrEmpty()]`, `[ValidateSet()]` ou `[ValidateRange()]`.

### 4. Desempenho e Tipagem Forte
- **Evitar Concatenação de Arrays (`+=`)**: O operador `+=` recria todo o array na memória a cada iteração. Para coleções grandes, use `[System.Collections.Generic.List[PSObject]]` ou atribua o resultado do loop diretamente a uma variável:
  ```powershell
  $results = foreach ($item in $items) {
      [PSCustomObject]@{
          Id   = $item.Id
          Name = $item.Name
      }
  }
  ```
- **Tipagem de Parâmetros**: Declare explicitamente os tipos de todos os parâmetros (`[string]`, `[int]`, `[switch]`, `[datetime]`) para evitar coerção implícita e comportamentos inesperados.

### 5. Segurança e Boas Práticas
- **Evitar `Invoke-Expression` (iex)**: Nunca utilize `Invoke-Expression` com strings construídas dinamicamente ou oriundas de fontes não confiáveis para prevenir injeção de código.
- **Gerenciamento de Credenciais**: Nunca insira senhas ou tokens como texto limpo (*hardcoded*). Utilize `[PSCredential]`, o módulo `SecretManagement` ou variáveis de ambiente seguras.

---

## 🧰 Padrões de Código Recomendados

### Função Avançada Completa com Suporte a Pipeline e Validation

```powershell
function Get-SystemServiceReport {
    [CmdletBinding(SupportsShouldProcess = $false)]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [string[]]$ServiceName,

        [Parameter(Mandatory = $false)]
        [ValidateSet('Running', 'Stopped', 'All')]
        [string]$StatusFilter = 'All'
    )

    begin {
        Write-Verbose "Iniciando relatório de serviços..."
        $results = [System.Collections.Generic.List[PSCustomObject]]::new()
    }

    process {
        foreach ($name in $ServiceName) {
            Write-Verbose "Processando serviço: $name"
            try {
                $service = Get-Service -Name $name -ErrorAction Stop
                
                if ($StatusFilter -eq 'All' -or $service.Status -eq $StatusFilter) {
                    $results.Add([PSCustomObject]@{
                        ServiceName = $service.Name
                        DisplayName = $service.DisplayName
                        Status      = $service.Status.ToString()
                        StartType   = $service.StartType.ToString()
                        Timestamp   = [DateTime]::UtcNow
                    })
                }
            } catch [Microsoft.PowerShell.Commands.ServiceCommandException] {
                Write-Warning "Serviço não encontrado: $name"
            } catch {
                Write-Error "Erro ao consultar o serviço $name: $_"
            }
        }
    }

    end {
        Write-Verbose "Relatório concluído com $($results.Count) item(ns)."
        return $results
    }
}

# Exemplo de Uso via Pipeline:
# @('wuauserv', 'Spooler', 'NonExistentService') | Get-SystemServiceReport -StatusFilter Running -Verbose
```

### Script de Automação com Robustez e Logs Structurados

```powershell
# Requires -Version 5.1
$ErrorActionPreference = 'Stop'

function Invoke-MaintenanceTask {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetDirectory,

        [Parameter(Mandatory = $false)]
        [int]$DaysOld = 30
    )

    if (-not (Test-Path -Path $TargetDirectory -PathType Container)) {
        throw [System.IO.DirectoryNotFoundException]::new("O diretório de destino não existe: $TargetDirectory")
    }

    $cutoffDate = (Get-Date).AddDays(-$DaysOld)
    Write-Verbose "Limpando arquivos anteriores a $cutoffDate em $TargetDirectory"

    $filesToRemove = Get-ChildItem -Path $TargetDirectory -File -Recurse | 
        Where-Object { $_.LastWriteTime -lt $cutoffDate }

    $removedCount = 0
    foreach ($file in $filesToRemove) {
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction Stop
            $removedCount++
            Write-Verbose "Arquivo removido: $($file.FullName)"
        } catch {
            Write-Warning "Falha ao remover $($file.FullName): $_"
        }
    }

    return [PSCustomObject]@{
        TargetDirectory = $TargetDirectory
        FilesEvaluated  = $filesToRemove.Count
        FilesRemoved    = $removedCount
        ExecutionTime   = [DateTime]::Now
    }
}
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Injeção de Script (`Invoke-Expression`)**: Evite usar `Invoke-Expression` ou `iex` com entradas do usuário. Use objetos com tipagem forte ou passe parâmetros via `ScriptBlock` parametrizado.
- **Bypasses de Execução e EDR**: Lembre-se de que a política de execução (`ExecutionPolicy`) é uma proteção contra acidentes, não um limite de segurança; atacantes conseguem contorná-la facilmente (ex: `-ExecutionPolicy Bypass`).
- **Segredos Hardcoded**: Nunca armazene senhas ou tokens em variáveis no código dos scripts. Utilize o utilitário `SecretManagement` ou criptografia DPAPI (`SecureString`).

