"""
PCG Execution and Verification helpers for Unreal MCP Server.
Provides tools to execute PCG graphs, inspect logs, analyze output, and capture screenshots.
"""
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Valid enum values for validation
VALID_DETAIL_LEVELS = {"basic", "verbose", "debug"}
VALID_LOG_LEVELS = {"info", "warning", "error"}
VALID_CAMERA_ANGLES = {"top", "perspective", "walkthrough"}
VALID_METRICS = {"count", "density", "variety", "distribution"}


def execute_pcg_handler(
    unreal_connection,
    volume_name: Optional[str] = None,
    graph_name: Optional[str] = None,
    run_async: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Execute a PCG graph to generate procedural content.

    Args:
        unreal_connection: The Unreal Engine connection object
        volume_name: Optional specific volume to generate
        graph_name: Optional specific graph to run
        run_async: Optional flag to run generation in background

    Returns:
        Dictionary with execution result and stats
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        params = {}
        if volume_name is not None:
            params["volume_name"] = volume_name
        if graph_name is not None:
            params["graph_name"] = graph_name
        if run_async is not None:
            params["async"] = bool(run_async)

        target = graph_name or volume_name or "all"
        logger.info(f"Executing PCG generation for: {target} (async={run_async or False})")
        response = unreal_connection.send_command("execute_pcg", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"execute_pcg_handler error: {e}")
        return {"success": False, "message": str(e)}


def get_pcg_execution_log_handler(
    unreal_connection,
    graph_name: str,
    detail_level: Optional[str] = None,
    filter_by_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve the execution log from a PCG graph run.

    Args:
        unreal_connection: The Unreal Engine connection object
        graph_name: Graph to inspect (required)
        detail_level: Log detail level — "basic", "verbose", or "debug"
        filter_by_level: Filter logs — "info", "warning", or "error"

    Returns:
        Dictionary containing the execution log entries
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not graph_name or not isinstance(graph_name, str):
            return {"success": False, "message": "graph_name is required and must be a non-empty string"}

        params = {"graph_name": graph_name}

        if detail_level is not None:
            detail_level = detail_level.lower()
            if detail_level not in VALID_DETAIL_LEVELS:
                return {
                    "success": False,
                    "message": f"detail_level must be one of {sorted(VALID_DETAIL_LEVELS)}, got '{detail_level}'"
                }
            params["detail_level"] = detail_level

        if filter_by_level is not None:
            filter_by_level = filter_by_level.lower()
            if filter_by_level not in VALID_LOG_LEVELS:
                return {
                    "success": False,
                    "message": f"filter_by_level must be one of {sorted(VALID_LOG_LEVELS)}, got '{filter_by_level}'"
                }
            params["filter_by_level"] = filter_by_level

        logger.info(
            f"Getting execution log for graph '{graph_name}' "
            f"(detail={detail_level or 'default'}, filter={filter_by_level or 'none'})"
        )
        response = unreal_connection.send_command("get_pcg_execution_log", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"get_pcg_execution_log_handler error: {e}")
        return {"success": False, "message": str(e)}


def analyze_pcg_output_handler(
    unreal_connection,
    volume_name: str,
    metrics: List[str]
) -> Dict[str, Any]:
    """
    Analyze the output of a PCG generation within a volume.

    Args:
        unreal_connection: The Unreal Engine connection object
        volume_name: Volume to analyze (required)
        metrics: List of metrics to compute (required),
                 e.g., ["count", "density", "variety", "distribution"]

    Returns:
        Dictionary with computed metrics
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not volume_name or not isinstance(volume_name, str):
            return {"success": False, "message": "volume_name is required and must be a non-empty string"}
        if not metrics or not isinstance(metrics, list):
            return {"success": False, "message": "metrics is required and must be a non-empty list"}

        # Validate metric names
        invalid_metrics = [m for m in metrics if m.lower() not in VALID_METRICS]
        if invalid_metrics:
            return {
                "success": False,
                "message": (
                    f"Invalid metrics: {invalid_metrics}. "
                    f"Valid metrics are: {sorted(VALID_METRICS)}"
                )
            }

        params = {
            "volume_name": volume_name,
            "metrics": [m.lower() for m in metrics]
        }

        logger.info(f"Analyzing PCG output in volume '{volume_name}': metrics={metrics}")
        response = unreal_connection.send_command("analyze_pcg_output", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"analyze_pcg_output_handler error: {e}")
        return {"success": False, "message": str(e)}


def screenshot_pcg_result_handler(
    unreal_connection,
    volume_name: str,
    camera_angle: Optional[str] = None
) -> Dict[str, Any]:
    """
    Capture a screenshot of PCG-generated content within a volume.

    Args:
        unreal_connection: The Unreal Engine connection object
        volume_name: Volume to capture (required)
        camera_angle: Camera perspective — "top", "perspective", or "walkthrough"

    Returns:
        Dictionary with screenshot path/data
    """
    try:
        if not unreal_connection:
            return {"success": False, "message": "No Unreal connection provided"}

        if not volume_name or not isinstance(volume_name, str):
            return {"success": False, "message": "volume_name is required and must be a non-empty string"}

        params = {"volume_name": volume_name}

        if camera_angle is not None:
            camera_angle = camera_angle.lower()
            if camera_angle not in VALID_CAMERA_ANGLES:
                return {
                    "success": False,
                    "message": f"camera_angle must be one of {sorted(VALID_CAMERA_ANGLES)}, got '{camera_angle}'"
                }
            params["camera_angle"] = camera_angle

        logger.info(f"Capturing screenshot of volume '{volume_name}' (angle={camera_angle or 'default'})")
        response = unreal_connection.send_command("screenshot_pcg_result", params)
        return response or {"success": False, "message": "No response from Unreal"}

    except Exception as e:
        logger.error(f"screenshot_pcg_result_handler error: {e}")
        return {"success": False, "message": str(e)}
