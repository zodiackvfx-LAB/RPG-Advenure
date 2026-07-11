"""
Zodiac Optimizer – Windows-Tweaking-Tool
GUI im Stil von EXM / Paragon: Kategorien links, Tweaks mit Schaltern rechts.

Start (aus Quellcode):  python main.py
Build zur .exe:         build.bat ausführen
"""

import sys
import threading
import tkinter.messagebox as mb

import engine
from tweaks import CATEGORIES, all_tweaks

try:
    import customtkinter as ctk
except ImportError:
    print("CustomTkinter fehlt. Bitte ausführen:  pip install -r requirements.txt")
    sys.exit(1)

APP_NAME = "Zodiac Optimizer"
VERSION = "1.0.0"

ACCENT = "#7b5cff"
ACCENT_HOVER = "#6446e0"
BG_DARK = "#101018"
BG_CARD = "#181824"
BG_SIDEBAR = "#0b0b12"
TEXT_DIM = "#8a8a9e"


class ZodiacOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME}  v{VERSION}")
        self.geometry("1060x680")
        self.minsize(900, 560)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("dark")

        self.applied = engine.load_state()
        self.switches = {}          # tweak_id -> CTkSwitch
        self.current_category = None
        self.busy = False

        self._build_sidebar()
        self._build_main_area()
        self._select_category(next(iter(CATEGORIES)))

    # ------------------------------------------------------------- Sidebar

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=BG_SIDEBAR)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="⚡ ZODIAC", font=("Segoe UI", 26, "bold"),
                     text_color=ACCENT).pack(pady=(28, 0))
        ctk.CTkLabel(sidebar, text="OPTIMIZER", font=("Segoe UI", 13),
                     text_color=TEXT_DIM).pack(pady=(0, 24))

        self.category_buttons = {}
        for cat in CATEGORIES:
            btn = ctk.CTkButton(
                sidebar, text=cat, anchor="w", height=44, corner_radius=10,
                font=("Segoe UI", 14), fg_color="transparent",
                hover_color=BG_CARD, text_color="#d8d8e8",
                command=lambda c=cat: self._select_category(c),
            )
            btn.pack(fill="x", padx=14, pady=3)
            self.category_buttons[cat] = btn

        # Untere Aktionen
        bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=14, pady=16)

        ctk.CTkButton(bottom, text="🛟  Wiederherstellungspunkt", height=38,
                      corner_radius=10, fg_color=BG_CARD, hover_color="#22222f",
                      font=("Segoe UI", 12),
                      command=self._create_restore_point).pack(fill="x", pady=3)
        ctk.CTkButton(bottom, text="↩  Alles zurücksetzen", height=38,
                      corner_radius=10, fg_color=BG_CARD, hover_color="#3a1f28",
                      font=("Segoe UI", 12),
                      command=self._revert_all).pack(fill="x", pady=3)

    # ------------------------------------------------------------- Hauptbereich

    def _build_main_area(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=24, pady=18)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x")

        self.title_label = ctk.CTkLabel(header, text="", font=("Segoe UI", 24, "bold"),
                                        text_color="#f0f0fa")
        self.title_label.pack(side="left")

        self.apply_all_btn = ctk.CTkButton(
            header, text="✔  Alle anwenden", height=38, corner_radius=10,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, font=("Segoe UI", 13, "bold"),
            command=self._apply_category)
        self.apply_all_btn.pack(side="right")

        self.tweak_frame = ctk.CTkScrollableFrame(main, fg_color="transparent")
        self.tweak_frame.pack(fill="both", expand=True, pady=(14, 8))

        self.status = ctk.CTkLabel(main, text="Bereit.", anchor="w",
                                   font=("Segoe UI", 12), text_color=TEXT_DIM)
        self.status.pack(fill="x")

    def _select_category(self, category):
        self.current_category = category
        for cat, btn in self.category_buttons.items():
            btn.configure(fg_color=ACCENT if cat == category else "transparent",
                          text_color="#ffffff" if cat == category else "#d8d8e8")
        self.title_label.configure(text=category.split("  ", 1)[-1])

        for child in self.tweak_frame.winfo_children():
            child.destroy()
        self.switches = {}

        for tweak in CATEGORIES[category]:
            self._build_tweak_card(tweak)

    def _build_tweak_card(self, tweak):
        card = ctk.CTkFrame(self.tweak_frame, corner_radius=12, fg_color=BG_CARD)
        card.pack(fill="x", pady=5, padx=2)

        text = ctk.CTkFrame(card, fg_color="transparent")
        text.pack(side="left", fill="both", expand=True, padx=16, pady=12)

        name = tweak["name"] + ("   🔁" if tweak.get("reboot") else "")
        ctk.CTkLabel(text, text=name, anchor="w",
                     font=("Segoe UI", 14, "bold"), text_color="#eeeef8").pack(fill="x")
        ctk.CTkLabel(text, text=tweak["desc"], anchor="w", justify="left",
                     font=("Segoe UI", 12), text_color=TEXT_DIM,
                     wraplength=620).pack(fill="x")

        switch = ctk.CTkSwitch(card, text="", width=52, progress_color=ACCENT,
                               command=lambda t=tweak: self._toggle(t))
        switch.pack(side="right", padx=16)
        if tweak["id"] in self.applied:
            switch.select()
        self.switches[tweak["id"]] = switch

    # ------------------------------------------------------------- Aktionen

    def _set_status(self, text):
        self.after(0, lambda: self.status.configure(text=text))

    def _run_async(self, work, done_msg):
        """Führt Tweak-Arbeit im Hintergrund-Thread aus, damit die GUI nicht einfriert."""
        if self.busy:
            return
        self.busy = True

        def runner():
            try:
                work()
                self._set_status(done_msg)
            except PermissionError:
                self._set_status("❌ Zugriff verweigert – bitte als Administrator starten.")
            except Exception as exc:
                self._set_status(f"❌ Fehler: {exc}")
            finally:
                engine.save_state(self.applied)
                self.busy = False

        threading.Thread(target=runner, daemon=True).start()

    def _toggle(self, tweak):
        switch = self.switches[tweak["id"]]
        turn_on = switch.get() == 1

        def work():
            if turn_on:
                engine.apply_tweak(tweak)
                self.applied.add(tweak["id"])
            else:
                engine.revert_tweak(tweak)
                self.applied.discard(tweak["id"])

        hint = "  (Neustart empfohlen)" if tweak.get("reboot") else ""
        msg = (f"✔ „{tweak['name']}“ angewendet{hint}" if turn_on
               else f"↩ „{tweak['name']}“ zurückgesetzt{hint}")
        self._run_async(work, msg)

    def _apply_category(self):
        category = self.current_category
        tweaks = CATEGORIES[category]

        def work():
            for tweak in tweaks:
                if tweak["id"] not in self.applied:
                    self._set_status(f"⏳ Wende an: {tweak['name']} …")
                    engine.apply_tweak(tweak)
                    self.applied.add(tweak["id"])
                    tid = tweak["id"]
                    self.after(0, lambda t=tid: self.switches.get(t) and self.switches[t].select())

        reboot = any(t.get("reboot") for t in tweaks)
        hint = "  (Neustart empfohlen)" if reboot else ""
        self._run_async(work, f"✔ Alle Tweaks in „{category.split('  ', 1)[-1]}“ angewendet{hint}")

    def _revert_all(self):
        if not self.applied:
            self._set_status("Nichts zurückzusetzen.")
            return
        if not mb.askyesno(APP_NAME, "Wirklich ALLE angewendeten Tweaks auf den "
                                     "Originalzustand zurücksetzen?"):
            return

        def work():
            for tweak in all_tweaks():
                if tweak["id"] in self.applied:
                    self._set_status(f"⏳ Setze zurück: {tweak['name']} …")
                    engine.revert_tweak(tweak)
                    self.applied.discard(tweak["id"])
                    tid = tweak["id"]
                    self.after(0, lambda t=tid: self.switches.get(t) and self.switches[t].deselect())

        self._run_async(work, "↩ Alle Tweaks zurückgesetzt. Neustart empfohlen.")

    def _create_restore_point(self):
        def work():
            self._set_status("⏳ Erstelle Wiederherstellungspunkt … (kann 1–2 Minuten dauern)")
            engine.create_restore_point()
        self._run_async(work, "🛟 Wiederherstellungspunkt erstellt.")


def main():
    if not engine.IS_WINDOWS:
        print("Dieses Tool funktioniert nur unter Windows.")
        sys.exit(1)

    if not engine.is_admin():
        # Ohne Adminrechte neu starten (UAC-Dialog)
        engine.relaunch_as_admin()
        sys.exit(0)

    app = ZodiacOptimizer()
    app.mainloop()


if __name__ == "__main__":
    main()
