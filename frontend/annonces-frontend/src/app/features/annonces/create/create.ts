import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-create',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './create.html',
  styleUrl: './create.scss'
})
export class Create {

  annonceForm: FormGroup;
  isLoading: boolean = false;
  imagePreview: string = '';

  categories: string[] = [
    'Téléphones', 'Informatique', 'Sport', 'Meubles', 'Photo', 'Autre'
  ];

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {
    this.annonceForm = this.fb.group({
      titre: ['', [Validators.required, Validators.minLength(5)]],
      description: ['', [Validators.required, Validators.minLength(20)]],
      prix: ['', [Validators.required, Validators.min(1)]],
      categorie: ['', Validators.required],
      localisation: ['', Validators.required]
    });
  }

  get titre() { return this.annonceForm.get('titre'); }
  get description() { return this.annonceForm.get('description'); }
  get prix() { return this.annonceForm.get('prix'); }
  get categorie() { return this.annonceForm.get('categorie'); }
  get localisation() { return this.annonceForm.get('localisation'); }

  onImageChange(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  onSubmit(): void {
    if (this.annonceForm.invalid) {
      this.annonceForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;

    // Simulation — plus tard on enverra à l'API Spring Boot
    setTimeout(() => {
      this.router.navigate(['/annonces']);
    }, 1000);
  }
}