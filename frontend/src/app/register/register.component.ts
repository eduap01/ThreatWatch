import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  username: string = '';    // <-- añadir
  email: string = '';       // <-- añadir
  password: string = '';    // <-- añadir

  constructor(private auth: AuthService, private router: Router) {}

  onRegister() {
    this.auth.register({ username: this.username, email: this.email, password: this.password }).subscribe({
      next: (res) => {
        alert('Usuario registrado correctamente');
        this.router.navigate(['/login']); // redirige a login
      },
      error: (err) => {
        console.error(err);
        alert('Error al registrar usuario');
      }
    });
  }
}
