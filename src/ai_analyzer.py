"""
AI Analyzer Module - Gemini API Integration

This module handles the integration with Google Gemini API to analyze
counseling texts and generate insights about strengths and career potential.
"""

import json
import os
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

import google.generativeai as genai
from dotenv import load_dotenv


@dataclass
class AnalysisResult:
    """Data class to hold analysis results."""

    strengths: List[str]
    potential_jobs: List[Dict[str, str]]
    quantitative_scores: Dict[str, int]
    raw_response: str
    processing_time: float


class AIAnalyzer:
    """
    AI Analyzer class that uses Google Gemini API to analyze counseling texts.

    Features:
    - Reframes negative traits into positive strengths
    - Provides qualitative analysis (5 strengths, 3 career recommendations)
    - Generates quantitative scores across 6 capability dimensions
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Analyzer.

        Args:
            api_key: Google Gemini API key. If None, loads from environment.
        """
        # Load environment variables
        load_dotenv()

        # Set up API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables or parameters"
            )

        # Configure Gemini API
        genai.configure(api_key=self.api_key)

        # Initialize the model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        # Define system prompt based on SPECIFICATION.md
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt based on specifications."""
        return """あなたは、高度な『共感力』と『鋭い分析眼』を持つ、『プロフェッショナル・キャリア戦略家』です。
あなたの『任務』は、ユーザー（キャリアカウンセラー等）が入力した、『自信』を失ったクライアント（診断対象者）の『面談記録』を分析することです。

以下の『厳格なルール』に従い、クライアントの『隠された才能』を『翻訳』し、『客観的』な分析結果を提供しなさい。

## 厳格なルール

1.  **【ネガティブ・ポジティブ リフレーミング】:**
    入力テキストに含まれる、いかなる『ネガティブ』な表現（例：「人見知りだ」「続かない」「飽きっぽい」「ゲームばかりしている」「不安だ」）も、
    『すべて』、客観的かつ『ポジティブ』な『強み（ポテンシャル）』として『再定義（リフレーミング）』しなさい。
    （例：「人見知り」→「高い集中力を持つ」「思慮深い」）
    （例：「飽きっぽい」→「好奇心が旺盛」「行動の切り替えが早い」）
    （例：「ゲームばかり」→「高い攻略（戦略）能力」「継続的な実行力」）

2.  **【2種類の分析結果の生成】:**
    あなたの分析結果は、以下の「A」と「B」の「2種類」を『必ず』生成しなければなりません。

    * **A: 『定性的』分析（文章）:**
        * クライアントの『強み（再定義後）』を『5つ』、箇条書きで『抽出』しなさい。
        * その『強み』を活かせると『判断』した、『3つ』の『職業適性の可能性』を、その『理由』と共に『提示』しなさい。

    * **B: 『定量的』分析（スコア）:**
        * 入力テキストから、クライアントの『潜在能力』を以下の『6つ』の『軸』で『分析』し、それぞれ『10点満点（整数）』で『採点』しなさい。
        * **『6つ』の『軸』:**
            1.  **【継続・集中力】:** （一つのことへの没頭度、忍耐力）
            2.  **【実行・行動力】:** （決断の速さ、行動への移行性）
            3.  **【共感・協調性】:** （他者への配慮、傾聴力、感受性）
            4.  **【論理・分析力】:** （構造的把握、原因追及、数値的思考）
            5.  **【創造・発想力】:** （独自の視点、趣味や芸術性）
            6.  **【計画・堅実性】:** （慎重さ、不安感（＝リスク管理）、安定志向）

3.  **【出力フォーマット（厳格）】:**
    あなたの『回答』は、『単一』の『JSONオブジェクト』『のみ』で『出力』すること。
    JSONの前後に、解説文やマークダウン指定（例: ```json）を『一切』、『含めてはならない』。

## 出力JSONフォーマット

{
  "qualitative_analysis": {
    "strengths": [
      "（ここに『翻訳』した『強み』1）",
      "（ここに『翻訳』した『強み』2）",
      "（ここに『翻訳』した『強み』3）",
      "（ここに『翻訳』した『強み』4）",
      "（ここに『翻訳』した『強み』5）"
    ],
    "potential_jobs": [
      {
        "job_title": "（ここに『職業の可能性』1）",
        "reason": "（ここに、その『理由』）"
      },
      {
        "job_title": "（ここに『職業の可能性』2）",
        "reason": "（ここに、その『理由』）"
      },
      {
        "job_title": "（ここに『職業の可能性』3）",
        "reason": "（ここに、その『理由』）"
      }
    ]
  },
  "quantitative_scores": {
    "継続・集中力": （ここに1から10の『整数』）,
    "実行・行動力": （ここに1から10の『整数』）,
    "共感・協調性": （ここに1から10の『整数』）,
    "論理・分析力": （ここに1から10の『整数』）,
    "創造・発想力": （ここに1から10の『整数』）,
    "計画・堅実性": （ここに1から10の『整数』）
  }
}"""

    def validate_input(self, text: str) -> Tuple[bool, str]:
        """
        Validate input text.

        Args:
            text: Input text to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text or not text.strip():
            return False, "入力テキストが空です。分析対象のテキストを入力してください。"

        if len(text.strip()) < 10:
            return False, "入力テキストが短すぎます。より詳細な内容を入力してください。"

        if len(text) > 10000:
            return (
                False,
                f"入力テキストが長すぎます。{len(text)}文字ですが、上限は10,000文字です。",
            )

        return True, ""

    def analyze_text(self, text: str, max_retries: int = 3) -> AnalysisResult:
        """
        Analyze the input text using Gemini API.

        Args:
            text: Input text to analyze
            max_retries: Maximum number of retry attempts

        Returns:
            AnalysisResult object containing the analysis results

        Raises:
            ValueError: If input validation fails
            Exception: If API call fails after retries
        """
        # Validate input
        is_valid, error_msg = self.validate_input(text)
        if not is_valid:
            raise ValueError(error_msg)

        start_time = time.time()

        # Prepare the prompt
        full_prompt = f"{self.system_prompt}\n\n## 分析対象テキスト\n{text}"

        # Attempt API call with retries
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(full_prompt)
                raw_response = response.text

                # Parse JSON response
                analysis_data = self._parse_response(raw_response)

                processing_time = time.time() - start_time

                return AnalysisResult(
                    strengths=analysis_data["qualitative_analysis"]["strengths"],
                    potential_jobs=analysis_data["qualitative_analysis"][
                        "potential_jobs"
                    ],
                    quantitative_scores=analysis_data["quantitative_scores"],
                    raw_response=raw_response,
                    processing_time=processing_time,
                )

            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(
                        f"API呼び出しが失敗しました（{max_retries}回試行）: {str(e)}"
                    )

                # Wait before retry (exponential backoff)
                wait_time = 2**attempt
                time.sleep(wait_time)
                continue

    def _parse_response(self, response_text: str) -> Dict:
        """
        Parse the JSON response from Gemini API.

        Args:
            response_text: Raw response text from API

        Returns:
            Parsed JSON data as dictionary

        Raises:
            ValueError: If JSON parsing fails
        """
        try:
            # Clean the response text (remove any markdown formatting)
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()

            # Parse JSON
            data = json.loads(cleaned_response)

            # Validate structure
            self._validate_response_structure(data)

            return data

        except json.JSONDecodeError as e:
            raise ValueError(
                f"JSON解析に失敗しました: {str(e)}\nレスポンス: {response_text[:500]}"
            )

    def _validate_response_structure(self, data: Dict) -> None:
        """
        Validate the structure of parsed response data.

        Args:
            data: Parsed JSON data

        Raises:
            ValueError: If structure validation fails
        """
        required_keys = ["qualitative_analysis", "quantitative_scores"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"必須キー '{key}' がレスポンスに含まれていません")

        # Validate qualitative analysis
        qual_analysis = data["qualitative_analysis"]
        if "strengths" not in qual_analysis or len(qual_analysis["strengths"]) != 5:
            raise ValueError("強みは5項目である必要があります")

        if (
            "potential_jobs" not in qual_analysis
            or len(qual_analysis["potential_jobs"]) != 3
        ):
            raise ValueError("職業適性は3項目である必要があります")

        # Validate quantitative scores
        quant_scores = data["quantitative_scores"]
        expected_dimensions = [
            "継続・集中力",
            "実行・行動力",
            "共感・協調性",
            "論理・分析力",
            "創造・発想力",
            "計画・堅実性",
        ]

        for dimension in expected_dimensions:
            if dimension not in quant_scores:
                raise ValueError(f"能力次元 '{dimension}' がスコアに含まれていません")

            score = quant_scores[dimension]
            if not isinstance(score, int) or score < 1 or score > 10:
                raise ValueError(
                    f"スコア '{dimension}' は1-10の整数である必要があります"
                )

    def get_capability_dimensions(self) -> List[str]:
        """
        Get the list of capability dimensions used in analysis.

        Returns:
            List of capability dimension names
        """
        return [
            "継続・集中力",
            "実行・行動力",
            "共感・協調性",
            "論理・分析力",
            "創造・発想力",
            "計画・堅実性",
        ]
