# Remote Job Tracker

A full‑stack web app to log job applications, track pipeline status, and visualize analytics to improve your job search.

---

## ✨ Current Status (MVP in progress)

* **Monorepo** with `backend/` (Django + DRF) and `frontend/` (React + Vite + Tailwind v4)
* **Backend**: Django + DRF project with health endpoint and first domain models (Job, Note, Tag) wired for migrations.
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

* ✅ Models: `Job`, `Note`, `Tag`
* DRF serializers + viewsets and routes under `/api/*`
* React Router pages: Dashboard, Applications
* Analytics endpoint + charts (applications/week, status breakdown)
* Auth (JWT), protected routes, user profiles

---

## 📖 User Stories (MVP)

### Core CRUD
- **As a job seeker, I can create a job entry with a title, company, source, link, status, salary range, location, applied date, next action date, and notes so that I can track opportunities in one place.**  
  - Given I am on the "Add Job" form  
  - When I fill in all required fields and click "Save"  
  - Then a new job entry is created and shown in my job list with the provided details.  

- **As a job seeker, I can edit any job entry so that my records stay accurate and up to date.**  
  - Given I am viewing a job in my list  
  - When I click "Edit," update a field, and save  
  - Then the job entry is updated and displays the new information.  

- **As a job seeker, I can delete a job entry so that I can remove irrelevant or outdated opportunities.**  
  - Given I am viewing a job in my list  
  - When I click "Delete" and confirm  
  - Then the job entry is removed from my list.  

### Status Tracking
- **As a job seeker, I can update the status of a job (Wishlist → Applied → Interview → Offer → Rejected) so that I can see where I stand in the hiring pipeline.**  
  - Given a job exists in my list  
  - When I select a new status from the dropdown  
  - Then the job’s status is updated and visible in the list.  

### Filtering & Searching
- **As a job seeker, I can filter my jobs by status so that I can focus on opportunities at a specific stage.**  
  - Given I have multiple jobs with different statuses  
  - When I select a filter option (e.g., "Interview")  
  - Then only jobs with that status are shown in the list.  

- **As a job seeker, I can search jobs by company name or job title so that I can quickly find specific entries.**  
  - Given I have jobs saved with different titles and companies  
  - When I type a keyword into the search bar  
  - Then only jobs that match the keyword appear in the list.  

### Notes
- **As a job seeker, I can add timestamped notes to a job entry so that I can log progress, reminders, or interactions with recruiters.**  
  - Given I am viewing a job entry  
  - When I add a note and click "Save"  
  - Then the note is saved with the current date/time and displayed in a log under that job.  

---

## 🔮 Future Enhancements

These features are out of scope for the MVP but are planned for later iterations:

### Job Management
- Attach **CVs, cover letters, or interview prep documents** to each application.
- Add **tags/categories** (e.g. "Tech", "Finance", "Start-up") for easier grouping.
- Import job postings directly from **LinkedIn / Indeed / API integrations**.

### Collaboration & Communication
- Add recruiter or hiring manager **contact details** to job entries.
- Enable **email integration** (auto-pulling emails into notes, reminders for follow-ups).
- Support **in-app notifications** (e.g., upcoming interview dates, deadlines).

### Calendar & Scheduling
- Calendar view with **upcoming interviews / follow-ups**.
- Sync with **Google Calendar / Outlook** for reminders.

### Analytics & Insights
- Track **time in pipeline stages** (e.g., average days from application to interview).
- Add charts for **conversion rates** (applied → interview → offer).
- Compare **applications across industries or roles**.

### User Accounts & Profiles
- Multi-user support (different job seekers, shared accounts).
- OAuth login with **Google/GitHub/LinkedIn**.
- User settings for **custom statuses** or **preferred salary currency**.

### Mobile & Offline
- **Mobile-friendly PWA** for on-the-go job tracking.
- Offline mode with **local storage sync**.

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
