import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.scss'
})
export class Register {

  registerForm: FormGroup;
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      nom: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      motDePasse: ['', [Validators.required, Validators.minLength(6)]],
      confirmMotDePasse: ['', [Validators.required]]
    }, { validators: this.passwordsMatch });
  }

  // Validateur personnalisé — vérifie que les 2 mots de passe sont identiques
  passwordsMatch(form: FormGroup) {
    const mdp = form.get('motDePasse')?.value;
    const confirm = form.get('confirmMotDePasse')?.value;
    return mdp === confirm ? null : { passwordsMismatch: true };
  }

  get nom() { return this.registerForm.get('nom'); }
  get email() { return this.registerForm.get('email'); }
  get motDePasse() { return this.registerForm.get('motDePasse'); }
  get confirmMotDePasse() { return this.registerForm.get('confirmMotDePasse'); }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    // Simulation d'une inscription réussie
    // Plus tard on appellera l'API Spring Boot ici
    setTimeout(() => {
      this.router.navigate(['/auth/login']);
    }, 1000);
  }
}