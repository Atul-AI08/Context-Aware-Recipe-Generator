import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-context',
  standalone: true,
  imports: [],
  templateUrl: './context.component.html',
  styleUrl: './context.component.scss'
})
export class ContextComponent {
  skill_level: string  = "Beginner";
  context: string[] = [];

  @Output() contextChange = new EventEmitter<{ context: string[], skill_level: string }>();
  onContextChange() {
    this.contextChange.emit({ context: this.context, skill_level: this.skill_level });
  }

  changeSkillLevel(level: string) {
    this.skill_level = level;
  }

  addContext(c: string) {
    if (this.context.includes(c)) {
      this.removeContext(this.context.indexOf(c));
    }
    else this.context.push(c);
  }

  checkAndRemoveContext(c: string) {
    if (this.context.includes(c)) {
      this.removeContext(this.context.indexOf(c));
    }
  }

  removeContext(index: number) {
    this.context = this.context.filter((_, i) => i !== index);
  }
}
