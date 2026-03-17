import streamlit as st
import openai

# --- SECURITY: QARINTA API KEY-GA ---
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    api_key = ""

def mishiinka_sirdoonka_mujaahid(category, selection):
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    
    system_prompt = """
    Waxaad tahay 'Sirdoonka Mujaahidka ah'. 
    1. Aragtidaadu: Difaaca Diinta, Midnimada dalka, iyo kashifidda khayaanada DFS iyo gumeysiga cusub.
    2. Dadka & Dalka: Sharax gobol kasta, beelaha dega, iyo sababta ay shisheeyuhu u degeen aalkaas.
    3. Isbarbardhig: Muuji farqiga u dhexeeya maamulada dilaaliinta ah (DFS/Goonigoosad) iyo kuwa xornimada raba.
    """

    user_prompt = f"Baaritaan qoto dheer ku samee {category}: {selection}. Kashif xogta qarsoon iyo khayaanada dalka lagu hayo."

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
st.set_page_config(page_title="Indhaha Shacabka 🇸🇴", layout="wide")

st.title("🇸🇴 Indhaha Shacabka: Mishiinka Xaqiiqada (v7 Master)")

# USER GUIDE
with st.expander("📖 HAGAHAA ISTICMAALKA (User Guide)"):
    st.markdown("""
    * **Maamulka:** Baro siday DFS iyo kuwa kale u fududeeyaan boobka.
    * **Ciidanka & Saldhigyada:** Kashif meelaha shisheeyuhu ku dhuumaalaystaan.
    * **Dalka & Dadka:** Baro juqraafiga beelaha iyo siday shisheeyuhu u kala qaybiyaan.
    * **Kheyraadka:** Baro hantida qaranka ee la rabo in la dhaco.
    """)

# --- 6-DA DROPDOWN EE SIRDOONKA (SIDEBAR) ---
st.sidebar.header("🔍 Baaritaanka Sirdoonka")

# 1. Maamulada
maamul = st.sidebar.selectbox("🏛️ Maamulka:", ["DFS (Muqdisho)", "Al-Shabaab", "Somaliland (Goonigoosad)", "Puntland"])

# 2. Ciidamada Shisheeye
ciidan = st.sidebar.selectbox("🪖 Ciidanka Shisheeye:", ["ATMIS (Uganda/Burundi)", "Itoobiya (ENDF)", "Kenya (KDF)", "US Special Ops", "Turksom"])

# 3. Saldhigyada Shisheeye
saldhig = st.sidebar.selectbox("🛰️ Saldhigga:", ["Ballidogle (US)", "Berbera (UAE)", "Kismaayo (Kenya)", "Bosaaso (UAE/PMPF)"])

# 4. Dalka & Dadka (Dib-u-habayn lagu sameeyey)
juqraafi = st.sidebar.selectbox("🌍 Dalka & Dadka (Gobolada):", [
    "Waqooyiga (Awdal, Maroodi-jeex, Togdheer, Sanaag, Sool)",
    "Bari & Woqooyi-Bari (Bari, Nugaal, Mudug)",
    "Bartamaha (Galgaduud, Hiiraan)",
    "Koonfurta (Shabeellaha Hoose/Dhexe, Bay, Bakool)",
    "Koonfur-Galbeed/Jubbooyinka (Gedo, Jubbada Hoose/Dhexe)"
])

# 5. Kheyraadka Qaranka
kheyraad = st.sidebar.selectbox("💎 Kheyraadka:", ["Uranium-ka Mudug", "Dahabka & Macdanta Sanaag", "Shidaalka Offshore (Badda)", "Beeraha & Webiyada"])

# 6. Isbarbardhigga Xaqiiqada
isbarbardhig = st.sidebar.selectbox("⚖️ Isbarbardhig:", ["DFS vs Mujaahidiinta", "Gumeysi vs Xornimo"])

# --- QAYBTA BANDHIGGA ---
selection_map = {
    "Maamulka": maamul, "Ciidanka Shisheeye": ciidan, "Saldhigga": saldhig,
    "Dalka & Dadka": juqraafi, "Kheyraadka": kheyraad, "Isbarbardhigga": isbarbardhig
}

target = st.radio("Dooro mowduuca aad hadda falanqeynayso:", list(selection_map.keys()), horizontal=True)

if st.button("BILOW BAARITAANKA SIRDOONKA"):
    sel = selection_map[target]
    with st.spinner(f"AI-du waxay baaraysaa xogta qarsoon ee {sel}..."):
        report = mishiinka_sirdoonka_mujaahid(target, sel)
        st.error(report)

# COMPARISON TABLE
st.write("---")
st.subheader("⚖️ Shaxda Xaqiiqada (Quick Insight)")
st.table({
    "Qodobka": ["Hadafka", "Xiriirka Shisheeye", "Illaalinta Khayraadka", "Diinta"],
    "DFS / Maamulada": ["Dilaalnimo", "Adeegayaal", "Boob-Fududeeye", "Daciif/Wada-shaqeeye"],
    "Mujaahidiinta": ["Xornimo Dhab ah", "Cadow", "Illaaliye", "Difaace/Xukun"]
})