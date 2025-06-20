import streamlit as st
import requests

st.set_page_config(page_title="AI Diagnostic Assistant", layout="centered")

# Header with styling
st.markdown("""
<h1>🔬 AI Diagnostic Assistant</h1>
<b>Sant Parmanand Hospital</b><br>
<span style='font-size:14px; color:gray;'>
<i>Supervised by Dr. Ankit Jain</i><br>
<i>Built by Principal Researcher <b>Govind Sharma</b>, M.Sc. AI in Medicine (2024–26), DPSRU</i>
</span>
<hr style="margin-top:10px; margin-bottom:20px;">
""", unsafe_allow_html=True)

st.markdown("## 🧪 Enter Your Lab Test Results")

# Input form
with st.form("lab_form"):
    col1, col2 = st.columns(2)

    with col1:
        hemoglobin = st.text_input("Hemoglobin (g/dL)", help="Normal: 12–17.5")
        wbc = st.text_input("WBC (/µL)", help="Normal: 4,000–11,000")
        platelets = st.text_input("Platelets (/µL)", help="Normal: 150,000–450,000")
        ldl = st.text_input("LDL (mg/dL)", help="Optimal: <100")
        hdl = st.text_input("HDL (mg/dL)", help="Optimal: >40 (M), >50 (F)")
        triglycerides = st.text_input("Triglycerides (mg/dL)", help="Normal: <150")
        creatinine = st.text_input("Creatinine (mg/dL)", help="Normal: 0.6–1.3")
        uric_acid = st.text_input("Uric Acid (mg/dL)", help="Normal: 3.5–7.2")

    with col2:
        tsh = st.text_input("TSH (µIU/mL)", help="Normal: 0.4–4.0")
        t3 = st.text_input("T3 (ng/mL)", help="Normal: 0.8–2.0")
        t4 = st.text_input("T4 (µg/dL)", help="Normal: 5.0–12.0")
        alt = st.text_input("ALT (U/L)", help="Normal: 7–56")
        ast = st.text_input("AST (U/L)", help="Normal: 10–40")
        bilirubin = st.text_input("Bilirubin (mg/dL)", help="Normal: 0.1–1.2")
        protein = st.selectbox("Protein in Urine", ["", "Present", "Absent"], help="Normally: Absent")
        rbc = st.text_input("RBC in Urine", help="Normal: 0–2/hpf")

    submitted = st.form_submit_button("🔍 Analyze Report")

# Risk checking
def get_risks(data):
    risks = []
    if data.get("Hemoglobin", 999) < 12: risks.append("Low Hemoglobin – anemia risk")
    if data.get("WBC", 0) > 11000: risks.append("High WBC – infection risk")
    if data.get("Platelets", 999999) < 150000: risks.append("Low Platelets – bleeding risk")
    if data.get("LDL", 0) > 160: risks.append("High LDL – cardiovascular risk")
    if data.get("HDL", 999) < 40: risks.append("Low HDL – poor cholesterol profile")
    if data.get("Triglycerides", 0) > 150: risks.append("High Triglycerides – metabolic risk")
    if data.get("TSH", 0) > 5: risks.append("High TSH – hypothyroidism risk")
    if data.get("TSH", 999) < 0.3: risks.append("Low TSH – hyperthyroidism risk")
    if data.get("ALT", 0) > 55: risks.append("High ALT – liver damage")
    if data.get("AST", 0) > 45: risks.append("High AST – liver inflammation")
    if data.get("Bilirubin", 0) > 1.2: risks.append("High Bilirubin – jaundice risk")
    if data.get("Creatinine", 0) > 1.3: risks.append("High Creatinine – kidney function risk")
    if data.get("Uric Acid", 0) > 7: risks.append("High Uric Acid – gout or kidney risk")
    if data.get("Protein", "").lower() == "present": risks.append("Protein in urine – kidney issue")
    if "3" in str(data.get("RBC", "")): risks.append("RBC in urine – infection or bleeding risk")
    return risks

# Submit handler
if submitted:
    def parse_float(val):
        try: return float(val)
        except: return None

    inputs = {
        "Hemoglobin": parse_float(hemoglobin),
        "WBC": parse_float(wbc),
        "Platelets": parse_float(platelets),
        "LDL": parse_float(ldl),
        "HDL": parse_float(hdl),
        "Triglycerides": parse_float(triglycerides),
        "TSH": parse_float(tsh),
        "T3": parse_float(t3),
        "T4": parse_float(t4),
        "ALT": parse_float(alt),
        "AST": parse_float(ast),
        "Bilirubin": parse_float(bilirubin),
        "Creatinine": parse_float(creatinine),
        "Uric Acid": parse_float(uric_acid),
        "Protein": protein,
        "RBC": rbc
    }

    risks = get_risks(inputs)
    st.markdown("### 📊 AI-Powered Analysis in Progress...")

    prompt = f"""
A patient has submitted lab results:

{inputs}

System-detected risk flags:
{risks}

Please include:
1. Abnormal Test Values – explain in plain language.
2. Risk Assessment – what conditions may arise.
3. Probable Diagnoses.
4. Likely Symptoms.
5. Next Steps for the patient.

Respond in professional, structured medical format.
"""

    headers = {
        "Authorization": "Bearer YOUR_GROQ_API_KEY",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        st.markdown("### 🩺 Diagnosis Report")
        st.markdown(reply)
    else:
        st.error("❌ Failed to get diagnosis.")
