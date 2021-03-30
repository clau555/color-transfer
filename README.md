# Transfert de couleurs entre images par coupe 1D

Un transfert de couleur consiste à transférer les couleurs d'une image source sur une image cible.<br/>
Ici, un pixel de l'image source ne peut être utilisé qu'une fois.<br/>
L'opération revient donc à réorganiser les pixels de l'image source
de manière à ce que le résultat ressemble le plus possible à l'image cible.

## Dépendances

- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

## Utilisation

<img src="monarch.png" width="350"/> <img src="tulips.png" width="350"/>

Faisons un transfert des couleurs de tulips sur monarch, avec 10 tirages de vecteurs aléatoires.
```
python color_transfer.py monarch.png tulips.png 10
```
Sortie
```
initialization...
0       vector : (-38, -14, -36)        cost : 2784094891.0     best cost : 2784094891.0
1       vector : (-18, 49, 46)          cost : 4268187515.0     best cost : 2784094891.0
2       vector : (11, 27, 36)           cost : 3058036397.0     best cost : 2784094891.0
3       vector : (7, -24, -16)          cost : 4192963159.0     best cost : 2784094891.0
4       vector : (-15, -40, 39)         cost : 6917477127.0     best cost : 2784094891.0
5       vector : (31, -42, 48)          cost : 5106665427.0     best cost : 2784094891.0
6       vector : (-26, 49, 16)          cost : 5383925421.0     best cost : 2784094891.0
7       vector : (-18, 10, -1)          cost : 5281800411.0     best cost : 2784094891.0
8       vector : (15, -31, 4)           cost : 6920590813.0     best cost : 2784094891.0
9       vector : (-16, -34, 22)         cost : 4226440309.0     best cost : 2784094891.0

best vector : (-38, -14, -36)
quality : 0.40229150461694835
```

L'image de sortie est affichée lors de la fin du programme et est enregistrée dans le fichier output.png.

<img src="output.png" width="600"/>
