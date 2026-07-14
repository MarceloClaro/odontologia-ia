#!/usr/bin/env python3
"""
Sistema de Experiência (XP) — OdontoIA: Livro Imersão
SPEC-951-R200
Autor: Edson Laranjeiras

Motor de gamificação que calcula XP, níveis e badges
com base no progresso do leitor no livro.
"""

from __future__ import annotations
import yaml
import json
from pathlib import Path
from dataclasses import dataclass, field, fields
from typing import Optional
import hashlib

# ---------------------------------------------------------------------------
# Tabela de Ações e XP
# ---------------------------------------------------------------------------

TABELA_XP: dict[str, int] = {
    "ler_secao": 50,
    "fazer_pratica": 200,
    "passar_testes_tdd": 500,
    "responder_desafio": 300,
    "completar_capitulo": 1000,
    "completar_parte": 5000,
    "escrever_spec": 250,
    "rodar_notebook": 150,
    "criar_figura": 200,
    "publicar_modelo": 1000,
    "revisar_codigo": 300,
    "ajudar_comunidade": 400,
}

LIMITE_XP_DIARIO = 5000

# ---------------------------------------------------------------------------
# Níveis e Progressão
# ---------------------------------------------------------------------------

NIVEIS: list[dict] = [
    {"nivel": 1, "titulo": "Curioso Digital", "xp_necessario": 0},
    {"nivel": 2, "titulo": "Aprendiz de IA", "xp_necessario": 2_000},
    {"nivel": 3, "titulo": "Praticante Clínico", "xp_necessario": 5_000},
    {"nivel": 4, "titulo": "Desenvolvedor Odontológico", "xp_necessario": 12_000},
    {"nivel": 5, "titulo": "Arquiteto de Soluções", "xp_necessario": 25_000},
    {"nivel": 6, "titulo": "Pesquisador IA-Odonto", "xp_necessario": 50_000},
    {"nivel": 7, "titulo": "Mestre em Gêmeos Digitais", "xp_necessario": 100_000},
    {"nivel": 8, "titulo": "PhD em Odontologia IA", "xp_necessario": 200_000},
]


# ---------------------------------------------------------------------------
# Modelos de Dados
# ---------------------------------------------------------------------------

@dataclass
class Badge:
    id: str
    nome: str
    descricao: str
    icone: str
    xp: int
    capitulo: int
    requisito: str = ""
    conquistado: bool = False
    data_conquista: Optional[str] = None


@dataclass
class ProgressoLeitor:
    leitor_id: str
    nome: str
    email: str
    xp_total: int = 0
    xp_diario: int = 0
    data_ultima_acao: Optional[str] = None
    capitulos_completos: list[int] = field(default_factory=list)
    badges_conquistados: list[str] = field(default_factory=list)
    acoes: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Motor de Imersão
# ---------------------------------------------------------------------------

class MotorImersao:
    """Motor central de gamificação do OdontoIA."""

    def __init__(self, leitor_id: str, nome: str, email: str):
        self.leitor = ProgressoLeitor(
            leitor_id=leitor_id,
            nome=nome,
            email=email,
        )
        self._carregar_badges()

    def _carregar_badges(self):
        """Carrega badges do arquivo YAML."""
        badges_path = Path(__file__).parent / "badges.yaml"
        if badges_path.exists():
            with open(badges_path) as f:
                data = yaml.safe_load(f)
            campos_badge = {f.name for f in fields(Badge)}
            self.badges_disponiveis = [
                Badge(**{k: v for k, v in b.items() if k in campos_badge})
                for b in data["badges"]
            ]
        else:
            self.badges_disponiveis = []

    def registrar_acao(
        self, acao: str, capitulo: int, metadata: Optional[dict] = None
    ) -> dict:
        """
        Registra uma ação do leitor e retorna resultado com XP, badges, etc.
        
        Args:
            acao: Tipo de ação (ver TABELA_XP)
            capitulo: Número do capítulo
            metadata: Informações adicionais
            
        Returns:
            Dict com resultado da ação
        """
        
        # Calcular XP
        xp_acao = TABELA_XP.get(acao, 10)
        
        # Verificar limite diário
        if self.leitor.xp_diario + xp_acao > LIMITE_XP_DIARIO:
            xp_acao = LIMITE_XP_DIARIO - self.leitor.xp_diario
            if xp_acao <= 0:
                return {
                    "status": "limite_diario",
                    "mensagem": "Limite diário de XP atingido! Volte amanhã.",
                    "xp_ganho": 0,
                }
        
        # Atualizar XP
        self.leitor.xp_total += xp_acao
        self.leitor.xp_diario += xp_acao
        
        # Registrar ação
        self.leitor.acoes.append({
            "acao": acao,
            "capitulo": capitulo,
            "xp": xp_acao,
            "metadata": metadata or {},
        })
        
        # Verificar novo nível
        nivel_anterior = self._calcular_nivel(self.leitor.xp_total - xp_acao)
        nivel_atual = self._calcular_nivel(self.leitor.xp_total)
        subiu_nivel = nivel_atual["nivel"] > nivel_anterior["nivel"]
        
        # Verificar badges
        badges_novos = self._verificar_badges(capitulo)
        
        # Verificar capítulo completo
        capitulo_completo = False
        if acao == "completar_capitulo" and capitulo not in self.leitor.capitulos_completos:
            self.leitor.capitulos_completos.append(capitulo)
            capitulo_completo = True
        
        return {
            "status": "ok",
            "xp_ganho": xp_acao,
            "xp_total": self.leitor.xp_total,
            "nivel_anterior": nivel_anterior,
            "nivel_atual": nivel_atual,
            "subiu_nivel": subiu_nivel,
            "badges_novos": badges_novos,
            "capitulo_completo": capitulo_completo,
            "proximo_nivel": self._proximo_nivel(),
        }
    
    def _calcular_nivel(self, xp: int) -> dict:
        """Calcula o nível com base no XP total."""
        nivel_atual = NIVEIS[0]
        for nivel in reversed(NIVEIS):
            if xp >= nivel["xp_necessario"]:
                nivel_atual = nivel
                break
        return nivel_atual
    
    def _proximo_nivel(self) -> dict:
        """Retorna informações do próximo nível."""
        nivel_atual = self._calcular_nivel(self.leitor.xp_total)
        idx_atual = next(
            i for i, n in enumerate(NIVEIS) if n["nivel"] == nivel_atual["nivel"]
        )
        if idx_atual + 1 < len(NIVEIS):
            proximo = NIVEIS[idx_atual + 1]
            return {
                "nivel": proximo["nivel"],
                "titulo": proximo["titulo"],
                "xp_necessario": proximo["xp_necessario"],
                "xp_faltando": proximo["xp_necessario"] - self.leitor.xp_total,
                "progresso_pct": (
                    (self.leitor.xp_total / proximo["xp_necessario"]) * 100
                ),
            }
        return {"nivel": nivel_atual["nivel"], "titulo": "MÁXIMO", "completo": True}
    
    def _verificar_badges(self, capitulo: int) -> list[Badge]:
        """Verifica se novos badges foram conquistados."""
        novos = []
        for badge in self.badges_disponiveis:
            if (
                badge.id not in self.leitor.badges_conquistados
                and badge.capitulo <= capitulo
            ):
                # Verificar requisitos específicos
                if self._requisito_badge_atendido(badge):
                    badge.conquistado = True
                    self.leitor.badges_conquistados.append(badge.id)
                    self.leitor.xp_total += badge.xp
                    novos.append(badge)
        return novos
    
    def _requisito_badge_atendido(self, badge: Badge) -> bool:
        """Verifica se requisitos do badge foram atendidos."""
        # Implementação base — será expandida
        return (
            badge.capitulo <= len(self.leitor.capitulos_completos) + 1
            and len(self.leitor.acoes) > 0
        )
    
    def get_relatorio(self) -> dict:
        """Gera relatório completo do leitor."""
        nivel = self._calcular_nivel(self.leitor.xp_total)
        return {
            "leitor": self.leitor.leitor_id,
            "nome": self.leitor.nome,
            "nivel": nivel,
            "xp_total": self.leitor.xp_total,
            "capitulos_completos": len(self.leitor.capitulos_completos),
            "badges": len(self.leitor.badges_conquistados),
            "proximo_nivel": self._proximo_nivel(),
            "acoes_total": len(self.leitor.acoes),
        }
    
    def salvar(self, caminho: Optional[Path] = None) -> Path:
        """Salva progresso do leitor em JSON."""
        if caminho is None:
            caminho = Path(f"progresso_{self.leitor.leitor_id}.json")
        with open(caminho, "w") as f:
            json.dump({
                "leitor_id": self.leitor.leitor_id,
                "nome": self.leitor.nome,
                "email": self.leitor.email,
                "xp_total": self.leitor.xp_total,
                "capitulos_completos": self.leitor.capitulos_completos,
                "badges": self.leitor.badges_conquistados,
            }, f, indent=2, ensure_ascii=False)
        return caminho


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    """Interface de linha de comando para teste do sistema de gamificação."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Motor de Gamificação — OdontoIA Livro Imersão"
    )
    parser.add_argument("--leitor", default="demo", help="ID do leitor")
    parser.add_argument("--nome", default="Leitor Demo", help="Nome do leitor")
    parser.add_argument("--email", default="demo@odontologia-ia.com", help="Email")
    parser.add_argument("--acao", choices=list(TABELA_XP.keys()), default="ler_secao")
    parser.add_argument("--capitulo", type=int, default=1)
    parser.add_argument("--relatorio", action="store_true", help="Mostrar relatório")
    
    args = parser.parse_args()
    
    motor = MotorImersao(
        leitor_id=args.leitor,
        nome=args.nome,
        email=args.email,
    )
    
    resultado = motor.registrar_acao(
        acao=args.acao,
        capitulo=args.capitulo,
    )
    
    print(f"\n{'='*50}")
    print(f"🎮 Ação: {args.acao} | Capítulo {args.capitulo}")
    print(f"{'='*50}")
    print(f"XP Ganho:  +{resultado['xp_ganho']}")
    print(f"XP Total:  {resultado['xp_total']}")
    print(f"Nível:     {resultado['nivel_atual']['titulo']} (Nv {resultado['nivel_atual']['nivel']})")
    
    if resultado["subiu_nivel"]:
        print(f"\n{'⭐'*5} SUBIU DE NÍVEL! {'⭐'*5}")
        print(f"{resultado['nivel_anterior']['titulo']} → {resultado['nivel_atual']['titulo']}")
    
    if resultado["badges_novos"]:
        print(f"\n{'🏅'*3} NOVOS BADGES! {'🏅'*3}")
        for b in resultado["badges_novos"]:
            print(f"  {b.icone} {b.nome}: {b.descricao} (+{b.xp} XP)")
    
    if resultado["capitulo_completo"]:
        print(f"\n✅ Capítulo {args.capitulo} completo!")
    
    proximo = resultado["proximo_nivel"]
    if not proximo.get("completo"):
        print(f"\nPróximo nível: {proximo['titulo']} (Nv {proximo['nivel']})")
        print(f"Progresso: {proximo['progresso_pct']:.1f}%")
        print(f"Faltam: {proximo['xp_faltando']} XP")
    
    if args.relatorio:
        relatorio = motor.get_relatorio()
        print(f"\n{'='*50}")
        print("RELATÓRIO COMPLETO")
        print(f"{'='*50}")
        for k, v in relatorio.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
