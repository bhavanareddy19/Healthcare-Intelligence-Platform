# Healthcare Intelligence Platform - Testing Guide

## 🧪 Sample Synthetic Clinical Data

Here are 3 sample clinical notes you can copy and use to test the platform:

---

### Sample 1: Diabetes Patient with Multiple Comorbidities

```
PATIENT: John Smith (DOB: 05/15/1958)
MRN: HIP-2024-001
DATE: 01/28/2024
PROVIDER: Dr. Sarah Johnson, MD

CHIEF COMPLAINT: Follow-up for diabetes management

HISTORY OF PRESENT ILLNESS:
66-year-old male with Type 2 Diabetes Mellitus (diagnosed 2010) presents for 
routine follow-up. Patient reports occasional polyuria and mild fatigue. 
Currently on Metformin 1000mg BID and Glipizide 5mg daily. Home glucose 
readings averaging 145-180 mg/dL fasting.

PAST MEDICAL HISTORY:
- Type 2 Diabetes Mellitus (E11.9)
- Essential Hypertension (I10)
- Hyperlipidemia (E78.5)
- Obesity (E66.9) - BMI 32.4
- History of tobacco use, quit 2018

CURRENT MEDICATIONS:
1. Metformin 1000mg BID
2. Glipizide 5mg daily
3. Lisinopril 20mg daily
4. Atorvastatin 40mg daily
5. Aspirin 81mg daily

ALLERGIES: Penicillin (rash)

VITAL SIGNS:
- BP: 142/88 mmHg
- HR: 78 bpm
- Weight: 210 lbs
- Height: 5'9"
- BMI: 31.0

LABORATORY RESULTS (01/20/2024):
- HbA1c: 8.2% (elevated, goal <7%)
- Fasting Glucose: 168 mg/dL (elevated)
- Total Cholesterol: 198 mg/dL
- LDL: 118 mg/dL (slightly elevated)
- HDL: 42 mg/dL (low)
- Triglycerides: 190 mg/dL (elevated)
- Creatinine: 1.1 mg/dL
- eGFR: 72 mL/min/1.73m2 (Stage 2 CKD)
- Microalbumin/Creatinine Ratio: 45 mg/g (elevated)

PHYSICAL EXAMINATION:
General: Alert, oriented, obese male in no distress
HEENT: Normal
Cardiovascular: Regular rate and rhythm, no murmurs
Lungs: Clear bilaterally
Extremities: No edema, peripheral pulses intact
Neurologic: Decreased sensation to monofilament bilateral feet

ASSESSMENT AND PLAN:
1. Type 2 Diabetes, uncontrolled (HbA1c 8.2%)
   - Add Jardiance (empagliflozin) 10mg daily
   - Continue Metformin and Glipizide
   - Diabetes education referral
   - Goal HbA1c < 7%

2. Hypertension, not at goal
   - Increase Lisinopril to 40mg daily
   - Goal BP < 130/80

3. Diabetic nephropathy, early stage
   - Jardiance will provide renal protection
   - Recheck microalbumin in 3 months

4. Peripheral neuropathy
   - Refer to podiatry
   - Foot care education

5. Hyperlipidemia
   - Increase Atorvastatin to 80mg daily
   - Dietary counseling

FOLLOW-UP: 3 months
```

---

### Sample 2: Cardiac Patient - Post MI Follow-up

```
PATIENT: Maria Garcia (DOB: 03/22/1962)
MRN: HIP-2024-002
DATE: 01/28/2024
PROVIDER: Dr. Michael Chen, MD, Cardiology

CHIEF COMPLAINT: Post-MI follow-up, 6 weeks post-event

HISTORY OF PRESENT ILLNESS:
61-year-old female presenting for follow-up after NSTEMI on 12/15/2023. 
Patient underwent PCI with drug-eluting stent to LAD. Currently on dual 
antiplatelet therapy. Reports some residual fatigue but denies chest pain, 
dyspnea, or palpitations. Participating in cardiac rehabilitation.

PAST MEDICAL HISTORY:
- NSTEMI (I21.4) - December 2023
- Coronary artery disease (I25.10)
- Type 2 Diabetes Mellitus (E11.65)
- Former smoker (15 pack-years, quit post-MI)

CURRENT MEDICATIONS:
1. Aspirin 81mg daily
2. Clopidogrel (Plavix) 75mg daily
3. Metoprolol succinate 50mg daily
4. Lisinopril 10mg daily
5. Atorvastatin 80mg daily
6. Metformin 500mg BID

VITAL SIGNS:
- BP: 118/72 mmHg
- HR: 62 bpm
- Weight: 165 lbs
- O2 Sat: 98% RA

LABORATORY RESULTS:
- Troponin I: <0.01 ng/mL (normal)
- BNP: 85 pg/mL (normal)
- LDL: 68 mg/dL (at goal)
- HbA1c: 6.8%
- Creatinine: 0.9 mg/dL

ECHOCARDIOGRAM (01/20/2024):
- EF: 50% (mild reduction)
- Anteroapical hypokinesis
- No significant valvular disease
- No pericardial effusion

ASSESSMENT AND PLAN:
1. CAD s/p NSTEMI and PCI to LAD
   - Continue DAPT for 12 months
   - Continue statin, beta-blocker, ACE-I
   - Cardiac rehab 3x/week

2. Heart failure with reduced EF (HFrEF)
   - EF 50%, monitor closely
   - Consider adding Entresto if EF declines

3. Type 2 Diabetes, controlled
   - HbA1c at goal
   - Continue current regimen

4. Smoking cessation
   - Congratulate on quitting
   - Continue support

FOLLOW-UP: 3 months with repeat echo
```

---

### Sample 3: Pediatric Asthma Case

```
PATIENT: Emily Johnson (DOB: 08/10/2016)
MRN: HIP-2024-003
DATE: 01/28/2024
PROVIDER: Dr. Lisa Park, MD, Pediatrics

CHIEF COMPLAINT: Asthma follow-up, increased symptoms

HISTORY OF PRESENT ILLNESS:
7-year-old female with moderate persistent asthma presents for follow-up. 
Mother reports increased nighttime coughing (3-4 nights/week) and need 
for rescue inhaler 4-5 times weekly over past month. No recent URI or 
known trigger exposure. School reported gym class participation limited.

PAST MEDICAL HISTORY:
- Moderate persistent asthma (J45.40), diagnosed age 4
- Allergic rhinitis (J30.9)
- Eczema (L30.9)

ALLERGIES: 
- Environmental: dust mites, cat dander, grass pollen
- No known drug allergies

CURRENT MEDICATIONS:
1. Flovent HFA (fluticasone) 44mcg 2 puffs BID
2. Albuterol HFA PRN
3. Zyrtec 5mg daily
4. Flonase 1 spray each nostril daily

VITAL SIGNS:
- BP: 98/62 mmHg
- HR: 88 bpm
- RR: 18/min
- Weight: 52 lbs (50th percentile)
- Height: 48 inches (60th percentile)
- O2 Sat: 99% RA
- Peak Flow: 180 L/min (80% predicted)

PHYSICAL EXAMINATION:
General: Alert, active, in no distress
HEENT: Clear rhinorrhea, pale turbinates
Lungs: Mild expiratory wheezes bilaterally, good air movement
Skin: Dry patches bilateral antecubital fossae

ASTHMA CONTROL TEST (ACT) Score: 16 (not well-controlled, goal >19)

ASSESSMENT AND PLAN:
1. Moderate persistent asthma, not well-controlled
   - Step up therapy: Increase Flovent to 110mcg 2 puffs BID
   - Add Singulair (montelukast) 5mg chewable daily
   - Review inhaler technique
   - Asthma action plan updated

2. Allergic rhinitis
   - Continue Flonase and Zyrtec
   - Consider allergy testing if symptoms persist

3. Compliance assessment
   - Discussed importance of daily controller medication
   - Spacer use demonstrated

FOLLOW-UP: 4 weeks to reassess control
```

---

## 📋 Step-by-Step Testing Guide

### Step 1: Start the Backend Server

```bash
cd Healthcare-Intelligence-Platform/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Verify Backend is Running

Open a browser and go to:
- **http://localhost:8000** - Should show "Healthcare Intelligence Platform is running"
- **http://localhost:8000/docs** - Interactive API documentation (Swagger UI)

### Step 3: Start the Frontend (New Terminal)

```bash
cd Healthcare-Intelligence-Platform/frontend
npm install
npm run dev
```

You should see:
```
VITE ready in X ms
➜  Local:   http://localhost:5173/
```

### Step 4: Open the Application

Go to **http://localhost:5173** in your browser.

---

## 🧭 Feature Walkthrough

### 1. Dashboard (Home Page)
- View platform overview and statistics
- See available agents and their status
- Quick action buttons

### 2. Upload Documents
- Click **"Upload"** in the navigation
- Click **"Load Sample Documents"** to load pre-configured samples
- OR drag-and-drop your own PDF/TXT/DOCX files

### 3. Semantic Search
- Click **"Search"** in the navigation
- Try these sample queries:
  - "patient with diabetes"
  - "medications for blood pressure"
  - "lab results abnormal"
- Toggle **"Use RAG"** for AI-enhanced answers

### 4. Multi-Agent Analysis (Most Important Feature!)
- Click **"Agents"** in the navigation
- Copy one of the sample clinical notes above
- Paste into the text area OR click **"Load Sample Text"**
- Select specific agents or leave all selected
- Click **"Run Analysis"**
- View results from each specialized agent:
  - Diagnoses extracted
  - ICD-10 codes suggested
  - Medications analyzed
  - Risk factors identified
  - Clinical summary generated

### 5. Analytics Dashboard
- Click **"Analytics"** in the navigation
- View platform metrics
- See agent performance statistics

---

## 🔬 API Testing with cURL

### Load Sample Documents
```bash
curl -X POST http://localhost:8000/api/documents/sample
```

### Run Multi-Agent Analysis
```bash
curl -X POST http://localhost:8000/api/agents/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "66-year-old male with Type 2 Diabetes presenting with HbA1c 8.2%. Current medications include Metformin 1000mg BID."}'
```

### Semantic Search
```bash
curl -X POST http://localhost:8000/api/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "diabetes treatment", "top_k": 5, "use_rag": true}'
```

---

## 🎯 Key Things to Observe

1. **Agent Execution Time**: Each agent shows how long it took (in milliseconds)
2. **Confidence Scores**: Each agent provides a confidence level for its analysis
3. **ICD-10 Codes**: The system extracts billing codes from clinical text
4. **RAG Context**: Search shows which documents were used for the answer
5. **Executive Summary**: After all agents run, a summary is generated

---

## 📁 Project Structure Quick Reference

```
backend/
├── app/main.py          # FastAPI app entry point
├── core/                # Document processing
├── llm/                 # Groq API & prompts
├── agents/              # 14 specialized agents
└── vectorstore/         # FAISS vector database

frontend/
├── src/App.jsx          # All React components
└── src/index.css        # Premium dark theme
```

---

*Happy Testing! 🚀*
