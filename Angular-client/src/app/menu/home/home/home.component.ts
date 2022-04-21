import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private roles: string[];
  isLoggedIn = false;
  showAdminBoard = false;
  showModeratorBoard = false;
  username: string;
  constructor(private router: Router) { }

  ngOnInit(): void {

  }

  ePatinet() {
    this.router.navigate(['patientList']);
  }

  newPatient() {
    this.router.navigate(['patient']);
  }
}
