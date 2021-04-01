#!/usr/bin/env python
# coding: utf-8
# Projet du groupe : Siyu Wang et Natia Davitashvili

# -------------------------------------------------------------------------------------------------------------
#   python3 indexerDocuments <chemin de dossier>
#
#   Indexation des xml d'un dossier (corpus_16EN-16FR/) :
#   Parcours des fichiers ; pour chacun :
#       0. indexation de document (id: Fichier(chemin),Titre)
#       1. extraction du contenu textuel 
#       2. détecter la langue (EN ou FR)
#       3. lemmatisation : TreeTagger
#       4. indexation des termes FR et EN
#   Sauvegarde fichier des index (inversé & documents)
# -------------------------------------------------------------------------------------------------------------


import os
import re
import sys
import glob
import json
from langdetect import detect
import traitementCommun as trc

# -------- à paramétrer ---------------
# chemin du dossier saisi par l'utilisatuer
chemin = sys.argv[1]

# corpus à indexer
corpus = chemin + "/*.txt"

# index résultats
fiIndex = "./documentsIndexes"

# ----------------- traitements TAL----------------------------------

# TRAITEMENT POUR OBTENIR UN DICTIONNAIRE AVEC L'ID D'ARTICLE COMME CLÉ ET LE DICT DES FRÉQUENCES COMME VALEUR
def traitement_terme_per_doc(doc,texte,langue,dict_doc_termes):
    print("--- Langue : "+langue)
    texte = trc.supprimPonct(texte)
    tags = trc.treetagger_tag(texte,'fr')
    dict_terme_par_doc = trc.get_terme_per_doc(tags)
    dict_doc_termes[doc]=dict_terme_par_doc
    nom_f = './documentsIndexes/index_par_document_'+langue+'.json'
    trc.ecrireJson(nom_f,dict_doc_termes)
    

# TRAITEMENT POUR RETOURNER UN LISTE DE TOUS LES TERMES DE TOUS LES DOCUMENTS
def get_termelist(dict_doc_termes):
    list_termes = list()
    for a, d in dict_doc_termes.items():
        for m,f in d.items():
            if m not in list_termes:
                list_termes.append(m)
    return list_termes

# ----------------- index -----------------------------------------

# ÉCRIRE LE FICHIER D'INDEXATION DES DOCUMENTS EN FORMAT JSON
def get_indexDocs(nb_docs):
    index_final = dict()
    index_docs = dict()
    x = 1
    while (x<nb_docs+1):
        for doc in list_docs:
            print("Traitement du fichier : "+doc)
            text = trc.lireFichier(doc)
            titre = text[1]
            titre = re.sub (r'<[^>]+>', '', titre)
            titre = re.sub (r'\n', '', titre)
            index_docs[x]={"Fichier":doc, "Titre":titre}
            x+=1
    index_final['indexDocs'] = index_docs
    return index_final


# TRAITEMENT POUR RETOURNER UN DICTIONNAIRE FINAL D'INDEXATION, AVEC LE TERME COMME CLÉ ET L'ID D'ARTICLE ET SA FRÉQUENCE COMME VALEUR
def get_terme_dict_total(dict_doc_termes,list_termes):
    dict_termes_total = dict()
    for a,d in dict_doc_termes.items():
        for t in list_termes:
            if t in d.keys():
                if t not in dict_termes_total.keys():
                    dict_termes_total[t] = [{"doc_id":a,"fréquence":d[t]}]
                else:
                    dict_termes_total[t].append({"doc_id":a,"fréquence":d[t]})
    return dict_termes_total


# ------------------------ main ----------------------------

print("***************************************")
print("*            Projet Indexeur          *")
print("*    Siyu WANG et Natia DAVITASHVILI  *")
print("***************************************")
print("------ Execution en cours ------ ")

# liste de tous les fichiers txt du dossier initial
list_docs = glob.glob(corpus)
nb_docs = len(list_docs)

# crée le fichier indexDocs.json
index_docs = get_indexDocs(nb_docs)
print("------ Fichier IndexDocs.json a été créé avec succès ! ------")
trc.ecrireJson("./documentsIndexes/IndexDocs.json",index_docs)

dict_doc_termes_fr = dict()
dict_doc_termes_en = dict()

# parcourir les documents pour indexer les termes
for doc in list_docs:
    print("--- Indexation des termes du fichier: "+doc)

    # extraire le contenu text du fichier
    texte = trc.extraitTexteFichier(doc)

    # si la langue français détectée
    if detect(texte)=="fr":
        # traitement pour obtenir un dicionnaire avec le nom du fichier comme clé et le dicionnaire de mot : fréquence comme valeur
        traitement_terme_per_doc(doc,texte,'fr',dict_doc_termes_fr)

    # si la langue anglais détectée
    if detect(texte)=='en':
        # traitement pour obtenir un dicionnaire avec le nom du fichier comme clé et le dicionnaire de mot : fréquence comme valeur
        traitement_terme_per_doc(doc,texte,'en',dict_doc_termes_en)

# créer un liste de termes de tous les documents
list_termes_fr = get_termelist(dict_doc_termes_fr)
list_termes_en = get_termelist(dict_doc_termes_en)

# créer un dictionnaire avec le terme comme clé et un liste de {document : fréquence} comme valeur
print("--- Indexation totale en cours pour les documents en français---")
dict_termes_total_fr = get_terme_dict_total(dict_doc_termes_fr,list_termes_fr)
print("--- Indexation totale en cours pour les documents en anglais---")
dict_termes_total_en = get_terme_dict_total(dict_doc_termes_en,list_termes_en)

# écrire le fichier json pour sauvegarder les indexations français
trc.ecrireJson("./documentsIndexes/IndexTermesFR.json",dict_termes_total_fr)
print("--- Fichier IndexTermesFR.json a été généré avec succès ! ---")

# écrire le fichier json pour sauvegarder les indexations français
trc.ecrireJson("./documentsIndexes/IndexTermesEN.json",dict_termes_total_en)
print("--- Fichier IndexTermesEN.json a été généré avec succès ! ---")


