"""Local, per-user settings for FileOrganizer."""

from copy import deepcopy
import json
import os
from pathlib import Path


APP_NAME = "FileOrganizer"
SETTINGS_PATH = Path(os.environ.get("APPDATA", Path.home())) / APP_NAME / "settings.json"
INVALID_WINDOWS_CHARS = '<>:"/\\|?*'

DEFAULT_RULES = [
    {"name": "PDFs", "extensions": [".pdf"], "destination": "PDFs", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Images", "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"], "destination": "Images", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Videos", "extensions": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm"], "destination": "Videos", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Audio", "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"], "destination": "Audio", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Documents", "extensions": [".doc", ".docx", ".txt", ".rtf", ".odt"], "destination": "Documents", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Excel", "extensions": [".xls", ".xlsx", ".xlsm", ".csv", ".ods"], "destination": "Excel", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Presentations", "extensions": [".ppt", ".pptx", ".ppsx", ".odp"], "destination": "Presentations", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
    {"name": "Other", "extensions": [], "destination": "Other", "rename_enabled": False, "rename_pattern": "{original}", "starting_number": 1, "number_padding": 3},
]


def default_settings() -> dict:
    return {"version": 1, "rules": deepcopy(DEFAULT_RULES)}


def load_settings() -> dict:
    """Load settings, falling back safely to defaults when absent or invalid."""
    try:
        with SETTINGS_PATH.open("r", encoding="utf-8") as file:
            settings = json.load(file)
        if not isinstance(settings.get("rules"), list):
            raise ValueError("Missing rules")
        return settings
    except (OSError, ValueError, json.JSONDecodeError):
        return default_settings()


def save_settings(settings: dict) -> None:
    """Save settings under the current user's AppData directory."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SETTINGS_PATH.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)


def validate_rule(rule: dict, other_names: set[str] | None = None) -> list[str]:
    """Return clear validation errors for a client-editable rule."""
    errors = []
    name = rule.get("name", "").strip()
    destination = rule.get("destination", "").strip()
    pattern = rule.get("rename_pattern", "")
    if not name:
        errors.append("Category name is required.")
    elif any(char in name for char in INVALID_WINDOWS_CHARS) or name.endswith((".", " ")):
        errors.append("Category name contains invalid Windows filename characters.")
    elif other_names and name.casefold() in other_names:
        errors.append("Category names must be unique.")
    if not destination:
        errors.append("Destination folder is required.")
    elif any(char in destination for char in INVALID_WINDOWS_CHARS) or destination.endswith((".", " ")) or destination in {".", ".."}:
        errors.append("Destination must be one safe folder name.")
    if not isinstance(pattern, str) or not pattern.strip():
        errors.append("Rename pattern is required.")
    try:
        if int(rule.get("starting_number", 0)) < 0:
            errors.append("Starting number cannot be negative.")
    except (TypeError, ValueError):
        errors.append("Starting number must be a whole number.")
    for extension in rule.get("extensions", []):
        if not isinstance(extension, str) or not extension.startswith(".") or len(extension) == 1:
            errors.append("Extensions must start with a dot, for example .pdf.")
            break
    return errors


def validate_settings(settings: dict) -> list[str]:
    errors = []
    seen_names = set()
    seen_extensions = set()
    for rule in settings.get("rules", []):
        errors.extend(validate_rule(rule, seen_names))
        name = rule.get("name", "").strip().casefold()
        seen_names.add(name)
        for extension in rule.get("extensions", []):
            normalized = extension.lower()
            if normalized in seen_extensions:
                errors.append(f"Extension {normalized} is used by more than one category.")
            seen_extensions.add(normalized)
    if not settings.get("rules"):
        errors.append("At least one category is required.")
    return errors
