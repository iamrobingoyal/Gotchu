"""Safe file scanning, categorization, renaming, and moving logic."""

from datetime import datetime
from pathlib import Path
import shutil

from config import INVALID_WINDOWS_CHARS, default_settings


def get_category(file_path: Path, rules: list[dict] | None = None) -> dict:
    """Return the matching rule, using Other as the fallback when available."""
    rules = rules or default_settings()["rules"]
    extension = file_path.suffix.lower()
    fallback = next((rule for rule in rules if rule["name"].casefold() == "other"), None)
    return next((rule for rule in rules if extension and extension in [item.lower() for item in rule.get("extensions", [])]), fallback or rules[0])


def sanitize_filename(name: str, extension: str) -> str:
    """Make a safe Windows filename while retaining the original extension."""
    safe = "".join("_" if char in INVALID_WINDOWS_CHARS or ord(char) < 32 else char for char in name)
    safe = safe.strip().rstrip(".") or "file"
    extension = extension if extension.startswith(".") else f".{extension}" if extension else ""
    max_stem_length = max(1, 180 - len(extension))
    return f"{safe[:max_stem_length]}{extension}"


def build_filename(file_path: Path, rule: dict, number: int, now: datetime | None = None) -> str:
    """Build a safe output filename from a configured rule without writing files."""
    if not rule.get("rename_enabled", False):
        return file_path.name
    now = now or datetime.now()
    padding = max(1, int(rule.get("number_padding", 3)))
    extension = file_path.suffix
    values = {
        "original": file_path.stem,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H-%M-%S"),
        "datetime": now.strftime("%Y-%m-%d_%H-%M-%S"),
        "number": str(number).zfill(padding),
        "extension": extension,
    }
    try:
        base_name = rule.get("rename_pattern", "{original}").format(**values)
    except (KeyError, ValueError):
        base_name = file_path.stem
    # A pattern containing {extension} already supplied it; otherwise preserve it.
    suffix = "" if "{extension}" in rule.get("rename_pattern", "") else extension
    return sanitize_filename(base_name, suffix)


def get_unique_destination(destination_folder: Path, file_name: str) -> Path:
    """Return a non-existing destination, never replacing an existing file."""
    original = Path(file_name)
    candidate = destination_folder / file_name
    number = 1
    while candidate.exists():
        candidate = destination_folder / sanitize_filename(f"{original.stem}_{number}", original.suffix)
        number += 1
    return candidate


def organize_files(folder: Path, rules: list[dict] | None = None) -> dict:
    """Organize direct files in folder using rules and return a detailed summary."""
    rules = rules or default_settings()["rules"]
    summary = {"processed": 0, "moved": 0, "skipped": 0, "renamed": 0, "errors": [], "details": []}
    counters = {rule["name"]: int(rule.get("starting_number", 1)) for rule in rules}
    try:
        files = [item for item in folder.iterdir() if item.is_file()]
    except OSError as error:
        summary["errors"].append(f"Could not scan '{folder}': {error}")
        return summary

    for file_path in files:
        summary["processed"] += 1
        try:
            rule = get_category(file_path, rules)
            destination_folder = folder / rule["destination"]
            destination_folder.mkdir(exist_ok=True)
            number = counters[rule["name"]]
            new_name = build_filename(file_path, rule, number)
            destination = get_unique_destination(destination_folder, new_name)
            shutil.move(str(file_path), str(destination))
            counters[rule["name"]] += 1
            summary["moved"] += 1
            if destination.name != file_path.name:
                summary["renamed"] += 1
            summary["details"].append(f"{file_path.name} -> {destination.relative_to(folder)}")
        except (OSError, ValueError, KeyError) as error:
            summary["skipped"] += 1
            summary["errors"].append(f"Could not move '{file_path.name}': {error}")
    return summary
