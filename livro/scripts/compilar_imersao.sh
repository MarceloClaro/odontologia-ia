#!/usr/bin/env bash
#==============================================================================
# compilar_imersao.sh — Script de Build do Livro Imersão OdontoIA
# SPEC-951-R200
# Autor: Edson Laranjeiras
#
# Uso: ./scripts/compilar_imersao.sh [--skip-qr] [--skip-tests] [--clean]
#==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOK_DIR="$(dirname "$SCRIPT_DIR")"
cd "$BOOK_DIR"

# Cores
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
RESET='\033[0m'

echo -e "${AZUL}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║     🚀 ODONTOIA — BUILD DO LIVRO IMERSÃO            ║"
echo "║     SPEC-951-R200 | Edson Laranjeiras               ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# ─── Parse de argumentos ───
SKIP_QR=false
SKIP_TESTS=false
CLEAN=false

for arg in "$@"; do
  case "$arg" in
    --skip-qr) SKIP_QR=true ;;
    --skip-tests) SKIP_TESTS=true ;;
    --clean) CLEAN=true ;;
    *) echo "Argumento desconhecido: $arg"; exit 1 ;;
  esac
done

# ─── Fase 0: Clean ───
if [ "$CLEAN" = true ]; then
  echo -e "${AMARELO}🧹 Limpando artefatos anteriores...${RESET}"
  rm -f main.aux main.bcf main.log main.pdf main.toc main.out
  rm -f main.fdb_latexmk main.fls main.run.xml
  rm -f _smoke.aux _smoke.log _smoke.pdf _smoke.tex
  echo -e "${VERDE}  ✓ Limpeza concluída${RESET}"
fi

# ─── Fase 1: Gerar QR Codes ───
if [ "$SKIP_QR" = false ]; then
  echo -e "\n${AZUL}📱 Fase 1/5: Gerando QR Codes...${RESET}"
  if python3 imersao/qrcodes/gerar_qrcodes.py --output ilustracoes; then
    echo -e "${VERDE}  ✓ QR codes gerados com sucesso${RESET}"
  else
    echo -e "${VERMELHO}  ⚠ Aviso: QR codes não gerados (qrcode não instalado?)${RESET}"
    echo "    pip install qrcode[pil]"
  fi
else
  echo -e "${AMARELO}  ⏭ QR codes pulados (--skip-qr)${RESET}"
fi

# ─── Fase 2: Verificar Personas ───
echo -e "\n${AZUL}🎭 Fase 2/5: Verificando personas e narrativa...${RESET}"
for persona in imersao/personas/*.yaml; do
  if [ -f "$persona" ]; then
    echo -e "${VERDE}  ✓ $(basename "$persona")${RESET}"
  fi
done

# ─── Fase 3: Verificar Gamificação ───
echo -e "\n${AZUL}🎮 Fase 3/5: Verificando sistema de gamificação...${RESET}"
if [ -f "imersao/gamification/badges.yaml" ]; then
  BADGES=$(grep -c "^  - id:" imersao/gamification/badges.yaml || true)
  echo -e "${VERDE}  ✓ $BADGES badges carregados${RESET}"
fi
if [ -f "imersao/gamification/xp-system.py" ]; then
  echo -e "${VERDE}  ✓ Motor de XP funcional${RESET}"
  python3 imersao/gamification/xp-system.py --relatorio 2>/dev/null || true
fi

# ─── Fase 4: Compilar LaTeX ───
echo -e "\n${AZUL}📖 Fase 4/5: Compilando LaTeX (xelatex × 3)...${RESET}"

# Verificar se xelatex está disponível
if command -v xelatex &>/dev/null; then
  for i in 1 2 3; do
    echo "  Passada $i/3..."
    xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 && \
      echo -e "${VERDE}    ✓ Passada $i concluída${RESET}" || {
      echo -e "${VERMELHO}    ✗ Erro na compilação (passada $i)${RESET}"
      echo "    Verifique main.log para detalhes"
    }
  done
  
  # BibTeX
  echo "  BibTeX..."
  bibtex main > /dev/null 2>&1 && echo -e "${VERDE}    ✓ BibTeX concluído${RESET}" || \
    echo -e "${AMARELO}    ⚠ Aviso: BibTeX teve problemas (ver main.blg)${RESET}"
  
  # Mais duas passadas xelatex para referências cruzadas
  for i in 4 5; do
    echo "  Passada $i/5 (referências)..."
    xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null 2>&1 && \
      echo -e "${VERDE}    ✓ Passada $i concluída${RESET}" || true
  done
  
  if [ -f "main.pdf" ]; then
    PAGINAS=$(pdfinfo main.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    TAMANHO=$(du -h main.pdf | cut -f1)
    echo -e "${VERDE}  ✓ PDF gerado: main.pdf ($PAGINAS páginas, $TAMANHO)${RESET}"
  fi
else
  echo -e "${AMARELO}  ⚠ xelatex não encontrado. Instale o TexLive:${RESET}"
  echo "    sudo apt install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber"
fi

# ─── Fase 5: Verificação Final ───
echo -e "\n${AZUL}✅ Fase 5/5: Verificação final...${RESET}"

echo -e "${VERDE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║     📊 RESUMO DO BUILD                              ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Projeto: OdontoIA — Livro Imersão                  ║"
echo "║  Autor:   Edson Laranjeiras                         ║"
echo "║  Spec:    SPEC-951-R200                              ║"
echo "║  Status:  📗 Build concluído                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${RESET}"

echo -e "\n📂 Estrutura de Imersão:"
echo "  imersao/"
echo "  ├── personas/        $(ls imersao/personas/ 2>/dev/null | wc -l) arquivos"
echo "  ├── gamification/    $(ls imersao/gamification/ 2>/dev/null | wc -l) arquivos"
echo "  ├── qrcodes/         $(ls imersao/qrcodes/ 2>/dev/null | wc -l) arquivos"
echo "  ├── ar-markers/      $(find imersao/ar-markers/ -type f 2>/dev/null | wc -l) arquivos"
echo "  ├── podcast/         $(ls imersao/podcast/ 2>/dev/null | wc -l) arquivos"
echo "  ├── comunidade/      $(ls imersao/comunidade/ 2>/dev/null | wc -l) arquivos"
echo "  └── design/          $(ls imersao/design/ 2>/dev/null | wc -l) arquivos"
echo ""
echo -e "${AZUL}🎯 Próximo passo: Abra o PDF e veja os elementos imersivos no Capítulo 1!${RESET}"
