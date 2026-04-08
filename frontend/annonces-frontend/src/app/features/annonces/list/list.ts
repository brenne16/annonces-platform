import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Annonce {
  id: number;
  titre: string;
  description: string;
  prix: number;
  categorie: string;
  localisation: string;
  image: string;
  date: string;
}

@Component({
  selector: 'app-list',
  imports: [CommonModule],
  templateUrl: './list.html',
  styleUrl: './list.scss'
})
export class List {

  // Données fictives pour tester l'interface avant l'API
  annonces: Annonce[] = [
    {
      id: 1,
      titre: 'iPhone 14 Pro - Excellent état',
      description: 'Vendu avec boîte et accessoires originaux. Aucune rayure.',
      prix: 750,
      categorie: 'Téléphones',
      localisation: 'Casablanca',
      image: 'https://placehold.co/300x200',
      date: '2024-03-20'
    },
    {
      id: 2,
      titre: 'Vélo de route Trek',
      description: 'Vélo adulte taille M, très bon état, utilisé 6 mois.',
      prix: 1200,
      categorie: 'Sport',
      localisation: 'Rabat',
      image: 'https://placehold.co/300x200',
      date: '2024-03-19'
    },
    {
      id: 3,
      titre: 'Canapé 3 places gris',
      description: 'Canapé confortable, tissu gris anthracite, comme neuf.',
      prix: 2500,
      categorie: 'Meubles',
      localisation: 'Marrakech',
      image: 'https://placehold.co/300x200',
      date: '2024-03-18'
    },
    {
      id: 4,
      titre: 'MacBook Pro M2 2023',
      description: '16Go RAM, 512Go SSD, sous garantie Apple.',
      prix: 14000,
      categorie: 'Informatique',
      localisation: 'Casablanca',
      image: 'https://placehold.co/300x200',
      date: '2024-03-17'
    },
    {
      id: 5,
      titre: 'Appareil photo Canon EOS',
      description: 'Reflex Canon EOS 250D avec objectif 18-55mm.',
      prix: 3500,
      categorie: 'Photo',
      localisation: 'Fès',
      image: 'https://placehold.co/300x200',
      date: '2024-03-16'
    },
    {
      id: 6,
      titre: 'Table de salle à manger',
      description: 'Table 6 personnes en bois massif, très bon état.',
      prix: 1800,
      categorie: 'Meubles',
      localisation: 'Tanger',
      image: 'https://placehold.co/300x200',
      date: '2024-03-15'
    }
  ];

  categories: string[] = [
    'Toutes', 'Téléphones', 'Informatique', 'Sport', 'Meubles', 'Photo'
  ];

  categorieSelectionnee: string = 'Toutes';

  get annoncesFiltrees(): Annonce[] {
    if (this.categorieSelectionnee === 'Toutes') {
      return this.annonces;
    }
    return this.annonces.filter(a => a.categorie === this.categorieSelectionnee);
  }

  filtrerParCategorie(categorie: string): void {
    this.categorieSelectionnee = categorie;
  }
}