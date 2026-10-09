# ProtocolX: What Did I Miss? 🔍

## Project Description
A simple AI micro-app designed to solve the "Unread Problem" from overwhelming chat conversations. It quickly analyzes raw chat logs and provides an executive summary, action items, deadlines, and key decisions based on urgency and relevance.

## Gen AI Services Used
* **Service:** Google Gemini API (gemini-3.8-flash model)
* **Implementation Location:** Backend logic in `app.py`. It takes the raw chat stream input, processes the text to extract actionable insights and strict deadlines, and generates the structured markdown summary displayed on the right column of the UI.