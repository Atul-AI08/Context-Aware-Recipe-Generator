import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getDish(formData: FormData): Observable<any> {
    return this.http.post('http://localhost:8000/predict', formData);
  }

  getRecipe(dish: string, context: string[], skill_level: string): Observable<any> {
    return this.http.post('http://localhost:8000/generate-recipe', { 'dish_name': dish, 'dietary_preferences': context, 'skill_level': skill_level });
  }

  getCustomRecipe(dish: string, recipe: string, context: string[], skill_level: string): Observable<any> {
    return this.http.post('http://localhost:8000/custom-recipe', { 'dish_name': dish, 'recipe': recipe, 'dietary_preferences': context, 'skill_level': skill_level });
  }
}
