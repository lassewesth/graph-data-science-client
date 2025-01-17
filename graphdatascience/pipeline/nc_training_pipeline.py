from typing import Any, Dict, List, Union

from ..model.node_classification_model import NCModel
from ..pipeline.training_pipeline import TrainingPipeline
from ..query_runner.query_runner import QueryRunner, Row


class NCTrainingPipeline(TrainingPipeline):
    def selectFeatures(self, node_properties: Union[str, List[str]]) -> Row:
        query = (
            f"{self._query_prefix()}selectFeatures($pipeline_name, $node_properties)"
        )
        params = {"pipeline_name": self.name(), "node_properties": node_properties}

        return self._query_runner.run_query(query, params)[0]

    def feature_properties(self) -> List[Dict[str, Any]]:
        return self._list_info()["pipelineInfo"]["featurePipeline"]["featureProperties"]  # type: ignore

    def _query_prefix(self) -> str:
        return "CALL gds.beta.pipeline.nodeClassification."

    def _create_trained_model(self, name: str, query_runner: QueryRunner) -> NCModel:
        return NCModel(name, query_runner)
