# src/controllers/blender_controller.py

import socket
import json
import time

class BlenderController:
    """A simple RPC client to send commands to our Blender server."""
    def __init__(self, host='127.0.0.1', port=8006):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self) -> str:
        """Connects to the Blender server."""
        try:
            print(f"CONTROLLER: Attempting to connect to Blender on {self.host}:{self.port}...")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5) # 5-second timeout
            self.client_socket.connect((self.host, self.port))
            print("CONTROLLER: Connection successful.")
            return "Successfully connected to Blender."
        except ConnectionRefusedError:
            error_message = f"Error: Connection refused. Is Blender running with the server script?"
            print(f"CONTROLLER: {error_message}")
            self.client_socket = None
            return error_message
        except Exception as e:
            error_message = f"An unknown error occurred during connection: {e}"
            print(f"CONTROLLER: {error_message}")
            self.client_socket = None
            return error_message

    def disconnect(self):
        """Closes the connection."""
        if self.client_socket:
            print("CONTROLLER: Disconnecting from Blender.")
            self.client_socket.close()
        self.client_socket = None

    def execute_command(self, command: str) -> str:
        """Sends a command and gets a response."""
        if not self.client_socket:
            connection_result = self.connect()
            if "Error" in connection_result:
                return connection_result

        try:
            print(f"CONTROLLER: Sending command to Blender:\n---\n{command}\n---")
            self.client_socket.sendall(command.encode('utf-8'))
            
            # Wait for and receive the response
            response_data = self.client_socket.recv(4096).decode('utf-8')
            response_dict = json.loads(response_data)

            result = f"Command executed. stdout: {response_dict.get('stdout')}, stderr: {response_dict.get('stderr')}"
            print(f"CONTROLLER: Received response: {result}")
            return result
        except Exception as e:
            error_msg = f"An error occurred while sending command: {e}"
            self.disconnect() # Disconnect on error
            return error_msg

# Instantiate the single controller
blender_controller = BlenderController()