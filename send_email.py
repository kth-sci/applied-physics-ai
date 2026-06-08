#!/usr/bin/env python3
"""
General-purpose email CLI for the APHYS AI Initiative.

Usage examples:
  # Send a plain message to one person
  python3 send_email.py --to "Name <email@kth.se>" --subject "Hello" --body "Your message here"

  # Send a Claude seat approval
  python3 send_email.py --to "Name <email@kth.se>" --template claude-approved

  # Send a Claude seat rejection
  python3 send_email.py --to "Name <email@kth.se>" --template claude-rejected

  # Send to multiple recipients
  python3 send_email.py --to "A <a@kth.se>" --to "B <b@kth.se>" --subject "Hi" --body "..."

  # Preview without sending
  python3 send_email.py --to "Name <email@kth.se>" --template claude-approved --dry-run

Credentials are read from .env (SMTP_USER, SMTP_PASS, SMTP_FROM_NAME).
"""
import smtplib, os, sys, argparse, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SMTP_USER     = os.getenv("SMTP_USER", "kth.aphys.ai@gmail.com")
SMTP_PASS     = os.getenv("SMTP_PASS")
SMTP_FROM     = f"{os.getenv('SMTP_FROM_NAME', 'APHYS AI Initiative')} <{SMTP_USER}>"
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 465


# ── HTML wrapper ────────────────────────────────────────────────────────────

def html_wrap(body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/></head>
<body style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;
             color:#333;line-height:1.6;padding:20px;">
  <div style="border-bottom:3px solid #C46849;padding-bottom:12px;margin-bottom:24px;">
    <span style="font-weight:700;color:#C46849;font-size:18px;">APHYS AI Initiative</span>
    <span style="color:#888;font-size:13px;margin-left:8px;">KTH Applied Physics</span>
  </div>
  {body_html}
  <div style="border-top:1px solid #e8e4da;margin-top:32px;padding-top:16px;
              font-size:12px;color:#999;">
    APHYS AI Initiative · KTH Applied Physics ·
    <a href="https://kth-sci.github.io/applied-physics-ai/" style="color:#C46849;">aphys-ai.kth.se</a>
  </div>
</body></html>"""


# ── Templates ────────────────────────────────────────────────────────────────

def template_claude_approved(first_name: str, expiry: str = "") -> tuple[str, str, str]:
    subject = "Your Claude Team seat has been approved"
    expiry_plain = f"\nValid until: {expiry}\n" if expiry else ""
    expiry_html = (
        f'<p style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;'
        f'padding:10px 14px;font-size:14px;color:#166534;margin:12px 0;">'
        f'<strong>Valid until:</strong> {expiry}</p>'
    ) if expiry else ""

    plain = f"""Hi {first_name},

Your request for a Claude Team seat through the KTH Applied Physics AI Initiative has been approved.
{expiry_plain}
Install Claude Code:
  macOS / Linux:  curl -fsSL https://claude.ai/install.sh | bash
  Windows:        irm https://claude.ai/install.ps1 | iex

Then run `claude` and log in with your KTH email address.

If you have any questions, reply to this email.

Best,
Wei Ouyang & Jonas Sellberg
APHYS AI Initiative"""

    html = html_wrap(f"""
  <p>Dear {first_name},</p>
  <p>Your request for a <strong>Claude Team seat</strong> through the KTH Applied Physics AI Initiative
  has been <strong style="color:#059669;">approved</strong>.</p>
  {expiry_html}
  <div style="background:#faf9f4;border:1px solid #e8e4da;border-radius:10px;padding:16px 20px;margin:16px 0;">
    <p style="margin:0 0 8px;font-weight:600;">Install Claude Code</p>
    <p style="margin:0 0 6px;font-size:14px;color:#555;">macOS / Linux / WSL:</p>
    <pre style="background:#1a1a1a;color:#e0e0e0;border-radius:6px;padding:10px 14px;
                font-size:13px;margin:0 0 12px;">curl -fsSL https://claude.ai/install.sh | bash</pre>
    <p style="margin:0 0 6px;font-size:14px;color:#555;">Windows (PowerShell):</p>
    <pre style="background:#1a1a1a;color:#e0e0e0;border-radius:6px;padding:10px 14px;
                font-size:13px;margin:0;">irm https://claude.ai/install.ps1 | iex</pre>
  </div>
  <p>Run <code style="background:#f0ede5;padding:2px 6px;border-radius:4px;
     font-family:monospace;color:#C46849;">claude</code> and log in with your KTH email address.</p>
  <p>Questions? Reply to this email.</p>
  <p>Best,<br/>Wei Ouyang &amp; Jonas Sellberg</p>""")

    return subject, plain, html


def template_seat_type_changed(first_name: str, new_seat: str = "Standard", expiry: str = "") -> tuple[str, str, str]:
    subject = f"Update: your Claude Team seat has been changed to {new_seat}"
    expiry_plain = f"\nValid until: {expiry}\n" if expiry else ""
    expiry_html = (
        f'<p style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;'
        f'padding:10px 14px;font-size:14px;color:#166534;margin:12px 0;">'
        f'<strong>Valid until:</strong> {expiry}</p>'
    ) if expiry else ""

    plain = f"""Hi {first_name},

Your Claude Team seat type has been updated to: {new_seat}
{expiry_plain}
No action is needed — the change takes effect automatically in your Claude account.

If you have questions about your seat type or access level, reply to this email.

Best,
Wei Ouyang & Jonas Sellberg
APHYS AI Initiative"""

    html = html_wrap(f"""
  <p>Dear {first_name},</p>
  <p>Your <strong>Claude Team seat type</strong> has been updated to:
  <strong style="color:#6366f1;">{new_seat}</strong>.</p>
  {expiry_html}
  <p>No action is needed — the change takes effect automatically in your Claude account.</p>
  <p>If you have questions about your seat type or access level, please reply to this email.</p>
  <p>Best,<br/>Wei Ouyang &amp; Jonas Sellberg</p>"""
    )

    return subject, plain, html


def template_claude_rejected(first_name: str) -> tuple[str, str, str]:
    subject = "Your Claude seat request — update"
    plain = f"""Hi {first_name},

Thank you for your interest in the Claude Team seat through the APHYS AI Initiative.

Unfortunately we are unable to approve your request at this time — seats are currently reserved for faculty, researchers, and PhD students within the Department of Applied Physics.

You can still use Claude for free at https://claude.ai, and ChatGPT at https://chat.openai.com.

If your situation has changed or you believe this decision is in error, please reply and we will review.

Best,
Wei Ouyang & Jonas Sellberg
APHYS AI Initiative"""

    html = html_wrap(f"""
  <p>Dear {first_name},</p>
  <p>Thank you for your interest in the Claude Team seat through the APHYS AI Initiative.</p>
  <p>Unfortunately we are unable to approve your request at this time — seats are currently
  reserved for faculty, researchers, and PhD students within the Department of Applied Physics.</p>
  <p>You can still use Claude for free at
  <a href="https://claude.ai" style="color:#C46849;">claude.ai</a>, and ChatGPT at
  <a href="https://chat.openai.com" style="color:#C46849;">chat.openai.com</a>.</p>
  <p>If your situation has changed or you believe this decision is in error,
  please reply and we will review.</p>
  <p>Best,<br/>Wei Ouyang &amp; Jonas Sellberg</p>""")

    return subject, plain, html


TEMPLATES = {
    "claude-approved": template_claude_approved,
    "claude-rejected": template_claude_rejected,
    "seat-type-changed": template_seat_type_changed,
}


# ── Parse "Name <email>" ─────────────────────────────────────────────────────

def parse_recipient(s: str) -> tuple[str, str]:
    m = re.match(r'^(.*?)\s*<([^>]+)>$', s.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    if "@" in s:
        return s.split("@")[0].capitalize(), s.strip()
    raise ValueError(f"Cannot parse recipient: {s!r}  — use 'Name <email@example.com>'")


# ── Send ─────────────────────────────────────────────────────────────────────

def send(to_addr: str, to_name: str, subject: str, plain: str, html: str, dry_run: bool):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SMTP_FROM
    msg["To"]      = f"{to_name} <{to_addr}>"
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html,  "html"))

    if dry_run:
        print(f"[DRY RUN] To: {to_name} <{to_addr}>")
        print(f"          Subject: {subject}")
        print(f"          Body preview: {plain[:120].strip()}…")
        return

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as s:
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    print(f"✓ Sent → {to_name} <{to_addr}>")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="Send emails from the APHYS AI Initiative Gmail account.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Templates:
  claude-approved     Claude Team seat approved — includes install instructions
                      Use --expiry DATE to include an expiration date.
  claude-rejected     Claude seat request declined
  seat-type-changed   Seat type updated — use --seat TYPE and --expiry DATE.

Examples:
  python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --template claude-approved
  python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --template claude-approved --expiry "2027-06-08"
  python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --template seat-type-changed --seat Premium --expiry "2026-09-08"
  python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --subject "Hi" --body "Hello"
  python3 send_email.py --to "A <a@kth.se>" --to "B <b@kth.se>" --template claude-approved --dry-run""")

    p.add_argument("--to",       action="append", required=True,
                   metavar="'Name <email>'", help="Recipient (repeatable)")
    p.add_argument("--subject",  help="Email subject (required without --template)")
    p.add_argument("--body",     help="Plain-text body (required without --template)")
    p.add_argument("--template", choices=TEMPLATES.keys(),
                   help="Use a pre-built template instead of --subject/--body")
    p.add_argument("--expiry",   default="",
                   metavar="DATE", help="Expiration date to embed (e.g. '2027-06-08'); used by claude-approved and seat-type-changed templates")
    p.add_argument("--seat",     default="Standard",
                   metavar="SEAT", help="Seat type label for seat-type-changed template (default: Standard)")
    p.add_argument("--dry-run",  action="store_true",
                   help="Print what would be sent without actually sending")

    args = p.parse_args()

    if not args.template and not (args.subject and args.body):
        p.error("Provide either --template or both --subject and --body")

    if not SMTP_PASS and not args.dry_run:
        p.error("SMTP_PASS not set in .env")

    for raw in args.to:
        name, addr = parse_recipient(raw)
        first = name.split()[0]

        if args.template:
            fn = TEMPLATES[args.template]
            if args.template == "claude-approved":
                subject, plain, html = fn(first, expiry=args.expiry)
            elif args.template == "seat-type-changed":
                subject, plain, html = fn(first, new_seat=args.seat, expiry=args.expiry)
            else:
                subject, plain, html = fn(first)
        else:
            subject = args.subject
            plain   = args.body
            html    = html_wrap(f"<p>{args.body.replace(chr(10), '</p><p>')}</p>")

        send(addr, name, subject, plain, html, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
