---
name: manim-video-creator
description: Manim（Mathematical Animation Engine）を使用してアニメーション動画を作成します。このスキルは、(1) 解説動画やビジュアライゼーションの作成、(2) プレゼンテーション動画、(3) ロゴアニメーション、(4) インフォグラフィック、(5) 教育コンテンツ、(6) 3Dアニメーション、(7) アルゴリズムやデータ構造の可視化に使用します。2D/3Dシーン、LaTeX数式、グラフ、TTSナレーション、BGMなどをサポートします。
---

# Manim 動画クリエイター

Manim Community ライブラリを使用して、TTSナレーション・BGM付きのアニメーション動画を作成します。

---

## 動画作成前の必須ヒアリング

**重要**: 動画作成を開始する前に、必ず `AskUserQuestion` ツールを使用して以下の情報をヒアリングしてください。

### ヒアリング項目

```
AskUserQuestionで以下を確認：

1. 動画の種類
   - 解説・教育動画（論文解説、チュートリアル等）
   - プレゼンテーション動画
   - ロゴアニメーション
   - インフォグラフィック・データ可視化
   - アルゴリズム・コード可視化
   - その他

2. 作成範囲
   - Manim動画のみ（音声なし）
   - Manim動画 + 台本
   - フル版（Manim + TTSナレーション + BGM）

3. ナレーション音声（フル版の場合）
   - 日本語女性（ja-JP-NanamiNeural）- 推奨
   - 日本語男性（ja-JP-KeitaNeural）
   - 英語女性（en-US-JennyNeural）
   - 英語男性（en-US-GuyNeural）

4. BGMの種類（フル版の場合）
   - 自動生成（アンビエント）- 著作権フリー
   - BGMなし
   - 外部BGMを後から追加

5. プラットフォーム/アスペクト比
   - YouTube（16:9, 1920x1080）- 推奨
   - YouTube Shorts/TikTok（9:16, 1080x1920）
   - Instagram投稿（1:1, 1080x1080）
   - カスタム
```

---

## ワークフロー概要

### ステージ1: Manim動画作成
1. ナレーション台本を先に作成し、各セグメントの長さを測定
2. タイミングを計算してManimシーンを設計
3. シーンスクリプトを作成（各セクションの開始・終了時間をコメントで明示）
4. 低品質でプレビューレンダリング → タイミング確認
5. 高品質で最終レンダリング

### ステージ2: 音声生成
1. edge-ttsでナレーション音声を生成
2. 各セグメントを正確なタイムスタンプで配置

### ステージ3: 音声・動画合成
1. BGMを生成または準備
2. ナレーションとBGMを合成（BGM音量: -18dB推奨）
3. ffmpegで動画と音声を合成

---

## 重要: タイミング同期のベストプラクティス

### ナレーション先行設計

動画とナレーションのずれを防ぐため、**ナレーション台本を先に作成**し、その長さに基づいて動画のタイミングを設計します。

```python
# ステップ1: ナレーション台本を作成し、各セグメントの長さを測定
NARRATIONS = [
    "最初のナレーション。",  # 測定結果: 3.5秒
    "2番目のナレーション。",  # 測定結果: 4.2秒
]

# ステップ2: タイミング構成を設計
"""
タイミング構成:
- セクション1: 0.0 - 4.0秒（ナレーション1 + 余白）
- セクション2: 4.0 - 9.0秒（ナレーション2 + 余白）
"""

# ステップ3: シーンに反映
class MyScene(Scene):
    """
    タイミング構成（ナレーション同期版）:
    - セクション1: 0.0 - 4.0秒
    - セクション2: 4.0 - 9.0秒
    """
    def construct(self):
        self.section1()  # 4秒
        self.section2()  # 5秒

    def section1(self):
        """セクション1: 0.0 - 4.0秒
        ナレーション (0.5秒開始, 3.5秒): 最初のナレーション。
        """
        # 0.0-1.5秒: タイトル表示
        self.play(Write(title), run_time=1.5)
        # 1.5-4.0秒: 待機（ナレーション終了を待つ）
        self.wait(2.5)
        # 累計: 4.0秒
```

### アニメーション時間の計算式

```python
# 基本式
待機時間 = ナレーション終了時間 - 現在の累計アニメーション時間

# 例: ナレーションが8.5秒で終了、現在のアニメーションが6秒まで進んでいる場合
self.wait(8.5 - 6.0)  # = 2.5秒待機
```

### シーンのドキュメント形式

各セクションに以下の情報をコメントで明示してください：

```python
def show_section(self):
    """セクション名: 開始時間 - 終了時間（所要時間）
    ナレーション1 (開始秒, 長さ): テキスト...
    ナレーション2 (開始秒, 長さ): テキスト...
    """
    # タイムスタンプコメント
    # 0.0-1.0秒: アニメーション説明
    self.play(...)
    # 1.0-3.0秒: 待機
    self.wait(2)
    # 累計: 3.0秒
```

---

## クイックスタート

### プロジェクトセットアップ
```bash
# uvでプロジェクトを作成
uv init --python 3.12 my-animation
cd my-animation
uv add manim

# 音声処理用（フル版）
uv add edge-tts pydub

# システム依存パッケージのインストール
# macOS
brew install pkg-config cairo pango ffmpeg
brew install --cask mactex  # LaTeXサポート用

# Linux (Ubuntu/Debian)
# sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg texlive-full

# Windows
# 1. MiKTeX をインストール: https://miktex.org/download
# 2. FFmpeg をインストール: https://ffmpeg.org/download.html
# 3. パスを環境変数に追加

# インストール確認
uv run manim checkhealth
```

### 基本的なシーン構造
```python
from manim import *

# 日本語フォント設定
config.font = "Hiragino Sans"  # macOS
# config.font = "Noto Sans CJK JP"  # Linux
# config.font = "Yu Gothic"  # Windows

# ダークモード背景（推奨）
config.background_color = "#1a1a2e"

# カラーパレット
PRIMARY = "#4fc3f7"
SECONDARY = "#81c784"
ACCENT = "#ffb74d"
HIGHLIGHT = "#f06292"

class MyScene(Scene):
    def construct(self):
        title = Text("タイトル", font_size=48, color=PRIMARY)
        self.play(Write(title))
        self.wait(2)
```

### レンダリングコマンド
```bash
# 低品質プレビュー（高速）- 開発・タイミング確認用
uv run manim -ql scene.py MyScene --disable_caching

# 高品質 - 最終出力用
uv run manim -qh scene.py MyScene --disable_caching

# 4K品質
uv run manim -qk scene.py MyScene
```

---

## 動画ジャンル別シーン構成

### 1. 解説・教育動画（論文解説など）

```python
class ExplainerScene(Scene):
    """
    タイミング構成:
    - タイトル: 0-8秒
    - セクション1: 8-25秒
    - セクション2: 25-45秒
    - まとめ: 45-55秒
    - エンディング: 55-65秒
    """
    def construct(self):
        self.show_title()
        self.show_section1()
        self.show_section2()
        self.show_summary()
        self.show_ending()

    def show_title(self):
        """タイトル: 0-8秒
        ナレーション (0.5秒, 7秒): タイトルの説明...
        """
        title = Text("タイトル", font_size=72, color=PRIMARY, weight=BOLD)
        subtitle = Text("サブタイトル", font_size=32, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)

        # 0.0-1.5秒: タイトル
        self.play(Write(title), run_time=1.5)
        # 1.5-2.5秒: サブタイトル
        self.play(FadeIn(subtitle), run_time=1)
        # 2.5-7.0秒: 待機
        self.wait(4.5)
        # 7.0-8.0秒: トランジション
        self.play(FadeOut(title), FadeOut(subtitle), run_time=1)

    def show_section1(self):
        """セクション1: 8-25秒"""
        section_title = Text("セクション1", font_size=42, color=ACCENT)
        section_title.to_edge(UP, buff=0.5)
        self.play(Write(section_title), run_time=1)
        # ... セクションの内容
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    def show_summary(self):
        """まとめセクション"""
        title = Text("まとめ", font_size=42, color=ACCENT)
        title.to_edge(UP, buff=0.5)

        points = VGroup(
            Text("• ポイント1", font_size=26),
            Text("• ポイント2", font_size=26),
            Text("• ポイント3", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        points.next_to(title, DOWN, buff=0.8)
        points.shift(LEFT * 2)

        self.play(Write(title))
        for point in points:
            self.play(FadeIn(point, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(1.5)

    def show_ending(self):
        """エンディング"""
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        thanks = Text("ご視聴ありがとうございました", font_size=32, color=GRAY)
        self.play(Write(thanks))
        self.wait(3)
```

### 2. プレゼンテーション動画

```python
class PresentationScene(Scene):
    """スライド形式のプレゼン動画"""
    def construct(self):
        self.slide_title("プレゼンタイトル", "発表者名")
        self.slide_bullets("概要", ["ポイント1", "ポイント2", "ポイント3"])
        self.slide_diagram()

    def slide_title(self, title, author):
        t = Text(title, font_size=56, color=PRIMARY)
        a = Text(author, font_size=28, color=GRAY)
        a.next_to(t, DOWN, buff=0.5)
        self.play(Write(t), FadeIn(a))
        self.wait(2)
        self.play(FadeOut(t), FadeOut(a))

    def slide_bullets(self, title, bullets):
        t = Text(title, font_size=42, color=ACCENT).to_edge(UP)
        items = VGroup(*[
            Text(f"• {b}", font_size=28) for b in bullets
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.next_to(t, DOWN, buff=0.8).shift(LEFT * 2)

        self.play(Write(t))
        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.5))
            self.wait(1)
        self.wait(1)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
```

### 3. ロゴアニメーション

```python
class LogoAnimation(Scene):
    def construct(self):
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.8)
        text = Text("LOGO", font_size=48, color=WHITE)

        self.play(GrowFromCenter(circle), run_time=1)
        self.play(Write(text), run_time=0.8)
        self.play(
            circle.animate.scale(1.1),
            text.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=0.5
        )
        self.wait(1)
```

### 4. フローチャート・サイクル図

```python
class CycleFlowScene(Scene):
    """サイクル図（Thought→Action→Observation等）"""
    def construct(self):
        # ボックス作成
        box1 = RoundedRectangle(width=3, height=1.2, corner_radius=0.15,
                                fill_color=PRIMARY, fill_opacity=0.3,
                                stroke_color=PRIMARY, stroke_width=2)
        box1.shift(UP * 1.5)
        label1 = Text("ステップ1", font_size=22, color=PRIMARY)
        label1.move_to(box1.get_center())

        box2 = RoundedRectangle(width=3, height=1.2, corner_radius=0.15,
                                fill_color=SECONDARY, fill_opacity=0.3,
                                stroke_color=SECONDARY, stroke_width=2)
        box2.shift(RIGHT * 3 + DOWN * 0.8)
        label2 = Text("ステップ2", font_size=22, color=SECONDARY)
        label2.move_to(box2.get_center())

        box3 = RoundedRectangle(width=3, height=1.2, corner_radius=0.15,
                                fill_color=ACCENT, fill_opacity=0.3,
                                stroke_color=ACCENT, stroke_width=2)
        box3.shift(LEFT * 3 + DOWN * 0.8)
        label3 = Text("ステップ3", font_size=22, color=ACCENT)
        label3.move_to(box3.get_center())

        # 矢印
        arrow1 = Arrow(box1.get_right() + DOWN * 0.2, box2.get_top(), color=WHITE, buff=0.1)
        arrow2 = Arrow(box2.get_left(), box3.get_right(), color=WHITE, buff=0.1)
        arrow3 = Arrow(box3.get_top() + RIGHT * 0.3, box1.get_left() + DOWN * 0.2, color=WHITE, buff=0.1)

        # 順番にアニメーション
        self.play(Create(box1), Write(label1), run_time=1)
        self.play(Create(arrow1), run_time=0.5)
        self.play(Create(box2), Write(label2), run_time=1)
        self.play(Create(arrow2), run_time=0.5)
        self.play(Create(box3), Write(label3), run_time=1)
        self.play(Create(arrow3), run_time=0.5)
        self.wait(2)
```

---

## TTSナレーション

### 利用可能な音声

| 言語 | 音声ID | 性別 | 特徴 |
|------|--------|------|------|
| 日本語 | ja-JP-NanamiNeural | 女性 | 明瞭で聞きやすい（推奨）|
| 日本語 | ja-JP-KeitaNeural | 男性 | 落ち着いた声 |
| 英語 | en-US-JennyNeural | 女性 | ナチュラル |
| 英語 | en-US-GuyNeural | 男性 | プロフェッショナル |
| 英語 | en-US-AriaNeural | 女性 | エネルギッシュ |
| 中国語 | zh-CN-XiaoxiaoNeural | 女性 | 標準的 |
| 韓国語 | ko-KR-SunHiNeural | 女性 | 標準的 |

### ナレーション長さの測定

```python
# measure_audio.py
import asyncio
import edge_tts
from pydub import AudioSegment
import os

VOICE = "ja-JP-NanamiNeural"  # または選択された音声

NARRATIONS = [
    "最初のナレーション。",
    "2番目のナレーション。",
]

async def measure_duration(text: str, index: int) -> float:
    temp_path = f"temp_{index}.mp3"
    communicate = edge_tts.Communicate(text, VOICE, rate="+0%")
    await communicate.save(temp_path)

    audio = AudioSegment.from_mp3(temp_path)
    duration = len(audio) / 1000.0

    os.remove(temp_path)
    return duration

async def main():
    print("ナレーション音声長さ測定:")
    print("=" * 50)
    total = 0
    for i, text in enumerate(NARRATIONS):
        duration = await measure_duration(text, i)
        total += duration
        print(f"{i+1}. [{duration:.2f}秒] {text[:30]}...")
    print("=" * 50)
    print(f"合計: {total:.2f}秒")

asyncio.run(main())
```

### タイムスタンプ付き音声生成

```python
# generate_audio.py
import asyncio
import edge_tts
from pydub import AudioSegment
import os

VOICE = "ja-JP-NanamiNeural"

# (開始秒, テキスト)
NARRATIONS = [
    (0.5, "最初のナレーション。"),
    (8.5, "2番目のナレーション。"),
    (16.0, "3番目のナレーション。"),
]

async def generate_audio_segment(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate="+0%")
    await communicate.save(output_path)

async def main():
    audio_dir = "audio_segments"
    os.makedirs(audio_dir, exist_ok=True)

    # 動画の総時間を指定
    video_duration_ms = 120 * 1000
    final_audio = AudioSegment.silent(duration=video_duration_ms)

    print("ナレーション生成中...")
    for i, (start_time, text) in enumerate(NARRATIONS):
        segment_path = f"{audio_dir}/segment_{i:02d}.mp3"
        print(f"  {i+1}/{len(NARRATIONS)}: [{start_time:.1f}秒] {text[:30]}...")
        await generate_audio_segment(text, segment_path)

        segment = AudioSegment.from_mp3(segment_path)
        start_ms = int(start_time * 1000)
        final_audio = final_audio.overlay(segment, position=start_ms)

    final_audio.export("narration.mp3", format="mp3")
    print("完成: narration.mp3")

    # クリーンアップ
    for i in range(len(NARRATIONS)):
        os.remove(f"{audio_dir}/segment_{i:02d}.mp3")
    os.rmdir(audio_dir)

asyncio.run(main())
```

---

## BGM生成・追加

### 自動生成BGM（著作権フリー）

外部ダウンロード不要で、pydubのみでアンビエントBGMを生成できます。

```python
# generate_bgm.py
import math
import struct
import wave
import os
from pydub import AudioSegment

def generate_ambient_chord(frequencies, duration_ms, sample_rate=44100, amplitude=0.15):
    """複数の周波数を合成してアンビエントなコードを生成"""
    n_samples = int(sample_rate * duration_ms / 1000)
    samples = []

    for i in range(n_samples):
        t = i / sample_rate
        value = 0
        for freq in frequencies:
            phase_mod = 0.002 * math.sin(2 * math.pi * 0.1 * t)
            value += amplitude * math.sin(2 * math.pi * freq * t * (1 + phase_mod))
        samples.append(value / len(frequencies))

    return samples

def apply_envelope(samples, attack_ms, decay_ms, sustain_level, release_ms, sample_rate=44100):
    """ADSRエンベロープを適用"""
    n_samples = len(samples)
    attack_samples = int(sample_rate * attack_ms / 1000)
    decay_samples = int(sample_rate * decay_ms / 1000)
    release_samples = int(sample_rate * release_ms / 1000)

    result = []
    for i, sample in enumerate(samples):
        if i < attack_samples:
            envelope = i / attack_samples
        elif i < attack_samples + decay_samples:
            decay_progress = (i - attack_samples) / decay_samples
            envelope = 1.0 - (1.0 - sustain_level) * decay_progress
        elif i > n_samples - release_samples:
            release_progress = (i - (n_samples - release_samples)) / release_samples
            envelope = sustain_level * (1.0 - release_progress)
        else:
            envelope = sustain_level
        result.append(sample * envelope)

    return result

def samples_to_wav(samples, filename, sample_rate=44100):
    """サンプルをWAVファイルに書き出し"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for sample in samples:
            sample = max(-1.0, min(1.0, sample))
            packed = struct.pack('h', int(sample * 32767))
            wav_file.writeframes(packed)

def generate_ambient_bgm(duration_seconds=130, output_path="bgm.mp3"):
    """アンビエントBGMを生成"""
    print("アンビエントBGMを生成中...")

    sample_rate = 44100
    duration_ms = duration_seconds * 1000

    # Cメジャー系コード進行
    chord_progressions = [
        [130.81, 164.81, 196.00],  # C E G
        [146.83, 174.61, 220.00],  # D F A
        [164.81, 196.00, 246.94],  # E G B
        [130.81, 164.81, 196.00],  # C E G
    ]

    chord_duration_ms = 8000
    all_samples = []

    for i in range(int(duration_ms / chord_duration_ms) + 1):
        chord = chord_progressions[i % len(chord_progressions)]
        samples = generate_ambient_chord(chord, chord_duration_ms, sample_rate, amplitude=0.12)
        samples = apply_envelope(samples, 2000, 1000, 0.7, 2000, sample_rate)
        all_samples.extend(samples)

    all_samples = all_samples[:int(sample_rate * duration_seconds)]

    # ベースドローン追加
    print("  ベースドローンを追加中...")
    drone_freq = 65.41  # C2
    for i in range(len(all_samples)):
        t = i / sample_rate
        drone = 0.08 * math.sin(2 * math.pi * drone_freq * t)
        drone += 0.04 * math.sin(2 * math.pi * drone_freq * 1.5 * t)
        all_samples[i] += drone

    # フェードイン・フェードアウト
    print("  フェード処理中...")
    fade_in_samples = int(sample_rate * 3)
    fade_out_samples = int(sample_rate * 5)

    for i in range(fade_in_samples):
        all_samples[i] *= i / fade_in_samples

    for i in range(fade_out_samples):
        idx = len(all_samples) - fade_out_samples + i
        all_samples[idx] *= (fade_out_samples - i) / fade_out_samples

    # WAVに書き出し
    temp_wav = "temp_bgm.wav"
    samples_to_wav(all_samples, temp_wav, sample_rate)

    # MP3に変換
    audio = AudioSegment.from_wav(temp_wav)
    audio.export(output_path, format="mp3", bitrate="128k")

    os.remove(temp_wav)
    print(f"BGM生成完了: {output_path}")

if __name__ == "__main__":
    generate_ambient_bgm(130, "bgm.mp3")
```

### ナレーションとBGMの合成

```python
# combine_final.py
from pydub import AudioSegment
import subprocess
import os

def combine_audio_and_video():
    """ナレーションとBGMを合成し、動画と結合"""
    print("音声を処理中...")

    narration = AudioSegment.from_mp3("narration.mp3")
    bgm = AudioSegment.from_mp3("bgm.mp3")

    # BGMをナレーションの長さに合わせる
    if len(bgm) < len(narration):
        while len(bgm) < len(narration):
            bgm = bgm + bgm
    bgm = bgm[:len(narration)]

    # BGM音量調整（-18dB推奨）
    bgm = bgm - 18

    # フェードイン・フェードアウト
    bgm = bgm.fade_in(3000).fade_out(4000)

    # 合成
    combined = narration.overlay(bgm)
    combined.export("combined_audio.mp3", format="mp3", bitrate="192k")

    # 動画と合成
    subprocess.run([
        "ffmpeg", "-i", "media/videos/scene/1080p60/MyScene.mp4",
        "-i", "combined_audio.mp3",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest", "-y", "final_output.mp4"
    ])

    os.remove("combined_audio.mp3")
    print("完成: final_output.mp4")

if __name__ == "__main__":
    combine_audio_and_video()
```

---

## エンディング動画の結合

### ディレクトリ構成と検索優先順位

> **重要**: エンディング動画は自動検索されます。ユーザーにパスを聞く必要はありません。

エンディング動画は**以下の優先順位**で自動検索されます：

| 優先度 | 場所 | パス |
|--------|------|------|
| 1 | プロジェクトディレクトリ | `./endings/{aspect_dir}/ending.mp4` |
| 2 | プラグインディレクトリ | `${CLAUDE_PLUGIN_ROOT}/endings/{aspect_dir}/ending.mp4` |

※ `{aspect_dir}` は動画のアスペクト比に応じて `16_9`、`9_16`、`1_1` のいずれか

#### 1. プロジェクトディレクトリ（優先）

プロジェクト固有のエンディング動画がある場合：

```
./                          # 現在のmanimプロジェクトディレクトリ
└── endings/
    ├── 16_9/
    │   └── ending.mp4
    ├── 9_16/
    │   └── ending.mp4
    └── 1_1/
        └── ending.mp4
```

#### 2. プラグインディレクトリ（フォールバック）

プロジェクトにエンディング動画がない場合、共通のエンディング動画を使用：

```
${CLAUDE_PLUGIN_ROOT}/
└── endings/
    ├── 16_9/    # YouTube用（1920x1080）
    │   └── ending.mp4
    ├── 9_16/    # Shorts/TikTok用（1080x1920）
    │   └── ending.mp4
    └── 1_1/     # Instagram用（1080x1080）
        └── ending.mp4
```

### CLAUDE_PLUGIN_ROOT 環境変数

`CLAUDE_PLUGIN_ROOT` はClaude Codeによって自動的に設定される環境変数で、プラグインのルートディレクトリを指します。

```bash
# 環境変数の確認
echo $CLAUDE_PLUGIN_ROOT

# 例: ~/.claude/plugins/marketplaces/manim-video-creator/plugins/manim-video-creator
```

**注意:**
- プロジェクト固有のエンディングがある場合は `./endings/` に配置
- 共通のエンディングは `${CLAUDE_PLUGIN_ROOT}/endings/` に配置
- どちらにもエンディングがない場合は、エンディングなしで動画を出力

### エンディング動画結合スクリプト

```python
# concat_ending.py
import subprocess
import os
import sys

def get_video_dimensions(video_path):
    """動画の幅と高さを取得"""
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        video_path
    ], capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split(','))
    return width, height

def get_aspect_ratio_dir(width, height):
    """アスペクト比に基づいてディレクトリ名を返す"""
    if width > height:
        return "16_9"
    elif width < height:
        return "9_16"
    else:
        return "1_1"

def find_ending_video(aspect_dir, plugin_root=None):
    """エンディング動画を検索（プロジェクト優先、プラグインフォールバック）

    Args:
        aspect_dir: アスペクト比ディレクトリ名（16_9, 9_16, 1_1）
        plugin_root: プラグインのルートディレクトリ

    Returns:
        エンディング動画のパス、見つからない場合はNone
    """
    # 1. プロジェクトディレクトリを優先
    project_ending = os.path.join(".", "endings", aspect_dir, "ending.mp4")
    if os.path.exists(project_ending):
        print(f"プロジェクトのエンディング動画を使用: {project_ending}")
        return project_ending

    # 2. プラグインディレクトリをフォールバック
    if plugin_root is None:
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", ".")

    plugin_ending = os.path.join(plugin_root, "endings", aspect_dir, "ending.mp4")
    if os.path.exists(plugin_ending):
        print(f"プラグインのエンディング動画を使用: {plugin_ending}")
        return plugin_ending

    # どちらにも見つからない
    print(f"警告: エンディング動画が見つかりませんでした")
    print(f"  - プロジェクト: {project_ending}")
    print(f"  - プラグイン: {plugin_ending}")
    return None

def concat_with_ending(main_video, plugin_root=None):
    """メイン動画とエンディング動画を結合

    Args:
        main_video: メイン動画のパス
        plugin_root: プラグインのルートディレクトリ（指定しない場合は環境変数から取得）
    """
    width, height = get_video_dimensions(main_video)
    aspect_dir = get_aspect_ratio_dir(width, height)

    # エンディング動画を検索（プロジェクト優先）
    ending_path = find_ending_video(aspect_dir, plugin_root)

    if ending_path is None:
        print("エンディング動画なしで続行します")
        return main_video

    # 結合リストを作成
    with open("concat_list.txt", "w") as f:
        f.write(f"file '{os.path.abspath(main_video)}'\n")
        f.write(f"file '{os.path.abspath(ending_path)}'\n")

    output_path = main_video.replace(".mp4", "_with_ending.mp4")

    # 動画を結合（同じコーデックの場合は高速）
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "concat_list.txt",
        "-c", "copy", "-y", output_path
    ])

    os.remove("concat_list.txt")
    print(f"完成: {output_path}")
    return output_path

if __name__ == "__main__":
    main_video = sys.argv[1] if len(sys.argv) > 1 else "final_output.mp4"
    concat_with_ending(main_video)
```

### 注意事項

- メイン動画とエンディング動画のコーデック・解像度・フレームレートを一致させる
- 不一致の場合は再エンコードが必要：

```bash
ffmpeg -f concat -safe 0 -i concat_list.txt \
  -c:v libx264 -preset medium -crf 18 \
  -c:a aac -b:a 192k \
  -y final_with_ending.mp4
```

---

## デザインガイドライン

### 推奨カラーパレット

```python
# ダークモード（推奨）
config.background_color = "#1a1a2e"
PRIMARY = "#4fc3f7"      # ライトブルー
SECONDARY = "#81c784"    # グリーン
ACCENT = "#ffb74d"       # オレンジ
HIGHLIGHT = "#f06292"    # ピンク
TEXT_COLOR = WHITE

# ライトモード
config.background_color = WHITE
PRIMARY = "#2563eb"
SECONDARY = "#16a34a"
ACCENT = "#f59e0b"
HIGHLIGHT = "#ec4899"
TEXT_COLOR = "#1f2937"
```

### フォント設定

```python
# 日本語フォント（OS別）
config.font = "Hiragino Sans"     # macOS
# config.font = "Noto Sans CJK JP"  # Linux
# config.font = "Yu Gothic"         # Windows

# 推奨フォントサイズ
# メインタイトル: 48-72
# セクションタイトル: 36-42
# 本文: 22-28
# キャプション: 18-22
```

---

## プラットフォーム別設定

| プラットフォーム | 解像度 | アスペクト比 | 最大長さ |
|------------------|--------|--------------|----------|
| YouTube | 1920x1080 | 16:9 | 制限なし |
| YouTube Shorts | 1080x1920 | 9:16 | 60秒 |
| TikTok | 1080x1920 | 9:16 | 10分 |
| Instagram Reels | 1080x1920 | 9:16 | 90秒 |
| Instagram 投稿 | 1080x1080 | 1:1 | 60秒 |
| Twitter/X | 1920x1080 | 16:9 | 2分20秒 |

---

## 動画作成後の注意事項

### 著作権に関する重要事項

動画作成完了後、以下の注意事項をユーザーに必ず伝えてください：

```
【動画利用に関する重要な注意事項】

1. BGMについて
   - 「自動生成BGM」を使用した場合：
     → このBGMは著作権フリーです。商用・非商用問わず自由に利用できます。

   - 外部BGMを使用する場合：
     → 必ず利用規約を確認してください
     → フリーBGMサイトでも「クレジット表記必須」「商用利用不可」などの
       条件がある場合があります
     → 推奨フリーBGMサイト:
       - DOVA-SYNDROME (https://dova-s.jp/)
       - 甘茶の音楽工房 (https://amachamusic.chagasi.com/)
       - YouTube Audio Library

2. TTSナレーションについて
   - edge-ttsで生成した音声は、Microsoftの利用規約に従います
   - 商用利用の場合は、Azure Speech Servicesの有料プランを検討してください

3. コンテンツについて
   - 論文解説などの場合、引用元を明記してください
   - 他者の著作物を使用する場合は、著作権法に従ってください

4. 推奨クレジット表記例
   「アニメーション: Manim Community
    BGM: [BGMのソース]
    ナレーション: Microsoft Edge TTS」
```

---

## テンプレート

- **シーンテンプレート**: [scene_template.py](templates/scene_template.py)
- **音声測定**: [measure_audio.py](templates/measure_audio.py)
- **音声生成**: [generate_audio.py](templates/generate_audio.py)

## リファレンス

- **アニメーション**: [animations.md](references/animations.md)
- **Mobjects**: [mobjects.md](references/mobjects.md)
- **テキスト & 数式**: [text-and-math.md](references/text-and-math.md)
- **3Dシーン**: [3d-scenes.md](references/3d-scenes.md)
- **グラフ**: [graphing.md](references/graphing.md)

## トラブルシューティング

### 音声と動画がずれる
1. ナレーション台本を先に作成し、各セグメントの長さを測定
2. 測定結果に基づいて動画のタイミングを設計
3. 各セクションの累計時間をコメントで追跡
4. wait()の時間を調整して同期

### テキストが画面端で切れる
- font_sizeを小さくする（日本語は48以下推奨）
- buff値を調整してマージンを確保
- shift()で位置を調整

### レンダリングが遅い
- 開発中は `-ql` オプション（低品質）を使用
- 最終出力のみ `-qh` を使用
- `--disable_caching` でキャッシュ問題を回避
