import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScoreFrameComponent } from './score-frame.component';

describe('ScoreFrameComponent', () => {
  let component: ScoreFrameComponent;
  let fixture: ComponentFixture<ScoreFrameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScoreFrameComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScoreFrameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
