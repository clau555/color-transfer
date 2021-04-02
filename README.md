# Transfert de couleurs entre images par coupe 1D

Un transfert de couleur consiste à transférer les couleurs d'une image source sur une image cible.<br/>
Ici, un pixel de l'image source ne peut être utilisé qu'une fois.<br/>
L'opération revient donc à réorganiser les pixels de l'image source
de manière à ce que le résultat ressemble le plus possible à l'image cible.

## Dépendances

- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

## Utilisation

<img src="monarch.png" width="350"/> <img src="tulips.png" width="350"/>

Faisons un transfert des couleurs de tulips sur monarch, avec 40 tirages de vecteurs aléatoires.
```
python color_transfer.py monarch.png tulips.png 40
```
Sortie
```
initialization...
0       vector : (-22, -4, 5)           cost : 3940552947.0     best cost : 3294499155.0
1       vector : (-40, 46, -46)         cost : 4994295771.0     best cost : 3294499155.0
2       vector : (-12, -11, 34)         cost : 6614810727.0     best cost : 3294499155.0
.
.
.
11      vector : (-20, -5, -14)         cost : 2783448129.0     best cost : 2783448129.0
.
.
.
37      vector : (37, -27, -45)         cost : 6385495563.0     best cost : 2783448129.0
38      vector : (-5, 26, 33)           cost : 3802899065.0     best cost : 2783448129.0
39      vector : (40, -24, -23)         cost : 7649534025.0     best cost : 2783448129.0

best vector : (-20, -5, -14)
quality : 0.36387159268828795
```

L'image de sortie est affichée lors de la fin du programme et est enregistrée dans le fichier output.png.

<img src="output.png" width="600"/>
