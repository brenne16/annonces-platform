import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { Navbar } from './components/navbar/navbar';
import { Footer } from './components/footer/footer';
import { CardAnnonce } from './components/card-annonce/card-annonce';
import { SearchBar } from './components/search-bar/search-bar';


@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    Navbar,
    Footer,
    CardAnnonce,
    SearchBar
  ],
  exports: [
    Navbar,
    Footer,
    CardAnnonce,
    SearchBar,
    CommonModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class SharedModule { }