#!/usr/bin/env python3
"""Aide à la lecture d'une carte brute du bar (.docx) : texte dans l'ordre (tableaux compris)
et logos reconnus (empreinte d'image → label, voir logos.json).

Usage : python3 inspect_raw.py CARTE.docx
Rendu visuel à faire à côté : soffice --headless --convert-to pdf CARTE.docx ; pdftoppm -r 70 -png CARTE.pdf page
"""
import hashlib, json, pathlib, sys
import docx
from docx.oxml.ns import qn

logos = json.load(open(pathlib.Path(__file__).with_name("logos.json"), encoding="utf-8"))
d = docx.Document(sys.argv[1])
rid = {r.rId: hashlib.md5(r.target_part.blob).hexdigest()[:8] for r in d.part.rels.values() if "image" in r.reltype}

def para_line(el, prefix=""):
    txt = "".join(t.text or "" for t in el.iter(qn("w:t"))).replace("\t", " ⇥ ")
    ids = [b.get(qn("r:embed")) for b in el.iter(qn("a:blip"))]
    marks = [logos.get(rid.get(i), "logo inconnu " + str(rid.get(i))) for i in ids]
    if txt.strip() or marks:
        print(f"{prefix}{txt.strip()}" + (f"   [LOGO: {', '.join(marks)}]" if marks else ""))

for el in d.element.body:
    if el.tag == qn("w:p"):
        para_line(el)
    elif el.tag == qn("w:tbl"):
        print("┌ TABLEAU")
        for tr in el.iter(qn("w:tr")):
            cells = []
            for tc in tr.iter(qn("w:tc")):
                parts = []
                for p in tc.iter(qn("w:p")):
                    t = "".join(x.text or "" for x in p.iter(qn("w:t"))).strip()
                    ids = [b.get(qn("r:embed")) for b in p.iter(qn("a:blip"))]
                    if ids:
                        t += " [LOGO: " + ", ".join(logos.get(rid.get(i), "inconnu") for i in ids) + "]"
                    parts.append(t)
                cells.append(" / ".join(x for x in parts if x))
            print("│ " + " | ".join(cells))
        print("└")
