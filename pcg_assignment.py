"""
PCG Assignment helpers for Unreal MCP Server.
Provides tools to assign assets to spawner nodes and graphs to volumes.
"""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


def set_spawner_assets_handler(
    unreal_connection,
    graph_name: str,
    node_id: str,
    assets: List[str],
    weights: Optional[List[float]] = None
) -> Dict[str, Any]:
    """
    Set which assets a spawner node should use, with optional probability weights.

    Args:
        unreal_connection: The Unreal Engine connection object
        graph_name: Target PCG graph name
        node_id: Spawner node ID
        assets: List of asset names/paths to spawn (e.g., ["Oak_Tree", "Pine_Tree"])
        weights: Optional probability weights (e.g., [0.5, 0.5]). Must match assets length.

    Returns:
        Dictionary with assignment result
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}
        if not node_id or not isinstance(node_id, str):
            return {"success": False, "message": "node_id is required and must be a non-empty string"}
        if not assets or not isinstance(assets, list):
            return {"success": False, "message": "assets is required and must be a non-empty list"}

        params = {
            "graph_name": graph_name,
            "node_id": node_id,
            "assets": assets
        }

        if weights is not None:
            if not isinstance(weights, list):
                return {"success": False, "message": "weights must be a list of float values"}
            if len(weights) != len(assets):
                return {
                    "success": False,
                    "message": f"weights length ({len(weights)}) must match assets length ({len(assets)})"
                }
            # Validate all weights are numeric and non-negative
            for i, w in enumerate(weights):
                if not isinstance(w, (int, float)) or w < 0:
                    return {
                        "success": False,
                        "message": f"Weight at index {i} must be a non-negative number, got {w}"
                    }
            params["weights"] = [float(w) for w in weights]

        logger.info(
            f"Setting {len(assets)} assets on spawner '{node_id}' in graph '{graph_name}'"
        )
        response = unreal_connection.send_command("set_spawner_assets", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"set_spawner_assets_handler error: {e}")
        return {"success": False, "message": str(e)}


def assign_pcg_graph_to_volume_handler(
    unreal_connection,
    volume_name: str,
    graph_name: str
) -> Dict[str, Any]:
    """
    Assign a PCG graph to a volume so the graph generates content within that volume.

    Args:
        unreal_connection: The Unreal Engine connection object
        volume_name: Name of the target volume
        graph_name: Name of the PCG graph to assign

    Returns:
        Dictionary with assignment result
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not volume_name or not isinstance(volume_name, str):
            return {"success": False, "message": "volume_name is required and must be a non-empty string"}
        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}

        params = {
            "volume_name": volume_name,
            "graph_name": graph_name
        }

        logger.info(f"Assigning PCG graph '{graph_name}' to volume '{volume_name}'")
        response = unreal_connection.send_command("assign_pcg_graph_to_volume", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"assign_pcg_graph_to_volume_handler error: {e}")
        return {"success": False, "message": str(e)}
