# <span style="color: red">WARNING : slow script</span>

# Transfert de couleurs entre images par coupe 1D

Un transfert de couleur consiste à transférer les couleurs d'une image source sur une image cible.<br/>
Ici, un pixel de l'image source ne peut être utilisé qu'une fois.<br/>
L'opération revient donc à réorganiser les pixels de l'image source
de manière à ce que le résultat ressemble le plus possible à l'image cible.

## Dépendance

- [Pillow](https://pypi.org/project/Pillow/) ```pip install pillow```

## Utilisation

<img src="space.jpg" width="320" alt="img"/> <img src="sky.jpg" width="320" alt="img"/>

Faisons un transfert des couleurs avec space.jpg en image cible et clouds.jpg en image source.
```
python color_transfer.py monarch.png tulips.png
```
Sortie
```
initialization...

1       vector : (-22, -4, 5)           cost : 3940552947.0     best cost : 3294499155.0
2       vector : (-40, 46, -46)         cost : 4994295771.0     best cost : 3294499155.0
...
5      vector : (-20, -5, -14)         cost : 2783448129.0     best cost : 2783448129.0
...
9      vector : (-5, 26, 33)           cost : 3802899065.0     best cost : 2783448129.0
10      vector : (40, -24, -23)         cost : 7649534025.0     best cost : 2783448129.0

best vector : (-20, -5, -14)
```

L'image de sortie est affichée lors de la fin du programme et est enregistrée dans le fichier output.png.

<img src="output.png" width="640" alt="img"/>

## Limites

L'algorithme utilisé ici est naïf et ne tire aucun avantage de rapidité de calcul
qu'aurait pu donner la bibliothèque numpy de python par exemple.<br/>
De ce fait, le script est d'autant plus lent que la taille des images à analyser est grande.
