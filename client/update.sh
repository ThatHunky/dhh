#!/bin/bash
# DHH Modpack Client Update Script
# Compatible with Prism Launcher, MultiMC, and other launchers

set -e

# Switch to script directory (inside .minecraft)
cd "$(dirname "$0")"

# Determine Java executable
if [ -n "$1" ]; then
    JAVA_CMD="$1"
elif [ -n "$INST_JAVA" ]; then
    JAVA_CMD="$INST_JAVA"
elif command -v java &> /dev/null; then
    JAVA_CMD="java"
else
    echo "=============================================="
    echo "[ERROR] Java not found!"
    exit 1
fi

echo "Using Java: $JAVA_CMD"

# 1. Download bootstrapper if not present
if [ ! -f "packwiz-installer-bootstrap.jar" ]; then
    echo "Downloading packwiz-installer-bootstrap..."
    curl -LO https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar
fi

# 2. Synchronize mods folder (Cleanup stale JARs)
echo "Synchronizing mods folder..."
if [ -d "mods" ]; then
    # Fetch lists of valid mods from index.toml
    # This extract filenames from 'file = "mods/modname.pw.toml"' and converts to .jar
    VALID_MODS=$(curl -s https://dhh.dobrovolskyi.xyz/index.toml | grep 'file = "mods/' | sed -E 's/.*mods\/(.*)\.pw\.toml.*/\1.jar/' | tr '[:upper:]' '[:lower:]')
    
    if [ -n "$VALID_MODS" ]; then
        for mod in mods/*.jar; do
            [ -e "$mod" ] || continue
            filename=$(basename "$mod" | tr '[:upper:]' '[:lower:]')
            if ! echo "$VALID_MODS" | grep -qxw "$filename"; then
                echo "[CLEAN] Removing stale mod: $(basename "$mod")"
                rm "$mod"
            fi
        done
    fi
fi

# 3. Run the installer
"$JAVA_CMD" -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml

echo "Update complete!"
