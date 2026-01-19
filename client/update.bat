@echo off
:: DHH Modpack Client Update Script
:: Compatible with Prism Launcher, MultiMC, and other launchers
::
:: This script downloads packwiz mods and custom JAR mods from the server.

:: Switch context to this script's directory (inside .minecraft)
cd /d "%~dp0"

:: State file for tracking updates
set "STATE_FILE=update-state.json"

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

:: Check if this is first launch and initialize state file
if not exist "%STATE_FILE%" (
    echo First launch detected - creating state file...
    powershell -Command "$state = @{ first_launch = $true; last_update = $null; install_date = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss') + 'Z' } | ConvertTo-Json; $state | Out-File -FilePath '%STATE_FILE%' -Encoding UTF8"
    
    :: Download config files on first launch
    echo Downloading initial config files...
    powershell -Command "$serverBaseUrl = 'https://dhh.dobrovolskyi.xyz'; $configFiles = @('DistantHorizons.toml', 'inventoryprofilesnext/inventoryprofiles.json'); if (-not (Test-Path 'config')) { New-Item -ItemType Directory -Path 'config' | Out-Null }; foreach ($cf in $configFiles) { $cp = 'config\' + $cf; $cd = Split-Path -Parent $cp; if ($cd -and -not (Test-Path $cd)) { New-Item -ItemType Directory -Path $cd -Force | Out-Null }; if (-not (Test-Path $cp)) { Write-Host '  Downloading config:' $cf; try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri ($serverBaseUrl + '/config/' + $cf) -OutFile $cp -UseBasicParsing -ErrorAction Stop; Write-Host '    Downloaded' $cf } catch { Write-Host '    Failed to download' $cf } } }"
    
    :: Download options.txt
    if not exist "options.txt" (
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri 'https://dhh.dobrovolskyi.xyz/options.txt' -OutFile 'options.txt' -UseBasicParsing; Write-Host '  Downloaded options.txt' } catch { Write-Host '  Failed to download options.txt' }"
    )
    
    :: Download servers.dat
    if not exist "servers.dat" (
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri 'https://dhh.dobrovolskyi.xyz/servers.dat' -OutFile 'servers.dat' -UseBasicParsing; Write-Host '  Downloaded servers.dat' } catch { Write-Host '  Failed to download servers.dat' }"
    )
) else (
    echo Previous installation found
)

:: 1. Download bootstrapper if not present
if not exist "packwiz-installer-bootstrap.jar" (
    echo Downloading packwiz-installer-bootstrap...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar' -OutFile 'packwiz-installer-bootstrap.jar'"
)

:: 2. Download custom (non-packwiz) mods from server
:: Currently no custom mods configured

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

:: Update state file with last update time
powershell -Command "$sf='%STATE_FILE%'; if (Test-Path $sf) { $s=Get-Content $sf|ConvertFrom-Json } else { $s=@{first_launch=$false;install_date=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')+'Z'} }; $s.first_launch=$false; $s.last_update=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')+'Z'; $s|ConvertTo-Json|Out-File -FilePath $sf -Encoding UTF8"

echo Update complete!