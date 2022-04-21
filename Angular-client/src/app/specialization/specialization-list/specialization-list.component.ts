import { Component, OnInit, Renderer2 } from '@angular/core';
import { Router } from '@angular/router';
import { SpecializationService } from 'src/app/service/Specialization/specialization.service';

import { Specialization } from '../Specialization';

@Component({
  selector: 'app-specialization-list',
  templateUrl: './specialization-list.component.html',
  styleUrls: ['./specialization-list.component.css']
})
export class SpecializationListComponent implements OnInit {

  ​​​​​​​​desc='';
  search;
  specList:Specialization[];
  isLoggedIn = false;
  showAdminBoard = false;
  private roles: string[];

  constructor(private router:Router,private ss:SpecializationService,  private renderer: Renderer2) { }

  ngOnInit(): void {
    this.renderer.setStyle(document.body, 'background-color', '#f7f9fa');
  }
  getList(){
    this.ss.getAllSpecialization()
      .subscribe((list) =>{
      this.specList=list;
    },
    error =>{
      console.log(error);
    });
    }


  gotoSpecialization(){
    this.router.navigate(['specialization']);
  }

  getSpecialization(id:number){
    this.router.navigate(['specializationUpdate',id]);
  }

  deleteSpecialization(id:number){
    this.ss.deleteSpecialization(id)
       .subscribe((response)=>{
         console.log(response);
         alert('Specialization deleted');
         this.getList();
       },
       error =>{
       console.log(error);
     });
  }

}
