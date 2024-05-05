from django.shortcuts import redirect, render
from django.http import HttpResponse
from employee_information.models import Department, Position, Employees, Task,Feedback
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
from django.shortcuts import render  
from django.http import HttpResponse  
employees = [

    {
        'code':1,
        'name':"John D Smith",
        'contact':'09123456789',
        'address':'Sample Address only'
    },{
        'code':2,
        'name':"Claire C Blake",
        'contact':'09456123789',
        'address':'Sample Address2 only'
    }

]
# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':'','isadmin':False}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if username=="admin":
                    setcookie(request,isadmin=True)
                else:
                    setcookie(request,isadmin=False)
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#cookies
def setcookie(request,isadmin):  
    response = HttpResponse("Cookie Set")  
    response.set_cookie('isadmin', isadmin)  
    return response  
def getcookie(request):  
    isadmin = request.COOKIES['isadmin']  
    return HttpResponse("isadmin@:"+ isadmin);  


#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
    context = {
        'page_title':'Home',
        'employees':employees,
        'total_department':len(Department.objects.all()),
        'total_position':len(Position.objects.all()),
        'total_employee':len(Employees.objects.all()),
    }
    return render(request, 'employee_information/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'employee_information/about.html',context)

# Departments
@login_required
def departments(request):
    department_list = Department.objects.all()
    context = {
        'page_title':'Departments',
        'departments':department_list,
    }
    return render(request, 'employee_information/departments.html',context)
@login_required
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()
    
    context = {
        'department' : department
    }
    return render(request, 'employee_information/manage_department.html',context)

@login_required
def save_department(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_department = Department.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_department = Department(name=data['name'], description = data['description'],status = data['status'])
            save_department.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_department(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Department.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Positions
@login_required
def positions(request):
    position_list = Position.objects.all()
    context = {
        'page_title':'Positions',
        'positions':position_list,
    }
    return render(request, 'employee_information/positions.html',context)
@login_required
def manage_positions(request):
    position = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()
    
    context = {
        'position' : position
    }
    return render(request, 'employee_information/manage_position.html',context)

@login_required
def save_position(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_position = Position.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_position = Position(name=data['name'], description = data['description'],status = data['status'])
            save_position.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_position(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Position.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
# Employees
def employees(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title':'Employees',
        'employees':employee_list,
    }
    return render(request, 'employee_information/employees.html',context)
@login_required
def manage_employees(request):
    employee = {}
    departments = Department.objects.filter(status = 1).all() 
    positions = Position.objects.filter(status = 1).all() 
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
        'departments' : departments,
        'positions' : positions
    }
    return render(request, 'employee_information/manage_employee.html',context)

@login_required
def save_employee(request):
    data =  request.POST
    resp = {'status':'failed'}
    if (data['id']).isnumeric() and int(data['id']) > 0:
        check  = Employees.objects.exclude(id = data['id']).filter(code = data['code'])
    else:
        check  = Employees.objects.filter(code = data['code'])
    print(check)
    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()
            print(dept,pos)
            print(data)
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_employee = Employees.objects.filter(id = data['id']).update(code=data['code'], firstname = data['firstname'],middlename = data['middlename'],lastname = data['lastname'],dob = data['dob'],gender = data['gender'],contact = data['contact'],email = data['email'],address = data['address'],department_id = dept,position_id = pos,date_hired = data['date_hired'],salary = data['salary'],status = data['status'])
            else:
                save_employee = Employees(code=data['code'], firstname = data['firstname'],middlename = data['middlename'],lastname = data['lastname'],dob = data['dob'],gender = data['gender'],contact = data['contact'],email = data['email'],address = data['address'],department_id = dept,position_id = pos,date_hired = data['date_hired'],salary = data['salary'],status = data['status'])
                save_employee.save()
            print("hi",save_employee)
            resp['status'] = 'success'
        except Exception:
            resp['status'] = 'failed'
            print(Exception)
            print(json.dumps({"code":data['code'], "firstname" : data['firstname'],"middlename" : data['middlename'],"lastname" : data['lastname'],"dob" : data['dob'],"gender" : data['gender'],"contact" : data['contact'],"email" : data['email'],"address" : data['address'],"department_id" : data['department_id'],"position_id" : data['position_id'],"date_hired" : data['date_hired'],"salary" : data['salary'],"status" : data['status']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employees.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_employee(request):
    employee = {}
    departments = Department.objects.filter(status = 1).all() 
    positions = Position.objects.filter(status = 1).all() 
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
        'departments' : departments,
        'positions' : positions
    }
    return render(request, 'employee_information/view_employee.html',context)


#Tasks
@login_required
def task(request):
    Task_list= Task.objects.all()
    context = {
        'page_title':'Task',
        'tasks':Task_list,
    }
    return render(request, 'employee_information/task.html',context)

@login_required
def manage_task(request):
    task = {}
    employees = Employees.objects.filter().all() 
    
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            task = Task.objects.filter(id=id).first()
    context = {
        'task':task,
        'employees':employees
        
    }
    return render(request, 'employee_information/manage_task.html',context)


@login_required
def save_task(request):
    data =  request.POST
    resp = {'status':'failed'}
    print(data)
    

    try:
            employee = Employees.objects.filter(id=data['employee_id']).first()
            print("employee",employee)
            print(data)
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                print(data)
                save_task = Task.objects.filter(id = data['id']).update(taskname=data['taskname'],taskdescription=data['taskdescription'],employee_id=employee,taskdeadline=data['taskdeadline'],taskprogress=data['taskprogress'])
            else:
                print("else exec")
                save_task = Task( taskname=data['taskname'],taskdescription=data['taskdescription'],employee_id=employee,taskdeadline=data['taskdeadline'],taskprogress=data['taskprogress'])
                print(save_task)
                save_task.save()
            
            resp['status'] = 'success'
    except Exception:
            resp['status'] = 'failed'
            print(Exception)
            print(json.dumps({ "taskname":data['taskname'],"taskdescription":data['taskdescription'],"taskdeadline":data['taskdeadline'],"taskprogress":data['taskprogress']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_task(request):
    data =  request.POST
    print(data)
    resp = {'status':''}
    try:
        Task.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#feedback
@login_required
def feedback(request):
    feedback_list = Feedback.objects.all()
    context = {
        'page_title':'Feedback',
        'feedbacks':feedback_list,
    }
    return render(request, 'employee_information/feedback.html',context)


@login_required
def manage_feedback(request):
    feedback = {}
    employees = Employees.objects.filter().all() 
    tasks= Task.objects.filter().all() 
    print(employees)
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            feedback = Feedback.objects.filter(id=id).first()
    context = {
        'feedback':feedback,
        'employees':employees,
        'tasks':tasks
        
        
    }
    return render(request, 'employee_information/manage_feedback.html',context)

@login_required
def save_feedback(request):
    data =  request.POST
    resp = {'status':'failed'}
    print(data)
    
    try:
            employee = Employees.objects.filter(id=data['employee_id']).first()
            
            task=Task.objects.filter(id=data['task_id']).first()
            
            print(employee,task)
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_feedback = Feedback.objects.filter(id = data['id']).update(title=data['title'], feedback = data['feedback'],suggestions = data['suggestion'],employee_id = employee,task_id = task)
            else:
                print("elsse exec")
                save_feedback = Feedback( title=data['title'], feedback = data['feedback'],suggestions = data['suggestion'],employee_id = employee,task_id = task)
                print(save_feedback)
                save_feedback.save()

            resp['status'] = 'success'
    except Exception:
            resp['status'] = 'failed'
            print(Exception)
            # print(json.dumps({"code":data['code'], "taskname":data['taskname'],"taskdescription":data['taskdescription'],"employee_id":employee,"taskdeadline":data['taskdeadline'],"taskprogress":data['taskprogress'],"taskcreated":data['taskcreated']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_feedback(request):
    data =  request.POST
    print(data)
    resp = {'status':''}
    try:
        Feedback.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")