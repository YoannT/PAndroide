#!/usr/bin/python
# -*-coding:Utf-8 -*

import BeautifulSoup
import io

def lectureFichierXML(filename):

    listeBatiments=[]
    listeNomBat=[]
    soup = BeautifulSoup.BeautifulSoup(io.open(filename,encoding='utf8'))
    batiments = soup.findAll('batiment')
    
    for batiment in batiments:
        listeNomBat.append(batiment.find('nom').text)
        pieces = batiment.findAll('piece')
        listePieces = []
        listeNomPiece = []

        for piece in pieces:
            desc = []
            listeNomPiece.append(piece.find('nom').text)
            murs = piece.findAll('murs')
            obstacles = piece.findAll('obstacle')
            sorties = piece.findAll('sortie')
            listeMurs = []
            listeObstacles = []
            listeSorties = []
       
            for segment in murs:
                coords = segment.findAll('coordonnees')
                listeSeg = []
                for coord in coords:
                    listeSeg.append(coord.text)
                listeMurs.append(listeSeg)
            
            for segment in obstacles:
                coords = segment.findAll('coordonnees')
                listeSeg = []
                for coord in coords:
                    listeSeg.append(coord.text)
                listeObstacles.append(listeSeg)
            
            for tmp in sorties:
                coords = tmp.findAll('coordetnompiececonnexe')
                for coord in coords:
                    listeSorties.append(coord.text)

            desc.append(piece.find('nom'))
            desc.append(listeMurs)
            desc.append(listeObstacles)
            desc.append(listeSorties)
            listePieces.append(desc)

        descriptionbat = []
        descriptionbat.append(listeNomPiece)
        descriptionbat.append(listePieces)
        listeBatiments.append(descriptionbat)
        
    return listeNomBat, listeBatiments
    
def lectureFichierXMLobjet(filename):

    segments = []
    soup = BeautifulSoup.BeautifulSoup(io.open(filename,encoding='utf8'))
    coordonnees = soup.findAll('coordonnees')
    nom = soup.findAll('nom')[0].text
    
    for val in coordonnees:
        segment = val.text
        segments.append(segment)
    
    return nom, segments

def sauvegardeXML(filepath1,fic,dicobstacles,nomorigin,datorigin):
    
    soup = BeautifulSoup.BeautifulSoup(io.open(filepath1,encoding='utf8'))
    
    fic.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<racine xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="./bp.xsd" >\n<batiment>\n\n')
    
    fic.write(str(soup.find('nom')))
    
    print dicobstacles
    
    pieces = soup.findAll('piece')
    for val in pieces:
        fic.write('<piece>')
        nom = val.find('nom')
        fic.write(str(nom)+'\n')
        murs = val.find('murs')
        fic.write(str(murs)+'\n')
        
        if nom.text in dicobstacles.keys():
            ind = nomorigin.index(nom.text)
            val0 = datorigin[ind].split(';')
            x0 = float(val0[0])
            y0 = float(val0[1])
            
            fic.write('<obstacles>\n')
            
            for val2 in dicobstacles[nom.text]:
                fic.write('<obstacle>\n')
                for cpt, obs in enumerate(val2[0]):
                    if cpt < len(val2[0])-1:
                        fic.write('<coordonnees>'+str(obs-x0)+';'+str(val2[1][cpt]-y0)+','+str(val2[0][cpt+1]-x0)+';'+str(val2[1][cpt+1]-y0)+'</coordonnees>\n')
                fic.write('</obstacle>\n')
                
            fic.write('</obstacles>\n')
            
        sorties = val.find('sortie')
        fic.write(str(sorties)+'\n')
        fic.write('</piece>\n')
        
    fic.write('</batiment>\n</racine>')
    fic.close()