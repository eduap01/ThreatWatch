import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = ''; // Asume que frontend y backend están en mismo dominio y puerto  (si no, cambia aquí)

  constructor(private http: HttpClient) {}

  // --- AUTH ---

  register(user: {username: string; email: string; password: string}): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/register`, user);
  }

  login(formData: {username: string; password: string}): Observable<any> {
    const body = new URLSearchParams();
    body.set('username', formData.username);
    body.set('password', formData.password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post(`${this.baseUrl}/auth/login`, body.toString(), { headers });
  }

  getCurrentUser(token: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    return this.http.get(`${this.baseUrl}/auth/me`, { headers });
  }

  // --- FILES ---

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/files/upload`, formData);
  }

  getFileAnalysis(fileId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/files/${fileId}`);
  }

  analyzeFile(fileId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/analyze/${fileId}`);
  }

  getFileStatus(fileId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/files/${fileId}/status`);
  }
}
