# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Spendly" — a personal expense tracker (repo: `spendify-a-expense-calculator-using-claude-code`), built incrementally as a learning exercise. Flask + SQLite + server-rendered Jinja templates, with vanilla CSS/JS: no frontend framework, no build step, no dependencies beyond `requirements.txt`.

The app is scaffolding at this point. Most functionality is still a stub, and the stubs are numbered by teaching step (Step 1: database, Step 3: logout, Step 4: profile, Step 7: add expense, Step 8: edit, Step 9: delete). **Check `app.py` and `database/db.py` before assuming a feature exists** — see "Current state" below.

## Commands

```bash
source venv/bin/activate      # virtualenv already exists at ./venv
pip install -r requirements.txt
python app.py                 # dev server on http://localhost:5001 (note: 5001, not 5000; debug=True)
```

`pytest` and `pytest-flask` are pinned in `requirements.txt`, but **no tests, `conftest.py`, or pytest config exist yet** — `pytest` currently collects nothing. If asked to add tests, create the test layout and any needed fixtures from scratch.

There is no lint or format command configured.

## Current state (what is real vs. stubbed)

- Working routes: `/`, `/register`, `/login`, `/terms`, `/privacy` — all GET-only, and all just `render_template(...)`.
- `login.html` and `register.html` already `POST` to `/login` and `/register`, but those routes are declared without `methods=["GET", "POST"]`, so submitting either form returns **405**. Adding auth means adding the methods *and* the handler logic.
- `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` return plain "coming in Step N" strings.
- `database/db.py` is a comment block only. No DB, no models, no queries anywhere in the app.
- No `app.secret_key`, no session/auth plumbing, no `flask.g` teardown — all of that still needs to be introduced when auth or the DB lands.
- `static/js/main.js` is an empty placeholder (one comment line).

## Architecture

- **`app.py`** — the entire Flask app: one module, all routes registered directly with `@app.route`, no blueprints, no app factory. Keep new routes in the same flat style.
- **`database/db.py`** — the intended single home for DB access: `get_db()` (SQLite connection with `row_factory` and foreign keys on), `init_db()` (`CREATE TABLE IF NOT EXISTS`), `seed_db()` (dev sample data). Implement data access here rather than opening ad-hoc `sqlite3` connections in routes. `expense_tracker.db` is gitignored and created at runtime.
- **`templates/base.html`** — the only layout: nav, footer, and blocks `title` / `head` / `content` / `scripts`. Every page extends it; never duplicate nav or footer markup.
- **Template links use `url_for('<view function name>')`**, not hardcoded paths (`url_for('landing')`, `url_for('terms')`, …). Renaming a view function breaks templates, so grep before renaming.
- **`static/css/style.css`** — one global stylesheet for the whole site (~700 lines), organized by commented section banners (Variables, Reset, Navbar, …). All styling goes here; there is no per-page CSS file, despite `file.txt` referencing a `landing.css` that was never created. New styling must reuse the `:root` design tokens (`--ink*`, `--paper*`, `--accent`, `--accent-2`, `--danger`, `--border*`, `--font-display` = DM Serif Display, `--font-body` = DM Sans, `--radius-*`, `--max-width`, `--auth-width`) rather than introducing raw hex values or new fonts. Fonts load from Google Fonts in `base.html`.
- **JavaScript** — `static/js/main.js` is loaded globally on every page by `base.html`; page-specific behavior instead goes inline in that template's `{% block scripts %}` (see the YouTube modal at the bottom of `landing.html`). Vanilla JS only — no libraries, no CDN scripts.

## Conventions

Taken from `file.txt`, a scratch log of the prompts used to build the project so far (it is a log, not app code):

- Changes are scoped tightly. Prompts routinely say "modify only the hero section" / "do not modify anything else on the page" — do not touch unrelated parts of a template, route, or stylesheet while making a change.
- New UI matches the existing theme instead of introducing a new styling approach.
- No JS/CSS frameworks or new dependencies — vanilla HTML/CSS/JS.
- Each step ends in a single scoped commit with a `<area>: <change>` subject (`landing: add privacy policy page and route`).

`Screenshot 2026-03-25 at 12.36.20 AM.png` at the repo root is the hero-section design mockup the current landing page was built against.
