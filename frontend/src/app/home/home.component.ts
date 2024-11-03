import { Component } from '@angular/core';
import { RecipeComponent } from '../recipe/recipe.component';
import { ContextComponent } from '../context/context.component';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../api.service';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FaIconComponent } from '@fortawesome/angular-fontawesome';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RecipeComponent, ContextComponent, FormsModule, FaIconComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  providers: [ApiService]
})
export class HomeComponent {
  faSearch = faSearch;

  query = '';
  image: string = '';
  dish: string = '';
  context: string[] = [];
  ingredients: string[] = [];
  instructions: string[] = [];

  constructor(private apiService: ApiService) { }

  scroll(val: string) {
    const el = document.getElementById(val);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  onClickSearch() {
    this.dish = this.query;
    setTimeout(() => {
      this.scroll('context');
    }, 100);
  }

  upload(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const imageUrl = e.target.result;
        this.image = imageUrl;
      };

      reader.readAsDataURL(file);
      const formData = new FormData();
      formData.append('file', file);

      this.apiService.getDish(formData).subscribe((data: any) => {
        this.query = data.dish;
      });
    }
  }

  setContext(context: string[]) {
    this.context = context;

    this.apiService.getRecipe(this.dish, this.context).subscribe((data: any) => {
      this.ingredients = data.ingredients;
      this.instructions = data.instructions;
      setTimeout(() => {
        this.scroll('recipe');
      }, 100);
    });
  }

  removeImg() {
    this.image = '';
    this.query = '';
  }
}
