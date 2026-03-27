# music_space

Exploration de donnees sur les exoplanetes a partir du catalogue Open Exoplanet Catalogue.

## Ce que nous avons fait

Nous avons construit une premiere base de travail dediee uniquement aux exoplanetes.

Pour cela, nous avons utilise une table CSV derivee du catalogue Open Exoplanet Catalogue :

`https://raw.githubusercontent.com/OpenExoplanetCatalogue/oec_tables/master/comma_separated/open_exoplanet_catalogue.txt`

Le script [export_planets.py](c:/Users/Alexandre%20SCHOHN/Dropbox/Music_space/open_exoplanet_catalogue/scripts/export_planets.py) :

- lit cette table avec `pandas`
- conserve uniquement les colonnes utiles a notre analyse
- renomme certaines colonnes en francais
- ajoute une colonne `type`
- exporte le resultat dans un fichier CSV exploitable

Cette approche nous convient car notre objectif, a cette etape, est de travailler uniquement sur les exoplanetes et non sur toute la structure XML complete du catalogue.

## Colonnes retenues

Le jeu de donnees final repose sur les colonnes suivantes :

| Colonne finale | Colonne source | Signification |
| --- | --- | --- |
| `nom` | `name` | Nom de l'exoplanete |
| `distance` | `system_distance` | Distance du systeme planetaire par rapport au Soleil |
| `ascension_droite` | `system_rightascension` | Ascension droite du systeme |
| `declinaison` | `system_declination` | Declinaison du systeme |
| `masse` | `mass` | Masse de l'exoplanete |
| `temperature` | `temperature` | Temperature de l'exoplanete |
| `type` | valeur ajoutee dans le script | Type d'objet. Ici, toutes les lignes valent `planet` |

## Pourquoi ces colonnes

Nous avons retenu ces variables car elles permettent de decrire simplement chaque exoplanete :

- `nom` identifie l'objet
- `distance`, `ascension_droite` et `declinaison` localisent le systeme d'appartenance
- `masse` et `temperature` apportent des informations physiques utiles
- `type` rend la table explicite et facilite d'eventuels ajouts futurs

## Choix de ne pas garder certaines variables

Nous avons choisi de ne pas conserver `age` dans cette premiere version, car cette information etait trop peu renseignee dans les donnees extraites et n'etait pas assez exploitable.

## Resultat

Le resultat est un fichier CSV simplifie, adapte a une premiere phase d'exploration, de tri, de filtrage et de visualisation des exoplanetes.
