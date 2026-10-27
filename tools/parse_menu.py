#!/usr/bin/env python3
"""Lit la carte du Clandestin au format Word « modèle propre » et produit menu.json.

Aucune API : le fichier doit respecter le modèle décrit dans MENU/README.md.
Toute anomalie bloque la publication (code de sortie 1) : l'appli garde alors l'ancienne carte.

Usage : parse_menu.py CARTE.docx SORTIE.json [--previous ANCIEN.json] [--force]
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata

from docx import Document
from docx.oxml.ns import qn

# Styles Word -> rôle. Les noms français couvrent un fichier réenregistré par un Word en français.
ROLES = {
    "title": "universe", "titre": "universe",
    "heading 1": "section", "titre 1": "section",
    "heading 2": "group", "titre 2": "group",
    "formats": "formats",
    "article": "item",
    "appellation": "appellation",
    "cépages": "grapes", "cepages": "grapes",
    "description": "description",
    "composition": "component",
    "labels": "labels",
    "note": "note",
}
LABELS = {"Bio", "HVE", "Terra Vitis", "Agriculture raisonnée", "Fait maison", "Sans alcool", "Végétarien", "Vin nature"}
PRICE_RE = re.compile(r"^(\d+(?:[.,]\d{1,2})?)\s*€$")
NO_PRICE = {"—", "-", "–"}
MAX_DROP = 0.30  # baisse maximale du nombre d'articles tolérée sans --force


def slug(*parts):
    s = "-".join(p for p in parts if p)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def parse(path):
    doc = Document(path)
    errors = []
    body = doc.element.body
    if body.findall(qn("w:tbl")):
        errors.append("Le fichier contient un tableau : le modèle n'en utilise pas.")

    menu = {"notes": [], "universes": []}
    uni = sec = grp = item = None
    formats = None

    def scope():
        return grp or sec or uni or menu

    for n, p in enumerate(doc.paragraphs, 1):
        text = p.text.strip()
        if not text:
            continue
        style = (p.style.name if p.style is not None else "").strip().lower()
        role = ROLES.get(style)
        where = f"paragraphe {n} « {text[:60]} »"
        if role is None:
            errors.append(f"{where} : style « {p.style.name} » hors modèle.")
            continue

        if role == "universe":
            uni = {"name": text, "notes": [], "sections": []}
            menu["universes"].append(uni)
            sec = grp = item = None
            formats = None
        elif role == "section":
            if uni is None:
                errors.append(f"{where} : rubrique avant le premier titre (Boissons / À manger).")
                continue
            sec = {"name": text, "notes": [], "groups": []}
            uni["sections"].append(sec)
            grp = item = None
            formats = None
        elif role == "group":
            if sec is None:
                errors.append(f"{where} : sous-rubrique hors d'une rubrique.")
                continue
            grp = {"name": text, "notes": [], "items": []}
            sec["groups"].append(grp)
            item = None
            formats = None
        elif role == "formats":
            formats = [c.strip() for c in p.text.split("\t") if c.strip()]
            item = None
        elif role == "item":
            if sec is None:
                errors.append(f"{where} : article hors d'une rubrique.")
                continue
            if formats is None:
                errors.append(f"{where} : aucune ligne « Formats » avant cet article.")
                continue
            fields = [f.strip() for f in p.text.split("\t") if f.strip()]
            name, raw_prices = fields[0], fields[1:]
            if len(raw_prices) != len(formats):
                errors.append(f"{where} : {len(raw_prices)} prix pour {len(formats)} formats ({', '.join(formats)}).")
                continue
            prices = []
            for label, rp in zip(formats, raw_prices):
                if rp in NO_PRICE:
                    continue
                m = PRICE_RE.match(rp)
                if not m:
                    errors.append(f"{where} : prix illisible « {rp} ».")
                    continue
                prices.append({"label": label, "amount": float(m.group(1).replace(",", "."))})
            if not prices:
                errors.append(f"{where} : aucun prix.")
            if grp is None:  # rubrique sans sous-rubrique : groupe implicite
                grp = {"name": None, "notes": [], "items": []}
                sec["groups"].append(grp)
            item = {"id": slug(sec["name"], grp["name"] or "", name), "name": name, "prices": prices,
                    "labels": [], "appellation": None, "grapes": None, "description": None, "components": []}
            grp["items"].append(item)
        elif role == "note":
            scope()["notes"].append(text)
        else:  # détails rattachés au dernier article
            if item is None:
                errors.append(f"{where} : ligne « {p.style.name} » sans article au-dessus.")
                continue
            if role == "labels":
                for lab in (l.strip() for l in text.split(",")):
                    if lab not in LABELS:
                        errors.append(f"{where} : label inconnu « {lab} » (autorisés : {', '.join(sorted(LABELS))}).")
                    else:
                        item["labels"].append(lab)
            elif role == "component":
                item["components"].append(re.sub(r"^[–\-•]\s*", "", text))
            elif item[role]:
                item[role] += " " + text
            else:
                item[role] = text

    # Contrôles de structure
    if not menu["universes"]:
        errors.append("Aucun titre (style Titre) : il faut au moins « Boissons » ou « À manger ».")
    for u in menu["universes"]:
        if not u["sections"]:
            errors.append(f"Le titre « {u['name']} » n'a aucune rubrique.")
        for s in u["sections"]:
            s["groups"] = [g for g in s["groups"] if g["items"] or g["name"]]
            if not any(g["items"] for g in s["groups"]):
                errors.append(f"La rubrique « {s['name']} » est vide.")
            for g in s["groups"]:
                if not g["items"]:
                    errors.append(f"La sous-rubrique « {g['name']} » ({s['name']}) est vide.")
    ids = [i["id"] for u in menu["universes"] for s in u["sections"] for g in s["groups"] for i in g["items"]]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append("Articles en double : " + ", ".join(sorted(dup)))
    return menu, errors, len(ids)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("out")
    ap.add_argument("--previous", help="menu.json publié, pour détecter une carte tronquée")
    ap.add_argument("--force", action="store_true", help="publier malgré une forte baisse du nombre d'articles")
    a = ap.parse_args()

    menu, errors, count = parse(a.docx)
    if a.previous and not a.force:
        try:
            old = json.load(open(a.previous, encoding="utf-8")).get("itemCount", 0)
            if old and count < old * (1 - MAX_DROP):
                errors.append(f"Seulement {count} articles contre {old} avant : carte probablement tronquée "
                              f"(relancer avec --force si c'est voulu).")
        except FileNotFoundError:
            pass

    if errors:
        print(f"❌ Carte refusée, {len(errors)} problème(s) :", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(1)

    menu = {"schema": 1, "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": a.docx.rsplit("/", 1)[-1], "itemCount": count, **menu}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(menu, f, ensure_ascii=False, indent=2)
    print(f"✅ Carte valide : {count} articles.")
    for u in menu["universes"]:
        for s in u["sections"]:
            n = sum(len(g["items"]) for g in s["groups"])
            print(f"   {u['name']} › {s['name']} : {n}")


if __name__ == "__main__":
    main()
