#!/usr/bin/env python3
"""
Send the May 8 tutorial preparation email to all registered participants.
Usage:
    python3 send_tutorial_email.py --test          # send only to Wei + Jonas
    python3 send_tutorial_email.py --send          # send to all participants
"""
import smtplib, os, sys, time, argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = f"{os.getenv('SMTP_FROM_NAME', 'APHYS AI Initiative')} <{SMTP_USER}>"

# ── Participant list (43 attendees — synced from attendees/may8-attendees.csv) ─
PARTICIPANTS = [
    ("Jonas Sellberg",                    "jonassel@kth.se",                   "AlbaNova"),
    ("Christian Ohm",                     "chohm@kth.se",                      "AlbaNova"),
    ("Anna Burvall",                      "at@kth.se",                         "AlbaNova"),
    ("Ulrich Vogt",                       "uvogt@kth.se",                      "AlbaNova"),
    ("Magnus Andersson",                  "magnusan@kth.se",                   "AlbaNova"),
    ("Mats Persson",                      "mats.persson@mi.physics.kth.se",    "AlbaNova"),
    ("Carlota Canalias",                  "ccg@kth.se",                        "AlbaNova"),
    ("Valdas Pasiskevicius",              "vp@kth.se",                         "AlbaNova"),
    ("Jingjian Zhou",                     "jingjian@kth.se",                   "AlbaNova"),
    ("Maciej Dendzik",                    "dendzik@kth.se",                    "AlbaNova"),
    ("Satwik Mishra",                     "satwik@kth.se",                     "AlbaNova"),
    ("Sangita Bhowmick",                  "bhowmick@kth.se",                   "AlbaNova"),
    ("Yang Zhang",                        "yangz3@kth.se",                     "AlbaNova"),
    ("Joydeep Dutta",                     "joydeep@kth.se",                    "AlbaNova"),
    ("Yaqun Liu",                         "yaqun@kth.se",                      "Zoom"),
    ("Qichen Xu",                         "qichenx@kth.se",                    "AlbaNova"),
    ("Haichun Liu",                       "haichun@kth.se",                    "AlbaNova"),
    ("Zheheng Song",                      "zheheng@kth.se",                    "AlbaNova"),
    ("Kritika Vijay",                     "kritikav@kth.se",                   "Zoom"),
    ("Tunhe Zhou",                        "tunhe@kth.se",                      "AlbaNova"),
    ("Stefan Wennmalm",                   "stewen@kth.se",                     "Zoom"),
    ("Simone Mariani",                    "smariani@kth.se",                   "Zoom"),
    ("Chinmaya Venugopal Srambickal",     "chivs@kth.se",                      "AlbaNova"),
    ("Gaolong Cao",                       "gaoc@kth.se",                       "AlbaNova"),
    ("Martin Viklund",                    "bmw@kth.se",                        "AlbaNova"),
    ("Andrea Volpato",                    "andrvolp@kth.se",                   "AlbaNova"),
    ("Alexander Edström",                 "aleeds@kth.se",                     "Zoom"),
    ("Linda Lundström",                   "linda@biox.kth.se",                 "AlbaNova"),
    ("Mariia Mohylna",                    "mohylna@kth.se",                    "Zoom"),
    ("Renan Maciel",                      "renanm@kth.se",                     "AlbaNova"),
    ("Erik Holmgren",                     "eholmgr@kth.se",                    "AlbaNova"),
    ("Jonas Strandberg",                  "jostran@kth.se",                    "AlbaNova"),
    ("Lucie Delemotte",                   "lucied@kth.se",                     "Zoom"),
    ("Björn-Christian Ingwersen",         "bcin@kth.se",                       "AlbaNova"),
    ("Andrea Scotti",                     "ascotti@kth.se",                    "AlbaNova"),
    ("Faeze Mashayekhi",                  "faeze@kth.se",                      "AlbaNova"),
    ("Patricia Lopez",                    "palr2@kth.se",                      "AlbaNova"),
    ("Abhilash Kulkarni",                 "apku@kth.se",                       "AlbaNova"),
    ("Faik Ozan Özhan",                   "oozhan@kth.se",                     "AlbaNova"),
    ("Sarah Zayouna",                     "zayouna@kth.se",                    "AlbaNova"),
    ("Hans Hertz",                        "hertz@biox.kth.se",                 "AlbaNova"),
    ("Muhammet Toprak",                   "toprak@kth.se",                     "AlbaNova"),
    ("Adrian Iovan",                      "iovan@kth.se",                      "AlbaNova"),
]

TEST_RECIPIENTS = [
    ("Wei Ouyang",   "wei.ouyang@scilifelab.se", "AlbaNova"),
    ("Jonas Sellberg", "jonassel@kth.se",         "AlbaNova"),
]

# ── Email template ──────────────────────────────────────────────────────────
def make_email(name: str, mode: str) -> tuple[str, str]:
    first = name.split()[0]
    zoom_block = ""
    if mode == "Zoom":
        zoom_block = """
        <div style="background:#f0f4f8;border:1px solid #c5d5e5;border-radius:8px;
                    padding:12px 16px;margin:16px 0;font-size:14px;">
          <strong>You are registered to join via Zoom:</strong><br/>
          <a href="https://kth-se.zoom.us/j/68849683451"
             style="color:#C46849;">https://kth-se.zoom.us/j/68849683451</a>
        </div>"""

    subject = "Getting ready for Thursday — AI Tutorial May 8"
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/></head>
<body style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;
             color:#333;line-height:1.6;padding:20px;">

  <div style="border-bottom:3px solid #C46849;padding-bottom:12px;margin-bottom:24px;">
    <span style="font-weight:700;color:#C46849;font-size:18px;">APHYS AI Initiative</span>
    <span style="color:#888;font-size:13px;margin-left:8px;">KTH Applied Physics</span>
  </div>

  <p>Dear {first},</p>

  <p>We look forward to seeing you this <strong>Thursday, May 8, 13:00–17:00</strong>
  at <strong>FB53, AlbaNova University Center</strong>.</p>

  {zoom_block}

  <p>To make the most of the hands-on parts, please take
  <strong>10–15 minutes before Thursday</strong> to set up two tools on your laptop:</p>

  <div style="background:#faf9f4;border:1px solid #e8e4da;border-radius:10px;
              padding:16px 20px;margin:16px 0;">
    <p style="margin:0 0 8px;font-weight:600;">1. A ChatGPT account (free)</p>
    <p style="margin:0;color:#555;font-size:14px;">
      Sign up at <a href="https://chat.openai.com" style="color:#C46849;">chat.openai.com</a>
      if you don't already have one. The free tier is enough.
    </p>
  </div>

  <div style="background:#faf9f4;border:1px solid #e8e4da;border-radius:10px;
              padding:16px 20px;margin:16px 0;">
    <p style="margin:0 0 8px;font-weight:600;">2. Claude Code — install with one command</p>
    <p style="margin:0 0 10px;color:#555;font-size:14px;">
      You have been granted a KTH Applied Physics <strong>Claude Team seat</strong>.
      Install Claude Code and log in with your KTH email:
    </p>
    <div style="background:#1a1a1a;color:#e0e0e0;border-radius:8px;
                padding:10px 14px;font-family:monospace;font-size:13px;">
      # macOS / Linux<br/>
      curl -fsSL https://claude.ai/install.sh | bash<br/><br/>
      # Windows (PowerShell)<br/>
      irm https://claude.ai/install.ps1 | iex
    </div>
    <p style="margin:10px 0 0;color:#555;font-size:14px;">
      Then run <code style="background:#f0ede5;padding:2px 6px;border-radius:4px;">claude</code>
      and log in — it opens a browser tab. Use your KTH email.
    </p>
  </div>

  <p>Full setup instructions and the day's exercise prompts are at:<br/>
  <a href="https://aphys-ai.kth.se/may8-tutorial"
     style="color:#C46849;font-weight:600;">aphys-ai.kth.se/may8-tutorial</a></p>

  <p><strong>That's it.</strong> No data or slides to prepare — just show up with your laptop.</p>

  <div style="background:#f0f8f4;border-left:4px solid #2D7A4F;border-radius:0 8px 8px 0;
              padding:12px 16px;margin:20px 0;font-size:14px;color:#444;">
    <strong>Programme overview:</strong><br/>
    13:00 Arrival &amp; setup<br/>
    13:15 Context intro — AI and the labor market<br/>
    13:30 ChatGPT hands-on (Jonas)<br/>
    14:00 Claude Code hands-on (Wei)<br/>
    14:30 ☕ Coffee break<br/>
    15:00 Showcases — advanced use cases from colleagues<br/>
    16:00 Group work — build something with AI<br/>
    16:45 Group presentations &amp; wrap-up
  </div>

  <p>See you Thursday!</p>

  <p><strong>Wei Ouyang</strong> &amp; <strong>Jonas Sellberg</strong><br/>
  <span style="color:#888;font-size:13px;">Department of Applied Physics, KTH</span></p>

  <div style="border-top:1px solid #e8e4da;margin-top:28px;padding-top:12px;
              font-size:12px;color:#aaa;">
    APHYS AI Initiative · KTH Royal Institute of Technology ·
    <a href="https://aphys-ai.kth.se" style="color:#C46849;">aphys-ai.kth.se</a>
  </div>

</body></html>"""
    return subject, html


# ── Send logic ──────────────────────────────────────────────────────────────
def send_all(recipients: list, dry_run: bool = False):
    if dry_run:
        print(f"[DRY RUN] Would send to {len(recipients)} recipient(s):")
        for name, email, mode in recipients:
            print(f"  {name} <{email}> [{mode}]")
        return

    print(f"Connecting to smtp.gmail.com:587 as {SMTP_USER}...")
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo(); s.starttls(); s.login(SMTP_USER, SMTP_PASS)
        print(f"Authenticated. Sending to {len(recipients)} recipient(s)...\n")
        for name, email, mode in recipients:
            subject, html = make_email(name, mode)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = SMTP_FROM
            msg["To"]      = email
            msg.attach(MIMEText(html, "html"))
            s.sendmail(SMTP_USER, email, msg.as_string())
            print(f"  ✓ {name} <{email}>")
            time.sleep(1)  # avoid rate-limiting
    print(f"\nDone — {len(recipients)} email(s) sent.")


# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="Send only to Wei + Jonas")
    parser.add_argument("--send", action="store_true",
                        help="Send to all 32 participants")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print list without sending")
    args = parser.parse_args()

    if args.dry_run:
        send_all(PARTICIPANTS, dry_run=True)
    elif args.test:
        send_all(TEST_RECIPIENTS)
    elif args.send:
        confirm = input(f"Send to all {len(PARTICIPANTS)} participants? [yes/no]: ")
        if confirm.strip().lower() == "yes":
            send_all(PARTICIPANTS)
        else:
            print("Aborted.")
    else:
        parser.print_help()
