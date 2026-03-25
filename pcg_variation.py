"""
PCG Variation helpers for Unreal MCP Server.
Provides tools to add random variation to PCG-generated content.
"""
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Supported variation properties
SUPPORTED_PROPERTIES = {"scale", "rotation", "color"}


def create_random_variation_handler(
    unreal_connection,
    graph_name: str,
    property: str,
    variation_range: Dict[str, float]
) -> Dict[str, Any]:
    """
    Add random variation to a property in a PCG graph.

    Args:
        unreal_connection: The Unreal Engine connection object
        graph_name: Target PCG graph name
        property: Property to vary ("scale", "rotation", "color")
        variation_range: Range dict {"min": 0.8, "max": 1.2}

    Returns:
        Dictionary with variation setup result
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}
        if not property or not isinstance(property, str):
            return {"success": False, "message": "property is required and must be a non-empty string"}

        # Validate variation_range
        if not isinstance(variation_range, dict):
            return {"success": False, "message": "variation_range must be a dict with 'min' and 'max' keys"}
        if "min" not in variation_range or "max" not in variation_range:
            return {"success": False, "message": "variation_range must contain both 'min' and 'max' keys"}

        min_val = variation_range["min"]
        max_val = variation_range["max"]

        if not isinstance(min_val, (int, float)) or not isinstance(max_val, (int, float)):
            return {"success": False, "message": "'min' and 'max' must be numeric values"}
        if min_val > max_val:
            return {
                "success": False,
                "message": f"'min' ({min_val}) must be less than or equal to 'max' ({max_val})"
            }

        # Warn if property is not in the typical set
        if property not in SUPPORTED_PROPERTIES:
            logger.warning(
                f"Property '{property}' is not in the standard set {SUPPORTED_PROPERTIES}. "
                f"It may still be valid for custom PCG setups."
            )

        params = {
            "graph_name": graph_name,
            "property": property,
            "variation_range": {
                "min": float(min_val),
                "max": float(max_val)
            }
        }

        logger.info(
            f"Creating random variation for '{property}' in graph '{graph_name}': "
            f"[{min_val}, {max_val}]"
        )
        response = unreal_connection.send_command("create_random_variation", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"create_random_variation_handler error: {e}")
        return {"success": False, "message": str(e)}
