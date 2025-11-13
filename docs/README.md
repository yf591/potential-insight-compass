# PIC ドキュメントインデックス

Potential Insight Compass (PIC) システムの包括的なドキュメントへようこそ。

## 📚 ドキュメント構成

### 🚀 はじめに
- **[README (English)](../README.md)** - プロジェクト概要とクイックスタート（英語）
- **[README (日本語)](../README-ja.md)** - プロジェクト概要とクイックスタート（日本語）
- **[システム仕様書](../SPECIFICATION.md)** - 詳細な技術仕様（日本語）

### 🔧 開発者向けドキュメント
- **[コードドキュメント](code-documentation.md)** - 各ファイルとモジュールの詳細解説
- **[APIリファレンス](api-reference.md)** - クラスとメソッドの完全なAPIリファレンス

### 📁 ファイル構造概要

```
docs/
├── README.md              # このファイル（ドキュメントインデックス）
├── code-documentation.md  # コード詳細解説
└── api-reference.md       # APIリファレンス
```

## 🎯 用途別ガイド

### 初回利用者向け
1. [日本語README](../README-ja.md) でシステム概要を把握
2. [クイックスタート](../README-ja.md#-クイックスタート) でセットアップ
3. [使用方法](../README-ja.md#-使用方法) で基本操作を確認

### 開発者向け
1. [システム仕様書](../SPECIFICATION.md) で全体設計を理解
2. [コードドキュメント](code-documentation.md) で実装詳細を確認
3. [APIリファレンス](api-reference.md) で具体的な使用方法を確認

### カスタマイズ・拡張
1. [アーキテクチャ設計](code-documentation.md#-設計思想) を理解
2. [拡張ガイド](api-reference.md#-拡張ガイド) で実装方法を確認
3. [開発環境](../README-ja.md#-開発) でテスト・品質管理方法を確認

## 🔍 技術仕様サマリー

### システム構成
- **フロントエンド**: Streamlit (Python Webアプリ)
- **AI エンジン**: Google Gemini API
- **データ処理**: Pandas + NumPy
- **可視化**: Plotly (インタラクティブチャート)

### 主要機能
- **テキスト分析**: AI による面談記録の分析
- **リフレーミング**: ネガティブ特性をポジティブに変換
- **可視化**: 6軸レーダーチャートと棒グラフ
- **エクスポート**: JSON・Markdown形式での結果出力

### ファイル構成
```
src/
├── ai_analyzer.py      # AI分析エンジン
├── data_processor.py   # データ処理
└── visualizer.py       # チャート生成

tests/
└── test_analyzer.py    # ユニットテスト

app.py                  # メインアプリケーション
```

## 🛠️ 開発ワークフロー

### 基本的な開発フロー
1. **環境準備**
   ```bash
   source .venv/bin/activate  # 仮想環境有効化
   ```

2. **コード編集**
   - `src/` 内のモジュールを編集
   - [コードドキュメント](code-documentation.md) を参考に実装

3. **テスト実行**
   ```bash
   python -m pytest tests/
   ```

4. **アプリケーション起動**
   ```bash
   streamlit run app.py
   ```

### コード品質管理
```bash
# リンティング
flake8 src/

# 型チェック
mypy src/

# テストカバレッジ
pytest --cov=src tests/
```

## 📖 学習リソース

### Streamlit
- [公式ドキュメント](https://docs.streamlit.io/)
- [チュートリアル](https://docs.streamlit.io/library/get-started)

### Google Gemini API
- [公式ドキュメント](https://ai.google.dev/docs)
- [Python SDK](https://ai.google.dev/docs/python_quickstart)

### Plotly
- [公式ドキュメント](https://plotly.com/python/)
- [レーダーチャート](https://plotly.com/python/radar-chart/)

## 🚨 注意事項

### セキュリティ
- **APIキー**: `.env` ファイルは絶対にコミットしない
- **機密情報**: 分析対象テキストに個人情報が含まれる場合は適切に管理

### パフォーマンス
- **API制限**: Gemini APIのレート制限に注意
- **メモリ使用量**: 大量テキスト処理時はメモリ使用量を監視

### 互換性
- **Python バージョン**: 3.12.4以上を推奨
- **依存関係**: requirements.txtで管理されたバージョンを使用

## 🤝 貢献・サポート

### 貢献方法
1. イシューの作成・議論
2. プルリクエストの提出
3. ドキュメントの改善

### サポート窓口
- **GitHub Issues**: バグ報告・機能要望
- **ドキュメント**: 技術的な質問
- **コードレビュー**: 実装に関する相談

---