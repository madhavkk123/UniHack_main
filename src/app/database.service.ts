import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

const API_URL = "/34429336/Johanes/api"

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  constructor(private http: HttpClient) {
  }

  getUnits(driver: any){

  }

  getEnrolledUnits(){

  }

  removeUnits(unit: any){

  }

  addUnits(unit: any){
  }

  getDocument(){

  }

  addDocument(file: File){

  }





}
