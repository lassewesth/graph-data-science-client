from typing import Any, Dict, List

from ..error.illegal_attr_checker import IllegalAttrChecker
from ..error.uncallable_namespace import UncallableNamespace
from ..graph.graph_object import Graph
from ..query_runner.query_runner import QueryRunner


class UtilProcRunner(UncallableNamespace, IllegalAttrChecker):
    def __init__(self, query_runner: QueryRunner, namespace: str):
        self._query_runner = query_runner
        self._namespace = namespace

    def asNode(self, node_id: int) -> Dict[str, Any]:
        self._namespace += ".asNode"
        result = self._query_runner.run_query(
            f"RETURN {self._namespace}({node_id}) AS node"
        )

        return result[0]["node"]  # type: ignore

    def asNodes(self, node_ids: List[int]) -> List[Dict[str, Any]]:
        self._namespace += ".asNodes"
        result = self._query_runner.run_query(
            f"RETURN {self._namespace}({node_ids}) AS nodes"
        )

        return result[0]["nodes"]  # type: ignore

    def nodeProperty(
        self, G: Graph, node_id: int, property_key: str, node_label: str = "*"
    ) -> Any:
        self._namespace += ".nodeProperty"

        query = f"RETURN {self._namespace}($graph_name, $node_id, $property_key, $node_label) as property"
        params = {
            "graph_name": G.name(),
            "node_id": node_id,
            "property_key": property_key,
            "node_label": node_label,
        }
        result = self._query_runner.run_query(query, params)

        return result[0]["property"]
