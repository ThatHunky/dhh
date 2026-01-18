# Installation Guide

## Requirements

- Minecraft 1.21.1 
- ~4GB RAM allocated to Minecraft (8GB recommended with shaders)

## Client Installation

### Method 1: Prism Launcher / MultiMC (Recommended)

This method provides automatic updates whenever you launch the game.

1. **Create a new instance**
   - Open Prism Launcher or MultiMC
   - Click "Add Instance"
   - Select Minecraft **1.21.11**
   - Install **NeoForge 21.11.34-beta** as the mod loader

2. **Download packwiz-installer-bootstrap**
   - Get `packwiz-installer-bootstrap.jar` from [GitHub Releases](https://github.com/packwiz/packwiz-installer-bootstrap/releases)
   - Place it in your instance's `.minecraft` folder

3. **Configure pre-launch command**
   - Right-click your instance → Edit → Settings → Custom Commands
   - Enable "Custom Commands"
   - Set **Pre-launch command** to:
   ```bash
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://YOUR_PACK_URL/pack.toml
   ```
   > Replace `https://YOUR_PACK_URL/pack.toml` with the actual URL where the pack is hosted.

4. **Launch the game**
   - The installer will automatically download all mods on first launch
   - Future launches will check for updates

### Method 2: Manual Installation

1. Install NeoForge 21.11.34-beta for Minecraft 1.21.11
2. Download all mod JARs from Modrinth using the links in [mods.md](mods.md)
3. Place mods in your `.minecraft/mods` folder
4. Download the shaderpack from Modrinth and place in `.minecraft/shaderpacks`

> ⚠️ Manual installation requires you to update mods yourself.

## Server Installation

See [Server Setup Guide](server-setup.md) for detailed server installation instructions.

### Quick Start

1. Download [NeoForge server installer](https://neoforged.net/)
2. Run: `java -jar neoforge-installer.jar --installServer`
3. Use packwiz-installer to download mods:
   ```bash
   java -jar packwiz-installer-bootstrap.jar -s server https://YOUR_PACK_URL/pack.toml
   ```
   The `-s server` flag only downloads server-side mods.

4. Start the server:
   ```bash
   java -Xmx4G -jar neoforge-server.jar nogui
   ```

## Verifying Installation

After launching, verify the modpack is working:

1. Check the mod count in Mod Menu (should show 58 mods)
2. Open F3 debug screen - should show "DHH" in the window title
3. Create a new world and verify Biomes O' Plenty biomes generate

## Troubleshooting

See [FAQ](faq.md) for common issues and solutions.

### Common Issues

| Issue | Solution |
|-------|----------|
| "Out of memory" crash | Allocate more RAM (4-8GB) |
| Mods not downloading | Check pack.toml URL is accessible |
| NeoForge version mismatch | Use exactly NeoForge 21.11.34-beta |
| Shader not loading | Ensure Iris is installed and working |
