import streamlit as st
import openai

# --- CONFIGURATION & GREEN THEME ---
st.set_page_config(page_title="Indhaha Shacabka 🇸🇴", layout="wide")

# CSS si loogu beddelo muuqaalka mid sirdoon oo cagaar ah
st.markdown("""
    <style>
    /* Midabka guud ee bogga */
    .stApp {
        background-color: #050505;
    }
    /* Sanduuqa xogta sirdoonka */
    .report-box {
        color: #00FF00;
        background-color: #000000;
        padding: 25px;
        border-radius: 5px;
        border: 2px solid #00FF00;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 0 15px #00FF00;
        line-height: 1.6;
    }
    /* Badanka Execute */
    .stButton>button {
        background-color: #00FF00 !important;
        color: black !important;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    /* Qoraalka dropdown-ka */
    .stSelectbox label, .stRadio label {
        color: #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKSHANKA CODKA (SONAR BEEP) ---
def play_sonar():
    # Cod sirdoon oo kooban oo dhacaya marka xogta la keeno
    audio_html = """
        <audio autoplay>
        <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# --- SECURITY: API KEY ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    api_key = ""

def mishiinka_sirdoonka_mujaahid(category, selection):
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    # SYSTEM PROMPT: Tactical & Aggressive Intel
    system_prompt = """
    Waxaad tahay 'Sirdoonka Mujaahidka ah'. 
    Nidaamkaagu maaha sheeko iyo hadal robot. 
    1. Si toos ah u sheeg 'Muhiimadda Istaraatiijiga ah' ee goobtan/shaygan.
    2. Kashif 'Khayaanada Qarsoon' ee u dhexaysa DFS iyo Shisheeyaha.
    3. Ha u hadlin sidii robot, u hadal sidii sarkaal sirdoon oo xog culus dhex jooga.
    4. Xogtaadu ha noqoto mid midho-dhal ah (Actionable Intel).
    """

    user_prompt = f"TARGET: {selection} ({category}). Baaritaan Sirdoon: Kashif muhiimadda iyo khayaanada."

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-001",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

# --- INTERFACE-KA MASTER CONTROL ---
st.title("🇸🇴 SIRDOONKA QARANKA: INDHAHA SHACABKA")

# --- 6-DA DROPDOWN EE SIRDOONKA (SIDEBAR) ---
st.sidebar.header("🔍 INTELLIGENCE FEED")
maamul = st.sidebar.selectbox("🏛️ Maamulka:", ["DFS (Muqdisho)", "Al-Shabaab", "Somaliland (Goonigoosad)", "Puntland"])
ciidan = st.sidebar.selectbox("🪖 Ciidanka Shisheeye:", ["ATMIS (Uganda/Burundi)", "Itoobiya (ENDF)", "Kenya (KDF)", "US Special Ops", "Turksom"])
saldhig = st.sidebar.selectbox("🛰️ Saldhigga:", ["Ballidogle (US)", "Berbera (UAE)", "Kismaayo (Kenya)", "Bosaaso (UAE/PMPF)"])
juqraafi = st.sidebar.selectbox("🌍 Dalka & Dadka (Gobolada):", [
    "Waqooyiga (Awdal, Maroodi-jeex, Togdheer, Sanaag, Sool)",
    "Bari & Woqooyi-Bari (Bari, Nugaal, Mudug)",
    "Bartamaha (Galgaduud, Hiiraan)",
    "Koonfurta (Shabeellaha Hoose/Dhexe, Bay, Bakool)",
    "Koonfur-Galbeed/Jubbooyinka (Gedo, Jubbada Hoose/Dhexe)"
])
kheyraad = st.sidebar.selectbox("💎 Kheyraadka:", ["Uranium-ka Mudug", "Dahabka & Macdanta Sanaag", "Shidaalka Offshore (Badda)", "Beeraha & Webiyada"])
isbarbardhig = st.sidebar.selectbox("⚖️ Isbarbardhig:", ["DFS vs Mujaahidiinta", "Gumeysi vs Xornimo"])

# --- QAYBTA BANDHIGGA ---
selection_map = {
    "Maamulka": maamul, "Ciidanka Shisheeye": ciidan, "Saldhigga": saldhig,
    "Dalka & Dadka": juqraafi, "Kheyraadka": kheyraad, "Isbarbardhigga": isbarbardhig
}

target = st.radio("SELECT TARGET FOR ANALYSIS:", list(selection_map.keys()), horizontal=True)

if st.button("EXECUTE INTELLIGENCE SCAN"):
    sel = selection_map[target]
    with st.spinner(f"Decoding secret signals for {sel}..."):
        report = mishiinka_sirdoonka_mujaahid(target, sel)
        play_sonar() # Codka beep-ka
        st.markdown(f"""
            <div class="report-box">
            <h2 style="color: #00FF00; border-bottom: 1px solid #00FF00;">🚩 TOP SECRET REPORT: {sel}</h2>
            <p>{report}</p>
            </div>
        """, unsafe_allow_html=True)

# COMPARISON TABLE
st.write("---")
st.subheader("⚖️ STATUS: OPERATIONAL VERDICT")
st.table({
    "Qodobka": ["Hadafka", "Xiriirka Shisheeye", "Illaalinta Khayraadka", "Diinta"],
    "DFS / Maamulada": ["Dilaalnimo", "Adeegayaal", "Boob-Fududeeye", "Daciif/Wada-shaqeeye"],
    "Mujaahidiinta": ["Xornimo Dhab ah", "Cadow", "Illaaliye", "Difaace/Xukun"]
})
