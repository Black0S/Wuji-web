# Wuji-web

Le site de [Wuji](https://github.com/Black0S/Wuji) — un navigateur pour macOS.

Statique : trois fichiers, aucune dépendance, aucun build. Ce que GitHub sert est
exactement ce qui est dans le dépôt.

```
index.html   la page
styles.css   la feuille de style
assets/      l'icône, extraite de AppIcon.icns
.nojekyll    demande à Pages de servir les fichiers tels quels
```

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
