from langchain.tools import tool
from src.controllers.blender_controller import blender_controller

@tool
def connect_to_blender() -> str:
    """
    Establishes a connection with the running Blender instance.
    This should be the first step in any Blender-related task.
    """
    return blender_controller.connect()

@tool
def send_blender_command(python_code: str) -> str:
    """
    Sends a string of Python code to be executed by the connected Blender instance.
    Use this to perform all actions like creating objects, applying materials, etc.
    The code should be valid Blender Python API (`bpy`) code.
    Args:
        python_code (str): A string containing the Python code to execute in Blender.
    """
    return blender_controller.execute_command(python_code)

@tool
def disconnect_from_blender() -> str:
    """Closes the connection to the Blender instance when the task is complete."""
    blender_controller.disconnect()
    return "Disconnected from Blender."

