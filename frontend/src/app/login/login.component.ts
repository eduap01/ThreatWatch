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
  email: string = '';       // <-- añadir
  password: string = '';

  constructor(private auth: AuthService, private router: Router) {}

  onLogin() {
    this.auth.login(this.username, this.password).subscribe({
      next: (res: LoginResponse) => {
        if (res.access_token) {
          this.auth.saveToken(res.access_token); // guardamos token en localStorage
          this.router.navigate(['/dashboard']); // redirigimos al dashboard
        } else {
          alert('Usuario o contraseña incorrectos');
        }
      },
      error: (err) => {
        console.error(err);
        alert('Error al iniciar sesión');
      }
    });
  }
}
