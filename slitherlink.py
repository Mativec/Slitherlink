# VECCHIO Matias (Td- C)
# XU Kevin (Td- C)

import fltk
import time

#############################################################
#############  Tâche 1: Structures de données  ##############
#############################################################


def tableau_init(nom):
    """
    prend le nom d'un document, l'ouvre et return un tableau
    nom : string
    return
    indices : list
    """
    print(nom)
    indices = []
    fichier = open(nom + '.txt', 'r')
    texte = fichier.read()
    ligne = texte.split("\n")
    for etat in ligne:
        indices.append(list(etat))
    indices.pop(-1)
    print(indices)
    for ligne in range(len(indices)):
        for colonne in range(len(indices[ligne])):
            if indices[ligne][colonne] == "_":
                indices[ligne][colonne] = None
    fichier.close()
    return indices


def est_vierge(etat, segment):
    """
    Fonction renvoyant True si segment est vierge dans etat, et False sinon
    :param etat: list
    :param segment: tuple
    :return value: bool
    """
    return (etat == {}) or (segment not in etat)


def est_trace(etat, segment):
    """
    Fonction renvoyant True si segment est tracé dans etat, et False sinon
    :param etat: list
    :param segment: tuple
    :return value: bool
    """
    return (not est_vierge(etat, segment)) and (etat[segment] == 1)


def est_interdit(etat, segment):
    """
    Fonction renvoyant True si segment est interdit dans etat, et False sinon
    :param etat: list
    :param segment: tuple
    :return value: bool
    """
    return (not est_vierge(etat, segment) and (etat[segment] == -1))


def tracer_segment(etat, segment):
    """
    Fonction modifiant etat afin de représenter le fait que segment
    est maintenant tracé
    :param etat: list
    :param segment: tuple
    """
    if est_vierge(etat, segment) or est_interdit(etat, segment):
        etat[segment] = 1


def interdire_segment(etat, segment):
    """
    Fonction modifiant etat afin de représenter le fait que segment
    est maintenant interdit
    :param etat: list
    :param segment: tuple
    """
    if est_vierge(etat, segment) or est_trace(etat, segment):
        etat[segment] = -1


def effacer_segment(etat, segment):
    """
    Fonction modifiant etat afin de représenter le fait que segment
    est maintenant vierge
    :param etat: list
    :param segment: tuple
    """
    if est_trace(etat, segment) or est_interdit(etat, segment):
        del etat[segment]


def segments_traces(etat, sommet):
    """
    Fonction  renvoyant la liste des segments tracés adjacents à
    sommet dans etat
    :param etat: list
    :param sommet: tuple
    :return value: list
    """
    liste = []
    for i, j in etat:
        if (est_trace(etat, (i, j))) and (i == sommet or j == sommet):
            liste.append((i, j))
    return sorted(liste)


def segments_interdits(etat, sommet):
    """
    Fonction  renvoyant la liste des segments interdit adjacents à
    sommet dans etat
    :param etat: list
    :param sommet: tuple
    :return value: list
    """
    liste = []
    for i, j in etat:
        if (est_interdit(etat, (i, j))) and (i == sommet or j == sommet):
            liste.append((i, j))
    return sorted(liste)


def segments_vierges(indices, etat, sommet):
    """
    Fonction  renvoyant la liste des segments vierges adjacents à
    sommet dans etat
    :param etat: list
    :param sommet: tuple
    :return value: list
    """
    liste = []
    i, j = sommet
    if i > 0 and est_vierge(etat, o := ((i-1, j), (i, j))):
        liste.append(o)
    if i < len(indices[0]) and est_vierge(etat, e := ((i, j), (i+1, j))):
        liste.append(e)
    if j > 0 and est_vierge(etat, n := ((i, j-1), (i, j))):
        liste.append(n)
    if j < len(indices) and est_vierge(etat, s := ((i, j), (i, j+1))):
        liste.append(s)
    return sorted(liste)


def total_traits(etat):
    """
    Renvoie le nombre de segment tracé total (hors boucle inclus)
    :param etat: dict
    """
    if etat == {}:
        return 0
    cmpt = 0
    for i, j in etat:
        if est_trace(etat, (i, j)):
            cmpt += 1
    return cmpt


def statut_case(indices, etat, case):
    """
    Fonction recevant le tableau d’indices, l’état de la grille et les
    coordonnées d’une case (pas d’un sommet !) et renvoyant None si cette case
    ne porte aucun indice, et un nombre entier sinon
    – 0 si l’indice est satisfait ;
    – >0 s’il est encore possible de satisfaire l’indice
    – <0 s’il n’est plus possible de satisfaire l’indice
    :param indices: list
    :param etat: list
    :param case: tuple
    :return value: int or None
    """
    y, x = case  # coord sommet en haut à gauche de la case
    if x < 0 or x > len(indices[0]) - 1 or y < 0 or y > len(indices) - 1:
        return None
    indice = indices[y][x]
    if indice == '_' or indice is None:
        return None
    else:
        nb_traits = 0
        if est_trace(etat, ((x, y), (x+1, y))):
            nb_traits += 1
        if est_trace(etat, ((x, y), (x, y+1))):
            nb_traits += 1
        if est_trace(etat, ((x+1, y), (x+1, y+1))):
            nb_traits += 1
        if est_trace(etat, ((x, y+1), (x+1, y+1))):
            nb_traits += 1
        return int(indice) - nb_traits

#############################################################
#############  Tâche 2 : conditions de victoire  ############
#############################################################


def longueur_boucle(etat, segment):
    """
    Fonction renvoyant None si le segment n’appartient pas à une boucle, et la
    longueur de la boucle à laquelle il appartient sinon
    """
    if etat == {}:
        return False
    depart = segment[0]
    precedent = segment[0]
    courant = segment[1]
    cmpt = 1
    while courant != depart:
        liste = segments_traces(etat, courant)
        if not len(liste) == 2:
            return None
        else:
            # Remarque -> liste = [(case1, courant), (courant, case2)]
            # ici ce n'est pas le cas
            # ex : [(case1, courant), (case2, courant)]
            if liste[0][1] != liste[1][0]:
                if liste[0][1] == courant:
                    liste[1] = liste[1][::-1]
                else:
                    liste[0] = liste[0][::-1]
            # c'est bon c'est corrigé
            if liste[0][0] == precedent:
                courant = liste[1][1]
            else:
                courant = liste[0][0]
            precedent = liste[0][1]
        cmpt += 1
    return cmpt


def satisfaits_indices(indices, etat):
    """
    Fonction qui renvoie True si tous les indices sont satisfaits, False sinon
    """
    cond_indice = True
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            if indices[i][j] is not None and statut_case(indices, etat, ((i, j))) != 0:
                cond_indice = False
    return cond_indice


def win(indices, etat):
    """
    Fonction qui va détecter automatiquement la fin de la partie.
    La grille est résolue et le joueur a gagné lorsque les deux
    conditions suivantes sont réunies :
    1. Chaque indice est satisfait : chaque case contenant un nombre k compris
    entre 0 et 3 a exactement k côtés tracés.
    2. L’ensemble des segments tracés forme une unique boucle fermée.
    """
    cond_boucle = True
    if etat != {} and longueur_boucle(etat, min(etat)) != total_traits(etat):
        cond_boucle = False
    return satisfaits_indices(indices, etat), cond_boucle

#############################################################
##############  Tâche 3: Interface graphique  ###############
#############################################################


def Choix_grille():
    """
    Fonction qui  permet à l'utilisateur de choisir la grille sur laquelle joué.
    """
    fltk.cree_fenetre(600, 600)
    fltk.texte(10, 10, 'XU Kevin, VECCHIO Matias', taille=10, couleur='blue')
    fltk.texte(300, 100, "Choisissez la grille", taille=20, ancrage="center",
               couleur='blue')

    fltk.rectangle(50, 200, 250, 300, couleur='black', remplissage='white')
    fltk.texte(150, 250, "grille1", taille=12,
               ancrage="center", couleur='black')
    fltk.rectangle(350, 200, 550, 300, couleur='black', remplissage='white')

    fltk.texte(450, 250, "grille2", taille=12,
               ancrage="center", couleur='black')
    fltk.rectangle(50, 400, 250, 500, couleur='black', remplissage='white')

    fltk.texte(150, 450, "grille-triviale", taille=12,
               ancrage="center", couleur='black')
    fltk.rectangle(350, 400, 550, 500, couleur='black', remplissage='white')
    fltk.texte(450, 450, "grille-vide", taille=12,
               ancrage="center", couleur='black')

    fltk.rectangle(250, 325, 350, 375, couleur='black', remplissage='white')
    fltk.texte(300, 350, "Autre", taille=12,
               ancrage="center", couleur='black')
    boucle = True
    while boucle:
        x, y = fltk.attend_clic_gauche()
        if 50 <= x <= 250 and 200 <= y <= 300:
            indices = tableau_init('grille1')
            boucle = False
        elif 350 <= x <= 550 and 200 <= y <= 300:
            indices = tableau_init('grille2')
            boucle = False
        elif 50 <= x <= 250 and 400 <= y <= 500:
            indices = tableau_init('grille-triviale')
            boucle = False
        elif 350 <= x <= 550 and 400 <= y <= 500:
            indices = tableau_init('grille-vide')
            boucle = False
        elif 250 <= x <= 350 and 325 <= y <= 375:
            indices = tableau_init(input('Insérer nom grille(sans le .txt)\t'))
            boucle = False
    fltk.ferme_fenetre()
    return indices


def Init_graph(indices, etat):
    """
    La fonction permet d'initialisé la fenete graphique en interpretent indices
    indices : liste
    """
    fltk.rectangle(0, 0, t_ligne * t_case + 18,
                   t_colonne * t_case + 18, 'white', 'white')
    for i in range(t_colonne):
        for j in range(t_ligne):
            if indices != {} and indices[i][j] is not None:
                statut = statut_case(indices, etat, (i, j))
                couleur = 'black' * (statut > 0) + 'blue' * \
                    (statut == 0) + 'red' * (statut < 0)
                fltk.texte((j + 0.5) * t_case + 6, t_case * (i + 0.5) + 6,
                           str(indices[i][j]), taille=20, ancrage="center",
                           couleur=couleur)
    for i in range(t_colonne + 1):
        for j in range(t_ligne + 1):
            fltk.point(j * t_case + 6, t_case * i + 6, "black", 4)


def calc_position(x, y):
    """
    Calcule la position en x et y sur le tableau et dit s'il est l'horizontal
    ou vertical
    """
    case_x, case_y = x // t_case, y // t_case
    rotation_x, rotation_y = x - (case_x * t_case), y - (case_y * t_case)
    if 0 <= rotation_x <= 14:
        return (case_x, case_y), (case_x, case_y + 1)  # Verticale
    elif 0 <= rotation_y <= 14:
        return (case_x, case_y), (case_x + 1, case_y)  # Horizontale
    else:
        return 0, 0


def calcul_hv(i, p):
    """
    p:string p=>Position  h=horizontal et v=vertical  le x permet de disociée
    avec interdit
    x_p,x_p1 :int
    position en x du debut et fin du segment .
    y_p,y_p1 :int
    position en y du debut et fin du segment .
    """
    x, y = i
    t_case = 100
    if p == "h":
        x_p = x * t_case + 11
        y_p = t_case * y + 7
        x_p1 = (x + 1) * t_case + 2
        y_p1 = t_case * y + 7
    elif p == "v":
        t_case = 100
        x_p = t_case * x + 7
        y_p = y * t_case + 11
        x_p1 = t_case * x + 7
        y_p1 = (y + 1) * t_case + 2
    elif p == "hx":
        x_m = (2 * x * t_case + t_case) / 2
        x_p = x_m + 11
        y_p = y * t_case + 11
        x_p1 = x_m + 2
        y_p1 = y * t_case + 2
    elif p == "vx":
        y_m = (2 * y * t_case + t_case) / 2
        x_p = x * t_case + 11
        y_p = y_m + 11
        x_p1 = x * t_case + 2
        y_p1 = y_m + 2

    return x_p, y_p, x_p1, y_p1


def dessin(indices, etat, couleur):
    """
    Dessine le segment ou une croix à la place si il est interdit
    :param indices: list
    :param etat: list
    """
    Init_graph(indices, etat)
    for i, j in etat:
        if est_trace(etat, (i, j)):
            rotation = 'h' * (i[0] + 1 == j[0]) + 'v' * (i[1] + 1 == j[1])
            x_p, y_p, x_p1, y_p1 = calcul_hv(i, rotation)
            fltk.ligne(x_p, y_p, x_p1, y_p1, couleur=couleur, epaisseur=4)
        elif est_interdit(etat, (i, j)):
            rotation = 'hx' * (i[0] + 1 == j[0]) + 'vx' * (i[1] + 1 == j[1])
            x_p, y_p, x_p1, y_p1 = calcul_hv(i, rotation)
            fltk.ligne(x_p, y_p, x_p1, y_p1, couleur='red', epaisseur=4)
            fltk.ligne(x_p - 9, y_p, x_p1 + 9, y_p1,
                       couleur='red', epaisseur=4)


def clique(indices, etat, ev):
    """
    Fonction qui permet prendre la position du clique puis de le tracer,
    effacer ou dire qu'il est interdit
    :param etat: dict
    """
    touche, action = ev
    if touche == 'ClicGauche':
        case1, case2 = calc_position(action.x, action.y)
        if case1 != 0 and case2 != 0:
            if est_vierge(etat, (case1, case2)):
                tracer_segment(etat, (case1, case2))

            elif est_trace(etat, (case1, case2)) or est_interdit(etat, (case1, case2)):
                effacer_segment(etat, (case1, case2))

    elif touche == 'ClicDroit':
        case1, case2 = calc_position(action.x, action.y)
        if case1 != 0 and case2 != 0:
            if est_vierge(etat, (case1, case2)):
                interdire_segment(etat, (case1, case2))

            elif est_trace(etat, (case1, case2)) or est_interdit(etat, (case1, case2)):
                effacer_segment(etat, (case1, case2))
    else:
        return None
    return etat, case1, case2


#############################################################
############  Tâche 4: Recherche de solutions  ##############
#############################################################

def lst_depart(indices, cible=None, liste=None):
    """
    Fonction qui renvoit la liste des possible points de départ du solveur
    par ordre d'importance.
    """
    if cible is None:
        cible = 3
    if liste is None:
        liste = []
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            if indices[i][j] is not None and int(indices[i][j]) == cible:
                liste.append((j, i))
    if cible == 1:
        liste.append((0, 0))
    else:
        lst_depart(indices, cible - 1, liste)
    return liste


def poseinterdit(indices, etat):
    """
    Fonction qui va poser les interdits selon l'indice de chaque case et
    le nombre de segments tracer autour.
    :param indice: int
    :param ligne: int
    :param colonne: int
    :param etat: dict
    """
    for ligne in range(len(indices)):
        for colonne in range(len(indices[0])):
            indice = indices[ligne][colonne]
            if indice is not None and indice != '_':
                # point en haut à gauche : ligne, colonne = y, x du point
                reste_segment = int(indice)  # nb de segment max

                segment = (colonne, ligne), (colonne + 1, ligne)
                if etat != {} and segment in etat and est_trace(etat, segment):
                    reste_segment -= 1

                segment1 = (colonne, ligne), (colonne, ligne + 1)
                if etat != {} and segment1 in etat and est_trace(etat, segment1):
                    reste_segment -= 1

                segment2 = (colonne, ligne + 1), (colonne + 1, ligne + 1)
                if etat != {} and segment2 in etat and est_trace(etat, segment2):
                    reste_segment -= 1

                segment3 = (colonne + 1, ligne), (colonne + 1, ligne + 1)
                if etat != {} and segment3 in etat and est_trace(etat, segment3):
                    reste_segment -= 1

                if reste_segment == 0:

                    if est_vierge(etat, segment):
                        interdire_segment(etat, segment)

                    if est_vierge(etat, segment1):
                        interdire_segment(etat, segment1)

                    if est_vierge(etat, segment2):
                        interdire_segment(etat, segment2)

                    if est_vierge(etat, segment3):
                        interdire_segment(etat, segment3)


def reset_interdit(etat):
    """
    Efface les interdits autour d'une case
    :param indice: int
    :param ligne: int
    :param colonne: int
    :param etat: dict
    """
    liste = []
    for i, j in etat:
        if est_interdit(etat, (i, j)):
            liste.append((i, j))
    for i, j in liste:
        if est_interdit(etat, (i, j)):
            effacer_segment(etat, (i, j))
    return None


def solveur(indices, solutions, sommet, graphique=None):
    """
    Fonction qui gère le solveur.
    :param indices: list
    :param solutions: dict, le etat du solveur
    :param sommet: tuple
    """
    if graphique is None:
        graphique = False
    reset_interdit(solutions)
    poseinterdit(indices, solutions)

    if graphique:
        fltk.efface_tout()
        dessin(indices, solutions, 'green')
        fltk.mise_a_jour()

    if len(indices) < 3 and len(indices[0]) < 3:
        time.sleep(1/10)  # vitesse

    nb_adjacent = len(segments_traces(solutions, sommet))

    if nb_adjacent == 2:
        if satisfaits_indices(indices, solutions):
            return True
        else:
            return False

    elif nb_adjacent > 2:
        return False

    elif total_traits(solutions) == 0 or nb_adjacent == 1:
        for segment in segments_vierges(indices, solutions, sommet)[::-1]:
            if est_vierge(solutions, segment):
                tracer_segment(solutions, segment)
                if segment[0] == sommet:
                    autre = segment[1]
                else:
                    autre = segment[0]
                if solveur(indices, solutions, autre, graphique):
                    return True
                effacer_segment(solutions, segment)
    return False


if __name__ == '__main__':
    indices = Choix_grille()
    etat = {}
    t_case = 100
    t_ligne = len(indices[0])
    t_colonne = len(indices)
    solution = False
    fltk.cree_fenetre(t_ligne * t_case + 18, t_colonne * t_case + 18)
    conditions = (False, False)
    while not (conditions[0] * conditions[1]) or etat == {}:
        fltk.efface_tout()
        dessin(indices, etat, 'blue')
        ev = fltk.attend_ev()
        if ev[1].keysym == "Return":
            solution = 'normal'
            break
        elif ev[1].keysym == "Shift_R" or ev[1].keysym == "Shift_L":
            solution = 'graphique'
            break
        clique(indices, etat, ev)
        fltk.mise_a_jour()
        conditions = win(indices, etat)
        if conditions[0]:
            print('\n\n\nIndices tous satisfaits')
        else:
            print('\n\n\nIndices encore insatisfaits')
        if conditions[1]:
            print('Segments tracés formant une boucle unique')
        else:
            print('Segments tracés ne formant pas une boucle unique')

        if not conditions[0] or not conditions[1]:
            print("appuyer sur 'Entrée' pour avoir la solution (shift pour la graphique)")
        else:
            print('\nVICTOIRE!!!')

    fltk.efface_tout()
    dessin(indices, etat, 'blue')
    fltk.mise_a_jour()
    if solution == 'normal' or solution == 'graphique':
        solutions = {}
        depart = lst_depart(indices)
        if solution == 'normal':
            while depart != []:
                solveur(indices, solutions, depart[0], False)
                depart = depart[1:]
        elif solution == 'graphique':
            while depart != []:
                solveur(indices, solutions, depart[0], True)
                depart = depart[1:]
        print('\n', solutions, sep='')
        print(total_traits(solutions))
        fltk.efface_tout()
        dessin(indices, solutions, 'green')
        fltk.mise_a_jour()
    fltk.attend_fermeture()
