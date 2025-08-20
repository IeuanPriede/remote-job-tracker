# Remote Job Tracker

A full‑stack web app to log job applications, track pipeline status, and visualize analytics to improve your job search.

---

## ✨ Current Status (MVP in progress)

* **Monorepo** with `backend/` (Django + DRF) and `frontend/` (React + Vite + Tailwind v4)
* **Backend**: Django project scaffolded with a health endpoint at `GET /api/health/`
* **Frontend**: Vite + React app bootstrapped; Tailwind v4 wired via `@tailwindcss/postcss`
* Local dev instructions below reproduce a working setup from a fresh clone

---

## 🧱 Tech Stack

**Frontend**: React, Vite, Tailwind CSS v4, PostCSS 8
**Backend**: Django, Django REST Framework, django-cors-headers
**DB**: PostgreSQL (planned), SQLite (dev default)
**Auth**: JWT (planned)
**Charts**: Recharts (planned)

---

## 📁 Repository Structure

```
remote-job-tracker/
  backend/
    core/                # Django project
    apps/                # App(s) for domain models & views
    manage.py
    venv/                # Local virtualenv (not committed)
  frontend/
    index.html
    src/
      main.jsx
      App.jsx
      index.css          # Tailwind entry
    package.json
  README.md
```

---

## 🚀 Getting Started

### Prerequisites

* **Python** ≥ 3.11
* **Node.js** ≥ 18 (LTS recommended) and **npm**
* **Git**

> Windows shell: PowerShell. Replace paths as needed.

### 1) Clone

```powershell
git clone https://github.com/<YOUR_USERNAME>/remote-job-tracker.git
cd remote-job-tracker
```

### 2) Backend (Django API)

```powershell
cd backend
python -m venv venv
./venv/Scripts/Activate.ps1
pip install django djangorestframework django-cors-headers python-dotenv

# If not already created, start a project
# django-admin startproject core .

python manage.py migrate
python manage.py runserver
# → http://127.0.0.1:8000/api/health/  should return {"status": "ok"}
```

**Minimal wiring (already in repo):**

* `core/urls.py` includes:

  ```py
  from django.contrib import admin
  from django.urls import path
  from apps.views import health

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/health/', health),
  ]
  ```
* `apps/views.py` provides the `health` view returning JSON

### 3) Frontend (React + Vite + Tailwind v4)

```powershell
cd ../frontend
npm install
npm install -D tailwindcss @tailwindcss/postcss postcss autoprefixer
```

Ensure **PostCSS config** uses the v4 plugin:

* `postcss.config.cjs`

  ```js
  module.exports = {
    plugins: {
      '@tailwindcss/postcss': {},
    },
  };
  ```
* `src/index.css`

  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```
* (Optional) `tailwind.config.js` for content scanning

  ```js
  export default {
    content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
    theme: { extend: {} },
    plugins: [],
  };
  ```

Run dev server:

```powershell
npm run dev
# → http://localhost:5173
```

**Sanity test:** in `App.jsx`

```jsx
export default function App() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <h1 className="text-6xl font-extrabold text-red-500 underline">
        HELLO TAILWIND
      </h1>
    </div>
  );
}
```

### 4) Run both servers

* Terminal A (backend): `python manage.py runserver`
* Terminal B (frontend): `npm run dev`

> Tip: From repo root you can start the frontend without `cd`: `npm --prefix frontend run dev`

---

## 🔧 Troubleshooting

* **Tailwind v4 PostCSS error**: If you see *“use `@tailwindcss/postcss`”*, ensure `postcss.config.cjs` matches the snippet above and restart Vite.
* **Unknown at-rule `@tailwind` in VS Code**: Install the **Tailwind CSS IntelliSense** extension or create `.vscode/settings.json` with:

  ```json
  { "css.lint.unknownAtRules": "ignore" }
  ```
* **`npx tailwindcss` not found**: With v4 you don’t need the CLI; PostCSS plugin is enough.
* **LF/CRLF warnings on Windows**: Add `.gitattributes` to normalize line endings:

  ```gitattributes
  * text=auto
  *.{js,jsx,ts,tsx,css,html,json,md,yml,yaml,py} text eol=lf
  *.bat text eol=crlf
  ```

  Then run `git add --renormalize .` and commit.

---

## 🛣️ Roadmap (next)

* Models: `Company`, `JobPosting`, `Application`
* DRF serializers + viewsets and routes under `/api/*`
* React Router pages: Dashboard, Applications, Companies
* Analytics endpoint + charts (applications/week, status breakdown)
* Auth (JWT), protected routes, user profiles
* Deployment (Render/Fly.io for API, Vercel/Netlify for frontend)

---

## 🧪 Health Endpoint (for reference)

**GET** `/api/health/` → `{"status": "ok"}`

---

## 🤝 Contributing / Branch Workflow

```bash
# create a feature branch
git switch -c <your-branch>
# commit and push
git add .
git commit -m "feat: describe your change"
git push -u origin <your-branch>
# open a PR into main
```

---
