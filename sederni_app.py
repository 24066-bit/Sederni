import streamlit as st
import json
import random

st.set_page_config(
    page_title="Sederni — Guide IA de Nouakchott",
    page_icon="🌍",
    layout="centered"
)

# ─── CSS personnalisé ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        color: #f0c040;
        font-size: 3rem;
        margin: 0;
        font-family: 'Tajawal', sans-serif;
    }
    .hero p {
        color: #a0aec0;
        font-size: 1rem;
        margin: 0.5rem 0 0;
    }
    .result-box {
        background: #f8f9fa;
        border-left: 4px solid #f0c040;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
    }
    .hassaniya-box {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .hassaniya-box .label {
        color: #a0aec0;
        font-size: 0.85rem;
        margin-bottom: 0.3rem;
    }
    .hassaniya-box .word {
        color: #f0c040;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .hassaniya-box .translation {
        color: #e2e8f0;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }
    .suggestion-pill {
        display: inline-block;
        background: #edf2f7;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.85rem;
        color: #2d3748;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    .note-culturelle {
        background: #fffbeb;
        border-left: 3px solid #f6ad55;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        color: #744210;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #edf2f7;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #1a1a2e !important;
        color: #f0c040 !important;
    }
    .expr-du-jour {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin-top: 1rem;
    }
    .expr-du-jour .fr { color: #a0aec0; font-size: 1rem; }
    .expr-du-jour .hass { color: #f0c040; font-size: 2.5rem; font-weight: 700; }
    .expr-du-jour .expl { color: #e2e8f0; font-size: 0.9rem; margin-top: 0.5rem; }
    
    div[data-testid="stButton"] button {
        border-radius: 20px !important;
        font-size: 0.82rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Chargement des données ───
@st.cache_data
def load_data():
    with open("SEDERNI_DATASET_FINAL_COMPLET.json", "r", encoding="utf-8") as f:
        guide_data = json.load(f)
    hassaniya_files = [
        "hassaniya_salutations.json", "hassaniya_restaurant.json",
        "hassaniya_transport.json", "hassaniya_shopping.json",
        "hassaniya_urgences.json", "hassaniya_culture.json",
        "hassaniya_logement.json", "hassaniya_tourisme.json",
        "hassaniya_chiffres.json", "hassaniya_meteo.json",
    ]
    hassaniya_data = []
    for f in hassaniya_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                hassaniya_data.extend(json.load(fp))
        except:
            pass
    return guide_data, hassaniya_data

guide_data, hassaniya_data = load_data()

# ─── Fonctions de recherche ───
def chercher_guide(question):
    question = question.lower()
    meilleur, meilleur_score = None, 0
    for item in guide_data:
        score = sum(1 for mot in question.split() if mot in item["instruction"].lower())
        if score > meilleur_score:
            meilleur_score = score
            meilleur = item
    return meilleur if meilleur_score > 0 else None

def chercher_hassaniya(question):
    question = question.lower()
    meilleur, meilleur_score = None, 0
    for item in hassaniya_data:
        score = sum(1 for mot in question.split()
                   if mot in item["input"].lower()
                   or mot in item.get("français","").lower())
        if score > meilleur_score:
            meilleur_score = score
            meilleur = item
    return meilleur if meilleur_score > 0 else None

# ─── HERO ───
st.markdown("""
<div class="hero">
    <h1>🌍 Sederni — سدرني</h1>
    <p>Guide touristique IA de Nouakchott · Apprendre le Hassaniya mauritanien</p>
</div>
""", unsafe_allow_html=True)

# ─── ONGLETS ───
tab1, tab2 = st.tabs(["🗺️  Guide Touristique", "🗣️  Apprendre le Hassaniya"])

# ════════════════════════════════
# ONGLET 1 — GUIDE TOURISTIQUE
# ════════════════════════════════
with tab1:
    st.markdown("### Pose ta question sur Nouakchott")

    suggestions = [
        "Meilleurs restaurants ?",
        "Quartier le plus chic ?",
        "Comment se déplacer ?",
        "Où aller à la plage ?",
        "Hôtels avec spa ?",
        "Y a-t-il un zoo ?",
    ]

    cols = st.columns(3)
    for i, sug in enumerate(suggestions):
        if cols[i % 3].button(sug, key=f"sug_{i}"):
            st.session_state["guide_question"] = sug

    question_guide = st.text_input(
        "",
        value=st.session_state.get("guide_question", ""),
        placeholder="✍️  Ex : Où manger un bon thiéboudienne ?",
        key="input_guide"
    )

    if question_guide:
        resultat = chercher_guide(question_guide)
        if resultat:
            st.markdown(f"""
            <div class="result-box">
                <strong>{resultat['instruction']}</strong><br><br>
                {resultat['output'].replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            hass = chercher_hassaniya(question_guide)
            if hass:
                st.markdown(f"""
                <div class="hassaniya-box">
                    <div class="label">🗣️ En Hassaniya</div>
                    <div class="word">{hass.get('hassaniya', '')}</div>
                    <div class="translation">{hass.get('français', '')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Je n'ai pas trouvé de réponse. Essaie une autre formulation !")

# ════════════════════════════════
# ONGLET 2 — HASSANIYA
# ════════════════════════════════
with tab2:
    st.markdown("### Apprends le Hassaniya mauritanien")
    st.caption("Transcription en alphabet latin — accessible à tous les touristes 🌍")

    col1, col2 = st.columns([1, 2])
    with col1:
        categories = sorted(set(
            item.get("categorie", "") for item in hassaniya_data
            if item.get("categorie", "")
        ))
        categorie = st.selectbox("Catégorie", ["Toutes"] + categories)
    with col2:
        recherche = st.text_input("", placeholder="🔍  Recherche : bonjour, taxi, prix...")

    # Filtrage
    filtres = hassaniya_data if categorie == "Toutes" else [
        d for d in hassaniya_data if d.get("categorie") == categorie
    ]
    if recherche:
        filtres = [d for d in filtres if
            recherche.lower() in d["input"].lower() or
            recherche.lower() in d.get("français","").lower() or
            recherche.lower() in d.get("hassaniya","").lower()
        ]

    st.markdown(f"**{len(filtres)} expressions trouvées**")

    for item in filtres[:15]:
        with st.expander(f"🇫🇷  {item.get('français', item['input'][:50])}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🇫🇷 Français**")
                st.write(item.get("français", "—"))
            with c2:
                st.markdown("**🌍 Hassaniya**")
                st.markdown(f"### {item.get('hassaniya', '—')}")
            st.markdown("**Explication**")
            st.write(item["output"])
            if item.get("note_culturelle"):
                st.markdown(f"""
                <div class="note-culturelle">
                    💡 {item['note_culturelle']}
                </div>
                """, unsafe_allow_html=True)

    # Expression du jour
    st.markdown("---")
    col_titre, col_btn = st.columns([3, 1])
    with col_titre:
        st.markdown("### ✨ Expression du jour")
    with col_btn:
        if st.button("🎲 Nouvelle"):
            st.session_state["expression_jour"] = random.choice(hassaniya_data)

    expr = st.session_state.get("expression_jour", random.choice(hassaniya_data))
    st.markdown(f"""
    <div class="expr-du-jour">
        <div class="fr">{expr.get('français', '')}</div>
        <div class="hass">{expr.get('hassaniya', '')}</div>
        <div class="expl">{expr['output'][:120]}...</div>
    </div>
    """, unsafe_allow_html=True)
