import streamlit as st
import json
import base64

st.set_page_config(layout="wide")

# ---------------- LOAD DOCS ----------------
with open("data/docs.json", encoding="utf-8") as f:
    docs = json.load(f)

platforms = list(docs.keys())

logos = {
    "Azure": "assets/azure.png",
    "Databricks": "assets/databricks.png",
    "Snowflake": "assets/snowflake.png",
    "Google Cloud": "assets/gcp.png",
    "AWS": "assets/aws.png"
}

# ---------------- IMAGE HELPER ----------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

azure_logo = img_to_base64("assets/azure.png")
databricks_logo = img_to_base64("assets/databricks.png")
snowflake_logo = img_to_base64("assets/snowflake.png")
gcp_logo = img_to_base64("assets/gcp.png")
aws_logo = img_to_base64("assets/aws.png")
fabric_logo = img_to_base64("assets/fabric.png")
hexaware_logo = "assets/hexaware.png"

logo_base64 = {
    "Azure": azure_logo,
    "Databricks": databricks_logo,
    "Snowflake": snowflake_logo,
    "Google Cloud": gcp_logo,
    "AWS": aws_logo
}

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp{
    background:linear-gradient(180deg,#edf3f9,#dde8f5);
    font-family:Segoe UI;
}

/* ---------------- HEADER ---------------- */
.title{
    font-size:34px;
    font-weight:700;
    color:#1f2937;
    text-align:center;
    margin:0;
    line-height:1;
}
.title-wrap{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:8px;
}
.title-logo{
    width:34px;
    height:34px;
    object-fit:contain;
    display:block;
}

/* ---------------- PLATFORM HEADER ROW ---------------- */
.platform-header{
    margin-top:10px;
    margin-bottom:6px;
}
.cloud-wrap{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
    width:100%;
}
.cloud-label{
    font-size:16px;
    font-weight:700;
    color:#1f2937;
    white-space:nowrap;
    margin-top:2px;
}

/* ---- WHITE CARD FOR EACH HYPERSCALER (main header area) ---- */
.platform-card{
    background:#ffffff;
    border-radius:14px;
    padding:14px 12px;
    border:1px solid rgba(0,0,0,0.08);
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
    height:100%;
}

/* ---- EXTRA GAP BETWEEN PLATFORM HEADER AND FIRST EXPANDER ---- */
.platform-header-spacer{
    height:18px;
}

/* Also ensure expanders have a small top margin globally */
.stExpander{
    margin-top:6px;
}

/* ---------------- TILES ---------------- */
.tile{
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,#9fcdf0 0%, #b9bdf7 100%);
    border-radius:12px;
    padding:8px;
    margin-bottom:12px;
    font-size:11px;
    font-weight:600;
    text-align:center;
    color:#000000;
    transition:all .30s ease;
    box-shadow:0 6px 14px rgba(80,140,200,0.20);
    border:1px solid rgba(255,255,255,0.22);
    min-height:56px;
}

.tile::after{
    content:"➜";
    position:absolute;
    right:12px;
    top:8px;
    font-size:16px;
    color:rgba(255,255,255,0.45);
    font-weight:700;
}

.tile:hover{
    transform:translateY(-5px) scale(1.03);
}

.tile a{
    text-decoration:none;
    color:#000000;
    display:block;
    width:100%;
    height:100%;
}

.tile-inner{
    display:flex;
    align-items:center;
    justify-content:center;
    min-height:36px;
}

.tile-title{
    padding:0 30px;
}

/* chips */
.fabric-chip{
    position:absolute;
    right:8px;
    bottom:8px;
    width:16px;
    height:16px;
}
.source-chip{
    position:absolute;
    left:8px;
    top:8px;
    width:16px;
    height:16px;
}

/* ---------------- EXPANDER CARET (unchanged) ---------------- */
.stExpander > details > summary [data-testid="stIconMaterial"]{
  display:none !important;
}
.stExpander > details > summary{
  list-style:none;
  position:relative;
  padding-left:18px;
}
.stExpander > details > summary::before{
  content:"▸";
  position:absolute;
  left:0;
  top:0.1rem;
  font-weight:700;
}
.stExpander > details[open] > summary::before{
  content:"▾";
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.image(hexaware_logo, width=80)

with col2:
    st.markdown(
        f"""
        <div class="title-wrap">
            <img class="title-logo" src="data:image/png;base64,{fabric_logo}">
            <div class="title">Fabric Migration Explorer</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- FILTER (TEXT ONLY, NO ARROW) ----------------
with col3:
    selected = st.selectbox(
        "Hyperscaler",
        ["All"] + platforms,
        index=0,
        key="flt",
        label_visibility="visible"
    )

# Compute filtered list
filtered_platforms = platforms if selected == "All" else [selected]

# ---------------- PLATFORM HEADER ----------------
st.markdown('<div class="platform-header"></div>', unsafe_allow_html=True)
cols = st.columns(len(filtered_platforms))
for i, p in enumerate(filtered_platforms):
    with cols[i]:
        st.markdown(
            f"""
            <div class="platform-card">
                <div class="cloud-wrap">
                    <img src="data:image/png;base64,{logo_base64[p]}" width="26">
                    <div class="cloud-label">{p}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('<div class="platform-header-spacer"></div>', unsafe_allow_html=True)

# ---------------- TILE RENDER ----------------
def render_tile(name, link, src_logo):
    name = name.replace("à†’", "→")
    st.markdown(
        f"""
        <div class="tile">
            <a href="{link}" target="_blank">
                <img class="source-chip" src="data:image/png;base64,{src_logo}">
                <div class="tile-inner">
                    <div class="tile-title">{name}</div>
                </div>
                <img class="fabric-chip" src="data:image/png;base64,{fabric_logo}">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- SECTIONS ----------------
with st.expander("STORAGE 📦"):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            for n, l in docs[p].get("Storage", {}).items():
                render_tile(n, l, logo_base64[p])

with st.expander("ETL ⚙"):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            for n, l in docs[p].get("ETL", {}).items():
                render_tile(n, l, logo_base64[p])

with st.expander("REPORTING 📊"):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            for n, l in docs[p].get("Reporting", {}).items():
                render_tile(n, l, logo_base64[p])