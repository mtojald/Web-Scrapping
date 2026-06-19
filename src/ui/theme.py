"""Tema visual Atlas Insights (OO) — cores, fontes e CSS global."""
from __future__ import annotations

import textwrap


class AtlasTheme:
    """Centraliza paleta e CSS reaproveitado por toda a aplicação."""

    CORES = {
        "bg":          "#edeae4",
        "sidebar1":    "#122c34",
        "sidebar2":    "#0c1f26",
        "card":        "#ffffff",
        "card_border": "#cce3df",
        "card_soft":   "#eaf5f3",
        "ink":         "#0f2027",
        "ink2":        "#4a6b70",
        "ink3":        "#253a40",
        "accent":      "#1a5060",
        "accent_lt":   "#2a9aad",
        "highlight":   "#5ecfde",
        "good":        "#1c7f54",
        "bad":         "#b8362b",
        "warn":        "#c28a00",
    }

    FONTE_SANS = "'DM Sans', sans-serif"
    FONTE_MONO = "'JetBrains Mono', monospace"

    @classmethod
    def css_global(cls) -> str:
        c = cls.CORES
        return textwrap.dedent(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: {cls.FONTE_SANS};
            background-color: {c['bg']} !important;
            color: {c['ink']} !important;
        }}
        .main .block-container {{
            background: {c['bg']};
            padding-top: 1.2rem;
            max-width: 1400px;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background: linear-gradient(175deg, {c['sidebar1']} 0%, {c['sidebar2']} 100%);
            border-right: 1px solid rgba(42,180,200,0.12);
        }}
        [data-testid="stSidebar"] * {{ color: #eaf6f5 !important; }}
        [data-testid="stSidebar"] .stMultiSelect span,
        [data-testid="stSidebar"] input {{
            background: rgba(0,0,0,0.2) !important;
            color: #eaf6f5 !important;
        }}

        hr.atlas {{ border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 8px 0; }}

        .user-tag {{
            background: rgba(94,207,222,0.12); color: #8ee8f0 !important;
            font-size: 9px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
            padding: 2px 8px; border-radius: 3px; display: inline-block; margin-top: 3px;
            border: 1px solid rgba(94,207,222,0.18);
        }}

        .eyebrow {{
            font-family: {cls.FONTE_MONO}; font-size: 10px; color: {c['ink2']};
            letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 6px;
        }}
        .page-title {{
            font-size: 28px; font-weight: 700; color: {c['ink']};
            letter-spacing: -0.025em; line-height: 1; margin-bottom: 4px;
        }}
        .page-subtitle {{ font-size: 13px; color: {c['ink2']}; margin-bottom: 22px; }}

        .atlas-card {{
            background: {c['card']}; border: 1px solid {c['card_border']};
            border-radius: 16px; padding: 20px 22px;
            box-shadow: 0 2px 14px rgba(15,32,39,0.07);
        }}
        .atlas-card h4 {{
            font-size: 15px; font-weight: 700; color: {c['ink']};
            letter-spacing: -0.015em; margin: 0 0 2px;
        }}
        .atlas-card .mono {{
            font-family: {cls.FONTE_MONO}; font-size: 10px; color: {c['ink2']};
            text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 14px;
        }}

        .metric-card {{
            background: {c['card']}; border: 1px solid {c['card_border']};
            border-top: 3px solid {c['accent']}; border-radius: 14px;
            padding: 18px 22px 16px; box-shadow: 0 2px 12px rgba(15,32,39,0.07);
        }}
        .metric-label {{
            font-family: {cls.FONTE_MONO}; font-size: 10px; color: {c['ink2']};
            text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;
        }}
        .metric-value {{
            font-size: 30px; font-weight: 700; color: {c['ink']};
            letter-spacing: -0.025em; line-height: 1.1; margin-bottom: 4px;
        }}
        .metric-delta {{ font-size: 11px; font-family: {cls.FONTE_MONO}; }}

        .gauge-row {{ margin-bottom: 16px; }}
        .gauge-label {{
            font-size: 11px; color: {c['ink2']}; font-family: {cls.FONTE_MONO};
            text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;
        }}
        .gauge-track {{ flex: 1; height: 8px; border-radius: 4px; background: #e8f0ef; overflow: hidden; }}
        .gauge-fill {{ height: 100%; border-radius: 4px; }}

        .post-card {{
            background: {c['card_soft']}; border: 1px solid {c['card_border']};
            border-left: 4px solid {c['accent']}; border-radius: 12px; padding: 14px;
        }}
        .post-avatar {{
            width: 36px; height: 36px; border-radius: 10px;
            background: linear-gradient(135deg, {c['accent']}, {c['accent_lt']});
            display: flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 700; font-size: 12px; flex-shrink: 0;
        }}
        .post-title {{ font-weight: 700; font-size: 13.5px; color: {c['ink']}; line-height: 1.3; }}
        .post-meta {{ font-size: 11px; color: {c['ink2']}; }}
        .post-body {{ font-size: 13px; line-height: 1.55; color: {c['ink3']}; margin: 10px 0 8px; }}
        .post-stats {{
            display: flex; gap: 16px; padding-top: 8px;
            border-top: 1px solid {c['card_border']}; font-size: 11.5px; color: {c['ink2']};
        }}

        .bar-row {{ margin-bottom: 8px; }}
        .bar-track {{ height: 7px; border-radius: 3px; background: #e8f0ef; overflow: hidden; }}
        .bar-fill {{ height: 100%; border-radius: 3px; }}

        .pub-section-header {{
            display:flex; align-items:center; gap:8px; font-size:13px; font-weight:700;
            color:{c['accent']}; letter-spacing:0.04em; margin-bottom:16px; text-transform:uppercase;
        }}
        .pub-section-header::before {{ content:"❖"; font-size:14px; color:{c['accent_lt']}; }}
        .pub-card {{
            background:{c['card']}; border:1.5px solid {c['card_border']};
            border-radius:16px; padding:20px; margin-bottom:18px;
        }}
        .pub-card-header {{ display:flex; align-items:center; gap:12px; margin-bottom:14px; }}
        .pub-source-icon {{
            width:42px; height:42px; border-radius:10px; display:flex;
            align-items:center; justify-content:center; font-size:16px; font-weight:700;
            color:#fff; flex-shrink:0;
        }}
        .pub-title {{ font-size:15px; font-weight:700; color:{c['ink']}; line-height:1.35; }}
        .pub-body {{
            font-size:13.5px; color:{c['ink3']}; line-height:1.55; margin-bottom:14px;
            background:{c['card_soft']}; border-radius:8px; padding:10px 14px;
            border-left:3px solid {c['card_border']}; font-style:italic;
        }}
        .badge-row {{ display:flex; justify-content:space-between; align-items:center; }}
        .pub-time {{ font-size:11.5px; color:{c['ink2']}; font-family:{cls.FONTE_MONO}; }}

        .intent-card {{
            background:{c['card']}; border:1px solid {c['card_border']}; border-radius:14px;
            padding:16px; box-shadow: 0 2px 8px rgba(15,32,39,0.05); height: 100%;
        }}
        .intent-num {{
            font-family:{cls.FONTE_MONO}; font-size:10px; font-weight:700; color:{c['accent']};
            text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;
        }}
        .intent-title {{ font-size:14px; font-weight:700; color:{c['ink']}; margin-bottom:8px; letter-spacing:-0.01em; line-height:1.3; }}
        .intent-desc {{ font-size:12.5px; color:{c['ink3']}; line-height:1.55; }}

        .timeline-chip {{
            background:{c['card_soft']}; border:1.5px solid {c['card_border']}; border-radius:6px;
            padding:5px 14px; font-size:10.5px; font-weight:700; color:{c['ink']};
            font-family:{cls.FONTE_MONO}; text-transform:uppercase; letter-spacing:0.06em;
            white-space:nowrap; display:inline-block; margin-bottom: 14px;
        }}
        .timeline-dot {{
            width:14px; height:14px; border-radius:50%; background:{c['accent']};
            box-shadow: 0 0 0 3px {c['bg']}, 0 0 0 5px {c['accent']}; margin-bottom: 14px;
        }}
        .timeline-event {{
            background:{c['card_soft']}; border:1px solid {c['card_border']}; border-radius:10px;
            padding:10px 12px; font-size:11.5px; color:{c['ink3']}; line-height:1.5; text-align:center;
        }}

        .empreendedor-avatar {{
            width:72px; height:72px; border-radius:50%;
            background: linear-gradient(135deg, {c['accent']}, {c['accent_lt']});
            display:flex; align-items:center; justify-content:center; font-size:32px;
            margin: 0 auto 16px; border: 3px solid {c['card_border']};
            box-shadow: 0 4px 16px rgba(26,80,96,0.18);
        }}

        /* Navegação da sidebar */
        div[data-testid="stSidebar"] .stButton > button {{
            width: 100%; background: transparent !important; border: none !important;
            color: rgba(219,238,237,0.65) !important; font-size: 14px !important; font-weight: 500 !important;
            text-align: left !important; padding: 9px 14px !important; border-radius: 0 8px 8px 0 !important;
            margin-bottom: 2px !important; cursor: pointer; border-left: 3px solid transparent !important;
        }}
        div[data-testid="stSidebar"] .stButton > button:hover {{ background: rgba(255,255,255,0.08) !important; }}
        div[data-testid="stSidebar"] .nav-active > button {{
            background: rgba(255,255,255,0.1) !important; font-weight: 700 !important;
            color: #ffffff !important; border-left: 3px solid {c['highlight']} !important;
        }}

        /* Toggle de plataformas */
        div[data-testid="stSidebar"] .platform-toggle > button {{
            border-radius: 8px !important; padding: 7px 10px !important;
            font-size: 12px !important; margin-bottom: 4px !important;
        }}

        /* Containers nativos usados como "card" quando o conteúdo mistura
           HTML com widgets nativos do Streamlit (ex: st.columns internas) */
        div[class*="st-key-card_"] {{
            background: {c['card']} !important;
            border: 1px solid {c['card_border']} !important;
            border-radius: 16px !important;
            padding: 20px 22px !important;
            box-shadow: 0 2px 14px rgba(15,32,39,0.07) !important;
        }}
        </style>
        """)
