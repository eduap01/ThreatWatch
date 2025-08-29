import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://localhost:8000/auth'; // FastAPI auth endpoints
  private tokenKey = 'access_token';

  constructor(private http: HttpClient, private router: Router) {}

  register(data: { username: string; email: string; password: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/register`, data);
  }

login(username: string, password: string) {
  const body = new URLSearchParams();
  body.set('username', username);
  body.set('password', password);

  return this.http.post<LoginResponse>(`${this.baseUrl}/login`, body.toString(), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
}



  saveToken(token: string) {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  logout() {
    localStorage.removeItem(this.tokenKey);
    this.router.navigate(['/login']);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}
