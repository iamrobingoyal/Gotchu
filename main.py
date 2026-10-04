"""Tkinter desktop interface for FileOrganizer."""

from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from config import default_settings, load_settings, save_settings, validate_rule, validate_settings
from organizer import build_filename, organize_files


def resource_path(relative_path: str) -> str:
    """Find a bundled asset in source mode and in a PyInstaller build."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str(base_path / relative_path)


class FileOrganizerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("File Organizer")
        self.iconbitmap(resource_path("assets/file_organizer.ico"))
        self.geometry("720x500")
        self.minsize(650, 430)
        self.settings = load_settings()
        self.source_folder = tk.StringVar()
        self.status = tk.StringVar(value="Ready. Choose a source folder.")
        self._build_ui()
        self.refresh_rules()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="FILE ORGANIZER", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Organize files locally using your saved rules.").pack(anchor="w", pady=(0, 14))

        source = ttk.LabelFrame(frame, text="Source Folder", padding=10)
        source.pack(fill="x")
        ttk.Entry(source, textvariable=self.source_folder).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(source, text="Browse", command=self.choose_folder).pack(side="right")

        rules = ttk.LabelFrame(frame, text="Rules", padding=8)
        rules.pack(fill="both", expand=True, pady=14)
        self.tree = ttk.Treeview(rules, columns=("extensions", "destination", "rename"), show="headings", height=9)
        self.tree.heading("extensions", text="Extensions")
        self.tree.heading("destination", text="Destination")
        self.tree.heading("rename", text="Renaming")
        self.tree.column("extensions", width=290)
        self.tree.column("destination", width=170)
        self.tree.column("rename", width=100)
        self.tree.pack(fill="both", expand=True)

        actions = ttk.Frame(frame)
        actions.pack(fill="x")
        ttk.Button(actions, text="Settings", command=self.open_settings).pack(side="left")
        ttk.Button(actions, text="Start Organizing", command=self.start_organizing).pack(side="right")
        ttk.Label(frame, textvariable=self.status, foreground="#245a85").pack(anchor="w", pady=(14, 0))

    def choose_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self, title="Choose a folder to organize")
        if folder:
            self.source_folder.set(folder)
            self.status.set("Ready to organize the selected folder.")

    def refresh_rules(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for rule in self.settings["rules"]:
            extensions = ", ".join(rule["extensions"]) or "All other extensions"
            renaming = "On" if rule["rename_enabled"] else "Off"
            self.tree.insert("", "end", values=(f"{rule['name']}: {extensions}", rule["destination"], renaming))

    def open_settings(self) -> None:
        SettingsDialog(self, self.settings, self.save_settings)

    def save_settings(self, settings: dict) -> None:
        self.settings = settings
        save_settings(settings)
        self.refresh_rules()
        self.status.set("Settings saved for this Windows user.")

    def start_organizing(self) -> None:
        folder_text = self.source_folder.get().strip()
        if not folder_text:
            messagebox.showwarning("Choose a folder", "Choose a source folder first.", parent=self)
            return
        folder = Path(folder_text)
        if not folder.is_dir():
            messagebox.showerror("Folder not found", "The selected source folder is not available.", parent=self)
            return
        errors = validate_settings(self.settings)
        if errors:
            messagebox.showerror("Settings need attention", "\n".join(errors), parent=self)
            return
        self.status.set("Organizing files...")
        self.update_idletasks()
        summary = organize_files(folder, self.settings["rules"])
        self.status.set(f"Complete: {summary['moved']} moved, {summary['skipped']} skipped.")
        SummaryDialog(self, summary)


class SettingsDialog(tk.Toplevel):
    def __init__(self, parent: FileOrganizerApp, settings: dict, save_callback) -> None:
        super().__init__(parent)
        self.title("File Organizer Settings")
        self.geometry("800x470")
        self.transient(parent)
        self.grab_set()
        self.settings = {"version": settings.get("version", 1), "rules": [rule.copy() | {"extensions": list(rule["extensions"])} for rule in settings["rules"]]}
        self.save_callback = save_callback
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=14)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="SETTINGS", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Rules are saved locally and apply to future organizing runs.").pack(anchor="w", pady=(0, 10))
        self.tree = ttk.Treeview(frame, columns=("name", "extensions", "destination", "rename", "pattern", "number"), show="headings")
        for key, title, width in (("name", "Category", 110), ("extensions", "Extensions", 160), ("destination", "Destination", 110), ("rename", "Rename", 60), ("pattern", "Pattern", 210), ("number", "Start", 55)):
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True)
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=10)
        ttk.Button(buttons, text="Add Rule", command=self.add_rule).pack(side="left")
        ttk.Button(buttons, text="Edit Rule", command=self.edit_rule).pack(side="left", padx=6)
        ttk.Button(buttons, text="Delete Rule", command=self.delete_rule).pack(side="left")
        ttk.Button(buttons, text="Reset Defaults", command=self.reset_defaults).pack(side="left", padx=6)
        ttk.Button(buttons, text="Save Settings", command=self.save).pack(side="right")

    def refresh(self) -> None:
        for item in self.tree.get_children(): self.tree.delete(item)
        for index, rule in enumerate(self.settings["rules"]):
            start = str(rule["starting_number"]).zfill(rule.get("number_padding", 3))
            self.tree.insert("", "end", iid=str(index), values=(rule["name"], ", ".join(rule["extensions"]) or "Other", rule["destination"], "On" if rule["rename_enabled"] else "Off", rule["rename_pattern"], start))

    def selected_index(self) -> int | None:
        selected = self.tree.selection()
        return int(selected[0]) if selected else None

    def add_rule(self) -> None:
        RuleDialog(self, None, self.apply_rule)

    def edit_rule(self) -> None:
        index = self.selected_index()
        if index is None:
            messagebox.showinfo("Select a rule", "Select a rule to edit.", parent=self)
            return
        RuleDialog(self, self.settings["rules"][index], lambda rule: self.apply_rule(rule, index))

    def apply_rule(self, rule: dict, index: int | None = None) -> None:
        if index is None: self.settings["rules"].append(rule)
        else: self.settings["rules"][index] = rule
        self.refresh()

    def delete_rule(self) -> None:
        index = self.selected_index()
        if index is None: return
        if messagebox.askyesno("Delete rule", f"Delete '{self.settings['rules'][index]['name']}'?", parent=self):
            del self.settings["rules"][index]
            self.refresh()

    def reset_defaults(self) -> None:
        if messagebox.askyesno("Reset settings", "Replace all current rules with defaults?", parent=self):
            self.settings = default_settings()
            self.refresh()

    def save(self) -> None:
        errors = validate_settings(self.settings)
        if errors:
            messagebox.showerror("Settings need attention", "\n".join(errors), parent=self)
            return
        self.save_callback(self.settings)
        self.destroy()


class RuleDialog(tk.Toplevel):
    def __init__(self, parent: SettingsDialog, rule: dict | None, on_save) -> None:
        super().__init__(parent)
        self.title("Edit Rule" if rule else "Add Rule")
        self.transient(parent); self.grab_set(); self.on_save = on_save
        rule = rule or {"name": "", "extensions": [], "destination": "", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3}
        self.name = tk.StringVar(value=rule["name"])
        self.extensions = tk.StringVar(value=", ".join(rule["extensions"]))
        self.destination = tk.StringVar(value=rule["destination"])
        self.rename_enabled = tk.BooleanVar(value=rule["rename_enabled"])
        self.pattern = tk.StringVar(value=rule["rename_pattern"])
        self.start = tk.StringVar(value=str(rule["starting_number"]).zfill(rule.get("number_padding", 3)))
        self.preview = tk.StringVar()
        frame = ttk.Frame(self, padding=14); frame.pack(fill="both", expand=True)
        for row, (label, variable) in enumerate((("Category", self.name), ("Extensions (comma separated)", self.extensions), ("Destination folder", self.destination), ("Rename pattern", self.pattern), ("Starting number", self.start))):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=4)
            ttk.Entry(frame, textvariable=variable, width=48).grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Checkbutton(frame, text="Rename files", variable=self.rename_enabled, command=self.update_preview).grid(row=5, column=1, sticky="w", pady=5)
        ttk.Label(frame, text="Preview").grid(row=6, column=0, sticky="w", pady=4)
        ttk.Label(frame, textvariable=self.preview, foreground="#245a85").grid(row=6, column=1, sticky="w", pady=4)
        ttk.Label(frame, text="Placeholders: {original} {date} {time} {datetime} {number} {extension}", wraplength=360).grid(row=7, column=1, sticky="w", pady=(0, 8))
        ttk.Button(frame, text="Save Rule", command=self.save).grid(row=8, column=1, sticky="e")
        frame.columnconfigure(1, weight=1)
        for variable in (self.name, self.extensions, self.destination, self.pattern, self.start): variable.trace_add("write", lambda *_: self.update_preview())
        self.update_preview()

    def current_rule(self) -> dict:
        start_text = self.start.get().strip()
        start = int(start_text) if start_text.isdigit() else -1
        extensions = [item.strip().lower() for item in self.extensions.get().split(",") if item.strip()]
        return {"name": self.name.get().strip(), "extensions": extensions, "destination": self.destination.get().strip(), "rename_enabled": self.rename_enabled.get(), "rename_pattern": self.pattern.get(), "starting_number": start, "number_padding": max(1, len(start_text))}

    def update_preview(self) -> None:
        try: self.preview.set(build_filename(Path("invoice123.pdf"), self.current_rule(), max(0, int(self.start.get() or 0))))
        except (ValueError, TypeError): self.preview.set("Enter a whole-number starting value")

    def save(self) -> None:
        rule = self.current_rule(); errors = validate_rule(rule)
        if errors:
            messagebox.showerror("Rule needs attention", "\n".join(errors), parent=self); return
        self.on_save(rule); self.destroy()


class SummaryDialog(tk.Toplevel):
    def __init__(self, parent: FileOrganizerApp, summary: dict) -> None:
        super().__init__(parent); self.title("Organization Complete"); self.transient(parent)
        frame = ttk.Frame(self, padding=16); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="ORGANIZATION COMPLETE", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(frame, text=f"Files scanned: {summary['processed']}\nFiles moved: {summary['moved']}\nFiles skipped: {summary['skipped']}\nRenamed: {summary['renamed']}").pack(anchor="w", pady=10)
        details = "\n".join(summary["details"] + summary["errors"]) or "No files found."
        ttk.Label(frame, text="Details").pack(anchor="w")
        box = tk.Text(frame, height=10, width=75, wrap="word"); box.pack(fill="both", expand=True)
        box.insert("1.0", details); box.configure(state="disabled")
        ttk.Button(frame, text="Close", command=self.destroy).pack(anchor="e", pady=(10, 0))


if __name__ == "__main__":
    FileOrganizerApp().mainloop()
