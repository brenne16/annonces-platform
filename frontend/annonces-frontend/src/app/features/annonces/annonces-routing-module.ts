import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { List } from './list/list';
import { Detail } from './detail/detail';
import { Create } from './create/create';

const routes: Routes = [
  { path: '', component: List },
  { path: 'create', component: Create },
  { path: ':id', component: Detail }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AnnoncesRoutingModule { }