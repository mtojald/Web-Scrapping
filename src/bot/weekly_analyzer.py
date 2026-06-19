"""Geração do resumo semanal via Claude, com fallback local (OO)."""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime

import requests

from .models import FeedbackCollection


class WeeklyAnalysis:
    """Estrutura de dados do resultado de uma análise semanal."""

    def __init__(self, dados: dict, gerado_por_ia: bool, fonte_label: str):
        self.o_que_mudou = dados.get("o_que_mudou", "")
        self.intencoes = dados.get("intencoes", [])
        self.timeline = dados.get("timeline", [])
        self.empreendedor = dados.get("empreendedor", {})
        self.gerado_por_ia = gerado_por_ia
        self.fonte_label = fonte_label


class WeeklyAnalyzer:
    """Gera o resumo semanal a partir de uma FeedbackCollection.

    Tenta usar a API do Claude (ANTHROPIC_API_KEY); se indisponível ou
    com erro, usa uma análise heurística local (fallback).
    """

    MODELO = "claude-sonnet-4-6"
    ENDPOINT = "https://api.anthropic.com/v1/messages"

    def __init__(self, colecao: FeedbackCollection, api_key: str | None = None):
        self.colecao = colecao
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")

    # ── Contexto para o prompt ────────────────────────────
    def _preparar_contexto(self) -> str:
        por_data: dict[str, list[str]] = defaultdict(list)
        for f in self.colecao:
            resumo = f"{f.titulo} — {f.comentario}"[:200]
            por_data[f.data or "sem_data"].append(resumo)

        linhas = []
        for dt in sorted(por_data.keys())[-7:]:
            linhas.append(f"\n[{dt}]")
            for texto in por_data[dt][:5]:
                linhas.append(f"  • {texto}")

        fontes = ", ".join(self.colecao.fontes_presentes())
        return f"Total: {self.colecao.total}\nFontes: {fontes}\n\nPublicações recentes:{''.join(linhas)}"

    def _montar_prompt(self, contexto: str) -> str:
        return f"""Você é analista de mídias sociais do SEBRAE. Analise as publicações e retorne APENAS JSON válido, sem markdown.

Dados:
{contexto}

JSON esperado:
{{
  "o_que_mudou": "2-3 frases sobre o que mudou esta semana (tom, volume, temas)",
  "intencoes": [
    {{"titulo": "Buscar X", "descricao": "frase curta"}},
    {{"titulo": "Buscar Y", "descricao": "frase curta"}},
    {{"titulo": "Buscar Z", "descricao": "frase curta"}}
  ],
  "timeline": [
    {{"dia": "Segunda", "evento": "descrição breve"}},
    {{"dia": "Quarta",  "evento": "descrição breve"}},
    {{"dia": "Sexta",   "evento": "descrição breve"}}
  ],
  "empreendedor": {{
    "perfil": "Tipo de empreendedor (setor)",
    "descricao": "2-3 frases sobre frustrações, comportamentos e canais usados"
  }}
}}"""

    def _chamar_claude(self) -> dict:
        contexto = self._preparar_contexto()
        prompt = self._montar_prompt(contexto)
        resp = requests.post(
            self.ENDPOINT,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": self.MODELO,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        resp.raise_for_status()
        texto = resp.json()["content"][0]["text"]
        texto = re.sub(r"```(?:json)?|```", "", texto).strip()
        return json.loads(texto)

    # ── Fallback heurístico ────────────────────────────────
    def _analise_fallback(self) -> dict:
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        por_data = self.colecao.agrupar_por_data()

        timeline = []
        for dt in sorted(d for d in por_data if d != "sem_data")[-3:]:
            try:
                dia_nome = dias_semana[datetime.strptime(dt, "%Y-%m-%d").weekday()]
            except ValueError:
                dia_nome = dt
            itens_dia = por_data[dt][:2]
            titulos = [f.titulo or f.comentario[:60] for f in itens_dia]
            evento = "; ".join(t for t in titulos if t)[:120] or "Publicações coletadas neste dia."
            timeline.append({"dia": dia_nome, "evento": evento})

        if not timeline:
            timeline = [
                {"dia": "Seg", "evento": "Início da semana com publicações sobre capacitação."},
                {"dia": "Qua", "evento": "Pico de interações sobre crédito e financiamento."},
                {"dia": "Sex", "evento": "Conteúdos de empreendedorismo digital."},
            ]

        fontes = self.colecao.fontes_presentes()
        return {
            "o_que_mudou": (
                f"Foram coletadas {self.colecao.total} publicações de {', '.join(fontes) or 'nenhuma fonte'} "
                "sobre o SEBRAE. O volume indica atividade constante, com predominância de temas "
                "relacionados a capacitação e empreendedorismo."
            ),
            "intencoes": [
                {"titulo": "Buscar Capacitação", "descricao": "Usuários buscando cursos, oficinas e materiais de apoio do SEBRAE."},
                {"titulo": "Buscar Informação", "descricao": "Empreendedores pesquisando sobre MEI, crédito e regularização de negócios."},
                {"titulo": "Buscar Validação", "descricao": "Usuários compartilhando experiências para validar decisões de negócio."},
            ],
            "timeline": timeline,
            "empreendedor": {
                "perfil": "Microempreendedor Iniciante (setor de Serviços)",
                "descricao": "Pequeno empreendedor em fase de formalização. Busca respostas rápidas sobre MEI e crédito. Usa redes sociais e YouTube para aprender sobre gestão do negócio.",
            },
        }

    # ── API pública ────────────────────────────────────────
    def gerar(self) -> WeeklyAnalysis:
        if self.api_key:
            try:
                dados = self._chamar_claude()
                return WeeklyAnalysis(dados, gerado_por_ia=True, fonte_label="✨ Análise gerada por IA")
            except Exception as exc:  # noqa: BLE001 - queremos cair no fallback em qualquer erro
                dados = self._analise_fallback()
                return WeeklyAnalysis(dados, gerado_por_ia=False, fonte_label=f"⚠️ Fallback (erro na API: {exc})")
        dados = self._analise_fallback()
        return WeeklyAnalysis(dados, gerado_por_ia=False, fonte_label="ℹ️ Análise automática (sem ANTHROPIC_API_KEY)")
