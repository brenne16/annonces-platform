import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared-module';
import { AuthRoutingModule } from './auth-routing-module';
import { Login } from './login/login';
import { Register } from './register/register';

@NgModule({
  imports: [
    SharedModule,
    AuthRoutingModule,
    Login,
    Register
  ]
})
export class AuthModule { }