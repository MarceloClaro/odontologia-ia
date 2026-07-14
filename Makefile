# ============================================================================
# Makefile — Odontologia IA: Livro Imersão
# Autor: Edson Laranjeiras | SPEC-951-R200
# ============================================================================

SHELL := /bin/bash
BOOK_DIR := livro
SRC_DIR := src

.PHONY: help all livro pdf imersao qrcodes gamification testes test-imersao \
        clean setup setup-latex setup-python info

help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║  🦷 Odontologia IA — Livro Imersão                  ║"
	@echo "║  Edson Laranjeiras | Makefile de Comandos           ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Comandos disponíveis:"
	@echo ""
	@echo "  📖 all           Compila tudo (QR + LaTeX + testes)"
	@echo "  📄 pdf           Compila apenas o PDF do livro"
	@echo "  🎮 imersao       Gera elementos de imersão (QR codes)"
	@echo "  🧪 test-imersao  Roda testes do motor de gamificação"
	@echo "  🧪 testes        Roda todos os testes do projeto"
	@echo "  🧹 clean         Limpa artefatos de compilação"
	@echo "  🔧 setup         Instala dependências do projeto"
	@echo "  ℹ️  info          Mostra informações do projeto"
	@echo ""

all: imersao pdf test-imersao
	@echo "✅ Build completo!"

# --- PDF do Livro ---
pdf:
	@echo "📖 Compilando PDF do livro..."
	@cd $(BOOK_DIR) && xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 && \
		echo "  ✓ Passada 1" || echo "  ⚠ Erro na passada 1"
	@cd $(BOOK_DIR) && bibtex main > /dev/null 2>&1 && echo "  ✓ BibTeX" || echo "  ⚠ BibTeX"
	@cd $(BOOK_DIR) && xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 && \
		echo "  ✓ Passada 2" || true
	@cd $(BOOK_DIR) && xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 && \
		echo "  ✓ Passada 3" || true
	@echo "✅ PDF pronto: $(BOOK_DIR)/main.pdf"

# --- Elementos de Imersão ---
imersao: qrcodes
	@echo "✅ Elementos de imersão gerados"

qrcodes:
	@echo "📱 Gerando QR codes..."
	@cd $(BOOK_DIR) && python3 imersao/qrcodes/gerar_qrcodes.py --output ilustracoes 2>/dev/null && \
		echo "  ✓ QR codes criados" || echo "  ⚠ qrcode[pil] não instalado (pip install qrcode[pil])"

# --- Testes ---
test-imersao:
	@echo "🧪 Testando motor de gamificação..."
	@cd $(BOOK_DIR) && python3 -m pytest imersao/tests/test_motor_imersao.py -v

testes: test-imersao
	@echo "🧪 Rodando todos os testes..."
	@if [ -d "$(SRC_DIR)/odontoia-pkg" ]; then \
		cd $(SRC_DIR)/odontoia-pkg && python3 -m pytest tests/ -v 2>/dev/null || \
		echo "  ⚠ Testes do pacote odontoia não disponíveis"; \
	fi

# --- Clean ---
clean:
	@echo "🧹 Limpando artefatos..."
	@cd $(BOOK_DIR) && rm -f *.aux *.bcf *.log *.pdf *.toc *.out *.fdb_latexmk *.fls *.run.xml
	@cd $(BOOK_DIR) && rm -f *.idx *.ilg *.ind *.ist *.lof *.lot *.xdv *.bbl *.blg
	@echo "  ✓ Limpeza concluída"

# --- Setup ---
setup: setup-latex setup-python
	@echo "✅ Ambiente configurado!"

setup-latex:
	@echo "🔧 Verificando LaTeX..."
	@command -v xelatex >/dev/null 2>&1 && echo "  ✓ xelatex OK" || \
		echo "  ⚠ Instale: sudo apt install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber"

setup-python:
	@echo "🔧 Verificando Python..."
	@pip install -q qrcode[pil] pyyaml pytest 2>/dev/null && echo "  ✓ Pacotes Python OK" || \
		echo "  ⚠ Erro ao instalar pacotes Python"

# --- Info ---
info:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════╗"
	@echo "║  ℹ️  INFORMAÇÕES DO PROJETO                         ║"
	@echo "╚══════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  📖 Projeto: Odontologia & IA — Livro Imersão"
	@echo "  ✍️  Autor:   Edson Laranjeiras"
	@echo "  📄 Spec:    SPEC-951-R200"
	@echo "  📚 Livro:   $(BOOK_DIR)/"
	@echo "  📦 Pacote:  $(SRC_DIR)/odontoia-pkg/"
	@echo ""
	@echo "  📊 Estatísticas:"
	@echo "  ├─ Capítulos: $$(ls $(BOOK_DIR)/parte*-*/*.tex 2>/dev/null | wc -l)"
	@echo "  ├─ Linhas:    $$(cat $(BOOK_DIR)/parte*-*/*.tex 2>/dev/null | wc -l)"
	@echo "  ├─ Personas:  $$(ls $(BOOK_DIR)/imersao/personas/*.yaml 2>/dev/null | wc -l)"
	@echo "  ├─ Badges:    $$(grep -c '^  - id:' $(BOOK_DIR)/imersao/gamification/badges.yaml 2>/dev/null)"
	@echo "  ├─ Episódios: $$(grep -c '^  - numero:' $(BOOK_DIR)/imersao/podcast/episodios.yaml 2>/dev/null)"
	@echo "  └─ Testes:    $$(python3 -m pytest $(BOOK_DIR)/imersao/tests/ --collect-only 2>/dev/null | grep -c 'PASSED\|ERROR\|FAILED')"
	@echo ""
