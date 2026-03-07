#!/usr/bin/env python3
"""
KE Tech Jobs - Daily Scraper
Scrapes IT/software/tech jobs from Kenyan job boards.
Sources: Corporate Staffing, MyJobMag
Saves results to jobs.json for the frontend website.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

TECH_KEYWORDS = [
    "software", "developer", "engineer", "devops", "cloud", "data analyst",
    "data engineer", "python", "java", "react", "node", "backend", "frontend",
    "fullstack", "full stack", "full-stack", "network", "systems", "database",
    "security", "architect", "machine learning", "artificial intelligence",
    "infrastructure", "linux", "kubernetes", "docker", "SRE", "ERP", "SAP",
    "CRM", "netsuite", "salesforce", "power platform", "cybersecurity",
    "ICT", "information technology", "programmer", "IT manager", "IT support",
    "ict support", "technical support", "aiops", "nlp", "llm", "platform",
    "site reliability", "helpdesk", "service desk", "network admin",
    "system admin", "sysadmin", "web developer", "mobile developer",
    "android", "ios developer", "flutter", "kotlin", "swift",
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def is_tech_job(title: str) -> bool:
    t = title.lower()
    return any(kw.lower() in t for kw in TECH_KEYWORDS)


def categorize(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ["cloud", "devops", "aws", "azure", "gcp",
                             "kubernetes", "docker", "platform engineer",
                             "terraform", "ansible", "ci/cd"]):
        return "Cloud / DevOps"
    if any(k in t for k in ["data engineer", "big data", "etl", "pipeline",
                             "spark", "hadoop", "analytics engineer", "dbt"]):
        return "Data Engineering"
    if any(k in t for k in ["machine learning", "aiops", "nlp", "llm",
                             "artificial intelligence", " ml ", "ai lead"]):
        return "AI / Machine Learning"
    if any(k in t for k in ["architect", "solution design",
                             "enterprise architect"]):
        return "Architecture"
    if any(k in t for k in ["integration", "esb", "middleware",
                             "tibco", "mulesoft"]):
        return "Systems Integration"
    if any(k in t for k in ["systems engineer", "netsuite", " erp ",
                             " sap ", "oracle systems"]):
        return "Systems Engineering"
    if any(k in t for k in ["it support", "ict support", "helpdesk",
                             "it manager", "it operations", "ict manager",
                             "service desk"]):
        return "IT Operations"
    if any(k in t for k in ["telecom", "bss", "oss", "noc engineer",
                             "network engineer"]):
        return "Telecom IT"
    if any(k in t for k in ["cyber", "security analyst", "infosec",
                             " soc ", "penetration"]):
        return "Cybersecurity"
    if any(k in t for k in ["android", "ios", "flutter", "mobile",
                             "kotlin", "swift"]):
        return "Mobile Development"
    return "Software Development"


def clean_title(title: str) -> str:
    """Remove 'Job' suffix and company name after 'at'."""
    t = title.split(" at ")[0] if " at " in title else title
    t = re.sub(r'\s*[Jj]ob\s*$', '', t)
    t = re.sub(r'^[Jj]ob\s+', '', t)
    return t.strip()


def get_company_from_title(title: str) -> str:
    """Extract company name from patterns like 'Role at Company' or 'Role - Company'."""
    if " at " in title:
        return title.split(" at ")[-1].strip()
    if " – " in title:
        return title.split(" – ")[-1].strip()
    if " - " in title:
        return title.split(" - ")[-1].strip()
    return ""


def parse_date(text: str):
    """Parse date strings like 'March 4, 2026' or '4 March 2026'.
    Returns (date_str: str, days_ago: int)."""
    today = datetime.now()
    text = text.strip()
    for fmt in ["%B %d, %Y", "%d %B %Y", "%B %d %Y", "%d %B, %Y"]:
        try:
            dt = datetime.strptime(text, fmt)
            days = max(0, (today - dt).days)
            return dt.strftime("%Y-%m-%d"), days
        except ValueError:
            pass
    return today.strftime("%Y-%m-%d"), 0


# ---------------------------------------------------------------------------
# SCRAPER: CORPORATE STAFFING
# ---------------------------------------------------------------------------

def scrape_corporate_staffing() -> list:
    jobs = []
    pages = [
        "https://www.corporatestaffing.co.ke/category/it-jobs-in-kenya/",
        "https://www.corporatestaffing.co.ke/category/it-jobs-in-kenya/page/2/",
    ]

    for url in pages:
        try:
            print(f"  Fetching: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(resp.text, "html.parser")

            for heading in soup.find_all(["h2", "h3"]):
                a_tag = heading.find("a", href=True)
                if not a_tag:
                    continue
                href = a_tag["href"]
                if "/job/" not in href:
                    continue

                raw_title = a_tag.get_text(strip=True)
                if not is_tech_job(raw_title):
                    continue

                title = clean_title(raw_title)
                company = get_company_from_title(raw_title) or "Kenya"
                link = href

                # Try to find the date in surrounding text
                parent = heading.find_parent()
                date_text = ""
                if parent:
                    full_text = parent.get_text()
                    m = re.search(
                        r'(January|February|March|April|May|June|July|'
                        r'August|September|October|November|December)'
                        r'\s+\d{1,2},\s+\d{4}',
                        full_text
                    )
                    if m:
                        date_text = m.group(0)

                posted, days_ago = parse_date(date_text) if date_text else (
                    datetime.now().strftime("%Y-%m-%d"), 0
                )

                if days_ago > 7:
                    continue

                jobs.append({
                    "id": abs(hash(title + link)) % 10_000_000,
                    "title": title,
                    "company": company,
                    "location": "Nairobi",
                    "type": "Full-time",
                    "category": categorize(title),
                    "daysAgo": days_ago,
                    "posted": posted,
                    "source": "Corporate Staffing",
                    "sourceUrl": link,
                    "applyUrl": link,
                    "description": "",
                    "responsibilities": [],
                    "requirements": [],
                    "howToApply": (
                        "Visit the Corporate Staffing listing page for full "
                        "details and to apply online."
                    ),
                })

            time.sleep(2)

        except Exception as exc:
            print(f"  ERROR scraping Corporate Staffing ({url}): {exc}")

    return jobs


# ---------------------------------------------------------------------------
# SCRAPER: MYJOBMAG
# ---------------------------------------------------------------------------

def scrape_myjobmag() -> list:
    jobs = []
    urls = [
        "https://www.myjobmag.co.ke/jobs-by-field/information-technology",
        "https://www.myjobmag.co.ke/jobs-by-field/information-technology/2",
    ]

    for url in urls:
        try:
            print(f"  Fetching: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(resp.text, "html.parser")
            today = datetime.now()

            for li in soup.find_all("li"):
                a_tag = li.find("a", href=lambda h: h and "/job/" in h)
                if not a_tag:
                    continue

                title = a_tag.get_text(strip=True)
                if not title or not is_tech_job(title) or len(title) < 6:
                    continue

                link = a_tag["href"]
                if not link.startswith("http"):
                    link = "https://www.myjobmag.co.ke" + link

                # Date
                li_text = li.get_text()
                date_match = re.search(
                    r'(\d{1,2})\s+'
                    r'(January|February|March|April|May|June|July|'
                    r'August|September|October|November|December)',
                    li_text
                )
                days_ago = 0
                posted = today.strftime("%Y-%m-%d")
                if date_match:
                    try:
                        dt = datetime.strptime(
                            f"{date_match.group(1)} {date_match.group(2)} "
                            f"{today.year}",
                            "%d %B %Y"
                        )
                        days_ago = max(0, (today - dt).days)
                        posted = dt.strftime("%Y-%m-%d")
                    except ValueError:
                        pass

                if days_ago > 7:
                    continue

                company = get_company_from_title(title) or "Kenya"
                clean = clean_title(title)

                jobs.append({
                    "id": abs(hash(clean + link)) % 10_000_000,
                    "title": clean,
                    "company": company,
                    "location": "Nairobi",
                    "type": "Full-time",
                    "category": categorize(clean),
                    "daysAgo": days_ago,
                    "posted": posted,
                    "source": "MyJobMag",
                    "sourceUrl": link,
                    "applyUrl": link,
                    "description": "",
                    "responsibilities": [],
                    "requirements": [],
                    "howToApply": (
                        "Visit the MyJobMag listing page for full details "
                        "and to apply."
                    ),
                })

            time.sleep(2)

        except Exception as exc:
            print(f"  ERROR scraping MyJobMag ({url}): {exc}")

    return jobs


# ---------------------------------------------------------------------------
# ENRICHER — fetch individual job page for full details
# ---------------------------------------------------------------------------

def enrich_job(job: dict) -> dict:
    """Fetch the individual job page to extract description,
    responsibilities, requirements, and the real apply URL."""
    try:
        resp = requests.get(job["sourceUrl"], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        content = (
            soup.find("article")
            or soup.find(class_="entry-content")
            or soup.find(id="primary")
            or soup.find(id="content")
        )
        if not content:
            return job

        # --- Description (first long paragraph) ---
        for p in content.find_all("p"):
            txt = p.get_text(strip=True)
            if len(txt) > 80 and not re.search(
                r'click here|apply now|CV writing|shortlist|register your cv',
                txt, re.I
            ):
                job["description"] = txt[:400]
                break

        # --- Responsibilities & Requirements ---
        current_section = None
        for el in content.find_all(["h2", "h3", "h4", "strong", "b", "ul", "ol"]):
            if el.name in ["h2", "h3", "h4", "strong", "b"]:
                tl = el.get_text(strip=True).lower()
                if any(k in tl for k in [
                    "responsibilit", "duties", "what you'll do",
                    "key tasks", "your role", "the role"
                ]):
                    current_section = "resp"
                elif any(k in tl for k in [
                    "qualif", "requirement", "experience",
                    "skills", "about you", "what you need",
                    "knowledge", "preferred"
                ]):
                    current_section = "req"
                else:
                    current_section = None

            elif el.name in ["ul", "ol"] and current_section:
                items = [
                    li.get_text(strip=True)
                    for li in el.find_all("li")
                    if len(li.get_text(strip=True)) > 10
                ]
                if current_section == "resp" and not job["responsibilities"]:
                    job["responsibilities"] = items[:6]
                elif current_section == "req" and not job["requirements"]:
                    job["requirements"] = items[:5]

        # --- Real Apply URL ---
        for a in content.find_all("a", href=True):
            txt = a.get_text(strip=True).lower()
            if any(k in txt for k in [
                "click here to apply", "apply now",
                "apply here", "apply online"
            ]):
                href = a["href"]
                if (href and href != "#"
                        and "corporatestaffing" not in href
                        and "myjobmag" not in href):
                    job["applyUrl"] = href
                break

        # --- How to Apply text ---
        for el in content.find_all(["h2", "h3", "h4", "strong", "b"]):
            if "how to apply" in el.get_text(strip=True).lower():
                nxt = el.find_next(["p", "a"])
                if nxt:
                    job["howToApply"] = nxt.get_text(strip=True)[:300]
                break

        time.sleep(1.5)

    except Exception as exc:
        print(f"    Enrich error for '{job.get('title', '?')[:40]}': {exc}")

    return job


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print(f"\n{'='*60}")
    print(f"  KE Tech Jobs Scraper")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} EAT")
    print(f"{'='*60}\n")

    # 1. Scrape sources
    print("[1/5] Scraping Corporate Staffing...")
    css_jobs = scrape_corporate_staffing()
    print(f"      → {len(css_jobs)} tech jobs found\n")

    print("[2/5] Scraping MyJobMag...")
    mjm_jobs = scrape_myjobmag()
    print(f"      → {len(mjm_jobs)} tech jobs found\n")

    fresh_jobs = css_jobs + mjm_jobs

    # 2. Deduplicate
    print("[3/5] Deduplicating...")
    seen: set = set()
    unique: list = []
    for j in fresh_jobs:
        key = (j["title"].lower()[:40], j["company"].lower()[:20])
        if key not in seen:
            seen.add(key)
            unique.append(j)
    print(f"      → {len(unique)} unique jobs after dedup\n")

    # 3. Enrich (fetch full details for each job page)
    enrich_limit = min(len(unique), 25)
    print(f"[4/5] Enriching top {enrich_limit} jobs with full details...")
    for i, job in enumerate(unique[:enrich_limit]):
        print(f"      {i+1:02d}/{enrich_limit}  {job['title'][:55]}")
        enrich_job(job)

    # 4. Merge with existing jobs.json
    print("\n[5/5] Merging with existing data...")
    existing: list = []
    if os.path.exists("jobs.json"):
        try:
            with open("jobs.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                existing = data.get("jobs", [])
            print(f"      Loaded {len(existing)} existing jobs")
        except Exception as exc:
            print(f"      Could not read jobs.json: {exc}")

    # Merge: new on top, remove stale (> 7 days), deduplicate
    all_jobs: list = []
    seen2: set = set()
    cutoff = datetime.now() - timedelta(days=7)

    for j in unique + existing:
        key = (j.get("title", "").lower()[:40],
               j.get("company", "").lower()[:20])
        if key in seen2:
            continue
        seen2.add(key)
        try:
            posted_dt = datetime.strptime(j["posted"], "%Y-%m-%d")
            if posted_dt >= cutoff:
                all_jobs.append(j)
        except (KeyError, ValueError):
            all_jobs.append(j)

    # Sort newest first
    all_jobs.sort(key=lambda j: j.get("daysAgo", 99))

    # 5. Save
    output = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M EAT"),
        "totalJobs": len(all_jobs),
        "jobs": all_jobs,
    }

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Summary
    today_count  = sum(1 for j in all_jobs if j.get("daysAgo", 99) == 0)
    week_count   = sum(1 for j in all_jobs if j.get("daysAgo", 99) <= 3)

    print(f"\n{'='*60}")
    print(f"  ✅ Done!  Saved {len(all_jobs)} jobs to jobs.json")
    print(f"     Posted today    : {today_count}")
    print(f"     Posted ≤ 3 days : {week_count}")
    print(f"     Total kept      : {len(all_jobs)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
