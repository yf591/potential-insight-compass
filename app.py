"""
Main Streamlit Application for Potential Insight Compass (PIC)

This is the main entry point for the web application that provides
AI-powered career counseling analysis with interactive visualizations.
"""

import streamlit as st
import time
from datetime import datetime
from typing import Optional

# Import our custom modules
from src.ai_analyzer import AIAnalyzer, AnalysisResult
from src.data_processor import DataProcessor, ProcessedData
from src.visualizer import ChartVisualizer


# Page configuration
st.set_page_config(
    page_title="Potential Insight Compass (PIC)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ca02c;
        background-color: #f0f8f0;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #d62728;
        background-color: #fff0f0;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []


def display_header():
    """Display the main header and description."""
    st.markdown(
        '<div class="main-header">🎯 Potential Insight Compass (PIC)</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="info-box">
        <strong>AIキャリア分析システム</strong><br>
        面談記録やカウンセリングノートを分析し、隠れた強みとキャリアの可能性を発見します。
        ネガティブな特性もポジティブな強みとして再定義し、新たな自己理解をサポートします。
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_sidebar():
    """Display sidebar with information and controls."""
    st.sidebar.markdown("## 📊 システム情報")

    st.sidebar.markdown(
        """
    ### 分析項目
    **定性分析:**
    - 5つの強み
    - 3つの職業適性
    
    **定量分析:**
    - 継続・集中力
    - 実行・行動力
    - 共感・協調性
    - 論理・分析力
    - 創造・発想力
    - 計画・堅実性
    """
    )

    st.sidebar.markdown("---")

    # Analysis history
    if st.session_state.analysis_history:
        st.sidebar.markdown("### 📝 分析履歴")
        st.sidebar.write(
            f"これまでの分析回数: {len(st.session_state.analysis_history)}"
        )

        if st.sidebar.button("履歴をクリア"):
            st.session_state.analysis_history = []
            st.sidebar.success("履歴をクリアしました")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
    ### ℹ️ 使用方法
    1. 面談記録やカウンセリングノートを入力
    2. 「分析開始」ボタンをクリック
    3. 結果を確認し、必要に応じてエクスポート
    """
    )


def input_section():
    """Display the text input section."""
    st.markdown(
        '<div class="sub-header">📝 分析対象テキストの入力</div>',
        unsafe_allow_html=True,
    )

    # Input text area
    input_text = st.text_area(
        label="面談記録・カウンセリングノート",
        height=200,
        max_chars=10000,
        placeholder="ここに分析したいテキストを入力してください...\n\n例：\n- 面談での発言内容\n- カウンセリングでの相談内容\n- 自己評価や悩みについて\n- 過去の経験や興味について",
        help="最大10,000文字まで入力できます。より詳細な内容ほど正確な分析が可能です。",
    )

    # Character count
    if input_text:
        char_count = len(input_text)
        st.caption(f"文字数: {char_count:,} / 10,000")

    return input_text


def analysis_section(input_text: str, analyzer: AIAnalyzer, processor: DataProcessor):
    """Handle the analysis process."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        analyze_button = st.button(
            "🚀 分析開始",
            type="primary",
            use_container_width=True,
            disabled=not input_text or len(input_text.strip()) < 10,
        )

    if analyze_button and input_text:
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Update progress
            status_text.text("📊 AI分析を実行中...")
            progress_bar.progress(25)

            # Perform analysis
            analysis_result = analyzer.analyze_text(input_text)
            progress_bar.progress(75)

            # Process data
            status_text.text("📈 データを処理中...")
            processed_data = processor.process_analysis_result(
                input_text, analysis_result
            )
            progress_bar.progress(100)

            # Store results in session state
            st.session_state.analysis_result = analysis_result
            st.session_state.processed_data = processed_data

            # Add to history
            st.session_state.analysis_history.append(
                {
                    "timestamp": datetime.now(),
                    "input_length": len(input_text),
                    "processing_time": analysis_result.processing_time,
                }
            )

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Show success message
            st.markdown(
                """
            <div class="success-box">
                ✅ <strong>分析完了!</strong><br>
                分析結果が下部に表示されました。結果をスクロールして確認してください。
            </div>
            """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.markdown(
                f"""
            <div class="warning-box">
                ❌ <strong>エラーが発生しました</strong><br>
                {str(e)}
            </div>
            """,
                unsafe_allow_html=True,
            )


def display_results(processed_data: ProcessedData, visualizer: ChartVisualizer):
    """Display analysis results."""
    if processed_data is None:
        return

    st.markdown("---")
    st.markdown('<div class="sub-header">📊 分析結果</div>', unsafe_allow_html=True)

    # Processing metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="処理時間", value=f"{processed_data.processing_time:.2f}秒")

    with col2:
        st.metric(label="入力文字数", value=f"{processed_data.input_length:,}")

    with col3:
        avg_score = processed_data.scores_df["スコア"].mean()
        st.metric(label="平均スコア", value=f"{avg_score:.1f}/10")

    with col4:
        max_score = processed_data.scores_df["スコア"].max()
        st.metric(label="最高スコア", value=f"{max_score}/10")

    # Qualitative Analysis
    st.markdown("### 💪 発見された強み")

    for i, strength in enumerate(processed_data.strengths, 1):
        st.markdown(f"**{i}.** {strength}")

    # Career Recommendations
    st.markdown("### 🎯 適性のある職業")

    for i, job in enumerate(processed_data.potential_jobs, 1):
        with st.expander(f"{i}. {job['job_title']}", expanded=i == 1):
            st.write(f"**理由:** {job['reason']}")

    # Quantitative Analysis
    st.markdown("### 📈 能力スコア可視化")

    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["🕸️ レーダーチャート", "📊 棒グラフ", "📈 統計情報"])

    with tab1:
        radar_chart = visualizer.create_radar_chart(processed_data.scores_df)
        st.plotly_chart(radar_chart, use_container_width=True)

    with tab2:
        bar_chart = visualizer.create_bar_chart(
            processed_data.scores_df, horizontal=True
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    with tab3:
        # Calculate statistics
        from src.data_processor import DataProcessor

        temp_processor = DataProcessor()
        statistics = temp_processor.calculate_statistics(processed_data.scores_df)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 統計サマリー")
            for metric, value in statistics.items():
                st.metric(label=metric, value=f"{value:.2f}")

        with col2:
            st.markdown("#### 🏆 トップ3能力")
            top_strengths = temp_processor.identify_top_strengths(
                processed_data.scores_df
            )
            for i, (dimension, score) in enumerate(top_strengths, 1):
                st.write(f"**{i}.** {dimension}: {score}/10")

            st.markdown("#### 🎯 成長領域")
            development_areas = temp_processor.identify_development_areas(
                processed_data.scores_df
            )
            for dimension, score in development_areas:
                st.write(f"• {dimension}: {score}/10")


def export_section(processed_data: ProcessedData, processor: DataProcessor):
    """Display export options."""
    if processed_data is None:
        return

    st.markdown("### 💾 結果のエクスポート")

    col1, col2 = st.columns(2)

    with col1:
        # JSON export
        json_data = processor.export_to_json(processed_data, include_raw_text=False)
        st.download_button(
            label="📄 JSON形式でダウンロード",
            data=json_data,
            file_name=f"analysis_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )

    with col2:
        # Markdown export
        markdown_data = processor.export_to_markdown(processed_data)
        st.download_button(
            label="📝 Markdown形式でダウンロード",
            data=markdown_data,
            file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()

    # Display header
    display_header()

    # Display sidebar
    display_sidebar()

    try:
        # Initialize components
        analyzer = AIAnalyzer()
        processor = DataProcessor()
        visualizer = ChartVisualizer()

        # Input section
        input_text = input_section()

        # Analysis section
        analysis_section(input_text, analyzer, processor)

        # Display results if available
        if st.session_state.processed_data:
            display_results(st.session_state.processed_data, visualizer)
            export_section(st.session_state.processed_data, processor)

    except Exception as e:
        st.error(f"システム初期化エラー: {str(e)}")
        st.info("環境変数の設定を確認してください。詳細はREADME.mdを参照してください。")


if __name__ == "__main__":
    main()
