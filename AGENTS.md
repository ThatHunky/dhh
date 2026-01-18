# AGENTS.md

Instructions for AI coding assistants working with this repository.

## Project Overview

This is a **Minecraft modpack** managed with [packwiz](https://packwiz.infra.link/). The pack runs on **NeoForge 1.21.11** and uses **Sinytra Connector** for Fabric mod compatibility.

## Key Files

| File | Purpose |
|------|---------|
| `pack.toml` | Main pack configuration (name, version, Minecraft/loader versions) |
| `index.toml` | Auto-generated file index with SHA256 hashes |
| `mods/*.pw.toml` | Metadata files for each mod (NOT the actual JARs) |
| `docs/` | Documentation (included in pack distribution) |

## Important Concepts

### Packwiz Metadata Format

Mods are NOT stored as JAR files. Instead, each mod has a `.pw.toml` metadata file:

```toml
name = "Mod Name"
filename = "modfile.jar"
side = "both"  # client, server, or both

[download]
url = "https://cdn.modrinth.com/..."
hash-format = "sha512"
hash = "..."

[update]
[update.modrinth]
mod-id = "XXXXXXXX"
version = "abc123"
```

### Index File

`index.toml` is auto-generated and tracks all files with their hashes. **Never edit manually** - run `packwiz refresh` instead.

## Common Tasks

### Adding a Mod

```bash
# From Modrinth (preferred)
packwiz modrinth install <mod-name>

# From CurseForge
packwiz curseforge install <mod-name>
```

### Removing a Mod

```bash
packwiz remove <mod-name>
```

### Updating Mods

```bash
# Single mod
packwiz update <mod-name>

# All mods
packwiz update --all
```

### After Manual Edits

Always run after editing any files:
```bash
packwiz refresh
```

## Do's and Don'ts

### ✅ DO

- Run `packwiz refresh` after any manual file changes
- Use `packwiz modrinth install` for adding mods
- Check mod compatibility with NeoForge 1.21.11
- Keep documentation in `/docs` updated
- Use `side = "client"` for client-only mods, `side = "server"` for server-only

### ❌ DON'T

- Never manually edit `index.toml` - it's auto-generated
- Don't commit `.jar` files (they're in `.gitignore`)
- Don't change `hash` values manually - use `packwiz refresh`
- Don't assume Fabric mods work without testing (Connector has limitations)

## Loader Compatibility

This pack uses:
- **NeoForge** as the primary loader
- **Sinytra Connector** + **Forgified Fabric API** for Fabric mod support

When adding Fabric-only mods, they should work via Connector. If a mod needs explicit Fabric loader:
```toml
loader = "fabric"
```

## Version Compatibility

```toml
[versions]
minecraft = "1.21.11"
neoforge = "21.11.34-beta"

[options]
acceptable-game-versions = ["1.21.10", "1.21.11", "1.21.1", "1.21"]
```

Mods targeting any of the acceptable versions should work.

## Documentation

See `/docs` for:
- [Mod List](docs/mods.md) - All mods with categories and descriptions
- [Installation](docs/installation.md) - Client/server setup
- [Server Setup](docs/server-setup.md) - Server configuration
- [Development](docs/development.md) - Packwiz workflow

## Testing Changes

```bash
# Start local server for testing
packwiz serve

# Then configure launcher to use: http://localhost:8080/pack.toml
```
