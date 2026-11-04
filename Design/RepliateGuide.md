# FullChair Rebuild: Step-by-Step Guide

Oct 29, 2026 · @maryam

## Overview

This guide rebuilds FullChair, an AI receptionist for salons, from an empty folder through Step 3: a FastAPI app with a SQLite database, five tables, API endpoints, eight passing tests, and a GitHub repo. Follow the parts in order and type the code yourself.

### Roadmap

1. Setup and first endpoint: FastAPI basics and your first test. **Done.**
2. Database models: salons, stylists, services, clients, and appointments with SQLAlchemy. **Done.**
3. API endpoints: creating and reading data, with validation and tests. **In progress.**
4. Availability logic: the algorithm that finds open time slots.
5. The AI agent: a Claude tool-use loop, starting with two tools.
6. Chat interface: a simple page to talk to the receptionist.
7. SMS: receiving and replying to texts, in demo mode first.
8. Background jobs: refilling cancelled appointments from the waitlist.
9. Dashboard: the owner's view in Next.js.
10. Ship it: Docker, GitHub Actions, and deployment.

### Folder structure after Step 3

```
fullchair/
├── .venv/                (virtual environment, not on GitHub)
├── app/
│   ├── __init__.py       (empty)
│   ├── database.py       (engine, sessions, Base, get_db)
│   ├── models.py         (the five tables)
│   ├── schemas.py        (what the API accepts and returns)
│   └── main.py           (the FastAPI app and endpoints)
├── tests/
│   ├── __init__.py       (empty)
│   ├── conftest.py       (shared test fixtures)
│   ├── test_health.py
│   ├── test_models.py
│   └── test_salons.py
├── .gitignore
├── fullchair.db          (created when the app starts, not on GitHub)
├── README.md
└── requirements.txt
```

## Part 0: Setup

Install four tools, connect Git to GitHub, then create the repo and its virtual environment. Do this once per computer and once per project.

### 1. Install the tools

Check what you already have:

```bash
python3 --version
git --version
code --version
gh --version
```

| Tool | Get it from | Notes |
| --- | --- | --- |
| Python 3.12+ | python.org/downloads | macOS ships 3.9, which is too old for some later code |
| Git | git-scm.com | macOS may offer to install it when you run `git --version` |
| VS Code | code.visualstudio.com | Run **Shell Command: Install 'code' command in PATH**; install the Python extension |
| GitHub CLI | cli.github.com | Lets you create repos from the terminal |

Close and reopen the terminal after installing.

### 2. Connect Git and GitHub

```bash
git config --global user.name "Maryam Usman"
git config --global user.email "your-github-email@example.com"
gh auth login
```

For `gh auth login`, choose GitHub.com, HTTPS, Yes, then Login with a web browser.

### 3. Create the repo

```bash
mkdir -p ~/projects && cd ~/projects
gh repo create fullchair --public --clone --add-readme --gitignore Python
cd fullchair
code .
```

This creates the GitHub repo with a README and a Python `.gitignore`, downloads it, and opens it in VS Code. The `.gitignore` keeps files like your virtual environment and secrets off GitHub.

Add this line to the end of `.gitignore` so your local database is never uploaded:

```
*.db
```

### 4. Create the virtual environment

A virtual environment gives this project its own private set of Python libraries, so projects never break each other.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pytest httpx sqlalchemy
python --version
```

You'll see `(.venv)` at the start of the terminal line when it's active. **Activate it in every new terminal.** If conda's `(base)` also shows, run `conda deactivate` first, or turn it off for good with `conda config --set auto_activate_base false`.

### 5. Select the interpreter in VS Code

1. Press Cmd+Shift+P.
2. Run **Python: Select Interpreter**.
3. Pick the one with `.venv` in its path.

This lets VS Code autocomplete and check your code. Also turn on **File → Auto Save** so pytest never runs an unsaved file.

## Step 1: First endpoint and first test

Step 1 ends with a running FastAPI server, one `/health` endpoint, and one passing test.

### 1. Create the folders and files

```
app/__init__.py        (empty: makes app a package Python can import)
app/main.py
tests/__init__.py      (empty)
tests/test_health.py
```

### 2. Write the endpoint in `app/main.py`

```python
from fastapi import FastAPI

app = FastAPI(title="FullChair")


@app.get("/health")
def health():
    return {"ok": True}
```

`@app.get("/health")` is a decorator: when someone sends a GET request to `/health`, FastAPI runs the function below it and turns the returned dictionary into JSON.

| Decorator | Used for | Example |
| --- | --- | --- |
| `@app.get` | Reading data | Viewing appointments |
| `@app.post` | Creating things | Booking an appointment |
| `@app.put` / `@app.patch` | Updating | Changing an appointment time |
| `@app.delete` | Deleting | Cancelling an appointment |

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

`app.main:app` means: in the file `app/main.py`, run the object called `app`. `--reload` restarts the server whenever you save. Stop it with Ctrl+C.

Then open:

- http://127.0.0.1:8000/health shows `{"ok":true}`.
- http://127.0.0.1:8000/docs shows interactive API docs FastAPI builds for you.

Visiting `http://127.0.0.1:8000/` alone shows `{"detail":"Not Found"}`. That's expected: there's no endpoint for `/`.

### 4. Write the test in `tests/test_health.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
```

Run it with `pytest`. You should see `1 passed`.

`TestClient` sends fake requests straight to your app without starting a server, so tests run in milliseconds. pytest only finds files and functions whose names start with `test_`.

### 5. Server vs. pytest

|  | Running the server | Running pytest |
| --- | --- | --- |
| Command | `uvicorn app.main:app --reload` | `pytest` |
| What it does | Starts the app and keeps listening on port 8000 | Runs your test functions, then exits |
| How you check it | By hand, in the browser or `/docs` | Automatically, with `assert` |
| Stops | When you press Ctrl+C | By itself |

### 6. Commit and push

```bash
pip freeze > requirements.txt
git add .
git commit -m "FastAPI app with health endpoint and first test"
git push
```

- `pip freeze > requirements.txt` records the exact library versions, so anyone can reinstall them with `pip install -r requirements.txt`.
- `git add .` stages your changes.
- `git commit -m "..."` saves a snapshot with a message.
- `git push` uploads your commits to GitHub.

## Step 2: Database models

Step 2 defines FullChair's five tables with SQLAlchemy and proves the relationships work with a test. SQLAlchemy is an ORM: you write Python classes, and it writes the SQL for you.

### 1. The design

```
Salon ──< Stylist ──< Appointment >── Client
  │                       │
  └──< Service ───────────┘      (──< means "has many")
```

Two design decisions:

- **Prices are stored in cents** (`8500`, not `85.00`), because decimals in computers produce rounding errors like `0.1 + 0.2 = 0.30000000000000004`.
- **Appointments store `start_at` and `end_at`**, which makes checking for overlapping appointments simple in Step 4.

### 2. Connect to the database: `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(
    "sqlite:///fullchair.db",
    connect_args={"check_same_thread": False},
    echo=True,
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
```

| Piece | What it is | Analogy |
| --- | --- | --- |
| `engine` | The connection to the database, created once | The hallway to the filing cabinet |
| `SessionLocal` | A factory that makes a new session each time you call it | A machine that hands out clipboards |
| A session | Collects changes; `commit()` saves them all at once | A clipboard of changes |
| `Base` | Parent class every table inherits from, so SQLAlchemy knows it exists | The sign-up sheet for tables |

- `"sqlite:///fullchair.db"` is a relative path: the file is created in whatever folder you run the app from, so always run from the project folder.
- `check_same_thread: False` lets FastAPI's threads (workers) share the SQLite connection. It's SQLite-only and must sit inside `connect_args`.
- `echo=True` prints every SQL statement, which is great for learning. Set it to `False` if output gets noisy.

### 3. Define the tables: `app/models.py`

```python
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Salon(Base):
    __tablename__ = "salons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    stylists: Mapped[list["Stylist"]] = relationship(back_populates="salon")
    services: Mapped[list["Service"]] = relationship(back_populates="salon")
    clients: Mapped[list["Client"]] = relationship(back_populates="salon")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="salon")


class Stylist(Base):
    __tablename__ = "stylists"

    id: Mapped[int] = mapped_column(primary_key=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    name: Mapped[str] = mapped_column(String(100))

    salon: Mapped["Salon"] = relationship(back_populates="stylists")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="stylist")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    name: Mapped[str] = mapped_column(String(100))
    duration_minutes: Mapped[int]
    price_cents: Mapped[int]

    salon: Mapped["Salon"] = relationship(back_populates="services")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="service")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))

    salon: Mapped["Salon"] = relationship(back_populates="clients")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="client")


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    salon_id: Mapped[int] = mapped_column(ForeignKey("salons.id"))
    stylist_id: Mapped[int] = mapped_column(ForeignKey("stylists.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    start_at: Mapped[datetime]
    end_at: Mapped[datetime]
    status: Mapped[str] = mapped_column(String(20), default="booked")

    salon: Mapped["Salon"] = relationship(back_populates="appointments")
    stylist: Mapped["Stylist"] = relationship(back_populates="appointments")
    service: Mapped["Service"] = relationship(back_populates="appointments")
    client: Mapped["Client"] = relationship(back_populates="appointments")
```

Every class is built from three kinds of lines:

1. `__tablename__`: the table's name in the database.
2. **Columns** (`Mapped[...] = mapped_column(...)` or just `Mapped[...]`): real data stored in the database, including foreign keys like `salon_id`.
3. **Relationships** (`relationship(...)`): not stored. Python shortcuts like `stylist.salon` or `salon.stylists` that use the foreign keys to fetch related objects.

Other details: `primary_key=True` makes `id` the unique row number (1, 2, 3...); `String(100)` caps text at 100 characters; `default="booked"` fills in the status when you don't pass one. Indentation decides what belongs to a class: every line must be indented under its `class`.

### 4. The naming rules (the part that causes most errors)

**Plural or singular:** ask "from here, how many of the other thing are there?" Many → plural list (`salon.stylists`, `Mapped[list["Stylist"]]`). One → singular object (`stylist.salon`, `Mapped["Salon"]`).

**`ForeignKey` takes a database name; `back_populates` takes a Python name:**

| Where | Uses | Example |
| --- | --- | --- |
| `__tablename__`, `ForeignKey(...)` | The table name, `"table.column"` | `ForeignKey("salons.id")` |
| `back_populates=...` | The attribute name on the OTHER class, copied exactly | `back_populates="salon"` |
| `Mapped["..."]` | The class name | `Mapped["Salon"]` |

Every relationship pair, with what each side's `back_populates` copies:

| Class | Attribute | One or many | back\_populates |
| --- | --- | --- | --- |
| Salon | `stylists` | many | `"salon"` |
| Stylist | `salon` | one | `"stylists"` |
| Salon | `services` | many | `"salon"` |
| Service | `salon` | one | `"services"` |
| Salon | `clients` | many | `"salon"` |
| Client | `salon` | one | `"clients"` |
| Salon | `appointments` | many | `"salon"` |
| Appointment | `salon` | one | `"appointments"` |
| Stylist | `appointments` | many | `"stylist"` |
| Appointment | `stylist` | one | `"appointments"` |
| Service | `appointments` | many | `"service"` |
| Appointment | `service` | one | `"appointments"` |
| Client | `appointments` | many | `"client"` |
| Appointment | `client` | one | `"appointments"` |

Check any `back_populates`: go to the class in `Mapped[...]`, find an attribute with exactly that name, and confirm its `back_populates` points back.

### 5. Create the tables when the app starts

Add these lines to `app/main.py`, above `app = FastAPI(...)`:

```python
from app import models  # noqa: F401  (registers the tables with Base)
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
```

`create_all` creates any missing tables and never wipes existing ones. It runs whenever `main.py` is imported, including when pytest imports it, which is what creates `fullchair.db`.

### 6. Test the models

`tests/conftest.py` gives every test a fresh, empty, in-memory database (Step 3 replaces this file with an upgraded version):

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401
from app.database import Base


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
```

A fixture is setup code pytest runs for you: any test with a parameter named `db` receives this session. Code before `yield` runs before the test; code after runs afterward to clean up.

`tests/test_models.py`:

```python
from datetime import datetime, timedelta

from sqlalchemy import select

from app.models import Appointment, Client, Salon, Service, Stylist


def test_book_an_appointment(db):
    salon = Salon(name="Juniper Hair Studio")
    stylist = Stylist(name="Aisha", salon=salon)
    service = Service(name="Silk Press", duration_minutes=90, price_cents=8500, salon=salon)
    client = Client(name="Sara", phone="+17345550101", salon=salon)

    start = datetime(2026, 11, 3, 10, 0)
    appointment = Appointment(
        salon=salon,
        stylist=stylist,
        service=service,
        client=client,
        start_at=start,
        end_at=start + timedelta(minutes=service.duration_minutes),
    )
    db.add(appointment)
    db.commit()

    saved = db.scalars(select(Appointment)).one()
    assert saved.stylist.name == "Aisha"
    assert saved.end_at == datetime(2026, 11, 3, 11, 30)
    assert saved.status == "booked"
    assert salon.stylists == [stylist]
    assert client.appointments == [saved]
```

`db.add(appointment)` also saves the salon, stylist, service, and client, because SQLAlchemy follows the relationships (a cascade). `select(Appointment)` builds a query, and `.one()` fails if there isn't exactly one result.

Run `pytest`: **2 passed**. Then commit: `git add .`, `git commit -m "Add SQLAlchemy models with relationships and tests"`, `git push`.

### 7. Seeing what's happening

- `pytest -v` lists every test by name.
- `pytest -s` shows `print()` output and the SQL from `echo=True`.
- The **SQLite Viewer** VS Code extension shows `fullchair.db` like a spreadsheet; or run `sqlite3 fullchair.db`, then `.tables` and `SELECT * FROM salons;`.
- Click left of a line number to set a breakpoint, then debug the test from the Testing tab (flask icon).

## Step 3: API endpoints

Step 3 lets people create and view salons and stylists through the API, with validation, error codes, and tests. Done when `pytest -v` shows **8 passed**.

### 1. One database session per request: `get_db` in `app/database.py`

Add to the bottom of `app/database.py`:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This is the bridge between FastAPI and SQLAlchemy. During one request:

1. An endpoint asks for `db: Session = Depends(get_db)`, so FastAPI calls `get_db()`.
2. `SessionLocal()` opens a fresh session for this request.
3. `yield db` hands the session to the endpoint and pauses `get_db`.
4. The endpoint runs its queries and returns.
5. FastAPI resumes `get_db`, and `finally` closes the session, even if the endpoint crashed.

Each request gets its own session, so requests never mix their changes. This pattern is called dependency injection.

### 2. Schemas: `app/schemas.py`

Models describe the database; schemas describe what goes in and out of the API.

```python
from pydantic import BaseModel, ConfigDict, Field


class SalonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class SalonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class StylistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class StylistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    salon_id: int
```

- `SalonCreate` is what someone sends: just a name, since the database assigns the `id`.
- `SalonOut` is what the API sends back.
- `Field(min_length=1, max_length=100)` rejects empty or too-long names before your code runs.
- `from_attributes=True` lets Pydantic read a SQLAlchemy object and turn it into JSON.

### 3. Endpoints: `app/main.py`

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db
from app.schemas import SalonCreate, SalonOut, StylistCreate, StylistOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FullChair")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/salons", response_model=SalonOut, status_code=201)
def create_salon(salon_in: SalonCreate, db: Session = Depends(get_db)):
    salon = models.Salon(name=salon_in.name)
    db.add(salon)
    db.commit()
    db.refresh(salon)
    return salon


@app.get("/salons", response_model=list[SalonOut])
def list_salons(db: Session = Depends(get_db)):
    return db.scalars(select(models.Salon).order_by(models.Salon.id)).all()


@app.get("/salons/{salon_id}", response_model=SalonOut)
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return salon


@app.post("/salons/{salon_id}/stylists", response_model=StylistOut, status_code=201)
def create_stylist(salon_id: int, stylist_in: StylistCreate, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    stylist = models.Stylist(name=stylist_in.name, salon=salon)
    db.add(stylist)
    db.commit()
    db.refresh(stylist)
    return stylist


@app.get("/salons/{salon_id}/stylists", response_model=list[StylistOut])
def list_stylists(salon_id: int, db: Session = Depends(get_db)):
    salon = db.get(models.Salon, salon_id)
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return salon.stylists
```

| Piece | What it does |
| --- | --- |
| `@app.post("/salons")` | POST creates something; runs this function |
| `response_model=SalonOut` | Sends the result back in the `SalonOut` shape |
| `salon_in: SalonCreate` | Reads and validates the request's JSON |
| `Depends(get_db)` | Gives the function a database session |
| `{salon_id}` in the URL | A path parameter: `/salons/5` sets `salon_id = 5` |
| `db.get(models.Salon, salon_id)` | Looks up a row by ID; `None` if missing |
| `db.refresh(salon)` | Reloads the row to get the new `id` |
| `raise HTTPException(404, ...)` | Stops and returns Not Found |

| Status code | Meaning |
| --- | --- |
| 200 | OK (the default) |
| 201 | Created successfully |
| 404 | Not found |
| 422 | The data sent was invalid |

### 4. Try it in the browser

Run `uvicorn app.main:app --reload` and open http://127.0.0.1:8000/docs.

1. **POST /salons** → Try it out → `{"name": "Juniper Hair Studio"}` → Execute. Expect 201 with an `id`.
2. **GET /salons** to see it listed.
3. **GET /salons/{salon\_id}** with 999 to see the 404.
4. **POST /salons** with `{"name": ""}` to see the 422.
5. Add a stylist to the salon, then list them.
6. Open `fullchair.db` in SQLite Viewer to see the saved rows.

### 5. Upgrade the fixtures: `tests/conftest.py`

Replace the whole file:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.database import Base, get_db
from app.main import app


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

- `StaticPool` makes every connection share the same in-memory database; without it, the test client sees an empty database.
- `dependency_overrides` swaps the real `get_db` for the test session, so endpoint tests never touch `fullchair.db`.

### 6. Endpoint tests: `tests/test_salons.py`

```python
def test_create_salon(client):
    response = client.post("/salons", json={"name": "Juniper Hair Studio"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Juniper Hair Studio"
    assert "id" in data


def test_list_salons(client):
    client.post("/salons", json={"name": "Juniper"})
    client.post("/salons", json={"name": "Maple"})

    response = client.get("/salons")

    assert response.status_code == 200
    assert [s["name"] for s in response.json()] == ["Juniper", "Maple"]


def test_get_missing_salon_returns_404(client):
    response = client.get("/salons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Salon not found"


def test_empty_name_is_rejected(client):
    response = client.post("/salons", json={"name": ""})

    assert response.status_code == 422


def test_add_and_list_stylists(client):
    salon_id = client.post("/salons", json={"name": "Juniper"}).json()["id"]

    created = client.post(f"/salons/{salon_id}/stylists", json={"name": "Aisha"})
    assert created.status_code == 201
    assert created.json()["salon_id"] == salon_id

    stylists = client.get(f"/salons/{salon_id}/stylists").json()
    assert [s["name"] for s in stylists] == ["Aisha"]


def test_stylist_for_missing_salon_returns_404(client):
    response = client.post("/salons/999/stylists", json={"name": "Aisha"})

    assert response.status_code == 404
```

These cover the happy path (things working) and sad paths (missing salon, empty name). Run `pytest -v`: **8 passed**.

### 7. Commit

```bash
git add .
git commit -m "Add salon and stylist endpoints with validation and tests"
git push
```

**Bonus challenge:** add `GET /salons/{salon_id}/stylists/{stylist_id}` that returns one stylist, with a 404 if it doesn't exist or belongs to another salon, plus a test for it.

## Debugging guide

Every error so far came from a small mismatch: a name, an indent, an unsaved file, or the wrong environment.

### How to read an error

1. Press **Cmd+K** to clear the terminal, save all files, and rerun, so the error is current.
2. Read the bottom line starting with `E` first: it names the error type and the problem.
3. Walk up the trace to the first line in **your** code; skip anything in `.venv/lib/...`.
4. Compare that line to what you meant to write.
5. If the error quotes code you've already changed, the output is stale or the file isn't saved.

### Errors hit so far

| Error | Cause | Fix |
| --- | --- | --- |
| `collected 0 items` | Test file unsaved (white dot on the tab), or file not named `test_*.py` | Save with Cmd+S; rename `testmodels.py` to `test_models.py` |
| `Address already in use` | Another server (e.g. the old AI-Receptionist) is on port 8000 | `lsof -i :8000`, then `kill <PID>`; or use `--port 8001` |
| `{"ok":true,"ai":false}` in the browser | That's the old app, not yours | Stop the old server (above) |
| `{"detail":"Not Found"}` | No endpoint at that URL (e.g. `/`) | Visit `/health` or `/docs` |
| `Invalid argument(s) 'check_same_thread'` | Passed directly to `create_engine` | Wrap it: `connect_args={"check_same_thread": False}` |
| `cannot import name 'Base'` | `Base` written as `def`, or nested inside another class | `class Base(DeclarativeBase): pass` at the top level of the file |
| `could not assemble any primary key columns` | Lines under the class aren't indented, so `id` is outside it | Indent every column 4 spaces under its `class` |
| `cannot import name 'Salon'` | Class renamed (e.g. `class salons`) by Find and Replace | Class names are capitalized and singular: `Salon` |
| `Mapper 'X' has no property 'y'` | A `back_populates` names an attribute that doesn't exist on class X | Copy the exact attribute name from class X (pairs table in Step 2) |
| `'duration_minutes' is an invalid keyword argument` | The test passes a name the class doesn't have | Add the column, or match names between test and model |
| `ModuleNotFoundError` / missing `(.venv)` | Virtual environment not active in this terminal | `source .venv/bin/activate` |
| Python 3.9.6 in the status bar | Old macOS Python | Recreate `.venv` with `python3.12 -m venv .venv` and reselect the interpreter |

### Prevention habits

- Turn on Auto Save, or press Cmd+S before every run.
- Open the test and the model side by side; every keyword the test passes must exist on the class with the same spelling.
- Avoid Replace All in code. If you use Find and Replace, turn on Match Case (`Aa`) and Whole Word (`ab`). Cmd+Z undoes a bad replace.
- Commit after every working piece, so you can always get back to a good state.

## Daily workflow cheat sheet

Start every session by opening the project and activating the environment; end it with a commit.

```bash
# start of a session
cd ~/Documents/GitHub/fullchair
code .
source .venv/bin/activate

# while working
uvicorn app.main:app --reload     # run the app (Ctrl+C to stop)
pytest                            # run all tests
pytest -v                         # list each test by name
pytest -s                         # show print() and SQL output
pytest tests/test_salons.py       # run one test file

# after installing a new library
pip install <name>
pip freeze > requirements.txt

# save your work
git status                        # see what changed
git add .
git commit -m "Describe what you did"
git push

# fixing a busy port
lsof -i :8000
kill <PID>
```

| Address | What you see |
| --- | --- |
| http://127.0.0.1:8000/health | `{"ok":true}` |
| http://127.0.0.1:8000/docs | Interactive API docs to try every endpoint |