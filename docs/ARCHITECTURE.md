# 🏗️ Arquitetura do Projeto — Odontologia IA: Livro Imersão

**Autor:** Edson Laranjeiras | **Spec:** SPEC-951-R200  
**Versão:** 2.0.0 | **Data:** 2026-07-14

---

## 1. Visão Geral da Arquitetura

```
┌──────────────────────────────────────────────────────────────────┐
│                    ODONTOIA — LIVRO IMERSÃO                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  📖 CAMADA DE CONTEÚDO (SPEC-950)                      │     │
│  │  LaTeX + ABNT + 28 capítulos + 500 laudas              │     │
│  └────────────┬───────────────────────────────────────────┘     │
│               │  \input{}                                     │
│  ┌────────────▼───────────────────────────────────────────┐     │
│  │  🎭 CAMADA DE IMERSÃO (SPEC-951)                       │     │
│  │  design-imersao.tex + comandos LaTeX personalizados    │     │
│  └────────────┬───────────────────────────────────────────┘     │
│               │                                               │
│  ┌────────────▼──────────┐  ┌────────────────────────────┐   │
│  │  🎮 Gamificação       │  │  📱 QR Codes              │   │
│  │  ├─ xp_system.py      │  │  ├─ gerador Python        │   │
│  │  ├─ badges.yaml       │  │  ├─ 5 tipos por capítulo  │   │
│  │  └─ testes pytest     │  │  └─ manifest JSON         │   │
│  └───────────────────────┘  └────────────────────────────┘   │
│                                                               │
│  ┌───────────────────────┐  ┌────────────────────────────┐   │
│  │  🎭 Personas          │  │  🎧 Podcast               │   │
│  │  ├─ Dra. Marina       │  │  ├─ 10 episódios          │   │
│  │  ├─ Seu Raimundo      │  │  ├─ Roteiros .yaml        │   │
│  │  └─ Prof. Lucas       │  │  └─ Integração XP         │   │
│  └───────────────────────┘  └────────────────────────────┘   │
│                                                               │
│  ┌───────────────────────┐  ┌────────────────────────────┐   │
│  │  🧠 Código Python     │  │  🌐 Comunidade            │   │
│  │  ├─ odontoia-pkg      │  │  ├─ Discord               │   │
│  │  ├─ Notebooks Colab   │  │  ├─ GitHub Discussions    │   │
│  │  └─ Scripts           │  │  └─ Eventos semanais      │   │
│  └───────────────────────┘  └────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Ecossistema de Tecnologias

### 2.1 Stack Principal

| Camada | Tecnologia | Função |
|--------|-----------|--------|
| **Texto** | LaTeX (abntex2 + xelatex) | Formatação do livro conforme NBR 6029/14724 |
| **Design** | TikZ + tcolorbox + xcolor | Figuras vetoriais, boxes imersivos, cores |
| **Código** | Python 3.14+ | Motor de gamificação, scripts, notebooks |
| **Testes** | pytest 9.x | TDD do motor de imersão e pacotes |
| **Build** | Makefile + Bash | Pipeline de compilação unificada |
| **Dados** | YAML + JSON | Personas, badges, episódios, manifestos |

### 2.2 Pacote Python (odontoia-pkg)

```
src/odontoia-pkg/
├── pyproject.toml
├── setup.py
├── requirements.txt
├── src/odontoia/
│   ├── __init__.py
│   ├── imersao/           # Motor de imersão (gamificação)
│   │   ├── xp_system.py
│   │   └── ...
│   ├── modelos/           # Modelos de ML
│   ├── processamento/     # Pré-processamento de imagens
│   └── utils/             # Utilitários
├── tests/
│   ├── test_imersao.py
│   └── ...
└── notebooks/             # Templates Colab
```

---

## 3. Fluxo de Dados

### 3.1 Pipeline de Compilação

```
[Fonte LaTeX] → xelatex (3x) → [PDF do Livro]
                    ↕
           [bibtex → referências]
                    ↕
           [makeindex → glossário + índice]
                    ↕
           [design-imersao.tex → elementos visuais]
                    ↕
           [QR codes → ilustracoes/]
```

### 3.2 Sistema de Gamificação

```
[Leitor] → ação (ler, praticar, testar, desafio)
    ↓
[MotorImersao.registrar_acao()]
    ├── Calcula XP (TABELA_XP)
    ├── Verifica nível (NIVEIS)
    ├── Checa badges (badges.yaml)
    └── Retorna resultado + badges + progresso
```

---

## 4. Estrutura de Diretórios

```
odontologia-ia-livro-imersao/
│
├── 📁 livro/                         ← Conteúdo do livro (links p/ ecossistema)
│   ├── main.tex                     ← Arquivo principal LaTeX
│   ├── Makefile                     ← Compilação do livro
│   ├── config/                      ← Configurações LaTeX
│   ├── parte1-fundamentos/          ← Capítulos 1-5
│   ├── parte2-teoria-modelos/       ← Capítulos 6-11
│   ├── parte3-engenharia-sdd-tdd/   ← Capítulos 12-17
│   ├── parte4-aplicacoes-avancadas/ ← Capítulos 18-23
│   ├── parte5-futuro-etica/         ← Capítulos 24-28
│   ├── prefacio/                    ← Elementos pré-textuais
│   ├── apendices/                   ← Apêndices
│   ├── imersao/                     ← 🆕 Camada de imersão
│   │   ├── personas/                ← Perfis narrativos
│   │   ├── gamification/            ← Sistema XP + badges
│   │   ├── qrcodes/                 ← Gerador de QR codes
│   │   ├── design/                  ← Comandos LaTeX imersivos
│   │   ├── podcast/                 ← Roteiros de episódios
│   │   ├── comunidade/              ← Config. Discord/GitHub
│   │   └── tests/                   ← Testes do motor
│   ├── figuras/                     ← Figuras TikZ
│   ├── ilustracoes/                 ← QR codes, badges
│   ├── codigos/                     ← Códigos dos capítulos
│   └── scripts/                     ← Scripts de build
│
├── 📁 src/                          ← Código fonte
│   ├── odontoia-pkg/                ← Pacote Python oficial
│   ├── scripts/                     ← Scripts auxiliares
│   └── notebooks/                   ← Notebooks Colab
│
├── 📁 tests/                        ← Testes do projeto
├── 📁 docs/                         ← Documentação
├── 📁 assets/                       ← Recursos multimídia
├── 📁 comunidade/                   ← Arquivos da comunidade
├── 📁 publishing/                   ← Artefatos de publicação
│
├── 📁 .github/                      ← GitHub Actions + Templates
├── README.md                        ← ← VOCÊ ESTÁ AQUI
├── Makefile                         ← Comandos do projeto
└── .gitignore                       ← Arquivos ignorados
```

---

## 5. Decisões Arquiteturais (ADRs)

### ADR-001: Links Simbólicos para o Conteúdo

**Contexto:** O conteúdo do livro reside no ecossistema OpenCode (`opencode-ecosystem-core/livro-odontologia-ia/`).  
**Decisão:** A pasta de projeto usa **links simbólicos** para o conteúdo existente, evitando duplicação.  
**Consequência:** O projeto é uma "visão organizada" do conteúdo, que continua sendo editado no ecossistema.

### ADR-002: Imersão como Camada Separada

**Contexto:** O livro existente já tem 18.389 linhas de conteúdo.  
**Decisão:** A imersão é uma **camada adicional** (SPEC-951) sobre a base (SPEC-950), sem modificar o conteúdo original.  
**Consequência:** Compatibilidade total. Pode-se compilar com ou sem imersão.

### ADR-003: Gamificação em Python (não LaTeX)

**Contexto:** Lógica de gamificação poderia ser em LuaLaTeX ou Python.  
**Decisão:** Motor em Python puro (pytest, YAML, JSON) — mais testável, portátil e integrável com o ecossistema.  
**Consequência:** 19 testes unitários, fácil manutenção, pode virar API web.

---

## 6. Integração com o Ecossistema OpenCode

```
OpenCode Ecosystem Core
│
├── specs/
│   ├── SPEC-950-livro-odontologia-ia.md    ← Especificação do conteúdo
│   └── SPEC-951-R200.md                    ← Especificação da imersão ←
│
├── livro-odontologia-ia/                    ← Conteúdo fonte do livro
│   └── ...                                  ← (linkado no projeto)
│
└── evolution/
    └── cycles.py → ciclo R200 registrado    ← Ciclo de evolução
```

---
*Para mais detalhes técnicos, consulte a [SPEC-951-R200](../specs/SPEC-951-R200.md)*
