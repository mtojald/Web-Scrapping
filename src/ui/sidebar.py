"""Sidebar do Atlas Insights, encapsulada em uma classe (OO)."""
from __future__ import annotations

import streamlit as st

from .theme import AtlasTheme
from ..bot.models import SOURCE_META


class AtlasSidebar:
    """Renderiza a sidebar compartilhada: perfil, stats, navegação e filtros."""

    PAGINAS = {
        "Dashboard":   "pages/1_dashboard.py",
        "Publicações": "pages/2_publicacoes.py",
        "Resumo":      "pages/3_resumo.py",
        "Descobertas": None,
    }

    def __init__(self, pagina_atual: str, colecao, usuario: str = "João Cabral", org: str = "SEBRAE"):
        self.pagina_atual = pagina_atual
        self.colecao = colecao
        self.usuario = usuario
        self.org = org
        self._fontes_disponiveis = colecao.fontes_presentes() if colecao else []

    # ── Sub-renders ──────────────────────────────────────
    def _renderizar_perfil(self) -> None:
        iniciais = "".join(p[0] for p in self.usuario.split()[:2]).upper()
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:18px 14px 14px">
            <div style="width:40px;height:40px;border-radius:10px;
                        background:linear-gradient(135deg,#2a8aa3,#1a5060);
                        border:1.5px solid rgba(255,255,255,0.18);
                        display:flex;align-items:center;justify-content:center;
                        font-size:15px;font-weight:700;color:#fff;flex-shrink:0">{iniciais}</div>
            <div>
                <div style="font-size:13px;font-weight:600;color:#eaf6f5">{self.usuario}</div>
                <span class="user-tag">{self.org}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def _renderizar_stats(self) -> None:
        total = len(self.colecao) if self.colecao else 0
        n_fontes = len(self._fontes_disponiveis)
        total_fmt = f"{total:,}".replace(",", ".")
        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px 14px;
                    margin:0 0 12px;font-size:11.5px">
            <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:7px">
                <span style="color:#6ba8a4;font-size:9.5px;font-family:'JetBrains Mono',monospace;
                            text-transform:uppercase;letter-spacing:0.06em">Publicações</span>
                <b style="color:#eaf6f5;font-size:12px">{total_fmt}</b>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:baseline">
                <span style="color:#6ba8a4;font-size:9.5px;font-family:'JetBrains Mono',monospace;
                            text-transform:uppercase;letter-spacing:0.06em">Fontes ativas</span>
                <b style="color:#eaf6f5;font-size:12px">{n_fontes}</b>
            </div>
        </div>
        <hr class="atlas"/>
        """, unsafe_allow_html=True)

    def _renderizar_navegacao(self) -> None:
        for nome, destino in self.PAGINAS.items():
            ativo = nome == self.pagina_atual
            if ativo:
                st.markdown("<div class='nav-active'>", unsafe_allow_html=True)
            if st.button(nome, key=f"nav_{nome}", use_container_width=True, disabled=destino is None):
                if destino:
                    st.switch_page(destino)
            if ativo:
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr class='atlas'/>", unsafe_allow_html=True)

    def _renderizar_filtro_plataformas(self) -> set[str]:
        """Filtro de plataformas no estilo toggle do Atlas Insights."""
        if not self._fontes_disponiveis:
            return set()

        chave_estado = "atlas_plataformas_ativas"
        if chave_estado not in st.session_state:
            st.session_state[chave_estado] = set(self._fontes_disponiveis)

        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;color:#6ba8a4;
                    text-transform:uppercase;letter-spacing:0.06em;margin:4px 0 8px;padding:0 14px">
            Plataformas
        </div>
        """, unsafe_allow_html=True)

        ativas: set[str] = set(st.session_state[chave_estado])
        for fonte in self._fontes_disponiveis:
            ligado = fonte in ativas
            meta = SOURCE_META.get(fonte, {"icon": "○", "color": "#1a5060"})
            rotulo = f"{'✓' if ligado else '○'} {meta['icon']} {fonte}"
            st.markdown("<div class='platform-toggle'>", unsafe_allow_html=True)
            if st.button(rotulo, key=f"toggle_{fonte}", use_container_width=True):
                if ligado:
                    ativas.discard(fonte)
                else:
                    ativas.add(fonte)
                if ativas:
                    st.session_state[chave_estado] = ativas
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Todas", key="sel_todas", use_container_width=True):
                st.session_state[chave_estado] = set(self._fontes_disponiveis)
                st.rerun()
        with col_b:
            if st.button("Nenhuma", key="sel_nenhuma", use_container_width=True):
                st.session_state[chave_estado] = {self._fontes_disponiveis[0]}
                st.rerun()

        return set(st.session_state[chave_estado])

    # ── API pública ────────────────────────────────────────
    def renderizar(self, extra_content=None) -> set[str]:
        """Renderiza a sidebar completa e retorna o conjunto de plataformas ativas."""
        st.markdown(AtlasTheme.css_global(), unsafe_allow_html=True)
        with st.sidebar:
            self._renderizar_perfil()
            self._renderizar_stats()
            self._renderizar_navegacao()
            plataformas_ativas = self._renderizar_filtro_plataformas()
            if extra_content:
                st.markdown("<hr class='atlas'/>", unsafe_allow_html=True)
                extra_content()
        return plataformas_ativas
