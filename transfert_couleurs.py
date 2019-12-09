#!/usr/bin/env python

from PIL import Image
from random import randint
from operator import itemgetter
import time

best_u = (0,0,0)
quality = 0

"""
    Légende :
    im : image
    _RGB : objet image en rgb
    _rgb : liste de tuples rgb
    _ord : _rgb ordonné selon u
    u : vecteur tiré aléatoirement
    cost : coût
    _cur : courant
"""



def intro(fichier1, fichier2):
    """ Entrées : deux fichiers image
        Sortie : booléen
        Vérifie la compatibilité de taille et mode des deux images """

    im1 = Image.open(fichier1)
    im2 = Image.open(fichier2)

    print()
    print("=== Image A ===\nFormat : {}\nTaille : {}\nMode : {}".format(im1.format, im1.size, im1.mode))
    print()
    print("=== Image B ===\nFormat : {}\nTaille : {}\nMode : {}".format(im2.format, im2.size, im2.mode))
    print()
    if im1.size==im2.size :
        print("Fichiers OK")
        print()
        res = True
    else :
        print("ATTENTION, incompatibilité des fichiers")
        res = False

    im1.close()
    im2.close()
    return res



def to_rgb(im):
    """ Entrée : image
        Sortie : liste de tuples
        Convertie un objet image en liste rgb """

    im_RGB = im.convert('RGB')
    size = [ im_RGB.size[0], im_RGB.size[1] ]
    im_rgb = []

    for j in range (0, size[1]):
        for i in range (0, size[0]):
            pix = im_RGB.getpixel((i, j))
            im_rgb.append(pix)

    return(im_rgb)



def to_ord(im1_rgb, im2_rgb, u):
    """ Entrée : deux listes de tuples et un tuple (vecteur)
        Sortie : un tuple de deux listes de tuples
        Ordonne deux listes rgb selon un vecteur u """

    im1_ord = []
    im2_ord = []

    for i in range(0,len(im1_rgb)):
        px1_ord = ( im1_rgb[i][0]*u[0] + im1_rgb[i][1]*u[1] + im1_rgb[i][2]*u[2], im1_rgb[i][0], im1_rgb[i][1], im1_rgb[i][2], i )
        im1_ord += [px1_ord]

        px2_ord = ( im2_rgb[i][0]*u[0] + im2_rgb[i][1]*u[1] + im2_rgb[i][2]*u[2], im2_rgb[i][0], im2_rgb[i][1], im2_rgb[i][2], i )
        im2_ord += [px2_ord]

    im1_ord.sort()
    im2_ord.sort()

    for i in range(0,len(im1_ord)):
        #im2_ord[i][4] = im1_ord[i][4]
        #im2_ord[i] = tuple(im2_ord[i])
        im2_ord[i] = (im2_ord[i][0],im2_ord[i][1],im2_ord[i][2],im2_ord[i][3],im1_ord[i][4])

    return(im1_ord, im2_ord)



def cost(im1_rgb, im2_rgb, u):
    """ Entrée : deux listes de tuples et un tuple
        Sortie : un entier
        Calcul le coût entre deux listes rgb selon un vecteur u """

    im12_ord = to_ord(im1_rgb, im2_rgb, u)
    im1_ord = im12_ord[0]
    im2_ord = im12_ord[1]
    dist = 0.0
    for i in range (0, len(im1_rgb)):
        #dist += 1.0*(im1_ord[i][1]-im2_ord[i][1])**2 + 1.0*(im1_ord[i][2]-im2_ord[i][2])**2 + 1.0*(im1_ord[i][3]-im2_ord[i][3])**2
        dist += 0.3*(im1_ord[i][1]-im2_ord[i][1])**2 + 0.58*(im1_ord[i][2]-im2_ord[i][2])**2 + 0.12*(im1_ord[i][3]-im2_ord[i][3])**2

    return dist



def best_cost(im1_rgb, im2_rgb):
    """ Entrée : deux listes de tuples
        Sortie : un entier
        Calcul le meilleur coût entre deux listes rgb """

    global best_u

    u = (randint(-500,500), randint(-500,500), randint(-500,500)) # rand en flottant !
    best_cost = cost(im1_rgb, im2_rgb, u)


    nb_u = 20 # nombre de tirages de u
    cost_list = [] # liste de tout les coûts que l'on va calculer
    for i in range(0, nb_u):
        # print("Calcul du meilleur coût en cours {}/{}".format(i+1, nb_u))
        u = (randint(-500,500), randint(-500,500), randint(-500,500))
        cost_cur = cost(im1_rgb, im2_rgb, u)
        cost_list += [ cost_cur ]

        # echo
        print( i+1, best_cost, cost_cur )

        if cost_cur < best_cost :
            best_cost = cost_cur
            best_u = u

    quality = min(cost_list) / max(cost_list)

    print()
    print("Meilleur vecteur u :", best_u)
    print("Qualité :", quality)
    print()
    return best_cost



def new_image(fichier1, fichier2, fichier3):
    """ Entrées : deux fichiers image, puis le nom du fichier créé
        Sortie : rien
        Créer un fichier en transférant la palette du fichier 2 vers le fichier 1 """

    global best_u

    # echo
    inittime = time.time()
    print ('init',inittime)

    im1 = Image.open(fichier1)
    im2 = Image.open(fichier2)

    im1_rgb = to_rgb(im1)
    im2_rgb = to_rgb(im2)

    # echo
    intime = time.time() - inittime
    print ('toRgb ',intime)
    print()

    best_cost(im1_rgb, im2_rgb)

    # echo
    intime = time.time() - inittime
    print ('best_cost ',intime)

    # on récuperre les deux listes ordonnées par le meilleur vercteur
    var = to_ord(im1_rgb, im2_rgb, best_u)
    im1_ord = var[0]
    im2_ord = var[1]
    im3_rgb = [0]*len(im1_ord)

    # echo
    intime = time.time() - inittime
    print ('to_ord ',intime)

    im2_ord.sort(key=itemgetter(4))

    im3_rgb = im2_ord
    for i in range(0,len(im2_ord)):
        im3_rgb[i] = im2_ord[i][1:4]
        im3_rgb[i] = tuple(im3_rgb[i])


    # echo
    intime = time.time() - inittime
    print ('im3_rgb ',intime)

    im3 = Image.new(im1.mode, im1.size)
    im3.putdata(im3_rgb)

    # echo
    intime = time.time() - inittime
    print ('im3 ',intime)

    print()
    print("sauvegarde du nouveau fichier")
    im3.save(fichier3, "BMP")
    print("Fin")

    im1.close()
    im2.close()


def main():
    fichier1 = input("Entrez le nom/chemin du fichier image à recolorer (image A)\n")
    fichier2 = input("Entrez le nom/chemin du fichier image palette (image B)\n")
    fichier3 = input("Entrez le nom/chemin souhaité du fichier image de sortie\n")
    if intro(fichier1, fichier2):
        new_image(fichier1, fichier2, fichier3)

main()