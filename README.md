# Wuji-web

Le site de Wuji — un navigateur pour macOS.

Statique : du HTML, trois feuilles de style, un script. Aucune dépendance, aucun build. Ce
que GitHub sert est exactement ce qui est dans le dépôt.

```
index.html                  l'accueil
pages/<sujet>/index.html    une page par sujet — toutes les fonctions, rangées
  naviguer/ lire/ blocage/ confidentialite/ mots-de-passe/ sites/
  developpeurs/ performance/ raccourcis/ installer/
styles/css/base.css         les jetons du thème clair de Wuji, la typographie
styles/css/layout.css       la barre, les bandes, le gabarit des pages, le pied
styles/css/components.css   boutons, cartes, figures, tableaux, touches, visionneuse
styles/js/site.js           le menu du téléphone, le sommaire qui suit la lecture,
                            la visionneuse des captures, le choix AZERTY / QWERTY
assets/                     l'icône et la favicone
assets/captures/            les captures de l'application
.nojekyll                   demande à Pages de servir les fichiers tels quels
```

**Un seul thème, le clair**, et les captures aussi : les couleurs de `base.css` sont celles du
thème clair de `Sources/DesignSystem/Tokens.swift`.

**Le script n'est qu'un confort.** Sans lui, chaque page se lit en entière, le pied de page
mène partout, et les touches qui changent d'un clavier à l'autre — celles à droite du P, `]`
et `[` en QWERTY, `$` et `^` en AZERTY — affichent leurs deux signes côte à côte. Avec lui,
seul celui du clavier choisi reste : AZERTY d'office pour un navigateur en français, et le
choix se retient.

**La barre et le pied se répètent dans chaque page**, sans script qui les injecte : une page
s'affiche entière même sans JavaScript, et c'est ce qu'un moteur de recherche lit. Une page
ajoutée se déclare donc dans la barre, le menu du téléphone, le sommaire latéral et le pied
de chaque page.

## Les captures

Elles viennent du banc de Wuji — un profil neuf, jamais celui de quelqu'un : une session semée
(un dossier, une paire d'onglets), quelques favoris, un historique d'essai. La fenêtre est mise
à 1440 × 907 points, photographiée sans ombre et réduite à 1440 pixels de large ; les fenêtres
de réglages font 1440 × 1041. Pour en changer une : garder le nom et le rapport, sinon corriger
`width` et `height` là où elle est posée, qui réservent la place avant le chargement.

| capture | ce qu'elle montre |
|---|---|
| `accueil.png` | la fenêtre : un dossier d'onglets, un article, les favoris |
| `double-page.png` | deux pages côte à côte |
| `zen.png` | le mode zen |
| `lune.png` | une page rendue sombre par la lune |
| `lecture.png` | le mode lecture |
| `palette.png` | la palette ouverte |
| `historique.png` | la colonne de droite sur l'historique |
| `outils.png` | les outils de développement |
| `blocage.png`, `regles.png` | Réglages › Blocage, Mes règles |
| `confidentialite.png`, `sites-web.png`, `performances.png`, `apparence.png`, `barre-adresse.png` | les sections des réglages |

## Le voir en local

```bash
python3 -m http.server 8000
```

## Publier une version

Le dépôt du code est privé : **les versions se publient ici.** Une release de ce dépôt, avec le
`.dmg` en pièce jointe sous le nom exact **`Wuji.dmg`**. Deux choses en dépendent :

- les boutons « Télécharger » visent `releases/latest/download/Wuji.dmg` — la dernière release,
  sans rien à changer dans les pages ;
- la vérification de version de l'application lit la dernière release de ce dépôt ;
  l'étiquette doit porter le numéro, `v0.7.5` par exemple.

Le numéro de version écrit dans les pages (l'accueil, « Installer », le pied) se met à jour à
la main.

## Le publier

Le site paraît sur `https://black0s.github.io/Wuji-web/` : le workflow
`.github/workflows/static.yml` le déploie à chaque poussée sur `main`.
