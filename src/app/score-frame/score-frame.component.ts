import { HttpClient, HttpHeaders, HttpParams, HttpRequest, HttpResponse } from '@angular/common/http';
import { Component, OnInit, Sanitizer } from '@angular/core';
import { Injectable } from '@angular/core';
import { Svg } from '../score-canvas/score-canvas.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { MatSnackBar } from '@angular/material/snack-bar';

export interface Modulation {
  type: String,
  shortcut: String[],
  loewe: String,
  checked: Boolean
}

const headerDict = {
  //'Content-Type': 'multipart/form-data',
  //'Accept': 'application/json',
  'Accept': '*/*',
  //'Access-Control-Allow-Headers': 'headers',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  //'Access-Control-Request-Method': 'POST',
  //'Access-Control-Request-Headers': 'X-PINGOTHER, Content-Type'
  //'responseType': 'text'
}

const requestOptions = {                                                                                                                                                                                
  headers: new HttpHeaders(headerDict), 
};

@Component({
  selector: 'app-score-frame',
  templateUrl: './score-frame.component.html',
  styleUrls: ['./score-frame.component.css']
})
@Injectable({
  providedIn: 'root'
})
export class ScoreFrameComponent implements OnInit {
  
  oberquinte: Modulation = {type: "Oberquinte", shortcut: ["5", "bi bi-arrow-up"], loewe: "Loewe I", checked: true}
  oberquarte: Modulation = {type: "Oberquarte", shortcut: ["4", "bi bi-arrow-up"], loewe: "Loewe II", checked: false}
  kleineUnterterz: Modulation = {type: "Kleine Unterterz", shortcut: ["m3", "bi bi-arrow-down"], loewe: "Loewe III", checked: false}
  großeUnterterz: Modulation = {type: "Große Unterterz", shortcut: ["M3", "bi bi-arrow-down"], loewe: "Loewe IV", checked: false}
  kleineOberterz: Modulation = {type: "Kleine Oberterz", shortcut: ["m3", "bi bi-arrow-up"], loewe: "Loewe IX", checked: false}
  großeOberterz: Modulation = {type: "Große Oberterz", shortcut: ["M3", "bi bi-arrow-up"], loewe: "Loewe X", checked: false}
  kleineObersekunde: Modulation = {type: "Kleine Obersekunde", shortcut: ["m2", "bi bi-arrow-up"], loewe: "Loewe V", checked: false}
  großeObersekunde: Modulation = {type: "Große Obersekunde", shortcut: ["M2", "bi bi-arrow-up"], loewe: "Loewe VI", checked: false}
  kleineUntersekunde: Modulation = {type: "Kleine Obersekunde", shortcut: ["m2", "bi bi-arrow-down"], loewe: "Loewe VIII", checked: false}
  grosseUntersekunde: Modulation = {type: "Große Untersekunde", shortcut: ["M2", "bi bi-arrow-down"], loewe: "Loewe VII", checked: false}
  tritonus: Modulation = {type: "Tritonus", shortcut: ["a4/d5 ", "bi bi-arrow-down-up"], loewe: "Loewe XI", checked: false}
  

  modulations: Modulation[] = [this.oberquinte, this.oberquarte, this.kleineUnterterz, this.großeUnterterz,
                              this.kleineOberterz, this.großeOberterz, this.großeObersekunde, this.kleineObersekunde,
                              this.grosseUntersekunde, this.kleineUntersekunde, this.tritonus]; //
  

  submitted = false;
  userMods = [];
  endpointAufgabe = 'https://d1159dfa5528.ngrok.io/loewe/api/neueAufgabe'; //'https://satzlehre-online.de/loewe/api/neueAufgabeApp'; //'https://f6a7a7f31ca4.ngrok.io/loewe/api/neueAufgabeApp';//glarean.mh-freiburg.de/hessen/loewe/api/neueAufgabe 71c0c76a931d.ngrok.io
  selectedMods: String[] = [];
  selMod: String;
  oldhint: string = "";

  //'https://glarean.mh-freiburg.de/hessen/loewe/neueAufgabe';'neueAufgabe'

  svg: SafeHtml;
  public lsg: SafeHtml;
  hint: SafeHtml;

  constructor(private hC: HttpClient, public scores: Svg,
              private sanitizer: DomSanitizer,
              private hintSnack: MatSnackBar) { }

  ngOnInit(): void {
  }

  public async onSubmitNewExercise() {
    this.oldhint = this.scores.hint;
    this.selectedMods = [];
    this.checkSelection();
    this.modulations.forEach((el) => {
      if (el.checked) {
        this.selectedMods.push(el.loewe);
      }
    });

    let formData: FormData = new FormData();
    this.selMod = this.selectedMods.toString();
    formData.append('modType', JSON.stringify(this.selectedMods)); //.toString()
    formData.append("client", "svg");
    console.log(formData.getAll("modType"));
    //console.log(this.selectedMods);
    //const req: HttpRequest<FormData> = new HttpRequest("POST", this.endpointAufgabe, formData);
    //const res = this.makeFileRequest(formData);
    this.scores.done = "loading"
    await this.hC.post(this.endpointAufgabe, formData, requestOptions).toPromise()
      .catch((error) => {
            console.log(error);
        })
      .then((response: any) => {
        this.scores.done = response.done;
        this.scores.hint = response.hint;
        this.scores.lsg = this.sanitizer.bypassSecurityTrustHtml(response.lsg.toString());
        this.scores.svg = this.sanitizer.bypassSecurityTrustHtml(response.svg.toString());
        this.checkHint(this.scores.hint);
      });

  }
  
  public checkSelection() {
    let isNotSelected: Boolean;
    isNotSelected = this.modulations.every((el) => 
      el.checked === false);
    console.log(isNotSelected);
    if (isNotSelected) {
      alert("Bitte Modulation auswählen. Loewe I wird automatisch gesetzt.");
      this.oberquinte.checked = true;
    }
  }

  public checkHint(hint: string) {
    if (this.oldhint != hint) {
      //console.log(this.oldhint, hint);
      this.hintSnack.dismiss();
    }
  }

  public openHint(hint: string) {
    this.hintSnack.open(hint, "Close")
  }
}
