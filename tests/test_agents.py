import json

import pandas as pd
import pytest

from agents.state import AgentState
from agents.data_analysis_agent import data_analysis_agent
from agents.anomaly_detection_agent import anomaly_detection_agent
from agents.visualization_agent import visualization_agent


@pytest.fixture
def sample_df() -> pd.DataFrame:
    import numpy as np
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=50, freq="D"),
        "region": rng.choice(["North", "South", "East", "West"], 50),
        "revenue": rng.uniform(10_000, 100_000, 50),
        "units": rng.integers(10, 500, 50),
    })


@pytest.fixture
def base_state(sample_df) -> AgentState:
    return AgentState(
        user_query="Why did revenue drop last month?",
        session_id="test-session-001",
        dataset_ids=["ds1"],
        dataframes={"sales": sample_df},
        dataset_schemas={
            "sales": {
                "columns": sample_df.columns.tolist(),
                "dtypes": sample_df.dtypes.astype(str).to_dict(),
            }
        },
        errors=[],
        metadata={},
    )


class TestDataAnalysisAgent:
    def test_returns_analysis_results(self, base_state):
        result = data_analysis_agent(base_state)
        assert "analysis_results" in result
        assert "sales" in result["analysis_results"]

    def test_kpi_extraction(self, base_state):
        result = data_analysis_agent(base_state)
        assert "kpi_summary" in result
        assert isinstance(result["kpi_summary"], dict)

    def test_no_dataframes(self):
        state = AgentState(user_query="test", session_id="s", errors=[])
        result = data_analysis_agent(state)
        assert result["errors"]


class TestAnomalyDetectionAgent:
    def test_detects_anomalies(self, base_state):
        base_state["dataframes"]["sales"].loc[0, "revenue"] = 9_999_999
        result = anomaly_detection_agent(base_state)
        assert "anomalies" in result
        assert isinstance(result["anomalies"], list)

    def test_explanations_generated(self, base_state):
        result = anomaly_detection_agent(base_state)
        assert "anomaly_explanations" in result


class TestVisualizationAgent:
    def test_charts_generated(self, base_state):
        state = data_analysis_agent(base_state)
        result = visualization_agent(state)
        assert "chart_specs" in result
        assert len(result["chart_specs"]) > 0

    def test_chart_types_logged(self, base_state):
        state = data_analysis_agent(base_state)
        result = visualization_agent(state)
        assert "chart_types_chosen" in result
        assert len(result["chart_types_chosen"]) == len(result["chart_specs"])

    def test_visualization_agent_returns_json_serialized_charts(self, sample_df):
        state = AgentState(
            user_query="Test chart generation",
            session_id="test-session-visualization",
            dataframes={"sales": sample_df},
            dataset_ids=["sales"],
            dataset_schemas={"sales": {
                "columns": sample_df.columns.tolist(),
                "dtypes": sample_df.dtypes.astype(str).to_dict(),
            }},
            errors=[],
            metadata={},
        )

        result = visualization_agent(state)
        chart_specs = result.get("chart_specs", [])
        assert chart_specs, "Expected at least one serialized chart"
        assert isinstance(chart_specs[0], dict)

        import plotly.io as pio
        json_chart = json.dumps(chart_specs[0])
        fig = pio.from_json(json_chart)
        assert fig.data, "Deserialized Plotly figure should contain traces"
