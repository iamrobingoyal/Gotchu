# File Organizer - Master Test Plan & QA Specification

> **Document Type:** Master Test Plan & QA Risk Assessment  
> **Target Application:** FileOrganizer (Windows Desktop Automation)  
> **Status:** Ready for Execution  
> **App Version:** 1.0.0  

---

## 1. Executive Summary & Test Strategy

This document establishes the end-to-end quality assurance verification plan for the **FileOrganizer** Windows automation utility. Testing spans core organization logic, pattern-based renaming, configuration persistence, Windows operating system edge conditions, installer/uninstaller lifecycle, and portability across clean Windows installations.

### Testing Principles
- **Non-Destructive Integrity:** User files must never be overwritten, corrupted, or deleted. In conflict scenarios, safe non-colliding names must be generated.
- **Fail-Safe Operation:** Invalid inputs, locked files, missing paths, and Windows-restricted characters must be handled gracefully without application crashes.
- **Client Zero-Dependency:** Standalone executable and installed distribution must function without pre-existing Python runtimes or developer dependencies.

---

## 2. File Organizer Acceptance Checklist (Quick Verification Matrix)

This checklist tracks high-level operational readiness across primary user journeys:

```markdown
FILE ORGANIZER ACCEPTANCE CHECKLIST

[ ] Application opens
[ ] Folder selection works
[ ] PDF detection works
[ ] JPG detection works
[ ] PNG detection works
[ ] DOCX detection works
[ ] XLSX detection works
[ ] MP4 detection works
[ ] Unknown file handling works

[ ] Category creation works
[ ] Category deletion works
[ ] Extension addition works
[ ] Extension removal works
[ ] Destination configuration works

[ ] Rename OFF works
[ ] Rename ON works
[ ] {original} works
[ ] {date} works
[ ] {time} works
[ ] {datetime} works
[ ] {number} works

[ ] Duplicate filenames handled
[ ] Invalid characters handled
[ ] Existing files not overwritten

[ ] Settings persist after restart
[ ] Reset settings works

[ ] EXE works
[ ] Installer works
[ ] Desktop shortcut works
[ ] Start Menu shortcut works
[ ] Uninstaller works

[ ] Works on another Windows PC
```

---

## 3. Comprehensive Test Cases by Functional Area

### Area 1: File Organization
Verifies that direct files in a chosen directory are scanned, sorted, and moved into designated category subfolders.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-ORG-001** | Standard batch file organization | 1. Place a mix of files (`report.pdf`, `photo.jpg`, `doc.docx`) in a test folder.<br>2. Launch FileOrganizer.<br>3. Click **Browse** and select test folder.<br>4. Click **Start Organizing**. | Files are moved into their respective subfolders (`PDFs/`, `Images/`, `Documents/`). The Summary dialog reports 3 processed, 3 moved, 0 skipped. | [ ] Pass<br>[ ] Fail |
| **TC-ORG-002** | Re-running organization on already organized directory | 1. Select a folder where files were already organized into subfolders.<br>2. Click **Start Organizing**. | Subfolders are ignored (not moved or nested). Summary dialog reports 0 processed, 0 moved. No files are duplicated or corrupted. | [ ] Pass<br>[ ] Fail |
| **TC-ORG-003** | Existing destination folders reuse | 1. Pre-create a folder named `PDFs` with an existing file inside.<br>2. Place a new file `invoice.pdf` in the root test folder.<br>3. Run **Start Organizing**. | Existing `PDFs` folder is reused; `invoice.pdf` is safely moved into it alongside existing files. | [ ] Pass<br>[ ] Fail |
| **TC-ORG-004** | Large batch file organization | 1. Generate 500 mixed files in a source directory.<br>2. Click **Start Organizing**. | All 500 files are processed and moved into corresponding folders. Summary dialog shows 500 processed and 500 moved. UI remains responsive or recovers promptly. | [ ] Pass<br>[ ] Fail |
| **TC-ORG-005** | Direct files only (no recursive subfolder traversal) | 1. Create a subfolder `Nested/` containing `sub_doc.pdf`.<br>2. Place `root_doc.pdf` in root.<br>3. Run organization. | `root_doc.pdf` is moved to `PDFs/`. `Nested/sub_doc.pdf` remains untouched inside `Nested/`. | [ ] Pass<br>[ ] Fail |
| **TC-ORG-006** | File with no read permission in source directory | 1. Place a file in the folder and lock read access or assign restricted ACL.<br>2. Run organization. | File cannot be moved; error is caught and detailed in Summary dialog; other files process normally. | [ ] Pass<br>[ ] Fail |

---

### Area 2: File Extension Detection
Verifies accurate classification across standard, case-variant, compound, and extensionless filenames.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-EXT-001** | Case insensitivity of extensions | 1. Create `test.PDF`, `test.Jpg`, `test.PnG`, `test.DocX`.<br>2. Execute organization with default rules. | Files correctly move to `PDFs`, `Images`, and `Documents` despite uppercase/mixed-case extensions. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-002** | Multiple dots in filename | 1. Create `archive.backup.2024.pdf`, `photo.v1.min.jpg`.<br>2. Execute organization. | The system extracts final extension (`.pdf`, `.jpg`) and organizes files into `PDFs` and `Images`. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-003** | Files without extensions | 1. Create files `LICENSE`, `README`, `INSTALL`.<br>2. Execute organization. | Files have no suffix; system categorizes them into fallback `Other` destination. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-004** | Hidden dotfiles (e.g., Unix-style files) | 1. Place `.gitignore`, `.env`, `.editorconfig` in source folder.<br>2. Run organization. | Dotfiles with empty suffix are categorized under `Other` without runtime error. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-005** | Uncommon image and audio extensions | 1. Create `test.webp`, `test.svg`, `test.flac`, `test.m4a`.<br>2. Run organization with default rules. | `test.webp` and `test.svg` move to `Images`; `test.flac` and `test.m4a` move to `Audio`. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-006** | Video file extension coverage | 1. Create `clip.mp4`, `clip.mov`, `clip.mkv`, `clip.webm`.<br>2. Run organization. | All files move to `Videos` destination. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-007** | Spreadsheet extension coverage | 1. Create `sheet.xlsx`, `sheet.xls`, `data.csv`, `sheet.ods`.<br>2. Run organization. | All files move to `Excel` destination. | [ ] Pass<br>[ ] Fail |
| **TC-EXT-008** | Presentation extension coverage | 1. Create `deck.pptx`, `deck.ppt`, `slides.odp`.<br>2. Run organization. | All files move to `Presentations` destination. | [ ] Pass<br>[ ] Fail |

---

### Area 3: Category Rules Management
Verifies adding, editing, deleting, and validating rules within the Settings window.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CAT-001** | Create a new custom category | 1. Open Settings -> **Add Rule**.<br>2. Name: `Archives`, Extensions: `.zip, .rar, .7z`, Destination: `Archives`.<br>3. Save Rule -> Save Settings. | New category appears in Settings tree and main window rule table. Files matching `.zip` route to `Archives/`. | [ ] Pass<br>[ ] Fail |
| **TC-CAT-002** | Delete an existing category | 1. Open Settings.<br>2. Select `Audio` category.<br>3. Click **Delete Rule** and confirm prompt.<br>4. Click **Save Settings**. | `Audio` rule is removed from list. Subsequent audio files route to fallback `Other`. | [ ] Pass<br>[ ] Fail |
| **TC-CAT-003** | Prevent duplicate category names | 1. Open Settings -> **Add Rule**.<br>2. Enter category name `PDFs` (existing rule name).<br>3. Attempt to save. | Validation error alerts that category names must be unique. Rule is not saved. | [ ] Pass<br>[ ] Fail |
| **TC-CAT-004** | Prevent duplicate extension across categories | 1. Open Settings -> **Add Rule**.<br>2. Name: `Ebooks`, Extension: `.pdf`, Destination: `Ebooks`.<br>3. Save Rule -> Click **Save Settings**. | Validation fails stating that extension `.pdf` is used by more than one category. | [ ] Pass<br>[ ] Fail |
| **TC-CAT-005** | Modify extensions for an existing category | 1. Open Settings -> Select `Images` -> **Edit Rule**.<br>2. Append `, .ico, .tiff` to extensions.<br>3. Save Rule -> Save Settings. | Images rule now includes `.ico` and `.tiff`. Organizing files with `.ico` moves them to `Images/`. | [ ] Pass<br>[ ] Fail |
| **TC-CAT-006** | Prevent saving with zero categories | 1. Open Settings -> Delete all categories.<br>2. Click **Save Settings**. | Validation error alerts that at least one category is required. | [ ] Pass<br>[ ] Fail |

---

### Area 4: Destination Configuration
Verifies validation and directory creation behavior for destination folder paths.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DEST-001** | Custom destination folder name | 1. Edit `PDFs` rule to destination `My_PDF_Documents`.<br>2. Save and organize folder with `sample.pdf`. | Subfolder `My_PDF_Documents/` is created under source folder and file is moved there. | [ ] Pass<br>[ ] Fail |
| **TC-DEST-002** | Reject relative navigation destination | 1. Edit rule destination to `..` or `.`.<br>2. Attempt to save rule. | Validation error: "Destination must be one safe folder name." Change rejected. | [ ] Pass<br>[ ] Fail |
| **TC-DEST-003** | Reject path separators in destination | 1. Edit rule destination to `Sub/Folder` or `Sub\Folder`.<br>2. Attempt to save rule. | Validation error: Destination contains invalid characters (`/` or `\`). | [ ] Pass<br>[ ] Fail |
| **TC-DEST-004** | Reject destination ending with dots or spaces | 1. Edit rule destination to `Folder.` or `Folder `.<br>2. Attempt to save rule. | Validation error flags trailing dot/space as invalid Windows folder name. | [ ] Pass<br>[ ] Fail |

---

### Area 5: Rename Functionality (Global & Rule Level)
Verifies renaming toggle behavior and preservation of original extensions.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-REN-001** | Rename disabled (Default state) | 1. Ensure `rename_enabled` is OFF for `Documents`.<br>2. Organize folder containing `Quarterly_Report_2024.docx`. | File is moved to `Documents/Quarterly_Report_2024.docx` with identical filename. | [ ] Pass<br>[ ] Fail |
| **TC-REN-002** | Rename enabled with custom pattern | 1. Edit `PDFs` rule: Enable **Rename files**.<br>2. Set pattern: `Doc_{original}`.<br>3. Organize folder containing `contract.pdf`. | File is moved to `PDFs/Doc_contract.pdf`. Summary dialog increments "Renamed" count by 1. | [ ] Pass<br>[ ] Fail |
| **TC-REN-003** | Real-time preview update in Rule Dialog | 1. Open Edit Rule dialog.<br>2. Check/uncheck **Rename files** and modify rename pattern.<br>3. Inspect the **Preview** label. | Preview label updates immediately to reflect dynamic pattern using `invoice123.pdf`. | [ ] Pass<br>[ ] Fail |

---

### Area 6: Rename Placeholders Validation
Verifies token parsing and formatting across all supported variables.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-PLC-001** | `{original}` placeholder | 1. Rule pattern: `File_{original}`.<br>2. Organize `test.pdf`. | Output: `File_test.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-PLC-002** | `{date}` placeholder | 1. Rule pattern: `{date}_{original}`.<br>2. Organize `report.docx`. | Output: `YYYY-MM-DD_report.docx` matching current date. | [ ] Pass<br>[ ] Fail |
| **TC-PLC-003** | `{time}` placeholder | 1. Rule pattern: `{time}_{original}`.<br>2. Organize `memo.txt`. | Output: `HH-MM-SS_memo.txt` matching current time (colons sanitized to dashes). | [ ] Pass<br>[ ] Fail |
| **TC-PLC-004** | `{datetime}` placeholder | 1. Rule pattern: `{datetime}_{original}`.<br>2. Organize `log.txt`. | Output: `YYYY-MM-DD_HH-MM-SS_log.txt`. | [ ] Pass<br>[ ] Fail |
| **TC-PLC-005** | `{number}` placeholder | 1. Rule pattern: `Invoice_{number}` (Starting: 1, padding: 3).<br>2. Organize `scan.pdf`. | Output: `Invoice_001.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-PLC-006** | Compound pattern combining all placeholders | 1. Rule pattern: `{date}_{time}_{number}_{original}`.<br>2. Organize `bill.pdf`. | Output contains formatted date, time, zero-padded number, and original stem. | [ ] Pass<br>[ ] Fail |
| **TC-PLC-007** | Unknown or malformed placeholder tolerance | 1. Rule pattern: `Test_{unknown_token}_{foo}`.<br>2. Organize `doc.pdf`. | System catches `KeyError`, falls back safely to original file stem `doc.pdf`. No crash occurs. | [ ] Pass<br>[ ] Fail |

---

### Area 7: Sequential Numbering & Padding
Verifies sequential counter increments across multiple files in a category and padding logic.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-NUM-001** | Multi-file sequential counter increment | 1. Rule: `Item_{number}`, start = `001`.<br>2. Place 3 PDFs in folder (`a.pdf`, `b.pdf`, `c.pdf`).<br>3. Organize folder. | Files are named `Item_001.pdf`, `Item_002.pdf`, `Item_003.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-NUM-002** | Independent counters per category | 1. Enable `{number}` renaming for both `PDFs` and `Images`.<br>2. Place 2 PDFs and 2 JPGs in source folder.<br>3. Organize folder. | `PDFs` has `_001` and `_002`; `Images` has independent `_001` and `_002`. | [ ] Pass<br>[ ] Fail |
| **TC-NUM-003** | Custom starting number offset | 1. Set starting number to `50` (padding: 2).<br>2. Organize 2 documents. | First document is named `Doc_50.docx`, second is `Doc_51.docx`. | [ ] Pass<br>[ ] Fail |
| **TC-NUM-004** | Variable padding width | 1. Set starting number to `0001` (4 digits).<br>2. Organize document. | Output contains 4-digit padded number: `Doc_0001.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-NUM-005** | Negative starting number rejection | 1. In Edit Rule dialog, set starting number to `-5`.<br>2. Save rule. | Validation error: "Starting number cannot be negative." | [ ] Pass<br>[ ] Fail |

---

### Area 8: Duplicate Filenames & Conflict Resolution
Verifies that existing destination files and naming collisions are handled without data loss.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DUP-001** | Conflict with existing file in destination | 1. In `PDFs/`, create file `report.pdf`.<br>2. In root, create `report.pdf` (rename OFF).<br>3. Organize folder. | Existing `PDFs/report.pdf` remains untouched. Incoming file is saved as `PDFs/report_1.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-DUP-002** | Multiple successive duplicate conflicts | 1. In `PDFs/`, create `report.pdf`, `report_1.pdf`, `report_2.pdf`.<br>2. Organize folder containing root `report.pdf`. | Incoming file is safely saved as `PDFs/report_3.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-DUP-003** | Pattern-generated collisions | 1. Rename pattern: Static text `Archive` (without `{original}` or `{number}`).<br>2. Organize 3 PDFs (`a.pdf`, `b.pdf`, `c.pdf`). | Output files become `Archive.pdf`, `Archive_1.pdf`, and `Archive_2.pdf`. No file is overwritten. | [ ] Pass<br>[ ] Fail |
| **TC-DUP-004** | Case collision on Windows NTFS | 1. Pre-create `TEST.pdf` in `PDFs/`.<br>2. Organize root `test.pdf` (NTFS is case-preserving but insensitive). | Conflict detected; file saved as `test_1.pdf`. Original `TEST.pdf` intact. | [ ] Pass<br>[ ] Fail |

---

### Area 9: Invalid Windows Characters & Filename Sanitization
Verifies stripping/replacing characters forbidden by the Windows filesystem (`< > : " / \ | ? *` and control characters).

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-SAN-001** | Illegal characters in rename pattern | 1. Pattern: `File:?<*>{original}`.<br>2. Organize `sample.pdf`. | Prohibited characters are replaced with underscores: `File_____sample.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-SAN-002** | Trailing dots and spaces stripping | 1. Pattern: `TestFolder... `.<br>2. Organize `sample.pdf`. | Windows removes trailing dots and spaces: becomes `TestFolder.pdf`. | [ ] Pass<br>[ ] Fail |
| **TC-SAN-003** | Non-printable ASCII control characters | 1. Filename contains ASCII `\x07` or `\x1F` (ord < 32).<br>2. Execute organization and sanitization. | Control characters are sanitized to underscores. | [ ] Pass<br>[ ] Fail |
| **TC-SAN-004** | Truncation of excessively long filenames | 1. Organize a file whose generated name exceeds 200 characters.<br>2. Verify output name. | Stem is safely bounded to 180 characters plus extension to prevent Windows `MAX_PATH` errors. | [ ] Pass<br>[ ] Fail |
| **TC-SAN-005** | Category name with invalid characters | 1. In Settings, try to add category name `Docs:2024?`.<br>2. Attempt to save. | Validation error alerts that category name contains invalid characters. | [ ] Pass<br>[ ] Fail |

---

### Area 10: Configuration Persistence
Verifies settings storage, read/write integrity at `%APPDATA%\FileOrganizer\settings.json`, and process restarts.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CFG-001** | Settings write on save | 1. Modify rules in Settings (e.g. change destination of `PDFs` to `Invoices`).<br>2. Click **Save Settings**.<br>3. Inspect `%APPDATA%\FileOrganizer\settings.json`. | File is created/updated with valid JSON reflecting new rule values. | [ ] Pass<br>[ ] Fail |
| **TC-CFG-002** | Persistence across application restarts | 1. Save custom rules in Settings.<br>2. Close FileOrganizer application completely.<br>3. Re-launch FileOrganizer. | Custom rules are loaded and displayed in the main table. | [ ] Pass<br>[ ] Fail |
| **TC-CFG-003** | Discard changes on dialog cancel/close | 1. Open Settings -> Edit a rule.<br>2. Close dialog via `X` without clicking **Save Settings**.<br>3. Re-open Settings. | Discarded changes are not saved; previous saved settings remain in effect. | [ ] Pass<br>[ ] Fail |
| **TC-CFG-004** | Graceful recovery from corrupt settings.json | 1. Open `%APPDATA%\FileOrganizer\settings.json` in editor.<br>2. Replace contents with corrupt text `{ invalid_json `. <br>3. Launch FileOrganizer. | App does not crash; falls back gracefully to default settings. | [ ] Pass<br>[ ] Fail |

---

### Area 11: Reset Configuration Defaults
Verifies reverting all customizations back to factory defaults.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-RST-001** | Reset Defaults dialog action | 1. Open Settings after modifying several categories.<br>2. Click **Reset Defaults**.<br>3. Confirm "Replace all current rules with defaults?".<br>4. Click **Save Settings**. | Settings list reverts to standard 8 default categories (`PDFs`, `Images`, `Videos`, `Audio`, `Documents`, `Excel`, `Presentations`, `Other`). | [ ] Pass<br>[ ] Fail |
| **TC-RST-002** | Cancel Reset Defaults prompt | 1. In Settings, click **Reset Defaults**.<br>2. Click **No** on confirmation dialog. | Existing custom rules remain unchanged. | [ ] Pass<br>[ ] Fail |
| **TC-RST-003** | Reset Defaults followed by Cancel dialog | 1. Click **Reset Defaults** and confirm.<br>2. Close Settings window (`X`) without clicking **Save Settings**.<br>3. Re-open Settings. | Changes were not committed; pre-existing custom rules remain intact. | [ ] Pass<br>[ ] Fail |

---

### Area 12: Error Handling & Resilience
Verifies that runtime exceptions are reported cleanly without unexpected termination.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-ERR-001** | Organizing without selecting a folder | 1. Launch app with blank source folder entry.<br>2. Click **Start Organizing**. | Warning dialog: "Choose a source folder first." No error thrown. | [ ] Pass<br>[ ] Fail |
| **TC-ERR-002** | Source folder path manually edited to non-existent path | 1. Type a non-existent path into Source Folder entry.<br>2. Click **Start Organizing**. | Error dialog: "The selected source folder is not available." | [ ] Pass<br>[ ] Fail |
| **TC-ERR-003** | Destination collision where a file has folder's name | 1. Create a file named `PDFs` (no extension) in root folder.<br>2. Place `sample.pdf` in root folder.<br>3. Organize folder. | `mkdir` fails because `PDFs` is a file; error logged in Summary dialog; app does not crash. | [ ] Pass<br>[ ] Fail |
| **TC-ERR-004** | Invalid rule settings validation before run | 1. Alter rule to have empty category name or invalid pattern.<br>2. Run **Start Organizing**. | Pre-run validation alerts user with error list; organize operation aborted safely. | [ ] Pass<br>[ ] Fail |
| **TC-ERR-005** | Read-only target volume or restricted destination | 1. Attempt organization targeting a write-protected USB drive or restricted folder. | Moving fails; error message captured in Summary dialog details list. | [ ] Pass<br>[ ] Fail |

---

### Area 13: Missing Files & Dynamic Directory Changes
Verifies behavior when files are deleted or moved during an active session.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-MIS-001** | File deleted between scan and move | 1. Place `doc1.pdf` and `doc2.pdf` in folder.<br>2. Delete `doc1.pdf` right as organization begins. | `doc1.pdf` error caught and reported in Summary dialog; `doc2.pdf` processed successfully. | [ ] Pass<br>[ ] Fail |
| **TC-MIS-002** | Source directory deleted before clicking Start Organizing | 1. Select folder in UI.<br>2. In Windows Explorer, delete that folder.<br>3. Click **Start Organizing**. | App detects directory is missing and presents "Folder not found" warning. | [ ] Pass<br>[ ] Fail |
| **TC-MIS-003** | Source folder renamed before clicking Start Organizing | 1. Select folder in UI.<br>2. Rename folder in Windows Explorer.<br>3. Click **Start Organizing**. | UI reports folder is not available; user prompted to select valid folder. | [ ] Pass<br>[ ] Fail |

---

### Area 14: Permission Errors & Locked Files
Verifies handling of files locked by open processes (Word, Excel, Media Player, running processes).

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-PERM-001** | File locked exclusively by another application | 1. Open `test.docx` in Microsoft Word or open with exclusive file lock.<br>2. Place un-locked `test2.docx` in folder.<br>3. Run organization. | `test.docx` move raises `PermissionError`; caught and counted under "skipped"; `test2.docx` moves successfully. | [ ] Pass<br>[ ] Fail |
| **TC-PERM-002** | Destination folder write permission denied | 1. Remove write permissions from existing destination subfolder.<br>2. Attempt organization. | Operation fails gracefully for affected files; detailed in Summary error window. | [ ] Pass<br>[ ] Fail |
| **TC-PERM-003** | In-use executable file lock | 1. Place a running `.exe` in a test folder categorized for organization.<br>2. Run organization. | Locked binary is skipped with `PermissionError` captured in Summary details. | [ ] Pass<br>[ ] Fail |

---

### Area 15: Empty Folders & Directory Boundary Conditions
Verifies handling of blank directories and non-file directory structures.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-EMP-001** | Completely empty source directory | 1. Select an empty folder.<br>2. Click **Start Organizing**. | Summary dialog displays: Processed: 0, Moved: 0, Skipped: 0. Details: "No files found." | [ ] Pass<br>[ ] Fail |
| **TC-EMP-002** | Source folder contains only subdirectories | 1. Create a folder with only subfolders (`FolderA/`, `FolderB/`) and no root files.<br>2. Run organization. | Subfolders are ignored; Summary displays 0 processed, 0 moved. | [ ] Pass<br>[ ] Fail |
| **TC-EMP-003** | 0-byte (empty) files | 1. Create empty 0-byte files `empty.pdf`, `empty.jpg`.<br>2. Run organization. | Files are categorized and moved successfully to `PDFs` and `Images`. | [ ] Pass<br>[ ] Fail |

---

### Area 16: Unsupported & Non-Standard File Types
Verifies behavior for extensions not defined in standard categories or rules.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-UNS-001** | Arbitrary unknown extension (Default fallback) | 1. Place `data.xyz`, `model.onnx`, `script.py` in folder.<br>2. Run organization with default rules. | Files are categorized into fallback `Other/` destination folder. | [ ] Pass<br>[ ] Fail |
| **TC-UNS-002** | Fallback when "Other" category is deleted | 1. Delete `Other` category from Settings.<br>2. Place `data.xyz` in folder.<br>3. Run organization. | Code falls back to `rules[0]` (`PDFs/`). File is moved safely without crash. | [ ] Pass<br>[ ] Fail |
| **TC-UNS-003** | Filenames with spaces and unicode symbols | 1. Create `My Presentation (Final) 🌟.pptx`, `résumé.pdf`.<br>2. Run organization. | Unicode characters and spaces preserved in safe format; files move to respective folders. | [ ] Pass<br>[ ] Fail |
| **TC-UNS-004** | File ending with dot before extension (`name..pdf`) | 1. Create `test..pdf`.<br>2. Run organization with rename ON. | File stem is sanitized and properly recognized as `.pdf`. | [ ] Pass<br>[ ] Fail |

---

### Area 17: Standalone FileOrganizer.exe
Verifies the PyInstaller standalone distribution (`dist\FileOrganizer.exe`).

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-EXE-001** | Launch standalone executable | 1. Navigate to `dist\FileOrganizer.exe`.<br>2. Double-click executable. | App window opens cleanly; Segoe UI font and window icon render properly; no console window appears. | [ ] Pass<br>[ ] Fail |
| **TC-EXE-002** | Embedded icon asset extraction | 1. Inspect window title bar and taskbar icon when running standalone exe. | Application icon `file_organizer.ico` is visible on title bar and taskbar (no default Tk feather icon). | [ ] Pass<br>[ ] Fail |
| **TC-EXE-003** | Standalone organization end-to-end | 1. Run `dist\FileOrganizer.exe`.<br>2. Select test directory with 5 files.<br>3. Organize files. | Organization completes; Summary dialog opens with complete details. | [ ] Pass<br>[ ] Fail |
| **TC-EXE-004** | Portable copy execution | 1. Copy `dist\FileOrganizer.exe` to a USB drive or different folder.<br>2. Execute from new location. | Operates autonomously without local repository dependencies. | [ ] Pass<br>[ ] Fail |

---

### Area 18: FileOrganizer_Setup.exe Installer
Verifies Inno Setup package compilation, wizard flow, and installation integrity.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-INST-001** | Standard user installation (non-admin) | 1. Launch `installer\FileOrganizer_Setup.exe` on standard user account.<br>2. Complete setup wizard. | Setup completes without requiring administrator elevation. Installs to `%LOCALAPPDATA%\Programs\FileOrganizer`. | [ ] Pass<br>[ ] Fail |
| **TC-INST-002** | Custom installation directory | 1. Run installer.<br>2. Specify custom directory in AppData.<br>3. Finish install. | Application installed correctly to specified directory. | [ ] Pass<br>[ ] Fail |
| **TC-INST-003** | Post-install launch option | 1. Leave "Launch File Organizer" checked on final wizard page.<br>2. Click **Finish**. | FileOrganizer launches automatically. | [ ] Pass<br>[ ] Fail |
| **TC-INST-004** | Overwrite/Upgrade installation | 1. Re-run `FileOrganizer_Setup.exe` over an existing installation. | Existing installation is upgraded cleanly without errors or file locks. | [ ] Pass<br>[ ] Fail |
| **TC-INST-005** | Installed payload integrity | 1. Check `%LOCALAPPDATA%\Programs\FileOrganizer`. | Contains `FileOrganizer.exe`, `unins000.exe`, `unins000.dat`. No extra debug files. | [ ] Pass<br>[ ] Fail |

---

### Area 19: Desktop Shortcut Verification
Verifies creation, icon display, and launch behavior of desktop shortcut.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-SHR-001** | Desktop shortcut creation & icon | 1. Complete installation via `FileOrganizer_Setup.exe`.<br>2. Check Windows Desktop. | "File Organizer" shortcut exists with proper application icon. | [ ] Pass<br>[ ] Fail |
| **TC-SHR-002** | Launch from Desktop shortcut | 1. Double-click "File Organizer" desktop shortcut. | FileOrganizer opens with correct working directory; settings load successfully. | [ ] Pass<br>[ ] Fail |

---

### Area 20: Start Menu Shortcut Verification
Verifies Start Menu shortcut creation, searchability, and launch behavior.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-STR-001** | Start Menu entry placement | 1. Open Windows Start Menu.<br>2. Locate "File Organizer" in app list. | Entry exists under `{autoprograms}` for current user. | [ ] Pass<br>[ ] Fail |
| **TC-STR-002** | Windows search indexing | 1. Press Windows Key, type `File Organizer`. | Application appears as primary search result and launches upon pressing Enter. | [ ] Pass<br>[ ] Fail |

---

### Area 21: Uninstallation Lifecycle
Verifies complete removal of installed application files, shortcuts, and registry entries.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-UNINST-001** | Uninstall via Windows Settings / Add or Remove Programs | 1. Open Windows Settings -> Installed Apps.<br>2. Select "File Organizer" -> **Uninstall**.<br>3. Confirm uninstallation. | Uninstaller runs smoothly and removes files from `%LOCALAPPDATA%\Programs\FileOrganizer`. | [ ] Pass<br>[ ] Fail |
| **TC-UNINST-002** | Shortcut cleanup on uninstall | 1. Check Desktop and Start Menu after uninstallation. | Desktop shortcut and Start Menu entry are removed. | [ ] Pass<br>[ ] Fail |
| **TC-UNINST-003** | Running process prompt during uninstall | 1. Launch FileOrganizer.<br>2. Attempt uninstallation while app is open. | Uninstaller warns that application is currently running, prompts to close before continuing. | [ ] Pass<br>[ ] Fail |
| **TC-UNINST-004** | User configuration retention policy | 1. Inspect `%APPDATA%\FileOrganizer\settings.json` after uninstallation. | User configuration is retained for future re-installations, or cleaned according to spec. | [ ] Pass<br>[ ] Fail |

---

### Area 22: Clean Windows Environment & Portability
Verifies operation on an isolated Windows system without developer tools.

| Test Case ID | Test Description | Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CLEAN-001** | Execution without Python runtime | 1. Copy `FileOrganizer.exe` to a clean Windows 10/11 VM (no Python installed).<br>2. Double-click executable. | App launches immediately without missing `.dll` or runtime errors (VCRUNTIME bundled). | [ ] Pass<br>[ ] Fail |
| **TC-CLEAN-002** | Fresh `%APPDATA%` generation | 1. Run app on a fresh Windows user account where `%APPDATA%\FileOrganizer` does not exist.<br>2. Modify a setting and save. | Directory and `settings.json` are created automatically without permission or path errors. | [ ] Pass<br>[ ] Fail |
| **TC-CLEAN-003** | Windows SmartScreen / Defender observation | 1. Transfer installer via network / USB.<br>2. Run installer. | Executable runs (SmartScreen warning expected if unsigned; verify "Run anyway" works as expected). | [ ] Pass<br>[ ] Fail |

---

## 4. Senior QA Technical Inspection: Difficult-to-Test & Potentially Unsafe Areas

During static code analysis of `config.py`, `organizer.py`, and `main.py`, several architectural risks, edge cases, and testing challenges were identified:

### ⚠️ Potentially Unsafe Areas

1. **Irreversible Batch Operations (No Undo / Rollback Mechanism):**
   - **Risk:** Once `organize_files` executes `shutil.move()`, files are physically relocated and renamed in-place. If a user inadvertently configures a destructive pattern (e.g. `FixedName` without `{original}` or `{number}`), or selects the wrong directory (e.g. `Desktop`), there is no "Undo" or activity log file to reverse the changes.
   - **Severity:** High
   - **QA Recommendation:** Future release should include a `.rollback.json` or transaction log enabling a 1-click "Undo Last Organization".

2. **Windows Reserved Device Names (DOS Con/Aux/Nul Namespace):**
   - **Risk:** In `organizer.py`, `sanitize_filename` strips `<>:"/\\|?*`, but does **not** sanitize Windows reserved device names: `CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, `LPT1`-`LPT9`.
   - If a user names a category `CON` or a rename pattern evaluates to `nul.txt`, Windows filesystem APIs throw `OSError: [WinError 87] The parameter is incorrect`.
   - **Severity:** Medium
   - **QA Recommendation:** Validate and sanitize reserved names (e.g. prepend underscore: `_CON`).

3. **Destination Folder Colliding with a File:**
   - **Risk:** In `organizer.py`:
     ```python
     destination_folder = folder / rule["destination"]
     destination_folder.mkdir(exist_ok=True)
     ```
     If the source directory already contains a file with the exact same name as the category destination (e.g. an extensionless file named `PDFs`), `mkdir` fails with `FileExistsError`. While caught by `except (OSError, ...)`, all files belonging to that category will fail to move.
   - **Severity:** Medium
   - **QA Recommendation:** Verify destination is a directory or generate an alternate non-colliding folder name.

4. **Synchronous UI Freezing on Large Batch or Cross-Volume Moves:**
   - **Risk:** In `main.py`, `organize_files()` runs synchronously on Tkinter's main event thread. If a user organizes 10,000 files or moves multi-gigabyte video files, Windows flags the window as **"Not Responding"** until completion.
   - **Severity:** Medium
   - **QA Recommendation:** Offload `organize_files` to a background worker thread (`threading.Thread`) with progress bar reporting.

5. **Settings Inconsistency if "Other" Category is Deleted:**
   - **Risk:** In `organizer.py`:
     ```python
     fallback = next((rule for rule in rules if rule["name"].casefold() == "other"), None)
     ```
     If a user deletes the `Other` category in Settings, `fallback` becomes `None`, and any unknown file extension is automatically routed to `rules[0]` (usually `PDFs`). This can surprise users when unknown `.xyz` files end up in `PDFs/`.
   - **Severity:** Low-Medium
   - **QA Recommendation:** Enforce that a catch-all fallback category always exists or keep unclassified files in root.

6. **Extension Placeholder Re-duplication (`{extension}` vs Implicit Extension):**
   - **Risk:** In `organizer.py`:
     ```python
     suffix = "" if "{extension}" in rule.get("rename_pattern", "") else extension
     ```
     If a user writes `{original}.pdf`, `{extension}` was not in the pattern, so `.pdf` gets appended again, yielding `document.pdf.pdf`.
   - **Severity:** Low-Medium

---

### 🔬 Difficult-to-Test Areas & Mitigation Strategies

| Area | Why It Is Difficult to Test | Mitigation / Test Approach |
| :--- | :--- | :--- |
| **Permission & File Locking** | Windows does not allow arbitrary processes to inject locks without holding an active Win32 file handle (`LockFileEx`). | Write a small Python scratch helper that opens a target file with `msvcrt.locking` or in exclusive write mode (`open(..., 'w')`) while running organization. |
| **Clean Machine Testing** | Developer machines already have Python, Visual C++ Redistributable, Git, and Inno Setup installed. | Use **Windows Sandbox** (`WindowsSandbox.exe`) or a clean Hyper-V / VirtualBox Windows 11 VM to test `dist\FileOrganizer.exe` and `FileOrganizer_Setup.exe`. |
| **Rapid Concurrency / Race Conditions** | Testing file movement while external processes (e.g., downloads or sync tools like OneDrive/Dropbox) are actively writing. | Run a concurrent writer script that continuously creates and modifies files in the source directory during the organization run. |
| **High-DPI Scaling** | Tkinter widgets can render blurry or misaligned on high-resolution displays (4K screens at 150%/200% scaling). | Test on multiple Windows display scaling settings (100%, 125%, 150%, 200%) via Windows Display Settings. |
| **Installer Uninstallation Hooks** | Verifying registry and directory cleanup thoroughly without leaving test artifacts on the host. | Run uninstaller test suite inside Windows Sandbox to verify complete isolation and cleanup. |

---

## 5. Sign-off & Execution Log

| Test Suite | Total Cases | Passed | Failed | Blocked | Execution Date | QA Engineer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1. File Organization | 6 | | | | | |
| 2. Extension Detection | 8 | | | | | |
| 3. Category Rules | 6 | | | | | |
| 4. Destination Config | 4 | | | | | |
| 5. Rename Functionality | 3 | | | | | |
| 6. Rename Placeholders | 7 | | | | | |
| 7. Sequential Numbering | 5 | | | | | |
| 8. Duplicate Filenames | 4 | | | | | |
| 9. Character Sanitization| 5 | | | | | |
| 10. Config Persistence | 4 | | | | | |
| 11. Reset Configuration | 3 | | | | | |
| 12. Error Handling | 5 | | | | | |
| 13. Missing Files | 3 | | | | | |
| 14. Permission Errors | 3 | | | | | |
| 15. Empty Folders | 3 | | | | | |
| 16. Unsupported Types | 4 | | | | | |
| 17. Standalone EXE | 4 | | | | | |
| 18. Setup Installer | 5 | | | | | |
| 19. Desktop Shortcut | 2 | | | | | |
| 20. Start Menu Shortcut| 2 | | | | | |
| 21. Uninstallation | 4 | | | | | |
| 22. Clean Environment | 3 | | | | | |
| **TOTAL** | **93** | | | | | |
