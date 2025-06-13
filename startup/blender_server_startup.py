# startup/blender_server_startup.py

import bpy
import socket
import threading
import traceback
import json
from io import StringIO
import sys

# --- SERVER IMPLEMENTATION ---
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8006         # Port to listen on

def execute_in_main_thread(code_to_exec):
    """
    Executes code in Blender's main thread to avoid context issues.
    Captures print statements (stdout) and errors (stderr).
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_stdout = sys.stdout = StringIO()
    redirected_stderr = sys.stderr = StringIO()
    
    try:
        # The compiled code is scheduled to be executed in the next main loop iteration
        def exec_code():
            exec(code_to_exec, globals())
        bpy.app.timers.register(exec_code, first_interval=0.1)
        
    except Exception:
        traceback.print_exc(file=sys.stderr)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
    return {
        "stdout": redirected_stdout.getvalue(),
        "stderr": redirected_stderr.getvalue(),
    }


def handle_client(conn, addr):
    print(f"[Server] Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(4096)  # Receive data in chunks
            if not data:
                break
            
            command = data.decode('utf-8')
            print(f"[Server] Received command:\n---\n{command}\n---")
            
            # This is not thread-safe, so we must schedule it for the main thread
            response_data = execute_in_main_thread(command)
            
            response_json = json.dumps(response_data)
            conn.sendall(response_json.encode('utf-8'))
    print(f"[Server] Connection with {addr} closed.")


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[Server] Blender RPC Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        # Start a new thread for each client to handle connections
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

# --- BLENDER OPERATOR TO START THE SERVER ---
class RunRPCServerOperator(bpy.types.Operator):
    bl_idname = "wm.run_rpc_server"
    bl_label = "Run RPC Server"
    
    _thread = None

    def invoke(self, context, event):
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=run_server)
            self._thread.daemon = True
            self._thread.start()
            print("RPC Server thread started.")
        return {'FINISHED'}

bpy.utils.register_class(RunRPCServerOperator)
# Immediately start the server when the script is run
bpy.ops.wm.run_rpc_server('INVOKE_DEFAULT')