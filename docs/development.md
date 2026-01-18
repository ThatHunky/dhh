# Development Guide

Guide for modpack maintainers using packwiz.

## Prerequisites

Install packwiz:

```bash
# Using Go
go install github.com/packwiz/packwiz@latest

# Or download from releases
# https://github.com/packwiz/packwiz/releases
```

## Project Structure

```
dhh/
├── pack.toml          # Main pack configuration
├── index.toml         # File index with hashes
├── mods/              # Mod metadata files (.pw.toml)
├── shaderpacks/       # Shaderpack files
├── docs/              # Documentation
├── AGENTS.md          # AI assistant instructions
└── README.md          # Repository readme
```

### pack.toml

Main configuration file:

```toml
name = "DHH"
author = "Vsevolod Dobrovolskyi"
version = "1.0.0"
pack-format = "packwiz:1.1.0"

[index]
file = "index.toml"
hash-format = "sha256"
hash = "..."  # Auto-generated

[versions]
minecraft = "1.21.11"
neoforge = "21.11.34-beta"

[options]
acceptable-game-versions = ["1.21.10", "1.21.11", "1.21.1", "1.21"]
```

### Mod Metadata (.pw.toml)

Each mod has a metadata file:

```toml
name = "Sodium"
filename = "sodium-1.21.11.jar"
side = "client"  # client, server, or both

[download]
url = "https://cdn.modrinth.com/..."
hash-format = "sha512"
hash = "..."

[update]
[update.modrinth]
mod-id = "AANobbMI"
version = "abc123"
```

## Common Tasks

### Adding a Mod

From Modrinth:
```bash
packwiz modrinth install sodium
```

From CurseForge:
```bash
packwiz curseforge install jei
```

From URL:
```bash
packwiz url add https://example.com/mod.jar
```

### Removing a Mod

```bash
packwiz remove sodium
```

### Updating Mods

Update a specific mod:
```bash
packwiz update sodium
```

Update all mods:
```bash
packwiz update --all
```

### Refreshing Index

After manually editing files:
```bash
packwiz refresh
```

### Exporting

To CurseForge format:
```bash
packwiz curseforge export
```

To Modrinth format:
```bash
packwiz modrinth export
```

## Hosting the Pack

### GitHub Pages

1. Push pack to GitHub repository
2. Enable GitHub Pages (Settings → Pages → main branch)
3. Pack URL: `https://username.github.io/repo/pack.toml`

### Self-Hosted

Serve files via any HTTP server:

```bash
# Development server (packwiz built-in)
packwiz serve

# Production (nginx, Caddy, etc.)
# Just serve the directory as static files
```

## Git Workflow

### .gitignore

```gitignore
# Ignore downloaded JARs
mods/*.jar
shaderpacks/*.zip

# Keep metadata
!mods/*.pw.toml
!shaderpacks/*.toml
```

### Committing Changes

1. Make changes (add/remove/update mods)
2. Run `packwiz refresh`
3. Commit both `.pw.toml` files and `index.toml`

## Troubleshooting

### "Hash mismatch" errors

Re-run `packwiz refresh` to update hashes.

### Mod not found on Modrinth

1. Check if mod exists for your Minecraft version
2. Use `packwiz url add` for direct downloads
3. Check mod loader compatibility (Fabric vs NeoForge)

### Fabric mods on NeoForge

This pack uses Sinytra Connector. For Fabric-only mods:

1. Add the mod normally via `packwiz modrinth install`
2. Connector will handle compatibility at runtime
3. Some mods may need `loader = "fabric"` in their `.pw.toml`

## Testing Changes

### Local Testing

1. Run `packwiz serve` in the pack directory
2. Configure launcher to use `http://localhost:8080/pack.toml`
3. Launch game and verify changes

### Validation

```bash
# Check for issues
packwiz refresh

# Verify all mods can be downloaded
packwiz refresh --check
```

## Server Deployment System

The server uses a custom Python deployment script instead of `packwiz-installer` for better control over side-exclusivity.

### deploy_modpack.py

Located at `~/games/servers/dhh-server/deploy_modpack.py`, this script:

1. **Parses** the remote `pack.toml` and `index.toml`
2. **Filters** mods by `side` property (skips `side = "client"`)
3. **Downloads** only server-compatible mods
4. **Cleans** stale JARs not in the current index

```python
# Key features:
# - Respects side = "client" | "server" | "both"
# - Hash verification for cached downloads
# - Automatic cleanup of orphaned mods
# - Real-time progress output (flush=True)
```

### loop.sh Integration

The server's `loop.sh` calls the deployment script before starting:

```bash
python3 deploy_modpack.py
if [ $? -ne 0 ]; then
    echo "❌ DEPLOY FAILED!"
    # ... error handling
fi
# Then start NeoForge server
bash run.sh nogui
```

### Why Not packwiz-installer?

The standard `packwiz-installer` had issues with:
- Not properly cleaning stale mods
- Inconsistent handling of `side` metadata
- Leaving orphaned Fabric mods after migration

The custom script ensures a 100% clean server environment.

## Client Update Scripts

### Directory Structure

```
client/
├── update.bat           # Windows (Prism, MultiMC)
├── update.sh            # Linux/macOS (Prism, MultiMC)
└── packwiz-installer-bootstrap.jar  # Downloaded automatically
```

### Windows (update.bat)

```batch
@echo off
cd /d "%~dp0"
"%~1" -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml
```

**Usage in Prism Launcher:**
1. Copy `client/` folder to your instance's `.minecraft/`
2. Set Pre-launch command: `cmd /c "$INST_MC_DIR/client/update.bat" "$INST_JAVA"`

### Linux/macOS (update.sh)

```bash
#!/bin/bash
cd "$(dirname "$0")"
"${1:-${INST_JAVA:-java}}" -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml
```

**Usage in Prism Launcher:**
1. Copy `client/` folder to your instance's `.minecraft/`
2. Make executable: `chmod +x update.sh`
3. Set Pre-launch command: `"$INST_MC_DIR/client/update.sh" "$INST_JAVA"`

### Modrinth Pack Format

To export for Modrinth App users:

```bash
packwiz modrinth export
```

This creates a `.mrpack` file that can be imported directly.

### CurseForge Format

For CurseForge App users:

```bash
packwiz curseforge export
```

### Manual Update (Any Launcher)

1. Download [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases)
2. Place in your `.minecraft/` folder
3. Run before launching:
   ```bash
   java -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml
   ```
