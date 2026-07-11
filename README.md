# ⚡ Zodiac Optimizer

Ein Windows-Tweaking-Tool im Stil von **EXM** / **Paragon**: moderne Dark-Mode-Oberfläche,
Kategorien in der Seitenleiste, jeder Tweak einzeln per Schalter an- und ausschaltbar.

**Ziele:** weniger Hintergrundprozesse · mehr FPS · geringerer Input Delay

## 📦 Kategorien

| Kategorie | Inhalt |
|---|---|
| 🎮 FPS & Gaming | Game DVR aus, Spielmodus, GPU-Planung, Vollbildoptimierungen aus, Höchstleistungs-Energieplan, Spiele-Task-Priorität |
| ⚡ Input Delay | Mausbeschleunigung aus, Maus-/Tastatur-Warteschlangen, Vordergrund-Priorität, Einrastfunktion aus |
| 🧹 Prozesse & Dienste | Telemetrie, SysMain, Xbox-Dienste, Hintergrund-Apps, Cortana, Such-Indizierung |
| 🌐 Netzwerk & Latenz | Netzwerk-Drosselung aus, Nagle-Algorithmus aus (weniger Ping) |
| 🖥 Visuelle Effekte | Beste Leistung, Transparenz aus, Menü-Verzögerung entfernen |
| 🔒 Privatsphäre | Werbe-ID, Tipps/Vorschläge, Aktivitätsverlauf aus |

## 🛟 Sicherheit

- **Automatisches Backup:** Vor jedem Tweak wird der originale Registry-Zustand in
  `%APPDATA%\ZodiacOptimizer\backup.json` gesichert. Schalter aus = exakter Originalzustand zurück.
- **„Alles zurücksetzen“**-Knopf stellt sämtliche Tweaks wieder her.
- **Wiederherstellungspunkt** per Knopfdruck (empfohlen vor der ersten Nutzung!).
- Tweaks mit 🔁 benötigen einen Neustart, um zu wirken.

## 🔨 EXE bauen

Voraussetzung: [Python 3.10+](https://www.python.org/downloads/) installiert
(beim Installieren **„Add Python to PATH“** anhaken).

1. Repository herunterladen / klonen
2. `build.bat` doppelklicken
3. Fertige Datei: **`dist\ZodiacOptimizer.exe`**

Die EXE fordert beim Start automatisch Administratorrechte an (nötig für Registry & Dienste).

> Hinweis: Selbst gebaute, unsignierte EXEs werden von Windows SmartScreen beim ersten
> Start ggf. gewarnt („Trotzdem ausführen“) – das ist normal.

## ▶ Direkt aus dem Quellcode starten

```
pip install -r requirements.txt
python main.py
```

## ⚠️ Haftungsausschluss

Alle Tweaks sind bekannte, weit verbreitete Windows-Optimierungen und einzeln rückgängig
machbar. Trotzdem: Nutzung auf eigene Verantwortung – vorher Wiederherstellungspunkt erstellen.
