import { Component } from '@angular/core';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  username = '';
  email = '';
  password = '';
  successMessage = '';
  errorMessage = '';

  constructor(private auth: AuthService) {}

  onSubmit() {
    this.auth.register({ username: this.username, email: this.email, password: this.password })
      .subscribe({
        next: () => {
          this.successMessage = 'Usuario registrado correctamente. Ahora puedes iniciar sesión.';
        },
        error: () => {
          this.errorMessage = 'Error registrando usuario';
        }
      });
  }
}
