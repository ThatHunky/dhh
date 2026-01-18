# Server Setup Guide

Complete guide for setting up and configuring a DHH modpack server.

## Requirements

- Java 21+
- 4GB RAM minimum (8GB+ recommended)
- Linux, Windows, or macOS

## Installation

### 1. Install NeoForge Server

```bash
# Download NeoForge installer
wget https://maven.neoforged.net/releases/net/neoforged/neoforge/21.11.34-beta/neoforge-21.11.34-beta-installer.jar

# Install server files
java -jar neoforge-21.11.34-beta-installer.jar --installServer

# Accept EULA
echo "eula=true" > eula.txt
```

### 2. Download Mods

Using packwiz-installer (recommended):

```bash
# Download packwiz-installer-bootstrap
wget https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar

# Install server-side mods only
java -jar packwiz-installer-bootstrap.jar -s server https://YOUR_PACK_URL/pack.toml
```

### 3. Start Server

```bash
java -Xmx8G -Xms4G -jar neoforge-server.jar nogui
```

## Configuration

### Simple Voice Chat

The server needs a dedicated UDP port for voice chat.

1. Edit `config/voicechat/voicechat-server.properties`:
   ```properties
   port=24454
   bind_address=0.0.0.0
   ```

2. Open port 24454 UDP in your firewall:
   ```bash
   # Linux (ufw)
   sudo ufw allow 24454/udp
   
   # Linux (firewalld)
   sudo firewall-cmd --add-port=24454/udp --permanent
   ```

### EasyAuth (Offline Mode Authentication)

Enable if running in offline mode for account protection.

1. Set `online-mode=false` in `server.properties`
2. Configure `config/easyauth/config.json`:
   ```json
   {
     "experimental": {
       "enableServerSideTranslation": true
     },
     "main": {
       "requirePassword": true
     }
   }
   ```

Players register with `/register <password>` and login with `/login <password>`.

### Ledger (Logging & Rollback)

Ledger logs all block changes for grief protection.

Commands:
- `/ledger inspect` - Toggle inspect mode (click blocks to see history)
- `/ledger search` - Search for actions
- `/ledger rollback` - Revert changes
- `/ledger restore` - Restore rolled-back changes

### Chunky (Pre-generation)

Pre-generate the world to reduce lag from chunk loading.

```
/chunky radius 5000
/chunky start
```

Monitor progress:
```
/chunky progress
```

## Performance Tuning

### JVM Arguments

Recommended startup flags:

```bash
java -Xmx8G -Xms8G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -jar neoforge-server.jar nogui
```

### server.properties

```properties
# Performance
view-distance=10
simulation-distance=8
network-compression-threshold=256

# Security
online-mode=false  # Set to true if using Mojang auth
enable-command-block=false
spawn-protection=16
```

### Spark Profiler

Use Spark to identify performance issues:

```
/spark profiler start
# Play for a few minutes
/spark profiler stop
```

View the generated report to find bottlenecks.

## Backups

Regular backups are essential. Recommended backup strategy:

```bash
#!/bin/bash
# backup.sh
WORLD_DIR="/path/to/server/world"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y-%m-%d_%H-%M)

tar -czf "$BACKUP_DIR/world_$DATE.tar.gz" "$WORLD_DIR"

# Keep only last 7 daily backups
find "$BACKUP_DIR" -name "world_*.tar.gz" -mtime +7 -delete
```

Run via cron:
```bash
0 4 * * * /path/to/backup.sh
```

## Updating the Pack

```bash
# Stop server first!
java -jar packwiz-installer-bootstrap.jar -s server https://YOUR_PACK_URL/pack.toml
```

This will download new mods and remove obsolete ones.
