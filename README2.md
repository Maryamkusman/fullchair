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

### Quick setup commands

```bash
echo -e ".venv/\n__pycache__/\n.pytest_cache/\n.env" > .gitignore
pip freeze > requirements.txt
git init && git add . && git commit -m "FastAPI app with health endpoint and first test"
```

### What does the `@app.get` decorator do?

It connects a URL to a Python function. `@app.get("/health")` tells FastAPI: "When someone sends a GET request to `/health`, run the function below and send back whatever it returns." FastAPI also converts the returned Python dictionary into JSON automatically.

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

GET is the HTTP method for reading data. Later you'll use other methods:

| Decorator | Used for | Example |
| --- | --- | --- |
| `@app.get` | Reading data | Viewing appointments |
| `@app.post` | Creating things | Booking an appointment |
| `@app.put` / `@app.patch` | Updating | Changing an appointment time |
| `@app.delete` | Deleting | Cancelling an appointment |

### Why use a virtual environment?

It gives each project its own private set of Python libraries. Without one, every project on your computer shares the same libraries, so if FullChair needs one version of a library and another project needs a different version, they'd break each other.

It also makes your project reproducible. `pip freeze > requirements.txt` records exactly what this project uses, so anyone (including a server when you deploy) can install the same versions with:

```bash
pip install -r requirements.txt
```

### What's the difference between running the server and running pytest?

**Running the server** (`uvicorn app.main:app --reload`) starts your app and keeps it running, listening for real requests on port 8000. You test it by hand, in a browser or on the `/docs` page, and it runs until you stop it.

**Running pytest** (`pytest`) runs your test functions automatically and then exits. It uses `TestClient`, which sends fake requests straight to your app without starting a real server, and checks the answers with `assert`. Each test passes or fails.
