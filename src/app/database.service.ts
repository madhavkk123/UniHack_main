import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({"Content-Type": "application/json"}),
};

const API_URL = "/34429336/Johanes/api"

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {


  constructor(private http: HttpClient) {
  }

  getUnits(driver: any){
    let url = API_URL + "/"
    return "hello"
  }

  getEnrolledUnits(driver: any){
    let url = API_URL + "/"
    return "hello"
  }

  addUnits(driver: any){
    let url = API_URL + "/"
    return "hello"
  }

  getDocument(){
    let url = API_URL + "/"
    return "hello"
  }

  addDocument(file: File){
    let url = API_URL + "/"
    return "hello"
  }





}
