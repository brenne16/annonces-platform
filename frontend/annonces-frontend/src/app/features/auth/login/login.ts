import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {

  loginForm: FormGroup;
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      motDePasse: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  // Getters pour accéder facilement aux champs dans le template
  get email() { return this.loginForm.get('email'); }
  get motDePasse() { return this.loginForm.get('motDePasse'); }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Pour l'instant on simule une connexion réussie
    // Plus tard on appellera l'API Spring Boot ici
    setTimeout(() => {
      const { email, motDePasse } = this.loginForm.value;
      if (email === 'test@test.com' && motDePasse === '123456') {
        localStorage.setItem('token', 'fake-jwt-token');
        this.router.navigate(['/annonces']);
      } else {
        this.errorMessage = 'Email ou mot de passe incorrect';
        this.isLoading = false;
      }
    }, 1000);
  }
}