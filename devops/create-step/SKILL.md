---
name: create-step
description: Cria um novo step para o bootstrap macOS. Use quando o usuário pedir para adicionar uma nova configuração ou instalação ao bootstrap.
---

# Criar Novo Step para Bootstrap

## Estrutura de um Step

Cada step precisa de dois arquivos:
1. `lib/bootstrap/steps/<nome>.rb` - Implementação
2. `test/steps/<nome>_test.rb` - Testes

## Template do Step

```ruby
# frozen_string_literal: true

require_relative '../step'

module Bootstrap
  module Steps
    class NomeDoStep < Step
      def name
        'Nome para Exibição'
      end

      def installed?
        # Retorna true se já está configurado (idempotência)
        # Exemplos:
        # - shell.file_exists?(path)
        # - shell.directory_exists?(path)
        # - shell.success?('which comando')
        # - Verificar conteúdo de arquivo de configuração
      end

      def install!
        # Executa a instalação/configuração
        # Use shell.run(command) para comandos não-interativos
        # Use shell.run_interactive(command) para comandos que precisam de TTY
      end

      private

      # Métodos auxiliares privados
    end
  end
end
```

## Template do Teste

```ruby
# frozen_string_literal: true

require_relative '../test_helper'
require 'bootstrap/steps/<nome>'

class NomeDoStepTest < Minitest::Test
  class MockShell
    attr_accessor :commands_run, :run_results, :existing_files, :success_results

    def initialize
      @commands_run = []
      @run_results = {}
      @existing_files = []
      @success_results = {}
    end

    def run(command)
      @commands_run << command
      @run_results[command] || Struct.new(:success?, :stderr, :output).new(true, '', '')
    end

    def run_interactive(command)
      @commands_run << command
      @run_results[command] || Struct.new(:success?, :stderr, :output).new(true, '', '')
    end

    def file_exists?(path)
      @existing_files.include?(path)
    end

    def directory_exists?(path)
      @existing_files.include?(path)
    end

    def success?(command)
      @commands_run << command
      @success_results.fetch(command, false)
    end
  end

  def setup
    @shell = MockShell.new
    @step = Bootstrap::Steps::NomeDoStep.new(shell: @shell)
  end

  def test_name
    assert_equal 'Nome para Exibição', @step.name
  end

  def test_installed_returns_false_when_not_configured
    # Configure mock para retornar estado não-instalado
    refute @step.installed?
  end

  def test_installed_returns_true_when_configured
    # Configure mock para retornar estado instalado
    assert @step.installed?
  end

  def test_install_executes_expected_commands
    @step.install!
    # Verifique comandos executados
    assert_includes @shell.commands_run, 'comando esperado'
  end

  def test_run_skips_when_already_configured
    # Configure mock para estado instalado
    result = @step.run!
    assert_equal :skipped, result[:status]
  end
end
```

## Checklist

1. [ ] Criar `lib/bootstrap/steps/<nome>.rb`
2. [ ] Implementar `name`, `installed?`, `install!`
3. [ ] Criar `test/steps/<nome>_test.rb`
4. [ ] Adicionar require em `bin/bootstrap`
5. [ ] Adicionar step na lista de steps em `bin/bootstrap`
6. [ ] Rodar `rake test` para validar

## Comandos Shell Disponíveis

| Método | Uso |
|--------|-----|
| `shell.run(cmd)` | Executa comando, captura output |
| `shell.run_interactive(cmd)` | Executa com TTY (para sudo, etc) |
| `shell.success?(cmd)` | Retorna true/false |
| `shell.file_exists?(path)` | Verifica arquivo |
| `shell.directory_exists?(path)` | Verifica diretório |

## Resultado de shell.run

```ruby
result = shell.run('comando')
result.success?  # true/false
result.output    # stdout (stripped)
result.stdout    # stdout raw
result.stderr    # stderr
```

## Exemplos de installed?

```ruby
# Verificar se programa existe
def installed?
  shell.success?('which programa')
end

# Verificar se arquivo de configuração existe
def installed?
  shell.file_exists?(CONFIG_PATH)
end

# Verificar valor de configuração
def installed?
  result = shell.run('defaults read com.apple.dock tilesize')
  result.success? && result.output.strip.to_i == 36
end

# Combinar múltiplas verificações
def installed?
  programa_instalado? && configuracao_correta?
end
```

## Exemplos de install!

```ruby
# Instalar via Homebrew
def install!
  result = shell.run('brew install programa')
  raise "Falhou: #{result.stderr}" unless result.success?
end

# Comando interativo (precisa de senha)
def install!
  result = shell.run_interactive('sudo comando')
  raise 'Falhou' unless result.success?
end

# Criar arquivo de configuração
def install!
  File.write(CONFIG_PATH, CONFIG_CONTENT)
end

# Múltiplas etapas
def install!
  instalar_dependencia
  configurar_sistema
  reiniciar_servico
end
```
