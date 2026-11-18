
import tkinter as tk
from tkinter import messagebox
import json
import os
from pathlib import Path
from datetime import datetime


# ==========================================
# 1. KLASSE AUFGABE
# ==========================================

class Aufgabe:

    def __init__(self, name, datum, erledigt=False):

        self.name = name
        self.datum = datum
        self.erledigt = erledigt

    def erledigen(self):

        self.erledigt = True

    def wieder_oeffnen(self):

        self.erledigt = False

    def als_dict(self):

        return {
            "name": self.name,
            "datum": self.datum,
            "erledigt": self.erledigt
        }


# ==========================================
# 2. KLASSE LERNPLANER
# ==========================================

class LernplanerApp:

    def __init__(self, fenster):

        self.fenster = fenster

        self.fenster.title("Mein Lernplaner")
        self.fenster.geometry("600x550")
        self.fenster.minsize(460, 450)

        # Speicherort festlegen

        self.app_ordner = Path(
            os.getenv("APPDATA", str(Path.home()))
        ) / "MeinLernplaner"

        self.datei = self.app_ordner / "aufgaben.json"

        # Interne Aufgabenliste

        self.aufgaben = []

        # Oberfläche erstellen

        self.oberflaeche_erstellen()

        # Gespeicherte Aufgaben laden

        self.laden()

        # Anzeige aktualisieren

        self.aktualisieren()

    # ======================================
    # 3. OBERFLÄCHE ERSTELLEN
    # ======================================

    def oberflaeche_erstellen(self):

        titel = tk.Label(
            self.fenster,
            text="Mein Lernplaner",
            font=("Arial", 22, "bold")
        )

        titel.pack(pady=(20, 5))

        untertitel = tk.Label(
            self.fenster,
            text="Organisiere deine schulischen Aufgaben"
        )

        untertitel.pack(pady=(0, 15))

        # Eingabe für den Aufgabennamen

        tk.Label(
            self.fenster,
            text="Aufgabe:"
        ).pack()

        self.eingabe = tk.Entry(
            self.fenster,
            font=("Arial", 12)
        )

        self.eingabe.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # Eingabe für das Datum

        tk.Label(
            self.fenster,
            text="Fälligkeitsdatum (TT.MM.JJJJ):"
        ).pack(pady=(8, 2))

        self.datum_eingabe = tk.Entry(
            self.fenster,
            font=("Arial", 12)
        )

        self.datum_eingabe.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # Button zum Hinzufügen

        tk.Button(
            self.fenster,
            text="Aufgabe hinzufügen",
            command=self.hinzufuegen
        ).pack(pady=8)

        # Enter-Taste zum Hinzufügen

        self.eingabe.bind(
            "<Return>",
            lambda event: self.hinzufuegen()
        )

        self.datum_eingabe.bind(
            "<Return>",
            lambda event: self.hinzufuegen()
        )

        # Listbox für die Aufgaben

        self.liste = tk.Listbox(
            self.fenster,
            font=("Arial", 11),
            height=12,
            selectmode=tk.SINGLE
        )

        self.liste.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        # Buttons für die Aufgabenverwaltung

        buttons = tk.Frame(self.fenster)

        buttons.pack(pady=5)

        tk.Button(
            buttons,
            text="Erledigt / Wieder öffnen",
            command=self.status_aendern
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Löschen",
            command=self.loeschen
        ).pack(side="left", padx=5)

        # Rückmeldungen anzeigen

        self.meldung = tk.Label(
            self.fenster,
            text=""
        )

        self.meldung.pack(pady=(5, 12))

    # ======================================
    # 4. AUFGABE HINZUFÜGEN
    # ======================================

    def hinzufuegen(self):

        name = self.eingabe.get().strip()
        datum = self.datum_eingabe.get().strip()

        # Prüfen, ob ein Name eingegeben wurde

        if not name:

            self.meldung.config(
                text="Bitte gib eine Aufgabe ein."
            )

            return

        # Prüfen, ob ein Datum eingegeben wurde

        if not datum:

            self.meldung.config(
                text="Bitte gib ein Datum ein."
            )

            return

        # Datum auf Gültigkeit prüfen

        try:

            datetime.strptime(
                datum,
                "%d.%m.%Y"
            )

        except ValueError:

            self.meldung.config(
                text="Ungültiges Datum! Format: TT.MM.JJJJ"
            )

            return

        # Neues Aufgabenobjekt erstellen

        neue_aufgabe = Aufgabe(
            name,
            datum
        )

        # Aufgabe zur internen Liste hinzufügen

        self.aufgaben.append(neue_aufgabe)

        # Speichern und Anzeige aktualisieren

        if self.speichern():

            self.aktualisieren()

            self.eingabe.delete(0, tk.END)
            self.datum_eingabe.delete(0, tk.END)

            self.meldung.config(
                text="Aufgabe erfolgreich gespeichert!"
            )

    # ======================================
    # 5. ANZEIGE AKTUALISIEREN
    # ======================================

    def aktualisieren(self):

        # Alte Anzeige löschen

        self.liste.delete(0, tk.END)

        # Alle Aufgaben erneut anzeigen

        for aufgabe in self.aufgaben:

            if aufgabe.erledigt:

                status = "✓ Erledigt"

            else:

                status = "○ Offen"

            text = (
                f"{status} | {aufgabe.name} "
                f"| Datum: {aufgabe.datum}"
            )

            self.liste.insert(
                tk.END,
                text
            )

    # ======================================
    # 6. STATUS ÄNDERN
    # ======================================

    def status_aendern(self):

        auswahl = self.liste.curselection()

        if not auswahl:

            self.meldung.config(
                text="Bitte wähle eine Aufgabe aus."
            )

            return

        # Index der ausgewählten Aufgabe bestimmen

        index = auswahl[0]

        aufgabe = self.aufgaben[index]

        # Status ändern

        if aufgabe.erledigt:

            aufgabe.wieder_oeffnen()

            nachricht = "Aufgabe wieder geöffnet!"

        else:

            aufgabe.erledigen()

            nachricht = "Aufgabe als erledigt markiert!"

        # Änderungen speichern

        if self.speichern():

            self.aktualisieren()

            self.liste.selection_set(index)

            self.meldung.config(
                text=nachricht
            )

    # ======================================
    # 7. AUFGABE LÖSCHEN
    # ======================================

    def loeschen(self):

        auswahl = self.liste.curselection()

        if not auswahl:

            self.meldung.config(
                text="Bitte wähle eine Aufgabe aus."
            )

            return

        # Ausgewählte Aufgabe bestimmen

        index = auswahl[0]

        aufgabe = self.aufgaben[index]

        # Sicherheitsabfrage

        bestaetigung = messagebox.askyesno(
            "Aufgabe löschen",
            f"Möchtest du diese Aufgabe wirklich löschen?\n\n"
            f"{aufgabe.name}"
        )

        if not bestaetigung:

            return

        # Aufgabe aus der internen Liste entfernen

        geloeschte_aufgabe = self.aufgaben.pop(index)

        # Änderungen speichern

        if self.speichern():

            self.aktualisieren()

            self.meldung.config(
                text="Aufgabe erfolgreich gelöscht!"
            )

        else:

            # Bei einem Speicherfehler Aufgabe zurücksetzen

            self.aufgaben.insert(
                index,
                geloeschte_aufgabe
            )

            self.aktualisieren()

    # ======================================
    # 8. AUFGABEN SPEICHERN
    # ======================================

    def speichern(self):

        try:

            # Speicherordner erstellen

            self.app_ordner.mkdir(
                parents=True,
                exist_ok=True
            )

            # Aufgabenobjekte in Dictionaries umwandeln

            daten = [
                aufgabe.als_dict()
                for aufgabe in self.aufgaben
            ]

            # Daten in JSON-Datei schreiben

            with open(
                self.datei,
                "w",
                encoding="utf-8"
            ) as datei:

                json.dump(
                    daten,
                    datei,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except OSError as fehler:

            messagebox.showerror(
                "Speicherfehler",
                f"Aufgaben konnten nicht gespeichert werden:\n{fehler}"
            )

            return False

    # ======================================
    # 9. AUFGABEN LADEN
    # ======================================

    def laden(self):

        try:

            # Speicherordner erstellen

            self.app_ordner.mkdir(
                parents=True,
                exist_ok=True
            )

            # Prüfen, ob die Datei existiert

            if not self.datei.exists():

                return

            # JSON-Datei öffnen

            with open(
                self.datei,
                "r",
                encoding="utf-8"
            ) as datei:

                daten = json.load(datei)

            if not isinstance(daten, list):

                raise ValueError(
                    "Ungültiges Datenformat."
                )

            # Gespeicherte Daten durchgehen

            for eintrag in daten:

                if not isinstance(eintrag, dict):

                    continue

                name = eintrag.get("name")
                datum = eintrag.get("datum", "")
                erledigt = eintrag.get("erledigt", False)

                # Daten überprüfen

                if (
                    isinstance(name, str)
                    and isinstance(datum, str)
                    and isinstance(erledigt, bool)
                ):

                    # Neues Aufgabenobjekt erstellen

                    aufgabe = Aufgabe(
                        name,
                        datum,
                        erledigt
                    )

                    # Objekt zur Aufgabenliste hinzufügen

                    self.aufgaben.append(aufgabe)

        except (
            OSError,
            json.JSONDecodeError,
            ValueError
        ) as fehler:

            messagebox.showerror(
                "Ladefehler",
                f"Aufgaben konnten nicht geladen werden:\n{fehler}"
            )


# ==========================================
# 10. PROGRAMM STARTEN
# ==========================================

fenster = tk.Tk()

app = LernplanerApp(fenster)

fenster.mainloop()
