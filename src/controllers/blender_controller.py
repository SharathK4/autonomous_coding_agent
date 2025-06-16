import socket
import json
import time

class BlenderController:
    """
    A simple RPC client to send commands to our Blender server.
    
    """
    def __init__(self, host='127.0.0.1', port=8006):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self) -> str:
        """Connects to the Blender server."""
        print(f"CONTROLLER: Attempting to connect to Blender on {self.host}:{self.port}...")
        
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5) 
        self.client_socket.connect((self.host, self.port))
        
        print("CONTROLLER: Connection successful.")
        return "Successfully connected to Blender."

    def disconnect(self):
        """Closes the connection."""
        if self.client_socket:
            print("CONTROLLER: Disconnecting from Blender.")
            self.client_socket.close()
        self.client_socket = None

    def execute_command(self, command: str) -> str:
        """
        Sends a command and gets a response.
        This will crash if the connection is lost or the response is invalid.
        """
       
        if not self.client_socket:
            self.connect()

        
        print(f"CONTROLLER: Sending command to Blender:\n---\n{command}\n---")
        self.client_socket.sendall(command.encode('utf-8'))
        
        
        response_data = self.client_socket.recv(4096).decode('utf-8')
        
        
        response_dict = json.loads(response_data)

        
        result = f"Command executed. stdout: {response_dict.get('stdout')}, stderr: {response_dict.get('stderr')}"
        print(f"CONTROLLER: Received response: {result}")
        return result



blender_controller = BlenderController()