from typing import Tuple

from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
from ..query_runner.query_runner import QueryRunner, Row
from .nc_training_pipeline import NCTrainingPipeline


class NCPipelineCreateRunner(UncallableNamespace, IllegalAttrChecker):
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    def create(self, name: str) -> Tuple[NCTrainingPipeline, Row]:
        self._namespace += ".create"

        query = f"CALL {self._namespace}($name)"
        params = {"name": name}
        result = self._query_runner.run_query(query, params)[0]

        return NCTrainingPipeline(name, self._query_runner), result
