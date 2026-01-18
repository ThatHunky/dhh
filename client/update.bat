@echo off
:: DHH Modpack Client Update Script
:: Compatible with Prism Launcher, MultiMC, and other launchers
::
:: This script ensures a clean update by removing stale mods.

:: Switch context to this script's directory (inside .minecraft)
cd /d "%~dp0"

:: Determine Java executable
if "%~1"=="" (
    set "JAVA_CMD=java"
) else (
    set "JAVA_CMD=%~1"
)

echo.
echo ==============================================
echo [DHH] Modpack Update System
echo ==============================================
echo Using Java: %JAVA_CMD%

:: 1. Download bootstrapper if not present
if not exist "packwiz-installer-bootstrap.jar" (
    echo Downloading packwiz-installer-bootstrap...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar' -OutFile 'packwiz-installer-bootstrap.jar'"
)

:: 2. RUN CLEANUP (Removes stale mods that packwiz might miss)
echo Synchronizing mods folder...
powershell -Command "& { ^
    $indexUrl = 'https://dhh.dobrovolskyi.xyz/index.toml'; ^
    try { ^
        $content = Invoke-WebRequest -Uri $indexUrl -UseBasicParsing; ^
        $validMods = @(); ^
        foreach ($line in $content.Content.Split(\"`n\")) { ^
            if ($line -match 'file = \"mods/([^\"]+)\"') { ^
                $validMods += $matches[1].Replace('.pw.toml', '.jar').ToLower(); ^
            } ^
        } ^
        if ($validMods.Count -gt 0 -and (Test-Path 'mods')) { ^
            $localMods = Get-ChildItem 'mods' -Filter *.jar; ^
            foreach ($mod in $localMods) { ^
                if ($validMods -notcontains $mod.Name.ToLower()) { ^
                    Write-Host \"[CLEAN] Removing stale mod: $($mod.Name)\" -ForegroundColor Yellow; ^
                    Remove-Item $mod.FullName -Force; ^
                } ^
            } ^
        } ^
    } catch { ^
        Write-Host \"[WARN] Could not reach index for cleanup. Skipping...\" -ForegroundColor Gray; ^
    } ^
}"

:: 3. Run the installer
"%JAVA_CMD%" -jar packwiz-installer-bootstrap.jar https://dhh.dobrovolskyi.xyz/pack.toml

:: Check for errors
if %errorlevel% neq 0 (
    echo.
    echo ----------------------------------------------------
    echo [ERROR] Packwiz update failed!
    echo Check your internet connection or the server URL.
    echo ----------------------------------------------------
    pause
    exit /b %errorlevel%
)

echo Update complete!