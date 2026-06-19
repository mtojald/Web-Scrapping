"""Modelos de dados orientados a objetos do projeto."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime


SOURCE_META = {
    "NewsAPI":   {"icon": "N",  "color": "#1848a0"},
    "YouTube":   {"icon": "▶",  "color": "#c00000"},
    "Reddit":    {"icon": "R",  "color": "#e04a1e"},
    "Apify":     {"icon": "A",  "color": "#6b2fb3"},
    "Instagram": {"icon": "IG", "color": "#c13584"},
    "Twitter":   {"icon": "𝕏",  "color": "#0f1419"},
}

SENTIMENT_STYLE = {
    "Positivo": {"bg": "#d4f0e4", "fg": "#1c7f54", "border": "#a8ddc4"},
    "Neutro":   {"bg": "#fff8e0", "fg": "#c28a00", "border": "#f0d98a"},
    "Crítico":  {"bg": "#fde8e6", "fg": "#b8362b", "border": "#f0b0aa"},
}

_POS_KEYWORDS = (
    "agradec", "parabéns", "excelente", "ótimo", "apoio", "expande", "cresce",
    "inovação", "capacita", "fortalec", "solução", "sucesso", "gratuito", "benefici",
)
_NEG_KEYWORDS = (
    "erro", "falha", "problema", "trava", "não consigo", "urgente", "crítico",
    "reclamação", "bug", "sistema", "prejuízo", "dificuldade", "impedimento",
)


class Sentimento:
    """Encapsula a lógica de classificação de sentimento de um feedback."""

    POSITIVO = "Positivo"
    NEUTRO = "Neutro"
    CRITICO = "Crítico"

    @staticmethod
    def extrair_nota(avaliacao: str) -> float | None:
        match = re.search(r"(\d+(?:[.,]\d+)?)", str(avaliacao))
        if not match:
            return None
        valor = float(match.group(1).replace(",", "."))
        return round(valor) if valor <= 5 else None

    @classmethod
    def classificar(cls, titulo: str, comentario: str, avaliacao: str) -> str:
        nota = cls.extrair_nota(avaliacao)
        if nota is not None:
            if nota >= 4:
                return cls.POSITIVO
            if nota == 3:
                return cls.NEUTRO
            return cls.CRITICO

        texto = f"{titulo} {comentario}".lower()
        pontos_pos = sum(1 for kw in _POS_KEYWORDS if kw in texto)
        pontos_neg = sum(1 for kw in _NEG_KEYWORDS if kw in texto)
        if pontos_neg > pontos_pos:
            return cls.CRITICO
        if pontos_pos > pontos_neg:
            return cls.POSITIVO
        return cls.NEUTRO

    @staticmethod
    def estilo(sentimento: str) -> dict:
        return SENTIMENT_STYLE.get(
            sentimento, {"bg": "#e8edf0", "fg": "#5b7083", "border": "#c5ced4"}
        )


@dataclass
class Feedback:
    """Representa um único item coletado por qualquer scraper."""

    fonte: str
    titulo: str = ""
    comentario: str = ""
    avaliacao: str = ""
    url: str = ""
    data: str = ""
    alvo_coleta: str = ""
    sentimento: str = field(default="", repr=False)

    def __post_init__(self):
        if not self.sentimento:
            self.sentimento = Sentimento.classificar(self.titulo, self.comentario, self.avaliacao)

    # ── Apresentação ──────────────────────────────────────
    @property
    def icone_fonte(self) -> str:
        return SOURCE_META.get(self.fonte, {}).get("icon", "○")

    @property
    def cor_fonte(self) -> str:
        return SOURCE_META.get(self.fonte, {}).get("color", "#1a5060")

    @property
    def estilo_sentimento(self) -> dict:
        return Sentimento.estilo(self.sentimento)

    @property
    def tempo_relativo(self) -> str:
        if not self.data:
            return "Data desconhecida"
        try:
            d = datetime.strptime(str(self.data)[:10], "%Y-%m-%d").date()
        except ValueError:
            return str(self.data)
        delta = (date.today() - d).days
        if delta <= 0:
            return "Hoje"
        if delta == 1:
            return "Há 1 dia"
        if delta < 7:
            return f"Há {delta} dias"
        if delta < 30:
            return f"Há {delta // 7} semana(s)"
        return f"Há {delta // 30} mês(es)"

    def corpo_resumido(self, limite: int = 220) -> str:
        texto = self.comentario or ""
        return (texto[:limite] + "…") if len(texto) > limite else texto

    def como_dict(self) -> dict:
        return {
            "fonte": self.fonte,
            "titulo_feedback": self.titulo,
            "comentario_usuario": self.comentario,
            "avaliacao": self.avaliacao,
            "url": self.url,
            "data": self.data,
            "alvo_coleta": self.alvo_coleta,
            "sentimento": self.sentimento,
        }

    @classmethod
    def de_dict(cls, dados: dict) -> "Feedback":
        return cls(
            fonte=dados.get("fonte", "Desconhecida"),
            titulo=dados.get("titulo_feedback", "") or "",
            comentario=dados.get("comentario_usuario", "") or "",
            avaliacao=dados.get("avaliacao", "") or "",
            url=dados.get("url", "") or "",
            data=dados.get("data", "") or "",
            alvo_coleta=dados.get("alvo_coleta", "") or "",
        )


class FeedbackCollection:
    """Coleção orientada a objetos de Feedbacks, com filtros e métricas agregadas."""

    def __init__(self, itens: list[Feedback] | None = None):
        self._itens: list[Feedback] = itens or []

    # ── Construção ────────────────────────────────────────
    @classmethod
    def de_lista_dicts(cls, lista: list[dict]) -> "FeedbackCollection":
        return cls([Feedback.de_dict(d) for d in lista])

    def __len__(self) -> int:
        return len(self._itens)

    def __iter__(self):
        return iter(self._itens)

    def adicionar(self, feedback: Feedback) -> None:
        self._itens.append(feedback)

    def estender(self, outros: "FeedbackCollection | list[Feedback]") -> "FeedbackCollection":
        novos = list(outros)
        return FeedbackCollection(self._itens + novos)

    # ── Filtros (retornam novas coleções, sem mutar) ───────
    def filtrar_por_fonte(self, fontes: set[str]) -> "FeedbackCollection":
        if not fontes:
            return FeedbackCollection(list(self._itens))
        return FeedbackCollection([f for f in self._itens if f.fonte in fontes])

    def filtrar_por_sentimento(self, sentimentos: set[str]) -> "FeedbackCollection":
        if not sentimentos:
            return FeedbackCollection(list(self._itens))
        return FeedbackCollection([f for f in self._itens if f.sentimento in sentimentos])

    def filtrar_por_busca(self, termo: str) -> "FeedbackCollection":
        if not termo:
            return FeedbackCollection(list(self._itens))
        termo = termo.lower()
        return FeedbackCollection([
            f for f in self._itens
            if termo in f.titulo.lower() or termo in f.comentario.lower()
        ])

    def ordenar_por_data(self, decrescente: bool = True) -> "FeedbackCollection":
        ordenados = sorted(self._itens, key=lambda f: f.data or "", reverse=decrescente)
        return FeedbackCollection(ordenados)

    def primeiro(self) -> Feedback | None:
        return self._itens[0] if self._itens else None

    def fontes_presentes(self) -> list[str]:
        return sorted({f.fonte for f in self._itens})

    def sentimentos_presentes(self) -> list[str]:
        return sorted({f.sentimento for f in self._itens})

    # ── Métricas agregadas ──────────────────────────────────
    def contar_por_sentimento(self, sentimento: str) -> int:
        return sum(1 for f in self._itens if f.sentimento == sentimento)

    @property
    def total(self) -> int:
        return len(self._itens)

    @property
    def positivos(self) -> int:
        return self.contar_por_sentimento(Sentimento.POSITIVO)

    @property
    def neutros(self) -> int:
        return self.contar_por_sentimento(Sentimento.NEUTRO)

    @property
    def criticos(self) -> int:
        return self.contar_por_sentimento(Sentimento.CRITICO)

    @property
    def percentual_positivo(self) -> int:
        return round(self.positivos / self.total * 100) if self.total else 0

    @property
    def percentual_neutro(self) -> int:
        return round(self.neutros / self.total * 100) if self.total else 0

    @property
    def percentual_critico(self) -> int:
        return round(self.criticos / self.total * 100) if self.total else 0

    @property
    def nps(self) -> int:
        if not self.total:
            return 50
        bruto = round((self.positivos - self.criticos) / self.total * 100) + 50
        return max(0, min(100, bruto))

    @property
    def csat(self) -> int:
        return self.percentual_positivo

    @property
    def media_estrelas(self) -> float:
        notas = [n for n in (Sentimento.extrair_nota(f.avaliacao) for f in self._itens) if n is not None]
        if notas:
            return sum(notas) / len(notas)
        return round(3.2 + self.percentual_positivo * 0.018, 1)

    def contagem_por_fonte(self) -> dict[str, int]:
        contagem: dict[str, int] = {}
        for f in self._itens:
            contagem[f.fonte] = contagem.get(f.fonte, 0) + 1
        return contagem

    def agrupar_por_data(self) -> dict[str, list[Feedback]]:
        grupos: dict[str, list[Feedback]] = {}
        for f in self._itens:
            grupos.setdefault(f.data or "sem_data", []).append(f)
        return grupos

    def como_lista_dicts(self) -> list[dict]:
        return [f.como_dict() for f in self._itens]
