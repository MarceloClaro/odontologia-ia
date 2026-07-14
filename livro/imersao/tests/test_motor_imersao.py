#!/usr/bin/env python3
"""
Testes do Motor de Imersão — OdontoIA: Livro Imersão
SPEC-951-R200
Autor: Edson Laranjeiras
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "gamification"))
from xp_system import MotorImersao, TABELA_XP, NIVEIS
import pytest


class TestMotorImersao:
    """Testes do motor de gamificação do Livro Imersão."""

    @pytest.fixture
    def motor(self):
        """Fixture: motor de imersão configurado."""
        return MotorImersao(
            leitor_id="test-001",
            nome="Leitor Teste",
            email="teste@teste.com",
        )

    def test_inicializacao_com_valores_padrao(self, motor):
        """Testa se o motor inicializa com valores corretos."""
        assert motor.leitor.xp_total == 0
        assert motor.leitor.capitulos_completos == []
        assert motor.leitor.badges_conquistados == []
        assert motor.leitor.leitor_id == "test-001"

    def test_registrar_acao_ler_secao(self, motor):
        """Testa registro de ação de leitura."""
        resultado = motor.registrar_acao("ler_secao", capitulo=1)
        assert resultado["status"] == "ok"
        assert resultado["xp_ganho"] == TABELA_XP["ler_secao"]
        assert resultado["xp_total"] == TABELA_XP["ler_secao"]

    def test_registrar_acao_completar_capitulo(self, motor):
        """Testa registro de capítulo completo."""
        resultado = motor.registrar_acao("completar_capitulo", capitulo=1)
        assert resultado["capitulo_completo"] is True
        assert 1 in motor.leitor.capitulos_completos

    def test_capitulo_nao_duplicado(self, motor):
        """Testa que capítulo não é adicionado duas vezes."""
        motor.registrar_acao("completar_capitulo", capitulo=1)
        resultado = motor.registrar_acao("completar_capitulo", capitulo=1)
        assert resultado["capitulo_completo"] is False
        assert len(motor.leitor.capitulos_completos) == 1

    def test_calculo_nivel_inicial(self, motor):
        """Testa cálculo de nível inicial."""
        nivel = motor._calcular_nivel(0)
        assert nivel["nivel"] == 1
        assert nivel["titulo"] == "Curioso Digital"

    def test_calculo_nivel_avancado(self, motor):
        """Testa cálculo de nível avançado."""
        nivel = motor._calcular_nivel(15000)
        assert nivel["nivel"] >= 4

    def test_subida_de_nivel(self, motor):
        """Testa se a subida de nível é detectada."""
        # Adicionar XP suficiente para subir de nível
        motor.leitor.xp_total = 2500
        resultado = motor.registrar_acao("completar_capitulo", capitulo=1)
        # Verificar que subiu (deve ter passado de 2000 para 3500, nível 2+)
        assert "nivel_atual" in resultado

    def test_todas_acoes_tem_xp_positivo(self):
        """Testa se todas as ações na tabela têm XP positivo."""
        for acao, xp in TABELA_XP.items():
            assert xp > 0, f"Ação {acao} tem XP <= 0"

    def test_niveis_crescentes(self):
        """Testa se os níveis estão em ordem crescente de XP."""
        xps = [n["xp_necessario"] for n in NIVEIS]
        for i in range(1, len(xps)):
            assert xps[i] > xps[i - 1], (
                f"Nível {i+1} tem XP menor que o nível {i}"
            )

    def test_badges_carregados(self, motor):
        """Testa se badges são carregados do YAML."""
        assert len(motor.badges_disponiveis) > 0
        badge_1 = motor.badges_disponiveis[0]
        assert hasattr(badge_1, "id")
        assert hasattr(badge_1, "nome")
        assert hasattr(badge_1, "xp")

    def test_proximo_nivel_informado(self, motor):
        """Testa se próximo nível é informado corretamente."""
        proximo = motor._proximo_nivel()
        assert "titulo" in proximo
        assert "xp_necessario" in proximo
        assert "xp_faltando" in proximo

    def test_relatorio_completo(self, motor):
        """Testa geração de relatório completo."""
        motor.registrar_acao("ler_secao", capitulo=1)
        motor.registrar_acao("fazer_pratica", capitulo=1)
        relatorio = motor.get_relatorio()
        assert relatorio["leitor"] == "test-001"
        assert relatorio["xp_total"] > 0
        assert relatorio["acoes_total"] > 0

    def test_salvar_progresso(self, motor, tmp_path):
        """Testa persistência do progresso."""
        motor.registrar_acao("completar_capitulo", capitulo=1)
        caminho = motor.salvar(tmp_path / "progresso_test.json")
        assert caminho.exists()
        conteudo = caminho.read_text()
        assert "test-001" in conteudo
        assert "capitulos_completos" in conteudo

    def test_xp_diario_limite(self, motor):
        """Testa limite diário de XP."""
        # Adicionar XP até o limite
        motor.leitor.xp_diario = 4900
        resultado = motor.registrar_acao("completar_capitulo", capitulo=1)
        # XP ganho deve ser limitado a 100 (para não exceder 5000)
        assert resultado["xp_ganho"] <= 100

    @pytest.mark.parametrize("acao,cap,esperado", [
        ("ler_secao", 1, TABELA_XP["ler_secao"]),
        ("fazer_pratica", 2, TABELA_XP["fazer_pratica"]),
        ("passar_testes_tdd", 3, TABELA_XP["passar_testes_tdd"]),
        ("responder_desafio", 4, TABELA_XP["responder_desafio"]),
        ("completar_capitulo", 5, TABELA_XP["completar_capitulo"]),
    ])
    def test_varias_acoes(self, motor, acao, cap, esperado):
        """Testa diferentes tipos de ação com parametrização."""
        resultado = motor.registrar_acao(acao, capitulo=cap)
        assert resultado["xp_ganho"] == esperado


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
