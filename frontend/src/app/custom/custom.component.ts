import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { FormsModule } from '@angular/forms';
import { ContextComponent } from '../context/context.component';
import { RecipeComponent } from '../recipe/recipe.component';

@Component({
  selector: 'app-custom',
  standalone: true,
  imports: [FormsModule, ContextComponent, RecipeComponent],
  templateUrl: './custom.component.html',
  styleUrl: './custom.component.scss',
  providers: [ApiService]
})
export class CustomComponent {
  skill_level: string = 'Beginner';
  dish: string = '';
  recipe: string = '';
  context: string[] = [];
  ingredients: string[] = [];
  instructions: string[] = [];

  isLoading = false;

  constructor(private apiService: ApiService) { }

  scroll(val: string) {
    const el = document.getElementById(val);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  setContext(event: { context: string[], skill_level: string }) {
    this.context = event.context;
    this.skill_level = event.skill_level;
    this.isLoading = true;

    this.apiService.getCustomRecipe(this.dish, this.recipe, this.context, this.skill_level).subscribe((data: any) => {
      this.isLoading = false;
      this.ingredients = data.ingredients;
      this.instructions = data.instructions;
      setTimeout(() => {
        this.scroll('recipe');
      }, 100);
    });
  }
}
