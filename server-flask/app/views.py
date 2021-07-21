import io
from typing import List
from xml.etree import ElementTree as ET
import subprocess, tempfile
import os, ast, json
import random
from flask import render_template, flash, redirect, session, url_for, request, send_from_directory, abort, send_file, jsonify, make_response
from flask.json import JSONDecoder    
from werkzeug.utils import secure_filename
from app import app
from config import MODULS_FOLDER, HOME
from music21 import stream, converter, musicxml
from flask_cors import cross_origin
import verovio
import subprocess
from cairosvg import svg2png
from base64 import b64encode
from svglib.svglib import svg2rlg
from xml.etree import ElementTree



@app.route(HOME + '/', methods = ['GET', 'POST'])
@app.route(HOME + '/index', methods = ['GET', 'POST'])
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
    if aufgabe == "Loewe I":
        hint = "[Keine Hinweise]"
    elif aufgabe == "Loewe II":
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

@app.route(HOME + '/api/neueAufgabeApp', methods = ['GET', 'POST', 'OPTIONS'])
@cross_origin()
def neueAufgabeApp():
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

    modTypeUsed = ""
    requestedMod = request.form.get('modType')
    fdata = request.form.get('modType')
    #print(fdata)
    #See what was requested. Website und App send Lists (as json) or Strings.
    try:
        requestedMod = json.loads(requestedMod)
        modTypeUsed = random.choice(requestedMod)
    except:
        return make_response("Wrong Request")
        #modTypeUsed = requestedMod
        #isAppRequest = False

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
    vtk.redoLayout()
    pageArray = []
    for each in range(vtk.getPageCount()):
        strSVG = vtk.renderToSVG(each+1)
        pageArray.append(strSVG)

    result['pngInk'] = bytes.decode(b64encode(renderPNG(pageArray[0])[0]))

    #render solution
    vtk.loadData(lsgXML.decode('utf-8'))
    vtk.setOption("pageHeight", "600")
    vtk.setOption("pageWidth", "1650")
    vtk.setScale(45)
    vtk.setOption("adjustPageHeight", "true")
    vtk.redoLayout()
    pageArrayLsg = []
    for each in range(vtk.getPageCount()):
        strSVG = vtk.renderToSVG(each+1)
        pageArrayLsg.append(strSVG)
    
    result['pngInkLsg'] = bytes.decode(b64encode(renderPNG(pageArrayLsg[0])[0]))
    
    #get hint if there are some.
    result["hint"] = collectHintsForFigures(modTypeUsed)

    #check if something is rendered
    if result["pngInk"]:
        result["done"] = True
    
    headers = { "Access-Control-Request-Headers": "X-Requested-With, accept, content-type",
                'Access-Control-Allow-Methods': 'GET, POST'}
                #'Access-Control-Allow-Origin': '*',
    resp = make_response((result, headers))
    return resp


@app.route(HOME + '/api/neueAufgabe', methods = ['GET', 'POST'])
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

    modTypeUsed = ""
    requestedMod = request.form.get("modType")
    isAppRequest = True
    print(requestedMod)
    requestDataType = request.form.get("dataType")
    
    #See what was requested. Website und App send Lists (as json) or Strings.
    try:
        requestedMod = json.loads(requestedMod)
        modTypeUsed = random.choice(requestedMod)
    except:
        modTypeUsed = requestedMod
        #isAppRequest = False

    #find the xml paths of the example.
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
    #vtk.setOption("pageHeight", "600")
    vtk.setOption("pageWidth", "980")
    vtk.setScale(40)
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
    #pngImg = b64encode(svg2png(pageArray[0], output_height=200, scale=1.5))
    #result["png"] = bytes.decode(pngImg)
    svgFile = io.StringIO(pageArray[0])
    img = svg2rlg(svgFile)
    #print(pageArray[0])
    #strSvg = img.asString("png")
    
    if requestDataType == 'png':
        result['png'] = bytes.decode(b64encode(img.asString('png')))
        result['pngInk'] = bytes.decode(b64encode(renderPNG(pageArray[0])[0]))
    #print(strSvg, result['png'], pageArray[0]) #strSvg

    #render solution
    vtk.loadData(lsgXML.decode('utf-8'))
    vtk.setOption("pageHeight", "600")
    vtk.setOption("pageWidth", "980")
    vtk.setScale(40)
    vtk.setOption("adjustPageHeight", "true")
    #vtk.setBorder(0)
    vtk.redoLayout()
    pageArrayLsg = []
    for each in range(vtk.getPageCount()):
        strSVG = vtk.renderToSVG(each+1)
        pageArrayLsg.append(strSVG)
    
    #get hints if necessary
    result["hint"] = collectHintsForFigures(modTypeUsed)

    #deliver svg as a jsonified result
    result["lsg"] = pageArrayLsg
    if requestDataType == 'png':
        result['pngInkLsg'] = bytes.decode(b64encode(renderPNG(pageArrayLsg[0])[0]))

    #check if something is rendered
    if result["svg"] != []:
        result["done"] = True
    
    #headers = {'Access-Control-Allow-Origin': '*'}, headers
    resp = make_response((result))
    return resp
    #jsonify(result=result)

@app.route(HOME + '/api/png', methods = ['GET', 'POST'])
@cross_origin()
def png():
    return send_file('static/Eroeffnung-Dur-1-1.png')

@app.route(HOME + '/api/neueAufgabeZwei', methods = ['GET', 'POST'])
@cross_origin()
def neueAufgabeZwei():
    return "Done"

def renderPNG(svg):
    temp = tempfile.NamedTemporaryFile(suffix='.svg')
    
    svgFile = bytes(svg, encoding='utf-8')
    temp.write(svgFile)
    temp.seek(0)
    tree = ET.parse(temp)
    for child in tree.iter():
        if "id" in child.attrib.keys():
            if 'system-' in child.attrib['id']:
                #print(child.attrib)
                systemId = child.attrib['id']
    png = subprocess.run(['inkscape', '-z', '--export-type=png', '--export-id={sysid}'.format(sysid = systemId), '--export-filename=-', '--export-dpi=300', temp.name], stdout=subprocess.PIPE, stdin=subprocess.PIPE)#
    return (png.stdout, png.stderr)
