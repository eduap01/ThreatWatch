import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, LoginResponse } from '../auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  // 🔹 Asegúrate de que auth y router están en el constructor
  constructor(private auth: AuthService, private router: Router) {}

  onLogin(): void {
    this.auth.login(this.username, this.password).subscribe({
      next: (res: LoginResponse) => {
        if (res.access_token) {
          this.auth.saveToken(res.access_token);
          this.router.navigate(['/dashboard']);
        } else {
          alert('Usuario o contraseña incorrectos');
        }
      },
      error: (err: any) => {  // 🔹 Declaramos explícitamente tipo 'any'
        console.error(err);
        alert(err.status === 401 ? 'Usuario o contraseña incorrectos' : 'Error al iniciar sesión');
      }
    });
  }
}
