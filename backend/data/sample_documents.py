"""
Healthcare Intelligence Platform - Sample Clinical Documents
Anonymized sample documents for testing and demonstration
"""

SAMPLE_DOCUMENTS = [
    {
        "title": "Discharge Summary - Diabetic Patient",
        "type": "discharge_summary",
        "content": """
DISCHARGE SUMMARY

Patient: John Doe (Anonymized)
Age: 65 years old
Gender: Male
Admission Date: 01/15/2024
Discharge Date: 01/20/2024
Attending Physician: Dr. Sarah Smith, MD

CHIEF COMPLAINT:
Hyperglycemia with blood glucose level of 450 mg/dL, accompanied by fatigue and increased urination.

HISTORY OF PRESENT ILLNESS:
The patient is a 65-year-old male with a history of Type 2 Diabetes Mellitus, Hypertension, and Hyperlipidemia who presented to the Emergency Department with symptoms of polyuria, polydipsia, and fatigue for the past week. Blood glucose on arrival was 450 mg/dL. Patient was found to have diabetic ketoacidosis (DKA) and was admitted to the ICU for management.

PAST MEDICAL HISTORY:
1. Type 2 Diabetes Mellitus - diagnosed 10 years ago
2. Hypertension - on medication for 15 years
3. Hyperlipidemia - on statin therapy
4. Coronary Artery Disease - status post CABG 2018
5. Chronic Kidney Disease Stage 3

PAST SURGICAL HISTORY:
- Coronary Artery Bypass Grafting (CABG) x3 - 2018
- Appendectomy - 1990

MEDICATIONS ON ADMISSION:
1. Metformin 1000mg BID
2. Glipizide 10mg BID
3. Lisinopril 20mg daily
4. Atorvastatin 40mg daily
5. Aspirin 81mg daily
6. Metoprolol 50mg BID

ALLERGIES:
- Penicillin (rash)
- Sulfa drugs (anaphylaxis)

SOCIAL HISTORY:
- Former smoker, quit 10 years ago (30 pack-year history)
- Occasional alcohol use
- Retired engineer
- Lives with spouse

FAMILY HISTORY:
- Father: Type 2 DM, died of MI at age 70
- Mother: Hypertension, alive at 88
- Sibling: Type 2 DM

PHYSICAL EXAMINATION ON ADMISSION:
Vital Signs: BP 145/92, HR 102, RR 24, Temp 98.6°F, SpO2 96% on RA
General: Alert, oriented, mild distress
HEENT: Dry mucous membranes
Cardiovascular: Tachycardia, regular rhythm, no murmurs
Respiratory: Clear to auscultation bilaterally, mild tachypnea
Abdomen: Soft, non-tender, no organomegaly
Extremities: No edema, pulses intact
Neurological: Alert and oriented x3, no focal deficits

LABORATORY DATA:
Glucose: 450 mg/dL (H)
HbA1c: 11.2% (H)
BUN: 35 mg/dL (H)
Creatinine: 1.8 mg/dL (H)
eGFR: 38 mL/min/1.73m2
Sodium: 132 mEq/L (L)
Potassium: 5.2 mEq/L
pH: 7.28 (L)
Bicarbonate: 14 mEq/L (L)
Anion Gap: 18 (H)
Beta-hydroxybutyrate: 4.5 mmol/L (H)
WBC: 12,500/uL (H)
Hemoglobin: 13.2 g/dL
Platelets: 235,000/uL

HOSPITAL COURSE:
The patient was admitted to the ICU with diabetic ketoacidosis. He was started on IV insulin infusion and aggressive fluid resuscitation. Anion gap closed within 24 hours and patient was transitioned to subcutaneous insulin. Metformin was held due to acute kidney injury. After stabilization, patient was transferred to the general medicine floor on hospital day 2.

During hospitalization, endocrinology was consulted and recommended initiation of basal-bolus insulin regimen. Diabetes education was provided including carbohydrate counting, insulin administration, and hypoglycemia management.

Nephrology was consulted for acute on chronic kidney injury. Creatinine improved to 1.5 mg/dL with fluid resuscitation. Recommended holding ACE inhibitor until kidney function stabilizes.

DISCHARGE DIAGNOSES:
1. Diabetic Ketoacidosis - resolved
2. Type 2 Diabetes Mellitus, uncontrolled
3. Acute on Chronic Kidney Disease, Stage 3b
4. Hypertension
5. Hyperlipidemia
6. Coronary Artery Disease, stable

DISCHARGE MEDICATIONS:
1. Lantus (insulin glargine) 20 units at bedtime
2. Humalog (insulin lispro) 6 units with meals
3. Metoprolol 50mg BID
4. Atorvastatin 40mg daily
5. Aspirin 81mg daily
6. Lisinopril 20mg daily - HOLD until follow-up
7. Metformin - DISCONTINUED

DISCHARGE INSTRUCTIONS:
1. Check blood glucose 4 times daily (before meals and bedtime)
2. Follow diabetic diet with carbohydrate counting
3. Keep follow-up appointments as scheduled
4. Return to ED for blood glucose >400 or <70, chest pain, shortness of breath

FOLLOW-UP:
1. Primary Care: Dr. Johnson - 1 week
2. Endocrinology: Dr. Williams - 2 weeks
3. Nephrology: Dr. Chen - 2 weeks
4. Cardiology: Dr. Davis - 1 month
5. Lab work: BMP and HbA1c in 3 months

Discharge Condition: Stable, improved
Code Status: Full Code

Signed: Dr. Sarah Smith, MD
Date: 01/20/2024
"""
    },
    {
        "title": "Progress Note - Hypertension Follow-up",
        "type": "progress_note",
        "content": """
PROGRESS NOTE

Date: 01/22/2024
Patient: Jane Smith (Anonymized)
Age: 58 years old
Provider: Dr. Michael Brown, MD

CHIEF COMPLAINT:
Follow-up for hypertension management

HISTORY OF PRESENT ILLNESS:
58-year-old female with history of essential hypertension for 10 years presents for routine follow-up. Patient reports good compliance with medications. She checks blood pressure at home and notes readings ranging from 125-140 systolic and 78-88 diastolic. She denies headaches, visual changes, chest pain, or shortness of breath. No recent dietary changes. Exercises 3 times weekly for 30 minutes.

CURRENT MEDICATIONS:
1. Amlodipine 10mg daily
2. Losartan 100mg daily
3. Hydrochlorothiazide 25mg daily
4. Vitamin D3 2000 IU daily

ALLERGIES: No known drug allergies

REVIEW OF SYSTEMS:
Constitutional: No fever, fatigue, or weight changes
Cardiovascular: No chest pain, palpitations, or edema
Respiratory: No shortness of breath or cough
Neurological: No headaches or dizziness

VITAL SIGNS:
Blood Pressure: 134/82 mmHg
Heart Rate: 72 bpm
Weight: 165 lbs
BMI: 27.2 kg/m2

PHYSICAL EXAMINATION:
General: Well-appearing, no acute distress
Cardiovascular: Regular rate and rhythm, no murmurs, no JVD
Lungs: Clear bilaterally
Extremities: No peripheral edema, pulses 2+ throughout

LABORATORY (from 2 weeks ago):
Basic Metabolic Panel:
- Sodium: 140 mEq/L
- Potassium: 4.0 mEq/L
- Creatinine: 0.9 mg/dL
- eGFR: >90 mL/min/1.73m2
- Glucose: 102 mg/dL

Lipid Panel:
- Total Cholesterol: 195 mg/dL
- LDL: 118 mg/dL
- HDL: 52 mg/dL
- Triglycerides: 125 mg/dL

ASSESSMENT AND PLAN:
1. Essential Hypertension - Currently at goal (<140/90) on triple therapy
   - Continue current regimen
   - Reinforce lifestyle modifications: DASH diet, sodium restriction <2g/day
   - Continue home BP monitoring, target <130/80

2. Prediabetes - Fasting glucose 102, borderline
   - Discussed lifestyle interventions
   - Order HbA1c to assess glycemic status
   - Dietary counseling referral

3. Hyperlipidemia - LDL slightly elevated at 118
   - Patient declined statin therapy at this time
   - Discussed cardiovascular risk
   - Will reconsider at next visit based on ASCVD risk calculation

4. Overweight - BMI 27.2
   - Encouraged increased physical activity
   - Nutrition counseling
   - Goal: 5-10% weight loss over 6 months

HEALTH MAINTENANCE:
- Mammogram: Due, ordered
- Colonoscopy: Up to date (2022)
- Flu vaccine: Administered today
- COVID-19 booster: Recommended, patient deferred

RETURN:
Follow-up in 3 months or sooner if blood pressure not controlled.

Electronically signed by:
Dr. Michael Brown, MD
01/22/2024
"""
    },
    {
        "title": "Lab Report - Complete Blood Count",
        "type": "lab_report",
        "content": """
LABORATORY REPORT

Patient: Robert Johnson (Anonymized)
DOB: 03/15/1960
Age: 63 years
Collection Date: 01/23/2024 08:15
Report Date: 01/23/2024 10:30
Ordering Provider: Dr. Emily Wilson, MD

COMPLETE BLOOD COUNT (CBC) WITH DIFFERENTIAL

Test                    Result      Units       Reference Range     Flag
--------------------------------------------------------------------------------
White Blood Cell Count   12.8        10^3/uL     4.5-11.0            H
Red Blood Cell Count     4.2         10^6/uL     4.5-5.5             L
Hemoglobin              11.8        g/dL        13.5-17.5           L
Hematocrit              35.4        %           40-52               L
MCV                     84          fL          80-100              
MCH                     28.1        pg          27-33               
MCHC                    33.3        g/dL        32-36               
RDW                     15.8        %           11.5-14.5           H
Platelet Count          425         10^3/uL     150-400             H
MPV                     8.9         fL          7.5-11.5            

DIFFERENTIAL:
Neutrophils             78          %           40-70               H
Lymphocytes             14          %           20-40               L
Monocytes               6           %           2-8                 
Eosinophils             1           %           1-4                 
Basophils               1           %           0-1                 

Absolute Counts:
ANC (Abs Neutrophils)   9.98        10^3/uL     1.8-7.7             H
ALC (Abs Lymphocytes)   1.79        10^3/uL     1.0-4.8             
AMC (Abs Monocytes)     0.77        10^3/uL     0.2-0.8             
AEC (Abs Eosinophils)   0.13        10^3/uL     0.0-0.4             
ABC (Abs Basophils)     0.13        10^3/uL     0.0-0.1             H

PERIPHERAL BLOOD SMEAR REVIEW:
RBC Morphology: Normocytic, normochromic with mild anisocytosis
WBC Morphology: Left shift noted with some band forms
Platelet Morphology: Adequate number, normal size and morphology

INTERPRETATION:
- Leukocytosis with neutrophilia and left shift - suggestive of infection or inflammatory process
- Mild normocytic anemia - recommend iron studies, B12, folate
- Elevated RDW - consider nutritional deficiency or chronic disease
- Thrombocytosis - mild, possibly reactive

CLINICAL CORRELATION RECOMMENDED

Pathologist: Dr. Patricia Lee, MD
Laboratory Director: Dr. James Wright, MD
CLIA: 12D0967432
"""
    },
    {
        "title": "Radiology Report - Chest X-Ray",
        "type": "radiology_report",
        "content": """
RADIOLOGY REPORT

Examination: CHEST X-RAY, PA AND LATERAL
Date of Exam: 01/24/2024
Patient: Mary Williams (Anonymized)
DOB: 07/22/1955
Age: 68 years
Ordering Physician: Dr. Thomas Anderson, MD

CLINICAL HISTORY:
68-year-old female with chronic cough and shortness of breath. History of COPD. Rule out pneumonia.

COMPARISON:
Chest X-ray dated 06/15/2023

TECHNIQUE:
PA and lateral views of the chest were obtained.

FINDINGS:

LUNGS: 
The lungs are hyperinflated consistent with known COPD. There is a new patchy opacity in the right lower lobe measuring approximately 3 cm, concerning for pneumonia. No pleural effusion identified. No pneumothorax.

CARDIAC SILHOUETTE:
The cardiac silhouette is mildly enlarged, stable compared to prior study. No pericardial effusion.

MEDIASTINUM:
The mediastinum is midline. The aorta shows calcifications consistent with atherosclerosis. No mediastinal widening or lymphadenopathy.

OSSEOUS STRUCTURES:
Degenerative changes of the thoracic spine. No acute fractures.

IMPRESSION:

1. NEW RIGHT LOWER LOBE OPACITY SUSPICIOUS FOR PNEUMONIA - Clinical correlation recommended. Consider CT chest if no improvement with treatment.

2. Hyperinflated lungs consistent with COPD, stable.

3. Mild cardiomegaly, stable.

4. Atherosclerotic changes of the aorta.

RECOMMENDATIONS:
- Correlate with clinical presentation and laboratory findings
- Consider antibiotic therapy if bacterial pneumonia suspected
- Follow-up chest X-ray in 4-6 weeks to document resolution
- If no improvement, recommend CT chest for further evaluation

Electronically signed by:
Dr. Susan Martinez, MD
Board Certified Radiologist
01/24/2024 14:22

Report finalized: 01/24/2024 14:45
"""
    },
    {
        "title": "Medication Reconciliation",
        "type": "medication_reconciliation",
        "content": """
MEDICATION RECONCILIATION DOCUMENT

Patient: William Thompson (Anonymized)
DOB: 11/30/1952
Age: 71 years
Date: 01/25/2024
Reconciled by: PharmD Jennifer Garcia
Verified by: Dr. Christopher Lee, MD

REASON FOR RECONCILIATION:
Admission to hospital for elective knee replacement surgery

CURRENT MEDICATIONS FROM PATIENT INTERVIEW:

Cardiovascular:
1. Metoprolol Succinate ER 100mg - once daily, morning
   Indication: Atrial fibrillation, rate control
   Last dose: 01/25/2024 7:00 AM
   
2. Eliquis (apixaban) 5mg - twice daily
   Indication: Stroke prevention in AFib
   Last dose: 01/24/2024 6:00 PM (HELD per surgical instructions)
   
3. Lisinopril 10mg - once daily
   Indication: Hypertension
   Last dose: 01/25/2024 7:00 AM
   
4. Furosemide 40mg - once daily
   Indication: Heart failure
   Last dose: 01/25/2024 7:00 AM

Metabolic:
5. Metformin 500mg - twice daily with meals
   Indication: Type 2 Diabetes
   Last dose: 01/24/2024 dinner (HELD per surgical instructions)
   
6. Januvia (sitagliptin) 100mg - once daily
   Indication: Type 2 Diabetes
   Last dose: 01/24/2024 morning (HELD per surgical instructions)

Pain/Musculoskeletal:
7. Meloxicam 15mg - once daily
   Indication: Osteoarthritis pain
   Last dose: 01/20/2024 (HELD 5 days pre-op per instructions)
   
8. Acetaminophen 650mg - as needed for pain
   Indication: Pain relief
   Last dose: 01/24/2024 10:00 PM

Gastrointestinal:
9. Omeprazole 20mg - once daily before breakfast
   Indication: GERD
   Last dose: 01/25/2024 6:30 AM

Supplements:
10. Vitamin D3 2000 IU - once daily
11. Calcium 600mg + D - twice daily
12. Fish Oil 1000mg - once daily
13. Multivitamin - once daily

ALLERGIES:
- Codeine (nausea, vomiting)
- Ibuprofen (GI bleeding)
- Latex (rash) - IMPORTANT for surgical team

MEDICATIONS HELD PRE-OPERATIVELY:
1. Eliquis - held 48 hours pre-op, bridging not required per cardiology
2. Metformin - held 24 hours pre-op
3. Januvia - held day of surgery
4. Meloxicam - held 5 days pre-op

DRUG INTERACTION CHECK:
- No significant interactions identified with current regimen
- Post-operative pain management: AVOID codeine, ibuprofen, and other NSAIDs

POST-OPERATIVE MEDICATION RECOMMENDATIONS:
1. Resume Metoprolol when taking oral medications
2. Resume Lisinopril once euvolemic
3. Restart anticoagulation 24-48 hours post-op per orthopedic surgeon
4. DVT prophylaxis until ambulatory
5. Pain management: Acetaminophen scheduled, consider tramadol if needed
6. Resume diabetic medications when eating, consider sliding scale insulin initially

RECONCILIATION STATUS: COMPLETE

Pharmacist Signature: Jennifer Garcia, PharmD
Physician Signature: Christopher Lee, MD
Date/Time: 01/25/2024 09:15
"""
    }
]


def get_sample_document(doc_type: str) -> dict:
    """Get a sample document by type."""
    for doc in SAMPLE_DOCUMENTS:
        if doc["type"] == doc_type:
            return doc
    return None


def get_all_sample_documents() -> list:
    """Get all sample documents."""
    return SAMPLE_DOCUMENTS
