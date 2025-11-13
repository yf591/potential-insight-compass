"""
Data Processor Module - Data Processing Utilities

This module handles data processing, validation, and transformation
for the Potential Insight Compass system.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict

import pandas as pd


@dataclass
class ProcessedData:
    """Data class for processed analysis data."""

    timestamp: str
    input_text: str
    input_length: int
    strengths: List[str]
    potential_jobs: List[Dict[str, str]]
    scores_df: pd.DataFrame
    processing_time: float
    metadata: Dict[str, Any]


class DataProcessor:
    """
    Data processor class for handling various data operations.

    Features:
    - Text preprocessing and normalization
    - Data validation and cleaning
    - DataFrame creation for visualization
    - Export functionality
    """

    def __init__(self):
        """Initialize the data processor."""
        self.capability_dimensions = [
            "継続・集中力",
            "実行・行動力",
            "共感・協調性",
            "論理・分析力",
            "創造・発想力",
            "計画・堅実性",
        ]

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess input text for analysis.

        Args:
            text: Raw input text

        Returns:
            Preprocessed text
        """
        if not text:
            return ""

        # Normalize whitespace and line breaks
        processed_text = re.sub(r"\s+", " ", text.strip())

        # Remove excessive punctuation
        processed_text = re.sub(r"[！]{2,}", "！", processed_text)
        processed_text = re.sub(r"[？]{2,}", "？", processed_text)
        processed_text = re.sub(r"[。]{2,}", "。", processed_text)

        # Normalize quotation marks
        processed_text = processed_text.replace('"', '"').replace('"', '"')
        processed_text = processed_text.replace(""", "'").replace(""", "'")

        return processed_text

    def validate_analysis_data(self, data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate analysis data structure and content.

        Args:
            data: Analysis data dictionary

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check top-level structure
        if not isinstance(data, dict):
            errors.append("データが辞書形式ではありません")
            return False, errors

        # Check qualitative analysis
        if "qualitative_analysis" not in data:
            errors.append("定性分析データが見つかりません")
        else:
            qual_data = data["qualitative_analysis"]

            # Check strengths
            if "strengths" not in qual_data:
                errors.append("強みデータが見つかりません")
            elif not isinstance(qual_data["strengths"], list):
                errors.append("強みデータがリスト形式ではありません")
            elif len(qual_data["strengths"]) != 5:
                errors.append(
                    f"強みは5項目である必要があります（現在: {len(qual_data['strengths'])}項目）"
                )

            # Check potential jobs
            if "potential_jobs" not in qual_data:
                errors.append("職業適性データが見つかりません")
            elif not isinstance(qual_data["potential_jobs"], list):
                errors.append("職業適性データがリスト形式ではありません")
            elif len(qual_data["potential_jobs"]) != 3:
                errors.append(
                    f"職業適性は3項目である必要があります（現在: {len(qual_data['potential_jobs'])}項目）"
                )
            else:
                for i, job in enumerate(qual_data["potential_jobs"]):
                    if not isinstance(job, dict):
                        errors.append(f"職業適性{i+1}が辞書形式ではありません")
                    elif "job_title" not in job or "reason" not in job:
                        errors.append(
                            f"職業適性{i+1}にjob_titleまたはreasonが不足しています"
                        )

        # Check quantitative scores
        if "quantitative_scores" not in data:
            errors.append("定量分析データが見つかりません")
        else:
            scores = data["quantitative_scores"]
            if not isinstance(scores, dict):
                errors.append("定量分析データが辞書形式ではありません")
            else:
                for dimension in self.capability_dimensions:
                    if dimension not in scores:
                        errors.append(f"能力次元 '{dimension}' が見つかりません")
                    else:
                        score = scores[dimension]
                        if not isinstance(score, (int, float)):
                            errors.append(f"'{dimension}' のスコアが数値ではありません")
                        elif score < 1 or score > 10:
                            errors.append(
                                f"'{dimension}' のスコアが範囲外です（1-10の間である必要があります）"
                            )

        return len(errors) == 0, errors

    def create_scores_dataframe(self, scores: Dict[str, int]) -> pd.DataFrame:
        """
        Create a pandas DataFrame from capability scores.

        Args:
            scores: Dictionary of capability scores

        Returns:
            DataFrame with scores for visualization
        """
        # Create DataFrame
        df = pd.DataFrame(
            [
                {"能力次元": dimension, "スコア": scores.get(dimension, 0)}
                for dimension in self.capability_dimensions
            ]
        )

        # Add additional columns for visualization
        df["最大値"] = 10
        df["パーセンテージ"] = (df["スコア"] / 10) * 100

        return df

    def process_analysis_result(
        self,
        input_text: str,
        analysis_result: Any,
        additional_metadata: Optional[Dict] = None,
    ) -> ProcessedData:
        """
        Process complete analysis result into structured format.

        Args:
            input_text: Original input text
            analysis_result: Analysis result object
            additional_metadata: Additional metadata to include

        Returns:
            ProcessedData object with structured data
        """
        # Create scores DataFrame
        scores_df = self.create_scores_dataframe(analysis_result.quantitative_scores)

        # Prepare metadata
        metadata = {
            "analysis_timestamp": datetime.now().isoformat(),
            "input_character_count": len(input_text),
            "processing_time_seconds": analysis_result.processing_time,
            "api_response_length": len(analysis_result.raw_response),
        }

        if additional_metadata:
            metadata.update(additional_metadata)

        return ProcessedData(
            timestamp=datetime.now().isoformat(),
            input_text=self.preprocess_text(input_text),
            input_length=len(input_text),
            strengths=analysis_result.strengths,
            potential_jobs=analysis_result.potential_jobs,
            scores_df=scores_df,
            processing_time=analysis_result.processing_time,
            metadata=metadata,
        )

    def export_to_json(
        self, processed_data: ProcessedData, include_raw_text: bool = False
    ) -> str:
        """
        Export processed data to JSON format.

        Args:
            processed_data: ProcessedData object to export
            include_raw_text: Whether to include raw input text

        Returns:
            JSON string representation
        """
        export_dict = {
            "timestamp": processed_data.timestamp,
            "input_length": processed_data.input_length,
            "processing_time": processed_data.processing_time,
            "strengths": processed_data.strengths,
            "potential_jobs": processed_data.potential_jobs,
            "quantitative_scores": processed_data.scores_df[["能力次元", "スコア"]]
            .set_index("能力次元")["スコア"]
            .to_dict(),
            "metadata": processed_data.metadata,
        }

        if include_raw_text:
            export_dict["input_text"] = processed_data.input_text

        return json.dumps(export_dict, ensure_ascii=False, indent=2)

    def export_to_markdown(self, processed_data: ProcessedData) -> str:
        """
        Export processed data to Markdown format.

        Args:
            processed_data: ProcessedData object to export

        Returns:
            Markdown string representation
        """
        md_content = f"""# 潜在能力分析結果レポート

## 📊 分析概要

- **分析日時**: {processed_data.timestamp}
- **入力文字数**: {processed_data.input_length:,} 文字
- **処理時間**: {processed_data.processing_time:.2f} 秒

## 💪 発見された強み

"""

        for i, strength in enumerate(processed_data.strengths, 1):
            md_content += f"{i}. {strength}\n"

        md_content += "\n## 🎯 適性のある職業\n\n"

        for i, job in enumerate(processed_data.potential_jobs, 1):
            md_content += f"### {i}. {job['job_title']}\n\n"
            md_content += f"**理由**: {job['reason']}\n\n"

        md_content += "## 📈 能力スコア\n\n"

        for _, row in processed_data.scores_df.iterrows():
            dimension = row["能力次元"]
            score = row["スコア"]
            percentage = row["パーセンテージ"]
            bar = "█" * int(percentage // 10) + "░" * (10 - int(percentage // 10))
            md_content += f"**{dimension}**: {score}/10 `{bar}` ({percentage:.0f}%)\n\n"

        return md_content

    def calculate_statistics(self, scores_df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate statistical measures from scores.

        Args:
            scores_df: DataFrame with capability scores

        Returns:
            Dictionary with statistical measures
        """
        scores = scores_df["スコア"].values

        return {
            "平均値": float(scores.mean()),
            "最大値": float(scores.max()),
            "最小値": float(scores.min()),
            "標準偏差": float(scores.std()),
            "中央値": float(pd.Series(scores).median()),
            "合計値": float(scores.sum()),
            "レンジ": float(scores.max() - scores.min()),
        }

    def identify_top_strengths(
        self, scores_df: pd.DataFrame, top_n: int = 3
    ) -> List[Tuple[str, int]]:
        """
        Identify top N capability dimensions based on scores.

        Args:
            scores_df: DataFrame with capability scores
            top_n: Number of top capabilities to return

        Returns:
            List of tuples (dimension_name, score) sorted by score
        """
        sorted_scores = scores_df.sort_values("スコア", ascending=False)
        return [
            (row["能力次元"], row["スコア"])
            for _, row in sorted_scores.head(top_n).iterrows()
        ]

    def identify_development_areas(
        self, scores_df: pd.DataFrame, bottom_n: int = 2
    ) -> List[Tuple[str, int]]:
        """
        Identify areas for development based on lowest scores.

        Args:
            scores_df: DataFrame with capability scores
            bottom_n: Number of development areas to return

        Returns:
            List of tuples (dimension_name, score) sorted by score (lowest first)
        """
        sorted_scores = scores_df.sort_values("スコア", ascending=True)
        return [
            (row["能力次元"], row["スコア"])
            for _, row in sorted_scores.head(bottom_n).iterrows()
        ]
