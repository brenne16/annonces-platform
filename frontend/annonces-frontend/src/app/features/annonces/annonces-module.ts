import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared-module';
import { AnnoncesRoutingModule } from './annonces-routing-module';
import { List } from './list/list';
import { Detail } from './detail/detail';
import { Create } from './create/create';

@NgModule({
  imports: [
    SharedModule,
    AnnoncesRoutingModule,
    List,
    Detail,
    Create
  ]
})
export class AnnoncesModule { }