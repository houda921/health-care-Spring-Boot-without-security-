import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Doctor } from './Doctor';

@Injectable({
  providedIn: 'root'
})
export class DoctorService {
  private baseURL = "http://localhost:9007/doctors";
  constructor(private httpClient: HttpClient) {

   }
   getDoctoList():Observable<Doctor[]>{
    return this.httpClient.get<Doctor[]>(`${this.baseURL}`);
   }
}
