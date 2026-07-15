# 📜 SPEC-999-R1 — Produção Monolítica do Livro OdontoIA

**Título:** Especificação Monolítica para Produção do Zero — Da Busca de Referências à Auditoria Final  
**Autor:** Edson Laranjeiras / marceloclaro (orquestrador)  
**Versão:** 1.0.0 | **Status:** ⚡ Template Executável  
**Normas:** NBR 6023:2018 | NBR 6024:2012 | NBR 6029 | NBR 10520:2023 | NBR 14724:2024  

---

## Índice

1. [Fase 0 — Setup do Ambiente](#fase-0--setup-do-ambiente)
2. [Fase 1 — Busca e Curadoria de Referências](#fase-1--busca-e-curadoria-de-referências)
3. [Fase 2 — Fichamento e Resenha Crítica](#fase-2--fichamento-e-resenha-crítica)
4. [Fase 3 — Esqueleto do Livro (SDD)](#fase-3--esqueleto-do-livro-sdd)
5. [Fase 4 — Produção de Conteúdo (TDD)](#fase-4--produção-de-conteúdo-tdd)
6. [Fase 5 — Camada de Imersão (SPEC-951)](#fase-5--camada-de-imersão-spec-951)
7. [Fase 6 — Compilação LaTeX](#fase-6--compilação-latex)
8. [Fase 7 — Revisão Técnica e Científica](#fase-7--revisão-técnica-e-científica)
9. [Fase 8 — Auditoria de Conformidade](#fase-8--auditoria-de-conformidade)
10. [Fase 9 — Checklist de Entrega Final](#fase-9--checklist-de-entrega-final)

---

## Fase 0 — Setup do Ambiente

### 0.1 Pré-requisitos

| Ferramenta | Versão mín. | Finalidade |
|-----------|-------------|------------|
| Python 3 | 3.12 | Scripts, testes, gamificação |
| XeLaTeX | 2024 | Compilação do PDF (fonte Noto Serif) |
| Biber | 2.20 | Processamento de referências (NBR 6023) |
| Git | 2.40 | Controle de versão |

### 0.2 Instalação

```bash
# LaTeX (Ubuntu/Debian)
sudo apt install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber \
  texlive-fonts-extra texlive-lang-portuguese

# Python
pip install qrcode[pil] pyyaml pytest

# Verificação
xelatex --version && biber --version && python3 --version
```

### 0.3 Estrutura de Diretórios

```
odontologia-ia-livro-imersao/
├── Makefile                          # Automação completa
├── livro/
│   ├── main.tex                      # Entry point LaTeX
│   ├── abntex2.cls                   # Classe ABNT customizada
│   ├── abntex2abrev.sty             # Abreviações ABNT
│   ├── abntex2cite.sty              # Citações ABNT
│   ├── config/
│   │   ├── metadados.tex             # Título, autor, ISBN
│   │   ├── pacotes.tex               # Todos os pacotes LaTeX
│   │   ├── preambulo.tex             # Configurações ABNT
│   │   ├── comandos.tex              # Comandos customizados
│   │   ├── design.tex                → Carrega abaixo
│   │   ├── design-cores.tex          # Paleta de cores
│   │   ├── design-fontes.tex         # Tipografia (Noto Serif)
│   │   ├── design-caixas.tex         # Caixas de destaque
│   │   ├── design-margem.tex         # Notas laterais
│   │   ├── design-aberturas.tex      # Abertura de capítulo
│   │   └── design-digital.tex        # Metadados PDF/A
│   ├── referencias/
│   │   ├── bibliografia.bib          # Base de referências
│   │   └── dois-pendentes.bib        # DOIs pendentes
│   ├── prefacio/                     # Elementos pré-textuais
│   ├── parte1-fundamentos/           # Capítulos 1–5
│   ├── parte2-teoria-modelos/        # Capítulos 6–11
│   ├── parte3-engenharia-sdd-tdd/   # Capítulos 12–17
│   ├── parte4-aplicacoes-avancadas/  # Capítulos 18–23
│   ├── parte5-futuro-etica/          # Capítulos 24–28
│   ├── imersao/
│   │   ├── design/                   # Comandos imersivos LaTeX
│   │   ├── personas/                 # 3 personas em YAML
│   │   ├── gamification/             # Badges, XP, sistema
│   │   ├── podcast/                  # 10 episódios
│   │   ├── qrcodes/                  # Gerador Python
│   │   ├── comunidade/               # Config do Discord
│   │   └── tests/                    # Testes pytest
│   └── imagens/                      # Figuras, diagramas
├── src/
│   ├── odontoia-pkg/                 # Pacote Python oficial
│   └── notebooks/                    # Google Colab
├── scripts/
│   └── setup.sh                      # Script de setup
├── tests/                            # Testes do ecossistema
└── docs/
    ├── ARCHITECTURE.md
    ├── ROADMAP.md
    └── GUIA-LEITOR.md
```

### 0.4 Makefile Targets

```bash
make pdf              # Compila o PDF (xelatex × 3 + biber)
make imersao          # Gera QR codes
make all              # imersao + pdf + test-imersao
make test-imersao     # Testes do motor de gamificação
make clean            # Limpa artefatos
make info             # Estatísticas do projeto
```

---

## Fase 1 — Busca e Curadoria de Referências

### 1.1 Fontes de Dados

Para cada capítulo/base temática, consultar **no mínimo 3** das seguintes bases:

| Base | URL | Cobertura |
|------|-----|-----------|
| PubMed / MEDLINE | https://pubmed.ncbi.nlm.nih.gov | Referência principal para odontologia |
| IEEE Xplore | https://ieeexplore.ieee.org | Deep learning, CNNs, modelos |
| Scopus | https://scopus.com | Indexação multidisciplinar |
| Web of Science | https://webofscience.com | Fator de impacto, citações |
| Google Scholar | https://scholar.google.com | Alcance amplo, gray literature |
| arXiv | https://arxiv.org | Pré-prints, estado da arte |
| DOAJ | https://doaj.org | Acesso aberto revisado por pares |
| CAPES Periódicos | https://periodicos.capes.gov.br | Acesso institucional brasileiro |

### 1.2 String de Busca Padrão

```
(dentistry OR dental OR oral OR odontolog*) 
AND (artificial intelligence OR deep learning OR machine learning 
     OR neural network OR convolutional OR CNN OR "computer vision")
AND (diagnosis OR classification OR segmentation OR detection)
```

Ajustar operadores e termos conforme o tema do capítulo (periodontia, câncer oral, ortodontia, etc.).

### 1.3 Critérios de Inclusão/Exclusão

**Incluir:**
- Artigos com DOI verificável
- Revisões sistemáticas com PRISMA
- Estudos com validação externa
- Métricas reportadas (AUC, sensibilidade, especificidade, F1, Dice)
- Código/dataset público (reprodutibilidade)

**Excluir:**
- Artigos sem DOI
- Apenas abstract (exceto clássicos)
- Estudos sem métricas quantitativas
- Publicações em fontes não revisadas por pares (exceto contexto histórico)
- Duplicatas

### 1.4 Metadados por Referência

Para CADA artigo selecionado, coletar:

| Campo | Obrigatório | Formato |
|-------|-------------|---------|
| Chave BibTeX | ✅ | `ODT-NNN` ou `DL-ODT-NNN` |
| DOI | ✅ | `10.xxxx/xxxxx` |
| Título completo | ✅ | Conforme artigo |
| Autores | ✅ | Sobrenome, Iniciais |
| Ano | ✅ | 2024 |
| Periódico | ✅ | Nome completo |
| Volume/Número/Páginas | ✅ | Conforme NBR 6023 |
| URL do PDF | ✅ | Link direto ou DOI |
| Palavras-chave | ✅ | 3–5 do artigo |
| Métricas reportadas | ✅ | AUC, sensibilidade, etc. |

### 1.5 Nomenclatura de Chaves BibTeX

```
ODT-NNN        → Odontologia geral (ex: ODT-001, ODT-052)
DL-ODT-NNN     → Deep Learning específico (ex: DL-ODT-012)
ronneberger2015u → Artigos clássicos por autor+ano+título
```

### 1.6 Verificação de DOIs

Todos os DOIs DEVEM ser verificados manualmente:

```bash
curl -sI "https://doi.org/10.xxxx/xxxxx" | head -1
# Deve retornar: HTTP/2 200 ou 302 (não 404)
```

---

## Fase 2 — Fichamento e Resenha Crítica

### 2.1 Template de Fichamento

Para cada referência selecionada, produzir um fichamento no seguinte formato:

```markdown
## Fichamento NNN — Autor (ANO)

**DOI:** 10.xxxx/xxxxx  
**Chave:** ODT-NNN  
**Periódico:** Nome do Periódico  
**Qualis:** A1/A2/B1  

### 2.1.1 Objetivo do Estudo
[1 parágrafo — o que os autores se propuseram a fazer]

### 2.1.2 Metodologia
- **Dataset:** N, origem, modalidade de imagem
- **Arquitetura:** Nome do modelo, parâmetros
- **Validação:** Interna/externa, k-fold, holdout
- **Métricas:** AUC, sensibilidade, especificidade, F1, Dice

### 2.1.3 Principais Resultados
- [Resultado quantitativo 1]
- [Resultado quantitativo 2]
- [Resultado qualitativo]

### 2.1.4 Limitações Declaradas
- [Limitação 1]
- [Limitação 2]

### 2.1.5 Relevância para o Livro
- [Conexão com o tema do capítulo]
- [Como será citado]

### 2.1.6 Resenha Crítica (3–5 linhas)
[Análise crítica da qualidade metodológica, impacto e limitações]

### 2.1.7 Citação ABNT
[Formatação NBR 6023 pronta para uso]
```

### 2.2 Organização dos Fichamentos

```
fichamentos/
├── parte1-fundamentos/
│   ├── fichamento-ODT-001-khanagar2021.md
│   ├── fichamento-ODT-002-brickley1998.md
│   └── ...
├── parte2-teoria-modelos/
│   └── ...
└── ...
```

### 2.3 Classes de Referência (Categorização)

| Classe | Descrição |
|--------|-----------|
| **🔴 Seminal** | Marco fundador do campo (Brickley 1998, Schleyer 2001) |
| **🟡 Suporte** | Fornece evidência para um ponto específico |
| **🟢 Contraste** | Apresenta visão divergente ou limitação |
| **⚪ Contexto** | Informação histórica ou metodológica |

---

## Fase 3 — Esqueleto do Livro (SDD)

### 3.1 Estrutura Geral

```
Pré-textuais (não numerados)
  ├── Folha de rosto
  ├── Ficha catalográfica
  ├── Dedicatória
  ├── Agradecimentos
  ├── Epígrafe
  ├── Resumo (PT/EN)
  ├── Lista de figuras
  ├── Lista de tabelas
  └── Sumário

Parte I — Fundamentos (Caps 1–5)
Parte II — Teoria e Modelos (Caps 6–11)
Parte III — Engenharia SDD/TDD (Caps 12–17)
Parte IV — Aplicações Avançadas (Caps 18–23)
Parte V — Futuro e Ética (Caps 24–28)

Pós-textuais
  ├── Referências (NBR 6023)
  ├── Glossário
  ├── Apêndices
  └── Índice remissivo
```

### 3.2 Template de Capítulo SDD

CADA capítulo DEVE seguir esta especificação:

```latex
%==============================================================================
% CAPÍTULO N — TÍTULO
% Autor: Edson Laranjeiras
%==============================================================================

\chapter{Título do Capítulo}
\label{cap:nome-curto}

% --- Abertura ---
\aberturacap
  {Epígrafe}
  {Autor da epígrafe}
  {Nível 0-5}{Tempo estimado}{Pré-requisitos}
  {\item Objetivo 1
   \item Objetivo 2
   \item Objetivo 3}

\colab{https://colab.research.google.com/...}

% --- Seção Primária ---
\section{Objetivos de Aprendizagem}

\subsection{Objetivo 1 — Título Descritivo}
Texto introdutório do objetivo...

\subsection{Objetivo 2 — Título Descritivo}
...

% --- Conteúdo Principal ---
\section{Fundamentação Teórica}
\subsection{...}
\subsubsection{...}  % quando necessário (1.1.1.1)

% --- Seções do corpo ---
\section{...}

% --- Prática/Laboratório ---
\section{Laboratório em Python e Google Colab}
\begin{pratica}
\spec{...}
\codigo{codigos/capNN/...}
\teste{...}
\end{pratica}

% --- Síntese ---
\section{Síntese do Capítulo}

% --- Imersão SPEC-951 ---
\personamoment{...}
\badgealert{...}
\gamificationbox{...}
\barraprogresso{...}
```

### 3.3 Critérios de Aceitação por Capítulo

| Critério | Obrigatório | Verificação |
|----------|-------------|-------------|
| Epígrafe com autoria | ✅ | Inspeção |
| Nível de dificuldade (0–5) | ✅ | Inspeção |
| Tempo estimado de leitura | ✅ | Inspeção |
| Objetivos de aprendizagem | ✅ | `\subsection` por objetivo |
| Mínimo de 5 referências | ✅ | Contagem BibTeX |
| Pelo menos 1 figura/tabela | ✅ | Inspeção |
| Laboratório prático SDD+TDD | ✅ (caps 1–27) | `\pratica` + `\spec` + `\codigo` + `\teste` |
| Síntese final | ✅ | `\section{Síntese}` |
| Elementos de imersão | ✅ | `\personamoment`, `\gamificationbox` |
| DOIs verificáveis | ✅ (≥80%) | Script de verificação |
| Fonte `\capitular` | ✅ (cap. 1 apenas) | `\lettrine` |

---

## Fase 4 — Produção de Conteúdo (TDD)

### 4.1 Ciclo RED → GREEN → REFACTOR

Para CADA laboratório prático:

```python
# RED: escrever o teste que FALHA
def test_classificador_carie():
    modelo = ClassificadorCarie()
    resultado = modelo.prever(imagem_teste)
    assert resultado['acuracia'] > 0.85  # ainda vai falhar

# GREEN: implementar o código MÍNIMO que passa
class ClassificadorCarie:
    def prever(self, imagem):
        # implementacao minima
        return {'acuracia': 0.87}

# REFACTOR: melhorar sem quebrar os testes
class ClassificadorCarie:
    def __init__(self):
        self.modelo = CarregarModeloPreTreinado()
    def prever(self, imagem):
        return {'acuracia': self.modelo.avaliar(imagem)}
```

### 4.2 Estrutura de Código por Capítulo

```
livro/
└── codigos/
    └── cap01/
        ├── linha_tempo_ia_odontologia.py   # Código do laboratório
        └── test_cap01.py                    # Testes TDD
```

### 4.3 Regras de Citação no Texto

| Tipo | Comando LaTeX | Exemplo |
|------|--------------|---------|
| Citação direta curta | `\cite{chave}` | ...conforme \cite{ODT-001}. |
| Citação direta longa | `\citacaoativa{chave}{doi}{texto}` | Bloco recuado (NBR 10520) |
| Citação de autor | `\citeonline{chave}` | \citeonline{ODT-002} demonstrou... |
| Citação com DOI na margem | `\citdoi{chave}{doi}` | Texto\citdoi{ODT-003}{10.xxxx/xxxxx} |
| Nota explicativa | `\notaexplicativa{texto}` | Rodapé autoral |
| Nota lateral | `\notalateral{texto}` | Margem externa |
| Figura de artigo real | `\artigofig{caminho}{chave}{legenda}` | Figura com DOI |
| Referência indireta | `\cite{chave1, chave2}` | Vários autores |

### 4.4 Checklist de Citação

- [ ] Toda citação direta tem `""` ou `\citacaoativa` com DOI
- [ ] Toda afirmação quantitativa tem referência
- [ ] Toda figura de artigo tem `\artigofig` com DOI e legenda
- [ ] Máximo de 1 citação longa (bloco) por subseção
- [ ] Mínimo de 1 citação por subseção com conteúdo técnico
- [ ] Todas as chaves BibTeX existem no `.bib`

---

## Fase 5 — Camada de Imersão (SPEC-951)

### 5.1 Componentes da Imersão

| Componente | Arquivo | Formato |
|-----------|---------|---------|
| 3 Personas | `imersao/personas/*.yaml` | YAML |
| 14 Badges | `imersao/gamification/badges.yaml` | YAML |
| 8 Níveis XP | `imersao/gamification/xp_system.py` | Python |
| 10 Episódios Podcast | `imersao/podcast/episodios.yaml` | YAML |
| QR Codes (5 tipos) | `imersao/qrcodes/gerar_qrcodes.py` | Python |
| 12 Comandos LaTeX | `imersao/design/design-imersao.tex` | LaTeX |
| Testes (pytest) | `imersao/tests/test_motor_imersao.py` | Python |
| Comunidade | `imersao/comunidade/config.yaml` | YAML |

### 5.2 Comandos LaTeX de Imersão

| Comando | Finalidade |
|---------|-----------|
| `\aberturacap{epígrafe}{autor}{nível}{tempo}{pré-req}{objetivos}` | Abertura de capítulo |
| `\personamoment[nome]{texto}` | Momento narrativo da persona |
| `\mentorbox{texto}` | Fala do mentor |
| `\badgealert{nome}{descrição}{requisito}{recompensa}` | Alerta de badge |
| `\desafio{título}{descrição}{entrega}` | Desafio do capítulo |
| `\gamificationbox{conteúdo}` | Caixa de progresso |
| `\qrchapter{capítulo}{título}{url_video}{url_colab}` | QR codes por capítulo |
| `\barraprogresso{cap}{nivel}{xp}` | Barra de progresso |
| `\trilhanivel{nível}` | Pílulas de nível |
| `\colab{url}` | Link para Google Colab |
| `\nivelzero` a `\nivelcinco` | Marcadores de nível |

### 5.3 Motor de Gamificação

```python
# xp_system.py — Engine central
class MotorImersao:
    NIVEL_LIMIAR = {0: 0, 1: 2000, 2: 5000, 3: 10000, 4: 20000, 5: 40000, 
                    6: 70000, 7: 100000}
    
    def calcular_nivel(self, xp_total: int) -> int:
        for nivel, limiar in sorted(self.NIVEL_LIMIAR.items(), reverse=True):
            if xp_total >= limiar:
                return nivel
        return 0
    
    def badge_desbloqueado(self, xp_total: int, badge_requisito_xp: int) -> bool:
        return xp_total >= badge_requisito_xp
```

### 5.4 Testes de Imersão

```bash
# Executar
cd livro && python3 -m pytest imersao/tests/test_motor_imersao.py -v

# Deve retornar 19 testes passando
```

---

## Fase 6 — Compilação LaTeX

### 6.1 Pipeline de Compilação

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ xelatex  │───▶│  biber   │───▶│ xelatex  │───▶│ xelatex  │
│ Passada 1│    │ .bcf→.bbl│    │ Passada 2│    │ Passada 3│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
  .aux + .bcf     .bbl + .blg    .toc + .aux     PDF final
```

### 6.2 Comandos Manuais

```bash
# A partir da pasta livro/
xelatex -interaction=nonstopmode -halt-on-error main.tex  # Passada 1
biber main                                                  # Referências
xelatex -interaction=nonstopmode -halt-on-error main.tex  # Passada 2
xelatex -interaction=nonstopmode -halt-on-error main.tex  # Passada 3
```

### 6.3 Ordem dos Elementos no main.tex

```latex
\documentclass[12pt,a4paper,twoside,openright,chapter=TITLE,section=TITLE]{abntex2}

% === PRÉ-TEXTUAIS (não numerados) ===
\input{config/preambulo}           % Carrega tudo
\input{prefacio/01-folha-rosto}
\input{prefacio/02-ficha-catalografica}
\input{prefacio/03-dedicatoria}
\input{prefacio/04-agradecimentos}
\input{prefacio/05-epigrafe}
\input{prefacio/06-resumo}
\input{prefacio/07-abstract}
\input{prefacio/08-lista-figuras}
\input{prefacio/09-lista-tabelas}
\input{prefacio/10-lista-siglas}
\input{prefacio/11-sumario}

% === PARTES TEXTUAIS (numerados) ===
\textual

\input{parte1-fundamentos/abertura-parte1}  % Parte I
\include{parte1-fundamentos/01-historia-ia-odontologia}
\include{parte1-fundamentos/02-evidencia-revisoes}
...                                          % Capítulos 1–28

% === PÓS-TEXTUAIS ===
\postextual
\bibliography{referencias/bibliografia,referencias/dois-pendentes}
\input{pos-textual/glossario}
\printindex
```

### 6.4 Formatação ABNT (preambulo.tex)

```latex
% NBR 6024:2012 — Hierarquia de seções
\renewcommand{\ABNTEXchapterfont}{\bfseries}           % Primária: CAP + NEG
\renewcommand{\ABNTEXsectionfont}{\bfseries}            % Secundária: CAP + NEG
\renewcommand{\ABNTEXsubsectionfont}{\bfseries}          % Terciária: 1ª maiúsc + NEG
\renewcommand{\ABNTEXsubsubsectionfont}{\itshape\mdseries} % Quaternária: itálico

% NBR 14724:2024 — Margens
\usepackage[a4paper, left=3cm, top=3cm, right=2cm, bottom=2cm]{geometry}

% NBR 14724:2024 — Espaçamento 1,5
\OnehalfSpacing

% NBR 14724:2024 — Notas de rodapé
\renewcommand{\footnoterule}{\kern-3pt\noindent\rule{5cm}{0.4pt}\kern2.6pt}

% NBR 6023:2018 — Referências (biblatex)
\usepackage[backend=biber, style=abnt-numeric, giveninits=true]{biblatex}
```

---

## Fase 7 — Revisão Técnica e Científica

### 7.1 Roteiro de Revisão por Capítulo

```
📘 Capítulo [N]: [Título]
─────────────────────────────────────────────

□ 1. ESTRUTURA
   □ \aberturacap completo (epígrafe, autor, nível, tempo, pré-req, objetivos)
   □ \section{Objetivos de Aprendizagem} com \subsection por objetivo
   □ Mínimo 5 seções \section{} no corpo
   □ \section{Síntese do Capítulo} ao final
   □ Elementos de imersão presentes

□ 2. CONTEÚDO
   □ Toda afirmação quantitativa tem citação
   □ Máximo 1 citação longa por subseção
   □ Mínimo 1 figura ou tabela
   □ Código prático testado com TDD
   □ TODOS os DOIs funcionam (verificar via curl)

□ 3. FORMATAÇÃO ABNT
   □ Hierarquia de títulos: CAP → CAP+NEG → 1ª maiúsc+NEG → itálico
   □ Citações: \cite{} ou \citacaoativa conforme NBR 10520:2023
   □ Margens 3/2/3/2
   □ Espaçamento 1,5
   □ Fonte Noto Serif (corpo) / Liberation Serif (pré/pós-textual)

□ 4. REFERÊNCIAS
   □ Todas as chaves \cite{} existem no .bib
   □ Nenhuma chave não citada no .bib
   □ DOIs verificados
   □ Formatação NBR 6023:2018 consistente

□ 5. IMERSÃO
   □ \personamoment presente
   □ \gamificationbox presente com XP
   □ \barraprogresso presente
   □ \qrchapter presente
   □ Nível de dificuldade correto
```

### 7.2 Scripts de Verificação Automática

```bash
# 1. Verificar DOIs
for doi in $(grep -roh '10\.[0-9]\{4,\}/[a-zA-Z0-9._/-]\+' livro/); do
    status=$(curl -sI "https://doi.org/$doi" | head -1)
    echo "$doi → $status"
done

# 2. Verificar chaves BibTeX citadas vs. existentes
grep -oh '\\cite{[^}]*}' livro/parte*/*.tex | sort -u > citadas.txt
grep -oh '@.*{.*,' livro/referencias/*.bib | sed 's/@.*{//;s/,//' | sort -u > existentes.txt
diff citadas.txt existentes.txt

# 3. Verificar \section sem conteúdo
grep -A1 '\\section{' livro/parte*/*.tex | grep -B1 '^$'

# 4. Contar referências por capítulo
for f in livro/parte*/*.tex; do
    echo "$(basename $f): $(grep -c '\\cite{' $f) citações"
done

# 5. Verificar erros de compilação
grep -c '^!' livro/main.log
```

---

## Fase 8 — Auditoria de Conformidade

### 8.1 Gates de Qualidade

| Gate | Critério | Ação se Falhar |
|------|----------|----------------|
| **G1 — SDD** | Capítulo tem spec prévia | Bloqueia escrita |
| **G2 — TDD** | Testes passam (RED→GREEN) | Bloqueia merge |
| **G3 — DOIs** | ≥80% dos DOIs verificados | Sinaliza alerta |
| **G4 — Referências** | 100% das chaves existem no .bib | Bloqueia compilação |
| **G5 — Compilação** | PDF gera com 0 erros | Bloqueia entrega |
| **G6 — Formatação** | ABNT conforme checklist | Bloqueia release |
| **G7 — Imersão** | 19 testes pytest passando | Bloqueia release |
| **G8 — Auditoria GitHub** | Nível G3 de confiabilidade | Sinaliza alerta |

### 8.2 Relatório de Auditoria

```markdown
# Auditoria Final — OdontoIA Livro Imersão
## Data: [data] | Versão: [hash git]

### Resumo
- Capítulos: 28/28 completos
- Páginas: [N]
- Erros LaTeX: [N]
- Testes imersão: [N]/19 passando
- DOIs verificados: [N]% (mín 80%)
- Referências: [N] citadas, [N] existentes no .bib

### Gates
┌──────┬──────────────────────────────┬────────┬──────────┐
│ Gate │ Critério                     │ Status │ Evidência│
├──────┼──────────────────────────────┼────────┼──────────┤
│ G1   │ SDD — spec prévia            │   ✅   │ specs/   │
│ G2   │ TDD — testes GREEN           │   ✅   │ make test│
│ G3   │ DOIs ≥80%                    │   ✅   │ curl     │
│ G4   │ Chaves BibTeX                │   ✅   │ diff     │
│ G5   │ PDF 0 erros                  │   ✅   │ make pdf │
│ G6   │ ABNT NBR 6024/14724          │   ✅   │ checklist│
│ G7   │ Imersão 19/19                │   ✅   │ pytest   │
│ G8   │ GitHub G3                    │   ✅   │ auditoria│
└──────┴──────────────────────────────┴────────┴──────────┘

### Pendências
- [ ] Pendência 1
- [ ] Pendência 2
```

---

## Fase 9 — Checklist de Entrega Final

### 9.1 Artefatos

- [ ] `OdontoIA-Livro-Imersao.pdf` — PDF final compilado (738+ páginas)
- [ ] `livro/main.pdf` — PDF espelho
- [ ] `fichamentos/` — Pasta com N fichamentos
- [ ] `referencias/bibliografia.bib` — Base completa
- [ ] `codigos/capNN/*.py` — Códigos de todos os laboratórios
- [ ] `docs/ARCHITECTURE.md` — Arquitetura atualizada
- [ ] `docs/ROADMAP.md` — Roadmap atualizado
- [ ] `docs/GUIA-LEITOR.md` — Guia do leitor
- [ ] `Makefile` — Comandos funcionando

### 9.2 Verificações Finais

```bash
echo "═══ AUDITORIA FINAL ═══"

# 1. Compilação limpa
make clean && make pdf
echo "Erros: $(grep -c '^!' livro/main.log)"

# 2. Páginas
echo "Páginas: $(pdfinfo livro/main.pdf | grep Pages | awk '{print $2}')"

# 3. Testes
make test-imersao | grep -c 'PASSED'

# 4. Capítulos
echo "Capítulos: $(ls livro/parte*/*.tex | wc -l)"

# 5. Referências
echo "Refs: $(grep -c '@' livro/referencias/bibliografia.bib)"

# 6. Citações
echo "Citações: $(grep -roh '\\cite{' livro/parte*/*.tex | wc -l)"

# 7. Linhas totais
echo "Linhas: $(cat livro/parte*/*.tex | wc -l)"
```

### 9.3 Liberação

Após aprovação em todos os 8 gates:

```bash
# Tag da versão
git tag -a v1.0.0 -m "OdontoIA Livro Imersão — 738 páginas, 0 erros"
git push origin v1.0.0

# Release no GitHub
gh release create v1.0.0 \
  OdontoIA-Livro-Imersao.pdf \
  --title "OdontoIA — Livro Imersão v1.0.0" \
  --notes "Primeira edição completa. 28 capítulos, 738 páginas."
```

---

## Apêndice A — Padronização ABNT Aplicada

| Elemento | Norma | Configuração |
|----------|-------|-------------|
| Estrutura | NBR 14724:2024 | Pré-textual, textual, pós-textual |
| Margens | NBR 14724:2024 | 3cm (esq/sup), 2cm (dir/inf) |
| Fonte | NBR 14724:2024 | 12pt, Noto Serif (corpo) |
| Espaçamento | NBR 14724:2024 | 1,5 entrelinhas |
| Numeração | NBR 6024:2012 | 1 → 1.1 → 1.1.1 → 1.1.1.1 |
| Primária | NBR 6024:2012 | MAIÚSCULAS + NEGRITO |
| Secundária | NBR 6024:2012 | MAIÚSCULAS + NEGRITO |
| Terciária | NBR 6024:2012 | 1ª maiúscula + NEGRITO |
| Quaternária | NBR 6024:2012 | 1ª maiúscula + ITÁLICO |
| Citações | NBR 10520:2023 | Curta: aspas; Longa: bloco 4cm |
| Referências | NBR 6023:2018 | biblatex + abnt-numeric |
| Notas de rodapé | NBR 14724:2024 | Fonte 10pt, filete 5cm |
| Legendas | NBR 14724:2024 | Justificadas, rótulo negrito |
| Sumário | NBR 6027:2012 | Hierarquia idêntica ao texto |

## Apêndice B — Diagrama de Fluxo da Produção

```
INÍCIO
  │
  ▼
┌─────────────────────────────────────────┐
│ FASE 0: Setup do Ambiente               │
│ ├─ Instalar LaTeX, Python, Git          │
│ ├─ Clonar template do projeto           │
│ └─ Verificar dependências (make setup)  │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 1: Busca e Curadoria               │
│ ├─ Definir strings de busca por tema    │
│ ├─ Consultar PubMed, IEEE, Scopus       │
│ ├─ Aplicar critérios de inclusão        │
│ └─ Coletar metadados (DOI, autores)     │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 2: Fichamento                      │
│ ├─ Criar fichamento por referência      │
│ ├─ Categorizar (seminal/suporte/contraste)│
│ ├─ Escrever resenha crítica             │
│ └─ Inserir no .bib com chave ODT-NNN    │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 3: Esqueleto SDD                   │
│ ├─ Criar capítulo com template padrão   │
│ ├─ Definir seções e subseções           │
│ ├─ Alocar referências por seção         │
│ └─ Aprovar spec (gate G1)               │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 4: Conteúdo TDD                    │
│ ├─ Escrever testes (RED)                │
│ ├─ Implementar código (GREEN)           │
│ ├─ Escrever texto com citações          │
│ └─ Refatorar (REFACTOR)                 │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 5: Camada de Imersão               │
│ ├─ Adicionar \personamoment             │
│ ├─ Adicionar \gamificationbox           │
│ ├─ Adicionar \qrchapter, \badgealert    │
│ └─ Rodar testes (gate G7)               │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 6: Compilação LaTeX                │
│ ├─ xelatex (passada 1)                  │
│ ├─ biber (referências)                  │
│ ├─ xelatex (passada 2 e 3)             │
│ └─ Verificar erros (gate G5)            │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 7: Revisão Técnica                 │
│ ├─ Roteiro por capítulo                 │
│ ├─ Scripts de verificação               │
│ ├─ DOIs, chaves, formatação             │
│ └─ Aprovar gates G3, G4, G6             │
└────────────────┬────────────────────────┘
                 ▼
┌─────────────────────────────────────────┐
│ FASE 8: Auditoria Final                 │
│ ├─ Todos os 8 gates                     │
│ ├─ Relatório de auditoria               │
│ ├─ Tag e release no GitHub              │
│ └─ ✅ LIVRO PRODUZIDO                   │
└─────────────────────────────────────────┘
```

---

**Fim da SPEC-999-R1** — Esta especificação é auto-contida e executável. Cada fase pode ser delegada a agentes especializados do ecossistema OpenCode via protocolo A2A/Blackboard.
