import os, ast, json
import random
from flask import render_template, flash, redirect, session, url_for, request, send_from_directory, abort, send_file, jsonify, make_response    
from werkzeug.utils import secure_filename
from app import app
from config import MODULS_FOLDER
from music21 import stream, converter, musicxml
from flask_cors import cross_origin
import verovio

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    mods = ["Loewe I",
            "Loewe II",
            "Loewe III",
            "Loewe IV",
            "Loewe V",
            "Loewe VI",
            "Loewe VII",
            "Loewe VIII",
            "Loewe IX",
            "Loewe X",
            "Loewe XI",
            "Teufelsmühle I",
            ]
    return render_template("index.html", mods=mods)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def collectHintsForFigures(aufgabe):
    if aufgabe == "Loewe II":
        hint = "Hinweis: „b5“ meint hier immer die verminderte Quinte über dem Basston."
    elif aufgabe == "Loewe III":
        hint = "Hinweis: „#6“ meint hier immer die große Sexte über dem Basston."
    elif aufgabe == "Loewe IV":
        hint = "Hinweis: „#“ und „b“ meint hier immer die große bzw. kleine Terz über dem Basston."
    elif aufgabe == "Loewe V":
        hint = "Hinweis: „#4“ meint hier immer die übermässige Quarte über dem Basston. „b6“ meint die kleine Sexte."
    elif aufgabe == "Loewe VI":
        hint = "Hinweis: „#4“ meint hier immer die übermässige Quarte über dem Basston."
    elif aufgabe == "Loewe VII":
        hint = "Hinweis: „b5“ meint hier immer die verminderte Quarte über dem Basston. „b4“ meint die reine Quarte."
    elif aufgabe == "Loewe VIII":
        hint = "Hinweis: „#6“ meint hier immer die übermässige Sexte über dem Basston. „#“ meint die Dur-Terz."
    elif aufgabe == "Loewe IX":
        hint = "Hinweis: „#“ und „b“ meint hier immer die Dur- bzw. Moll-Terz."
    elif aufgabe == "Loewe X":
        hint = "Hinweis: „#“ und „b“ meint hier immer die Dur- bzw. Moll-Terz. „#6“ meint die große Sexte über dem Basston. „#“ meint die Dur-Terz."
    elif aufgabe == "Loewe XI":
        hint = "Hinweis: „#“ meint hier immer die Dur-Terz. „b5“ meint die verminderte Quinte über dem Basston."
    else:
        return None
    return hint

@app.route('/api/neueAufgabe', methods = ['GET', 'POST'])
@cross_origin()
def neueAufgabe():
    #init a dict to be returned in the end
    result = {}
    modDict = {"Loewe III": MODULS_FOLDER + "loewe-3",
            "Loewe II": MODULS_FOLDER + "loewe-2",
            "Loewe I": MODULS_FOLDER + "loewe-1",
            "Loewe IV": MODULS_FOLDER + "loewe-4",
            "Loewe V": MODULS_FOLDER + "loewe-5",
            "Loewe VI": MODULS_FOLDER + "loewe-6",
            "Loewe VII": MODULS_FOLDER + "loewe-7",
            "Loewe VIII": MODULS_FOLDER + "loewe-8",
            "Loewe IX": MODULS_FOLDER + "loewe-9",
            "Loewe X": MODULS_FOLDER + "loewe-10",
            "Loewe XI": MODULS_FOLDER + "loewe-11",
            "Teufelsmühle I": MODULS_FOLDER + "teufelsmuehle-1",
            }

    requestedMod = request.form.get("modType")
    modTypeUsed = []
    if isinstance(requestedMod, str):
        modTypeUsed = requestedMod
    else:
        modType = json.loads(request.form.get("modType"))
        modTypeUsed = random.choice(modType)

    #print(modType, modTypeUsed)
    thePath = modDict[modTypeUsed]

    tInts = ["A-4", "P-4", "M-3", "m-3", "M-2", "M-2", "m-2", "P1", "P1", "m2", "M2", "M2", "m3", "M3", "P4", "A4"]
    tI = random.choice(tInts)
    s = converter.parse(thePath + ".musicxml")

    exS = s.transpose(tI)
    exerciceXML = musicxml.m21ToXml.GeneralObjectExporter().parse(exS)

    s = converter.parse(thePath + "-lsg.musicxml")
    lsgS = s.transpose(tI)
    lsgXML = musicxml.m21ToXml.GeneralObjectExporter().parse(lsgS)

    #render exercice
    vtk = verovio.toolkit()
    vtk.loadData(exerciceXML.decode('utf-8'))
    vtk.setOption("pageHeight", "600")
    vtk.setOption("pageWidth", "1500")
    vtk.setScale(45)
    vtk.setOption("header", "none")
    vtk.setOption("footer", "none")
    vtk.setOption("adjustPageHeight", "true")
#vtk.setBorder(0)
    vtk.redoLayout()
    pageArray = []
    for each in range(vtk.getPageCount()):
        strSVG = vtk.renderToSVG(each+1)
        pageArray.append(strSVG)
    result["svg"] = pageArray
    
    #render solution
    vtk.loadData(lsgXML.decode('utf-8'))
    vtk.setOption("pageHeight", "600")
    vtk.setOption("pageWidth", "1650")
    vtk.setScale(45)
    vtk.setOption("adjustPageHeight", "true")
#    vtk.setBorder(0)
    vtk.redoLayout()
    pageArrayLsg = []
    for each in range(vtk.getPageCount()):
        strSVG = vtk.renderToSVG(each+1)
        pageArrayLsg.append(strSVG)
    
    #get hints if necessary
    result["hint"] = collectHintsForFigures(modTypeUsed)

    #deliver svg as a jsonified result
    result["lsg"] = pageArrayLsg
    if result["svg"] != []:
        result["done"] = True
    
    headers = {'Access-Control-Allow-Origin': '*'}
    resp = make_response((result, headers))
    return resp
    #jsonify(result=result)

@app.route('/api/neueAufgabeZwei', methods = ['GET', 'POST'])
@cross_origin()
def neueAufgabeZwei():
    print(request.form.get("modType"))
    result =  request.form.get('modType')
    headers = {'Access-Control-Allow-Origin': '*'}
    return make_response(result, headers)