#!/usr/bin/env python3
"""Fabrique la version anglaise du site à partir des pages françaises.

    python3 tools/traduire.py            # refait en/ ; liste ce qui manque à i18n/en.json
    python3 tools/traduire.py --extraire # ajoute à i18n/en.json les textes nouveaux, vides

**Le français est la source, l'anglais se fabrique.** Les pages anglaises ne s'écrivent pas à la
main : elles sont les pages françaises, texte remplacé bloc par bloc d'après `i18n/en.json`.
La mise en page ne peut donc pas diverger, et une page française modifiée se retraduit d'une
commande — ce qui manque est listé, rien n'est inventé.

Un « bloc » est un texte avec sa mise en forme en ligne (`<a>`, `<code>`, `<strong>`, `<kbd>`…),
tel qu'il est dans la page : on le traduit entier, balises comprises. S'y ajoutent les textes
d'attributs (`alt`, `aria-label`, `title`) et les descriptions de la page.
"""
import html
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICO = os.path.join(RACINE, "i18n", "en.json")
SITE = "https://black0s.github.io/Wuji-web/"

PAGES = ["index.html"] + sorted(
    os.path.join("pages", d, "index.html") for d in os.listdir(os.path.join(RACINE, "pages"))
    if os.path.isfile(os.path.join(RACINE, "pages", d, "index.html")))

EN_LIGNE = {"a", "code", "strong", "em", "kbd", "br", "span", "abbr", "sup", "sub", "b", "i", "small", "wbr"}
IGNORÉS = {"script", "style", "svg"}
ATTRIBUTS = ("alt", "aria-label", "title")
JETON = re.compile(r"<!--.*?-->|<![^>]*>|<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>|([^<]+)", re.S)


def segments(source):
    """Les blocs de texte de la page : [(début, fin, texte)], dans l'ordre."""
    jetons = [(m.start(), m.end(), m) for m in JETON.finditer(source)]
    blocs, courant, ignoré = [], None, 0

    def fermer():
        nonlocal courant
        if courant:
            d, f = courant
            # Les espaces de bord restent hors du bloc : la mise en page les garde.
            brut = source[d:f]
            d += len(brut) - len(brut.lstrip())
            f -= len(brut) - len(brut.rstrip())
            # Un bloc tout entier dans un seul élément se réduit à son contenu : « Naviguer » se
            # traduit une fois, quel que soit le chemin du lien qui l'entoure.
            while True:
                m = re.fullmatch(r"<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*)</\1>", source[d:f], re.S)
                if not m or re.search(r"</?%s\b" % m.group(1), m.group(2)):
                    break
                d, f = d + m.start(2), d + m.end(2)
            texte = source[d:f]
            if re.search(r"[A-Za-zÀ-ÿ]", re.sub(r"<[^>]+>", "", texte)):
                blocs.append((d, f, texte))
        courant = None

    for d, f, m in jetons:
        if m.group(0).startswith("<!"):
            fermer()
            continue
        fermant, nom, _, _, texte = m.group(1), (m.group(2) or "").lower(), m.group(3), m.group(4), m.group(5)
        if nom in IGNORÉS:
            ignoré += -1 if fermant else (0 if m.group(0).endswith("/>") else 1)
            fermer()
            continue
        if ignoré:
            continue
        # Un saut de ligne entre deux éléments sépare deux blocs : les pages écrivent une phrase
        # sur une ligne, et mettent les éléments voisins — liens d'un menu, cartes — à la ligne.
        if texte is not None and not texte.strip() and "\n" in texte:
            fermer()
            continue
        if texte is not None or nom in EN_LIGNE:
            courant = (courant[0], f) if courant else (d, f)
        else:
            fermer()
    fermer()
    return blocs


def attributs(source):
    """Les textes d'attributs : [(début, fin, texte)] — la valeur seule, entre ses guillemets."""
    trouvés = []
    for m in re.finditer(r'\s(%s)="([^"]*)"' % "|".join(ATTRIBUTS), source):
        if re.search(r"[A-Za-zÀ-ÿ]", m.group(2)):
            trouvés.append((m.start(2), m.end(2), m.group(2)))
    for m in re.finditer(r'<meta (?:name|property)="(?:description|og:title|og:description)" content="([^"]*)"', source):
        trouvés.append((m.start(1), m.end(1), m.group(1)))
    return trouvés


def textes(source):
    """Tout ce qui se traduit dans une page, hors `<title>` géré comme un bloc."""
    zones = segments(source) + attributs(source)
    # Un attribut est dans une balise, jamais dans un bloc de texte : pas de recouvrement.
    return sorted(zones)


def chemin_en(page):
    return os.path.join("en", page)


def profondeur(page):
    return page.count("/")


def vers_les_ressources(source, page):
    """En anglais, la page est un dossier plus bas : ses ressources sont un cran plus haut."""
    return re.sub(r'((?:src|href|content)=")((?:\.\./)*)(assets/|styles/)', r"\1../\2\3", source)


def sélecteur(page, anglais):
    """Le lien vers la même page dans l'autre langue."""
    remonter = "../" * (profondeur(page) + (1 if anglais else 0))
    cible = page.replace("index.html", "")
    if anglais:
        return f'<a class="nav-lang" href="{remonter}{cible}" hreflang="fr" lang="fr">Français</a>'
    return f'<a class="nav-lang" href="{remonter}en/{cible}" hreflang="en" lang="en">English</a>'


def alternatives(page):
    cible = page.replace("index.html", "")
    return (f'<link rel="alternate" hreflang="fr" href="{SITE}{cible}">\n'
            f'<link rel="alternate" hreflang="en" href="{SITE}en/{cible}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{cible}">\n')


def préparer_français(source, page):
    """Pose le sélecteur et les alternatives dans la page française — une fois, sans doublon."""
    source = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", source)
    source = source.replace("</head>", alternatives(page).rstrip("\n") + "\n</head>", 1)
    source = re.sub(r'\s*<a class="nav-lang"[^>]*>[^<]*</a>', "", source)
    lien = sélecteur(page, anglais=False)
    source = source.replace('    <button class="nav-toggle"', "    " + lien + '\n    <button class="nav-toggle"', 1)
    source = source.replace('  <nav class="nav-menu wrap" id="menu" aria-label="',
                            '  <nav class="nav-menu wrap" id="menu" aria-label="', 1)
    return source


def traduire(source, page, dico, manquants):
    zones = textes(source)
    morceaux, fin = [], 0
    for d, f, texte in zones:
        if d < fin:
            continue
        cible = dico.get(texte, "")
        if not cible:
            manquants.setdefault(texte, page)
            cible = texte
        morceaux.append(source[fin:d])
        morceaux.append(cible)
        fin = f
    morceaux.append(source[fin:])
    sortie = "".join(morceaux)
    sortie = sortie.replace('<html lang="fr">', '<html lang="en">', 1)
    sortie = vers_les_ressources(sortie, page)
    sortie = re.sub(r'<a class="nav-lang"[^>]*>[^<]*</a>', sélecteur(page, anglais=True), sortie)
    return sortie


def main():
    extraire = "--extraire" in sys.argv
    dico = json.load(open(DICO, encoding="utf-8")) if os.path.exists(DICO) else {}
    manquants = {}
    for page in PAGES:
        chemin = os.path.join(RACINE, page)
        source = open(chemin, encoding="utf-8").read()
        française = préparer_français(source, page)
        if française != source:
            open(chemin, "w", encoding="utf-8").write(française)
        anglaise = traduire(française, page, dico, manquants)
        destination = os.path.join(RACINE, chemin_en(page))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        open(destination, "w", encoding="utf-8").write(anglaise)
    if extraire:
        for texte in manquants:
            dico.setdefault(texte, "")
        json.dump(dico, open(DICO, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    à_faire = [t for t in manquants if not dico.get(t)]
    print(f"{len(PAGES)} pages · {len(dico)} textes au dictionnaire · {len(à_faire)} à traduire")
    for texte in à_faire[:20]:
        print("  —", manquants[texte], ":", html.unescape(re.sub(r"<[^>]+>", "", texte))[:90])
    return 1 if à_faire else 0


if __name__ == "__main__":
    sys.exit(main())
