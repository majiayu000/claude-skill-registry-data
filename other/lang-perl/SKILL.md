---
name: "lang-perl"
description: "Fornece padrões de engenharia de software em Perl moderno (Perl 5.30+). Cobre uso estrito de pragmas (use strict; use warnings; use utf8;), subrotinas com assinaturas (signatures), Orientação a Objetos moderna (Moo/MooX ou Perl 5.38+ builtin class), expressões regulares defensivas, manipulação segura de arquivos com lexically scoped filehandles e boas práticas CPAN."
---

# Habilidade de IA: Engenharia de Perl (Perl Specialist)

Esta skill orienta a inteligência artificial a atuar como especialista na linguagem **Perl** (com foco em **Modern Perl**, versão 5.32+ e 5.38+), promovendo código limpo, seguro, manutenível e idiomático, eliminando vícios legados do código "Perl 4/5 arcaico".

---

## 🧭 Diretrizes de Desenvolvimento em Perl

Ao atuar nesta skill, aplique rigorosamente os seguintes padrões:

### 1. Pragmas Obrigatórios e Recursos Modernos
- **Estrito e Seguro**: TODO script ou módulo deve iniciar ativando a checagem estrita de compilação e alertas:
  ```perl
  use strict;
  use warnings;
  use utf8;
  ```
- **Ativação de Recursos Modernos (`use v5.36;`)**: Em versões modernas do Perl, prefira usar `use v5.36;` ou `use v5.38;`, que já ativam automaticamente `strict`, `warnings` e recursos como `signatures` (assinaturas de função) e `state`.

### 2. Assinaturas de Subrotinas (Subroutine Signatures)
- **Evitar `@_` Manual**: Substitua a descompactação tradicional `my ($self, $foo) = @_` por assinaturas de subrotinas nativas:
  ```perl
  use v5.36;

  sub calculate_total ($price, $tax_rate = 0.05, $discount = 0) {
      return ($price * (1 + $tax_rate)) - $discount;
  }
  ```

### 3. E/S de Arquivos e Manipulação Defensiva de Dados
- **Filehandles Lexicais e `open` com 3 Argumentos**: Sempre use a forma de três argumentos para a função `open` combinada com variáveis de escopo `my`:
  ```perl
  open(my $fh, '<:encoding(UTF-8)', $filename)
      or die "Não foi possível abrir '$filename': $!";
  ```
- **Uso de `autodie` ou Handling de Erros**: Utilize `use autodie;` em scripts de automação para evitar checagens repetitivas de `or die` em operações de arquivo e sistema.

### 4. Orientação a Objetos Moderna (Moo / Perl 5.38 Class)
- **Moo / Moose**: Para projetos estabelecidos, utilize `Moo` (ou `Moose`) para POO baseada em atributos declarativos, construtores automáticos e papéis (*roles*):
  ```perl
  package App::Model::User;
  use Moo;
  use namespace::autoclean;

  has id       => (is => 'ro', required => 1);
  has username => (is => 'rw', required => 1);
  has email    => (is => 'rw');

  sub is_active ($self) {
      return defined $self->email && length($self->email) > 0;
  }

  1;
  ```
- **Recurso Nativo `class` (Perl 5.38+)**: Quando em ambientes Perl 5.38+, utilize a nova sintaxe nativa `feature 'class'`.

### 5. Expressões Regulares Legíveis e Defensivas
- **Modificador `/x` (Extended Regex)**: Escreva regexes complexas em múltiplas linhas comentadas usando o modificador `/x`:
  ```perl
  if ($input =~ /
      ^                     # Início da linha
      (?<area_code> \d{3} ) # Código de área (3 dígitos)
      -
      (?<number>    \d{7} ) # Número principal (7 dígitos)
      $                     # Fim da linha
  /x) {
      my $area = $+{area_code};
  }
  ```

---

## 🧰 Padrões de Código Recomendados

### Script CLI Moderno de Processamento de Arquivos em Batch

```perl
#!/usr/bin/env perl
use v5.36;
use autodie;
use Path::Tiny;
use Getopt::Long qw(GetOptions);

# Declaração de Opções
my $input_dir  = '.';
my $output_file = 'report.csv';
my $verbose     = 0;

GetOptions(
    'dir|d=s'    => \$input_dir,
    'output|o=s' => \$output_file,
    'verbose|v'  => \$verbose,
) or die("Erro nos argumentos passados da linha de comando.\n");

sub process_log_file ($file_path) {
    say "Processando: $file_path" if $verbose;
    
    my $file = path($file_path);
    my @lines = $file->lines_utf8({ chomp => 1 });
    
    my $matched_count = 0;
    for my $line (@lines) {
        if ($line =~ /ERROR|CRITICAL/i) {
            $matched_count++;
        }
    }
    
    return {
        filename => $file->basename,
        errors   => $matched_count,
        size     => $file->stat->size,
    };
}

sub main () {
    my $dir = path($input_dir);
    die "Diretório inexistente: $input_dir\n" unless $dir->is_dir;

    my @results;
    my $iterator = $dir->iterator({ recurse => 0 });

    while (my $path = $iterator->()) {
        next unless $path->is_file && $path->basename =~ /\.log$/;
        push @results, process_log_file($path);
    }

    # Gravando relatório CSV de saída
    my $out_fh = path($output_file)->openw_utf8;
    $out_fh->say("Filename,ErrorCount,SizeBytes");

    for my $res (@results) {
        $out_fh->say(sprintf("%s,%d,%d", $res->{filename}, $res->{errors}, $res->{size}));
    }

    say "Relatório gerado com sucesso em: $output_file";
}

main();
```

### Classe Orientada a Objetos com `Moo` e Validação de Atributos

```perl
package Services::PaymentProcessor;
use Moo;
use Types::Standard qw(Str Num BoolObject InstanceOf);
use namespace::autoclean;
use v5.36;

# Atributos declarativos tipados
has api_key => (
    is       => 'ro',
    isa      => Str,
    required => 1,
);

has sandbox_mode => (
    is      => 'ro',
    isa     => BoolObject,
    default => sub { 1 },
);

has timeout => (
    is      => 'rw',
    isa     => Num,
    default => 30.0,
);

# Método público usando assinaturas
sub process_transaction ($self, $amount, $currency = 'USD') {
    die "Valor da transação deve ser maior que zero" if $amount <= 0;

    my $endpoint = $self->sandbox_mode
        ? 'https://sandbox.api.payment.com/v1/charge'
        : 'https://api.payment.com/v1/charge';

    say sprintf("Enviando cobrança de %.2f %s para %s (Timeout: %.1fs)...",
        $amount, $currency, $endpoint, $self->timeout);

    # Simulação de resposta da API
    return {
        success        => 1,
        transaction_id => 'TXN-' . int(rand(1_000_000)),
        amount         => $amount,
        currency       => $currency,
    };
}

1;
```

## 🔒 Questões de Segurança e Práticas Seguras

- **Injeção em `open()`**: Nunca use a sintaxe de dois argumentos da função `open` (ex: `open(FH, "$file")`). Prefira sempre a sintaxe de três argumentos `open(my $fh, '<', $file)` para evitar execução acidental de comandos.
- **Bypass de Taint Mode**: Sempre ative o Taint Mode (`-T`) em scripts Perl expostos à internet ou CGI para marcar entradas externas como inseguras até que sejam limpas via expressões regulares.
- **Regular Expression Denial of Service (ReDoS)**: Evite padrões de regex aninhados com quantificadores complexos que possam causar backtracking exponencial catastrófico.

