import streamlit as st
import json
import base64

st.set_page_config(layout="wide")

# Load docs
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

/* ---- EXTRA GAP BETWEEN PLATFORM HEADER AND FIRST EXPANDER ---- */
.platform-header-spacer{
    height:18px; /* creates a clear visual gap */
}

/* Also ensure expanders have a small top margin globally */
.stExpander{
    margin-top:6px;
}

/* ---------------- SECTION TITLES ---------------- */
.section{
    font-size:20px;
    font-weight:700;
    margin-top:20px;
    margin-bottom:8px;
    color:#1f2937;
}

/* ---------------- TILES (smaller) ---------------- */
.tile{
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,#9fcdf0 0%, #b9bdf7 100%);
    border-radius:12px;

    /* smaller tile */
    padding:8px;              /* was 12px */
    margin-bottom:12px;
    font-size:11px;           /* was 12px */
    font-weight:600;
    text-align:center;
    color:#000000;
    transition:all .30s ease;
    box-shadow:0 6px 14px rgba(80,140,200,0.20);
    border:1px solid rgba(255,255,255,0.22);
    min-height:56px;          /* was 68px */
}

/* soft directional flow overlay */
.tile::before{
    content:"";
    position:absolute;
    inset:auto -40px -40px auto;
    width:110px;
    height:110px;
    background:radial-gradient(circle, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.0) 70%);
    transform:rotate(-18deg);
}

/* diagonal arrow hint (slightly smaller) */
.tile::after{
    content:"➜";
    position:absolute;
    right:12px;
    top:8px;                  /* slight nudge to balance reduced height */
    font-size:16px;           /* was 18px */
    color:rgba(255,255,255,0.45);
    font-weight:700;
    transition:all .30s ease;
}

.tile:hover{
    transform:translateY(-5px) scale(1.03);
    background:linear-gradient(135deg,#a9d4f3 0%, #c5c8fa 100%);
    box-shadow:
        0 14px 26px rgba(80,140,200,0.28),
        0 0 18px rgba(150,150,240,0.22);
    border:1px solid rgba(255,255,255,0.35);
    cursor:pointer;
}
.tile:hover::after{
    transform:translateX(4px) scale(1.06);
    color:rgba(255,255,255,0.80);
}

/* clickable area */
.tile a{
    text-decoration:none;
    color:#000000;
    display:block;
    width:100%;
    height:100%;
}

/* tile internal layout (tighter) */
.tile-inner{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    min-height:36px;          /* was 44px */
    position:relative;
    z-index:2;
    padding:4px 0;            /* was 6px 0 */
}

/* document title */
.tile-title{
    width:100%;
    text-align:center;
    line-height:1.28;         /* slightly tighter */
    padding:0 30px 0 30px;    /* a bit less to reflect smaller chips */
    word-break:break-word;
    overflow-wrap:break-word;
}

/* subtle Fabric destination chip (smaller) */
.fabric-chip{
    position:absolute;
    right:8px;
    bottom:8px;
    width:16px;               /* was 18px */
    height:16px;              /* was 18px */
    border-radius:50%;
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.24);
    padding:2px;              /* was 3px */
    box-shadow:0 3px 8px rgba(0,0,0,0.10);
    backdrop-filter:blur(4px);
    transition:all .30s ease;
    z-index:3;
    pointer-events:none;
}
.tile:hover .fabric-chip{
    transform:scale(1.08);
    box-shadow:0 0 12px rgba(255,255,255,0.22);
}

/* source platform mini badge (smaller) */
.source-chip{
    position:absolute;
    left:8px;
    top:8px;
    width:16px;               /* was 18px */
    height:16px;              /* was 18px */
    border-radius:50%;
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.24);
    padding:2px;              /* was 3px */
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
    backdrop-filter:blur(4px);
    z-index:3;
    pointer-events:none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.image("assets/hexaware.png", width=80)

with col2:
    st.markdown(
        f'''
        <div class="title-wrap">
            <img class="title-logo" src="data:image/png;base64,{fabric_logo}">
            <div class="title">Fabric Migration Explorer</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# ---------------- PLATFORM HEADER (NOT IN WHITE BOX) ----------------
st.markdown('<div class="platform-header"></div>', unsafe_allow_html=True)
header_cols = st.columns(len(platforms))
for i, p in enumerate(platforms):
    with header_cols[i]:
        st.markdown(
            f'''
            <div class="cloud-wrap">
                <img src="data:image/png;base64,{logo_base64.get(p, '')}" width="26">
                <div class="cloud-label">{p}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )

# Spacer to create a distinct gap between platform row and first expander
st.markdown('<div class="platform-header-spacer"></div>', unsafe_allow_html=True)

# ---------------- SECTIONS WITH ARROW (EXPAND/COLLAPSE) ----------------
# 1) STORAGE
with st.expander("STORAGE 📦", expanded=False):
    cols = st.columns(len(platforms))
    for i, p in enumerate(platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("Storage", {}).items():
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

# 2) ETL
with st.expander("ETL ⚙", expanded=False):
    cols = st.columns(len(platforms))
    for i, p in enumerate(platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("ETL", {}).items():
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

# 3) REPORTING
with st.expander("REPORTING 📊", expanded=False):
    cols = st.columns(len(platforms))
    for i, p in enumerate(platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("Reporting", {}).items():
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