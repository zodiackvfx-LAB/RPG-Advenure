"""
Zodiac Optimizer – Tweak-Definitionen

Jeder Tweak:
  id              eindeutige Kennung (für Backup & Status)
  name            Anzeigename
  desc            kurze Beschreibung
  reboot          True = Neustart empfohlen
  registry        Liste von Registry-Werten, die gesetzt werden
                  (hive, path, name, type, value[, default für Revert ohne Backup])
  commands        Shell-Befehle beim Anwenden
  revert_commands Shell-Befehle beim Zurücksetzen
"""

CATEGORIES = {
    "🎮  FPS & Gaming": [
        {
            "id": "game_dvr_off",
            "name": "Game DVR / Xbox-Aufnahme deaktivieren",
            "desc": "Schaltet Hintergrund-Aufnahmen ab – spürbar mehr FPS in Spielen.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"System\GameConfigStore",
                 "name": "GameDVR_Enabled", "type": "dword", "value": 0, "default": 1},
                {"hive": "HKCU", "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR",
                 "name": "AppCaptureEnabled", "type": "dword", "value": 0, "default": 1},
                {"hive": "HKLM", "path": r"SOFTWARE\Policies\Microsoft\Windows\GameDVR",
                 "name": "AllowGameDVR", "type": "dword", "value": 0},
            ],
        },
        {
            "id": "game_mode_on",
            "name": "Windows-Spielmodus aktivieren",
            "desc": "Priorisiert Spiele gegenüber Hintergrundprozessen.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"SOFTWARE\Microsoft\GameBar",
                 "name": "AutoGameModeEnabled", "type": "dword", "value": 1},
                {"hive": "HKCU", "path": r"SOFTWARE\Microsoft\GameBar",
                 "name": "AllowAutoGameMode", "type": "dword", "value": 1},
            ],
        },
        {
            "id": "gpu_scheduling",
            "name": "Hardwarebeschleunigte GPU-Planung",
            "desc": "GPU verwaltet ihren Speicher selbst – weniger Latenz (Win10 2004+, moderne GPU).",
            "reboot": True,
            "registry": [
                {"hive": "HKLM", "path": r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                 "name": "HwSchMode", "type": "dword", "value": 2, "default": 1},
            ],
        },
        {
            "id": "fse_off",
            "name": "Vollbildoptimierungen deaktivieren",
            "desc": "Erzwingt echtes exklusives Vollbild – bessere Frametimes und weniger Input-Lag.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"System\GameConfigStore",
                 "name": "GameDVR_FSEBehaviorMode", "type": "dword", "value": 2, "default": 0},
                {"hive": "HKCU", "path": r"System\GameConfigStore",
                 "name": "GameDVR_HonorUserFSEBehaviorMode", "type": "dword", "value": 1, "default": 0},
                {"hive": "HKCU", "path": r"System\GameConfigStore",
                 "name": "GameDVR_EFSEFeatureFlags", "type": "dword", "value": 0},
                {"hive": "HKCU", "path": r"System\GameConfigStore",
                 "name": "GameDVR_DXGIHonorFSEWindowsCompatible", "type": "dword", "value": 1, "default": 0},
            ],
        },
        {
            "id": "power_plan_high",
            "name": "Energieplan „Höchstleistung“ aktivieren",
            "desc": "CPU taktet nicht mehr herunter – konstante Leistung in Spielen.",
            "reboot": False,
            "commands": ["powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
            "revert_commands": ["powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"],
        },
        {
            "id": "games_task_priority",
            "name": "GPU-/CPU-Priorität für Spiele erhöhen",
            "desc": "Windows-Scheduler stuft Spiele als hochpriorisierte Tasks ein.",
            "reboot": True,
            "registry": [
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "name": "GPU Priority", "type": "dword", "value": 8, "default": 2},
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "name": "Priority", "type": "dword", "value": 6, "default": 2},
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "name": "Scheduling Category", "type": "sz", "value": "High", "default": "Medium"},
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
                 "name": "SFIO Priority", "type": "sz", "value": "High", "default": "Normal"},
            ],
        },
    ],

    "⚡  Input Delay": [
        {
            "id": "mouse_accel_off",
            "name": "Mausbeschleunigung deaktivieren",
            "desc": "1:1-Mausbewegung ohne Windows-Beschleunigung – Pflicht für präzises Aiming.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"Control Panel\Mouse",
                 "name": "MouseSpeed", "type": "sz", "value": "0", "default": "1"},
                {"hive": "HKCU", "path": r"Control Panel\Mouse",
                 "name": "MouseThreshold1", "type": "sz", "value": "0", "default": "6"},
                {"hive": "HKCU", "path": r"Control Panel\Mouse",
                 "name": "MouseThreshold2", "type": "sz", "value": "0", "default": "10"},
            ],
        },
        {
            "id": "mouse_queue",
            "name": "Maus-Datenwarteschlange verkleinern",
            "desc": "Kleinerer Puffer im Maustreiber = geringere Eingabeverzögerung.",
            "reboot": True,
            "registry": [
                {"hive": "HKLM", "path": r"SYSTEM\CurrentControlSet\Services\mouclass\Parameters",
                 "name": "MouseDataQueueSize", "type": "dword", "value": 20, "default": 100},
            ],
        },
        {
            "id": "keyboard_queue",
            "name": "Tastatur-Datenwarteschlange verkleinern",
            "desc": "Kleinerer Puffer im Tastaturtreiber = schnellere Tasteneingaben.",
            "reboot": True,
            "registry": [
                {"hive": "HKLM", "path": r"SYSTEM\CurrentControlSet\Services\kbdclass\Parameters",
                 "name": "KeyboardDataQueueSize", "type": "dword", "value": 20, "default": 100},
            ],
        },
        {
            "id": "priority_separation",
            "name": "Vordergrund-Priorität optimieren (Win32PrioritySeparation)",
            "desc": "Das aktive Programm (dein Spiel) bekommt mehr CPU-Zeitscheiben.",
            "reboot": False,
            "registry": [
                {"hive": "HKLM", "path": r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                 "name": "Win32PrioritySeparation", "type": "dword", "value": 38, "default": 2},
            ],
        },
        {
            "id": "sticky_keys_off",
            "name": "Einrast-/Filter-/Umschalttasten deaktivieren",
            "desc": "Keine nervigen Popups mehr bei mehrfachem Shift-Drücken im Spiel.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"Control Panel\Accessibility\StickyKeys",
                 "name": "Flags", "type": "sz", "value": "506", "default": "510"},
                {"hive": "HKCU", "path": r"Control Panel\Accessibility\Keyboard Response",
                 "name": "Flags", "type": "sz", "value": "122", "default": "126"},
                {"hive": "HKCU", "path": r"Control Panel\Accessibility\ToggleKeys",
                 "name": "Flags", "type": "sz", "value": "58", "default": "62"},
            ],
        },
    ],

    "🧹  Prozesse & Dienste": [
        {
            "id": "telemetry_off",
            "name": "Telemetrie-Dienst (DiagTrack) deaktivieren",
            "desc": "Stoppt den Datensammel-Dienst von Microsoft – weniger Hintergrundlast.",
            "reboot": False,
            "registry": [
                {"hive": "HKLM", "path": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                 "name": "AllowTelemetry", "type": "dword", "value": 0},
            ],
            "commands": [
                "sc stop DiagTrack", "sc config DiagTrack start= disabled",
            ],
            "revert_commands": [
                "sc config DiagTrack start= auto", "sc start DiagTrack",
            ],
        },
        {
            "id": "sysmain_off",
            "name": "SysMain (Superfetch) deaktivieren",
            "desc": "Beendet aggressives Vorab-Laden – hilft besonders bei SSDs.",
            "reboot": False,
            "commands": [
                "sc stop SysMain", "sc config SysMain start= disabled",
            ],
            "revert_commands": [
                "sc config SysMain start= auto", "sc start SysMain",
            ],
        },
        {
            "id": "xbox_services_off",
            "name": "Xbox-Dienste deaktivieren",
            "desc": "Vier Xbox-Hintergrunddienste aus (nicht nutzen, wenn du Xbox-App/Game Pass brauchst).",
            "reboot": False,
            "commands": [
                "sc stop XblAuthManager", "sc config XblAuthManager start= disabled",
                "sc stop XblGameSave", "sc config XblGameSave start= disabled",
                "sc stop XboxNetApiSvc", "sc config XboxNetApiSvc start= disabled",
                "sc stop XboxGipSvc", "sc config XboxGipSvc start= disabled",
            ],
            "revert_commands": [
                "sc config XblAuthManager start= demand",
                "sc config XblGameSave start= demand",
                "sc config XboxNetApiSvc start= demand",
                "sc config XboxGipSvc start= demand",
            ],
        },
        {
            "id": "background_apps_off",
            "name": "Hintergrund-Apps deaktivieren",
            "desc": "Store-Apps laufen nicht mehr unsichtbar im Hintergrund weiter.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications",
                 "name": "GlobalUserDisabled", "type": "dword", "value": 1, "default": 0},
            ],
        },
        {
            "id": "cortana_off",
            "name": "Cortana deaktivieren",
            "desc": "Entfernt Cortana aus Suche und Hintergrund.",
            "reboot": True,
            "registry": [
                {"hive": "HKLM", "path": r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                 "name": "AllowCortana", "type": "dword", "value": 0},
            ],
        },
        {
            "id": "search_indexer_off",
            "name": "Such-Indizierung (WSearch) deaktivieren",
            "desc": "Achtung: Windows-Suche wird langsamer – dafür keine Indexer-Last beim Zocken.",
            "reboot": False,
            "commands": [
                "sc stop WSearch", "sc config WSearch start= disabled",
            ],
            "revert_commands": [
                "sc config WSearch start= delayed-auto", "sc start WSearch",
            ],
        },
    ],

    "🌐  Netzwerk & Latenz": [
        {
            "id": "network_throttling_off",
            "name": "Netzwerk-Drosselung deaktivieren",
            "desc": "Windows drosselt Netzwerkpakete bei Multimedia-Last – das schaltet es ab.",
            "reboot": True,
            "registry": [
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                 "name": "NetworkThrottlingIndex", "type": "dword", "value": 0xFFFFFFFF, "default": 10},
                {"hive": "HKLM",
                 "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                 "name": "SystemResponsiveness", "type": "dword", "value": 10, "default": 20},
            ],
        },
        {
            "id": "nagle_off",
            "name": "Nagle-Algorithmus deaktivieren (TCP)",
            "desc": "Sendet TCP-Pakete sofort statt gebündelt – geringerer Ping in Online-Spielen.",
            "reboot": True,
            "commands": [
                'powershell -NoProfile -Command "Get-ChildItem '
                "'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | "
                "ForEach-Object { Set-ItemProperty $_.PSPath -Name TcpAckFrequency -Value 1 -Type DWord; "
                'Set-ItemProperty $_.PSPath -Name TCPNoDelay -Value 1 -Type DWord }"',
            ],
            "revert_commands": [
                'powershell -NoProfile -Command "Get-ChildItem '
                "'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | "
                "ForEach-Object { Remove-ItemProperty $_.PSPath -Name TcpAckFrequency -ErrorAction SilentlyContinue; "
                'Remove-ItemProperty $_.PSPath -Name TCPNoDelay -ErrorAction SilentlyContinue }"',
            ],
        },
    ],

    "🖥  Visuelle Effekte": [
        {
            "id": "visual_fx_performance",
            "name": "Visuelle Effekte auf „Beste Leistung“",
            "desc": "Deaktiviert Animationen und Schatten – entlastet GPU und Desktop.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                 "name": "VisualFXSetting", "type": "dword", "value": 2, "default": 0},
            ],
        },
        {
            "id": "transparency_off",
            "name": "Transparenz-Effekte deaktivieren",
            "desc": "Kein Acryl-/Blur-Effekt mehr – weniger GPU-Last im Desktopbetrieb.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                 "name": "EnableTransparency", "type": "dword", "value": 0, "default": 1},
            ],
        },
        {
            "id": "menu_delay",
            "name": "Menü-Verzögerung entfernen",
            "desc": "Kontextmenüs öffnen sofort statt nach 400 ms.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU", "path": r"Control Panel\Desktop",
                 "name": "MenuShowDelay", "type": "sz", "value": "0", "default": "400"},
            ],
        },
    ],

    "🔒  Privatsphäre": [
        {
            "id": "advertising_id_off",
            "name": "Werbe-ID deaktivieren",
            "desc": "Apps können dich nicht mehr über die Werbe-ID tracken.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                 "name": "Enabled", "type": "dword", "value": 0, "default": 1},
            ],
        },
        {
            "id": "tips_suggestions_off",
            "name": "Tipps, Vorschläge & App-Werbung deaktivieren",
            "desc": "Keine automatisch installierten Apps und Vorschläge mehr im Startmenü.",
            "reboot": False,
            "registry": [
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                 "name": "SubscribedContent-338389Enabled", "type": "dword", "value": 0, "default": 1},
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                 "name": "SystemPaneSuggestionsEnabled", "type": "dword", "value": 0, "default": 1},
                {"hive": "HKCU",
                 "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                 "name": "SilentInstalledAppsEnabled", "type": "dword", "value": 0, "default": 1},
            ],
        },
        {
            "id": "activity_history_off",
            "name": "Aktivitätsverlauf deaktivieren",
            "desc": "Windows sammelt und sendet keinen Aktivitätsverlauf mehr.",
            "reboot": False,
            "registry": [
                {"hive": "HKLM", "path": r"SOFTWARE\Policies\Microsoft\Windows\System",
                 "name": "EnableActivityFeed", "type": "dword", "value": 0},
                {"hive": "HKLM", "path": r"SOFTWARE\Policies\Microsoft\Windows\System",
                 "name": "PublishUserActivities", "type": "dword", "value": 0},
            ],
        },
    ],
}


def all_tweaks():
    for tweaks in CATEGORIES.values():
        yield from tweaks
