import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {

  myImage:string ="assets/Image/image.jpg";

  private roles: string[];
  isLoggedIn = false;
  showAdminBoard = false;
  username: string;

  constructor(private router: Router){}
  ngOnInit(){

  }

  openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }

  closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }

  patinetList(){
    this.router.navigate(['patientList']);
  }

  doctorList(){
    this.router.navigate(['doctorList']);
  }

  wardList(){
    this.router.navigate(['wardList']);
  }

  departmentList(){
    this.router.navigate(['departmentList']);
  }

  specializationList(){
    this.router.navigate(['specializationList']);
  }

  insuranceList(){
    this.router.navigate(['insuranceList']);
  }

  billList(){
    this.router.navigate(['billList']);
  }

  operationList(){
    this.router.navigate(['operationList']);
  }

  testList(){
    this.router.navigate(['testList']);
  }

  medicosList(){
    this.router.navigate(['medicosList']);
  }

  employeeList(){
    this.router.navigate(['employeeList']);
  }

  logout(){
	//window.sessionStorage.clear();
	//window.location.reload();


  // window.location.reload();
  }

  home(){
    this.router.navigate(['home']);
  }

  contact(){
    this.router.navigate(['contact']);
  }

  about(){
    this.router.navigate(['about']);
  }

}
