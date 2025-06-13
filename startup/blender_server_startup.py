# startup/blender_server_startup.py

import bpy
import sys
import os

# Add the vendor directory to Python's path so Blender can find blender-mcp
# This assumes the script is run from the project's root directory
vendor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'vendor'))
if vendor_path not in sys.path:
    sys.path.append(vendor_path)

try:
    from blender_mcp import server
    print("Blender MCP server module found.")
    
    # This class will be registered by Blender and run automatically
    class RunMCPServer(bpy.types.Operator):
        bl_idname = "wm.run_mcp_server"
        bl_label = "Run MCP Server"

        def modal(self, context, event):
            # This allows the operator to run without blocking the UI
            return {'PASS_THROUGH'}

        def invoke(self, context, event):
            print("Starting Blender MCP server on port 8006...")
            try:
                server.run_server(port=8006)
                print("MCP Server is running in the background.")
            except Exception as e:
                print(f"Failed to start MCP server: {e}")
            
            # Add this operator to the modal timer to keep it running
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

    # Register the operator so we can call it
    bpy.utils.register_class(RunMCPServer)
    # Immediately invoke the operator to start the server
    bpy.ops.wm.run_mcp_server('INVOKE_DEFAULT')

except ImportError:
    print("FATAL: Could not import blender_mcp.server.")
    print("Please ensure the submodule is correctly installed at 'src/vendor/blender-mcp'")