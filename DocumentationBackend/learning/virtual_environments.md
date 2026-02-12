# 🐍 Virtual Environments

## What is a Virtual Environment?

A virtual environment is an **isolated Python installation** for your project. Think of it as a "bubble" — packages you install inside it don't affect your system Python or other projects.

**Without virtual environments:**
```
System Python
├── django 6.0 (Project A needs this)
├── django 4.2 (Project B needs this) ← CONFLICT!
└── Every project shares the same packages
```

**With virtual environments:**
```
Project A/venv/ → django 6.0 (isolated)
Project B/venv/ → django 4.2 (isolated)
System Python → clean, untouched
```

---

## Creating a Virtual Environment

Open your terminal in your project folder and run:

```bash
python -m venv venv
```

**What this does:**
- `python -m venv` — Runs Python's built-in `venv` module
- `venv` — The name of the folder to create (you can name it anything, but `venv` is the convention)

This creates a `venv/` folder containing a full copy of the Python interpreter and `pip`.

---

## Activating the Virtual Environment

You must **activate** the virtual environment before installing packages or running your project.

### Windows (PowerShell)
```bash
.\venv\Scripts\activate
```

### Windows (CMD)
```bash
venv\Scripts\activate.bat
```

### Mac / Linux
```bash
source venv/bin/activate
```

**How do you know it's active?**
Your terminal prompt will show `(venv)` at the beginning:
```
(venv) PS C:\Users\you\project>
```

---

## Deactivating

When you're done working, simply run:
```bash
deactivate
```

The `(venv)` prefix disappears, and you're back to system Python.

---

## ⚠️ Important Notes

1. **Always activate before running your project** — If you forget, Django won't find your installed packages.
2. **Never commit `venv/` to Git** — Add it to `.gitignore`. The `requirements.txt` file is how others recreate your environment.
3. **One venv per project** — Don't share virtual environments between projects.

### `.gitignore` entry:
```
venv/
```

---

## 🔗 Navigation

← **[Back to Learning Django](../learning_django.md)**

→ **Next: [Requirements & Dependencies](./requirements_and_dependencies.md)**
