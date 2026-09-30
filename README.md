# Wuji-web

Le site de Wuji — un navigateur pour macOS.

Statique : trois fichiers, aucune dépendance, aucun build. Ce que GitHub sert est
exactement ce qui est dans le dépôt.

```
index.html   la page
styles.css   la feuille de style, en clair
assets/      l'icône extraite de AppIcon.icns, et quatre captures
.nojekyll    demande à Pages de servir les fichiers tels quels
```

**Un seul thème, le clair**, et les captures aussi : les couleurs de `styles.css` sont
celles du thème clair de `Sources/DesignSystem/Tokens.swift`.

| capture | ce qu'elle montre | où | taille |
|---|---|---|---|
| `wuji-page.png` | un article de Wikipédia, les deux colonnes ouvertes | en tête | 1440 × 907 |
| `wuji-palette.png` | la palette ouverte (`⌘L`) | Fonctions | 1440 × 907 |
| `wuji-outils.png` | les outils de développement (`⌥⌘I`) | Fonctions | 1440 × 907 |
| `wuji-blocage.png` | Réglages › Blocage, rien en service | Blocage | 1440 × 1041 |

Les captures viennent du banc de Wuji — un profil neuf, jamais celui de quelqu'un —, la
fenêtre mise à 1440 × 907 points, photographiée sans ombre puis réduite à 1440 pixels de
large. Pour en changer : garder le nom et le rapport, sinon corriger `width` et `height`
dans `index.html`, qui réservent la place avant le chargement.

## Le voir en local

```bash
python3 -m http.server 8000
```

## Publier une version

Le dépôt du code est privé : **les versions se publient ici.** Une release de ce dépôt,
avec le `.dmg` en pièce jointe sous le nom exact **`Wuji.dmg`**. Deux choses en dépendent :

- les boutons « Télécharger » visent `releases/latest/download/Wuji.dmg` — la dernière
  release, sans rien à changer dans la page ;
- la vérification de version de l'application (Réglages › Fonctions) lit la dernière
  release de ce dépôt ; l'étiquette doit porter le numéro, `v0.7.5` par exemple.

Seul le numéro écrit dans `index.html` (en tête et dans « Installer ») se met à jour à la
main.

## Le publier

Le site paraît sur `https://black0s.github.io/Wuji-web/` : le workflow
`.github/workflows/static.yml` le déploie à chaque poussée sur `main`.
