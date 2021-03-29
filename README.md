# Transfert de couleurs entre images par coupe 1D

## Utilisation

<img src="monarch.png" width="300"/> <img src="tulips.png" width="300"/>

Faisons un transfert des couleurs de tulips sur monarch, avec 20 tirages de vecteur.
```
python color_transfer.py monarch.png tulips.png 20
```
Sortie
```
initialization...
0       vector : (-35, -9, 35)          cost : 8060445121.0     best cost : 3300235319.0
1       vector : (-12, 22, 44)          cost : 4475636187.0     best cost : 3300235319.0
2       vector : (-19, 39, -39)         cost : 5199083393.0     best cost : 3300235319.0
3       vector : (40, -22, -21)         cost : 7594484867.0     best cost : 3300235319.0
4       vector : (-28, -5, -12)         cost : 2811626187.0     best cost : 2811626187.0
5       vector : (-20, -48, 24)         cost : 3834215221.0     best cost : 2811626187.0
6       vector : (8, -24, -35)          cost : 4110067489.0     best cost : 2811626187.0
7       vector : (15, -2, -29)          cost : 6495452977.0     best cost : 2811626187.0
8       vector : (6, -27, -7)           cost : 4327101393.0     best cost : 2811626187.0
9       vector : (27, 19, -43)          cost : 7603852683.0     best cost : 2811626187.0
10      vector : (-49, -17, 28)         cost : 4728738651.0     best cost : 2811626187.0
11      vector : (28, 13, 16)           cost : 2790714639.0     best cost : 2790714639.0
12      vector : (-6, 22, -39)          cost : 4728696691.0     best cost : 2790714639.0
13      vector : (-38, -16, 30)         cost : 5376285339.0     best cost : 2790714639.0
14      vector : (-11, -1, 41)          cost : 5217697053.0     best cost : 2790714639.0
15      vector : (-44, 4, 47)           cost : 7468818843.0     best cost : 2790714639.0
16      vector : (-11, -10, -9)         cost : 2802298555.0     best cost : 2790714639.0
17      vector : (32, -37, 21)          cost : 6488715567.0     best cost : 2790714639.0
18      vector : (46, 21, -11)          cost : 3179848857.0     best cost : 2790714639.0
19      vector : (-36, -8, 16)          cost : 4654813901.0     best cost : 2790714639.0

best vector : (28, 13, 16)
quality : 0.3462233905332733
```

<img src="output.png" width="400"/>
