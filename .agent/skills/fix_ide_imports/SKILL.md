---
description: Automatically configure pyproject.toml for IDE/Pyrefly Import Resolution
---

This workflow detects your local `.venv` site-packages and updates `pyproject.toml` to fix "Cannot find module" errors.

1.  **Create the script `fix_ide.py`**:
    ```python
    import os
    import sys
    import glob

    def fix_imports():
        print("🔍 Detecting Python Environment...")
        
        # 1. Find .venv site-packages
        venv_path = os.path.join(os.getcwd(), ".venv")
        site_pkg = None
        
        if os.path.exists(venv_path):
            # Look for site-packages (e.g., .venv/lib/python3.9/site-packages)
            paths = glob.glob(os.path.join(venv_path, "lib", "python*", "site-packages"))
            if paths:
                site_pkg = os.path.relpath(paths[0], os.getcwd())
                print(f"✅ Found .venv site-packages: {site_pkg}")
        
        else:
            print("❌ No local .venv found. Are you using uv/poetry/venv?")
            return

        # 2. Append to pyproject.toml
        toml_path = "pyproject.toml"
        if not os.path.exists(toml_path):
            print("❌ pyproject.toml not found.")
            return
        
        # Check if already configured
        with open(toml_path, "r") as f:
            content = f.read()
        
        if "[tool.pyrefly]" in content:
            print("⚠️ [tool.pyrefly] already exists. Please edit manually to avoid overwriting.")
            return

        config_block = f'\n\n[tool.pyrefly]\n# "." tells Pyrefly to treat the project root as a source root.\n# We also add the site-packages from the local .venv so it finds installed libraries.\nsearch-path = [".", "{site_pkg}"]\n'
        
        with open(toml_path, "a") as f:
            f.write(config_block)
        print(f"✅ Appended [tool.pyrefly] configuration to {toml_path}")

    if __name__ == "__main__":
        fix_imports()
    ```

2.  **Run the script**:
    ```bash
    python fix_ide.py
    ```
