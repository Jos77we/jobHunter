# 🇰🇪 KE Tech Jobs — Daily IT Jobs in Kenya

A free, auto-updating job board that scrapes IT/software/tech jobs from Kenyan job sites every morning at **7:00 AM EAT** and publishes them as a live GitHub Pages website.

**Your live site will be at:** `https://YOUR-USERNAME.github.io/ke-tech-jobs`

---

## 📁 Project Files

```
ke-tech-jobs/
├── scraper.py                    ← Python scraper (runs daily via GitHub Actions)
├── jobs.json                     ← Auto-generated job data (do NOT edit manually)
├── index.html                    ← Your live website
├── .github/
│   └── workflows/
│       └── scrape.yml            ← GitHub Actions schedule
└── README.md
```

---

## 🪟 Windows Setup Guide (Complete Beginner)

### STEP 1 — Install Python

1. Go to **python.org/downloads**
2. Click the big yellow **Download Python** button
3. Run the `.exe` installer
4. ⚠️ **TICK THIS BOX before clicking Install:**
   ```
   ☑️ Add Python to PATH
   ```
5. Click **Install Now** → wait → click **Close**

**Test it:** Open Command Prompt (press `Win+R`, type `cmd`, press Enter) and run:
```
python --version
```
You should see: `Python 3.x.x` ✅

---

### STEP 2 — Install Git

1. Go to **git-scm.com/download/win**
2. Download the 64-bit installer → run it
3. Click **Next** through everything (all defaults are fine)

**Test it:**
```
git --version
```
You should see: `git version 2.x.x` ✅

---

### STEP 3 — Create a GitHub Account

1. Go to **github.com** → Sign up
2. Choose a username, verify your email

---

### STEP 4 — Create Your Repository

1. On GitHub, click **+** (top right) → **New repository**
2. Name: `ke-tech-jobs`
3. Visibility: ✅ **Public**
4. Tick ✅ **Add a README file**
5. Click **Create repository**

---

### STEP 5 — Create a Personal Access Token

GitHub requires a token instead of your password for command-line access.

1. GitHub → click your profile picture → **Settings**
2. Scroll down → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
4. Note: `ke-tech-jobs`
5. Expiration: **No expiration**
6. Tick ✅ the entire **repo** checkbox section
7. Click **Generate token**
8. **Copy the token** (starts with `ghp_...`) — save it in Notepad, you won't see it again!

---

### STEP 6 — Clone the Repo to Your Computer

Open Command Prompt and run these one by one:

```cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/YOUR-USERNAME/ke-tech-jobs.git
cd ke-tech-jobs
```

When asked for credentials:
- **Username:** your GitHub username
- **Password:** paste your **Personal Access Token** (not your real password)

---

### STEP 7 — Add the Project Files

Create the required folders:
```cmd
mkdir .github
mkdir .github\workflows
```

Now copy these 4 files into the `ke-tech-jobs` folder on your Desktop:
- `scraper.py` → paste into root of the folder
- `index.html` → paste into root of the folder
- `scrape.yml` → paste into `.github\workflows\` subfolder
- `README.md` → already there (overwrite it)

---

### STEP 8 — Install Python Libraries

In Command Prompt (still inside the `ke-tech-jobs` folder):
```cmd
pip install requests beautifulsoup4 lxml
```

---

### STEP 9 — Test the Scraper Locally

```cmd
python scraper.py
```

You'll see it scraping and saving jobs. When it's done, a `jobs.json` file appears in your folder.

Open `index.html` in your browser (double-click it) to preview the website locally. ✅

---

### STEP 10 — Push Everything to GitHub

```cmd
git add .
git commit -m "Initial setup with all project files"
git push origin main
```

Enter your GitHub username and Personal Access Token when prompted.

---

### STEP 11 — Enable GitHub Pages (Makes Your Site Live)

1. Go to your repo on GitHub: `github.com/YOUR-USERNAME/ke-tech-jobs`
2. Click **Settings** tab
3. Left sidebar → **Pages**
4. Under **Source** → **Deploy from a branch**
5. Branch: **main** | Folder: **/ (root)**
6. Click **Save**
7. Wait 2 minutes → your site is live at:
   **`https://YOUR-USERNAME.github.io/ke-tech-jobs`** 🎉

---

### STEP 12 — Run the First Automated Scrape on GitHub

1. Go to your repo → **Actions** tab
2. Click **Daily IT Jobs Scraper**
3. Click **Run workflow** → **Run workflow**
4. Wait ~3 minutes → green ✅ tick means it worked!

From now on, GitHub runs the scraper automatically every day at **7:00 AM Nairobi time**. You don't need to do anything.

---

## 🔧 Common Problems & Fixes

| Problem | Fix |
|---|---|
| `python: command not found` | Reinstall Python with **"Add Python to PATH"** ticked |
| `pip: command not found` | Try `pip3` instead of `pip` |
| Git asks for password | Use your **Personal Access Token**, not your GitHub password |
| Site shows 404 | Wait 5 minutes after enabling GitHub Pages. Check branch is `main` |
| Actions shows ❌ red | Click the failed run to read the error. Most common fix: re-run the workflow |
| `jobs.json` is empty | Scrapers may have been blocked. Try again in a few hours |

---

## ⏰ Schedule

The scraper runs every day at **7:00 AM Nairobi time (EAT)** automatically.
- Scrapes Corporate Staffing IT jobs
- Scrapes MyJobMag IT jobs
- Removes jobs older than 7 days
- Commits updated `jobs.json` to GitHub
- Site automatically shows fresh jobs

## 💰 Cost

**100% FREE.** GitHub Actions free tier = 2,000 minutes/month. This uses ~3 minutes/day = ~90 minutes/month.
