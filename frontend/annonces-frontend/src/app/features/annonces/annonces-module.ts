import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared-module';
import { AnnoncesRoutingModule } from './annonces-routing-module';
import { List } from './list/list';

@NgModule({
  imports: [
    SharedModule,
    AnnoncesRoutingModule,
    List
  ]
})
export class AnnoncesModule { }