import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitDialogComponent } from './unit-dialog.component';

describe('UnitDialogComponent', () => {
  let component: UnitDialogComponent;
  let fixture: ComponentFixture<UnitDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnitDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
