import streamlit as st
import openai

# --- SECURITY: QARINTA API KEY-GA ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    api_key = ""

# --- CACHING LOGIC: Si uu app-ku u noqdo mid aad u dheereeya ---
@st.cache_data(show_spinner=False, ttl=3600)
def mishiinka_sirdoonka_researcher(category, selection):
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    system_prompt = """
    Waxaad tahay 'Researcher Sirdoon' oo xeel dheer. 
    1. Adeegso af-Soomaali suuban oo miisaan leh (Elite Research Style).
    2. Kashif khayaanada DFS iyo maamulada goonigoosadka ah.
    3. Sharax siday Mujaahidiintu u yihiin xoogga difaacaya dalka iyo Shareecada.
    4. Isku xir kheyraadka dalka iyo damaca shisheeyaha ee saldhigyada ku dhuumanaya.
    """

    user_prompt = f"TARGET: {selection} ({category}). Falanqayn cilmi-baaris sirdoon oo qoto dheer."

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-001",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

# --- INTERFACE-KA MASTER CONTROL (SIDOODII) ---
st.set_page_config(page_title="Indhaha Shacabka 🇸🇴", layout="wide")

# CSS: Midabka Cagaarka Matrix-ka
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .report-box {
        color: #00FF00;
        background-color: #000000;
        padding: 25px;
        border: 2px solid #00FF00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #00FF00 !important;
        color: black !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇸🇴 Indhaha Shacabka: Mishiinka Xaqiiqada (v7 Master)")

# USER GUIDE
with st.expander("📖 HAGAHAA ISTICMAALKA (User Guide)"):
    st.markdown("""
    * **Maamulka:** Baro siday DFS iyo kuwa kale u fududeeyaan boobka.
    * **Ciidanka & Saldhigyada:** Kashif meelaha shisheeyuhu ku dhuumaalaystaan.
    * **Dalka & Dadka:** Baro juqraafiga beelaha iyo siday shisheeyuhu u kala qaybiyaan.
    * **Kheyraadka:** Baro hantida qaranka ee la rabo in la dhaco.
    """)

# --- 6-DA DROPDOWN EE SIRDOONKA (SIDOODII) ---
st.sidebar.header("🔍 Baaritaanka Sirdoonka")

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

target = st.radio("Dooro mowduuca aad hadda falanqeynayso:", list(selection_map.keys()), horizontal=True)

if st.button("BILOW BAARITAANKA SIRDOONKA"):
    sel = selection_map[target]
    with st.spinner(f"Researcher-ku wuxuu diyaarinayaa falanqaynta {sel}..."):
        report = mishiinka_sirdoonka_researcher(target, sel)
        st.markdown(f'<div class="report-box">### 🚩 XOGTA SIRDOONKA: {sel}\n\n{report}</div>', unsafe_allow_html=True)

# COMPARISON TABLE
st.write("---")
st.subheader("⚖️ Shaxda Xaqiiqada (Quick Insight)")
st.table({
    "Qodobka": ["Hadafka", "Xiriirka Shisheeye", "Illaalinta Khayraadka", "Diinta"],
    "DFS / Maamulada": ["Dilaalnimo", "Adeegayaal", "Boob-Fududeeye", "Daciif/Wada-shaqeeye"],
    "Mujaahidiinta": ["Xornimo Dhab ah", "Cadow", "Illaaliye", "Difaace/Xukun"]
})
