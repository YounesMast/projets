import pygame
from pygame.locals import *
import random

#initialisation de pygame
pygame.init()
#creation de la fenetre (taille, et autres paramètres optionnels)
pygame.display.set_caption('Battleguild')
ico = pygame.image.load("logo_ico.png")
pygame.display.set_icon(ico)
fenetre = pygame.display.set_mode((800, 480))


#booléen permettant de savoir si on est dans le menu de départ (false), ou dans le menu de combat (true)
mode='intro'

#booléens permettant de savoir dans quel combat on est ou si nous avons gagné
cbt_rencar=False
cbt_codush=False
cbt_thallas=False
cbt_igruk=False
cbt_yatay=False
gagner=False

#booléens permettant de savoir afficher quel descriptif lors du mode 'intro'
pres1=False
pres2=False
pres3=False

#Initialisation des classes
class Adversaire:
    """définit un adversaire"""
    def __init__(self,pv,pa,types,nom,image):
        self.pv = pv
        self.pa = pa
        self.types = types
        self.name = nom
        self.image = image


class Perso:
    """défini un personnage"""

    def __init__(self,pv,pvMax,pa,types,image,nom):
        self.pv=pv
        self.pvMax=pvMax
        self.pa=pa
        self.types=types        
        self.image = image
        self.name = nom

#chargement de l'image de fond
fond = pygame.image.load("bg.png").convert_alpha()
fond = pygame.transform.scale(fond, (800,480))

#chargement des images de présentation
pres_perso1=fond_choix=pygame.image.load("human/humanPresentation.png")
pres_perso2=fond_choix=pygame.image.load("elf/elfPresentation.png")
pres_perso3=fond_choix=pygame.image.load("orc/orcPresentation.png")

#redimension des images de présentation
pres_perso1=pygame.transform.scale(pres_perso1,(167,239))
pres_perso2=pygame.transform.scale(pres_perso2,(167,239))
pres_perso3=pygame.transform.scale(pres_perso3,(167,239))


#chargement des images de combat
imgPerso1=pygame.image.load("human/human.png")
imgPerso2=pygame.image.load("elf/elf.png")
imgPerso3=pygame.image.load("orc/orc.png")


#redimension des images de combat
imgPerso1=pygame.transform.scale(imgPerso1,(238,450))
imgPerso1=pygame.transform.flip(imgPerso1, True, False)
imgPerso2=pygame.transform.scale(imgPerso2,(238,450))
imgPerso2=pygame.transform.flip(imgPerso2, True, False)
imgPerso3=pygame.transform.scale(imgPerso3,(238,450))
imgPerso3=pygame.transform.flip(imgPerso3, True, False)

#initialisation de chaque personnage
perso1=Perso(25,25,5,'homme', imgPerso1, "Medhi")
perso2=Perso(20,20,7,'elfe',imgPerso2, "Hiroki")
perso3=Perso(15,15,10,'orc', imgPerso3, "Caleb")

#chargement des images des adversaires
imgRencar = pygame.image.load("adv/rencar.png")
imgCodush = pygame.image.load("adv/codush.png")
imgThallas = pygame.image.load("adv/thallas.png")
imgIgruk = pygame.image.load("adv/igruk.png")
imgYatay = pygame.image.load("adv/yatay.png")

#redimension des images des adversaires
imgRencar = pygame.transform.scale(imgRencar,(243,320))
imgRencar=pygame.transform.flip(imgRencar, True, False)
imgCodush = pygame.transform.scale(imgCodush,(243,320))
imgCodush= pygame.transform.flip(imgCodush, True, False)
imgThallas = pygame.transform.scale(imgThallas,(243,320))
imgIgruk = pygame.transform.scale(imgIgruk,(243,320))
imgIgruk=pygame.transform.flip(imgIgruk, True, False)
imgYatay = pygame.transform.scale(imgYatay,(243,320))

#initialisation des caractéristiques des adversaires
rencar = Adversaire(30,random.randint(5,8),'humain','Rencar', imgRencar)
codush = Adversaire(25, random.randint(12,15), 'elfe', 'Codush',imgCodush)
thallas = Adversaire(35, random.randint(14,17), 'orc', 'Thallas', imgThallas)
igruk = Adversaire(60,random.randint(8,11),'nain','Igruk', imgIgruk)
yatay = Adversaire(80,random.randint(20,23),'boss', 'Yatay', imgYatay)

#initialisation d'une image de potion
imgPotion=pygame.image.load("potion.png")
imgPotion=pygame.transform.scale(imgPotion, (44,50))

#affichage de l'image de fond
fenetre.blit(fond, (0,0))

#booléen qui permettra la fin du programme et la fermeture de la fenetre
stop = False

#Creation des rectangles cliquables (choix du personnage)
clickable_area1 = pygame.Rect((93,75), (106, 200))
rect_surf1 = pygame.Surface(clickable_area1.size)
clickable_area2 = pygame.Rect((293,75), (106, 200))
rect_surf2 = pygame.Surface(clickable_area2.size)
clickable_area3 = pygame.Rect((570,75), (106, 200))
rect_surf3 = pygame.Surface(clickable_area3.size)

#On rend ces rectangles invisibles en règlant la couche alpha (transparence) sur 0
rect_surf1.set_alpha(0)
rect_surf2.set_alpha(0)
rect_surf3.set_alpha(0)

#création de la zone cliquable pour attaquer dans le mode combat (elle reste en noir, et un texte y sera ajouté plus tard)
zone_attaque = pygame.Rect((500, 90), (243, 320))
rect_attaque = pygame.Surface(zone_attaque.size)
rect_attaque.set_alpha(0)

#création d'une zone parer
zone_parer = pygame.Rect((106,200),(110,48))
rect_parer = pygame.Surface(zone_parer.size)
rect_parer.set_alpha(0)

#création d'une zone potion
zone_potion = pygame.Rect((10,10),(44,100))
rect_potion = pygame.Surface(zone_potion.size)
rect_potion.set_alpha(0)

#création d'un rectangle pour pouvoir augmenter la lisibilité du titre de l'intro
s=pygame.Surface((640, 130))
s.set_alpha(128)
s.fill((0,0,0))

#création d'un rectangle pour pouvoir augmenter la lisibilité du mode pause                               
p=pygame.Surface((800,480))
p.set_alpha(187)
p.fill((0,0,0))

#chargement des textes et polices de caractères qui seront utilisées
pygame.font.init()
myfont = pygame.font.Font("CELTG___.TTF", 25)
myfont2 = pygame.font.Font("CELTG___.TTF", 100)
myfont3 = pygame.font.Font("CELTG___.TTF", 45)
myfont4 = pygame.font.Font("CELTG___.TTF", 30)
myfont5 = pygame.font.SysFont("Comic Sans MS", 25)
titre = myfont2.render("Battleguild", False, (84, 164, 220))
text = myfont.render("Choisissez un personnage !", False, (255, 255, 255))


def textPres(perso):
    """Fonction qui permet d'afficher le descriptif du personnage demandé"""
    #Initialisation des textes
    txt1=myfont5.render(("Le personnage est "+perso.name), False, (255,255,255))
    txt2=myfont5.render(("Il a "+str(perso.pv)+" points de vie"), False, (255,255,255))
    txt3=myfont5.render(("Il a "+str(perso.pa)+" points d'attaque"), False, (255,255,255))
    txt4=myfont5.render(("Et c'est un "+perso.types), False, (255,255,255))
    
    #Affichage des textes
    fenetre.blit(txt1, (80,305))
    fenetre.blit(txt2, (80,325))
    fenetre.blit(txt3, (80,345))
    fenetre.blit(txt4, (80,365))

def aff_combat(adv):
    """Fonction qui permet d'afficher le combat"""
    #Intialisation des textes (PV)
    text2 = myfont.render(str(adv.pv), False, (255, 255, 255))
    text3 = myfont.render(str(hero.pv), False, (255, 255, 255))
    
    #Affichage de tous les éléments
    fenetre.blit(fond, (0,0))
    fenetre.blit(hero.image, (110,48))
    fenetre.blit(adv.image, (500,90))
    fenetre.blit(text2,(600,20))
    fenetre.blit(text3,(220,20))
    fenetre.blit(imgPotion, (10,10))
    fenetre.blit(rect_attaque, zone_attaque)
    fenetre.blit(rect_parer, zone_parer)
    fenetre.blit(rect_potion, zone_potion)
    
def aff_pause2(adv):
    """Fonction qui permet d'afficher le 2eme menu pause, quand le 'hero' a battu un de ses adversaires"""
    #Initialisation des textes
    textWin = myfont3.render("Vous avez battu "+ adv.name+" !", False, (19, 248, 172))
    text = myfont.render("Pressez sur 'Entree' !", False, (255, 255, 255))
    
    #Affichage de tous les éléments
    fenetre.blit(fond, (0,0))
    fenetre.blit(p, (0,0))
    fenetre.blit(textWin, (80,50))
    fenetre.blit(text,(280,380))

def aff_pause(adv):
    """Fonction qui permet d'afficher le menu pause où il est affiché la personne contre qui on combat"""
    #Initialisation des textes
    textWin = myfont4.render("Vous allez vous battre contre "+adv.name+" !", False, (19, 248, 172))
    textDesc = myfont.render(adv.name+" a "+str(adv.pv)+" PV !", False, (248, 19, 19))
    text = myfont.render("Pressez sur 'Entree' !", False, (255, 255, 255))
    
    #Affichage de tous les éléments
    fenetre.blit(fond, (0,0))
    fenetre.blit(p, (0,0))
    if adv==igruk: #Igruk a un trop grand nom donc on le mets un peu plus à gauche pour qu'il puisse paraître au milieu
        fenetre.blit(textWin, (100,50))
    else:
        fenetre.blit(textWin, (80,50))
    fenetre.blit(text,(280,380))
    fenetre.blit(textDesc, (285, 220))


def refresh():
    """fonction raffraichissant tous les affichages de la fenêtre"""
    if mode=='combat':
        if cbt_rencar:
            aff_combat(rencar)
        if cbt_codush:
            aff_combat(codush)
        if cbt_thallas:
            aff_combat(thallas)
        if cbt_igruk:
            aff_combat(igruk)
        if cbt_yatay:
            aff_combat(yatay)
            
    elif mode=='pause2':
        if gagner:
            #Initialisation des textes
            textWin = myfont4.render("Vous avez gagne ! Bien joue !", False, (248, 19, 19))
            text = myfont.render("Pressez sur 'Entree' !", False, (255, 255, 255))
            
            #Affichage des textes et du fond
            fenetre.blit(fond, (0,0))
            fenetre.blit(textWin, (140,50))
            fenetre.blit(text,(280,380))
            
        if cbt_codush:
            aff_pause2(rencar)
        if cbt_thallas:
            aff_pause2(codush)
        if cbt_igruk:
            aff_pause2(thallas)
        if cbt_yatay:
            aff_pause2(igruk)
    
    elif mode=='pause':
        if cbt_rencar:
            aff_pause(rencar)
        if cbt_codush:
            aff_pause(codush)
        if cbt_thallas:
            aff_pause(thallas)
        if cbt_igruk:
            aff_pause(igruk)
        if cbt_yatay:
            aff_pause(yatay)
            
    elif mode=='perdu':   
        #Initialisation des textes
        textPerdu = myfont4.render("Vous avez ete battu. Reposez en paix !", False, (248, 19, 19))
        text = myfont.render("Pressez sur 'Entree' !", False, (255, 255, 255))
        
        #Affichage des textes et du fond
        fenetre.blit(fond, (0,0))
        fenetre.blit(p, (0,0)) 
        fenetre.blit(textPerdu, (70,50))
        fenetre.blit(text,(280,380))
        
        

    else: 
        #Initialisation du text
        text = myfont.render("Choisissez un personnage !", False, (255, 255, 255))
        
        #Affichage des éléments
        fenetre.blit(fond, (0,0))
        fenetre.blit(text,(220,40))
        fenetre.blit(s, (75,300))
        fenetre.blit(titre,(80,300))
        
        #Texte descriptif
        if pres1:
            s.set_alpha(255)
            fenetre.blit(s, (75,300))
            txt=textPres(perso1)
        elif pres2:
            s.set_alpha(255)
            fenetre.blit(s, (75,300))
            txt=textPres(perso2)
        elif pres3:
            s.set_alpha(255)
            fenetre.blit(s, (75,300))
            txt=textPres(perso3)
        else:
            s.set_alpha(128)
        
        #Affichage des images de présentation
        fenetre.blit(pres_perso1, (93,75))
        fenetre.blit(pres_perso2, (293,75))
        fenetre.blit(pres_perso3, (520,75))
        
        #Mise en place des zones cliquables
        fenetre.blit(rect_surf1, clickable_area1)
        fenetre.blit(rect_surf2, clickable_area2)
        fenetre.blit(rect_surf3, clickable_area3)
        


def combat(adv, cbt1, cbt2):
    """Fonction moteur du combat"""
    Parer=False
    ia=False
    if adv.pv==0:
        cbt1=False
        cbt2=True
        repos(adv)
        return ('pause2',cbt1,cbt2)
    if hero.pv==0:
        return('perdu',cbt1,cbt2)
    if event.type == MOUSEBUTTONUP: # sinon, quand on relache le bouton
        if event.button == 1: # on verifie que c'est le bon bouton de souris (1= clique gauche)
            p=True
            if p:
                if zone_attaque.collidepoint(event.pos): #on vérifie que la souris est au dessus du rectangle d'attaque
                    adv.pv = max(0, adv.pv - random.randint(hero.pa, hero.pa+3))
                    p=False
                    ia=True
                if zone_parer.collidepoint(event.pos):
                    Parer=True
                    p=False
                    ia=True
                if zone_potion.collidepoint(event.pos):
                    hero.pv += 200
                    if hero.pv > hero.pvMax:
                        hero.pv = hero.pvMax
                    p=False
                    ia=True
            if not Parer and ia: 
                hero.pv = max(0,hero.pv - adv.pa)
                ia=False
            Parer=False
    return('combat',cbt1,cbt2)

def repos(adv):
    """Fonction qui defini le nombre de pv, et de pa gagné après le gain d'un combat"""
    if adv.name=='Rencar':
        hero.pvMax+=5 #5pv de gagné
        hero.pa+=2 #2pa de gagné
    elif adv.name=='Codush':
        hero.pvMax+=5 #5pv de gagné
        hero.pa+=3 #3pa de gagné
    elif adv.name=='Thallas':
        hero.pvMax+=10 #10pv de gagné
        hero.pa+=5 #5pa de gagné
    elif adv.name=='Igruk':
        hero.pvMax+=25 #25pv de gagné
        hero.pa+=15 #15pa de gagné
    else:
        pass
    hero.pv=hero.pvMax #on ajoute le nombre de pv après le gain du combat



while not stop:
    if mode=='intro': #définition du menu de séléction et ses interactions     

        for event in pygame.event.get():#la boucle de travail se lance et on surveille tous les événements : souris, clavier...
            if event.type == pygame.QUIT: #si on clique sur la croix en haut de la fenêtre, on sort de la boucle
                stop = True
                
            elif event.type==MOUSEMOTION:
                if clickable_area1.collidepoint(event.pos):
                    pres1=True
                    pres2=False
                    pres3=False
                elif clickable_area2.collidepoint(event.pos):
                    pres1=False
                    pres2=True
                    pres3=False
                elif clickable_area3.collidepoint(event.pos):
                    pres1=False
                    pres2=False
                    pres3=True
                else:
                    pres1=False
                    pres2=False
                    pres3=False

            elif event.type == MOUSEBUTTONUP: # sinon, quand on relache le bouton
                if event.button == 1: # on verifie que c'est le bon bouton de souris (1= clique gauche)
                    if clickable_area1.collidepoint(event.pos): #on vérifie que la souris est au dessus du rectangle1
                            mode='pause'
                            cbt_rencar=True
                            hero=perso1
                    elif clickable_area2.collidepoint(event.pos): #on vérifie que la souris est au dessus du rectangle2
                            mode='pause'
                            cbt_rencar=True
                            hero=perso2
                    elif clickable_area3.collidepoint(event.pos): #on vérifie que la souris est au dessus du rectangle3
                            mode='pause'
                            cbt_rencar=True
                            hero=perso3
                    
                    


    elif mode=='combat': #définition des interactions en mode combat
        for event in pygame.event.get():#la boucle de travail se lance et on surveille tous les événements : souris, clavier...
            if event.type == pygame.QUIT: #si on clique sur la croix en haut de la fenêtre, on sort de la boucle
                stop = True

            if cbt_rencar:
                mode,cbt_rencar,cbt_codush=combat(rencar, cbt_rencar, cbt_codush)
            elif cbt_codush:
                mode,cbt_codush,cbt_thallas=combat(codush, cbt_codush, cbt_thallas)
            elif cbt_thallas:
                mode,cbt_thallas,cbt_igruk=combat(thallas, cbt_thallas, cbt_igruk)
            elif cbt_igruk:
                mode,cbt_igruk,cbt_yatay=combat(igruk, cbt_igruk, cbt_yatay)
            elif cbt_yatay:
                mode,cbt_yatay,gagner=combat(yatay, cbt_yatay, gagner)
                            
    elif mode=='pause2':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if gagner==True:
                        stop = True
                    else:
                        mode='pause'
    
    elif mode=='pause':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    mode='combat'
    
    elif mode=='perdu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    stop = True

    refresh()
    pygame.display.flip()

pygame.quit() #toujours quitter pygame à la fin