# Modpack Repository

This repository contains a Minecraft modpack managed with [packwiz](https://packwiz.infra.link/).

## How to Play

### Using MultiMC / Prism Launcher

1.  Create a new instance with the required Minecraft version and modloader (Fabric/Forge/NeoForge) specified in `pack.toml`.
2.  Download `packwiz-installer-bootstrap.jar` from the [official releases](https://github.com/packwiz/packwiz-installer-bootstrap/releases).
3.  Place `packwiz-installer-bootstrap.jar` in your instance's `.minecraft` folder.
4.  Enable "Custom Commands" in your instance settings.
5.  Set the **Pre-launch command** to:
    ```bash
    "$INST_JAVA" -jar packwiz-installer-bootstrap.jar [URL_TO_PACK.TOML]
    ```
    Replace `[URL_TO_PACK.TOML]` with the public URL of your `pack.toml` file (e.g., from GitHub Pages or a raw file link).

### Automatic Updates

Every time you launch the instance, `packwiz-installer` will automatically check for updates and download any new or modified mods.

## Repository Structure

- `pack.toml`: Main project configuration.
- `index.toml`: Index of all files in the modpack.
- `mods/`: Contains `.toml` metadata for each mod (actual `.jar` files are ignored by Git).
- `.gitignore`: Configured to exclude `.jar` files but include pack metadata.
- `.gitattributes`: Ensures consistent line endings and handles binary files.
