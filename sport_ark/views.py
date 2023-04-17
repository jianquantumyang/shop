from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
# Create your views here.


class Index(LoginRequiredMixin, ListView):
    template_name="index.html"
    model = Product
    context_object_name = "products"
    login_url = "/accounts/login/"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["categories"] = Category.objects.all()
        return data

@login_required
def search(request):
    context = {"products":Product.objects.filter(name__contains=request.GET["name"]),"search":request.GET["name"]}
    return render(request,"search.html",context=context)

class Categories(LoginRequiredMixin,ListView):
    template_name="category.html"
    model = Category
    context_object_name="categories"
   

from django.shortcuts import redirect

@login_required
def zakazat(request,id):
    if request.method == "POST":
        try:
            product = Product.objects.get(pk=int(id))
            if int(request.POST["count"]) > 100:
                counts = 100
            else:
                counts = int(request.POST["count"])
            zakaz_ = Zakaz(count=counts, product_zakaz=product, zakazatel=request.user)
            zakaz_.save()
            return redirect("/product/" + str(id) + "?form=success")
        except:
            return redirect("/")
    return redirect("/")


class Pod_Category_Detail(LoginRequiredMixin, DetailView):
    model = Pod_Category
    template_name="pod_category.html"
    context_object_name = "cat"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["products"] = Product.objects.filter(pod_category=self.object)
        return data


class Category_Detail(LoginRequiredMixin, DetailView):
    model = Category
    template_name="category_detail.html"
    context_object_name = "cat"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["pod_categories"] = Pod_Category.objects.filter(category_roditel=self.object)
        data["products"] = Product.objects.filter(category=self.object)
        return data

class Product_Detail(LoginRequiredMixin,DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product_obj"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            if Zakaz.objects.filter(zakazatel=self.request.user,product_zakaz=self.object)[0]!=None:
                data["rating"]=True
            else:
                data["rating"]=False
        except:
            data["rating"] = False

        try:
            if self.request.GET["form"]=="success":
                data["form"] = True
            else:
                data["form"] = False
        except:
            data["form"] = False
        try:
            
            data["ratins"] = self.object.rating/len(RatingProduct.objects.filter(product=self.object))
        except:
            data["ratins"] = 0
        return data
    

@login_required
def rating(request,id ):
    if request.method=="POST":
        if int(request.POST["rate"])>=6:
            rate = 5
        else: 
            rate = int(request.POST["rate"])
        try:
            rating_obj = RatingProduct.objects.get(author=request.user,product=Product.objects.get(pk=int(id)))
        except:
            rating_obj = None
        
        product = Product.objects.get(pk=int(id))
        if rating_obj==None:
            rating_sa = RatingProduct(author=request.user,
                              text=request.POST["text"],
                              rating=rate,
                              product=product)
            
            
            product.rating+=rate
            
            
            rating_sa.save()
        else:
            rating_obj.text = request.POST["text"]
            
            
            product.rating-=rating_obj.rating

            product.rating+=rate
            
            rating_obj.rating = rate
            
            rating_obj.save()
        
        return redirect("/product/"+str(id))
    return "redirect:/"

from django.contrib.auth import login, authenticate

from .forms import SignUpForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password,
            email=request.POST['email'])
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

