#!/usr/bin/env python3
"""Compare tous les prix de la carte d'origine (texte du PDF rendu) à ceux du menu.json produit.
Usage : python3 check_prices.py carte-origine.txt menu.json   (code 1 si un écart)"""
import collections, json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
src = collections.Counter(float(x.replace(",", ".")) for x in re.findall(r"(\d+(?:,\d{1,2})?)\s*€", t))
m = json.load(open(sys.argv[2], encoding="utf-8")); out = collections.Counter()
for u in m["universes"]:
    for s in u["sections"]:
        for g in s["groups"]:
            for i in g["items"]:
                for p in i["prices"]: out[p["amount"]] += 1
                for x in re.findall(r"(\d+,\d{2})\s*€", i.get("description") or ""): out[float(x.replace(",", "."))] += 1
print(f"prix carte d'origine : {sum(src.values())} | prix publiés : {sum(out.values())}")
a, b = dict(src - out), dict(out - src)
print("absents du menu :", a); print("en trop dans le menu :", b)
sys.exit(1 if a or b else 0)
