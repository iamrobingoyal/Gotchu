# 📂 FileOrganizer

> Your Downloads folder called. It wants its life back.

FileOrganizer is a lightweight Windows desktop automation tool that takes the repetitive chore of sorting, grouping, and renaming loose files and does it for you.

Instead of spending 15 minutes manually dragging PDFs, screenshots, datasets, spreadsheets, and recordings into separate folders... let the app handle it in one click. 🤝

---

### What it does

Drop files into a folder → choose your rules → hit organize. Clean directory achieved.

No more:
- *"Where did that invoice save?"*
- *"Why are there 942 unsorted files in Downloads?"*
- *"I really don't want to rename 40 photos by hand."* 💀

---

## ✨ Features

- **Automatic Sorting by Extension:** Routes incoming files into dedicated category folders (`PDFs`, `Images`, `Documents`, `Excel`, `Videos`, `Audio`, `Presentations`, etc.).
- **Fallback for Unknown Files:** Unrecognized file types are safely moved into an `Other/` bucket instead of being left behind or misplaced.
- **Configurable Rules:** Add new categories, delete unwanted ones, modify extension mappings, and change target destination folder names.
- **Custom Renaming Engine:** Toggle file renaming ON or OFF per category. Keep original filenames or standardize them using custom templates.
- **Dynamic Placeholders:** Embed dates, times, sequential numbers, and original stems into filenames.
- **Sequential Numbering & Padding:** Set custom starting counters (e.g. `1`, `100`) and customizable zero-padding (e.g. `001`, `0001`).
- **Live Rule Preview:** Test rename patterns right inside the settings dialog before touching any real files.
- **Safe Conflict Resolution:** If a file with the same name already exists in the destination, FileOrganizer automatically appends a safe counter (`_1`, `_2`) so files are **never overwritten**.
- **Per-User Configuration Persistence:** Custom rules and preferences automatically save to `%APPDATA%\FileOrganizer\settings.json` and persist across restarts.
- **One-Click Factory Reset:** Instantly revert back to default rules whenever needed.
- **Native Windows Desktop GUI:** Clean, responsive Tkinter interface styled with native Segoe UI typography and custom application iconography.

---

## 🏷️ Supported Rename Placeholders

When renaming is enabled for a category, you can combine any of the following tokens in your pattern:

| Placeholder | Description | Example Output |
| :--- | :--- | :--- |
| `{original}` | The file's original stem name (excluding extension) | `invoice` |
| `{date}` | Current date in `YYYY-MM-DD` format | `2026-10-04` |
| `{time}` | Current time in `HH-MM-SS` format | `16-30-00` |
| `{datetime}` | Combined timestamp (`YYYY-MM-DD_HH-MM-SS`) | `2026-10-04_16-30-00` |
| `{number}` | Sequential counter with zero-padding | `001`, `002`, `003` |
| `{extension}` | Optional explicit file extension token | `.pdf` |

### Real-World Pattern Examples

- **Pattern:** `Invoice_{date}_{number}`  
  → `Invoice_2026-10-04_001.pdf`

- **Pattern:** `{date}_{original}`  
  → `2026-10-04_Quarterly_Report.docx`

- **Pattern:** `Photo_{datetime}_{number}`  
  → `Photo_2026-10-04_16-30-00_001.jpg`

> **Note:** If `{extension}` is omitted from your pattern, FileOrganizer automatically preserves the file's original extension.

---

## 📁 Project Structure

```text
FileOrganizer/
├── assets/
│   └── file_organizer.ico      # Application and installer icon
├── build.bat                   # Automated build script for standalone executable
├── build_installer.bat         # Automated build script for Inno Setup installer
├── config.py                   # Settings loader, defaults, and schema validators
├── FileOrganizer.spec          # PyInstaller build specification
├── installer.iss               # Inno Setup 6/7 installer script
├── main.py                     # Main GUI desktop entry point (Tkinter)
├── organizer.py                # Core scanning, categorization, sanitization & moving logic
├── README.md                   # Project documentation & setup guide
├── requirements.txt            # Python build-time dependencies
├── TEST.md                     # QA test plan & test case matrix (93 test cases)
└── .gitignore                  # Git ignore rules for Python, builds & OS files
```

---

## 🚀 Installation & Development Setup

### Prerequisites
- Windows 10 or 11
- Python 3.10 or higher
- Git

### 1. Clone the repository
```powershell
git clone <repository-url>
cd FileOrganizer
```

### 2. Create and activate a virtual environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```
*(The application runtime relies entirely on the Python Standard Library. `requirements.txt` installs `pyinstaller` for building standalone executables).*

### 4. Run the application
```powershell
python main.py
```

---

## 📦 Build Windows Standalone EXE

To package the application into a standalone `.exe` that runs on any Windows machine without requiring Python:

```powershell
.\build.bat
```

This script cleans previous build artifacts and compiles the app into:
```text
dist\FileOrganizer.exe
```

End users can run this single executable directly without installing Python, runtime libraries, or virtual environments.

---

## 🛠️ Build Windows Installer

If you have [Inno Setup 6 or 7](https://jrsoftware.org/isdl.php) installed, you can generate a professional Windows installer:

```powershell
.\build_installer.bat
```

This compiles:
```text
installer\FileOrganizer_Setup.exe
```

### Distribution Comparison

| Package | Target Audience | Requirements | Shortcuts & Uninstaller |
| :--- | :--- | :--- | :--- |
| **Source Code** (`main.py`) | Developers | Python 3.10+ & Git | None (runs in terminal/IDE) |
| **Standalone** (`FileOrganizer.exe`) | Users wanting a portable binary | Windows (No Python needed) | Portable single file |
| **Installer** (`FileOrganizer_Setup.exe`) | General Windows users | Windows (No Python needed) | Desktop & Start Menu shortcuts + clean uninstaller |

---

## 🧪 Testing

Quality assurance is documented in [TEST.md](TEST.md), which includes:
- A 31-point rapid acceptance verification checklist
- 93 exhaustive test cases across 22 operational areas
- Technical edge-case analysis (path limits, file locks, character sanitization)

> **Note:** `TEST.md` is a developer QA document and is strictly excluded from client installer packages.

---

## ⚙️ Configuration & Storage

User settings and category definitions are stored in standard JSON format under the active Windows user profile:

```text
%APPDATA%\FileOrganizer\settings.json
```

If the file is deleted or becomes invalid, FileOrganizer gracefully falls back to default factory settings without crashing.

---

## 🛡️ Safety & Non-Destructive Design

- **Non-Destructive Moves:** FileOrganizer sorts existing files into subfolders; it never alters file contents or strips metadata.
- **Zero Overwriting:** If a destination folder already has a file with the same name, a safe numbered suffix (`_1`, `_2`) is automatically appended.
- **Filename Sanitization:** All generated names are sanitized against forbidden Windows characters (`< > : " / \ | ? *`) and control characters.
- **Recommended Practice:** As with any disk automation utility, test on a sample folder before organizing mission-critical directories.

---

## 📄 License

License: Not currently specified.
