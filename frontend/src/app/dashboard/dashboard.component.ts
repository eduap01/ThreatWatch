import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/auth.service';

interface File {
  name: string;
  date: string;
  result: string;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  username: string = 'Eduardo'; // o el valor que venga de tu auth
  files: File[] = [
    { name: 'archivo1.pdf', date: '2025-09-04', result: 'Limpio' },
    { name: 'archivo2.exe', date: '2025-09-04', result: 'Amenaza detectada' }
  ];

  constructor() {}

  ngOnInit(): void {
    // Aquí podrías cargar username y files desde tu AuthService o backend
  }
}
