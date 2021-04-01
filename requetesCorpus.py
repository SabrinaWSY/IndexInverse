#!/usr/bin/env python
# coding: utf-8
# Projet du groupe : Siyu Wang et Natia Davitashvili
import traitementCommun as trc
import time
from collections import Counter
# ------------------------------------------------------------------------------------------------------
#   script de requêtes
#   Usage : python3 requetesCorpus.py 
# ------------------------------------------------------------------------------------------------------

# -------------------------- Traitement de requête utilisateur ---------------------------------

# récupérer 3 listes de mots : mots obligatoires, mots interdits et mots optionnels
def get_wordlists(keywords):
    word_oblig = list()
    word_option = list()
    word_interdit = list()

    for word in keywords:
        word = word.lower()
        if word.startswith("+"): word_oblig.append(word.strip('+'))
        elif word.startswith("-"): word_interdit.append(word.strip('-'))
        else: word_option.append(word)

    return word_oblig, word_interdit, word_option


# récupérer un dicionnaire avec le mots comme clé et les documents contenant le mot comme valeur
def get_docs_words(wordlist,index_termes):
    word_dict = dict()

    for w in wordlist:
        if w not in index_termes.keys():
            print("Désolé, il y a pas de fichier contenant le mot '"+w+"' dans notre corpus.")
        else:
            list_docs = index_termes[w]
            list_docs_sorted = sorted(list_docs, key = lambda i: i['fréquence'],reverse=True) 
            word_dict[w]=list_docs_sorted

    return word_dict


# récupérer une liste de fichiers qui contiennent tous les mots obligatoires
def get_docs_obli(nb_word_obli,word_obli_dict):
    list_docs_obli = list()
    for x in range(nb_word_obli):
        l = list(word_obli_dict.values())[x]
        for i in l:
            idl = list(i.values())[0]
            list_docs_obli.append(idl)

    cnt = Counter(list_docs_obli)
    list_docs_final = list()

    for k,v in cnt.items():
        if v == nb_word_obli:
            list_docs_final.append(k)
    return list_docs_final


# récupérer une liste de fichiers qui contiennent tous les mots optionnels
def get_docs_option(nb_word_option,word_option_dict):
    list_docs_option = list()
    for x in range(nb_word_option):
        l = list(word_option_dict.values())[x]
        for i in l:
            idl = list(i.values())[0]
            if idl not in list_docs_option:
                list_docs_option.append(idl)

    return list_docs_option


# obtenir l'indexdocs avec l'id d'article comme clé et le titre d'article comme valeur
def get_indexdocs():
    indexDocs = trc.lireJson('./documentsIndexes/IndexDocs.json')
    indexdocs = dict()
    for i in indexDocs.values():
        for x in i.values():
            indexdocs[list(x.values())[0]]=list(x.values())[1]

    return indexdocs


# PROCESSUS DE TRAITEMENT POUR LES MOTS OPTIONNELS
def traitement_mots_option(word_option,index_termes,list_docs_obli,langue,word_oblig):

    # s'il y a bien les mots optionnels dans la requête
    if len(word_option)!=0:

        # récupérer un dicionnaire avec le mots optionnels comme clé et les documents correspondants comme valeur
        word_option_dict = get_docs_words(word_option,index_termes)

        # si les mots optionnels sont bien trouvés dans le corpus
        if len(word_option_dict) != 0:

            # obtenir le nombre des mots optionnels de la requête
            nb_word_option = len(word_option)

            # récupérer une liste de documents contenant les mots optionnels
            list_docs_option = get_docs_option(nb_word_option,word_option_dict)
            
            list_trouve = list()
            for o in list_docs_option:
                if o in list_docs_obli:
                    list_trouve.append(o)

            # si les fichiers obligatoires contient bien les mots optionnels
            if len(list_trouve)!= 0: 
                docs_perti = get_docs_by_obli(list_docs_obli,langue,word_oblig,word_option)

            # si aucun fichier obligatoire contient les mots optionnels
            else: 
                print("Aucun doc obligatoire contient les mots optionnels, retourne la liste obligatoire sans mots optionnels ")
                docs_perti = get_docs_by_obli(list_docs_obli,langue,word_oblig,word_option)
        
        # si pas de mots optionnels dans le corpus
        else:
            docs_perti = get_docs_by_obli(list_docs_obli,langue,word_oblig,word_option)

    # si pas de mots optionnels dans la requête
    else:
        docs_perti = get_docs_by_obli(list_docs_obli,langue,word_oblig,word_option)
        

# RECUPÉRER UN DICIONNAIRE DE PERTINENCE ORDONNÉE ET AFFICHER LES RÉSULTATS
def get_docs_by_obli(liste_docs,langue,word_oblig,word_option):
    index_tous_document = trc.lireJson('./documentsIndexes/index_par_document_'+langue+'.json')
    newdict = dict()
    for k,v in index_tous_document.items():
        if k in liste_docs:
            freqlist = dict()
            for w,f in v.items():
                if len(word_oblig)!=0:
                    for m in word_oblig:
                        if m == w:
                            freqlist[m]=f
                if len(word_option)!=0:
                    for o in word_option:
                        if o == w:
                            freqlist[o]=f
            newdict[k]=freqlist

    # calculer la somme des fréquences de tous les mots obligatoires
    new = dict()
    for a,f in newdict.items():
        nb_occ = sum(f.values())
        new[a]=nb_occ

    new = {k: v for k, v in sorted(new.items(), key=lambda item: item[1],reverse=True)}

    # obtenir un dicionnaire ordonné par la fréquence des mots
    dict_sorted = dict()
    for k in new.keys():
        dict_sorted[k] = newdict[k]

    # obtenir l'indexdocs avec l'id d'article comme clé et le titre d'article comme valeur
    indexdocs = get_indexdocs()

    # obtenir un dictionnaire avec les scores et les titres
    dict_score_titre = dict()
    for b in range(len(dict_sorted)):
        doc = list(dict_sorted.keys())[b]
        dict_score_titre[doc]={'score':100-(b*2), 'titre':indexdocs[doc]}

    # print au format de résultat demandé
    print('-'*50)
    print('Nombre de documents trouvés : '+ str(len(dict_score_titre)))
    for x,y in dict_score_titre.items():
        print('ID : {}\t Score : {}\t Titre : {}'.format(x,y['score'],y['titre']))
        
    return dict_score_titre


# IMPRIMER AU FORMAT DEMANDÉ POUR LES REQUÊTE AVEC SEULEMENT LES MOTS INTERDITS
def print_docs_sans_interdit(list_pertinent):
    # obtenir l'indexdocs avec l'id d'article comme clé et le titre d'article comme valeur
    indexdocs = get_indexdocs()

    # print au format de résultat demandé
    print('-'*50)
    print('Nombre de documents trouvés : '+ str(len(list_pertinent)))
    for i in list_pertinent:
        print('ID : {}\t Score : 100\t Titre : {}'.format(i,indexdocs[i]))


# GRAND PROCESSUS POUR RÉCUPÉRER LES DOCUMENTS PERTINENTS À LA REQUÊTE 
def get_docs(langue):

    # récupérer la requêtes entrée par utilisateur
    requete = input("Veillez saisir un ou plusieurs mots-clés pour faire la requête : ")
    print('*'*50)

    # split la requête par l'espace pour obtenir une liste de mots clés
    keywords = requete.split()

    # récupérer 3 listes de mots : mots obligatoires, mots interdits et mots optionnels
    word_oblig, word_interdit, word_option = get_wordlists(keywords)

    # lire le fichier IndexTermes.json et récupérer le dicionnaire index
    index_termes = trc.lireJson('./documentsIndexes/IndexTermes'+langue+'.json')

    # lire le fichier d'index par document pour obtnir une liste de tous documents de cette langue
    index_tous_document = trc.lireJson('./documentsIndexes/index_par_document_'+langue+'.json')
    list_tous_doc = list(index_tous_document.keys())

    # -------------- s'il y a bien les mots obligatoires --------------
    if len(word_oblig) != 0 :

        # récupérer un dicionnaire avec le mots obligatoires comme clé et les documents correspondants comme valeur
        word_obli_dict = get_docs_words(word_oblig,index_termes)

        # obtenir le nombre des mots obligatoires de la requête
        nb_word_obli = len(word_obli_dict)

        # récupérer une liste de documents contenant tous les mots obligatoires
        list_docs_obli = get_docs_obli(nb_word_obli,word_obli_dict)

        # si aucin fichier contient tous les mots obligatoires
        if len(list_docs_obli) == 0:
            print('Désolé, aucun fichier contient tous les mots obligatoires, essayez de retirer le +.')
        
        # si on trouve bien un fichier avec les mots obligatoires
        else:

            # s'il y a bien les mots interdits dans la requête
            if len(word_interdit)!= 0:
                nb_word_interdit = len(word_interdit)

                # récupérer un dicionnaire avec le mots interdits comme clé et les documents correspondants comme valeur
                word_interdit_dict = get_docs_words(word_interdit,index_termes)

                # si pas de mots interdits trouvés dans le corpus 
                if len(word_interdit_dict)==0:
                    print('Voici les docs pertinents: ')
                    docs_perti = get_docs_by_obli(list_docs_obli,langue,word_oblig,word_option)

                # s'il y a bien les mots interdits dans le corpus
                else:
                    # récupérer une liste de documents contenant les mots interdits
                    list_docs_interdit = get_docs_option(nb_word_interdit,word_interdit_dict)

                    # récupérer une liste de fichiers contenant les mots optionnels qui ne contiennent pas les mots interdits
                    list_pertinent = list()
                    for d in list_docs_obli:
                        if d not in list_docs_interdit:
                            list_pertinent.append(d)

                    # si pas de documents sans mots interdits
                    if len(list_pertinent) == 0:
                        print("Désolé, il n'y pas de fichiers obligatoires sans ces mots interdits, veuillez enlever les mots interdits.")
                    
                    # s'il y a bien les documents sans mots interdits
                    else:
                        # traitement si mots optionnels ou pas et afficher les resultats
                        traitement_mots_option(word_option,index_termes,list_pertinent,langue,word_oblig)

            # si pas de mots interdits
            else:
                # traitement si mots optionnels ou pas et afficher les resultats
                traitement_mots_option(word_option,index_termes,list_docs_obli,langue,word_oblig)


    # -------------- si pas de mots obligatoires --------------
    else:

        # ------ s'il y a bien les mots optionnels ------
        if len(word_option)!=0:

            # récupérer un dicionnaire avec le mots optionnels comme clé et les documents correspondants comme valeur
            word_option_dict = get_docs_words(word_option,index_termes)

            # si les mots optionnels sont bien trouvés dans le corpus
            if len(word_option_dict) != 0:

                # obtenir le nombre des mots optionnels de la requête
                nb_word_option = len(word_option)

                # récupérer une liste de documents contenant tous les mots optionnels
                list_docs_option = get_docs_option(nb_word_option,word_option_dict)

                # ------ s'il y a bien les mots interdits dans la requête ------
                if len(word_interdit)!= 0:
                    nb_word_interdit = len(word_interdit)

                    # récupérer un dicionnaire avec le mots interdits comme clé et les documents correspondants comme valeur
                    word_interdit_dict = get_docs_words(word_interdit,index_termes)

                    # si pas de mots interdits trouvés dans le corpus 
                    if len(word_interdit_dict)==0:
                        pass

                    # s'il y a bien les mots interdits dans le corpus
                    else:

                        # récupérer une liste de documents contenant les mots interdits
                        list_docs_interdit = get_docs_option(nb_word_interdit,word_interdit_dict)

                        # récupérer une liste de fichiers contenant les mots optionnels qui ne contiennent pas les mots interdits
                        list_pertinent = list()
                        for d in list_docs_option:
                            if d not in list_docs_interdit:
                                list_pertinent.append(d)

                        # si pas de documents sans mots interdits
                        if len(list_pertinent) == 0:
                            print("Désolé, il n'y pas de fichiers sans ces mots interdits, veuillez enlever les mots interdits.")
                        # si non
                        else:
                            print('Voici les docs pertinents: ')
                            docs_perti = get_docs_by_obli(list_pertinent,langue,word_oblig,word_option)
                            

                # ------ si pas de mots interdits dans la requête ------
                else:
                    print('Voici les docs pertinents: ')
                    docs_perti = get_docs_by_obli(list_docs_option,langue,word_oblig,word_option)

            # si pas de mots optionnels dans le corpus
            else: 
                
                # ------ s'il y a bien les mots interdits dans la requête ------
                if len(word_interdit)!= 0:
                    nb_word_interdit = len(word_interdit)

                    # récupérer un dicionnaire avec le mots interdits comme clé et les documents correspondants comme valeur
                    word_interdit_dict = get_docs_words(word_interdit,index_termes)

                    # si pas de mots interdits trouvés dans le corpus 
                    if len(word_interdit_dict)==0:
                        pass

                    # s'il y a bien les mots interdits dans le corpus
                    else:

                        # récupérer une liste de documents contenant les mots interdits
                        list_docs_interdit = get_docs_option(nb_word_interdit,word_interdit_dict)

                        # récupérer une liste de fichiers contenant les mots optionnels qui ne contiennent pas les mots interdits
                        list_pertinent = list()
                        for d in list_tous_doc:
                            if d not in list_docs_interdit:
                                list_pertinent.append(d)

                        # si pas de documents sans mots interdits
                        if len(list_pertinent) == 0:
                            print("Désolé, il n'y pas de fichiers sans ces mots interdits, veuillez enlever les mots interdits.")
                        # si non
                        else:
                            print('Tous les documents sans les mots interdits : '+str(word_interdit))
                            print_docs_sans_interdit(list_pertinent)


                            

                # ------ si pas de mots interdits dans la requête ------
                else:
                    print('Désolé ! Aucun des mots optionnels se trouve dans notre corpus.')

        # ------ si pas de mots optionnels ------
        else:

            # --- s'il y a bien les mots interdits dans la requête ---
            if len(word_interdit)!= 0:
                nb_word_interdit = len(word_interdit)

                # récupérer un dicionnaire avec le mots interdits comme clé et les documents correspondants comme valeur
                word_interdit_dict = get_docs_words(word_interdit,index_termes)

                # si pas de mots interdits trouvés dans le corpus 
                if len(word_interdit_dict)==0:
                    print('Pas de documents contenant ces mots interdits, donc tous les documents sont pertinents à votre requête.')

                # s'il y a bien les mots interdits dans le corpus
                else:

                    # récupérer une liste de documents contenant les mots interdits
                    list_docs_interdit = get_docs_option(nb_word_interdit,word_interdit_dict)

                    # récupérer une liste de fichiers contenant les mots optionnels qui ne contiennent pas les mots interdits
                    list_pertinent = list()
                
                    for d in list_tous_doc:
                        if d not in list_docs_interdit:
                            list_pertinent.append(d)

                    # si pas de documents sans mots interdits
                    if len(list_pertinent) == 0:
                        print("Désolé, il n'y pas de fichiers sans ces mots interdits, veuillez enlever les mots interdits.")
                    # si non
                    else:
                        print('Tous les documents sans les mots interdits : '+str(word_interdit))
                        print_docs_sans_interdit(list_pertinent)

            # --- si pas de mots obligatoire, pas de mots optionnels et pas de mots interdits dans la requête ---
            else:
                print("Requête inconnu, veuillez faire une requête au format demandé, merci !")



# ---------------------------- main -----------------------------------------
print('*'*50)
print('******     Partie Requêtes Utilisateur     *******')
print('*'*50)

choix = input("Quelle est votre langue de requête ? A. Anglais  B. Français\n(Tapez q pour quitter le programme)\n\t")

while choix not in ['q']:

    # si anglais
    if choix in ['a','A']:

        # procéder aux corpus anglais
        get_docs('EN')

        print("*"*50)
        # 2ème choix utilisateur
        choix2 = input("Voulez-vous faire une autre requête ? oui/non ")
        print("*"*50)

        if choix2 == 'oui':
            pass
        else:
            print(" ********** Programme arrêté ********** ")
            break

    # si français
    elif choix in ['B','b']:

        # procéder aux corpus français
        get_docs('FR')

        print("*"*50)
        # 2ème choix utilisateur
        choix2 = input("Voulez-vous faire une autre requête ? oui/non ")
        print("*"*50)

        if choix2 == 'oui':
            pass
        else:
            print(" ********** Programme arrêté ********** ")
            break

    # si mauvais saisi
    else:
        print('Désolé, choix inconnu, veuillez refaire le choix entre les 2 langues !')
        print('-'*50)
        time.sleep(0.7)
        choix = input("Quelle est votre langue de requête ? A. Français  B. Anglais\n(Tapez q pour arrêter le programme)\n\t")

