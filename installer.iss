; Inno Setup 6 script for the client-ready FileOrganizer installer.
#define MyAppName "File Organizer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "FileOrganizer"
#define MyAppExeName "FileOrganizer.exe"

[Setup]
AppId={{A3A3C1E2-7333-4E8B-9F96-1F5D2C4C8B11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
; Per-user location avoids administrator permissions and Program Files write limits.
DefaultDirName={localappdata}\Programs\FileOrganizer
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=FileOrganizer_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName={#MyAppName}
PrivilegesRequired=lowest

[Files]
Source: "dist\FileOrganizer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
