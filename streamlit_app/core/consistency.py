from __future__ import annotations

from collections import Counter
from typing import Iterable

EXPECTED_FDI = {
    *(str(n) for n in range(11, 19)),
    *(str(n) for n in range(21, 29)),
    *(str(n) for n in range(31, 39)),
    *(str(n) for n in range(41, 49)),
}

def run_consistency_checks(records: Iterable[dict], declared_findings: int | None = None) -> list[dict]:
    rows = list(records)
    checks: list[dict] = []
    fdi_values = [str(r.get("fdi", "")).strip() for r in rows if str(r.get("fdi", "")).strip()]
    invalid_fdi = sorted({x for x in fdi_values if x not in EXPECTED_FDI})
    duplicates = sorted(k for k, v in Counter(fdi_values).items() if v > 1)

    checks.append({"check":"FDI válido","status":"OK" if not invalid_fdi else "REVISAR",
                   "detail":"Todos os códigos FDI são plausíveis." if not invalid_fdi else f"FDI inválidos: {', '.join(invalid_fdi)}"})
    checks.append({"check":"FDI duplicado","status":"OK" if not duplicates else "REVISAR",
                   "detail":"Sem duplicidades." if not duplicates else f"Duplicidades: {', '.join(duplicates)}"})

    findings = [r for r in rows if str(r.get("finding", "Sem achado")).lower() not in {"sem achado","nenhum",""}]
    if declared_findings is not None:
        checks.append({"check":"Contagem de achados","status":"OK" if len(findings)==declared_findings else "REVISAR",
                       "detail":f"Declarados: {declared_findings}; rastreáveis: {len(findings)}."})

    low_quality = [r for r in rows if str(r.get("quality","")).lower() in {"baixa","não avaliável","nao avaliavel"}]
    checks.append({"check":"Qualidade por elemento","status":"OK" if not low_quality else "ATENÇÃO",
                   "detail":"Sem elementos marcados como baixa qualidade." if not low_quality else f"{len(low_quality)} elemento(s) com avaliação limitada."})

    conflicts=[]
    for r in rows:
        if bool(r.get("restoration",False)) and "cárie" in str(r.get("finding","")).lower():
            conflicts.append(str(r.get("fdi","?")))
    checks.append({"check":"Cárie × restauração","status":"OK" if not conflicts else "REVISAR",
                   "detail":"Sem conflito aparente." if not conflicts else f"Revisar interferência restauradora em: {', '.join(conflicts)}."})
    return checks
