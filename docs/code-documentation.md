# コードドキュメント - Potential Insight Compass (PIC)

## 📖 概要

このドキュメントでは、Potential Insight Compass (PIC) システムの各ファイルの詳細な構造と実装について説明します。

## 📁 ファイル構造

```
potential-insight-compass/
├── app.py                    # メインStreamlitアプリケーション
├── src/                      # ソースコードディレクトリ
│   ├── __init__.py          # パッケージ初期化ファイル
│   ├── ai_analyzer.py       # AI分析エンジン
│   ├── data_processor.py    # データ処理ユーティリティ
│   └── visualizer.py        # チャート可視化機能
└── tests/                   # テストファイル
    ├── __init__.py          # テストパッケージ初期化
    └── test_analyzer.py     # AI分析機能のテスト
```

---

## 🚀 app.py - メインアプリケーション

### 概要
StreamlitベースのWebアプリケーションのメインエントリーポイント。ユーザーインターフェースと全体的なアプリケーションフローを管理します。

### 主要機能

#### 1. セッション状態管理
```python
def initialize_session_state():
    """セッション状態変数を初期化"""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []
```

#### 2. UI コンポーネント
- **ヘッダー表示**: システムタイトルと説明
- **サイドバー**: システム情報と分析履歴
- **入力セクション**: テキストエリアと文字数カウント
- **分析セクション**: 分析実行とプログレス表示
- **結果表示**: 定性・定量分析結果の可視化

#### 3. 分析フロー
```python
def analysis_section(input_text: str, analyzer: AIAnalyzer, processor: DataProcessor):
    """分析処理を実行"""
    # 1. 入力検証
    # 2. AI分析実行（プログレスバー付き）
    # 3. データ処理
    # 4. セッション状態更新
    # 5. 結果表示
```

#### 4. カスタムCSS
- レスポンシブデザイン対応
- カラーテーマの統一
- 情報ボックス、成功ボックス、警告ボックスのスタイリング

### 技術仕様
- **Framework**: Streamlit 1.28.0+
- **Layout**: Wide layout with sidebar
- **State Management**: st.session_state
- **Progress Indication**: st.progress, st.spinner

---

## 🧠 src/ai_analyzer.py - AI分析エンジン

### 概要
Google Gemini APIを使用したAI分析の中核機能。テキスト分析からJSON形式の結果生成まで一貫して処理します。

### クラス構造

#### AIAnalyzer クラス
```python
class AIAnalyzer:
    def __init__(self, api_key: Optional[str] = None)
    def validate_input(self, text: str) -> Tuple[bool, str]
    def analyze_text(self, text: str, max_retries: int = 3) -> AnalysisResult
    def _parse_response(self, response_text: str) -> Dict
    def _validate_response_structure(self, data: Dict) -> None
    def get_capability_dimensions(self) -> List[str]
```

#### AnalysisResult データクラス
```python
@dataclass
class AnalysisResult:
    strengths: List[str]                    # 5つの強み
    potential_jobs: List[Dict[str, str]]    # 3つの職業適性
    quantitative_scores: Dict[str, int]     # 6軸スコア
    raw_response: str                       # 生レスポンス
    processing_time: float                  # 処理時間
```

### 主要機能

#### 1. 入力検証
- 空文字チェック
- 最小文字数検証（10文字以上）
- 最大文字数制限（10,000文字以下）

#### 2. システムプロンプト
SPECIFICATION.mdに基づく詳細なプロンプト設計:
- ネガティブ・ポジティブリフレーミング
- 定性分析（5つの強み、3つの職業適性）
- 定量分析（6軸スコア）
- 厳格なJSON出力フォーマット

#### 3. レスポンス処理
- JSONパース（Markdownラッパー対応）
- 構造検証
- エラーハンドリング
- リトライ機構

### 技術仕様
- **API**: Google Generative AI SDK
- **Model**: gemini-2.5-flash
- **Response Format**: JSON
- **Error Handling**: 最大3回リトライ
- **Timeout**: API応答タイムアウト設定

---

## 📊 src/data_processor.py - データ処理ユーティリティ

### 概要
AI分析結果の前処理、検証、変換、エクスポート機能を提供します。

### クラス構造

#### DataProcessor クラス
```python
class DataProcessor:
    def preprocess_text(self, text: str) -> str
    def validate_analysis_data(self, data: Dict) -> Tuple[bool, List[str]]
    def create_scores_dataframe(self, scores: Dict[str, int]) -> pd.DataFrame
    def process_analysis_result(self, input_text: str, analysis_result: Any, 
                               additional_metadata: Optional[Dict] = None) -> ProcessedData
    def export_to_json(self, processed_data: ProcessedData, 
                      include_raw_text: bool = False) -> str
    def export_to_markdown(self, processed_data: ProcessedData) -> str
    def calculate_statistics(self, scores_df: pd.DataFrame) -> Dict[str, float]
```

#### ProcessedData データクラス
```python
@dataclass
class ProcessedData:
    timestamp: str                          # 分析実行時刻
    input_text: str                         # 入力テキスト
    input_length: int                       # 入力文字数
    strengths: List[str]                    # 強み一覧
    potential_jobs: List[Dict[str, str]]    # 職業適性
    scores_df: pd.DataFrame                 # スコアDataFrame
    processing_time: float                  # 処理時間
    metadata: Dict[str, Any]                # メタデータ
```

### 主要機能

#### 1. テキスト前処理
- 空白文字の正規化
- 過剰な句読点の整理
- 引用符の統一

#### 2. データ検証
- 構造的整合性チェック
- 必須フィールド検証
- データ型検証
- スコア範囲検証（1-10）

#### 3. DataFrame作成
```python
def create_scores_dataframe(self, scores: Dict[str, int]) -> pd.DataFrame:
    # 6軸能力スコアをDataFrameに変換
    # 可視化用の追加カラム生成（最大値、パーセンテージ）
```

#### 4. エクスポート機能
- **JSON形式**: 構造化データの完全出力
- **Markdown形式**: 人間が読みやすい形式
- **統計計算**: 平均、最大、最小、標準偏差

### 技術仕様
- **Data Processing**: Pandas 2.0.0+
- **Export Formats**: JSON, Markdown
- **Character Encoding**: UTF-8
- **Statistics**: NumPy-based calculations

---

## 📈 src/visualizer.py - チャート可視化機能

### 概要
Plotlyを使用したインタラクティブな可視化機能。レーダーチャートと棒グラフによる多角的なデータ表現を提供します。

### クラス構造

#### ChartVisualizer クラス
```python
class ChartVisualizer:
    def __init__(self)
    def create_radar_chart(self, scores_df: pd.DataFrame, 
                          title: str = "能力スコア レーダーチャート", 
                          show_values: bool = True) -> go.Figure
    def create_bar_chart(self, scores_df: pd.DataFrame, 
                        title: str = "能力スコア 棒グラフ", 
                        horizontal: bool = False) -> go.Figure
    def create_comparison_chart(self, scores_df_list: List[pd.DataFrame], 
                               labels: List[str], 
                               title: str = "能力スコア 比較") -> go.Figure
    def create_distribution_chart(self, scores_df: pd.DataFrame) -> go.Figure
    def create_summary_metrics_chart(self, statistics: Dict[str, float]) -> go.Figure
```

### 主要機能

#### 1. レーダーチャート
```python
def create_radar_chart(self, scores_df: pd.DataFrame, 
                      title: str = "能力スコア レーダーチャート", 
                      show_values: bool = True) -> go.Figure:
    # 6軸の能力をレーダーチャートで表示
    # インタラクティブホバー情報
    # カスタムカラーパレット
    # 日本語フォント対応
```

**特徴:**
- 透明度付きの塗りつぶし（RGBA）
- スコア値のテキスト表示
- カスタムホバーテンプレート
- 10点満点スケール

#### 2. 棒グラフ
```python
def create_bar_chart(self, scores_df: pd.DataFrame, 
                    title: str = "能力スコア 棒グラフ", 
                    horizontal: bool = False) -> go.Figure:
    # 水平/垂直棒グラフの選択
    # スコア順ソート
    # カスタムマージン設定
    # レスポンシブ高さ設定
```

**特徴:**
- 水平チャート: 400px高、120px左マージン
- 垂直チャート: 500px高、120px下マージン
- グラデーションカラー
- ラベル回転対応

#### 3. 比較チャート
複数データセットの同時表示機能:
- 複数のレーダーチャート重ね合わせ
- 異なる色での区別
- 透明度調整

### 技術仕様
- **Visualization Library**: Plotly 5.15.0+
- **Chart Types**: Radar, Bar, Comparison
- **Interactivity**: Hover, Zoom, Pan
- **Color Palette**: 6色のカスタムパレット
- **Font Support**: 日本語対応

---

## 🧪 tests/test_analyzer.py - テストスイート

### 概要
AI分析機能とデータ処理機能の包括的なユニットテスト。

### テストクラス構造

#### TestAIAnalyzer クラス
```python
class TestAIAnalyzer(unittest.TestCase):
    def setUp(self)                                    # テスト初期化
    def test_input_validation_empty_text(self)         # 空文字検証
    def test_input_validation_short_text(self)         # 短文字検証
    def test_input_validation_long_text(self)          # 長文字検証
    def test_input_validation_valid_text(self)         # 有効文字検証
    def test_parse_response_valid_json(self)           # JSON解析テスト
    def test_parse_response_with_markdown_wrapper(self) # Markdown対応テスト
    def test_validate_response_structure_valid(self)    # 構造検証テスト
    def test_validate_response_structure_missing_keys(self) # エラー処理テスト
    def test_get_capability_dimensions(self)           # 能力軸取得テスト
```

#### TestDataProcessor クラス
```python
class TestDataProcessor(unittest.TestCase):
    def setUp(self)                                        # テスト初期化
    def test_preprocess_text_whitespace_normalization(self) # 空白正規化テスト
    def test_preprocess_text_punctuation_normalization(self) # 句読点正規化テスト
    def test_create_scores_dataframe(self)                  # DataFrame作成テスト
    def test_validate_analysis_data_valid(self)             # データ検証テスト
    def test_validate_analysis_data_invalid_structure(self) # 無効データテスト
```

### テストデータ
```python
self.sample_response_data = {
    "qualitative_analysis": {
        "strengths": [
            "高い集中力を持つ",
            "思慮深い判断力",
            "好奇心が旺盛",
            "行動の切り替えが早い",
            "継続的な実行力"
        ],
        "potential_jobs": [
            {
                "job_title": "データアナリスト",
                "reason": "論理的思考力と集中力を活かせる"
            },
            # ... more jobs
        ]
    },
    "quantitative_scores": {
        "継続・集中力": 8,
        "実行・行動力": 7,
        "共感・協調性": 6,
        "論理・分析力": 9,
        "創造・発想力": 7,
        "計画・堅実性": 8
    }
}
```

### テスト範囲
- **入力検証**: 境界値テスト、エラーケース
- **API応答処理**: JSON解析、構造検証
- **データ変換**: DataFrame作成、統計計算
- **モック使用**: 外部API依存の分離

### 技術仕様
- **Testing Framework**: unittest
- **Mocking**: unittest.mock
- **Coverage**: 主要機能の80%以上
- **Automation**: CI/CD対応可能

---

## 🔧 開発者向け情報

### 環境設定
1. 仮想環境の作成と有効化
2. 依存関係のインストール
3. 環境変数の設定（.env）
4. テストの実行

### コード品質
- **Linting**: flake8
- **Type Checking**: mypy
- **Testing**: pytest/unittest
- **Documentation**: docstring完備

### 拡張ポイント
1. **新しい分析軸の追加**: `capability_dimensions`の拡張
2. **可視化の追加**: 新しいチャートタイプの実装
3. **エクスポート形式**: 新しい出力フォーマット
4. **API統合**: 他のAIモデルとの連携

---

## 📝 設計思想

### アーキテクチャ原則
- **単一責任原則**: 各モジュールは明確な役割を持つ
- **依存関係の逆転**: インターフェースに依存し、実装に依存しない
- **開放閉鎖原則**: 拡張に対して開かれ、修正に対して閉じている

### パフォーマンス考慮
- **非同期処理**: API呼び出し時の応答性確保
- **キャッシュ機能**: セッション状態による結果保持
- **メモリ効率**: 大量テキスト処理時の最適化

### セキュリティ
- **API キー管理**: 環境変数による機密情報の分離
- **入力検証**: XSS、インジェクション攻撃の防止
- **エラー情報**: 機密情報の漏洩防止

---
