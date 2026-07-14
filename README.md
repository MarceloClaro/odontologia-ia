# 🦷 Odontologia & Inteligência Artificial — Livro Imersão

**Autor:** Edson Laranjeiras  
**Status:** 🟢 Em produção (SPEC-951-R200)  
**Versão:** 2.0.0 (Imersão)  
**Licença:** CC BY-NC-SA 4.0  

---

## 📖 Sobre o Projeto

Este é o repositório oficial do **Livro Imersão "Odontologia & Inteligência Artificial"**, 
do autor **Edson Laranjeiras** — Cirurgião-Dentista, Especialista em Sistemas e Agentes 
Inteligentes (UFG), Mestre em Ciências da Saúde.

### O que é um "Livro Imersão"?

Um **Livro Imersão** transcende o formato linear tradicional. Ele combina:

```
📖 Texto técnico     → 500 laudas, 28 capítulos, 5 partes
🎭 Narrativa viva    → Personas (Dra. Marina, Seu Raimundo, Prof. Lucas)
🎮 Gamificação       → XP, badges, níveis, desafios
📱 QR Codes          → Vídeos, Colab, Podcast, Testes, Referências
🎧 Podcast           → OdontoIA Cast (10 episódios por capítulo)
🌐 Comunidade        → Discord, GitHub Discussions, lives semanais
🧪 Código executável → Python + Google Colab + TDD
```

---

## 📚 Estrutura do Livro

| Parte | Título | Capítulos | Nível |
|-------|--------|-----------|-------|
| **I** | Fundamentos Históricos e Tecnológicos | 1–5 | 🟢 Iniciante |
| **II** | Teoria e Modelos de Deep Learning | 6–11 | 🟡 Intermediário |
| **III** | Engenharia de Software Odontológico (SDD/TDD) | 12–17 | 🔴 Avançado |
| **IV** | Aplicações Avançadas em Especialidades | 18–23 | 🟣 PhD |
| **V** | Futuro, Ética e Regulação da IA | 24–28 | 🟣 PhD |

### Total: **28 capítulos** | **500 laudas** | **35+ artigos científicos** | **93+ testes**

---

## 🚀 Como Usar

### Pré-requisitos

```bash
# Para compilar o livro (LaTeX)
sudo apt install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber

# Para o pacote Python (códigos)
pip install -e src/odontoia-pkg

# Para gerar QR codes
pip install qrcode[pil]
```

### Compilar o Livro

```bash
# Compilação completa com elementos de imersão
./livro/scripts/compilar_imersao.sh

# Ou manualmente (xelatex)
cd livro
xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex
```

### Rodar os Testes

```bash
# Testes do motor de gamificação
python3 -m pytest livro/imersao/tests/

# Testes do pacote odontoia
python3 -m pytest src/odontoia-pkg/tests/
```

---

## 🎮 Sistema de Imersão

### Personagens

| Persona | Papel | Descrição |
|---------|-------|-----------|
| 🎭 **Dra. Marina Duarte** | Protagonista | Periodontista que aprende IA do zero |
| 🦷 **Seu Raimundo** | Paciente | Caso clínico que atravessa o livro |
| 🧠 **Prof. Dr. Lucas Tancredi** | Mentor | PhD que traduz IA para odontologia |

### Gamificação

| Nível | Título | XP Total |
|-------|--------|----------|
| 1 | Curioso Digital | 0 |
| 2 | Aprendiz de IA | 2.000 |
| 3 | Praticante Clínico | 5.000 |
| 4 | Desenvolvedor Odontológico | 12.000 |
| 5 | Arquiteto de Soluções | 25.000 |
| 6 | Pesquisador IA-Odonto | 50.000 |
| 7 | Mestre em Gêmeos Digitais | 100.000 |
| 8 | PhD em Odontologia IA | 200.000 |

**14 badges** disponíveis — do "Curioso Digital" ao "PhD em Odontologia IA".

---

## 📋 Roadmap

| Fase | O quê | Status |
|------|-------|--------|
| **F0** | Base do livro (28 capítulos, 500 laudas) | ✅ Completo |
| **F1** | SPEC-951 — Conceito de Livro Imersão | ✅ Completo |
| **F2** | Personas e narrativa transmídia | ✅ Completo |
| **F3** | Gamificação (XP + badges + níveis) | ✅ Completo |
| **F4** | QR codes integrados | ✅ Script gerador pronto |
| **F5** | Design imersivo LaTeX | ✅ Integrado |
| **F6** | Podcast (roteiros) | ✅ 10 episódios |
| **F7** | Comunidade (Discord + GitHub) | ✅ Configurada |
| **F8** | Imersão estendida para todos os 28 capítulos | ⏳ Pendente |
| **F9** | Realidade Aumentada (marcadores 3D) | ⏳ Pendente |
| **F10** | Publicação (ISBN, DOI, ePub) | ⏳ Pendente |

---

## 🌐 Comunidade

- **Discord:** [discord.gg/odontologia-ia](https://discord.gg/odontologia-ia)
- **GitHub Discussions:** [Discussões](https://github.com/edsonlaranjeiras/odontologia-ia/discussions)
- **Podcast:** OdontoIA Cast (Spotify, Apple, YouTube)

---

## 📄 Licença

Este trabalho está licenciado sob **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International** (CC BY-NC-SA 4.0).

---

## 🧠 Citação

```bibtex
@book{laranjeiras2026odontologia,
  author    = {Edson Laranjeiras},
  title     = {Odontologia \& Inteligência Artificial: 
               Da História aos Gêmeos Digitais — Livro Imersão},
  year      = {2026},
  edition   = {1},
  note      = {500 laudas, 28 capítulos, 5 partes},
}
```

---

**Feito com 🦷 + 🧠 por Edson Laranjeiras**  
*"A IA não substitui o dentista — potencializa."*
