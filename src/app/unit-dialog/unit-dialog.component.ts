import { Component } from '@angular/core';
import {MatDialogModule} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatChipsModule} from '@angular/material/chips';
import {MatIcon} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import {DatabaseService} from '../database.service';



@Component({
  selector: 'app-unit-dialog',
  imports: [MatDialogModule, MatButtonModule, MatCardModule, MatChipsModule, MatGridListModule, MatIcon],
  templateUrl: './unit-dialog.component.html',
  standalone: true,
  styleUrl: './unit-dialog.component.css'
})
export class UnitDialogComponent {

  constructor(private dbs: DatabaseService) {
  }

  addUnit(code:string){
    this.dbs.addUnits(code)

    this.dbs.getEnrolledUnits()
  }

  removeUnit(code:string){
    this.dbs.removeUnits(code)

    this.dbs.getEnrolledUnits()
  }

  data = [{code:"FIT3155", title:"Advanced Algorithms", added:true, description:"Hi"},
    {code:"FIT2044", title:"Hypothetical", added:false, description:"Hi"},
    {code:"FIT2044", title:"Hypothetical", added:false, description:"Hi"},
    {code:"FIT2044", title:"Hypothetical", added:false, description:"Hi"}]
}
