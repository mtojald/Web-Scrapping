"""Pagina Resumo do Atlas Insights."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from src.ui.page import AtlasPage
from src.ui.components import IntentCard, TimelineEvent, EntrepreneurOfWeekCard
from src.bot.weekly_analyzer import WeeklyAnalyzer


class ResumoPage(AtlasPage):
    NOME_PAGINA = "Resumo"

    def conteudo_extra_sidebar(self) -> None:
        if st.button("Regenerar analise", use_container_width=True):
            st.session_state.pop("resumo_cache", None)
            st.rerun()

    def _obter_analise(self):
        if "resumo_cache" not in st.session_state:
            with st.spinner("Gerando analise..."):
                analise = WeeklyAnalyzer(self.colecao_filtrada).gerar()
                st.session_state["resumo_cache"] = analise
        return st.session_state["resumo_cache"]

    def renderizar_conteudo(self) -> None:
        self.cabecalho("Resumo Semanal", "Analise automatica do comportamento de usuarios nesta semana")

        analise = self._obter_analise()
        st.markdown(
            f"<div class='mono' style='margin-bottom:20px'>{analise.fonte_label}</div>",
            unsafe_allow_html=True,
        )

        # -- Linha 1: O que mudou + Intencoes ----------------
        col_mudou, col_intencoes = st.columns([1.1, 2])

        with col_mudou:
            st.markdown(f"""
            <div class="atlas-card" style="min-height:160px">
                <h4>O que mudou esta semana?</h4>
                <div class="mono">Em relacao a semana passada</div>
                <p style="font-size:13.5px;color:#2a3f44;line-height:1.65">{analise.o_que_mudou}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_intencoes:
            with st.container(key="card_intencoes"):
                st.markdown("""
                <h4 style="font-size:15px;font-weight:700;color:#0f2027;margin:0 0 2px">Intenções da semana</h4>
                <div class="mono">O que o usuário buscou</div>
                """, unsafe_allow_html=True)
                if analise.intencoes:
                    cols_int = st.columns(len(analise.intencoes))
                    for i, (col, item) in enumerate(zip(cols_int, analise.intencoes)):
                        with col:
                            IntentCard(
                                numero=f"{i + 1:02d}",
                                titulo=item.get("titulo", ""),
                                descricao=item.get("descricao", ""),
                            ).render()

        st.markdown("<div style='margin-top:18px'></div>", unsafe_allow_html=True)

        # -- Linha 2: Timeline + Empreendedor ----------------
        col_timeline, col_emp = st.columns([2, 1])

        with col_timeline:
            with st.container(key="card_timeline"):
                st.markdown("""
                <h4 style="font-size:16px;font-weight:700;color:#0f2027;margin:0 0 2px">Linha do tempo</h4>
                <div class="mono" style="margin-bottom:28px">Eventos relevantes da semana</div>
                """, unsafe_allow_html=True)
                if analise.timeline:
                    cols_tl = st.columns(len(analise.timeline))
                    for col, ev in zip(cols_tl, analise.timeline):
                        with col:
                            TimelineEvent(ev.get("dia", ""), ev.get("evento", "")).render()

        with col_emp:
            emp = analise.empreendedor or {}
            EntrepreneurOfWeekCard(
                perfil=emp.get("perfil", ""),
                descricao=emp.get("descricao", ""),
            ).render()


ResumoPage().executar()
