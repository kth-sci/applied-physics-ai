#!/usr/bin/env python3
"""Build enriched attendee + Claude-request lists for the May 8 tutorial.

Produces:
  attendees/may8-attendees.csv         (with position + division)
  attendees/may8-attendees.txt         (with position + division)
  attendees/claude-requests.csv        (deduped; X-marker for May 8 attendees)
  attendees/claude-requests.txt        (same, paste-friendly)

Position + division lookup is sourced from the public BON / Biophysics / LAMP
staff directories on aphys.kth.se. Anything not in those rosters is left
blank with a note.
"""
import csv
import json
import os
import sys
import urllib.request
from pathlib import Path

HYPHA = "https://hypha.aicell.io"
ROOT = Path(__file__).parent
REG_URL = f"{HYPHA}/kth-sci/artifacts/aphys-ai-registrations/children?pagination=true&limit=200&silent=true"
REQ_URL = f"{HYPHA}/kth-sci/artifacts/aphys-ai-claude-requests/children?pagination=true&limit=200&silent=true"

# (name_lower, division, position) — sourced from APHYS division staff pages and KTH profiles.
# Names are matched case-insensitive on full name; emails act as a secondary fallback.
ROSTER = [
    # ── Bio-Opto-Nano Physics (BON) ──
    ("linda lundström",                "BON",        "Professor (Head of BON)"),
    ("anna burvall",                   "BON",        "Associate Professor"),
    ("ulrich vogt",                    "BON",        "Professor (Deputy Head of Dept)"),
    ("carlota canalias",               "BON",        "Professor (Head of Department)"),
    ("carlota canalias gomez",         "BON",        "Professor (Head of Department)"),
    ("jonas sellberg",                 "BON",        "Associate Professor"),
    ("hans hertz",                     "BON",        "Senior Professor"),
    ("haichun liu",                    "BON",        "Researcher"),
    ("vaishali adya",                  "BON",        "Assistant Professor"),
    ("michael fokine",                 "BON",        "Professor"),
    ("anand srinivasan",               "BON",        "Professor"),
    ("muhammet toprak",                "BON",        "Professor"),
    ("ilja sytjugov",                  "BON",        "Professor"),
    ("peter unsbo",                    "BON",        "Associate Professor"),
    ("jerker widengren",               "BON",        "Professor"),
    ("tunhe zhou",                     "BON",        "Researcher"),
    ("jingjian zhou",                  "BON",        "Postdoc"),
    ("chinmaya venugopal srambickal",  "BON",        "Postdoc"),
    ("zheheng song",                   "BON",        "PhD Student"),
    ("hilma karlsson",                 "BON",        "PhD Student"),
    ("hanie esmaeeli",                 "BON",        "PhD Student"),
    ("faeze mashayekhi",               "BON",        "PhD Student"),
    ("samuel emtell",                  "BON",        "PhD Student"),
    ("abhilash kulkarni",              "BON",        "PhD Student"),
    ("hanna kylhammar",                "BON",        "PhD Student"),
    ("björn-christian ingwersen",      "BON",        "Industry PhD Student"),
    ("erik svanberg",                  "BON",        "PhD Student"),
    ("patricia almudena lopez ramirez","BON",        "PhD Student"),
    ("mikko erik kjellberg",           "BON",        "PhD Student"),
    ("faik ozan özhan",                "BON",        "PhD Student"),
    ("padryk merkl",                   "BON",        "Postdoc"),
    ("daniel voigt",                   "BON",        "Postdoc"),
    ("sandra wagner",                  "BON",        "Postdoc"),
    ("kian shaker",                    "BON",        "Researcher"),
    ("adem ergül",                     "BON",        "Researcher"),
    ("adem björn ergül",               "BON",        "Researcher"),
    ("bertha brodin",                  "BON",        "Researcher"),
    ("marina zelenina",                "BON",        "Lecturer"),

    # ── Biophysics ──
    ("martin viklund",                 "Biophysics", "Professor (Head of Biophysics)"),
    ("hjalmar brismar",                "Biophysics", "Professor"),
    ("lucie delemotte",                "Biophysics", "Professor (Deputy Head of Dept)"),
    ("lucie delemotte moussodia",      "Biophysics", "Professor (Deputy Head of Dept)"),
    ("berk hess",                      "Biophysics", "Professor"),
    ("erik lindahl",                   "Biophysics", "Professor"),
    ("ilaria testa",                   "Biophysics", "Professor"),
    ("björn önfelt",                   "Biophysics", "Professor"),
    ("francesca pennacchietti",        "Biophysics", "Associate Professor"),
    ("melanie hannebelle",             "Biophysics", "Assistant Professor"),
    ("wei ouyang",                     "Biophysics", "Assistant Professor"),
    ("andrea volpato",                 "Biophysics", "Researcher"),
    ("stefan wennmalm",                "Biophysics", "Researcher"),
    ("hans blom",                      "Biophysics", "Researcher"),
    ("yang zhang",                     "Biophysics", "Postdoc"),
    ("simone mariani",                 "Biophysics", "Postdoc"),

    # ── Light and Matter Physics (LAMP) ──
    ("mats ahmadi götelid",            "LAMP",       "Professor (Head of LAMP)"),
    ("alexander balatsky",             "LAMP",       "Professor"),
    ("anna delin",                     "LAMP",       "Professor"),
    ("joydeep dutta",                  "LAMP",       "Professor"),
    ("david b haviland",               "LAMP",       "Professor"),
    ("david haviland",                 "LAMP",       "Professor"),
    ("vladislav korenivski",           "LAMP",       "Professor"),
    ("fredrik laurell",                "LAMP",       "Professor"),
    ("saulius marcinkevicius",         "LAMP",       "Professor"),
    ("sergei popov",                   "LAMP",       "Professor"),
    ("oscar tjernberg",                "LAMP",       "Professor"),
    ("jonas weissenrieder",            "LAMP",       "Professor"),
    ("magnus andersson",               "LAMP",       "Associate Professor"),
    ("ali elshaari",                   "LAMP",       "Associate Professor"),
    ("ali wanis ali elshaari",         "LAMP",       "Associate Professor"),
    ("martin månsson",                 "LAMP",       "Associate Professor"),
    ("yasmine sassa",                  "LAMP",       "Associate Professor"),
    ("johan åkerman",                  "LAMP",       "Researcher"),
    ("alexander edström",              "LAMP",       "Researcher"),
    ("magnus hårdensson berntsen",     "LAMP",       "Researcher"),
    ("fei ye",                         "LAMP",       "Researcher"),
    ("anatolii kravets",               "LAMP",       "Researcher"),
    ("yanting sun",                    "LAMP",       "Researcher"),
    ("andrius zukauskas",              "LAMP",       "Researcher"),
    ("sangita bhowmick",               "LAMP",       "Researcher"),
    ("maciej dendzik",                 "LAMP",       "Researcher"),
    ("gaolong cao",                    "LAMP",       "Researcher"),
    ("yaqun liu",                      "LAMP",       "Postdoc"),
    ("mariia mohylna",                 "LAMP",       "Postdoc"),
    ("qichen xu",                      "LAMP",       "Postdoc"),
    ("erik holmgren",                  "LAMP",       "Research Engineer"),
    ("renan maciel",                   "LAMP",       "PhD Student"),
    ("kritika vijay",                  "LAMP",       "Postdoc"),
    ("lukas müllender",                "LAMP",       "PhD Student"),
    ("satwik mishra",                  "LAMP",       "PhD Student"),
    ("adrian iovan",                   "LAMP",       "Researcher"),

    # ── Outside APHYS dept (cross-school) ──
    ("christian ohm",                  "Particle Physics, Astro & Med Physics (KTH)", "Senior Lecturer (Master's Prog. Director)"),
    ("jonas strandberg",               "Particle Physics, Astro & Med Physics (KTH)", "Associate Professor"),
    ("mats persson",                   "Medical Imaging Physics (KTH)",                "Researcher"),
    ("valdas pasiskevicius",           "Laser Physics, KTH",                            "Faculty"),
    ("bmw",                            "Biophysics",                                    "Professor (Head of Biophysics)"),  # email alias
]

# Build indexes
def normalize(s):
    return s.strip().lower() if s else ""

NAME_LOOKUP = {normalize(n): (div, pos) for n, div, pos in ROSTER}

# Email-based fallback hints (KTH usernames → known person)
EMAIL_HINTS = {
    "iovan@kth.se":    ("LAMP", "Researcher"),
    "bmw@kth.se":      ("Biophysics", "Professor (Head of Biophysics)"),
    "lucied@kth.se":   ("Biophysics", "Professor (Deputy Head of Dept)"),
    "elshaari@kth.se": ("LAMP", "Associate Professor"),
    "balatsky@kth.se": ("LAMP", "Professor"),
    "lukasmu@kth.se":  ("LAMP", "PhD Student"),
    "linda@biox.kth.se": ("BON", "Professor (Head of BON)"),
    "hertz@biox.kth.se": ("BON", "Senior Professor"),
    "mats.persson@mi.physics.kth.se": ("Medical Imaging Physics (KTH)", "Researcher"),
    "ascotti@kth.se":  ("LAMP", "PhD Student"),  # Andrea Scotti — KTH profile
    "bcin@kth.se":     ("BON", "Industry PhD Student"),  # Björn-Christian Ingwersen
    "apku@kth.se":     ("BON", "PhD Student"),  # Abhilash Kulkarni
    "oozhan@kth.se":   ("BON", "PhD Student"),  # Faik Ozan Özhan
    "zayouna@kth.se":  ("", "(unknown — check KTH directory)"),
    "palr2@kth.se":    ("BON", "PhD Student"),  # Patricia Almudena Lopez Ramirez
    "faeze@kth.se":    ("BON", "PhD Student"),
    "toprak@kth.se":   ("BON", "Professor"),
}


def lookup(name, email):
    n = normalize(name)
    if n in NAME_LOOKUP:
        div, pos = NAME_LOOKUP[n]
        return div, pos
    e = normalize(email)
    if e in EMAIL_HINTS:
        return EMAIL_HINTS[e]
    # try last name match
    parts = n.split()
    if len(parts) > 1:
        # match on family name + first initial
        for k, v in NAME_LOOKUP.items():
            kp = k.split()
            if len(kp) > 1 and kp[-1] == parts[-1] and kp[0][:1] == parts[0][:1]:
                return v
    return "", ""


def fetch(url):
    return json.loads(urllib.request.urlopen(url, timeout=20).read())


def build_attendees():
    data = fetch(REG_URL)
    items = data.get("items", [])
    # Dedupe by email, keep earliest
    seen, unique = set(), []
    items.sort(key=lambda i: i["manifest"].get("timestamp", ""))
    for item in items:
        m = item["manifest"]
        e = normalize(m.get("email", ""))
        if not e or e in seen:
            continue
        seen.add(e)
        div, pos = lookup(m.get("name", ""), m.get("email", ""))
        m["division"] = div
        m["position"] = pos
        unique.append(m)
    return unique


def build_requests():
    data = fetch(REQ_URL)
    items = data.get("items", [])
    items.sort(key=lambda i: i["manifest"].get("timestamp", ""))
    # Dedupe by email — keep latest (re-applications overwrite earlier)
    by_email = {}
    for item in items:
        m = item["manifest"]
        e = normalize(m.get("email", ""))
        if not e:
            continue
        by_email[e] = m  # later entries overwrite, since we sorted ascending
    out = []
    for m in by_email.values():
        div, pos = lookup(m.get("name", ""), m.get("email", ""))
        m["division"] = div
        if not m.get("position") or m.get("position") in ("博士生",):
            m["position"] = pos or "PhD Student" if "博" in (m.get("position") or "") else m.get("position") or pos
        m["registered_may8"] = False  # filled below
        out.append(m)
    return out


def main():
    attendees = build_attendees()
    requests = build_requests()

    # Cross-check: which Claude requesters are registered for May 8?
    attendee_emails = {normalize(a["email"]) for a in attendees}
    for r in requests:
        r["registered_may8"] = normalize(r["email"]) in attendee_emails

    # ── Write attendees CSV (with position + division) ──
    with open(ROOT / "may8-attendees.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "name", "email", "attendance", "experience", "position", "division", "timestamp"])
        for i, m in enumerate(attendees, 1):
            w.writerow([
                i, m.get("name", ""), m.get("email", ""), m.get("attendance", ""),
                m.get("experience", ""), m.get("position", ""), m.get("division", ""),
                (m.get("timestamp") or "")[:10],
            ])

    # ── Write attendees TXT (paste-friendly) ──
    with open(ROOT / "may8-attendees.txt", "w") as f:
        f.write(f"# {len(attendees)} unique attendees\n\n")
        f.write("# All emails (paste into BCC):\n")
        f.write(", ".join(a["email"] for a in attendees))
        f.write("\n\n# Detailed list:\n")
        for i, m in enumerate(attendees, 1):
            div = f" — {m['division']}" if m.get("division") else ""
            pos = f" [{m['position']}]" if m.get("position") else ""
            f.write(f"{i:2}. {m.get('name','?')} <{m.get('email','?')}>{div}{pos}  "
                    f"({m.get('attendance','?')}, {m.get('experience','?')})\n")

    # ── Write claude requests CSV ──
    with open(ROOT / "claude-requests.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "name", "email", "position", "seat", "status", "may8_attendee",
                    "division", "motivation", "timestamp"])
        for i, m in enumerate(requests, 1):
            w.writerow([
                i, m.get("name", ""), m.get("email", ""), m.get("position", ""),
                m.get("seat", ""), m.get("status", "pending"),
                "yes" if m.get("registered_may8") else "no",
                m.get("division", ""), (m.get("motivation") or "").replace("\n", " ").strip(),
                (m.get("timestamp") or "")[:10],
            ])

    # ── Write claude requests TXT ──
    pending  = [r for r in requests if r.get("status", "pending") == "pending"]
    approved = [r for r in requests if r.get("status") == "approved"]
    rejected = [r for r in requests if r.get("status") == "rejected"]
    with open(ROOT / "claude-requests.txt", "w") as f:
        f.write(f"# {len(requests)} unique Claude Team requests "
                f"({len(approved)} approved, {len(pending)} pending, {len(rejected)} rejected)\n\n")
        attn_only = [r for r in requests if not r.get("registered_may8")]
        cross     = [r for r in requests if r.get("registered_may8")]
        f.write(f"## Cross-check vs May 8 attendees\n")
        f.write(f"  - Requests from May 8 attendees: {len(cross)}\n")
        f.write(f"  - Requests NOT registered for May 8: {len(attn_only)}\n\n")

        for label, group in [("APPROVED", approved), ("PENDING", pending), ("REJECTED", rejected)]:
            if not group:
                continue
            f.write(f"## {label} ({len(group)})\n")
            for r in group:
                marker = "✓ May 8" if r.get("registered_may8") else "✗ no May 8"
                div = f" — {r['division']}" if r.get("division") else ""
                f.write(f"  [{marker}] {r.get('name','?')} <{r.get('email','?')}>"
                        f" — {r.get('position','?')} / {r.get('seat','standard')}{div}\n")
            f.write("\n")

        f.write("## All emails (paste into BCC for any blast):\n")
        f.write(", ".join(r["email"] for r in requests))
        f.write("\n")

    print(f"Attendees: {len(attendees)}")
    print(f"Claude requests: {len(requests)} ({len(approved)} approved / {len(pending)} pending / {len(rejected)} rejected)")
    print(f"Cross-check: {sum(1 for r in requests if r['registered_may8'])} requesters are also May 8 attendees")
    missing = [a for a in attendees if not a.get("position")]
    if missing:
        print(f"\nMissing position info ({len(missing)}):")
        for a in missing:
            print(f"  - {a.get('name','?')} <{a.get('email','?')}>")


if __name__ == "__main__":
    main()
