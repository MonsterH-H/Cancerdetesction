import streamlit as st

def apply_custom_styles():
    # Primary Medical Theme: Teal / Emerald
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --accent: #0d9488;
            --accent-gradient: linear-gradient(135deg, #0d9488 0%, #065f46 100%);
            --border-color: #e2e8f0;
            --radius-lg: 20px;
            --radius-md: 12px;
            --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            --shadow-md: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }

        /* Global Styles */
        .stApp { background-color: var(--bg-secondary); }
        
        button, p, span, h1, h2, h3, label, div { 
            font-family: 'Outfit', sans-serif !important; 
        }

        /* Sidebar Standard */
        section[data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid var(--border-color) !important;
        }

        /* Sidebar Trigger fix */
        [data-testid="stSidebarCollapsedControl"] {
            background-color: var(--accent) !important;
            color: white !important;
            border-radius: 50%;
            padding: 5px;
        }
        
        /* Logo Styling */
        .logo-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1.5rem 1rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
            width: 100%;
        }
        
        .logo-icon-svg {
            width: 60px;
            height: 60px;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 4px 6px rgba(13, 148, 136, 0.2));
        }

        .logo-text {
            font-weight: 800;
            font-size: 1.6rem;
            letter-spacing: -1px;
            color: var(--text-main);
            margin: 0;
            padding: 0;
        }

        /* Typography */
        h1, h2, h3 { color: var(--text-main) !important; font-weight: 700 !important; letter-spacing: -0.5px; }
        p, span, label { color: var(--text-muted); }

        /* Premium Cards */
        .card {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card:hover { 
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
            border-color: var(--accent);
        }

        /* Metrics */
        [data-testid="stMetric"] {
            background: #ffffff;
            padding: 1.5rem !important;
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stMetricLabel"] { font-weight: 600 !important; text-transform: uppercase; font-size: 0.75rem !important; }
        [data-testid="stMetricValue"] { color: var(--accent) !important; font-size: 2.2rem !important; font-weight: 700 !important; }

        /* Buttons */
        .stButton>button {
            background: var(--accent-gradient);
            color: white !important;
            border-radius: var(--radius-md);
            border: none;
            padding: 0.8rem 1.5rem;
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(13, 148, 136, 0.4);
            background: var(--accent-gradient);
            opacity: 0.9;
        }

        /* Badges */
        .premium-badge {
            background: var(--accent-gradient);
            color: white;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
            box-shadow: 0 2px 8px rgba(13, 148, 136, 0.2);
        }

        /* Header Layout */
        .premium-header {
            padding-bottom: 2.5rem;
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        /* Cleanup Streamlit but keep triggers visible */
        footer {visibility: hidden;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0);}
        
    </style>
    """, unsafe_allow_html=True)

def get_logo_html(size=60):
    return f"""
        <div class="logo-container">
            <div style="font-size: 2.2rem; margin-bottom: 5px;">🧬</div>
            <div class="logo-text">ONCOAI <span style="color:var(--accent)">PRO</span></div>
            <p style="font-size:0.75rem; margin-top:5px; color:var(--text-muted); font-weight:600; text-transform: uppercase; letter-spacing: 1px;">Medical Intelligence</p>
        </div>
    """

def render_logo(sidebar=True):
    html = get_logo_html()
    if sidebar:
        st.sidebar.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)

def render_premium_header(title, subtitle, icon_class=None, badge=None):
    badge_html = f'<span class="premium-badge">{badge}</span>' if badge else ''
    
    st.markdown(f"""
        <div class="premium-header">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <h1 style="margin: 0; font-size: 2.2rem; color: #0f172a !important;">{title}</h1>
                    <p style="margin: 8px 0 0 0; font-size: 1rem; color: var(--text-muted);">{subtitle}</p>
                </div>
                {badge_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_section_title(title, icon_class=None):
    st.markdown(f"""
        <div style="margin-top: 2rem; margin-bottom: 1rem; border-left: 4px solid var(--accent); padding-left: 15px;">
            <h3 style="margin:0; font-size: 1.2rem; color: #0f172a !important; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h3>
        </div>
    """, unsafe_allow_html=True)
