import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface File {
  id: number;
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
  @ViewChild('fileInput') fileInput!: ElementRef;

  username: string = 'Eduardo'; // O lo que venga de tu AuthService
  files: File[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadFiles();
  }

  loadFiles() {
  this.http.get<File[]>('http://localhost:8000/files').subscribe(files => {
    this.files = files;

    // Ahora obtenemos el estado de cada archivo
    this.files.forEach(file => {
      this.http.get<{status: string}>(`http://localhost:8000/files/${file.id}/status`)
        .subscribe({
          next: (res) => file.result = res.status,
          error: () => file.result = 'Pendiente'
        });
    });
  });
}

analyzeFile(fileId: number) {
  this.http.get(`http://localhost:8000/analyze/${fileId}`).subscribe({
    next: () => this.loadFiles(), // recarga la tabla con el nuevo estado
    error: (err) => console.error(err)
  });
}


  onUploadClick() {
    this.fileInput.nativeElement.click();
  }

  uploadFile(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    this.http.post('http://localhost:8000/files/upload', formData).subscribe({
      next: () => {
        alert('Archivo subido correctamente');
        this.loadFiles(); // recarga la lista de archivos
      },
      error: (err) => {
        console.error('Error subiendo archivo', err);
        alert('Error subiendo el archivo');
      }
    });
  }
}
