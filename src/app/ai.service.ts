import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({"Content-Type": "application/json"}),
};

const API_URL = "/34429336/Johanes/api"

@Injectable({
  providedIn: 'root'
})
export class AIService {


  constructor(private http: HttpClient) {
  }

  sendQuestion(){
    let url = API_URL + "/questions/";
    return "hello"
  }

  getResponse(){
    let url = API_URL + "/questions/";
    return "hello"
  }

}
