"""
PCG Setup helpers for Unreal MCP Server.
Provides tools to create PCG graphs and volumes in Unreal Engine.
"""
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def create_pcg_graph_handler(
    unreal_connection,
    name: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new PCG (Procedural Content Generation) graph asset.

    Args:
        unreal_connection: The Unreal Engine connection object
        name: Name of the PCG graph (e.g., "MegaForest")
        description: Optional description of what this graph does

    Returns:
        Dictionary with the created graph info
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not name or not isinstance(name, str):
            return {"success": False, "message": "name is required and must be a non-empty string"}

        params = {"name": name}
        if description is not None:
            params["description"] = description

        logger.info(f"Creating PCG graph: '{name}'")
        response = unreal_connection.send_command("create_pcg_graph", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"create_pcg_graph_handler error: {e}")
        return {"success": False, "message": str(e)}


def create_pcg_volume_handler(
    unreal_connection,
    name: str,
    location: Dict[str, float],
    size: Dict[str, float],
    rotation: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Create a PCG volume in the level that defines the generation area.

    Args:
        unreal_connection: The Unreal Engine connection object
        name: Name of the volume (e.g., "ForestArea")
        location: Position dict {"x": 0, "y": 0, "z": 0}
        size: Extent dict {"x": 10000, "y": 10000, "z": 5000}
        rotation: Optional rotation dict {"roll": 0, "pitch": 0, "yaw": 0}

    Returns:
        Dictionary with the created volume info
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not name or not isinstance(name, str):
            return {"success": False, "message": "name is required and must be a non-empty string"}

        # Validate location dict
        if not isinstance(location, dict) or not all(k in location for k in ("x", "y", "z")):
            return {"success": False, "message": "location must be a dict with keys 'x', 'y', 'z'"}

        # Validate size dict
        if not isinstance(size, dict) or not all(k in size for k in ("x", "y", "z")):
            return {"success": False, "message": "size must be a dict with keys 'x', 'y', 'z'"}

        params = {
            "name": name,
            "location": location,
            "size": size
        }

        if rotation is not None:
            if not isinstance(rotation, dict):
                return {"success": False, "message": "rotation must be a dict with keys 'roll', 'pitch', 'yaw'"}
            params["rotation"] = rotation

        logger.info(f"Creating PCG volume: '{name}' at ({location['x']}, {location['y']}, {location['z']})")
        response = unreal_connection.send_command("create_pcg_volume", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"create_pcg_volume_handler error: {e}")
        return {"success": False, "message": str(e)}
