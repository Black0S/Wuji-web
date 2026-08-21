# Wuji-web

Le site de [Wuji](https://github.com/Black0S/Wuji) — un navigateur pour macOS.

Statique : trois fichiers, aucune dépendance, aucun build. Ce que GitHub sert est
exactement ce qui est dans le dépôt.

```
index.html   la page
styles.css   la feuille de style, en clair et en sombre
assets/      l'icône extraite de AppIcon.icns, et deux captures de l'application
.nojekyll    demande à Pages de servir les fichiers tels quels
```

Le site suit l'apparence du système, comme l'application suit celle de macOS : les deux
palettes de `styles.css` sont celles de `Sources/DesignSystem/Tokens.swift`, et rien ne
bascule à la main.

Les captures (`wuji-page.png`, `wuji-depot.png`) sont prises en apparence sombre. Elles
restent lisibles sur fond clair — ce sont des photos d'une fenêtre, pas des éléments du
site. Pour qu'elles suivent le thème, il faudrait les reprendre en clair et les servir en
`<picture>`.

## Le voir en local

```bash
python3 -m http.server 8000
```

## Le publier

Settings › Pages › Source : **Deploy from a branch**, branche `main`, dossier `/ (root)`.
Le site paraît sur `https://black0s.github.io/Wuji-web/` une minute plus tard.

Pour une adresse propre, deux possibilités :

- renommer le dépôt en `black0s.github.io` — le site occupe alors la racine ;
- poser un nom de domaine dans Settings › Pages › Custom domain, ce qui écrit un fichier
  `CNAME` ici même.

## Mettre à jour

La version affichée et le lien de téléchargement pointent vers
`releases/latest/download/Wuji.dmg` : la dernière publication du dépôt Wuji, sans rien à
changer ici. Seul le numéro de version écrit dans `index.html` se met à jour à la main.
