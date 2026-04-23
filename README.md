# Gabriel Pereira Portfolio

Interactive portfolio built with `Flask`, combining:

- personal resume section
- animated landing page
- project detail pages
- interactive demos in `Python`, `.NET`, and `QA / Analysis`

## Current Stack

- `Python`
- `Flask`
- `HTML / CSS / JavaScript`
- `C# / .NET` project concepts

## Featured Project Areas

- `Python`
  AI code review, challenge generation, remote productivity
- `.NET`
  API monitoring, validation workflows
- `QA / Analysis`
  bug triage, API auditing, test design

## Run Locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Project Structure

- `app.py`: Flask app and demo routes
- `data/profile.py`: portfolio data, CV content, and project metadata
- `templates/`: portfolio layout and project detail pages
- `static/css/style.css`: styling, layout, and animations
- `static/js/app.js`: reveal effects, canvas background, and project filters

## Personalization

Update these files when you want to tailor the portfolio further:

- `data/profile.py`
- `templates/index.html`
- `templates/project.html`
- `static/css/style.css`

## GitHub and Deployment

This project is perfect for GitHub as a code portfolio.

Important note:
- `GitHub Pages` does not run `Flask` applications on the server.
- If you publish with GitHub Pages only, the dynamic Flask routes will not work as they do locally.

Best options:

1. Keep this repository on GitHub as your source code portfolio.
2. Deploy the live Flask app on a Python-friendly platform like `Render`, `Railway`, or `PythonAnywhere`.
3. If you want, create a separate static version later just for `GitHub Pages`.

## Next Improvements

- add screenshots or mockups for each project
- export a dedicated PDF resume
- add an About section
- create a deploy-ready version for hosting
