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
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatListModule} from '@angular/material/list';
import {MatCard, MatCardModule} from '@angular/material/card';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet,
    MatSidenavModule, MatButtonModule,
    MatTreeModule, MatDialogModule, MatIconModule, MatTabsModule, ExamplePdfViewerComponent, MatListModule,
    MatFormFieldModule, MatInput, MatCardModule],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'uniHack';
  showFiller = false;

  constructor(private dialog: MatDialog, private dbs: DatabaseService) {}
  dataHistory: any[] = ["What is this?","This is Project Lecture Learner" +
  "by ByteStorm.","Great! What does it do?"]

  ngOnInit(){
      this.dbs.getEnrolledUnits()
    this.dbs.getDocument("principles of finance uni melb").subscribe(
      (data:any ) => {
        this.dataHistory = data.conversation_history
      }
    )
  }

  sendQuery(query:string){
    this.dbs.getDocument(query).subscribe(
      (data:any ) => {
        this.dataHistory = data.conversation_history
        console.log(this.dataHistory)
      }
    )
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
