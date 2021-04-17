import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { ScoreCanvasComponent, Svg } from '../score-canvas/score-canvas.component';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';


export interface Modulation {
  type: String,
  loewe: String,
  checked: Boolean
}

const headerDict = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Access-Control-Allow-Headers': 'Content-Type',
  'responseType': 'text'
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
  
  
  oberquinte: Modulation = {type: "Oberquinte", loewe: "Loewe I", checked: true}
  oberquarte: Modulation = {type: "Oberquarte", loewe: "Loewe II", checked: false}
  kleineUnterterz: Modulation = {type: "Kleine Unterterz", loewe: "Loewe III", checked: false}
  großeUnterterz: Modulation = {type: "Große Unterterz", loewe: "Loewe IV", checked: false}
  kleineOberterz: Modulation = {type: "Kleine Oberterz", loewe: "Loewe IX", checked: false}
  großeOberterz: Modulation = {type: "Große Oberterz", loewe: "Loewe X", checked: false}
  kleineObersekunde: Modulation = {type: "Kleine Obersekunde", loewe: "Loewe V", checked: false}
  großeObersekunde: Modulation = {type: "Große Obersekunde", loewe: "Loewe VI", checked: false}
  kleineUntersekunde: Modulation = {type: "Kleine Obersekunde", loewe: "Loewe VIII", checked: false}
  grosseUntersekunde: Modulation = {type: "Große Untersekunde", loewe: "Loewe VII", checked: false}
  tritonus: Modulation = {type: "Tritonus", loewe: "Loewe XI", checked: false}
  

  modulations: Modulation[] = [this.oberquinte, this.oberquarte, this.kleineUnterterz, this.großeUnterterz,
                              this.kleineOberterz, this.großeOberterz, this.großeObersekunde, this.kleineObersekunde,
                              this.grosseUntersekunde, this.tritonus, this.kleineUntersekunde];
  

  submitted = false;
  userMods = [];
  endpointAufgabe = 'api/neueAufgabe'
  selectedMods: String[] = [];
  selMod: String;
  //'https://glarean.mh-freiburg.de/hessen/loewe/neueAufgabe';

  svg: SafeHtml;
  lsg: SafeHtml;
  hint: SafeHtml;

  constructor(private hC: HttpClient, public scores: Svg, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  public async onSubmitNewExercise() {
    this.selectedMods = [];
    this.modulations.forEach((el) => {
      if (el.checked) {
        this.selectedMods.push(el.loewe);
      }
    });

    let formData: FormData = new FormData();
    this.selMod = JSON.stringify(this.selectedMods);
    formData.append("modType", JSON.stringify(this.selectedMods));
//    console.log();
//    console.log(formData.get('modType'));


    const result = await this.hC.post<Svg>(this.endpointAufgabe, formData).toPromise();
    if (result.done) {
      this.svg = this.sanitizer.bypassSecurityTrustHtml(result.svg.toString());
      this.lsg = this.sanitizer.bypassSecurityTrustHtml(result.lsg.toString());
      this.hint = result.hint;
    }
    else {
      this.scores.svg = "Serverfehler";
      this.scores.lsg = "Serverfehler";
      this.hint = "Serverfehler";
    }
  }

  public openDialog() {
    //this.loesung.open(ScoreCanvasComponent);
  }
}
