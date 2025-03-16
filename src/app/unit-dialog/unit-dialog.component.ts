import { Component } from '@angular/core';
import {MatDialogModule} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import {MatIcon} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';



@Component({
  selector: 'app-unit-dialog',
  imports: [MatDialogModule, MatButtonModule, MatCardModule, MatChipsModule, MatGridListModule, MatIcon],
  templateUrl: './unit-dialog.component.html',
  standalone: true,
  styleUrl: './unit-dialog.component.css'
})
export class UnitDialogComponent {

  data = [{code:"FIT3155", title:"Advanced Algorithms", added:true, description:"Hi"}]
}
