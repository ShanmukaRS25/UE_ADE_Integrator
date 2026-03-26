"""
PCG Node Creation helpers for Unreal MCP Server.
Provides tools to add and configure nodes within PCG graphs.
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Known PCG node types for validation hints (non-exhaustive)
KNOWN_NODE_TYPES = {
    "SurfaceSampler",
    "StaticMeshSpawner",
    "DensityFilter",
    "PointFilter",
    "TransformPoints",
    "BoundsModifier",
    "Difference",
    "Intersection",
    "Union",
    "CopyPoints",
    "MergePoints",
    "ProjectionOnSurface",
    "GetActorData",
    "AttributeNoise",
    "SplineSampler",
    "VolumeSampler",
}


def add_pcg_node_handler(
    unreal_connection,
    graph_name: str,
    node_type: str,
    position_x: int,
    position_y: int,
    node_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a new node to a PCG graph.

    Args:
        unreal_connection: The Unreal Engine connection object
        graph_name: Target PCG graph name
        node_type: Type of node (e.g., "SurfaceSampler", "StaticMeshSpawner")
        position_x: X coordinate in the graph editor
        position_y: Y coordinate in the graph editor
        node_name: Optional custom display name for the node

    Returns:
        Dictionary with the created node info including its node_id
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}
        if not node_type or not isinstance(node_type, str):
            return {"success": False, "message": "node_type is required and must be a non-empty string"}

        # Warn (but don't block) if node type is not in known list
        if node_type not in KNOWN_NODE_TYPES:
            logger.warning(
                f"Node type '{node_type}' is not in the known types list. "
                f"It may still be valid if it's a custom or plugin node type."
            )

        params = {
            "graph_name": graph_name,
            "node_type": node_type,
            "position_x": int(position_x),
            "position_y": int(position_y)
        }
        if node_name is not None:
            params["node_name"] = node_name

        logger.info(f"Adding PCG node '{node_type}' to graph '{graph_name}' at ({position_x}, {position_y})")
        response = unreal_connection.send_command("add_pcg_node", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"add_pcg_node_handler error: {e}")
        return {"success": False, "message": str(e)}


def set_pcg_node_property_handler(
    unreal_connection,
    graph_name: str,
    node_id: str,
    property_name: str,
    value: Any
) -> Dict[str, Any]:
    """
    Set a property on an existing PCG node.

    Args:
        unreal_connection: The Unreal Engine connection object
        graph_name: Target PCG graph name
        node_id: ID of the node to modify
        property_name: Name of the property to change
        value: New value for the property (any JSON-serializable type)

    Returns:
        Dictionary with updated property info
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}
        if not node_id or not isinstance(node_id, str):
            return {"success": False, "message": "node_id is required and must be a non-empty string"}
        if not property_name or not isinstance(property_name, str):
            return {"success": False, "message": "property_name is required and must be a non-empty string"}

        params = {
            "graph_name": graph_name,
            "node_id": node_id,
            "property_name": property_name,
            "value": value
        }

        logger.info(f"Setting property '{property_name}' on node '{node_id}' in graph '{graph_name}'")
        response = unreal_connection.send_command("set_pcg_node_property", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"set_pcg_node_property_handler error: {e}")
        return {"success": False, "message": str(e)}
