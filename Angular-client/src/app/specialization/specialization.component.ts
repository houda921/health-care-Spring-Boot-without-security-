import { Component, OnInit, Renderer2 } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SpecializationService } from '../service/Specialization/specialization.service';

import { Specialization } from './Specialization';

@Component({
  selector: 'app-specialization',
  templateUrl: './specialization.component.html',
  styleUrls: ['./specialization.component.css']
})
export class SpecializationComponent implements OnInit {

  spec : Specialization ={
    specId: null,
    speciality: ''
  };
  id;
  isLoggedIn = false;
  showAdminBoard = false;
  private roles: string[];

  constructor(private router: Router,private ss:SpecializationService,private route:ActivatedRoute,  private renderer: Renderer2) { }

  ngOnInit(): void {
    this.renderer.setStyle(document.body, 'background-color', '#C3E6FC');

   
  }

  getform(){
    if(this.route.snapshot.params['id']>0){
      this.id=this.route.snapshot.params['id'];
      this.getSpecialization();
    }
  }

  getSpecialization(){
    this.ss.getSpecializationById(this.id).subscribe((data)=>{
      this.spec=data;
    },
    error=>{
      console.log(error);
    });
  }

  onSubmit(){
    if(this.spec.specId !== 0 && this.spec.speciality !== ''){
      console.log(this.spec);
      this.save();
    }
    else{
      alert('Enter vaild data');
    }
  }

  save(){
    this.ss.addSpecialization(this.spec)
      .subscribe((data) => {
        console.log(data);
        alert('Specialization Added successfully');
        this.gotoNext();
      },
      error => {
        console.log(error);
        alert('can not save your data');
      })
  }
  gotoNext(){
    this.router.navigate(['specializationList']);
  }
}
