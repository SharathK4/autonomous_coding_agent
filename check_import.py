# check_import.py
import sys
import os

print("--- Starting Import Check ---")

# 1. Define the exact path we need for the import to work
# This path goes from this script's location into src/vendor/blender-mcp
vendor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'vendor', 'blender-mcp'))

print(f"\n[Step 1] Calculated Path to Blender-MCP Package: {vendor_path}")

# 2. Check if this crucial directory actually exists on your disk
if not os.path.isdir(vendor_path):
    print(f"\n[FATAL ERROR at Step 2] The directory does not exist! -> {vendor_path}")
    print("This is the root cause. The 'blender-mcp' submodule folder is not present at this location.")
    print("Please run the 'git submodule update --init --recursive' command again and verify the folder is created.")
    sys.exit(1)
else:
    print("[Step 2] Directory check PASSED.")

# 3. Check for the inner package folder
package_path = os.path.join(vendor_path, 'blender_mcp')
if not os.path.isdir(package_path):
    print(f"\n[FATAL ERROR at Step 3] The inner package folder is MISSING! -> {package_path}")
    print("This means the submodule is likely not initialized correctly.")
    print("The folder structure must be: .../vendor/blender-mcp/blender_mcp/")
    sys.exit(1)
else:
     print(f"[Step 3] Inner package folder '{package_path}' found. PASSED.")


# 4. Add the calculated path to Python's system path
if vendor_path not in sys.path:
    sys.path.append(vendor_path)
print("[Step 4] Path has been added to sys.path for this run.")


# 5. NOW, we attempt the import that has been failing
print("\n[Step 5] Attempting to import 'blender_mcp.client'...")
try:
    from blender_mcp.client import BlenderClient
    print("\n[--- SUCCESS! ---]")
    print("'BlenderClient' was imported correctly.")
    print("This confirms your file structure and submodule are now correct.")
    print("The main agent application should now be able to run without the import error.")

except ModuleNotFoundError as e:
    print(f"\n[--- FATAL ERROR at Step 5 ---]")
    print("The import failed even though the correct path was added.")
    print(f"Original Python error: {e}")
    print("\nThis means the issue is with the contents of the 'blender-mcp' folder itself.")
    print("Please re-run the git submodule commands to ensure a clean download.")

except Exception as e:
    print(f"\n[--- UNEXPECTED FATAL ERROR at Step 5 ---]")
    print(f"An unexpected error occurred: {e}")

print("\n--- Check Complete ---")