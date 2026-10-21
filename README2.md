# Notes

## 1. Create the project and a virtual environment

A virtual environment keeps this project's libraries separate from everything else on your computer.

```bash
mkdir fullchair && cd fullchair
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install fastapi uvicorn pytest httpx
```

## Folder Structure
```bash
fullchair/
├── app/
│   ├── __init__.py      (empty file)
│   └── main.py
└── tests/
    ├── __init__.py      (empty file)
    └── test_health.py
```

## 2. Select the Python interpreter

Point VS Code at the virtual environment:

1. Press `Cmd+Shift+P` (Windows/Linux: `Ctrl+Shift+P`).
2. Run **Python: Select Interpreter**.
3. Pick the interpreter with `.venv` in its path.

This lets VS Code autocomplete and check your code properly.

## 3. Save and push to GitHub

```bash
pip freeze > requirements.txt
git add .
git commit -m "FastAPI app with health endpoint and first test"
git push
```

This is the loop you'll use for the whole project:

- `git add .`: stages your changes, which picks what goes into the next snapshot.
- `git commit -m "..."`: saves a snapshot with a message describing what you did.
- `git push`: uploads your commits to GitHub.

## Topics