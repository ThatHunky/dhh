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
