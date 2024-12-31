import { Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { CustomComponent } from './custom/custom.component';

export const routes: Routes = [
    {"path": "about", "component": AboutComponent},
    {"path": "home", "component": HomeComponent},
    {"path": "custom", "component": CustomComponent},
    {"path": "", "redirectTo": "/home", "pathMatch": "full"},
    {"path": "**", "redirectTo": "/home", "pathMatch": "full"}
];
