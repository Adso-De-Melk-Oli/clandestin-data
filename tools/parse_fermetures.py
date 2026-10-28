#!/usr/bin/env python3
"""Lit FERMETURES.md (fermetures exceptionnelles du Clandestin) et produit fermetures.json.

Format d'une fermeture (une rubrique « ## » par fermeture) :

    ## 28/10/2026                      (un seul jour)
    ## 21/12/2026 → 04/01/2027         (plusieurs jours, « au » ou « -> » marchent aussi)
    Type : intempérie                  intempérie, imprévu, congés, travaux, privatisation
    Message : Alerte orange orages…    (facultatif) le texte affiché dans l'appli
    Réouverture : 29/10/2026 à 18h     (facultatif) sinon : prochaine ouverture habituelle
    Annonce : 7 jours avant            (facultatif) dès quand l'appli l'affiche, 7 jours par défaut
    Horaires : ouvert jusqu'à 20h      (facultatif) le bar n'est PAS fermé, ses horaires changent

Le texte entre <!-- et --> est ignoré (exemples, brouillons).
Toute anomalie bloque la publication (code de sortie 1) : l'appli garde alors l'ancienne version.

Usage : parse_fermetures.py FERMETURES.md SORTIE.json
"""
import datetime as dt
import json
import re
import sys
import unicodedata

TYPES = {
    "intemperie": "intempérie",
    "imprevu": "imprévu",
    "conges": "congés",
    "vacances": "congés",
    "travaux": "travaux",
    "privatisation": "privatisation",
}
DATE_RE = re.compile(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?")
TIME_RE = re.compile(r"(\d{1,2})\s*[hH:]\s*(\d{2})?")
RANGE_SEP = re.compile(r"\s*(?:→|->|–|—|\bau\b|-)\s*")


def plain(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def parse_date(text, ref_year, after=None):
    m = DATE_RE.search(text)
    if not m:
        return None
    d, mo, y = int(m.group(1)), int(m.group(2)), m.group(3)
    year = (2000 + int(y) if len(y) == 2 else int(y)) if y else ref_year
    date = dt.date(year, mo, d)
    if not y and after and date < after:
        date = dt.date(year + 1, mo, d)
    return date


def parse(text, today=None):
    today = today or dt.date.today()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    errors, closures = [], []
    blocks = re.split(r"^##\s+", text, flags=re.M)[1:]
    for block in blocks:
        lines = [l.strip() for l in block.strip().splitlines()]
        head, fields = lines[0], {}
        where = f"« ## {head} »"
        for l in lines[1:]:
            if not l or l.startswith("#"):
                continue
            if ":" not in l:
                errors.append(f"{where} : ligne sans « : » → « {l} »")
                continue
            k, v = l.split(":", 1)
            fields[plain(k)] = v.strip()

        try:
            parts = [p for p in RANGE_SEP.split(head, maxsplit=1) if p]
            start = parse_date(parts[0], today.year)
            end = parse_date(parts[1], start.year, after=start) if len(parts) > 1 and start else start
            if not start or not end:
                raise ValueError
        except (ValueError, TypeError, AttributeError):
            errors.append(f"{where} : date illisible (écrire 28/10/2026 ou 21/12/2026 → 04/01/2027)")
            continue
        if end < start:
            errors.append(f"{where} : la date de fin est avant la date de début")
            continue
        if (end - start).days > 62:
            errors.append(f"{where} : plus de deux mois de fermeture, vérifier les dates (année ?)")
            continue

        kind = TYPES.get(plain(fields.pop("type", "imprévu")))
        if not kind:
            errors.append(f"{where} : type inconnu (choisir : intempérie, imprévu, congés, travaux, privatisation)")
            continue

        c = {"from": start.isoformat(), "to": end.isoformat(), "type": kind}
        if fields.get("message"):
            c["message"] = fields.pop("message")
        else:
            fields.pop("message", None)

        r = fields.pop("reouverture", None)
        if r:
            day = parse_date(r, end.year, after=end)
            tm = TIME_RE.search(DATE_RE.sub("", r))
            if not day:
                errors.append(f"{where} : réouverture illisible (écrire 29/10/2026 à 18h)")
                continue
            if day <= end:
                errors.append(f"{where} : la réouverture doit être après le dernier jour fermé")
                continue
            h, mi = (int(tm.group(1)), int(tm.group(2) or 0)) if tm else (18, 0)
            c["reopen"] = f"{day.isoformat()}T{h:02d}:{mi:02d}"

        a = fields.pop("annonce", None)
        if a:
            m = re.search(r"\d+", a)
            if not m:
                errors.append(f"{where} : annonce illisible (écrire « 7 jours avant »)")
                continue
            c["announceDays"] = int(m.group())

        h = fields.pop("horaires", None)
        if h:
            c["hours"] = h

        for k in fields:
            errors.append(f"{where} : rubrique inconnue « {k} » (Type, Message, Réouverture, Annonce, Horaires)")
        closures.append(c)

    closures.sort(key=lambda c: c["from"])
    return closures, errors


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    closures, errors = parse(open(src, encoding="utf-8").read())
    if errors:
        print("Fermetures NON publiées :", file=sys.stderr)
        for e in errors:
            print(f"::error::{e}")
            print(f" - {e}", file=sys.stderr)
        sys.exit(1)
    data = {
        "schema": 1,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "closures": closures,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{len(closures)} fermeture(s) lue(s).")


if __name__ == "__main__":
    main()
