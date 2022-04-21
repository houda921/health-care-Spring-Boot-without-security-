import { Component, OnInit, Renderer2 } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DepartmentService } from '../service/department/department.service';

import { Department } from './Department';

@Component({
  selector: 'app-department',
  templateUrl: './department.component.html',
  styleUrls: ['./department.component.css']
})
export class DepartmentComponent implements OnInit  {

  deptList = <any>[];

  dept: Department = {
    deptId: 0,
    deptName: ''
  }
  id;
  isLoggedIn = false;
  showAdminBoard = false;
  private roles: string[];

  constructor(private router: Router,
    private ds: DepartmentService,
    private route: ActivatedRoute,

    private renderer: Renderer2) {
    }

    ngOnInit(): void {
    this.renderer.setStyle(document.body, 'background-color', '#C3E6FC');
    
  }

  getform(){
    if(this.route.snapshot.params['id']>0){
      this.id=this.route.snapshot.params['id'];
      this.getDepartment();
    }
  }

  getDepartment(){
    this.ds.getDepartmentById(this.id).subscribe((data)=>{
      this.dept=data;
    },
    error=>{
      console.log(error);
    });
  }

  onSubmit() {
    if(this.id>0){
      this.update();
    }else{
      this.save();
    }
  }

  update(){
  this.ds.updateDepartment(this.id, this.dept).subscribe((data)=>
    {
      console.log(data);
      alert("department updated successfully");
      this.gotoNext();
    },
    error => {
      console.log(error);
      alert('cannot save your data');
    });
}
  save(){
    this.ds.addDepartment(this.dept).subscribe((data)=>
    {
      console.log(data);
      alert("department added successfully");
      this.gotoNext();
    },
    error => {
      console.log(error);
      alert('can not save your data');
    });
  }

  gotoNext()
  {
    this.router.navigate(['departmentList']);
  }


}
