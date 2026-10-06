from __future__ import annotations
import io, json
from datetime import datetime
import pandas as pd
import streamlit as st
from PIL import Image
from core.consistency import run_consistency_checks
from core.demo import DEMO_RECORDS, demo_heatmap, draw_demo_overlay

st.set_page_config(page_title="Panoramica AI",page_icon="🦷",layout="wide",initial_sidebar_state="expanded")
st.title("Panoramica AI")
st.caption("Protótipo de apoio à pesquisa odontológica em radiografias panorâmicas — revisão humana obrigatória.")

with st.sidebar:
    st.header("Configuração")
    mode=st.radio("Modo",["Clínico","Pesquisador"],horizontal=True)
    threshold=st.slider("Limiar de score",0.10,0.95,0.45,0.05)
    demo_mode=st.toggle("Modo demonstração",value=True)
    st.divider()
    st.warning("Não usar como diagnóstico autônomo. Protótipo de pesquisa/validação.")

uploaded=st.file_uploader("Carregue uma radiografia panorâmica (PNG/JPG)",type=["png","jpg","jpeg"])
if uploaded is None:
    st.info("Carregue uma imagem para iniciar a revisão. O modo demonstração não executa inferência clínica real.")
    st.stop()

image=Image.open(io.BytesIO(uploaded.getvalue())).convert("RGB")
if "records" not in st.session_state:
    st.session_state.records=[dict(r) for r in DEMO_RECORDS]

records=st.session_state.records
visible_records=[r for r in records if float(r.get("score",0))>=threshold or r.get("finding")=="Sem achado"]

m1,m2,m3,m4=st.columns(4)
m1.metric("Elementos registrados",len(visible_records))
m2.metric("Achados rastreáveis",sum(r["finding"]!="Sem achado" for r in visible_records))
m3.metric("Revisões pendentes",sum(r["review"]=="Pendente" for r in visible_records))
m4.metric("Limiar",f"{threshold:.2f}")

tab1,tab2,tab3,tab4,tab5=st.tabs(["Imagem","Inventário / FDI","Explicabilidade","Consistência","Relatório"])

with tab1:
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Original")
        st.image(image,use_container_width=True)
    with c2:
        st.subheader("Anotada")
        if demo_mode:
            st.image(draw_demo_overlay(image),use_container_width=True)
            st.caption("Caixas demonstrativas. Substituir pela saída do detector/segmentador treinado.")
        else:
            st.image(image,use_container_width=True)
            st.caption("Nenhum backend de inferência foi conectado nesta versão.")

with tab2:
    st.subheader("Inventário dentário e revisão humana")
    df=pd.DataFrame(visible_records)
    edited=st.data_editor(df,use_container_width=True,hide_index=True,
        column_config={
            "score":st.column_config.NumberColumn("score bruto",min_value=0.0,max_value=1.0,format="%.2f"),
            "restoration":st.column_config.CheckboxColumn("restauração"),
            "endo":st.column_config.CheckboxColumn("endodontia"),
            "review":st.column_config.SelectboxColumn("revisão",options=["Pendente","Confirmado","Corrigido","Descartado"]),
        },disabled=["score"],key="inventory_editor")
    if st.button("Aplicar revisões",type="primary"):
        st.session_state.records=edited.to_dict(orient="records")
        st.success("Revisões aplicadas na sessão.")

with tab3:
    st.subheader("Explicabilidade")
    st.write("Fluxo previsto: imagem → ROI do dente → detecção/segmentação → CAM específica da predição.")
    if demo_mode:
        st.image(demo_heatmap(image),caption="Heatmap demonstrativo — NÃO é Grad-CAM real.",use_container_width=True)
        st.info("Para Grad-CAM real, conecte o tensor da classe/detecção ao mapa de ativação do modelo treinado. O heatmap acima apenas valida a interface.")
    else:
        st.info("Backend de explicabilidade ainda não conectado.")

with tab4:
    st.subheader("Clinical Consistency Engine")
    declared=st.number_input("Achados declarados pelo pipeline",min_value=0,value=sum(r["finding"]!="Sem achado" for r in visible_records),step=1)
    checks=run_consistency_checks(visible_records,int(declared))
    st.dataframe(pd.DataFrame(checks),use_container_width=True,hide_index=True)
    if any(x["status"]=="REVISAR" for x in checks):
        st.error("Há inconsistências que devem ser resolvidas antes da liberação do relatório.")
    else:
        st.success("Nenhum conflito crítico detectado pelas regras atuais.")

with tab5:
    st.subheader("Relatório estruturado")
    payload={
        "project":"Panoramica AI","generated_at":datetime.now().isoformat(timespec="seconds"),
        "mode":mode,"research_prototype":True,"threshold":threshold,"image_name":uploaded.name,
        "records":visible_records,"consistency_checks":run_consistency_checks(visible_records),
        "disclaimer":"Resultado de apoio à pesquisa. Requer validação e interpretação por profissional habilitado."
    }
    st.json(payload,expanded=False)
    st.download_button("Baixar JSON da revisão",data=json.dumps(payload,ensure_ascii=False,indent=2),
                       file_name="panoramica_ai_revisao.json",mime="application/json")

if mode=="Pesquisador":
    st.divider()
    with st.expander("Arquitetura / integração de modelos"):
        st.code("Quality AI → Tooth Instance Segmentation → FDI → Caries/Restoration/Endo/Periapical → Consistency Engine → Explainability → Human Review",language="text")
        st.write("Pontos de extensão recomendados: predict_teeth(image), classify_findings(rois), segment_anatomy(image) e explain_detection(model, target).")
