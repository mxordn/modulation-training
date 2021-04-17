import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScoreCanvasComponent } from './score-canvas.component';

describe('ScoreCanvasComponent', () => {
  let component: ScoreCanvasComponent;
  let fixture: ComponentFixture<ScoreCanvasComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScoreCanvasComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScoreCanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
