import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-recipe',
  standalone: true,
  imports: [],
  templateUrl: './recipe.component.html',
  styleUrl: './recipe.component.scss'
})
export class RecipeComponent {
  @Input() ingredients: string[] = []
  @Input() instructions: string[] = []
}
