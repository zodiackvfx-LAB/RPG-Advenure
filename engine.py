"""
Zodiac Optimizer – Engine
Kümmert sich um Registry-Zugriffe, Backups, Dienste und Befehle.

Sicherheitskonzept:
 - Vor jedem Tweak wird der aktuelle Registry-Zustand in eine Backup-Datei
   (%APPDATA%\\ZodiacOptimizer\\backup.json) geschrieben.
 - Beim Zurücksetzen wird exakt der vorherige Zustand wiederhergestellt
   (inkl. Löschen von Werten, die vorher nicht existierten).
 - Zusätzlich kann per Knopfdruck ein Windows-Wiederherstellungspunkt
   erstellt werden.
"""

import json
import os
import subprocess
import sys

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import ctypes
    import winreg

APP_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "ZodiacOptimizer")
BACKUP_FILE = os.path.join(APP_DIR, "backup.json")
STATE_FILE = os.path.join(APP_DIR, "state.json")

HIVES = {}
TYPES = {}
if IS_WINDOWS:
    HIVES = {
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKCU": winreg.HKEY_CURRENT_USER,
    }
    TYPES = {
        "dword": winreg.REG_DWORD,
        "sz": winreg.REG_SZ,
    }


# ---------------------------------------------------------------- Hilfsdateien

def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_json(path, data):
    os.makedirs(APP_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_state():
    """Gibt die Menge der aktuell angewendeten Tweak-IDs zurück."""
    return set(_load_json(STATE_FILE).get("applied", []))


def save_state(applied_ids):
    _save_json(STATE_FILE, {"applied": sorted(applied_ids)})


# ---------------------------------------------------------------- Admin-Check

def is_admin():
    if not IS_WINDOWS:
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin():
    """Startet das Programm mit Admin-Rechten neu (UAC-Abfrage)."""
    if getattr(sys, "frozen", False):
        exe, params = sys.executable, " ".join(f'"{a}"' for a in sys.argv[1:])
    else:
        exe = sys.executable
        params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1)


# ---------------------------------------------------------------- Registry

def _open_key(hive, path, write=False):
    access = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    if write:
        access |= winreg.KEY_SET_VALUE
        return winreg.CreateKeyEx(HIVES[hive], path, 0, access)
    return winreg.OpenKeyEx(HIVES[hive], path, 0, access)


def _read_value(hive, path, name):
    """Liest einen Registry-Wert. Gibt (existiert, wert, typ) zurück."""
    try:
        with _open_key(hive, path) as key:
            value, vtype = winreg.QueryValueEx(key, name)
            return True, value, vtype
    except FileNotFoundError:
        return False, None, None


def _write_value(hive, path, name, vtype, value):
    with _open_key(hive, path, write=True) as key:
        winreg.SetValueEx(key, name, 0, vtype, value)


def _delete_value(hive, path, name):
    try:
        with _open_key(hive, path, write=True) as key:
            winreg.DeleteValue(key, name)
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------- Befehle

def _run_commands(commands):
    """Führt eine Liste von Shell-Befehlen unsichtbar aus."""
    for cmd in commands:
        flags = subprocess.CREATE_NO_WINDOW if IS_WINDOWS else 0
        subprocess.run(cmd, shell=True, creationflags=flags,
                       capture_output=True, timeout=120)


# ---------------------------------------------------------------- Tweaks

def apply_tweak(tweak):
    """Wendet einen Tweak an: erst Backup, dann Registry + Befehle."""
    backups = _load_json(BACKUP_FILE)
    entries = []
    for reg in tweak.get("registry", []):
        existed, value, vtype = _read_value(reg["hive"], reg["path"], reg["name"])
        entries.append({
            "hive": reg["hive"], "path": reg["path"], "name": reg["name"],
            "existed": existed, "value": value, "type": vtype,
        })
    # Backup nur beim ersten Anwenden speichern, damit der Originalzustand
    # nicht durch mehrfaches Umschalten überschrieben wird.
    if tweak["id"] not in backups:
        backups[tweak["id"]] = entries
        _save_json(BACKUP_FILE, backups)

    for reg in tweak.get("registry", []):
        _write_value(reg["hive"], reg["path"], reg["name"],
                     TYPES[reg["type"]], reg["value"])
    _run_commands(tweak.get("commands", []))


def revert_tweak(tweak):
    """Setzt einen Tweak auf den gesicherten Originalzustand zurück."""
    backups = _load_json(BACKUP_FILE)
    entries = backups.get(tweak["id"])

    if entries is not None:
        for e in entries:
            if e["existed"]:
                _write_value(e["hive"], e["path"], e["name"], e["type"], e["value"])
            else:
                _delete_value(e["hive"], e["path"], e["name"])
        del backups[tweak["id"]]
        _save_json(BACKUP_FILE, backups)
    else:
        # Kein Backup vorhanden -> dokumentierte Windows-Standardwerte nutzen
        for reg in tweak.get("registry", []):
            if "default" in reg:
                _write_value(reg["hive"], reg["path"], reg["name"],
                             TYPES[reg["type"]], reg["default"])
            else:
                _delete_value(reg["hive"], reg["path"], reg["name"])

    _run_commands(tweak.get("revert_commands", []))


def create_restore_point():
    """Erstellt einen System-Wiederherstellungspunkt."""
    _run_commands([
        'powershell -NoProfile -Command "Checkpoint-Computer '
        '-Description \'Zodiac Optimizer\' -RestorePointType MODIFY_SETTINGS"'
    ])
