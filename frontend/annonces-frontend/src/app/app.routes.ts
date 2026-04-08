import { Routes } from '@angular/router';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'annonces',
    pathMatch: 'full'
  },

  {
    path: 'annonces',
    loadChildren: () =>
      import('./features/annonces/annonces-module')
        .then(m => m.AnnoncesModule)
  },

  {
    path: 'auth',
    loadChildren: () =>
      import('./features/auth/auth-module')
        .then(m => m.AuthModule)
  },

  {
    path: 'recherche',
    loadChildren: () =>
      import('./features/recherche/recherche-module')
        .then(m => m.RechercheModule)
  },

  {
    path: 'recommandations',
    loadChildren: () =>
      import('./features/recommandations/recommandations-module')
        .then(m => m.RecommandationsModule)
  },

  {
    path: 'dashboard',
    loadChildren: () =>
      import('./features/dashboard/dashboard-module')
        .then(m => m.DashboardModule)
  },

  {
    path: 'chatbot',
    loadChildren: () =>
      import('./features/chatbot/chatbot-module')
        .then(m => m.ChatbotModule)
  },

  {
    path: '**',
    redirectTo: 'annonces'
  }

];