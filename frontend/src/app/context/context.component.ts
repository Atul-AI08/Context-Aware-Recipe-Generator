import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-context',
  standalone: true,
  imports: [],
  templateUrl: './context.component.html',
  styleUrl: './context.component.scss'
})
export class ContextComponent {
  context: string[] = [];

  @Output() contextChange = new EventEmitter<string[]>();
  onContextChange() {
    this.contextChange.emit(this.context);
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
