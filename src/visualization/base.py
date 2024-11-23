from dataclasses import dataclass
from typing import Optional

@dataclass
class VisualizationResult:
    """Class to hold visualization results and metrics"""
    figure: Optional[object] = None
    metrics: dict = None
    insights: list[str] = None
