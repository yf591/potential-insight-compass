# API リファレンス - Potential Insight Compass (PIC)

## 📋 概要

このドキュメントでは、PICシステムの各クラスとメソッドの詳細なAPIリファレンスを記しています。

---

## 🧠 AIAnalyzer クラス (src/ai_analyzer.py)

### 概要
Google Gemini APIを使用してテキスト分析を行うメインクラス。

### コンストラクタ

```python
AIAnalyzer(api_key: Optional[str] = None)
```

**パラメータ**
- `api_key` (Optional[str]): Google Gemini API キー。Noneの場合は環境変数から取得

**例外**
- `ValueError`: API キーが見つからない場合

**使用例**
```python
# 環境変数から API キーを取得
analyzer = AIAnalyzer()

# 直接 API キーを指定
analyzer = AIAnalyzer(api_key="your-api-key-here")
```

### メソッド

#### validate_input

```python
validate_input(text: str) -> Tuple[bool, str]
```

入力テキストの妥当性を検証します。

**パラメータ**
- `text` (str): 検証するテキスト

**戻り値**
- `Tuple[bool, str]`: (有効性フラグ, エラーメッセージ)

**検証ルール**
- 空文字でないこと
- 10文字以上であること
- 10,000文字以下であること

**使用例**
```python
is_valid, error_msg = analyzer.validate_input("分析したいテキスト")
if not is_valid:
    print(f"エラー: {error_msg}")
```

#### analyze_text

```python
analyze_text(text: str, max_retries: int = 3) -> AnalysisResult
```

テキストを分析してAnalysisResultオブジェクトを返します。

**パラメータ**
- `text` (str): 分析対象のテキスト
- `max_retries` (int): 最大リトライ回数（デフォルト: 3）

**戻り値**
- `AnalysisResult`: 分析結果オブジェクト

**例外**
- `ValueError`: 入力検証に失敗した場合
- `Exception`: API呼び出しが最大リトライ回数後も失敗した場合

**使用例**
```python
try:
    result = analyzer.analyze_text("面談記録のテキスト...")
    print(f"強み: {result.strengths}")
    print(f"処理時間: {result.processing_time:.2f}秒")
except ValueError as e:
    print(f"入力エラー: {e}")
except Exception as e:
    print(f"分析エラー: {e}")
```

#### get_capability_dimensions

```python
get_capability_dimensions() -> List[str]
```

システムで使用される6つの能力軸を取得します。

**戻り値**
- `List[str]`: 能力軸のリスト

**使用例**
```python
dimensions = analyzer.get_capability_dimensions()
# ['継続・集中力', '実行・行動力', '共感・協調性', '論理・分析力', '創造・発想力', '計画・堅実性']
```

---

## 📊 DataProcessor クラス (src/data_processor.py)

### 概要
データの前処理、検証、変換、エクスポート機能を提供するクラス。

### コンストラクタ

```python
DataProcessor()
```

パラメータなしで初期化されます。

### メソッド

#### preprocess_text

```python
preprocess_text(text: str) -> str
```

テキストの前処理を行います。

**パラメータ**
- `text` (str): 前処理するテキスト

**戻り値**
- `str`: 前処理されたテキスト

**処理内容**
- 空白文字の正規化
- 過剰な句読点の整理
- 引用符の統一

**使用例**
```python
processor = DataProcessor()
clean_text = processor.preprocess_text("  不規則な　　空白があるテキスト！！！  ")
```

#### validate_analysis_data

```python
validate_analysis_data(data: Dict) -> Tuple[bool, List[str]]
```

分析データの構造と内容を検証します。

**パラメータ**
- `data` (Dict): 検証するデータ辞書

**戻り値**
- `Tuple[bool, List[str]]`: (有効性フラグ, エラーリスト)

**使用例**
```python
is_valid, errors = processor.validate_analysis_data(analysis_data)
if not is_valid:
    for error in errors:
        print(f"検証エラー: {error}")
```

#### create_scores_dataframe

```python
create_scores_dataframe(scores: Dict[str, int]) -> pd.DataFrame
```

能力スコア辞書からDataFrameを作成します。

**パラメータ**
- `scores` (Dict[str, int]): 能力軸とスコアの辞書

**戻り値**
- `pd.DataFrame`: 可視化用のDataFrame

**DataFrame構造**
```
| 能力次元      | スコア | 最大値 | パーセンテージ |
|--------------|-------|-------|---------------|
| 継続・集中力  | 8     | 10    | 80.0         |
| ...          | ...   | ...   | ...          |
```

**使用例**
```python
scores = {"継続・集中力": 8, "実行・行動力": 7, ...}
df = processor.create_scores_dataframe(scores)
```

#### export_to_json

```python
export_to_json(processed_data: ProcessedData, include_raw_text: bool = False) -> str
```

ProcessedDataをJSON形式で出力します。

**パラメータ**
- `processed_data` (ProcessedData): 出力するデータ
- `include_raw_text` (bool): 元テキストを含めるかどうか

**戻り値**
- `str`: JSON文字列

#### export_to_markdown

```python
export_to_markdown(processed_data: ProcessedData) -> str
```

ProcessedDataをMarkdown形式で出力します。

**パラメータ**
- `processed_data` (ProcessedData): 出力するデータ

**戻り値**
- `str`: Markdown文字列

---

## 📈 ChartVisualizer クラス (src/visualizer.py)

### 概要
Plotlyを使用したインタラクティブチャートの生成を行うクラス。

### コンストラクタ

```python
ChartVisualizer()
```

カラーパレットとフォント設定で初期化されます。

### メソッド

#### create_radar_chart

```python
create_radar_chart(
    scores_df: pd.DataFrame, 
    title: str = "能力スコア レーダーチャート", 
    show_values: bool = True
) -> go.Figure
```

6軸能力スコアのレーダーチャートを作成します。

**パラメータ**
- `scores_df` (pd.DataFrame): スコアDataFrame
- `title` (str): チャートタイトル
- `show_values` (bool): スコア値をチャート上に表示するか

**戻り値**
- `go.Figure`: Plotlyフィギュアオブジェクト

**使用例**
```python
visualizer = ChartVisualizer()
fig = visualizer.create_radar_chart(scores_df, "マイレーダーチャート")
```

#### create_bar_chart

```python
create_bar_chart(
    scores_df: pd.DataFrame, 
    title: str = "能力スコア 棒グラフ", 
    horizontal: bool = False
) -> go.Figure
```

能力スコアの棒グラフを作成します。

**パラメータ**
- `scores_df` (pd.DataFrame): スコアDataFrame
- `title` (str): チャートタイトル
- `horizontal` (bool): 水平棒グラフにするか

**戻り値**
- `go.Figure`: Plotlyフィギュアオブジェクト

**チャート仕様**
- 水平チャート: 400px高、120px左マージン
- 垂直チャート: 500px高、120px下マージン

**使用例**
```python
# 垂直棒グラフ
fig_vertical = visualizer.create_bar_chart(scores_df, "縦型棒グラフ")

# 水平棒グラフ
fig_horizontal = visualizer.create_bar_chart(scores_df, "横型棒グラフ", horizontal=True)
```

#### create_comparison_chart

```python
create_comparison_chart(
    scores_df_list: List[pd.DataFrame], 
    labels: List[str], 
    title: str = "能力スコア 比較"
) -> go.Figure
```

複数のデータセットを比較するレーダーチャートを作成します。

**パラメータ**
- `scores_df_list` (List[pd.DataFrame]): 比較するDataFrameのリスト
- `labels` (List[str]): 各データセットのラベル
- `title` (str): チャートタイトル

**戻り値**
- `go.Figure`: Plotlyフィギュアオブジェクト

**使用例**
```python
df_list = [scores_df1, scores_df2]
labels = ["分析1", "分析2"]
fig = visualizer.create_comparison_chart(df_list, labels, "比較分析")
```

---

## 📋 データクラス

### AnalysisResult (src/ai_analyzer.py)

AI分析結果を格納するデータクラス。

```python
@dataclass
class AnalysisResult:
    strengths: List[str]                    # 5つの強み
    potential_jobs: List[Dict[str, str]]    # 3つの職業適性
    quantitative_scores: Dict[str, int]     # 6軸スコア
    raw_response: str                       # 生レスポンス
    processing_time: float                  # 処理時間（秒）
```

**使用例**
```python
result = analyzer.analyze_text("テキスト")
print(f"強み数: {len(result.strengths)}")
print(f"職業適性数: {len(result.potential_jobs)}")
print(f"処理時間: {result.processing_time:.2f}秒")
```

### ProcessedData (src/data_processor.py)

処理済み分析データを格納するデータクラス。

```python
@dataclass
class ProcessedData:
    timestamp: str                          # 分析実行時刻（ISO形式）
    input_text: str                         # 入力テキスト
    input_length: int                       # 入力文字数
    strengths: List[str]                    # 強み一覧
    potential_jobs: List[Dict[str, str]]    # 職業適性
    scores_df: pd.DataFrame                 # スコアDataFrame
    processing_time: float                  # 処理時間（秒）
    metadata: Dict[str, Any]                # 追加メタデータ
```

**使用例**
```python
processed = processor.process_analysis_result(input_text, analysis_result)
print(f"分析時刻: {processed.timestamp}")
print(f"入力文字数: {processed.input_length}")
```

---

## 🔧 使用例とベストプラクティス

### 基本的な使用フロー

```python
from src.ai_analyzer import AIAnalyzer
from src.data_processor import DataProcessor
from src.visualizer import ChartVisualizer

# 1. 初期化
analyzer = AIAnalyzer()
processor = DataProcessor()
visualizer = ChartVisualizer()

# 2. テキスト分析
input_text = "分析したい面談記録..."
analysis_result = analyzer.analyze_text(input_text)

# 3. データ処理
processed_data = processor.process_analysis_result(input_text, analysis_result)

# 4. 可視化
radar_chart = visualizer.create_radar_chart(processed_data.scores_df)
bar_chart = visualizer.create_bar_chart(processed_data.scores_df)

# 5. エクスポート
json_data = processor.export_to_json(processed_data)
markdown_data = processor.export_to_markdown(processed_data)
```

### エラーハンドリングのベストプラクティス

```python
def safe_analysis_flow(input_text: str):
    try:
        # 入力検証
        analyzer = AIAnalyzer()
        is_valid, error_msg = analyzer.validate_input(input_text)
        if not is_valid:
            return {"error": f"入力エラー: {error_msg}"}
        
        # 分析実行
        result = analyzer.analyze_text(input_text)
        
        # データ処理
        processor = DataProcessor()
        processed_data = processor.process_analysis_result(input_text, result)
        
        return {"success": True, "data": processed_data}
        
    except ValueError as e:
        return {"error": f"検証エラー: {str(e)}"}
    except Exception as e:
        return {"error": f"処理エラー: {str(e)}"}
```

### パフォーマンス最適化

```python
# 1. 結果のキャッシュ
import functools

@functools.lru_cache(maxsize=100)
def cached_analysis(text_hash: str) -> AnalysisResult:
    return analyzer.analyze_text(text)

# 2. バッチ処理
def batch_analysis(texts: List[str]) -> List[AnalysisResult]:
    results = []
    for text in texts:
        try:
            result = analyzer.analyze_text(text)
            results.append(result)
        except Exception as e:
            print(f"分析失敗: {e}")
            continue
    return results
```

---

## 📚 拡張ガイド

### 新しい能力軸の追加

```python
# 1. DataProcessorのcapability_dimensionsを拡張
class ExtendedDataProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.capability_dimensions.extend([
            "リーダーシップ",
            "国際性"
        ])

# 2. システムプロンプトの更新（ai_analyzer.py）
# 3. テストケースの追加
```

### 新しい可視化の追加

```python
class ExtendedChartVisualizer(ChartVisualizer):
    def create_heatmap(self, scores_df: pd.DataFrame) -> go.Figure:
        """能力スコアのヒートマップを作成"""
        # ヒートマップの実装
        pass
    
    def create_timeline_chart(self, history_data: List[ProcessedData]) -> go.Figure:
        """時系列分析チャートを作成"""
        # タイムライン分析の実装
        pass
```

---

このAPIリファレンスを参考に、PICシステムの各機能を効果的に活用してください。