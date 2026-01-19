#!/bin/bash
# DHH Modpack Client Update Script
# Compatible with Prism Launcher, MultiMC, and other launchers

set -e

# Switch to script directory (inside .minecraft)
cd "$(dirname "$0")"

# State file for tracking updates
STATE_FILE="update-state.json"

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

# Check if this is first launch
FIRST_LAUNCH=false
if [ ! -f "$STATE_FILE" ]; then
    FIRST_LAUNCH=true
    echo "First launch detected - creating state file..."
    python3 -c "import json, datetime; json.dump({'first_launch': True, 'last_update': None, 'install_date': datetime.datetime.utcnow().isoformat()}, open('$STATE_FILE', 'w'), indent=2)" 2>/dev/null || {
        # Fallback if python3 not available - create basic JSON
        echo '{"first_launch": true, "last_update": null, "install_date": "'$(date -u +"%Y-%m-%dT%H:%M:%S")'Z"}' > "$STATE_FILE"
    }
else
    echo "Previous installation found"
fi

# Download config files and options.txt on first launch only
if [ "$FIRST_LAUNCH" = true ]; then
    SERVER_BASE_URL="https://dhh.dobrovolskyi.xyz"
    
    echo "Downloading initial config files..."
    
    # List of config files to download (relative paths from config/ directory)
    # Add more config files here as needed
    CONFIG_FILES=(
        "DistantHorizons.toml"
        "inventoryprofilesnext/inventoryprofiles.json"
    )
    
    # Download config files
    if [ ! -d "config" ]; then
        mkdir -p config
    fi
    
    for config_file in "${CONFIG_FILES[@]}"; do
        if [ -n "$config_file" ]; then
            config_path="config/$config_file"
            config_dir=$(dirname "$config_path")
            
            # Create subdirectory if needed
            if [ "$config_dir" != "config" ] && [ "$config_dir" != "." ]; then
                mkdir -p "$config_dir"
            fi
            
            # Only download if file doesn't exist
            if [ ! -f "$config_path" ]; then
                echo "  Downloading config: $config_file"
                curl -sL "${SERVER_BASE_URL}/config/${config_file}" -o "$config_path" && echo "    ✓ Downloaded $config_file" || echo "    ✗ Failed to download $config_file (may not exist on server)"
            else
                echo "  Config already exists: $config_file (skipping)"
            fi
        fi
    done
    
    # Download options.txt (root directory)
    if [ ! -f "options.txt" ]; then
        echo "  Downloading options.txt..."
        curl -sL "${SERVER_BASE_URL}/options.txt" -o "options.txt" && echo "    ✓ Downloaded options.txt" || echo "    ✗ Failed to download options.txt (may not exist on server)"
    else
        echo "  options.txt already exists (skipping)"
    fi
    
    # Download servers.dat (root directory)
    if [ ! -f "servers.dat" ]; then
        echo "  Downloading servers.dat..."
        curl -sL "${SERVER_BASE_URL}/servers.dat" -o "servers.dat" && echo "    ✓ Downloaded servers.dat" || echo "    ✗ Failed to download servers.dat (may not exist on server)"
    else
        echo "  servers.dat already exists (skipping)"
    fi
fi

# 1. Download bootstrapper if not present
if [ ! -f "packwiz-installer-bootstrap.jar" ]; then
    echo "Downloading packwiz-installer-bootstrap..."
    curl -LO https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar
fi

# 2. Download custom (non-packwiz) mods from server
echo "Checking for custom mods..."
if [ -d "mods" ]; then
    # List of custom JAR mods to download (mods without .pw.toml metadata)
    # Add more custom mods here as needed
    CUSTOM_MODS=()
    
    SERVER_MODS_URL="https://dhh.dobrovolskyi.xyz/mods/"
    
    for modjar in "${CUSTOM_MODS[@]}"; do
        if [ -n "$modjar" ]; then
            echo "[CUSTOM] Downloading custom mod: $modjar"
            curl -sL "${SERVER_MODS_URL}${modjar}" -o "mods/${modjar}" && echo "  ✓ Downloaded $modjar" || echo "  ✗ Failed to download $modjar"
        fi
    done
fi

# 3. Run the installer
"$JAVA_CMD" -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml

# Update state file with last update time
UPDATE_EXIT_CODE=$?
if [ $UPDATE_EXIT_CODE -eq 0 ]; then
    echo "Updating state file..."
    if command -v python3 &> /dev/null; then
        python3 -c "
import json
import datetime

try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    state = {'install_date': datetime.datetime.utcnow().isoformat() + 'Z'}

state['first_launch'] = False
state['last_update'] = datetime.datetime.utcnow().isoformat() + 'Z'

with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
    else
        # Fallback: basic JSON update (preserves install_date if file exists)
        if [ -f "$STATE_FILE" ]; then
            INSTALL_DATE=$(grep -o '"install_date":\s*"[^"]*"' "$STATE_FILE" | cut -d'"' -f4 || echo "")
        fi
        if [ -z "$INSTALL_DATE" ]; then
            INSTALL_DATE="$(date -u +"%Y-%m-%dT%H:%M:%S")Z"
        fi
        echo "{\"first_launch\": false, \"last_update\": \"$(date -u +"%Y-%m-%dT%H:%M:%S")Z\", \"install_date\": \"$INSTALL_DATE\"}" > "$STATE_FILE"
    fi
    echo "Update complete!"
else
    echo "Update failed - state not updated"
    exit $UPDATE_EXIT_CODE
fi
