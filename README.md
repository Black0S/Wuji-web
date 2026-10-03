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
en/                         le site en anglais — fabriqué, ne pas le modifier à la main
i18n/en.json                le dictionnaire : chaque bloc de texte français, et son anglais
tools/traduire.py           refait en/ depuis les pages françaises
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

Une seule série, prise dans Wuji le 1er octobre 2026 avec CleanShot : chaque fenêtre porte son
ombre et ses coins, sur fond transparent — le CSS n'en ajoute donc aucune. Les fenêtres du
navigateur sont réduites à 2000 pixels de large, celles des réglages à 1600, « À propos » garde
sa taille. Pour en changer une : garder son nom, et corriger sa taille dans `TAILLES` du
générateur si le rapport change — `width` et `height` réservent la place avant le chargement.

| capture | ce qu'elle montre |
|---|---|
| `fenetre.png` | la fenêtre : un dossier d'onglets, un article (accueil, Naviguer) |
| `favoris.png` | les deux colonnes, les favoris à droite |
| `colonnes-reduites.png`, `colonne-reduite.png` | les colonnes réduites à leurs icônes |
| `personnaliser.png` | la carte Personnaliser l'interface |
| `double-page.png` | deux pages côte à côte |
| `zen.png` | le mode zen |
| `lune.png` | une page rendue sombre par la lune |
| `lecture.png` | le mode lecture |
| `outils.png`, `outils-fenetre.png` | les outils de développement, sous la page et détachés |
| `reseau.png`, `reseau-requetes.png` | l'onglet Réseau, regroupé et détaillé |
| `general.png`, `apparence.png`, `barre-adresse.png`, `performances.png`, `confidentialite.png`, `espaces.png` | les réglages de Wuji |
| `sites-web.png`, `autorisations.png`, `mots-de-passe.png` | les réglages des sites |
| `blocage.png`, `regles.png`, `scripts.png`, `script.png` | le contenu : blocage, mes règles, scripts |
| `a-propos.png` | la fenêtre À propos, et le nom |

## En anglais

**Le français est la source, l'anglais se fabrique.** Les pages de `en/` sont les pages
françaises, texte remplacé bloc par bloc d'après `i18n/en.json` : la mise en page ne peut pas
diverger. Chaque page porte « English » ou « Français » dans sa barre, qui mène à la même page
dans l'autre langue, et les balises `hreflang` qui le disent aux moteurs de recherche.

Après avoir modifié une page française — un texte, une carte, le numéro de version :

```bash
python3 tools/traduire.py --extraire   # ajoute les textes nouveaux à i18n/en.json, vides
# … traduire les entrées vides dans i18n/en.json …
python3 tools/traduire.py              # refait en/ ; liste ce qui reste à traduire
```

Tant qu'un texte n'est pas traduit, la page anglaise le montre en français, et la commande le
liste et rend une erreur : rien n'est inventé, rien ne passe en silence. Une traduction garde
les balises de son bloc telles quelles — liens, `<code>`, `<kbd>`. Les captures restent celles
de l'interface française.

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
  l'étiquette doit porter le numéro, `v1.0.0` par exemple.

Le numéro de version écrit dans les pages (l'accueil, « Installer », le pied) se met à jour à
la main — puis `tools/traduire.py` pour l'anglais, voir plus haut.

## Le publier

Le site paraît sur `https://black0s.github.io/Wuji-web/` : le workflow
`.github/workflows/static.yml` le déploie à chaque poussée sur `main`.
