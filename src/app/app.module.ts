import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';


import { AppComponent } from './app.component';
import { ScoreCanvasComponent, Svg } from 'src/app/score-canvas/score-canvas.component';
import { ScoreFrameComponent } from 'src/app/score-frame/score-frame.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { InlineSVGModule } from 'ng-inline-svg';
import { HintComponent } from './hint/hint.component';

@NgModule({
  declarations: [
    AppComponent,
    ScoreCanvasComponent,
    ScoreFrameComponent,
    HintComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatTabsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatSlideToggleModule,
    MatListModule,
    MatSidenavModule,
    Svg,
    InlineSVGModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
