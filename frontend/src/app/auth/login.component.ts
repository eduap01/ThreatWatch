import { Component } from '@angular/core';
import { AuthService, LoginResponse } from './auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private auth: AuthService) {}

  onSubmit() {
    this.auth.login(this.username, this.password).subscribe({
      next: (res: LoginResponse) => {
        this.auth.saveToken(res.access_token);
        window.location.href = '/dashboard';
      },
      error: () => {
        this.errorMessage = 'Credenciales inválidas';
      }
    });
  }
}
