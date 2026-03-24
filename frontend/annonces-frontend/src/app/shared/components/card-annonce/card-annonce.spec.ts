import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardAnnonce } from './card-annonce';

describe('CardAnnonce', () => {
  let component: CardAnnonce;
  let fixture: ComponentFixture<CardAnnonce>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardAnnonce]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardAnnonce);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
