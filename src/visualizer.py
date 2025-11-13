"""
Visualizer Module - Chart Generation Functions

This module handles the creation of interactive visualizations
for the Potential Insight Compass system using Plotly.
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class ChartVisualizer:
    """
    Chart visualizer class for creating interactive charts and graphs.

    Features:
    - Radar charts for capability visualization
    - Bar charts for comparative analysis
    - Interactive charts with Plotly
    """

    def __init__(self):
        """Initialize the chart visualizer."""
        self.color_palette = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "warning": "#d62728",
            "info": "#9467bd",
            "light": "#17becf",
        }

        # Japanese font settings for better rendering
        self.font_family = "Arial, sans-serif"

    def create_radar_chart(
        self,
        scores_df: pd.DataFrame,
        title: str = "能力スコア レーダーチャート",
        show_values: bool = True,
    ) -> go.Figure:
        """
        Create an interactive radar chart for capability scores.

        Args:
            scores_df: DataFrame with capability scores
            title: Chart title
            show_values: Whether to show score values on the chart

        Returns:
            Plotly figure object
        """
        # Prepare data for radar chart
        dimensions = scores_df["能力次元"].tolist()
        scores = scores_df["スコア"].tolist()

        # Add the first dimension to the end to close the radar chart
        dimensions_closed = dimensions + [dimensions[0]]
        scores_closed = scores + [scores[0]]

        # Create radar chart
        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=scores_closed,
                theta=dimensions_closed,
                fill="toself",
                fillcolor=f'{self.color_palette["primary"]}30',  # 30% opacity
                line=dict(color=self.color_palette["primary"], width=3),
                marker=dict(color=self.color_palette["primary"], size=8),
                name="能力スコア",
                hovertemplate="<b>%{theta}</b><br>スコア: %{r}/10<extra></extra>",
            )
        )

        # Add score values as text annotations if requested
        if show_values:
            for i, (dim, score) in enumerate(zip(dimensions, scores)):
                # Calculate position for text
                angle = (i * 360 / len(dimensions)) * (
                    3.14159 / 180
                )  # Convert to radians
                r_text = score + 0.5  # Slightly outside the point

                fig.add_annotation(
                    x=r_text * np.cos(angle),
                    y=r_text * np.sin(angle),
                    text=str(score),
                    showarrow=False,
                    font=dict(
                        size=12,
                        color=self.color_palette["primary"],
                        family=self.font_family,
                    ),
                    xref="polar",
                    yref="polar",
                )

        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickmode="linear",
                    tick0=0,
                    dtick=2,
                    gridcolor="lightgray",
                    gridwidth=1,
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, family=self.font_family),
                    gridcolor="lightgray",
                    gridwidth=1,
                ),
            ),
            title=dict(text=title, x=0.5, font=dict(size=18, family=self.font_family)),
            showlegend=False,
            width=600,
            height=600,
            font=dict(family=self.font_family),
        )

        return fig

    def create_bar_chart(
        self,
        scores_df: pd.DataFrame,
        title: str = "能力スコア 棒グラフ",
        horizontal: bool = False,
    ) -> go.Figure:
        """
        Create a bar chart for capability scores.

        Args:
            scores_df: DataFrame with capability scores
            title: Chart title
            horizontal: Whether to create horizontal bar chart

        Returns:
            Plotly figure object
        """
        # Sort by score for better visualization
        sorted_df = scores_df.sort_values(
            "スコア", ascending=False if not horizontal else True
        )

        if horizontal:
            fig = go.Figure(
                data=[
                    go.Bar(
                        y=sorted_df["能力次元"],
                        x=sorted_df["スコア"],
                        orientation="h",
                        marker=dict(
                            color=sorted_df["スコア"],
                            colorscale="viridis",
                            showscale=False,
                        ),
                        text=sorted_df["スコア"],
                        textposition="inside",
                        hovertemplate="<b>%{y}</b><br>スコア: %{x}/10<extra></extra>",
                    )
                ]
            )

            fig.update_layout(
                xaxis_title="スコア",
                yaxis_title="能力次元",
            )
        else:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=sorted_df["能力次元"],
                        y=sorted_df["スコア"],
                        marker=dict(
                            color=sorted_df["スコア"],
                            colorscale="viridis",
                            showscale=False,
                        ),
                        text=sorted_df["スコア"],
                        textposition="outside",
                        hovertemplate="<b>%{x}</b><br>スコア: %{y}/10<extra></extra>",
                    )
                ]
            )

            fig.update_layout(
                xaxis_title="能力次元", yaxis_title="スコア", xaxis_tickangle=-45
            )

        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=18, family=self.font_family)),
            yaxis=dict(range=[0, 10]),
            font=dict(family=self.font_family),
            showlegend=False,
        )

        return fig

    def create_comparison_chart(
        self,
        scores_df_list: List[pd.DataFrame],
        labels: List[str],
        title: str = "能力スコア 比較",
    ) -> go.Figure:
        """
        Create a comparison radar chart for multiple score sets.

        Args:
            scores_df_list: List of DataFrames with capability scores
            labels: Labels for each dataset
            title: Chart title

        Returns:
            Plotly figure object
        """
        fig = go.Figure()

        colors = [
            self.color_palette["primary"],
            self.color_palette["secondary"],
            self.color_palette["success"],
            self.color_palette["warning"],
        ]

        for i, (scores_df, label) in enumerate(zip(scores_df_list, labels)):
            dimensions = scores_df["能力次元"].tolist()
            scores = scores_df["スコア"].tolist()

            # Close the radar chart
            dimensions_closed = dimensions + [dimensions[0]]
            scores_closed = scores + [scores[0]]

            color = colors[i % len(colors)]

            fig.add_trace(
                go.Scatterpolar(
                    r=scores_closed,
                    theta=dimensions_closed,
                    fill="toself",
                    fillcolor=f"{color}20",
                    line=dict(color=color, width=2),
                    marker=dict(color=color, size=6),
                    name=label,
                    hovertemplate=f"<b>{label}</b><br><b>%{{theta}}</b><br>スコア: %{{r}}/10<extra></extra>",
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickmode="linear",
                    tick0=0,
                    dtick=2,
                    gridcolor="lightgray",
                    gridwidth=1,
                ),
                angularaxis=dict(
                    tickfont=dict(size=12, family=self.font_family),
                    gridcolor="lightgray",
                    gridwidth=1,
                ),
            ),
            title=dict(text=title, x=0.5, font=dict(size=18, family=self.font_family)),
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            font=dict(family=self.font_family),
        )

        return fig

    def create_distribution_chart(self, scores_df: pd.DataFrame) -> go.Figure:
        """
        Create a distribution chart showing score distribution.

        Args:
            scores_df: DataFrame with capability scores

        Returns:
            Plotly figure object
        """
        scores = scores_df["スコア"].values

        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("スコア分布", "ボックスプロット"),
            vertical_spacing=0.15,
        )

        # Histogram
        fig.add_trace(
            go.Histogram(
                x=scores,
                nbinsx=10,
                marker=dict(color=self.color_palette["primary"], opacity=0.7),
                name="頻度",
            ),
            row=1,
            col=1,
        )

        # Box plot
        fig.add_trace(
            go.Box(
                y=scores, marker=dict(color=self.color_palette["primary"]), name="分布"
            ),
            row=2,
            col=1,
        )

        fig.update_layout(
            title=dict(
                text="能力スコア 分布分析",
                x=0.5,
                font=dict(size=18, family=self.font_family),
            ),
            showlegend=False,
            font=dict(family=self.font_family),
        )

        fig.update_xaxes(title_text="スコア", row=1, col=1)
        fig.update_yaxes(title_text="頻度", row=1, col=1)
        fig.update_yaxes(title_text="スコア", row=2, col=1)

        return fig

    def create_summary_metrics_chart(self, statistics: Dict[str, float]) -> go.Figure:
        """
        Create a chart showing summary statistics.

        Args:
            statistics: Dictionary with statistical measures

        Returns:
            Plotly figure object
        """
        metrics = list(statistics.keys())
        values = list(statistics.values())

        fig = go.Figure(
            data=[
                go.Bar(
                    x=metrics,
                    y=values,
                    marker=dict(color=values, colorscale="plasma", showscale=False),
                    text=[f"{v:.2f}" for v in values],
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>値: %{y:.2f}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text="統計サマリー", x=0.5, font=dict(size=18, family=self.font_family)
            ),
            xaxis_title="統計指標",
            yaxis_title="値",
            xaxis_tickangle=-45,
            font=dict(family=self.font_family),
            showlegend=False,
        )

        return fig
