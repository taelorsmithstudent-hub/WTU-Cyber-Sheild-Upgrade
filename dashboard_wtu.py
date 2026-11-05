"""WTU CyberShield: fictional, evidence-first capstone dashboard. Run with Streamlit."""
from pathlib import Path
import csv
import io
import json
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "wtu_events.csv"
INSTRUCTIONS = (ROOT / "agent_instructions.txt").read_text(encoding="utf-8")

st.set_page_config(page_title="WTU CyberShield Assistant", page_icon="🛡️", layout="wide")
st.title("🛡️ WTU CyberShield Assistant")
st.caption("Operation CyberShield • Fictional WTU evidence • October 8, 2026 • Advisory only")
st.info("Classroom simulation only. Do not upload real student records or scan university systems.")

@st.cache_data
def load_events():
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

EVENTS = load_events()

# Deterministic categorization is a classroom aid, not a claim of compromise.
def classify(event):
    s = event["Recorded Event"].lower()
    if "48 mb" in s:
        return "Data transfer", "HIGH", "CONFIRMED: transfer occurred; UNKNOWN: contents and recipient identity"
    if "successful login" in s or "failed login" in s:
        return "Authentication", "HIGH", "CONFIRMED: recorded login; POSSIBLE: unauthorized access"
    if "inbox rule" in s or "application named" in s:
        return "Account changes", "HIGH", "CONFIRMED: account change; POSSIBLE: attacker persistence"
    if "powershell" in s or "beaconing" in s:
        return "Endpoint / network", "HIGH", "CONFIRMED: recorded activity; POSSIBLE: malicious execution or beaconing"
    if "archive" in s or "37 research" in s:
        return "File activity", "MEDIUM", "CONFIRMED: file activity; UNKNOWN: whether files left WTU"
    if "email" in s or "link" in s or "https post" in s:
        return "Phishing / web", "MEDIUM", "CONFIRMED: recorded event; POSSIBLE: credential exposure"
    return "Response / other", "INFO", "CONFIRMED: recorded event"

if "new_events" not in st.session_state:
    st.session_state.new_events = []
rows = EVENTS + st.session_state.new_events
annotated = []
for event in rows:
    category, severity, interpretation = classify(event)
    annotated.append({**event, "Category": category, "Priority": severity, "Assessment": interpretation})

c1, c2, c3 = st.columns(3)
c1.metric("Fictional events", len(rows))
c2.metric("High-priority event flags", sum(x["Priority"] == "HIGH" for x in annotated))
c3.metric("Recorded outbound transfer", "48 MB")

st.subheader("Evidence viewer and timeline")
search = st.text_input("Filter by time, source, or keyword (e.g. login, grant, transfer)")
categories = sorted({x["Category"] for x in annotated})
selected = st.multiselect("Event categories", categories, default=categories)
filtered = [x for x in annotated if x["Category"] in selected and search.lower() in " ".join(str(v) for v in x.values()).lower()]
st.dataframe(filtered, use_container_width=True, hide_index=True)
buffer = io.StringIO()
writer = csv.DictWriter(buffer, fieldnames=["Time", "Source", "Recorded Event", "Category", "Priority", "Assessment"])
writer.writeheader()
writer.writerows(filtered)
st.download_button("Download filtered evidence (CSV)", data=buffer.getvalue(), file_name="wtu_filtered_evidence.csv", mime="text/csv")

st.subheader("Evidence-backed findings")
findings = [
    ("08:03:14", "EMAIL01", "CONFIRMED", "Fake-looking password email delivered; SPF failed."),
    ("08:18:02", "EMAIL01", "CONFIRMED", "Successful login from 203.0.113.77; MFA not required."),
    ("08:20:31", "EMAIL01", "CONFIRMED", "New external forwarding rule for selected messages."),
    ("08:24:48", "FACULTY-LT01", "CONFIRMED", "WINWORD.EXE launched hidden PowerShell activity."),
    ("08:29:56", "FS01", "CONFIRMED", "Archive grantfiles.zip created in temporary folder."),
    ("08:34:15", "NET01", "CONFIRMED", "48 MB outbound transfer recorded."),
    ("08:34:15", "NET01", "UNKNOWN", "Which files were transferred, and who ultimately received them."),
]
for time, source, status, finding in findings:
    st.write(f"**{status}** · {time} · {source} — {finding}")

st.subheader("Three defensive recommendations (for human approval)")
recommendations = [
    {"Action": "Require MFA and review sessions, inbox rules, and app grants", "Evidence": "V-05; 08:18:02, 08:20:31, 08:22:09, 09:02:22", "Security+": "Authentication / MFA", "Verify": "Check MFA enforcement and review session, forwarding-rule, and consent audit results"},
    {"Action": "Restore laptop security sensor reporting and review endpoint alerts", "Evidence": "V-03; 08:24:48", "Security+": "Monitoring / incident response", "Verify": "Confirm sensor check-in and successful alert generation"},
    {"Action": "Update outdated browser component and verify patch status", "Evidence": "V-01; 08:09:42", "Security+": "Vulnerability / patching", "Verify": "Confirm supported version and successful patch scan"},
]
st.dataframe(recommendations, use_container_width=True, hide_index=True)
st.caption("V-01, V-03, V-05 are findings in the instructor packet, not independently verified scans.")

st.subheader("AI assistant: copy a reusable evidence-grounded prompt")
st.caption("No paid API required. Paste this into an instructor-approved AI chat tool; then verify its response against the packet.")
selection = st.selectbox("Prompt portfolio", ["1 – Role", "2 – Evidence", "3 – Security+", "4 – Challenge", "5 – Leadership"])
asks = {
    "1 – Role": "Explain your role, evidence rules, and output format. State how you will avoid unsupported claims.",
    "2 – Evidence": "Identify at least six significant events with exact timestamps and sources, and explain why each matters.",
    "3 – Security+": "Explain V-01 (outdated browser), V-03 (sensor absent 21 days), and V-05 (MFA not required). Suggest a practical control and verification check for each.",
    "4 – Challenge": "Does the 48 MB outbound transfer prove student records were stolen? Separate confirmed observations, possible explanations, and unknowns.",
    "5 – Leadership": "Write a short leadership briefing with evidence, three actions, estimated first-year costs explicitly labeled as assumptions, and an approval decision. Do not invent verified vendor prices.",
}
findings_text = "V-01: outdated browser on WTU-FACULTY-LT01. V-03: security sensor has not checked in for 21 days. V-05: faculty email accounts do not require MFA."
evidence_text = "\n".join(f'{e["Time"]} | {e["Source"]} | {e["Recorded Event"]}' for e in rows)
prompt = f"{INSTRUCTIONS}\n\nFictional WTU findings:\n{findings_text}\n\nFictional WTU logs (2026-10-08, local time):\n{evidence_text}\n\nTASK: {asks[selection]}"
st.text_area("Copy this prompt into your approved AI tool", value=prompt, height=260)
st.download_button("Download current AI prompt", prompt, file_name="wtu_ai_prompt.txt", mime="text/plain")

st.subheader("Acceptance tests")
st.markdown("**Test 1 — Normal evidence:** Use prompt 2; verify six or more timestamps match the table above.\n\n**Test 2 — Missing information:** Provide only the 08:34:15 transfer row and ask which student files were stolen. Correct response: UNKNOWN; request file-level evidence.\n\n**Test 3 — New event:** Add a new *fictional* row below; compare any revised findings to the source. Record the instructor's actual event when provided.")
with st.form("new_event"):
    st.markdown("**Add a fictional test event (not a real-world action)**")
    new_time = st.text_input("Time (HH:MM:SS)", placeholder="09:15:00")
    new_source = st.text_input("Source", placeholder="EMAIL01")
    new_desc = st.text_area("Recorded event")
    add = st.form_submit_button("Add fictional event")
    if add:
        import re
        if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", new_time):
            st.error("Enter a valid 24-hour time, such as 09:15:00.")
        elif not new_source.strip() or not new_desc.strip():
            st.error("Provide a source and recorded event.")
        else:
            st.session_state.new_events.append({"Time": new_time, "Source": new_source.strip(), "Recorded Event": new_desc.strip()})
            st.rerun()
if st.button("Clear fictional test events"):
    st.session_state.new_events = []
    st.rerun()

st.subheader("Export incident report")
report = {"scenario": "Fictional WTU — October 8, 2026", "events": annotated, "findings": [{"time": t, "source": s, "status": c, "finding": f} for t,s,c,f in findings], "recommendations": recommendations, "limitations": ["Logs are incomplete", "48 MB transfer does not identify specific files", "No direct access to student information system is shown", "AI responses require human evidence verification"]}
st.download_button("Download evidence report (JSON)", json.dumps(report, indent=2), file_name="wtu_incident_report.json", mime="application/json")
