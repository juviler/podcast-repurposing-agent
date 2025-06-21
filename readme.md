# Podcast Repurposing Agent

A lightweight AI tool that turns podcast transcripts into high-leverage content formats like blog post outlines, LinkedIn posts, YouTube Shorts scripts, and more. Built with Flask and React, powered by GPT-4.

**Live app**: [https://podcast-repurposing-agent-frontend.onrender.com](https://podcast-repurposing-agent-frontend.onrender.com)  
**GitHub repo**: [https://github.com/juviler/podcast-repurposing-agent](https://github.com/juviler/podcast-repurposing-agent)

---

## 🧠 Overview

Podcast episodes often go underutilized once published. This tool helps media teams repurpose episode transcripts into multiple formats using AI — saving time and unlocking new distribution opportunities. Upload a transcript, select an output type, and get AI-generated content in seconds.

---

## 🚀 What It Does

- Accepts transcripts via:
  - File upload (.txt, .pdf, .docx)
  - YouTube URL
- Generates content in 6 formats:
  - Blog post outline
  - Newsletter blurb
  - YouTube Shorts script
  - Quote extraction
  - LinkedIn post draft
  - Internal team summary
- Frontend: React + Chakra UI  
- Backend: Flask + OpenAI GPT-4 API

---

## ⚠️ Limitations

- **YouTube transcripts**: May fail on shared hosts (Render) due to 429 rate limits. Works reliably on localhost.
- **Transcript length**: Limited to ~7,500 tokens for GPT-4. Longer inputs are truncated with a warning.
- **No authentication or storage**: This is a prototype — no sessions, logins, or saved history.

---

## ✅ Assumptions

- Media teams already produce podcast transcripts or upload episodes to YouTube.
- There are existing channels (e.g., newsletters, blogs, social) for repurposed content.
- Human review is still needed before publishing AI-generated outputs.

---

## 🔁 Optional Asana Integration

This tool can integrate with **Asana** to streamline editorial workflows.

- **Single Task Mode**: Generates one task based on selected output (e.g., blog outline).
- **Hub Task Mode**: Creates a parent task with subtasks for each selected output format.

Users review the output, fill in task metadata, and manually trigger task creation. The Asana API is used to generate the task(s) with proper fields and descriptions.

---

## 🛠️ Tools & Platforms Used

- OpenAI GPT-4 API  
- Flask (Python backend)  
- React + Chakra UI (frontend)  
- Asana REST API  
- Render (hosting)

---

## 🧑‍💻 Human Oversight vs. Automation

| Step                        | Automated         | Human Oversight     |
|-----------------------------|-------------------|----------------------|
| Transcript processing       | ✅                |                      |
| AI content generation       | ✅                |                      |
| Output review & approval    |                   | ✅                   |
| Asana task creation         | ✅ (triggered)    | ✅ (manual trigger)  |
| Final editing & publishing  |                   | ✅                   |
