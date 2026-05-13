# Research_reviewer

Two small Python implementations of a **research output submission + review/evaluation** flow:

- `initial_system/`: baseline design
- `improved_system/`: refactored/improved design

Both are self-contained (standard library only) and include a small demo entrypoint you can run.

## Requirements

- Python 3.8+ (no third-party dependencies)

## Setup (optional but recommended)

From the repository root (the folder that contains `initial_system/` and `improved_system/`):

### Windows (PowerShell)

```powershell
cd C:\path\to\Research_reviewer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

If activation is blocked by your PowerShell execution policy, run this once (current terminal only) and retry activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS/Linux (bash/zsh)

```bash
cd /path/to/Research_reviewer
python3 -m venv .venv
source .venv/bin/activate
python --version
```

## Run

Important: run these as modules (`-m`) from the repo root so the package-relative imports work.

If you are currently in `initial_system/` or `improved_system/`, go up one directory first:

```powershell
cd ..
```

Your PowerShell prompt should end with `...\Research_reviewer>` (repo root), not `...\Research_reviewer\initial_system>`.

Do **not** run files like `python initial_system\wiring.py` or `python wiring.py` from inside the folder — that will cause
`ImportError: attempted relative import with no known parent package`.

Also avoid `python -m wiring` / `python -m wiring.py` while inside `initial_system/` — that runs `wiring` as a top-level module,
so it still has no parent package and will fail with the same relative-import error.

### Baseline demo (`initial_system`)

```bash
python -m initial_system.wiring
```

Alternative entrypoint (same demo):

```bash
python -m initial_system.research_system
```

### Improved demo (`improved_system`)

```bash
python -m improved_system.wiring
```

Alternative entrypoint (same demo):

```bash
python -m improved_system.improved_research_system
```

## Troubleshooting (Windows)

- If `py` is not found: that’s ok — use `python` as shown above.
- If `python` points to `...\WindowsApps\python.exe` and fails to run or shows odd behavior, you likely have the Microsoft Store
	“app execution alias” stub. Install Python from python.org (or Windows Store) and/or disable the alias in:
	**Settings → Apps → Advanced app settings → App execution aliases**.
- If you accidentally created your virtual environment inside `initial_system/` (you see `initial_system/.venv/`): delete it and create
  the venv from the repo root instead (recommended). The module run commands in this README assume the repo root is your working directory.