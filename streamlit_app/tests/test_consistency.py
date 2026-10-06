from core.consistency import run_consistency_checks

def test_invalid_fdi_is_flagged():
    rows=[{"fdi":"99","finding":"Sem achado","quality":"Alta","restoration":False}]
    fdi=next(x for x in run_consistency_checks(rows) if x["check"]=="FDI válido")
    assert fdi["status"]=="REVISAR"

def test_restoration_caries_conflict_is_flagged():
    rows=[{"fdi":"26","finding":"Suspeita de cárie profunda","quality":"Moderada","restoration":True}]
    conflict=next(x for x in run_consistency_checks(rows) if x["check"]=="Cárie × restauração")
    assert conflict["status"]=="REVISAR"

def test_declared_findings_must_match():
    rows=[{"fdi":"13","finding":"Suspeita de cárie","quality":"Alta","restoration":False},{"fdi":"14","finding":"Sem achado","quality":"Alta","restoration":False}]
    count=next(x for x in run_consistency_checks(rows,declared_findings=2) if x["check"]=="Contagem de achados")
    assert count["status"]=="REVISAR"
