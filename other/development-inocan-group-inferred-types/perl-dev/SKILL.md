---
name: perl-dev
description: |
  Perl開発支援（Mojolicious/DBI/Carton）。
  モダンPerl、perlcritic、Test::Moreでガイド。
allowed-tools: Read, Grep, Glob, Bash
---

# Perl開発固有設定

このファイルはPerl開発に特化した設定を定義します。

## 公式ドキュメントリファレンス

最新の安定版バージョンは以下の公式ドキュメントを参照してください：

| 技術 | 公式ドキュメント | 用途 |
|-----|----------------|------|
| Perl | [Perl Downloads](https://www.perl.org/get.html) | バージョン確認・ダウンロード |
| Perl Releases | [Perl Development](https://dev.perl.org/) | リリース情報 |
| Mojolicious | [Mojolicious (MetaCPAN)](https://metacpan.org/dist/Mojolicious) | 最新版・リリース履歴 |
| Dancer2 | [Dancer2 (MetaCPAN)](https://metacpan.org/dist/Dancer2) | 最新版・リリース履歴 |
| DBIx::Class | [DBIx::Class (MetaCPAN)](https://metacpan.org/dist/DBIx-Class) | 最新版・リリース履歴 |
| Moo | [Moo (MetaCPAN)](https://metacpan.org/dist/Moo) | 最新版・リリース履歴 |
| Carton | [Carton (MetaCPAN)](https://metacpan.org/dist/Carton) | 最新版・リリース履歴 |

## Perl開発固有のルール

### バージョン要件

最新の安定版バージョンは上記の公式ドキュメントリファレンスで確認してください。

- Perl: 最新の安定版を使用（[公式サイト](https://www.perl.org/get.html)で確認）
  - 参考: Perl 5.38以降を推奨（2025年12月時点）
- strictとwarnings必須
- utf8プラグマの使用
- モダンPerlイディオムの活用

### コーディング標準
- use strict; use warnings; use utf8; 必須
- perlcritic準拠
- 意味のある変数名・サブルーチン名
- 適切なエラーハンドリング

### モダンPerl機能
```perl
#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use feature ':5.32';

# シグネチャを使用
use feature 'signatures';
no warnings 'experimental::signatures';

sub calculate($x, $y) {
    return $x + $y;
}

# sayを使用
say "Hello, World!";

# stateで永続的な変数
sub counter {
    state $count = 0;
    return ++$count;
}
```

### 用途別技術スタック

#### Webアプリケーション
- Mojolicious（モダンなWebフレームワーク）
- Dancer2（軽量Webフレームワーク）
- Catalyst（エンタープライズ向け）
- Plack/PSGI（Webサーバーインターフェース）

#### データベース
- DBI + DBD::mysql / DBD::Oracle
- DBIx::Class（ORM）
- Teng（軽量ORM）

### フレームワーク例

#### Mojolicious
```perl
# モダンなWebフレームワーク
package MyApp;
use Mojo::Base 'Mojolicious', -signatures;

sub startup($self) {
    my $r = $self->routes;

    # RESTfulルート
    $r->get('/users')->to('users#index');
    $r->post('/users')->to('users#create');
    $r->get('/users/:id')->to('users#show');
}

# コントローラー
package MyApp::Controller::Users;
use Mojo::Base 'Mojolicious::Controller', -signatures;

sub show($self) {
    my $id = $self->param('id');

    $self->render(json => {
        user => $self->db->get_user($id)
    });
}
```

#### オブジェクト指向 (Moo/Moose)
```perl
package MyClass;
use Moo;
use Types::Standard qw(Str Int);

has name => (
    is       => 'ro',
    isa      => Str,
    required => 1,
);

has age => (
    is      => 'rw',
    isa     => Int,
    default => 0,
);

sub introduce {
    my $self = shift;
    return sprintf("私は%s、%d歳です",
        $self->name, $self->age);
}

1;
```

### データベースアクセス
```perl
# プレースホルダ付きDBI
my $sth = $dbh->prepare(q{
    SELECT * FROM users
    WHERE status = ? AND created_at > ?
});
$sth->execute('active', $date);

# DBIx::Class for ORM
my $users = $schema->resultset('User')->search({
    status => 'active',
    age => { '>' => 18 }
});
```

### セキュリティ実装

グローバルセキュリティポリシーを参照してください。

#### Perl追加セキュリティ設定
- Taintモードの有効化（#!/usr/bin/perl -T）
- 入力サニタイズの実装
- HTML::Entitiesでエスケープ
- 適切なパスワード管理

```perl
#!/usr/bin/env -S perl -T
# 互換性重視の場合:
# #!/usr/bin/perl -T
# taintチェックを有効化

# 危険な文字を除去
$input =~ s/[^\w\s-]//g;

# HTML エスケープ
use HTML::Entities;
my $safe = encode_entities($user_input);
```

### エラーハンドリング
```perl
# Try::Tiny を使用
use Try::Tiny;

try {
    dangerous_operation();
} catch {
    warn "エラーが発生しました: $_";
    # エラー処理
} finally {
    # クリーンアップ
};

# または適切なエラーチェックでeval使用
eval {
    risky_code();
    1;
} or do {
    my $error = $@ || '不明なエラー';
    handle_error($error);
};
```

### テスト要件
- Test::More
- Test::Exception
- カバレッジ95%以上
- prove実行

```perl
use Test::More tests => 5;
use Test::Exception;

# 基本的なテスト
ok($result, '結果は真であるべき');
is($actual, $expected, '値が一致するべき');
like($string, qr/pattern/, '文字列がパターンに一致');

# 例外のテスト
dies_ok { dangerous_func() } 'dieするべき';
throws_ok {
    validate_input($bad_data)
} qr/Invalid input/, '正しいエラーを投げる';
```

### パフォーマンス
- state変数でキャッシング
- 正規表現のプリコンパイル（qr//）
- Devel::NYTProfでプロファイリング
- メモリ管理（循環参照の回避）

```perl
# 循環参照を避ける
use Scalar::Util 'weaken';
weaken($self->{parent});

# 大きなファイルは行単位で処理
while (<$fh>) {
    process_line($_);
}
```

### モジュール開発
```perl
=encoding utf-8

=head1 名前

MyModule - 簡潔な説明

=head1 概要

    use MyModule;
    my $obj = MyModule->new();

=head1 説明

モジュールの詳細な説明。

=head1 メソッド

=head2 new

コンストラクタメソッド。

=cut
```

### よく使うコマンド
```bash
# cpanm（モジュールインストール）
cpanm Mojolicious
cpanm DBI DBD::mysql

# テスト実行
prove -lv t/
prove -I lib t/

# コード品質チェック
perlcritic lib/
perltidy lib/

# プロファイリング
perl -d:NYTProf script.pl
nytprofhtml

# 依存関係管理（Carton）
carton install
carton exec -- perl script.pl
```

### 開発ツール
- cpanm（モジュールインストール）
- Carton（依存関係管理）
- perltidy（コードフォーマット）
- perlcritic（コード品質チェック）
- Devel::Cover（テストカバレッジ）
- Devel::NYTProf（プロファイリング）
