#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET,
auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "Ethan Maridat"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "Ethan Maridat"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Ethan Maridat"
__email__ = "ethanmrdt@gmail.com"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys
from constante import *

# Classe Tetris
class Jeu:
    """
	[Il manque la documentation de la classe]
	"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(TAILLE_FENETRE)
        self.fonts = {
            'defaut': pygame.font.Font('freesansbold.ttf', 18),
            'titre': pygame.font.Font('freesansbold.ttf', 100),
        }
        pygame.display.set_caption('Application Tetris')

    def start(self):
        self._afficher_texte('Tetris', CENTRE_FENETRE, font='titre')
        self._afficher_texte('Appuyer sur une touche...', POS)
        self._attente()

    def stop(self):
        #Méthode permettant de stoper le jeu une fois perdu
        self._afficher_texte('Perdu', CENTRE_FENETRE, font='titre')
        self._attente()
        self._quitter()

    def _afficher_texte(self, text, position, couleur=9, font='defaut'):
        #		print("Afficher Texte")
        font = self.fonts.get(font, self.fonts['defaut'])
        couleur = COULEURS.get(couleur, COULEURS[9])
        rendu = font.render(text, True, couleur)
        rect = rendu.get_rect()
        rect.center = position
        self.surface.blit(rendu, rect)

    def _get_event(self):
        # Cette méthode gère les événements Pygame,
        # notamment la fermeture de la fenêtre et les touches du clavier.
        for event in pygame.event.get():
            if event.type == QUIT:
                self._quitter()
            if event.type == KEYUP:

                if event.key == K_ESCAPE:
                    self._quitter()
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    continue
                return event.key

    def _quitter(self):
        #Fonction permettant de fermer la page du jeu
        print("Quitter")
        pygame.quit()
        sys.exit()

    def _rendre(self):
        pygame.display.update()
        self.clock.tick()

    def _attente(self):
        print("Attente")
        while self._get_event() == None:
            self._rendre()

    def _get_piece(self):
        # Cette méthode retourne une pièce Tetris aléatoire parmi les pièces disponibles.
        return PIECES.get(random.choice(PIECES_KEYS))

    def _get_current_piece_color(self):
        # Cette méthode retourne la couleur de la pièce Tetris actuelle.
        for ligne in self.current[0]:
            for case in ligne:
                if case != 0:
                    return case
        return 0

    def _calculer_donnees_piece_courante(self):
        # Cette méthode calcule les coordonnées de la pièce Tetris actuelle en fonction de sa position et de son orientation.
        m = self.current[self.position[2]]
        coords = []
        for i, ligne in enumerate(m):
            for j, case in enumerate(ligne):
                if case != 0:
                    coords.append([i + self.position[0], j + self.position[1]])
        self.coordonnees = coords

    def _est_valide(self, x=0, y=0, rotation=0):
        # Cette méthode vérifie si la position d'une pièce est valide.
        largeur_plateau, hauteur_plateau = DIM_PLATEAU

        if rotation == 0:
            coordonnees = self.coordonnees
        else:
            couche_rotation = self.current[(self.position[2] + rotation) % len(self.current)]
            coords = []

            for i, ligne in enumerate(couche_rotation):
                for j, cellule in enumerate(ligne):
                    if cellule != 0:
                        coords.append([i + self.position[0], j + self.position[1]])

            coordonnees = coords

        for cx, cy in coordonnees:
            if not 0 <= x + cx < largeur_plateau:
                # La pièce dépasse les limites horizontales du plateau.
                return False
            elif cy < 0:
                # La pièce dépasse les limites verticales supérieures du plateau.
                continue
            elif y + cy >= hauteur_plateau:
                # La pièce dépasse les limites verticales inférieures du plateau.
                return False
            else:
                if self.plateau[cy + y][cx + x] != 0:
                    # La position est déjà occupée sur le plateau.
                    return False
        
        # Si toutes les vérifications ont réussi, la position est valide.
        return True


    def _poser_piece(self):
        # Cette méthode est appelée lorsque la pièce atteint la fin de sa chute et doit être placée sur le plateau.
        print("La pièce est posée")
        if self.position[1] <= 0:
            self.perdu = True
        # Ajout de la pièce parmi le plateau
        couleur = self._get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur
        completees = []
        # calculer les lignes complétées
        for i, line in enumerate(self.plateau[::-1]):
            for case in line:
                if case == 0:
                    break
            else:
                print(self.plateau)
                print(">>> %s" % (DIM_PLATEAU[1] - 1 - i))
                completees.append(DIM_PLATEAU[1] - 1 - i)
        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * DIM_PLATEAU[0])
        # calculer le score et autre
        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / 10) + 1
        if lignes >= 4:
            self.tetris += 1
            self.score += self.niveau * self.tetris
        # Travail avec la pièce courante terminé
        self.current = None

    def _first(self):
        # Cette méthode initialise le jeu en créant un plateau vide et en définissant les statistiques à zéro.
        self.plateau = [[0] * DIM_PLATEAU[0] for i in range(DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
        self.current, self.next, self.perdu = None, self._get_piece(), False

    def _next(self):
        #Prochaine Pièce
        print("Piece suivante")
        self.current, self.next = self.next, self._get_piece()
        self.pieces += 1
        self.position = [int(DIM_PLATEAU[0] / 2) - 2, -4, 0]
        self._calculer_donnees_piece_courante()
        self.dernier_mouvement = self.derniere_chute = time.time()

    def _gerer_evenements(self):
        # Cette méthode gère les événements du jeu, tels que les mouvements de la pièce et la pause.
        event = self._get_event()
        if event == K_p:  #Appuie sur P pour mettre pause
            print("Pause")
            self.surface.fill(COULEURS.get(0))
            self._afficher_texte('Pause', CENTRE_FENETRE, font='titre')
            self._afficher_texte('Appuyer sur une touche...', POS)
            self._attente()
        elif event == K_LEFT:  #Appuie sur flèche de gauche pour deplacer vers la gauche
            print("Mouvement vers la gauche")
            if self._est_valide(x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:  #Appuie sur flèche de droite pour deplacer vers la droite
            print("Mouvement vers la droite")
            if self._est_valide(x=1):
                self.position[0] += 1
        elif event == K_DOWN:  #Appuie sur flèche du bas pour deplacer vers le bas
            print("Mouvement vers le bas")
            if self._est_valide(y=1):
                self.position[1] += 1
        elif event == K_UP:  #Appuie sur flèche du haut pour tourner la pièce
            print("Mouvement de rotation")
            if self._est_valide(rotation=1):
                self.position[2] = (self.position[2] + 1) % len(self.current)
        elif event == K_SPACE:  #Appuie sur espace pour faire descendre la pièce
            print("Mouvement de chute %s / %s" %
                  (self.position, self.coordonnees))
            if self.position[1] <= 0:
                self.position[1] = 1
                self._calculer_donnees_piece_courante()
            a = 0
            while self._est_valide(y=a):
                a += 1
            self.position[1] += a - 1
        self._calculer_donnees_piece_courante()

    def _gerer_gravite(self):
        if time.time() - self.derniere_chute > 0.35:
            self.derniere_chute = time.time()
            if not self._est_valide():
                print("On est dans une position invalide")
                self.position[1] -= 1
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            elif self._est_valide() and not self._est_valide(y=1):
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            else:
                print("On déplace vers le bas")
                self.position[1] += 1
                self._calculer_donnees_piece_courante()

    def _dessiner_plateau(self):
        self.surface.fill(COULEURS.get(0))
        pygame.draw.rect(self.surface, COULEURS[8],
                         START_PLABORD + TAILLE_PLABORD, BORDURE_PLATEAU)
        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = COULEURS[case]
                position = j, i
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        if self.current is not None:
            for position in self.coordonnees:
                couleur = COULEURS.get(self._get_current_piece_color())
                coordonnees = tuple([
                    START_PLATEAU[k] + position[k] * TAILLE_BLOC[k]
                    for k in range(2)
                ])
                pygame.draw.rect(self.surface, couleur,
                                 coordonnees + TAILLE_BLOC)
        self.score, self.pieces, self.lignes, self.tetris, self.niveau  
        self._afficher_texte('Score: >%s' % self.score, POSITION_SCORE)
        self._afficher_texte('Pièces: %s' % self.pieces, POSITION_PIECES)
        self._afficher_texte('Lignes: %s' % self.lignes, POSITION_LIGNES)
        self._afficher_texte('Tetris: %s' % self.tetris, POSITION_TETRIS)
        self._afficher_texte('Niveau: %s' % self.niveau, POSITION_NIVEAU)

        self._rendre()

    def play(self):
        print("Jouer")
        self.surface.fill(COULEURS.get(0))
        self._first()
        while not self.perdu:
            if self.current is None:
                self._next()
            self._gerer_evenements()
            self._gerer_gravite()
            self._dessiner_plateau()

if __name__ == '__main__':
    j = Jeu()
    print("Jeu prêt")
    j.start()
    print("Partie démarée")
    j.play()
    print("Partie terminée")
    j.stop()
    print("Arrêt du programme")
