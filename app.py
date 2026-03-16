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

/* ---------------- TILES (smaller + softer) ---------------- */
.tile{
    position:relative;
    overflow:hidden;
    background:linear-gradient(135deg,#9fcdf0 0%, #b9bdf7 100%);
    border-radius:12px;

    /* compact tile */
    padding:8px;
    margin-bottom:12px;
    font-size:11px;
    font-weight:600;
    text-align:center;
    color:#000000; /* black text */
    transition:all .30s ease;
    box-shadow:0 6px 14px rgba(80,140,200,0.20);
    border:1px solid rgba(255,255,255,0.22);
    min-height:56px;
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
    top:8px;
    font-size:16px;
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
    color:#000000; /* black text inside link */
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
    min-height:36px;
    position:relative;
    z-index:2;
    padding:4px 0;
}

/* document title */
.tile-title{
    width:100%;
    text-align:center;
    line-height:1.28;
    padding:0 30px 0 30px; /* to account for chips */
    word-break:break-word;
    overflow-wrap:break-word;
}

/* subtle Fabric destination chip (smaller) */
.fabric-chip{
    position:absolute;
    right:8px;
    bottom:8px;
    width:16px;
    height:16px;
    border-radius:50%;
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.24);
    padding:2px;
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
    width:16px;
    height:16px;
    border-radius:50%;
    background:rgba(255,255,255,0.14);
    border:1px solid rgba(255,255,255,0.24);
    padding:2px;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
    backdrop-filter:blur(4px);
    z-index:3;
    pointer-events:none;
}

/* ---------------- CARET / ICON PATCH FOR EXPANDERS (▸ / ▾) ---------------- */
.stExpander > details > summary [data-testid="stIconMaterial"]{
  display:none !important;
}
.stExpander > details > summary { list-style: none; }
.stExpander > details > summary::-webkit-details-marker { display: none; }
.stExpander > details > summary {
  position: relative;
  padding-left: 18px; /* space for caret */
}
.stExpander > details > summary::before {
  content: "▸";
  position: absolute;
  left: 0;
  top: 0.1rem;
  color: #1f2937;     /* dark gray to match theme */
  font-weight: 700;
  font-size: 14px;
  line-height: 1;
}
.stExpander > details[open] > summary::before {
  content: "▾";
}

/* ---------------- MATCH FILTER CARET TO EXPANDER CARET ---------------- */
/* 1) Hide default chevron in Streamlit selectboxes */
div[data-baseweb="select"] svg{
  display:none !important;
}
/* 2) Add the same caret (▸ / ▾) to the select trigger */
div[data-baseweb="select"] div[role="combobox"]{
  position:relative;
}
div[data-baseweb="select"] div[role="combobox"]::after{
  content:"▸";
  position:absolute;
  right:10px;
  top:50%;
  transform:translateY(-50%);
  color:#1f2937;
  font-weight:700;
  font-size:14px;
  line-height:1;
}
div[data-baseweb="select"] div[role="combobox"][aria-expanded="true"]::after{
  content:"▾";
}

/* 3) Also show the same caret beside the Filter label text */
/* We target the label bound to key="flt" and draw the caret on the left,
   and we toggle it (▸ / ▾) by a data-open attribute we will set via a tiny JS observer. */
label[for="flt"]{
  position:relative;
  padding-left:18px; /* space for caret */
}
label[for="flt"]::before{
  content:"▸";
  position:absolute;
  left:0;
  top:0.1rem;
  color:#1f2937;
  font-weight:700;
  font-size:14px;
  line-height:1;
}
label[for="flt"][data-open="true"]::before{
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
        f'''
        <div class="title-wrap">
            <img class="title-logo" src="data:image/png;base64,{fabric_logo}">
            <div class="title">Fabric Migration Explorer</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# ---------------- FILTER (top-right) ----------------
with col3:
    all_option = "All"
    # If st.popover exists, we still use the selectbox inside (no change requested)
    if hasattr(st, "popover"):
        with st.popover("Filter", use_container_width=True):
            selected = st.selectbox("Hyperscaler", [all_option] + platforms, index=0, key="flt")
    else:
        st.caption("")  # small spacer
        selected = st.selectbox("Filter: Hyperscaler", [all_option] + platforms, index=0, key="flt", label_visibility="collapsed")

# ---------------- JS: Keep Filter label caret (▸/▾) in sync with dropdown open state ----------------
# We set label[for="flt"][data-open="true"] when the combobox aria-expanded="true"
st.markdown("""
<script>
(function(){
  const update = () => {
    const sb = window.parent.document.querySelector('div[data-baseweb="select"] div[role="combobox"]');
    const lbl = window.parent.document.querySelector('label[for="flt"]');
    if(!sb || !lbl) return;
    const isOpen = sb.getAttribute('aria-expanded') === 'true';
    if(isOpen) lbl.setAttribute('data-open', 'true'); else lbl.removeAttribute('data-open');
  };
  const target = window.parent.document.querySelector('div[data-baseweb="select"] div[role="combobox"]');
  if(target){
    update();
    const mo = new MutationObserver(update);
    mo.observe(target, { attributes:true, attributeFilter:['aria-expanded'] });
  }
})();
</script>
""", unsafe_allow_html=True)

# Compute filtered list (affects which cards/columns are drawn)
filtered_platforms = platforms if selected == "All" else [selected]

# ---------------- PLATFORM HEADER (MAIN PAGE CARDS) ----------------
st.markdown('<div class="platform-header"></div>', unsafe_allow_html=True)
header_cols = st.columns(len(filtered_platforms))
for i, p in enumerate(filtered_platforms):
    with header_cols[i]:
        st.markdown(
            f'''
            <div class="platform-card">
                <div class="cloud-wrap">
                    <img src="data:image/png;base64,{logo_base64.get(p, '')}" width="26">
                    <div class="cloud-label">{p}</div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

# Spacer between header cards and sections
st.markdown('<div class="platform-header-spacer"></div>', unsafe_allow_html=True)

# ---------------- HELPER: TILE RENDER ----------------
def render_tile(name: str, link: str, src_logo: str):
    safe_name = name.replace("à†’", "→")
    st.markdown(
        f"""
        <div class="tile">
            <a href="{link}" target="_blank">
                <img class="source-chip" src="data:image/png;base64,{src_logo}">
                <div class="tile-inner">
                    <div class="tile-title">{safe_name}</div>
                </div>
                <img class="fabric-chip" src="data:image/png;base64,{fabric_logo}">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- SECTIONS WITH ARROW (EXPAND/COLLAPSE) ----------------
# 1) STORAGE
with st.expander("STORAGE 📦", expanded=False):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("Storage", {}).items():
                render_tile(name, link, src_logo)

# 2) ETL
with st.expander("ETL ⚙", expanded=False):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("ETL", {}).items():
                render_tile(name, link, src_logo)

# 3) REPORTING
with st.expander("REPORTING 📊", expanded=False):
    cols = st.columns(len(filtered_platforms))
    for i, p in enumerate(filtered_platforms):
        with cols[i]:
            src_logo = logo_base64.get(p, "")
            for name, link in docs[p].get("Reporting", {}).items():
                render_tile(name, link, src_logo)