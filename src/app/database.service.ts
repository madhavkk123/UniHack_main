import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';

const API_URL = "/34429336/Johanes/api"
const httpOptions = {
  headers: new HttpHeaders({"Content-Type": "application/json"}),
};
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

  getDocument(unitName:string){
      return this.http.post("http://0.0.0.0:8000/get_subject_context",{query:unitName},httpOptions)
  }

  addDocument(file: File){

  }





}
