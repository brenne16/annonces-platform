import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

interface Annonce {
  id: number;
  titre: string;
  description: string;
  prix: number;
  categorie: string;
  localisation: string;
  image: string;
  date: string;
  vendeur: string;
  telephone: string;
}

@Component({
  selector: 'app-detail',
  imports: [CommonModule, RouterLink],
  templateUrl: './detail.html',
  styleUrl: './detail.scss'
})
export class Detail implements OnInit {

  annonce: Annonce | null = null;

  // Même mock data que la liste — plus tard viendra de l'API
  private annonces: Annonce[] = [
    { id: 1, titre: 'iPhone 14 Pro - Excellent état', description: 'Vendu avec boîte et accessoires originaux. Aucune rayure. Batterie à 98%. Couleur noir sidéral. Mémoire 256Go. Débloqué tous opérateurs.', prix: 750, categorie: 'Téléphones', localisation: 'Casablanca', image: 'https://placehold.co/600x400', date: '2024-03-20', vendeur: 'Mohamed A.', telephone: '06 12 34 56 78' },
    { id: 2, titre: 'Vélo de route Trek', description: 'Vélo adulte taille M, très bon état, utilisé 6 mois. Cadre aluminium, 21 vitesses, freins à disque. Idéal pour la ville et les longues distances.', prix: 1200, categorie: 'Sport', localisation: 'Rabat', image: 'https://placehold.co/600x400', date: '2024-03-19', vendeur: 'Sara B.', telephone: '06 98 76 54 32' },
    { id: 3, titre: 'Canapé 3 places gris', description: 'Canapé confortable, tissu gris anthracite, comme neuf. Dimensions : 220x90x85cm. Livraison possible sur Marrakech.', prix: 2500, categorie: 'Meubles', localisation: 'Marrakech', image: 'https://placehold.co/600x400', date: '2024-03-18', vendeur: 'Karim M.', telephone: '06 55 44 33 22' },
    { id: 4, titre: 'MacBook Pro M2 2023', description: '16Go RAM, 512Go SSD, sous garantie Apple jusqu\'en 2025. Très peu utilisé, parfait état. Chargeur inclus.', prix: 14000, categorie: 'Informatique', localisation: 'Casablanca', image: 'https://placehold.co/600x400', date: '2024-03-17', vendeur: 'Yasmine K.', telephone: '06 77 88 99 00' },
    { id: 5, titre: 'Appareil photo Canon EOS', description: 'Reflex Canon EOS 250D avec objectif 18-55mm. 2500 déclenchements seulement. Vendu avec sacoche et 2 batteries.', prix: 3500, categorie: 'Photo', localisation: 'Fès', image: 'https://placehold.co/600x400', date: '2024-03-16', vendeur: 'Omar F.', telephone: '06 11 22 33 44' },
    { id: 6, titre: 'Table de salle à manger', description: 'Table 6 personnes en bois massif, très bon état. Dimensions : 180x90cm. Chaises non incluses. À récupérer sur place.', prix: 1800, categorie: 'Meubles', localisation: 'Tanger', image: 'https://placehold.co/600x400', date: '2024-03-15', vendeur: 'Fatima Z.', telephone: '06 66 55 44 33' }
  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.annonce = this.annonces.find(a => a.id === id) || null;
  }
}