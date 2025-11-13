"""
Unit tests for the AI Analyzer module.

This module contains tests for the AIAnalyzer class and related functionality.
"""

import unittest
from unittest.mock import Mock, patch
import json
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.ai_analyzer import AIAnalyzer, AnalysisResult
from src.data_processor import DataProcessor


class TestAIAnalyzer(unittest.TestCase):
    """Test cases for AIAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock API key for testing
        self.test_api_key = "test_api_key_123"

        # Sample valid response data
        self.sample_response_data = {
            "qualitative_analysis": {
                "strengths": [
                    "高い集中力を持つ",
                    "思慮深い判断力",
                    "好奇心が旺盛",
                    "行動の切り替えが早い",
                    "継続的な実行力",
                ],
                "potential_jobs": [
                    {
                        "job_title": "データアナリスト",
                        "reason": "論理的思考力と集中力を活かせる",
                    },
                    {
                        "job_title": "プロジェクトマネージャー",
                        "reason": "計画性と実行力が求められる職種",
                    },
                    {
                        "job_title": "UXデザイナー",
                        "reason": "創造性と共感力を活用できる",
                    },
                ],
            },
            "quantitative_scores": {
                "継続・集中力": 8,
                "実行・行動力": 7,
                "共感・協調性": 6,
                "論理・分析力": 9,
                "創造・発想力": 7,
                "計画・堅実性": 8,
            },
        }

    def test_input_validation_empty_text(self):
        """Test input validation with empty text."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        is_valid, error_msg = analyzer.validate_input("")
        self.assertFalse(is_valid)
        self.assertIn("空です", error_msg)

    def test_input_validation_short_text(self):
        """Test input validation with too short text."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        is_valid, error_msg = analyzer.validate_input("短い")
        self.assertFalse(is_valid)
        self.assertIn("短すぎます", error_msg)

    def test_input_validation_long_text(self):
        """Test input validation with too long text."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        long_text = "あ" * 10001  # Over 10,000 characters
        is_valid, error_msg = analyzer.validate_input(long_text)
        self.assertFalse(is_valid)
        self.assertIn("長すぎます", error_msg)

    def test_input_validation_valid_text(self):
        """Test input validation with valid text."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        valid_text = "これは有効なテストテキストです。十分な長さがあります。"
        is_valid, error_msg = analyzer.validate_input(valid_text)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        json_response = json.dumps(self.sample_response_data, ensure_ascii=False)
        parsed_data = analyzer._parse_response(json_response)

        self.assertEqual(
            parsed_data["qualitative_analysis"]["strengths"],
            self.sample_response_data["qualitative_analysis"]["strengths"],
        )

    def test_parse_response_with_markdown_wrapper(self):
        """Test parsing JSON response wrapped in markdown."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        json_response = (
            f"```json\n{json.dumps(self.sample_response_data, ensure_ascii=False)}\n```"
        )
        parsed_data = analyzer._parse_response(json_response)

        self.assertEqual(len(parsed_data["qualitative_analysis"]["strengths"]), 5)

    def test_validate_response_structure_valid(self):
        """Test response structure validation with valid data."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        # Should not raise any exception
        analyzer._validate_response_structure(self.sample_response_data)

    def test_validate_response_structure_missing_keys(self):
        """Test response structure validation with missing keys."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        invalid_data = {"qualitative_analysis": {}}  # Missing quantitative_scores

        with self.assertRaises(ValueError) as context:
            analyzer._validate_response_structure(invalid_data)

        self.assertIn("quantitative_scores", str(context.exception))

    def test_get_capability_dimensions(self):
        """Test getting capability dimensions."""
        analyzer = AIAnalyzer(api_key=self.test_api_key)

        dimensions = analyzer.get_capability_dimensions()

        expected_dimensions = [
            "継続・集中力",
            "実行・行動力",
            "共感・協調性",
            "論理・分析力",
            "創造・発想力",
            "計画・堅実性",
        ]

        self.assertEqual(dimensions, expected_dimensions)


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()

        # Sample scores data for testing
        self.sample_scores = {
            "継続・集中力": 8,
            "実行・行動力": 7,
            "共感・協調性": 6,
            "論理・分析力": 9,
            "創造・発想力": 7,
            "計画・堅実性": 8,
        }

    def test_preprocess_text_whitespace_normalization(self):
        """Test text preprocessing with whitespace normalization."""
        input_text = "これは　　テスト\n\n\nです。   "
        processed = self.processor.preprocess_text(input_text)

        self.assertEqual(processed, "これは テスト です。")

    def test_preprocess_text_punctuation_normalization(self):
        """Test text preprocessing with punctuation normalization."""
        input_text = "本当に！！！！そうですか？？？"
        processed = self.processor.preprocess_text(input_text)

        self.assertEqual(processed, "本当に！そうですか？")

    def test_create_scores_dataframe(self):
        """Test creating scores DataFrame."""
        df = self.processor.create_scores_dataframe(self.sample_scores)

        self.assertEqual(len(df), 6)  # 6 capability dimensions
        self.assertTrue("能力次元" in df.columns)
        self.assertTrue("スコア" in df.columns)
        self.assertTrue("最大値" in df.columns)
        self.assertTrue("パーセンテージ" in df.columns)

        # Check if percentages are calculated correctly
        first_row = df.iloc[0]
        expected_percentage = (first_row["スコア"] / 10) * 100
        self.assertEqual(first_row["パーセンテージ"], expected_percentage)

    def test_validate_analysis_data_valid(self):
        """Test analysis data validation with valid data."""
        valid_data = {
            "qualitative_analysis": {
                "strengths": ["強み1", "強み2", "強み3", "強み4", "強み5"],
                "potential_jobs": [
                    {"job_title": "職業1", "reason": "理由1"},
                    {"job_title": "職業2", "reason": "理由2"},
                    {"job_title": "職業3", "reason": "理由3"},
                ],
            },
            "quantitative_scores": self.sample_scores,
        }

        is_valid, errors = self.processor.validate_analysis_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_validate_analysis_data_invalid_structure(self):
        """Test analysis data validation with invalid structure."""
        invalid_data = {
            "qualitative_analysis": {
                "strengths": ["強み1", "強み2"],  # Should be 5 items
                "potential_jobs": [],  # Should be 3 items
            }
        }

        is_valid, errors = self.processor.validate_analysis_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)


if __name__ == "__main__":
    unittest.main()
