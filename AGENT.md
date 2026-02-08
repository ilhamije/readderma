# Project: AI-Assisted Clinical Trial Discovery (Skin Conditions)

## Your Role
You are an AI coding agent building a **working prototype** for a 24-hour hackathon.

This project is evaluated on:
- AI nativeness
- Reasoning and decision-making
- UX empathy
- Clear communication

It is **NOT** evaluated on production readiness or frontend sophistication.

You MUST:
- Generate ALL required code
- Keep the system simple and reliable
- Respect all scope boundaries below
- Prefer clarity over complexity

---

## Problem Statement
Patients often fail to discover relevant clinical trials due to:
- Lack of awareness that trials exist
- Complex and unreadable eligibility criteria
- Poor discovery tools designed for researchers, not patients

This prototype helps patients:
1. Upload a skin image
2. Receive an AI-assisted **pre-screening condition category**
3. Discover **actively recruiting clinical trials** related to that condition

This tool is for **clinical trial discovery only**.  
It does **NOT** provide medical diagnosis or treatment advice.

---

## Specific Skin Conditions
'Basal Cell Carcinoma', 'Darier_s Disease', 'Epidermolysis Bullosa Pruriginosa', 'Hailey-Hailey Disease', 'Herpes Simplex', 'Impetigo', 'Larva Migrans', 'Leprosy Borderline', 'Leprosy Lepromatous', 'Leprosy Tuberculoid', 'Lichen Planus', 'Lupus Erythematosus Chronicus Discoides', 'Melanoma', 'Molluscum Contagiosum', 'Mycosis Fungoides', 'Neurofibromatosis', 'Papilomatosis Confluentes And Reticulate', 'Pediculosis Capitis', 'Pityriasis Rosea', 'Porokeratosis Actinic', 'Psoriasis', 'Tinea Corporis', 'Tinea Nigra', 'Tungiasis', 'actinic keratosis', 'dermatofibroma', 'nevus', 'pigmented benign keratosis', 'seborrheic keratosis', 'squamous cell carcinoma', 'vascular lesion'

## Scope Constraints (VERY IMPORTANT)
- Condition focus: **Skin Conditions only**
- Primary user: **Patient or caregiver**
- Platform: **Web app (mobile-friendly)**
- No authentication or user accounts
- No persistent storage of images or personal data
- No medical advice, diagnosis, or severity scoring

If a feature does not directly support trial discovery, DO NOT build it.

---

## Core User Flow (Must Match Exactly)

1. User lands on a simple page explaining the tool
2. User uploads or captures a skin image
3. AI returns:
   - A condition category (Skin Conditions)
   - A confidence band (Low / Medium / High)
   - A plain-language explanation
4. The system fetches **actively recruiting clinical trials**
5. Trials are displayed as simple cards with explanations

---

## Core Features

### 1. Image Upload
- Accept image via file input or camera
- Process image in memory only
- Do NOT store images on disk or database

---

### 2. AI Pre-Screening (NOT Diagnosis)
- Use a pretrained, mocked, or simplified skin classifier
- Output:
  - Condition category: “Skin Conditions”
  - Confidence band: Low / Medium / High
  - Non-technical explanation
- NEVER use the word “diagnosis”

---

### 3. Clinical Trial Matching
- Use **ClinicalTrials.gov public API**
- Filter criteria:
  - Recruiting status: ACTIVE / RECRUITING
  - Condition: Skin Conditions
- Use an LLM to:
  - Simplify eligibility text
  - Generate a short “Why this may fit you” explanation

---

### 4. Results UI
Display trial results as cards containing:
- Trial title
- Recruiting status
- Location(s)
- Phase
- AI-generated “Why this may fit you”
- External link to the official ClinicalTrials.gov page

---

## UX & Language Rules
- Use patient-friendly, non-clinical language
- Always include this disclaimer visibly:

  “This tool does not provide medical diagnosis or treatment advice.  
  Results are intended only to help discover relevant clinical trials.”

- Avoid certainty
- Avoid percentages
- Prefer confidence bands and plain explanations

---

## Tech Stack (LOCKED — DO NOT CHANGE)
- Backend: **FastAPI**
- Frontend: **Server-rendered HTML (Jinja2 or plain HTML)**
- Styling: **Tailwind CSS via CDN**
- JavaScript: Minimal vanilla JS (`fetch`, form submission)
- AI:
  - Image classifier (real or mocked)
  - LLM for eligibility simplification
- Deployment: **Single Dockerized web app**

NO React  
NO Next.js  
NO separate frontend server  

---

## Success Criteria
A judge should be able to:
1. Open the app on a mobile browser
2. Upload a skin image
3. See an AI-assisted condition category
4. View real, actively recruiting clinical trials
5. Understand *why* those trials were shown

---

## Output Expectations
- Simple, readable code
- Clear folder structure
- Inline comments explaining AI usage
- One-command local run or Docker run
- A working demo is more important than polish

Build only what is necessary to demonstrate:
AI reasoning, patient empathy, and clinical trial discovery.
