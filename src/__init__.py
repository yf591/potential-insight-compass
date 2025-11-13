"""
Potential Insight Compass (PIC) - Source Code Package

AI-powered career counseling support system that analyzes interview records
and counseling notes to discover hidden strengths and career potentials.
"""

__version__ = "1.0.0"
__author__ = "PIC Development Team"
__email__ = "info@pic-system.com"

from .ai_analyzer import AIAnalyzer
from .data_processor import DataProcessor
from .visualizer import ChartVisualizer

__all__ = ["AIAnalyzer", "DataProcessor", "ChartVisualizer"]
