# src/controllers/blender_controller.py

import sys
import os
import time

# --- This logic MUST be at the top ---
# It adds the correct 'src' directory from the submodule to Python's path
# ✅ FINAL CORRECTION: Added '/src' to the end of the path.
vendor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vendor', 'blender-mcp', 'src'))
if vendor_path not in sys.path:
    sys.path.append(vendor_path)

# This try/except block is our main guard against installation issues
try:
    from blender_mcp.client import BlenderClient
except ImportError as e:
    print(f"FATAL: Failed to import BlenderClient. This likely means the git submodule is not initialized correctly.")
    print(f"Please run 'git submodule update --init --recursive' in your terminal and try again.")
    print(f"Original error: {e}")
    # We exit here because the controller is unusable without the client.
    sys.exit(1)


class BlenderController:
    """
    Manages a persistent connection to a live Blender instance
    running the MCP server.
    """
    def __init__(self, port=8006):
        self.port = port
        self.client = None

    def connect(self) -> str:
        """Establishes a connection to the Blender server."""
        if self.client and self.client.is_connected():
            return "Already connected to Blender."
        try:
            print(f"CONTROLLER: Attempting to connect to Blender on port {self.port}...")
            self.client = BlenderClient(self.port)
            time.sleep(1)
            if not self.client.is_connected():
                 raise ConnectionRefusedError
            print("CONTROLLER: Connection successful.")
            return "Successfully connected to Blender."
        except ConnectionRefusedError:
            error_message = (
                f"Error: Connection to Blender on port {self.port} refused. "
                "Is Blender running with the 'blender_server_startup.py' script? "
                "Please start it first."
            )
            print(f"CONTROLLER: {error_message}")
            self.client = None
            return error_message
        except Exception as e:
            print(f"CONTROLLER: An unknown error occurred during connection: {e}")
            self.client = None
            return f"An unknown error occurred: {e}"

    def disconnect(self):
        """Closes the connection."""
        if self.client and self.client.is_connected():
            print("CONTROLLER: Disconnecting from Blender.")
            self.client.close()
        self.client = None

    def execute_command(self, command: str) -> str:
        """Sends a string of Python code to be executed inside Blender."""
        if not self.client or not self.client.is_connected():
            connection_result = self.connect()
            if "Error" in connection_result:
                return connection_result

        print(f"CONTROLLER: Sending command to Blender:\n---\n{command}\n---")
        try:
            response = self.client.send(command)
            result = f"Command executed. stdout: {response.get('stdout')}, stderr: {response.get('stderr')}"
            print(f"CONTROLLER: Received response: {result}")
            return result
        except Exception as e:
            error_msg = f"An error occurred while sending command: {e}"
            print(f"CONTROLLER: {error_msg}")
            return error_msg

# Instantiate a single controller to be used throughout the application
blender_controller = BlenderController()