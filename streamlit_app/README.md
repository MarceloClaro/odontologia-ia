# Panoramica AI — Streamlit

Protótipo Streamlit para revisão estruturada de radiografias panorâmicas.

## Funcionalidades

- upload de radiografia panorâmica;
- modos Clínico e Pesquisador;
- inventário dentário / FDI editável;
- atributos independentes de restauração e endodontia;
- painel de explicabilidade com heatmap demonstrativo;
- Clinical Consistency Engine;
- revisão humana;
- exportação da sessão em JSON;
- testes unitários básicos das regras de consistência.

IMPORTANTE: esta versão não implementa diagnóstico autônomo. O modo demonstração usa dados e marcações simulados para validar a interface e a arquitetura.

## Executar localmente

    cd streamlit_app
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

No Windows, use .venv\Scripts\activate.

## Testes

    cd streamlit_app
    pytest -q

## Publicar no Streamlit Community Cloud

1. Conecte sua conta GitHub no Streamlit Community Cloud.
2. Selecione o repositório MarceloClaro/odontologia-ia.
3. Use a branch feature/panoramica-streamlit-v1 durante a homologação.
4. Main file path: streamlit_app/app.py.
5. Após validar, faça merge para main e altere o deploy para a branch principal.

## Arquitetura prevista

    Quality AI
      ↓
    Tooth Instance Segmentation
      ↓
    FDI
      ↓
    Caries / Restoration / Endodontics / Periapical
      ↓
    Consistency Engine
      ↓
    Explainability (Grad-CAM / HiResCAM / EigenCAM)
      ↓
    Human Review
      ↓
    Structured Report

Sugestão: manter pesos grandes fora do Git e versioná-los em storage de modelos ou releases, com checksums.
