from typing import Optional

from ..error.client_only_endpoint import client_only_endpoint
from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
from ..query_runner.query_runner import QueryResult, QueryRunner, Row
from .lp_pipeline_create_runner import LPPipelineCreateRunner
from .lp_training_pipeline import LPTrainingPipeline
from .nc_pipeline_create_runner import NCPipelineCreateRunner
from .nc_training_pipeline import NCTrainingPipeline
from .training_pipeline import TrainingPipeline


class PipelineProcRunner(UncallableNamespace, IllegalAttrChecker):
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    @property
    def linkPrediction(self) -> LPPipelineCreateRunner:
        return LPPipelineCreateRunner(
            self._query_runner, f"{self._namespace}.linkPrediction"
        )

    @property
    def nodeClassification(self) -> NCPipelineCreateRunner:
        return NCPipelineCreateRunner(
            self._query_runner, f"{self._namespace}.nodeClassification"
        )

    def list(self, pipeline: Optional[TrainingPipeline] = None) -> QueryResult:
        self._namespace += ".list"

        if pipeline:
            query = f"CALL {self._namespace}($pipeline_name)"
            params = {"pipeline_name": pipeline.name()}
        else:
            query = f"CALL {self._namespace}()"
            params = {}

        return self._query_runner.run_query(query, params)

    def exists(self, pipeline_name: str) -> Row:
        self._namespace += ".exists"

        query = f"CALL {self._namespace}($pipeline_name)"
        params = {"pipeline_name": pipeline_name}

        return self._query_runner.run_query(query, params)[0]

    def drop(self, pipeline: TrainingPipeline) -> Row:
        self._namespace += ".drop"

        query = f"CALL {self._namespace}($pipeline_name)"
        params = {"pipeline_name": pipeline.name()}

        return self._query_runner.run_query(query, params)[0]

    @client_only_endpoint("gds.pipeline")
    def get(self, pipeline_name: str) -> TrainingPipeline:
        query = "CALL gds.beta.pipeline.list($pipeline_name)"
        params = {"pipeline_name": pipeline_name}
        result = self._query_runner.run_query(query, params)

        if len(result) == 0:
            raise ValueError(f"No pipeline named '{pipeline_name}' exists")

        pipeline_type = result[0]["pipelineType"]
        return self._resolve_pipeline(pipeline_type, pipeline_name)

    def _resolve_pipeline(
        self, pipeline_type: str, pipeline_name: str
    ) -> TrainingPipeline:
        if pipeline_type == "Node classification training pipeline":
            return NCTrainingPipeline(pipeline_name, self._query_runner)
        elif pipeline_type == "Link prediction training pipeline":
            return LPTrainingPipeline(pipeline_name, self._query_runner)

        raise ValueError(f"Unknown model type encountered: '{pipeline_type}'")
