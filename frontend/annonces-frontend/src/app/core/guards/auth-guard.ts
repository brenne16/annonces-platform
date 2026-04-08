import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);

  // Vérifie si un token existe dans le localStorage
  const token = localStorage.getItem('token');

  if (token) {
    // Token trouvé → l'utilisateur est connecté → on laisse passer
    return true;
  } else {
    // Pas de token → l'utilisateur n'est pas connecté → on redirige
    router.navigate(['/auth/login']);
    return false;
  }
};