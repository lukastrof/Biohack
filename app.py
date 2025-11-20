import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Neuro-Metabolic Optimizer", page_icon="🧠", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    .highlight { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    .warning-box { border-left: 5px solid #ff4b4b; background-color: #ffe6e6; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- DATA: THE PROTOCOLS ---

# Phase 1: Foundation (Daily)
foundation_stack = [
    {"Name": "Zinc", "Dosage": "15-30mg", "Form": "Picolinate/Bisglycinate", "Purpose": "Testosterone/Dopamine"},
    {"Name": "B-Complex", "Dosage": "1 Serving", "Form": "Must possess P-5-P & 5-MTH", "Purpose": "Methylation"},
    {"Name": "Tongkat Ali", "Dosage": "200-400mg", "Form": "LJ100/200:1", "Purpose": "Free T / Cortisol Control"},
]

# Phase 2: The Learn Stack (Morning)
learn_stack = [
    {"Name": "Alpha-GPC", "Dosage": "300mg", "Form": "50% or 99%", "Purpose": "Choline Donor"},
    {"Name": "ALCAR", "Dosage": "500mg", "Form": "Acetyl-L-Carnitine", "Purpose": "Mitochondrial Fuel"},
    {"Name": "L-Tyrosine", "Dosage": "1000mg", "Form": "Free Form (Not NALT)", "Purpose": "Dopamine Fuel"},
    {"Name": "L-Theanine", "Dosage": "100mg", "Form": "Standardized", "Purpose": "Jitter Control"},
    {"Name": "Caffeine", "Dosage": "50-80mg", "Form": "Coffee/Matcha", "Purpose": "Adenosine Antagonist"},
    {"Name": "Lion's Mane", "Dosage": "1000mg", "Form": "8:1 Fruiting Body", "Purpose": "NGF Stimulation"},
    {"Name": "Uridine", "Dosage": "250mg", "Form": "Monohydrate (UMP)", "Purpose": "Synaptogenesis"},
]

# Phase 3: The Perform Stack (Pre-Work)
perform_stack = [
    {"Name": "Sabroxy", "Dosage": "100mg", "Form": "Oroxylum Indicum", "Purpose": "MAO-B Inhibition"},
    {"Name": "Cordyceps", "Dosage": "1000mg", "Form": "Militaris (Fruiting Body)", "Purpose": "ATP/Stamina"},
    {"Name": "Rhodiola", "Dosage": "300mg", "Form": "3% Rosavins", "Purpose": "Anti-Fatigue/Crash"},
]

# Phase 4: The Recover Stack (Night)
recover_stack = [
    {"Name": "Magnesium", "Dosage": "2000mg (target)", "Form": "L-Threonate (Magtein)", "Purpose": "Neuroplasticity/Sleep"},
    {"Name": "Apigenin", "Dosage": "50mg", "Form": "Chamomile Extract", "Purpose": "CD38 Inhibitor/GABA"},
    {"Name": "Phosphatidylserine", "Dosage": "400mg", "Form": "Soy-Free", "Purpose": "Cortisol Blocker"},
    {"Name": "Bacopa Monnieri", "Dosage": "300mg", "Form": "Synapsa/Bacognize", "Purpose": "Memory Consolidation"},
    {"Name": "Fish Oil", "Dosage": "2000mg", "Form": "High DHA", "Purpose": "Membrane Structure"},
    {"Name": "Ashwagandha", "Dosage": "300mg", "Form": "KSM-66", "Purpose": "Cortisol Crusher"},
]

# Maintenance (Weekend Washout)
maintenance_stack = [
    {"Name": "Creatine", "Dosage": "5g", "Form": "Monohydrate", "Purpose": "ATP Buffer"},
    {"Name": "Magnesium", "Dosage": "2000mg", "Form": "L-Threonate", "Purpose": "Sleep"},
    {"Name": "Fish Oil", "Dosage": "2000mg", "Form": "High DHA", "Purpose": "Repair"},
    {"Name": "Zinc", "Dosage": "15mg", "Form": "Picolinate", "Purpose": "Hormonal Base"},
]

# --- LOGIC ENGINE ---

def get_current_phase(now):
    if now.hour < 11:
        return "Phase 1 & 2: Foundation + Learn"
    elif 11 <= now.hour < 18:
        return "Phase 3: Perform (Pre-Work)"
    else:
        return "Phase 4: Recover (Sleep)"

# --- SIDEBAR ---
st.sidebar.title("⚙️ User Controls")
st.sidebar.header("Cycle Management")

# Boron Cycling Logic
boron_week = st.sidebar.selectbox("Boron Cycle Status", ["Week 1 (ON)", "Week 2 (ON)", "Week 3 (OFF)"])
boron_active = "OFF" not in boron_week

# Weekend Logic
today = datetime.now()
is_weekend = today.weekday() >= 5 # 5=Sat, 6=Sun

# Ashwagandha Logic (5 on 2 off)
# Assuming user starts Monday. Sat/Sun are off days for Ashwagandha naturally in this script if tied to weekend logic,
# but protocol says 5 on 2 off.
ash_active = not is_weekend

st.sidebar.divider()
st.sidebar.markdown("### 🛡️ Safety Checks")
st.sidebar.info("**SLUDGE Warning:** If you feel nausea, headache, or jaw tension, STOP Alpha-GPC.")
st.sidebar.info("**Hypertensive Risk:** Never mix Tyrosine (Morning) with Sabroxy (Afternoon) directly.")

# --- MAIN INTERFACE ---

st.title("🧬 Neuro-Metabolic Optimization")
st.markdown(f"**Current Status:** {today.strftime('%A, %B %d - %H:%M')}")

if is_weekend:
    st.error("⏸️ **WEEKEND WASHOUT PROTOCOL ACTIVE**")
    st.markdown("Stimulants (Caffeine, Tyrosine, Sabroxy) and Adaptogens are PAUSED to prevent receptor downregulation.")
else:
    st.success("⚡ **HIGH PERFORMANCE MODE ACTIVE**")

st.divider()

# --- DYNAMIC DASHBOARD ---

current_phase_name = get_current_phase(today)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🎯 Action Required: {current_phase_name}")
    
    # Logic to display correct dataframe
    display_df = pd.DataFrame()
    
    if is_weekend:
        display_df = pd.DataFrame(maintenance_stack)
        # Add Boron if active even on weekends? Usually specific cycle. Let's keep Boron on strict cycle.
        if boron_active:
             display_df = pd.concat([display_df, pd.DataFrame([{"Name": "Boron", "Dosage": "6-9mg", "Form": "Citrate", "Purpose": "SHBG Suppression"}])], ignore_index=True)
    else:
        # Weekday Logic
        if "Foundation" in current_phase_name:
            # Combine Phase 1 and 2
            p1 = pd.DataFrame(foundation_stack)
            p2 = pd.DataFrame(learn_stack)
            display_df = pd.concat([p1, p2], ignore_index=True)
            
            # Add Boron if active
            if boron_active:
                display_df = pd.concat([display_df, pd.DataFrame([{"Name": "Boron", "Dosage": "6-9mg", "Form": "Citrate", "Purpose": "SHBG Suppression"}])], ignore_index=True)
                
        elif "Perform" in current_phase_name:
            display_df = pd.DataFrame(perform_stack)
            
        elif "Recover" in current_phase_name:
            display_df = pd.DataFrame(recover_stack)
            if not ash_active:
                 display_df = display_df[display_df.Name != "Ashwagandha"]

    # Render Data
    if not display_df.empty:
        st.dataframe(display_df, hide_index=True, use_container_width=True)
        
        with st.expander("📝 Log Intake"):
            for index, row in display_df.iterrows():
                st.checkbox(f"Taken: {row['Name']} ({row['Dosage']})", key=row['Name'])

with col2:
    st.subheader("📊 Active Cycle Stats")
    
    # Boron Widget
    st.write(f"**Boron Status:** {'🟢 ON' if boron_active else '🔴 OFF'}")
    st.caption("Suppresses SHBG to free Testosterone.")
    
    # Ashwagandha Widget
    st.write(f"**Ashwagandha Status:** {'🟢 ON' if ash_active else '🔴 OFF'}")
    st.caption("Cortisol reduction. Cycle: 5 Days ON / 2 OFF.")

    # Weekend Washout Widget
    st.write(f"**Washout Status:** {'🟢 ACTIVE' if is_weekend else '⚪ INACTIVE'}")
    st.caption("Resensitizes Adenosine & Dopamine receptors.")

# --- COMPREHENSIVE PROTOCOL VIEW ---
st.divider()
st.header("📖 Full Protocol Reference")

tab1, tab2, tab3, tab4 = st.tabs(["Morning (Learn)", "Pre-Work (Perform)", "Night (Recover)", "Risk Management"])

with tab1:
    st.markdown("### The Cholinergic Axis")
    st.write("Focus: Acetylcholine synthesis and mitochondrial fueling.")
    st.dataframe(pd.DataFrame(foundation_stack + learn_stack), hide_index=True)
    st.info("Take 60-90 minutes post-wake on an empty stomach.")

with tab2:
    st.markdown("### The Dopaminergic Axis")
    st.write("Focus: Dopamine preservation (MAO-B inhibition) and ATP generation.")
    st.dataframe(pd.DataFrame(perform_stack), hide_index=True)
    st.warning("⚠️ **TIMING CRITICAL:** Do not take within 6 hours of sleep. Do not mix directly with L-Tyrosine.")

with tab3:
    st.markdown("### The Restoration Axis")
    st.write("Focus: GABAergic modulation, cortisol clearance, and sleep architecture.")
    st.dataframe(pd.DataFrame(recover_stack), hide_index=True)

with tab4:
    st.markdown("### ⚠️ Safety Protocols")
    st.markdown("""
    **1. Cholinergic Toxicity (SLUDGE)**
    * **Symptoms:** Salivation, watery eyes, headache, irritability.
    * **Action:** Stop Alpha-GPC and ALCAR immediately. Washout for 4 days.
    
    **2. Serotonin Syndrome**
    * **Risk:** Combining Rhodiola/Ashwagandha/Bacopa with SSRIs or MDMA.
    * **Action:** Do not use this stack if on psychiatric medication.
    
    **3. B6 Neuropathy**
    * **Check:** Ensure your B-Complex uses **P-5-P**, NOT Pyridoxine HCl.
    """)
