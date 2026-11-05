# WTU CyberShield Assistant

Classroom-only, fictional evidence dashboard adapted from the instructor's Operation CyberShield student capstone packet, especially pages 6, 8, 9, and 11. The event data is transcribed from page 8. Interpretations are advisory.

## macOS setup in VS Code

1. Extract this folder next to your existing CyberGuardAI project (do not overwrite your original files).
2. Open the folder in VS Code, then Terminal > New Terminal.
3. Run `python3 -m venv .venv`
4. Run `source .venv/bin/activate`
5. Run `python -m pip install -r requirements.txt`
6. Run `python -m streamlit run dashboard_wtu.py`
7. Open http://localhost:8501 if the browser does not open automatically.

If your old dashboard is still using port 8501, press Ctrl+C in its terminal first, or open the new port Streamlit prints.

## Capstone demonstration

- Filter the 17 events using 'login' or 'grant'.
- Show six or more evidence-linked findings and their labels.
- Download one of the five reusable AI prompts and use it in an instructor-approved chat tool.
- Ask whether the 48 MB transfer proves student records were stolen. Correct answer: no, file identities remain unknown.
- Add an instructor-supplied fictional event and explain whether it changes the interpretation.
- Save screenshots and manually verify all AI-generated claims.

## Limitations

This prototype does not scan networks, access university accounts, or perform live monitoring. It does not autonomously call an LLM; it prepares reusable prompts for an approved AI chat service. The local categorization is deterministic and may require analyst review. Budget and presentation deliverables must be prepared separately.
