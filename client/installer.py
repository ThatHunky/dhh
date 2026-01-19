#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DHH Modpack GUI Installer
Interactive installer for Prism Launcher with Ukrainian/English localization
Complete rewrite with proper instance structure and improved UX
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import shutil
import logging
import webbrowser
from pathlib import Path
from threading import Thread
from typing import Optional, Callable

# Try to use requests library for better networking (fallback to urllib)
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error
    import ssl

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('installer.log', encoding='utf-8')]
)
logger = logging.getLogger(__name__)

# Pack configuration
PACK_NAME = "DHH"
PACK_URL = "https://dhh.dobrovolskyi.xyz/pack.toml"
MINECRAFT_VERSION = "1.21.1"
NEOFORGE_VERSION = "21.1.218"
LWJGL_VERSION = "3.3.3"
MIN_MEMORY = 4096  # 4GB in MB
MAX_MEMORY = 8192  # 8GB in MB
PRE_LAUNCH_CMD = 'cmd /c \"$INST_DIR/minecraft/update.bat\" \"$INST_JAVA\"'

PRISM_DOWNLOAD_URL = "https://prismlauncher.org/download/"

# Translations
TRANSLATIONS = {
    'uk': {
        'title': 'Встановлення модпаку DHH',
        'language_toggle': '🇬🇧 English',
        'welcome': 'Ласкаво просимо!',
        'welcome_desc': 'Цей інсталятор автоматично встановить модпак DHH для Minecraft.',
        'checking_prism': 'Перевірка наявності Prism Launcher...',
        'prism_found': 'Prism Launcher знайдено!',
        'prism_not_found': 'Prism Launcher не знайдено',
        'prism_not_found_desc': 'Prism Launcher не встановлено на вашому комп\'ютері.\n\nНатисніть "Завантажити Prism", щоб відкрити сторінку завантаження.\nПісля встановлення натисніть "Перевірити знову".',
        'download_prism': 'Завантажити Prism',
        'check_again': 'Перевірити знову',
        'creating_instance': 'Створення екземпляра...',
        'copying_files': 'Копіювання файлів...',
        'configuring': 'Налаштування...',
        'success': 'Встановлення завершено!',
        'success_desc': 'Модпак DHH успішно встановлено.\n\nТепер ви можете запустити його через Prism Launcher.\nПри першому запуску буде завантажено моди.',
        'error': 'Помилка',
        'error_instance_create': 'Не вдалося створити екземпляр.',
        'error_file_copy': 'Не вдалося скопіювати файли.',
        'error_config': 'Не вдалося налаштувати екземпляр.',
        'error_permission': 'Немає доступу: {path}. Спробуйте запустити від імені адміністратора.',
        'start_installation': 'Почати встановлення',
        'close': 'Закрити',
        'instance_path': 'Шлях до екземпляра:',
        'launch_prism': 'Відкрити Prism Launcher',
    },
    'en': {
        'title': 'DHH Modpack Installer',
        'language_toggle': '🇺🇦 Українська',
        'welcome': 'Welcome!',
        'welcome_desc': 'This installer will automatically set up the DHH modpack for Minecraft.',
        'checking_prism': 'Checking for Prism Launcher...',
        'prism_found': 'Prism Launcher found!',
        'prism_not_found': 'Prism Launcher not found',
        'prism_not_found_desc': 'Prism Launcher is not installed on your computer.\n\nClick "Download Prism" to open the download page.\nAfter installation, click "Check Again".',
        'download_prism': 'Download Prism',
        'check_again': 'Check Again',
        'creating_instance': 'Creating instance...',
        'copying_files': 'Copying files...',
        'configuring': 'Configuring...',
        'success': 'Installation complete!',
        'success_desc': 'DHH modpack has been successfully installed.\n\nYou can now launch it through Prism Launcher.\nMods will be downloaded on first launch.',
        'error': 'Error',
        'error_instance_create': 'Failed to create instance.',
        'error_file_copy': 'Failed to copy files.',
        'error_config': 'Failed to configure instance.',
        'error_permission': 'Access denied: {path}. Try running as administrator.',
        'start_installation': 'Start Installation',
        'close': 'Close',
        'instance_path': 'Instance path:',
        'launch_prism': 'Open Prism Launcher',
    }
}


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(TRANSLATIONS['uk']['title'])
        self.root.geometry('600x450')
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Language (default: Ukrainian)
        self.current_lang = 'uk'
        
        # Prism Launcher paths
        self.prism_path: Optional[Path] = None
        self.prism_instances_path: Optional[Path] = None
        
        # Pack configuration
        self.instance_name = PACK_NAME
        
        # Created instance path (for success screen)
        self.created_instance_path: Optional[Path] = None
        
        # Setup UI
        self.setup_ui()
        
        logger.info("Installer initialized")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with language toggle
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(header_frame, text=self.t('title'), font=('Segoe UI', 18, 'bold'))
        self.title_label.pack(side=tk.LEFT)
        
        self.lang_button = ttk.Button(header_frame, text=self.t('language_toggle'), 
                                command=self.toggle_language, width=15)
        self.lang_button.pack(side=tk.RIGHT)
        
        # Content frame (changes based on state)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show welcome screen initially
        self.show_welcome_screen()
    
    def t(self, key: str) -> str:
        """Get translation for current language"""
        return TRANSLATIONS[self.current_lang].get(key, key)
    
    def toggle_language(self):
        """Toggle between Ukrainian and English"""
        self.current_lang = 'en' if self.current_lang == 'uk' else 'uk'
        self.update_ui_text()
    
    def update_ui_text(self):
        """Update all UI text when language changes"""
        self.root.title(self.t('title'))
        self.title_label.config(text=self.t('title'))
        self.lang_button.config(text=self.t('language_toggle'))
        
        # Update button texts if they exist
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                # Update known buttons by their current text patterns
                widget.update()
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        self.clear_content()
        
        # Welcome message
        welcome_label = ttk.Label(self.content_frame, text=self.t('welcome'), 
                                 font=('Segoe UI', 14, 'bold'))
        welcome_label.pack(pady=(40, 10))
        
        desc_label = ttk.Label(self.content_frame, text=self.t('welcome_desc'),
                              justify=tk.CENTER, wraplength=500, font=('Segoe UI', 10))
        desc_label.pack(pady=(0, 40))
        
        # Start button
        start_btn = ttk.Button(self.content_frame, text=self.t('start_installation'), 
                              command=self.start_installation, width=25)
        start_btn.pack(pady=20)
    
    def show_prism_not_found_screen(self):
        """Show Prism Launcher not found screen with download instructions"""
        self.clear_content()
        
        # Warning icon (using emoji)
        icon_label = ttk.Label(self.content_frame, text="⚠️", font=('Segoe UI', 48))
        icon_label.pack(pady=(20, 10))
        
        # Title
        title_label = ttk.Label(self.content_frame, text=self.t('prism_not_found'),
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(self.content_frame, text=self.t('prism_not_found_desc'),
                              justify=tk.CENTER, wraplength=500, font=('Segoe UI', 10))
        desc_label.pack(pady=(0, 30))
        
        # Buttons frame
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=20)
        
        # Download button (primary)
        download_btn = ttk.Button(btn_frame, text=self.t('download_prism'),
                                 command=self.open_prism_download, width=20)
        download_btn.pack(side=tk.LEFT, padx=10)
        
        # Check again button
        check_btn = ttk.Button(btn_frame, text=self.t('check_again'),
                              command=self.check_prism_again, width=20)
        check_btn.pack(side=tk.LEFT, padx=10)
    
    def show_progress_screen(self, message: str):
        """Show progress screen with spinner"""
        self.clear_content()
        
        # Spacer
        ttk.Frame(self.content_frame).pack(pady=50)
        
        # Status message
        self.status_label = ttk.Label(self.content_frame, text=message,
                                      font=('Segoe UI', 12))
        self.status_label.pack(pady=20)
        
        # Progress bar (indeterminate)
        self.progress = ttk.Progressbar(self.content_frame, mode='indeterminate', length=400)
        self.progress.pack(pady=20)
        self.progress.start(10)
    
    def update_status(self, message: str):
        """Update status message"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def show_success_screen(self):
        """Show success screen"""
        self.clear_content()
        
        # Success icon
        icon_label = ttk.Label(self.content_frame, text="✅", font=('Segoe UI', 48))
        icon_label.pack(pady=(30, 10))
        
        # Title
        title_label = ttk.Label(self.content_frame, text=self.t('success'),
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(self.content_frame, text=self.t('success_desc'),
                              justify=tk.CENTER, wraplength=500, font=('Segoe UI', 10))
        desc_label.pack(pady=(0, 20))
        
        # Instance path
        if self.created_instance_path:
            path_frame = ttk.Frame(self.content_frame)
            path_frame.pack(pady=10)
            
            path_label = ttk.Label(path_frame, text=self.t('instance_path'),
                                  font=('Segoe UI', 9))
            path_label.pack(side=tk.LEFT)
            
            path_value = ttk.Label(path_frame, text=str(self.created_instance_path),
                                  font=('Segoe UI', 9, 'italic'))
            path_value.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=30)
        
        # Launch Prism button
        if self.prism_path:
            launch_btn = ttk.Button(btn_frame, text=self.t('launch_prism'),
                                   command=self.launch_prism, width=20)
            launch_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = ttk.Button(btn_frame, text=self.t('close'),
                              command=self.root.quit, width=15)
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def show_error(self, message: str):
        """Show error dialog and reset to welcome screen"""
        if hasattr(self, 'progress'):
            self.progress.stop()
        messagebox.showerror(self.t('error'), message)
        self.show_welcome_screen()
    
    def open_prism_download(self):
        """Open Prism Launcher download page in browser"""
        logger.info(f"Opening download page: {PRISM_DOWNLOAD_URL}")
        webbrowser.open(PRISM_DOWNLOAD_URL)
    
    def check_prism_again(self):
        """Re-check for Prism Launcher after user installs it"""
        self.show_progress_screen(self.t('checking_prism'))
        
        def check_worker():
            if self.find_prism_launcher():
                self.root.after(0, self.continue_installation)
            else:
                self.root.after(0, self.show_prism_not_found_screen)
        
        Thread(target=check_worker, daemon=True).start()
    
    def launch_prism(self):
        """Launch Prism Launcher"""
        if self.prism_path and self.prism_path.exists():
            try:
                import subprocess
                subprocess.Popen([str(self.prism_path)], start_new_session=True)
                logger.info(f"Launched Prism Launcher: {self.prism_path}")
            except Exception as e:
                logger.error(f"Failed to launch Prism: {e}")
    
    def start_installation(self):
        """Start the installation process"""
        self.show_progress_screen(self.t('checking_prism'))
        
        def install_worker():
            # Step 1: Check for Prism Launcher
            if not self.find_prism_launcher():
                self.root.after(0, self.show_prism_not_found_screen)
                return
            
            self.root.after(0, self.continue_installation)
        
        Thread(target=install_worker, daemon=True).start()
    
    def continue_installation(self):
        """Continue installation after Prism is found"""
        self.show_progress_screen(self.t('prism_found'))
        
        def install_worker():
            try:
                # Step 2: Create instance
                self.root.after(0, lambda: self.update_status(self.t('creating_instance')))
                instance_path = self.create_instance()
                if not instance_path:
                    self.root.after(0, lambda: self.show_error(self.t('error_instance_create')))
                    return
                
                # Step 3: Copy update.bat
                self.root.after(0, lambda: self.update_status(self.t('copying_files')))
                if not self.copy_update_bat(instance_path):
                    self.root.after(0, lambda: self.show_error(self.t('error_file_copy')))
                    return
                
                # Step 4: Configure instance
                self.root.after(0, lambda: self.update_status(self.t('configuring')))
                if not self.configure_instance(instance_path):
                    self.root.after(0, lambda: self.show_error(self.t('error_config')))
                    return
                
                # Success!
                self.created_instance_path = instance_path
                self.root.after(0, self.show_success_screen)
                
            except PermissionError as e:
                logger.error(f"Permission error: {e}")
                error_msg = self.t('error_permission').format(path=str(e))
                self.root.after(0, lambda: self.show_error(error_msg))
            except Exception as e:
                logger.exception("Installation failed")
                error_msg = f"{self.t('error')}: {str(e)}"
                self.root.after(0, lambda: self.show_error(error_msg))
        
        Thread(target=install_worker, daemon=True).start()
    
    def find_prism_launcher(self) -> bool:
        """Find Prism Launcher installation"""
        logger.debug("Searching for Prism Launcher...")
        
        search_paths = []
        
        # Windows registry check
        if sys.platform == 'win32':
            search_paths.extend(self._search_registry())
        
        # Environment-based paths
        appdata = os.getenv('APPDATA')  # %APPDATA% (Roaming)
        localappdata = os.getenv('LOCALAPPDATA')  # %LOCALAPPDATA%
        programfiles = os.getenv('PROGRAMFILES')
        programfilesx86 = os.getenv('PROGRAMFILES(X86)')
        
        # Primary locations (Windows)
        if localappdata:
            search_paths.append(Path(localappdata) / 'Programs' / 'PrismLauncher')
        if appdata:
            search_paths.append(Path(appdata) / 'PrismLauncher')
        if programfiles:
            search_paths.append(Path(programfiles) / 'PrismLauncher')
        if programfilesx86:
            search_paths.append(Path(programfilesx86) / 'PrismLauncher')
        
        # Linux paths
        home = Path.home()
        search_paths.extend([
            home / '.local' / 'share' / 'PrismLauncher',
            home / '.var' / 'app' / 'org.prismlauncher.PrismLauncher' / 'data' / 'PrismLauncher',
            Path('/usr/share/prismlauncher'),
            Path('/opt/prismlauncher'),
        ])
        
        # Check each path
        for path in search_paths:
            if path and path.exists():
                exe_path = self._find_executable(path)
                if exe_path:
                    self.prism_path = exe_path
                    self.prism_instances_path = self._get_instances_path()
                    logger.info(f"Found Prism Launcher: {exe_path}")
                    logger.info(f"Instances path: {self.prism_instances_path}")
                    return True
        
        logger.debug("Prism Launcher not found")
        return False
    
    def _search_registry(self) -> list[Path]:
        """Search Windows registry for Prism installation"""
        paths = []
        try:
            import winreg
            registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            
            for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    key = winreg.OpenKey(hive, registry_path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "PrismLauncher" in display_name or "Prism Launcher" in display_name:
                                    try:
                                        install_loc = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                        if install_loc:
                                            paths.append(Path(install_loc))
                                    except (FileNotFoundError, OSError):
                                        pass
                            except (FileNotFoundError, OSError):
                                pass
                            finally:
                                subkey.Close()
                        except Exception:
                            pass
                    key.Close()
                except Exception:
                    pass
        except ImportError:
            pass
        
        return paths
    
    def _find_executable(self, directory: Path) -> Optional[Path]:
        """Find Prism executable in directory"""
        if sys.platform == 'win32':
            exe_names = ['PrismLauncher.exe', 'prismlauncher.exe']
        else:
            exe_names = ['prismlauncher', 'PrismLauncher']
        
        # Check direct path
        for name in exe_names:
            exe_path = directory / name
            if exe_path.exists():
                return exe_path
        
        # Check subdirectories (limited depth)
        for root, dirs, files in os.walk(str(directory)):
            depth = len(Path(root).relative_to(directory).parts)
            if depth > 3:
                dirs.clear()
                continue
            
            for name in exe_names:
                if name in files:
                    return Path(root) / name
        
        return None
    
    def _get_instances_path(self) -> Path:
        """Get Prism instances directory path"""
        # Instances are in %APPDATA%\PrismLauncher\instances (Windows)
        # or ~/.local/share/PrismLauncher/instances (Linux)
        
        if sys.platform == 'win32':
            base = Path(os.getenv('APPDATA', '')) / 'PrismLauncher'
        else:
            # Check Flatpak first
            flatpak_path = Path.home() / '.var' / 'app' / 'org.prismlauncher.PrismLauncher' / 'data' / 'PrismLauncher'
            if flatpak_path.exists():
                base = flatpak_path
            else:
                base = Path.home() / '.local' / 'share' / 'PrismLauncher'
        
        instances_path = base / 'instances'
        instances_path.mkdir(parents=True, exist_ok=True)
        return instances_path
    
    def create_instance(self) -> Optional[Path]:
        """Create a new Prism Launcher instance"""
        if not self.prism_instances_path:
            logger.error("No instances path available")
            return None
        
        try:
            # Find available instance name
            instance_dir = self.prism_instances_path / self.instance_name
            counter = 1
            while instance_dir.exists():
                instance_dir = self.prism_instances_path / f"{self.instance_name}-{counter}"
                counter += 1
            
            logger.info(f"Creating instance at: {instance_dir}")
            
            # Create instance directory
            instance_dir.mkdir(parents=True, exist_ok=True)
            
            # Create minecraft subdirectory (NOT .minecraft!)
            minecraft_dir = instance_dir / 'minecraft'
            minecraft_dir.mkdir(parents=True, exist_ok=True)
            
            # Create mmc-pack.json with correct component format
            mmc_pack_path = instance_dir / 'mmc-pack.json'
            mmc_pack_data = {
                "formatVersion": 1,
                "components": [
                    {
                        "cachedName": "LWJGL 3",
                        "cachedVersion": LWJGL_VERSION,
                        "cachedVolatile": True,
                        "dependencyOnly": True,
                        "uid": "org.lwjgl3",
                        "version": LWJGL_VERSION
                    },
                    {
                        "cachedName": "Minecraft",
                        "cachedRequires": [
                            {
                                "suggests": LWJGL_VERSION,
                                "uid": "org.lwjgl3"
                            }
                        ],
                        "cachedVersion": MINECRAFT_VERSION,
                        "important": True,
                        "uid": "net.minecraft",
                        "version": MINECRAFT_VERSION
                    },
                    {
                        "cachedName": "NeoForge",
                        "cachedRequires": [
                            {
                                "equals": MINECRAFT_VERSION,
                                "uid": "net.minecraft"
                            }
                        ],
                        "cachedVersion": NEOFORGE_VERSION,
                        "uid": "net.neoforged",
                        "version": NEOFORGE_VERSION
                    }
                ]
            }
            
            with open(mmc_pack_path, 'w', encoding='utf-8') as f:
                json.dump(mmc_pack_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Created mmc-pack.json at: {mmc_pack_path}")
            
            # Create instance.cfg
            instance_cfg_path = instance_dir / 'instance.cfg'
            instance_name_display = instance_dir.name
            
            cfg_content = f"""[General]
ConfigVersion=1.3
iconKey=neoforged
name={instance_name_display}
InstanceType=OneSix
"""
            
            with open(instance_cfg_path, 'w', encoding='utf-8') as f:
                f.write(cfg_content)
            
            logger.info(f"Created instance.cfg at: {instance_cfg_path}")
            
            return instance_dir
            
        except PermissionError:
            raise
        except Exception as e:
            logger.exception("Error creating instance")
            return None
    
    def copy_update_bat(self, instance_path: Path) -> bool:
        """Copy update.bat to instance minecraft directory"""
        minecraft_dir = instance_path / 'minecraft'
        
        # Find update.bat in multiple locations
        possible_paths = []
        
        # Next to script/executable
        script_dir = Path(__file__).parent
        possible_paths.append(script_dir / 'update.bat')
        
        # PyInstaller bundled resource
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
            possible_paths.append(base_path / 'update.bat')
        
        # Current working directory
        possible_paths.append(Path.cwd() / 'update.bat')
        
        # Parent of script directory
        possible_paths.append(script_dir.parent / 'update.bat')
        
        # Find existing update.bat
        source_path = None
        for path in possible_paths:
            if path.exists() and path.is_file():
                source_path = path
                logger.debug(f"Found update.bat at: {source_path}")
                break
        
        if not source_path:
            logger.error("Could not find update.bat")
            return False
        
        # Copy to destination
        dest_path = minecraft_dir / 'update.bat'
        try:
            shutil.copy2(source_path, dest_path)
            logger.info(f"Copied update.bat to {dest_path}")
            return True
        except PermissionError:
            raise
        except Exception as e:
            logger.exception("Error copying update.bat")
            return False
    
    def configure_instance(self, instance_path: Path) -> bool:
        """Configure instance settings (pre-launch, memory)"""
        instance_cfg_path = instance_path / 'instance.cfg'
        
        if not instance_cfg_path.exists():
            logger.error(f"Instance config not found: {instance_cfg_path}")
            return False
        
        try:
            # Read existing config
            config_dict = {}
            with open(instance_cfg_path, 'r', encoding='utf-8') as f:
                current_section = None
                for line in f:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        continue
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        config_dict[key.strip()] = value.strip()
            
            # Add/update settings
            config_dict['OverrideCommands'] = 'true'
            config_dict['PreLaunchCommand'] = PRE_LAUNCH_CMD
            config_dict['OverrideMemory'] = 'true'
            config_dict['MinMemAlloc'] = str(MIN_MEMORY)
            config_dict['MaxMemAlloc'] = str(MAX_MEMORY)
            config_dict['OverrideJavaLocation'] = 'false'
            
            # Write back with section header
            with open(instance_cfg_path, 'w', encoding='utf-8') as f:
                f.write("[General]\n")
                for key, value in config_dict.items():
                    f.write(f"{key}={value}\n")
            
            logger.info(f"Configured instance: {instance_cfg_path}")
            return True
            
        except PermissionError:
            raise
        except Exception as e:
            logger.exception("Error configuring instance")
            return False


def main():
    root = tk.Tk()
    
    # Set app icon if available (optional)
    try:
        if sys.platform == 'win32':
            root.iconbitmap(default='')
    except Exception:
        pass
    
    app = InstallerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
