import { HttpInterceptorFn } from '@angular/common/http';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {

  // Récupère le token stocké après la connexion
  const token = localStorage.getItem('token');

  if (token) {
    // Clone la requête et ajoute le header Authorization
    const reqWithToken = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
    // Envoie la requête modifiée
    return next(reqWithToken);
  }

  // Pas de token → envoie la requête telle quelle (ex: login, register)
  return next(req);
};