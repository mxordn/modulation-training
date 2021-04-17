import { Component, Injectable, NgModule, OnInit } from '@angular/core';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
@NgModule()
export class Svg {
  done: SafeHtml;
  hint: SafeHtml;
  svg: SafeHtml;
  lsg: SafeHtml;
}

@Component({
  selector: 'app-score-canvas',
  templateUrl: './score-canvas.component.html',
  styleUrls: ['./score-canvas.component.css']
})
export class ScoreCanvasComponent implements OnInit {

  constructor() {}

  ngOnInit(): void {
    ;
  }

}
