import {Component, inject} from '@angular/core';
import {Data, RouterOutlet} from '@angular/router';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatButtonModule} from '@angular/material/button';
import {MatTreeModule} from '@angular/material/tree';
import {MatIconModule} from '@angular/material/icon';
import {MatTabsModule} from '@angular/material/tabs';
import {ExamplePdfViewerComponent} from './example-pdf-viewer/example-pdf-viewer.component';
import {MatDialog, MatDialogModule} from '@angular/material/dialog';
import {UnitDialogComponent} from './unit-dialog/unit-dialog.component';
import {DatabaseService} from './database.service';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet,
    MatSidenavModule, MatButtonModule,
    MatTreeModule, MatDialogModule,MatIconModule, MatTabsModule, ExamplePdfViewerComponent],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'uniHack';
  showFiller = false;

  constructor(private dialog: MatDialog, private dbs: DatabaseService) {}

  ngOnInit(){
      this.dbs.getEnrolledUnits()
  }

  openDocument(node: any){

  }
  uploadFile(event: any){
    const file :File = event.target.files[0];

    if(file){
      this.dbs.addDocument(file)
    }
  }

  openDialog() {
    const dialogRef = this.dialog.open(UnitDialogComponent,{
      width: '1100px',
      height: '600px',
      maxWidth: '2000px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

  dataSource : any[] = [
    {
      name: 'Fruit',
      children: [{name: 'Apple'}, {name: 'Banana'}, {name: 'Fruit loops'}],
    },
    {
      name: 'Vegetables',
      children: [
        {
          name: 'Green',
          children: [{name: 'Broccoli'}, {name: 'Brussels sprouts'}],},
        {name: 'Orange',
          children: [{name: 'Pumpkins'}, {name: 'Carrots'}],},
      ],
    },
  ];



  childrenAccessor = (node: any) => node.children ?? [];
  hasChild = (_: number, node: any) => !!node.children && node.children.length > 0;



}
