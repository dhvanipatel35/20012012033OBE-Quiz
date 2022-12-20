from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from meal.forms import MealForm
from .forms import ContactForm
from meal.models import Meal,TableBooking,TableDetail,Finalbooked,Administrative
from meal.forms import CartAddProductForm
from django.contrib import messages
from django.http import HttpResponseRedirect,request
from django.views import generic
from ERestorent.settings import BASE_DIR
import os
from app1.forms import Site_User_Form,Form_Login,Form_Site_User
from app1.models import Orders,Site_User,Temp_Food, PermanentOrders
from django.urls import reverse_lazy
#from Pay import Checksum
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import random
import qrcode
#email
import smtplib
import email.message
#time
import time
from datetime import datetime, timezone
import razorpay

def index(request):
    if 'user' in request.session:
        form11 = Meal.objects.all()
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'index.html',{'form':form,'data':form11})
    else:
        return redirect('login')

def palce_order(request,id):
    cart = Orders()
    user = Site_User.objects.get(email=request.session['user'])
    product = get_object_or_404(Meal, id=id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart.user_name=user
        cart.meal_name=product.name
        cart.meal_qty = request.POST['quantity']
        cart.meal_price = int(product.price) * int(cart.meal_qty)
        
        qrdata = f"""
            name = {user}
            meal = {product.name}
            Qauntity = {cart.meal_qty}
            Price = {cart.meal_price}
            """ 
        num = random.randint(1111,9999)
        qr=qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(qrdata)
        qr.make(fit=True)
        img=qr.make_image(fill="black",back_color="white")
        img.save(os.path.join(BASE_DIR,"media/"+ str(num) +".jpeg"))
        y = f'{num}.jpeg'
        cart.qrimage=y
        #cart = Orders.objects.create(user_name=user,meal_name=product.name,meal_qty=cart.meal_qty,qrimage=y)
        cart.save()
        print("QR Saved")
            
        return redirect('order')

def orders(request):
    if 'user' in request.session:
        tot = 0
        user = Site_User.objects.get(email=request.session['user'])
        show_data = Orders.objects.all().filter(user_name=user)
        for i in show_data:
            tot += i.meal_price
        razorpay_amount=tot*100
        request.session['Order_total']=tot
    # ---------------------------------------------------------
        # amount = request.session['Order_total']
        if request.method == "POST":
            client = razorpay.Client(
            auth=("rzp_test_qDwTmKnksUVsaC", "QOr66ZQbsLdNZOmrV4YGX50V"))
            payment = client.order.create({'amount': razorpay_amount, 'currency': 'INR',
                                    'payment_capture': '1'})
            # ----------------------------------------------------
            client.order.create({
            'amount': tot*100,
            'currency': 'INR',
            'payment_capture': '1'
            })
            # ----------------------------------------------------
            for i in show_data:
                print("Saving order data on database")
                PermanentOrders.objects.create(
                    user_name=user, 
                    meal_name= i.meal_name, 
                    meal_qty= i.meal_qty, 
                    meal_price= i.meal_price
            )
            # ----------------------------------------------------
            show_data.delete()
            return(redirect('PAYMENT'))



        # # --------------------------Razorpay End--------------------------
        # payment1 = client.order.create({
        #     'amount': amount*100,
        #     'currency': 'INR',
        #     'payment_capture': '1'
        # })     
        # print("Payment Successfully Done", payment1)  
    # --------------------------Saving Orders on Permanent orders--------------------------
        # for i in show_data:
        #     print("Saving order data on database")
        #     PermanentOrders.objects.create(
        #         user_name=user,
        #         meal_name= i.meal_name, 
        #         meal_qty= i.meal_qty, 
        #         meal_price= i.meal_price
        # )
        # show_data.delete()
        # print("Payment Successfully Done")  
        # return(redirect('PAYMENT'))
    # --------------------------SMTP Start--------------------------
    
        # ---------------------------------------------------------
        return render(request,'orders.html',{'data':show_data,'total':tot,'razor':razorpay_amount,'User':user.name})
    else:
        return redirect('login')
    
def cart_remove(request,id):
    if 'user' in request.session:
        product = Orders.objects.get(id=id)
        product.delete()
        return redirect('order')
    else:
        return redirect('login')
    
def Checkavailability(request):
    if 'user' in request.session:
        foodname = request.POST['foodname'].strip()
        form1 =Meal.objects.filter(name__icontains=foodname)
        foodcount =Meal.objects.filter(name__icontains=foodname).count()
        return render(request,'index.html',{'meal':form1,'mealcheck':foodname,'foodcount':foodcount})
    else:
        return redirect('login')

def Mealview(request,choise):
    if 'user' in request.session:
        form1 =Meal.objects.all().filter(main_category = choise)
        if choise == 'vage':
            return render(request,'Meal.html',{'vag_meal': form1})
        elif choise == 'nonvage':
            return render(request,'Meal.html',{'non_vag_meal': form1})
        else:
            return render(request,'Meal.html',{'meal': form1})
    else:
        return redirect('login')

def VageMealview(request,choise):
    if 'user' in request.session:
        form1 =Meal.objects.all().filter(main_category = 'vage',category = choise)
        return render(request,'Meal.html',{'meal': form1})
    else:
        return redirect('login')

def NonVageMealview(request,choise):
    if 'user' in request.session:
        form1 =Meal.objects.all().filter(main_category = 'nonvage',category = choise)
        return render(request,'Meal.html',{'meal': form1})
    else:
        return redirect('login')

def Meal_single(request, id):
    if 'user' in request.session:
        book = Meal.objects.get(id = id)
        cart_product_form = CartAddProductForm()
        context = {
            'data':book,
            'cart_product_form': cart_product_form
        }
        return render(request,'meal-single.html',context)
    else:
        return redirect('login')

def restaurant(request):
    if 'user' in request.session:
        return render(request,'restaurant.html')
    else:
        return redirect('login')

def about(request):
    if 'user' in request.session:
        print(request.session['user'])
        return render(request,'about.html',{})
    else:
        return redirect('login')

def contact(request):
    if 'user' in request.session:
        form1 = ContactForm(request.POST)   
        if form1.is_valid():
            form1.save()
        return render(request,'contact.html',{'form1':form1})
    else:
        return redirect('login')

# ----------------------------------------------------
def RegisterView01(request):
    reg = Form_Site_User(request.POST or None)
    if reg.is_valid():
        obj = Site_User()
        obj.name = reg.cleaned_data['name']
        obj.dob = reg.cleaned_data['dob']
        obj.email = reg.cleaned_data['email']
        obj.m_no = reg.cleaned_data['mobile_no']
        obj.password = reg.cleaned_data['password1']
        obj.save()
        return redirect('login')
    return render(request,'registration/register.html',{'form':reg})
# ----------------------------------------------------

def RegisterView(request):
    if request.POST:
        try:
            data = Site_User.objects.get(email=request.POST['email'])
            if data:
                msg = "Email already registered"
                return render(request,'registration/register.html', {'msg':msg})
        except:
            if request.POST['confirmPassword'] == request.POST['password']:
                Site_User.objects.create(
                    name = request.POST['name'], 
                    email = request.POST['email'], 
                    dob = request.POST['dob'], 
                    m_no =  request.POST['mobile_no'], 
                    password = request.POST['password']
                )
                print("Signed up successfully")
                return redirect('login')
            else:
                msg = 'Please Enter Same Password'
                return render(request , 'registration/register.html',{'msg':msg})
    return render(request,'registration/register.html')

# ----------------------------------------------------
def LoginView(request):
    if request.POST:
        email = request.POST['email']
        pass1 = request.POST['password']
        try:
            valid = Site_User.objects.get(email=email,password=pass1)
            if valid:
                request.session['user'] = email
                return redirect('index')
        except:
            msg = f'{email} does not exist'
            return render(request , 'registration/login.html',{'msg':msg})
    return render(request,'registration/login.html')
    
def LogoutView(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('login')
    else:
        return redirect('login')

def verify(request):
    if request.POST:
        em = request.POST['email']
        m_no = int(request.POST['m_no'])
        try:
            valid = Site_User.objects.get(email=em)
            if valid.m_no == m_no:
                request.session['new'] = em
                return redirect('change_pass')
            else:
                messages.add_message(request,messages.ERROR,"Number Not Exist")
        except:
            messages.add_message(request,messages.ERROR,"Email Not Exist")
    return render(request,'verify.html')

def change_pass(request):
    if 'new' in request.session:
        if request.POST:
            p1 = request.POST['pass1']
            p2 = request.POST['pass2']
            if p1 == p2:
                obj = Site_User.objects.get(email=request.session['new'])
                obj.password = p2
                obj.save()
                del request.session['new']
                return redirect('login')
            else:
                messages.add_message(request,messages.ERROR,'Not Same Password') 

        return render(request,'change.html',{'email':request.session['new']})
    else:
        return redirect('login')

def EmailCall(request):
    print("----------------------Inside Email Call----------------------")
    user = Site_User.objects.get(email=request.session['user'])
    show_data = Orders.objects.all().filter(user_name=user)
    amount = request.session['Order_total']
 
    # --------------------------Razorpay Start--------------------------

    if request.method == "POST":
            client = razorpay.Client(
                auth=("rzp_test_qDwTmKnksUVsaC", "QOr66ZQbsLdNZOmrV4YGX50V"))

            payment = client.order.create({'amount': amount, 'currency': 'INR',
                                        'payment_capture': '1'})
            
    # client = razorpay.Client(auth=(
    #             "rzp_test_qDwTmKnksUVsaC", 
    #             "QOr66ZQbsLdNZOmrV4YGX50V"
    #         ))
   
    # --------------------------Razorpay End--------------------------

    payment = client.order.create({
        'amount': amount*100,
        'currency': 'INR',
        'payment_capture': '1'
    })     
    print("Payment Successfully Done", payment)  
    
    # --------------------------Saving Orders on Permanent orders--------------------------
    for i in show_data:
        print("Saving order data on database")
        PermanentOrders.objects.create(
            user_name=user, 
            meal_name= i.meal_name, 
            meal_qty= i.meal_qty, 
            meal_price= i.meal_price
    )
    return(redirect('PAYMENT'))
    # --------------------------SMTP Start--------------------------
    # my_email = "mailtesting681@gmail.com"
    # my_pass = "mailtest123@"
    # fr_email = user.email     
    # server = smtplib.SMTP('smtp.gmail.com',587)
    # mead_data = ""
    # front = """
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <div>
    #             <h2>Name : """ + user.name + """</h2>
    #             <h2>Email : """ + user.email + """</h2>
    #         </div>
    #         <br>
    #         <div>
    #             <table border="2">
    #                 <thead>
    #                     <tr>
    #                         <th>
    #                             Product Name
    #                         </th>
    #                         <th>
    #                             Product Qty
    #                         </th>
    #                         <th>
    #                             Product Price
    #                         </th>
    #                     </tr>
    #                 </thead>
    #                 <tbody>"""
                    
    # for i in show_data:
    #     mead_data += """<tr>
    #     <td>""" + str(i.meal_name) + """ </td>
    #     <td>""" + str(i.meal_qty) + """ </td> 
    #     <td>""" + str(i.meal_price) + """</td></td>
    #     </tr> """
        
    # ended = """<tr>
    # <td colspan="2">
    # You Have Paid
    # </td><td> """ + str(amo) + """
    #                         </td>
    #                     </tr>
    #                 </tbody>
    #             </table>
    #         </div> 
    #         <br>
    #         <div>
    #             <h3>Thank you for visiting ....</h3>
    #         </div>
    #     </body>
    # </html>
    # """
    
    # email_content = front + mead_data + ended
    # print(email_content)
    
    # msg = email.message.Message()
    # msg['Subject'] = 'Your Bill' 
    # msg['From'] = my_email
    # msg['To'] = fr_email
    # password = my_pass
    # msg.add_header('Content-Type', 'text/html')
    # msg.set_payload(email_content)
    # s = smtplib.SMTP('smtp.gmail.com',587)
    # s.starttls()
    # s.login('mailtesting681@gmail.com','mailtest123@')
    # s.sendmail(msg['From'], [msg['To']], msg.as_string())
    # show_data.delete()
    # print("963")
    # return(redirect('PAYMENT'))
    
def payment(request):
        mainMsg = "Thanks for choosing our services"
        return(render(request,'paymentSuccessPage.html',{'mainHeading':mainMsg}))

def allOrders(request):
    if 'user' in request.session:
        user = Site_User.objects.get(email=request.session['user'])
        allOrders = PermanentOrders.objects.filter(user_name=user)
        return render(request, 'allOrders.html', {'allOrders': allOrders}) 
    else:
        return redirect('login')   

def tablebooking(request,Table_No):
    if 'user' in request.session:
        user = Site_User.objects.get(email=request.session['user'])
        table=TableDetail.objects.get(Table_No=Table_No)
        print(table)
        print(user)
        print(table)
        request.session['table_no']=Table_No
        razorpay_amount=(table.Table_Price/2)*100
        print(razorpay_amount)
        #print(request.session['table_no'])
        try:
            if table.is_available==True:
                if request.method == "POST":
                    client = razorpay.Client(
                    auth=("rzp_test_qDwTmKnksUVsaC", "QOr66ZQbsLdNZOmrV4YGX50V"))
                    # ----------------------------------------------------
                    client.order.create({
                    'amount': razorpay_amount,
                    'currency': 'INR',
                    'payment_capture': '1'
                    })
                    model=TableBooking()
                    model.usereamil=user
                    model.table_no=table
                    model.time1=request.POST['time1']
                    model.date=request.POST['date']
                    model.save()
                    messages.info(request, f"Wait for approval table booking...")
                    return(redirect('PAYMENT'))
                return render(request,'booking.html',{'razor':razorpay_amount,'user':user,'table':table})
            else:
                    messages.info(request,'This table is booked already...')
                    return HttpResponseRedirect("/alltable/")
        except:
            messages.error(request, f"Table is Booked already..")  
    else:
        return redirect('login')
    return render(request,'booking.html',{'razor':razorpay_amount})


# def try():
#     if 'user' in request.session:
#         user = Site_User.objects.get(email=request.session['user'])
#         table=TableDetail.objects.get(Table_No=Table_No)
#         request.session['table_no']=Table_No
#         print(request.session['table_no'])
#         try:
#             if table.is_available==True:
#                 if request.method=="POST":
#                     model=TableBooking()
#                     model.usereamil=user
#                     model.table_no=table
#                     model.time1=request.POST['time1']
#                     model.date=request.POST['date']
#                     model.save()
#                     messages.info(request, f"Wait for approval table booking...")
#             else:
#                 messages.info(request,'This table is booked already...')
#                 return HttpResponseRedirect("/alltable/")
#         except:
#             messages.error(request, f"Table is Booked already..")  
#     else:
#         return redirect('login')
#     return render(request,'booking.html',{'user':user,'table':table})

def show_all(request):
    if 'user' in request.session:
        data=TableDetail.objects.all()
        
        return render(request,'alltable.html',{'data':data})
    # return redirect('login')
    else:
        return redirect('login')

def alltablebook(request):
    if 'email' in  request.session:     
        all=TableBooking.objects.all()
        return render(request,'allshow.html',{'all':all})
    else:
        return redirect('login')

# OrderList
 
def OrderList(request):
    if 'email' in  request.session:     
        all=Orders.objects.all()
        return render(request,'OrderList.html',{'all':all})
    else:
        return redirect('login')

def Account_status(request):
    if 'email' in  request.session:
        z = TableBooking.objects.all().filter(booked=False)
        return render(request, 'account_status.html', {'z': z})
    else:
        return redirect('login_admin')

def edit(request,id):
    if 'email' in  request.session:
        table=TableBooking.objects.get(id=id)
        return render(request,'edit.html',{'table':table})
    else:
        return redirect('login_admin')

def Approve_acc(request, id):
    if 'email' in  request.session:
        z = TableBooking.objects.get(id=id)
        if request.method=='POST':
            
            try:
                z.booked=request.POST['booked']
                print(z.booked)
                z.save()
                model=TableDetail.objects.get(Table_No=request.session['table_no'])
                model.is_available=False
                model.save()
     
                return redirect('/allshow/')
            except:
                return render(request, 'edit.html', {'msg': 'Something Went Wrong'})
           
        return render(request, 'edit.html')
    else:
        return redirect('/login_admin/')

def login_admin(request):
    if request.method == 'POST':
        print("done")
        try:
            email = request.POST['ema']
            password = request.POST['pas']
            user = Administrative.objects.get(email=email)
            print(user)
            if user.password == password:
                request.session['email'] = email
                print("loged")
                request.session['email'] = email
                return redirect('allshow')
            else:
                return render(request, 'login_admin.html' , {'msg': 'Wrong Password'})
        except:
            return render(request, 'login_admin.html' , {'msg': 'Wrong Email Address'})
    return render(request, 'login_admin.html')

def signup_admin(request):
    if request.POST:
        obj = Administrative()
        obj.name = request.POST['name']
        obj.dob = request.POST['dob']
        obj.email = request.POST['email']
        obj.m_no = request.POST['mobile_no']
        obj.password = request.POST['password']
        obj.save()
        return redirect('login_admin')
    return render(request,'signup_admin.html')

def logout_admin(request):
    if request.session.has_key('email'):
        del request.session['email']
        return redirect('/login_admin/')
    else:
        return redirect('/login_admin/')


def historydta(request):
    if 'user' in request.session:
        mod=Site_User.objects.get(email=request.session['user'])
        table=TableBooking.objects.filter(usereamil=mod)
        return render(request,'history.html',{'mod':mod,'table':table})
    else:
        return redirect('login')

