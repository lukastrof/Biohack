import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Neuro-Metabolic Optimizer 2.0",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING & CSS ---
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .highlight { color: #4CAF50; font-weight: bold; }
    .warning { color: #FF4B4B; font-weight: bold; }
    .metric-box {
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background-color: #1E1E1E;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'log' not in st.session_state:
    st.session_state.log = {} # Stores completed items { 'Date-ItemName': True }

# --- DATA: THE COMPREHENSIVE PROTOCOL (Section 8) ---

protocol_data = {
    "Phase 1: Foundation (Breakfast)": [
        {"Name": "Zinc", "Dosage": "15-30mg", "Form": "Picolinate/Bisglycinate", "Purpose": "Testosterone/Dopamine", "SafeWeekend": True},
        {"Name": "B-Complex", "Dosage": "1 Serving", "Form": "Must possess P-5-P & 5-MTHF", "Purpose": "Methylation Engine", "SafeWeekend": True},
        {"Name": "Tongkat Ali", "Dosage": "200-400mg", "Form": "LJ100/200:1", "Purpose": "Free T / Cortisol Control", "SafeWeekend": True}, 
        {"Name": "Boron", "Dosage": "6-9mg", "Form": "Citrate/Glycinate", "Purpose": "SHBG Suppression", "SafeWeekend": True, "SpecialLogic": "BoronCycle"},
    ],
    "Phase 2: Learn (Morning - Empty Stomach)": [
        {"Name": "Alpha-GPC", "Dosage": "300mg", "Form": "50% or 99%", "Purpose": "Choline Donor", "SafeWeekend": False},
        {"Name": "ALCAR", "Dosage": "500mg", "Form": "Acetyl-L-Carnitine", "Purpose": "Mitochondrial Fuel", "SafeWeekend": True}, 
        {"Name": "L-Tyrosine", "Dosage": "1000mg", "Form": "Free Form (Not NALT)", "Purpose": "Dopamine Fuel", "SafeWeekend": False},
        {"Name": "L-Theanine", "Dosage": "100mg", "Form": "Standardized", "Purpose": "Jitter Control", "SafeWeekend": False}, 
        {"Name": "Caffeine", "Dosage": "50-80mg", "Form": "Coffee/Matcha", "Purpose": "Adenosine Antagonist", "SafeWeekend": False},
        {"Name": "Lion's Mane", "Dosage": "1000mg", "Form": "8:1 Fruiting Body", "Purpose": "NGF Stimulation", "SafeWeekend": True}, 
        {"Name": "Creatine", "Dosage": "5g", "Form": "Monohydrate", "Purpose": "ATP Buffer", "SafeWeekend": True},
        {"Name": "Uridine", "Dosage": "250mg", "Form": "Monohydrate (UMP)", "Purpose": "Synaptogenesis", "SafeWeekend": True}, 
    ],
    "Phase 3: Perform (Pre-Work ~4:30 PM)": [
        {"Name": "Sabroxy", "Dosage": "100mg", "Form": "Oroxylum Indicum", "Purpose": "MAO-B Inhibition", "SafeWeekend": False},
        {"Name": "Cordyceps", "Dosage": "1000mg", "Form": "Militaris (Fruiting Body)", "Purpose": "ATP/Stamina", "SafeWeekend": True}, 
        {"Name": "Rhodiola", "Dosage": "300mg", "Form": "3% Rosavins", "Purpose": "Anti-Fatigue/Crash", "SafeWeekend": False},
        {"Name": "Panax Ginseng", "Dosage": "100mg", "Form": "GS15-4 Fermented", "Purpose": "Rapid Rescue Energy", "SafeWeekend": False, "Optional": True},
    ],
    "Phase 4: Recover (Post-Work ~10:00 PM)": [
        {"Name": "Magnesium", "Dosage": "2000mg", "Form": "L-Threonate (Magtein)", "Purpose": "Neuroplasticity/Sleep", "SafeWeekend": True},
        {"Name": "Apigenin", "Dosage": "50mg", "Form": "Chamomile Extract", "Purpose": "CD38 Inhibitor/GABA", "SafeWeekend": True},
        {"Name": "Phosphatidylserine", "Dosage": "400mg", "Form": "Soy-Free", "Purpose": "Cortisol Blocker", "SafeWeekend": True},
        {"Name": "Bacopa Monnieri", "Dosage": "300mg", "Form": "Synapsa/Bacognize", "Purpose": "Memory Consolidation", "SafeWeekend": False},
        {"Name": "Fish Oil", "Dosage": "2000mg", "Form": "High DHA", "Purpose": "Membrane Structure", "SafeWeekend": True},
        {"Name": "Ashwagandha", "Dosage": "300mg", "Form": "KSM-66", "Purpose": "Cortisol Crusher", "SafeWeekend": False, "SpecialLogic": "AshCycle"},
    ]
}

# --- HELPER FUNCTIONS ---

def get_current_phase_name(hour):
    if hour < 11: return "Phase 1 & 2: Foundation + Learn"
    elif 11 <= hour < 17: return "Phase 3: Perform (Pre-Work)"
    else: return "Phase 4: Recover (Sleep)"

# --- SIDEBAR: CONTROLS & LOGIC ---
st.sidebar.image("https://img.icons8.com/fluency/96/brain.png", width=60)
st.sidebar.title("User Controls")

# 1. Time Travel (For Testing)
st.sidebar.subheader("⏱️ Temporal Simulation")
use_manual_time = st.sidebar.checkbox("Override Time", value=False)
if use_manual_time:
    sim_time = st.sidebar.time_input("Set Time", value=datetime.now().time())
    sim_day = st.sidebar.selectbox("Set Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], index=datetime.now().weekday())
    
    # Map day string back to integer for logic
    days_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    current_weekday = days_map[sim_day]
    current_hour = sim_time.hour
else:
    now = datetime.now()
    current_weekday = now.weekday() # 0=Mon, 6=Sun
    current_hour = now.hour
    sim_day = now.strftime("%A")

# 2. Cycle Management
st.sidebar.divider()
st.sidebar.subheader("⚙️ Cycle Status")

# Boron Cycle (2 Weeks ON, 1 Week OFF)
boron_cycle_state = st.sidebar.radio(
    "Boron Cycle (Week)",
    ["Week 1 (ON)", "Week 2 (ON)", "Week 3 (OFF)"],
    index=0,
    help="Protocol: 2 Weeks ON, 1 Week OFF to prevent Estradiol rebound."
)
is_boron_on = "ON" in boron_cycle_state

# Logic Definitions
is_weekend = current_weekday >= 5 # Sat or Sun
is_washout = is_weekend # Weekend Washout Protocol

# Ashwagandha Logic (5 ON / 2 OFF)
is_ash_on = not is_weekend 

# --- MAIN DASHBOARD ---

st.title("🧬 Neuro-Metabolic Optimizer")
st.markdown(f"**Status:** {sim_day} | {current_hour}:00")

# Status Banners
if is_washout:
    st.error("🚫 **WEEKEND WASHOUT PROTOCOL ACTIVE**")
    st.caption("Stimulants and Adaptogens are PAUSED to resensitize receptors. Maintenance stack only.")
else:
    st.success("⚡ **HIGH PERFORMANCE MODE ACTIVE**")
    st.caption("Cholinergic & Dopaminergic systems are fully operational.")

st.divider()

# --- METRICS ROW ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Boron Status", "ON" if is_boron_on else "OFF", delta="SHBG Suppression" if is_boron_on else "Estrogen Reset", delta_color="normal")
with c2:
    st.metric("Cortisol Shield", "ON" if is_ash_on else "OFF", delta="Ashwagandha" if is_ash_on else "Receptor Reset", delta_color="normal")
with c3:
    st.metric("Current Phase", get_current_phase_name(current_hour).split(":")[0])
with c4:
    st.metric("Washout", "ACTIVE" if is_weekend else "INACTIVE", delta_color="inverse")

# --- MAIN FEED (DYNAMIC) ---

st.subheader(f"🎯 Required Action: {get_current_phase_name(current_hour)}")

# Determine which phases to show based on time
active_phases = []
if current_hour < 11:
    active_phases = ["Phase 1: Foundation (Breakfast)", "Phase 2: Learn (Morning - Empty Stomach)"]
elif 11 <= current_hour < 18:
    active_phases = ["Phase 3: Perform (Pre-Work ~4:30 PM)"]
else:
    active_phases = ["Phase 4: Recover (Post-Work ~10:00 PM)"]

# Render the Lists
for phase_title in active_phases:
    with st.container():
        st.markdown(f"#### {phase_title}")
        
        # Safety Warnings Contextual
        if "Perform" in phase_title and not is_weekend:
            st.warning("⚠️ **SAFETY CHECK:** Ensure 6-8 hours have passed since taking L-Tyrosine before taking Sabroxy.")
        if "Learn" in phase_title:
             st.info("ℹ️ **SLUDGE WATCH:** If you feel jaw tension or headache, skip Alpha-GPC.")
        
        items = protocol_data[phase_title]
        
        # Create a clean table for the phase
        phase_data = []
        
        for item in items:
            # --- FILTERING LOGIC ---
            # 1. Weekend Washout Filter
            if is_weekend and not item.get("SafeWeekend", False):
                continue 
            
            # 2. Boron Specific Logic
            if item.get("SpecialLogic") == "BoronCycle" and not is_boron_on:
                continue 
            
            # 3. Ashwagandha Specific Logic
            if item.get("SpecialLogic") == "AshCycle" and not is_ash_on:
                continue 
                
            phase_data.append(item)
        
        if not phase_data:
            st.info("Nothing to take in this phase during Washout/Cycle Off.")
        else:
            # Custom rendering for checkboxes
            for p_item in phase_data:
                key = f"{datetime.now().strftime('%Y-%m-%d')}-{p_item['Name']}"
                
                col_check, col_details = st.columns([1, 6])
                
                with col_check:
                    is_checked = st.checkbox("Done", key=key)
                
                with col_details:
                    st.markdown(f"**{p_item['Name']}** ({p_item['Dosage']})")
                    st.caption(f"*{p_item['Form']}* — {p_item['Purpose']}")
                    if p_item.get("Optional"):
                        st.markdown("tags: `OPTIONAL`")

st.divider()

# --- REFERENCE TABS ---
st.header("📖 Full Protocol Reference")
tab1, tab2, tab3, tab4 = st.tabs(["Morning", "Afternoon", "Night", "Safety & Risks"])

with tab1:
    st.markdown("### The Cholinergic Axis")
    st.dataframe(pd.DataFrame(protocol_data["Phase 1: Foundation (Breakfast)"] + protocol_data["Phase 2: Learn (Morning - Empty Stomach)"]), use_container_width=True)

with tab2:
    st.markdown("### The Dopaminergic Axis")
    st.dataframe(pd.DataFrame(protocol_data["Phase 3: Perform (Pre-Work ~4:30 PM)"]), use_container_width=True)

with tab3:
    st.markdown("### The Restoration Axis")
    st.dataframe(pd.DataFrame(protocol_data["Phase 4: Recover (Post-Work ~10:00 PM)"]), use_container_width=True)

with tab4:
    st.error("### ☣️ Critical Interactions")
    st.markdown("""
    **1. Tyrosine + Sabroxy (Hypertensive Risk)**
    * **Mechanism:** Tyrosine increases Dopamine synthesis. Sabroxy prevents breakdown.
    * **Risk:** Taking them together can spike blood pressure.
    * **Rule:** Always separate by at least 4-6 hours.
    """)
