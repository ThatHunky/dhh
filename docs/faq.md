# FAQ & Troubleshooting

Common questions and solutions for the DHH modpack.

## Installation Issues

### Q: "Out of memory" crash on launch

**A:** Allocate more RAM to Minecraft:
- Prism/MultiMC: Edit Instance → Settings → Java → Maximum memory allocation
- Recommended: 4-6GB without shaders, 8GB+ with shaders

### Q: Mods aren't downloading / packwiz-installer fails

**A:** Check:
1. Internet connection is working
2. pack.toml URL is correct and accessible
3. Java is installed and in PATH
4. Try running packwiz-installer manually to see errors:
   ```bash
   java -jar packwiz-installer-bootstrap.jar https://YOUR_URL/pack.toml
   ```

### Q: NeoForge version mismatch error

**A:** This pack requires exactly **NeoForge 21.11.34-beta**. Update your NeoForge installation to match.

### Q: "Mod X requires Fabric" error

**A:** This shouldn't happen as the pack includes Sinytra Connector. If it does:
1. Verify Sinytra Connector and Forgified Fabric API are installed
2. Check if the mod is known to be incompatible with Connector

## Gameplay Issues

### Q: Low FPS / poor performance

**A:** Try:
1. Lower render distance (8-12 chunks)
2. Disable shaders or use a lighter shaderpack
3. In Sodium settings, lower graphics quality
4. Disable Distant Horizons if not needed
5. Run `/spark profiler` to identify issues

### Q: Shaders not working

**A:** 
1. Press Escape → Options → Video Settings → Shader Packs
2. Select "Complementary Reimagined" or your preferred shader
3. Ensure you have enough RAM allocated (8GB+ recommended)

### Q: Voice chat not working

**A:** 
- **Client**: Check audio devices in Simple Voice Chat settings (V key by default)
- **Server**: Ensure port 24454 UDP is open in firewall
- Test with `/voicechat test`

### Q: Waystones not appearing in world

**A:** Waystones generate naturally in villages. You can also craft them. In new worlds, they will appear in newly generated chunks.

### Q: Maps not saving / resetting

**A:** Xaero's maps are stored per-server. If the server IP/name changes, maps may appear reset. Check `.minecraft/XaeroWorldMap` for saved data.

## Server Issues

### Q: Server won't start

**A:** Common causes:
1. EULA not accepted - create `eula.txt` with `eula=true`
2. Wrong Java version - requires Java 21+
3. Port already in use - check if another process uses port 25565
4. Not enough RAM - allocate at least 4GB

### Q: Players can't connect

**A:** Check:
1. Server is running and shows "Done" in console
2. Firewall allows port 25565 TCP
3. If behind NAT, port forwarding is configured
4. `server-ip=` in server.properties is empty or correct

### Q: Lag when players explore

**A:** Pre-generate chunks:
```
/chunky radius 5000
/chunky start
```
This prevents on-the-fly chunk generation lag.

### Q: How to whitelist players?

**A:** 
```
/whitelist on
/whitelist add PlayerName
```

## Mod-Specific Questions

### Q: How do I use JEI?

**A:** Press R on an item to see recipes, U to see uses. Type in the search bar to filter items.

### Q: How do I set up a waystone?

**A:** Craft a waystone and place it. Right-click to name it. Other waystones you discover are automatically linked.

### Q: How do I create a backpack?

**A:** Craft a Traveler's Backpack using leather and a chest. Equip it in the chest slot or back slot.

### Q: How do I use Distant Horizons?

**A:** It works automatically, rendering low-detail terrain beyond your normal render distance. Configure in Options → DH Settings.

## Updating

### Q: How do I update the modpack?

**A:** If using packwiz-installer, just launch the game - it updates automatically. For manual installs, re-download all mods.

### Q: Will updating break my world?

**A:** Generally no. Mod updates are usually save-compatible. Always backup your world before major updates.

### Q: How do I know what version I'm on?

**A:** Check `pack.toml` for the version number, or look at the window title in-game.

## Getting Help

If your issue isn't listed here:

1. Check the [Mod List](mods.md) for individual mod documentation
2. Search for your error message online
3. Check mod issue trackers on GitHub/Modrinth
4. Ask in the modpack community/Discord
