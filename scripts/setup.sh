#!/usr/bin/env bash
#==============================================================================
# setup.sh — Setup inicial do projeto Odontologia IA: Livro Imersão
# Autor: Edson Laranjeiras
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJ_DIR"

VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
RESET='\033[0m'

echo -e "${AZUL}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🔧 SETUP — Odontologia IA: Livro Imersão           ║"
echo "║  Edson Laranjeiras | SPEC-951-R200                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# ─── 1. Verificar dependências do sistema ───
echo -e "\n${AZUL}📦 1/4: Verificando dependências do sistema...${RESET}"

LATEX_OK=false
if command -v xelatex &>/dev/null; then
    echo -e "${VERDE}  ✓ xelatex encontrado${RESET}"
    LATEX_OK=true
else
    echo -e "${AMARELO}  ⚠ xelatex não encontrado${RESET}"
    echo "    Instale com: sudo apt install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber"
fi

PYTHON_OK=false
if command -v python3 &>/dev/null; then
    PYTHON_VER=$(python3 --version)
    echo -e "${VERDE}  ✓ $PYTHON_VER${RESET}"
    PYTHON_OK=true
else
    echo -e "${VERMELHO}  ✗ Python 3 não encontrado!${RESET}"
    echo "    Instale com: sudo apt install python3 python3-pip"
fi

# ─── 2. Instalar pacotes Python ───
echo -e "\n${AZUL}🐍 2/4: Instalando pacotes Python...${RESET}"

if [ "$PYTHON_OK" = true ]; then
    pip install --quiet -r livro/requirements.txt 2>/dev/null && \
        echo -e "${VERDE}  ✓ Dependências do livro${RESET}" || \
        echo -e "${AMARELO}  ⚠ Alguns pacotes não instalados${RESET}"

    pip install --quiet pyyaml pytest qrcode[pil] 2>/dev/null && \
        echo -e "${VERDE}  ✓ PyYAML + pytest + qrcode${RESET}" || \
        echo -e "${AMARELO}  ⚠ Alguns pacotes não instalados${RESET}"

    if [ -d "src/odontoia-pkg" ]; then
        pip install --quiet -e src/odontoia-pkg 2>/dev/null && \
            echo -e "${VERDE}  ✓ Pacote odontoia-pkg instalado${RESET}" || \
            echo -e "${AMARELO}  ⚠ odontoia-pkg não instalado${RESET}"
    fi
fi

# ─── 3. Verificar conteúdo do livro ───
echo -e "\n${AZUL}📖 3/4: Verificando conteúdo do livro...${RESET}"

CAP_ESCRITOS=$(find livro/parte* -name "*.tex" 2>/dev/null | wc -l)
LINHAS_TOTAIS=$(cat livro/parte*/**/*.tex 2>/dev/null | wc -l || cat livro/parte*/*.tex 2>/dev/null | wc -l)

echo -e "${VERDE}  ✓ $CAP_ESCRITOS arquivos de capítulo${RESET}"
echo -e "${VERDE}  ✓ ~$LINHAS_TOTAIS linhas de conteúdo${RESET}"

if [ -f "livro/main.tex" ]; then
    echo -e "${VERDE}  ✓ main.tex presente${RESET}"
fi
if ls livro/imersao/personas/*.yaml 2>/dev/null | grep -q .; then
    echo -e "${VERDE}  ✓ $(ls livro/imersao/personas/*.yaml | wc -l) personas carregadas${RESET}"
fi
if ls livro/imersao/gamification/*.py 2>/dev/null | grep -q .; then
    echo -e "${VERDE}  ✓ Motor de gamificação presente${RESET}"
fi

# ─── 4. Rodar testes ───
echo -e "\n${AZUL}🧪 4/4: Verificando testes...${RESET}"

if [ "$PYTHON_OK" = true ]; then
    if python3 -m pytest livro/imersao/tests/ -v --tb=short 2>&1 | tail -5; then
        echo -e "${VERDE}  ✓ Testes do motor de imersão passando!${RESET}"
    else
        echo -e "${AMARELO}  ⚠ Alguns testes falharam${RESET}"
    fi
fi

# ─── Resumo Final ───
echo -e "\n${VERDE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP CONCLUÍDO                                  ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  📖 Odontologia & IA — Livro Imersão                ║"
echo "║  ✍️  Edson Laranjeiras                               ║"
echo "║  📄 SPEC-951-R200                                    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${RESET}"

echo ""
echo "📋 Comandos úteis:"
echo "  make pdf         Compilar PDF"
echo "  make imersao     Gerar QR codes"
echo "  make test        Rodar testes"
echo "  make all         Fazer tudo"
echo "  make info        Status do projeto"
echo ""
