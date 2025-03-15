import { Component } from '@angular/core';
import {MatDialogModule} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';


@Component({
  selector: 'app-unit-dialog',
  imports: [MatDialogModule, MatButtonModule, MatCardModule, MatChipsModule],
  templateUrl: './unit-dialog.component.html',
  standalone: true,
  styleUrl: './unit-dialog.component.css'
})
export class UnitDialogComponent {
  longText = `The Chihuahua is a Mexican breed of toy dog. It is named for the
  Mexican state of Chihuahua and is among the smallest of all dog breeds. It is
  usually kept as a companion animal or for showing.`;
}
