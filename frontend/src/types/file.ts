// src/types/file.ts
export interface FileAnalysis {
  id: string;
  fileName: string;
  size: number; // en bytes
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  result?: string; // opcional, sólo si se completó el análisis
}
