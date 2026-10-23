---
name: drawio-diagram
description: 要件定義や設計の図をdraw.io (mxGraph)のXMLとして手書きで生成するときに使う。Factory Consoleがインライン描画できる自己完結したXMLを作る規約を定める。
---

# draw.io (mxGraph) XMLの書き方(drawio-diagram)

## この図の使われ方

生成したXMLファイルは、Consoleが同梱のdiagrams.netのビューアーで、隔離したiframeの中にインライン描画する。URLには載せない。
ビューアーは外部へ通信しないので、AWSなどの外部の図形ライブラリは使えず、図形が描かれない。toolbar、ズーム、レイヤも使えない。
XML自体が、すべての情報を含む自己完結した文書である必要がある。
外部ファイルの参照や、相対パスの画像は使わない。

図にリンクを入れない。`link`属性と、ラベルのHTMLの属性付きの`<a>`、`<area>`、`<map>`、`<meta>`、`<object>`、`<embed>`、`<form>`、`<img>`、`<image>`などは使わない。
HTMLのタグの中の`onclick=`のようなイベントハンドラ属性も使わない。
ラベルに、HTMLのコメント(`<!--`)と、`<!`か`<?`で始まる構文は使えない。
`x </ y`のように、`</`の後ろが英字でない書き方も使えない。
ラベルに次の要素は使えない。属性の有無を問わず拒否する。

- `<textarea>`、`<title>`、`<xmp>`、`<noscript>`、`<noembed>`、`<noframes>`、`<plaintext>`、`<iframe>`、`<style>`、`<script>`
- `<svg>`、`<math>`
- `<set>`、`<animate>`、`<animateMotion>`、`<animateTransform>`

`Map<title>`のように、型の表記がこれらの要素名と同じになるときは、型の名前を変えるか、文章で書く。
タグの外の文章にある`one = 1`や`online=true`は拒否しない。
`usemap=`、`formaction=`、`srcdoc=`も使わない。
`placeholders`属性と、`<mxfile>`の`vars`属性は使わない。
`placeholders`は、どの要素にあっても、値を問わずFactoryが拒否する。
ラベルの`%名前%`が祖先のセルの属性、ページの名前、`vars`の値に置き換わり、置き換えた後のラベルを検査で確かめきれないためである。
`Promise<Object>`のように、属性を持たない要素名だけの表記は使ってよい。
`<A extends B = C>`のように、型引数の名前が`a`や`map`などの要素名と同じで、後ろに`名前=`が続く表記は、属性付きの要素とみなして拒否することがある。そのときは、型引数の名前を変えるか、文章で書く。
図のXMLは信頼できない入力として描くので、リンクや圧縮で検査をすり抜ける図は、Factoryが生成の時点と読み戻しの時点で拒否するためである。

## 最小スケルトン

```xml
<mxfile host="app.diagrams.net">
  <diagram name="DIAGRAM_NAME" id="UNIQUE_ID">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- vertex と edge をここに追加 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- `mxCell id="0"`と`id="1"`(`parent="0"`)はdraw.ioの内部ルートで、必ず両方置く。以降のセルは、すべて`parent="1"`から辿れるようにする。
- `diagram`の`id`(`UNIQUE_ID`)は、ファイル内で一意であればよい。自分で決めた一意な文字列でよい。
- `diagram`の`name`(`DIAGRAM_NAME`)は、ファイル名(`<name>.drawio`)と本文の参照(`![name](name.drawio)`)と同じ値にする。`name`は`[a-z0-9-]{1,64}`の形式にする。

## vertex(ノード)の書き方

```xml
<mxCell id="node1" value="要求を受け取る" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="160" height="60" as="geometry" />
</mxCell>
```

- `value`が表示テキストである。`style`は`;`区切りのキー=値の並びで、`rounded`、`whiteSpace=wrap`、`html=1`が基本のセットである。
- `geometry`の`x` / `y`は左上の座標、`width` / `height`はノードのサイズである。`as="geometry"`は固定である。

## edge(矢印)の書き方

```xml
<mxCell id="edge1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;" edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `source` / `target`は、接続元と接続先の`vertex`の`id`である。ラベルを付けたい場合は、`value`に文言を入れる。
- 状態遷移図で条件ラベルを付ける場合も、同じく`value`を使う(例: `value="approve"`)。
- `parent`は必ず`"1"`にし、ルートセルを親にする。
- `mxGeometry`には`as="geometry"`を必ず付ける。`relative="1"`はedgeに特有の指定である。

## レイアウト規則

- グリッドの単位は120pxを基準にする。これがノード間の水平・垂直の間隔の目安である。
- 原則として、上から下への一方向のレイアウトにする。フローチャートなら左から右でもよい。矢印が交差する配置は避ける。
- 1つの図に詰め込むノードは15個までを目安にする。それを超える複雑さになりそうなら、図を分割して「1図1概念」にする(例: 全体構成図と、承認フローだけの図を分ける)。

図の種類ごとの目安は次のとおり。

| 種類 | 書き方 |
| --- | --- |
| コンテキスト図 | システムと外部アクター(GitHub、Discord、人)の関係を描く。ノードは少なくし、矢印にはやりとりの内容をラベルで書く。 |
| フロー図(擬似シーケンス) | 処理ステップを上から下に並べ、矢印で順序を表す。分岐は、菱形か条件ラベル付きの矢印で表す。 |
| 状態遷移図 | 状態をノード、遷移をラベル付きのedgeで表す。終端状態は、色や二重線のstyleで視覚的に区別する。 |
| データモデル図 | テーブルやエンティティをノードにし、関連をedgeで結ぶ。カラムの一覧は、`value`内に改行(`&lt;br&gt;`)区切りで列挙してよい。 |

## 非圧縮XMLであること

- `<mxfile>`に`compressed="true"`を付けない。属性ごと省略してもよい。
- deflateとbase64で圧縮したペイロードではなく、人が読めるプレーンなXMLをそのまま出力する。
- `<diagram>`の中に、空白以外のテキストやCDATAを入れない。要素と属性だけで書く。
- このスキルの責務は、妥当な非圧縮のXMLを作るところまでである。XMLの検証はFactory側(`f/factory/lib/drawio.ts`)が行い、表示はConsoleが行う。

## エスケープ規則

`value`属性やテキストの中では、次の文字をXMLエンティティに置き換える。

| 文字 | 置き換え |
| --- | --- |
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"`(属性値内) | `&quot;` |

`value`の中で改行したい場合は、`&lt;br&gt;`(エスケープ済みの`<br>`)を使う。

## 完全な例(4ノード・3エッジ)

Issue受付から承認までの簡易フロー図を示す。

```xml
<mxfile host="app.diagrams.net">
  <diagram name="issue-intake-flow" id="d1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="n1" value="Issue に factory ラベル" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="n2" value="claim して要件生成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="40" y="160" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="n3" value="承認待ち(要対応)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="40" y="280" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="n4" value="承認済み" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="40" y="400" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="n1" target="n2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="n2" target="n3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" value="approve" edge="1" parent="1" source="n3" target="n4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## セルフチェック

- `<mxfile>`がルート要素で、`compressed`属性が無いか`false`である。
- `placeholders`属性と、`<mxfile>`の`vars`属性が無い。
- すべての`vertex` / `edge`の`parent`が`"1"`を辿れる。孤立したセルが無い。
- すべての`source` / `target`が、実在する`vertex`の`id`を指している。
- `&` `<` `>` `"`がエスケープされている。ファイルの内容やユーザー入力に由来するラベルのテキストは特に注意する。
- すべての`mxCell`の`id`が一意で、ルートセルの`0` / `1`を再利用していない。
- 図名、ファイル名(`<name>.drawio`)、本文の参照(`![name](name.drawio)`)が一致している。`name`は`[a-z0-9-]{1,64}`の形式である。
- 非圧縮の生のXMLが256KB以内である。超える場合は、「1図1概念」の原則に従って図を分割する。
