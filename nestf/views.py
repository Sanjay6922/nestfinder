from django.shortcuts import render
from .models import Product, Reviews, Reg_form  # Import models explicitly

def index(request):
    # Fetch counts for hostels, PGs, and rooms
    hostel = Product.objects.filter(product='hostels').count()
    pg = Product.objects.filter(product='pg').count()
    room = Product.objects.filter(product='rooms').count()
    
    # Fetch total listings, reviews, and users for statistics
    total_listings = Product.objects.count()
    total_reviews = Reviews.objects.count()
    total_users = Reg_form.objects.count()
    
    # Fetch all reviews for the reviews section
    reviews = Reviews.objects.all()

    # Prepare context
    context = {
        'hostel': hostel,
        'pg': pg,
        'room': room,
        'reviews': reviews,          # For reviews section
        'total_listings': total_listings,  # For statistics
        'total_reviews': total_reviews,    # For statistics
        'total_users': total_users,        # For statistics
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method=='POST':
        name = request.POST['Name']   
        email= request.POST['Email']
        password = request.POST['Password']  
        confirm_password = request.POST['confirm_password']   
        phone_No = request.POST['phone_no']   
        age = request.POST['age']
        place= request.POST['place']
        gender= request.POST['gender']
        image=request.FILES.get('image')

        
        if  models.Reg_form.objects.filter(email=email).exists():
            alert="<script>alert('email already existed');window.location.href='/reg_form/';</script>" 
            return HttpResponse(alert)
        if password==confirm_password:
            user=models.Reg_form.objects.create(name=name,email=email,password=password,phone_No=phone_No,age=age,image=image,place=place,gender=gender)
            user.save()
            return redirect('/')
        else:
            
            alert="<script>alert('password do not match');window.location.href='/reg_form/';</script>" 
            return HttpResponse(alert)
    else:
        return render(request,'reg_form.html')
       
def login(request):
    if request.method=='POST':
        email=request.POST['Email']
        password=request.POST['Password']
        if models.Reg_form.objects.filter(email=email,password=password).exists():
            request.session['email']=email
            return redirect('/userhome/')
        else:
             alert="<script>alert('login failed');window.location.href='/login/';</script>" 
             return HttpResponse(alert)
    else:
        return render(request,'login.html')

from .models import Product, NearestPlace, ProductImage


from django.shortcuts import render
from .models import Product, Reviews  # Assuming Reviews is in the same models.py

def userhome(request):
    # Fetch counts for hostels, PGs, and rooms
    hostel = Product.objects.filter(product='hostels').count()
    pg = Product.objects.filter(product='pg').count()
    room = Product.objects.filter(product='rooms').count()
    
    # Fetch total listings count (all products)
    total_listings = Product.objects.count()
    
    # Fetch total reviews count
    total_reviews = Reviews.objects.count()
    
    # Fetch total users count
    total_users = Reg_form.objects.count()
    
    # Fetch all reviews with related user data (if needed elsewhere in the template)
    reviews = Reviews.objects.all()

    # Prepare context with all data
    context = {
        'hostel': hostel,
        'pg': pg,
        'room': room,
        'reviews': reviews,         # Full queryset for review display
        'total_reviews': total_reviews,  # Total reviews count
        'total_users': total_users,      # Total users count
        'total_listings': total_listings,  # Total listings count
    }
    return render(request, 'userhome.html', context)
  


def logout(request):
    request.session.flush()
    return redirect('/')

def add_review(request):
    if request.method == 'POST':
        review = request.POST['review']
        rating = request.POST['rating']
        user_email = request.session.get('email')
        user = models.Reg_form.objects.get(email=user_email)
        models.Reviews.objects.create(user=user, rating=rating, review_text=review)
        return redirect('userhome')
    
    else:
        return render(request, 'reviews.html')
    

from django.core.files.storage import default_storage



from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, HttpResponse

   
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Import login_required here
from . import models  # Assuming this is how you import your models

@login_required
def profile(request):
    user_email = request.session.get('email')
    if user_email:
        try:
            # Get the user based on email from session
            user = models.Reg_form.objects.get(email=user_email)
            
            # Get products owned by the user (assuming 'owner' is the ForeignKey to Reg_form)
            user_products = models.Product.objects.filter(owner=user)
            
          
            
            # Pass all data to the template
            context = {
                'user': user,
                'user_products': user_products,
                
            }
            return render(request, 'profile.html', context)
        except models.Reg_form.DoesNotExist:
            # If the user doesn't exist, redirect to login
            return redirect('/login/')
    else:
        # If no email in session, redirect to login
        return redirect('/login/')



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Reg_form





from .models import Product 




def user_profile(request):
    user_email = request.session.get('email')
    if user_email:
        try:
            reg_user = models.Reg_form.objects.get(email=user_email)
            user_products = models.Product.objects.filter(owner=reg_user)
            wishlist_items = models.AnonymousWishlist.objects.filter(user=reg_user)
            wishlist_products = [item.product for item in wishlist_items]
            print(f"User: {reg_user.name}, Listings: {len(user_products)}, Wishlist: {len(wishlist_products)}")
            context = {
                'user': reg_user,
                'user_products': user_products,
                'wishlist_products': wishlist_products,
            }
            return render(request, 'profile.html', context)
        except models.Reg_form.DoesNotExist:
            return redirect('login')  # Redirect to login if email not found
    else:
        # Anonymous user: no products, basic profile
        if not request.session.session_key:
            request.session.create()
        print(f"Anonymous profile, Session Key: {request.session.session_key}")
        return render(request, 'profile.html', {'user': None, 'user_products': []})

def edit_profile(request):
    user_email = request.session.get('email')
    if user_email:
        user = models.Reg_form.objects.get(email=user_email)
        
        if request.method == 'POST':
            user.name = request.POST['name']
            user.phone_No = request.POST['phone_no']
            user.age = request.POST['age']
            user.place = request.POST['place']
            user.gender = request.POST['gender']

            # If the user uploads a new image, update it. Otherwise, keep the existing image.
            new_image = request.FILES.get('image')
            if new_image:
                user.image = new_image  # Update with the new image
            # If no new image is selected, the old one remains

            user.save()
            return redirect('/profile/')

        return render(request, 'edit-profile.html', {'user': user})
    
    else:
        return redirect('/login/')
    
def delete_profile(request):
    delete=models.Reg_form.objects.get(email=request.session.get('email'))
    delete.delete()
    return redirect('/')

from django.shortcuts import render, redirect
from django.http import HttpResponse

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password']
        e = 'adminnestfinder@gmail.com'
        p = 'admin@123'
        if email == e and password == p:
            request.session['email'] = email
            return redirect('/admin_home/')
        else:
            alert = "<script>alert('Login failed'); window.location.href='/admin_login/';</script>"
            return HttpResponse(alert)
    else:  # Handle GET request
        return render(request, 'admin_login.html')
    
def admin_home(request):
    if 'email' in request.session:
        email=request.session['email']
    
        user=models.Reg_form.objects.count()
        mod=models.Product.objects.count()
        reviews=models.Reviews.objects.count()
       
    
        context={
             'user':user,
             'mod': mod,
             'reviews':reviews,
              # Pass the email to the template for display purposes.  # This is useful for tracking the user throughout the session.
        }
     
        return render(request,'admin_home.html', context)
    return redirect('admin_login')

def list_users(request):
    users = models.Reg_form.objects.all()
    return render(request, 'list_users.html', {'users': users})

def delete_user(request, id):
    user = models.Reg_form.objects.get(id=id)
    user.delete()
    return redirect('list_users')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Message, Reg_form

def message(request):
    if 'email' in request.session:
        email = request.session.get('email')

        # Fetch user from Reg_form based on session email
        try:
            user = Reg_form.objects.get(email=email)
        except Reg_form.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('some_error_page')  # Redirect to an error page or home
        
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            typing_message = request.POST.get('message', '')

            if subject and typing_message:
                # Save message to database
                Message.objects.create(
                    user=user,
                    name=user.name,  # Assuming Reg_form has a name field
                    subject=subject,
                    message=typing_message
                )
                alert="<script>alert('message sent suceesfully..!');window.location.href='/userhome/';</script>"
                return HttpResponse(alert) # Redirect to a success page
            
            messages.error(request, "All fields are required.")

        return render(request, 'message.html', {'user': user})
    
    messages.error(request, "You must be logged in to send a message.")
    return redirect('login')  # Redirect to login if no session email
def view_messages(request):
    msg=models.Message.objects.all()
    return render(request,'view_messages.html', {'msg':msg})





from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from . import models
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def register(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        password = request.POST['Password']
        confirm_password = request.POST['confirm_password']
        phone_No = request.POST['phone_no']
        age = request.POST['age']
        place = request.POST['place']
        gender = request.POST['gender']
        image = request.FILES.get('image')

        if models.Reg_form.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists');window.location.href='/reg_form/';</script>")
        
        if password != confirm_password:
            return HttpResponse("<script>alert('Passwords do not match');window.location.href='/reg_form/';</script>")

        # Create user and hash password
        user = models.Reg_form.objects.create(
            name=name, email=email,password=password, phone_No=phone_No, age=age,
            image=image, place=place, gender=gender
        )# Save hashed password

        # Generate OTP
        otp = generate_otp()
        user.otp = otp
        user.save()

        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}. Use it to verify your email.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp', user_id=user.id)

    return render(request, 'reg_form.html')


def verify_otp(request, user_id):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = models.Reg_form.objects.get(id=user_id)
        except models.Reg_form.DoesNotExist:
            return HttpResponse("User not found")

        if user.otp == otp:
            user.email_verified = True
            user.otp = None  # Clear OTP after verification
            user.save()
            return redirect('login')

        return HttpResponse('Invalid OTP')

    return render(request, 'verify_otp.html', {'user_id': user_id})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Message

def reply_message(request, m_id):
    message = get_object_or_404(Message, id=m_id)

    if request.method == "POST":
        reply_text = request.POST.get("reply")
        message.reply = reply_text
        message.save()
        return redirect("view_messages")  # Redirect back to messages list

    return render(request, "reply.html", {"message": message})




from .models import Message, Reg_form

def user_messages(request):
    email = request.session.get('email')  # Get email from query parameters
    if not email:
        return render(request, 'login.html')  # Redirect to login if email is not provided

    try:
        # Get the corresponding Reg_form user
        reg_user = Reg_form.objects.get(email=email)
        print(f"Found Reg_form user: {reg_user.name} (ID: {reg_user.id})")

        # Fetch messages for this user
        messages = Message.objects.filter(user=reg_user).order_by('-created_at')
        print(f"Messages count: {messages.count()}")  # Check if messages are retrieved

        for msg in messages:
            print(f"Message: {msg.subject} - {msg.message} - Reply: {msg.reply}")  # Print each message with reply

    except Reg_form.DoesNotExist:
        messages = []
        print("No matching Reg_form found for this email.")

    return render(request, "user_messages.html", {"messages": messages})

import random
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Reg_form  # Import user model
from django.contrib.auth.hashers import make_password

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = Reg_form.objects.filter(email=email).first()

        if user:
            otp = random.randint(100000, 999999)  # Generate 6-digit OTP
            request.session["otp"] = str(otp)  # Store OTP in session
            request.session["email"] = email  # Store email for verification
            request.session["otp_time"] = str(datetime.now())  # Store OTP generation time

            # Send OTP via email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp}",
                "noreply@primelandhub.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "If your email is registered, an OTP has been sent.")
            return redirect("verify_otp1")  # Redirect to OTP verification page
        else:
            messages.success(request, "If your email is registered, an OTP has been sent.")

    return render(request, "forgot_password.html")


def verify_otp1(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")  # Get OTP from session
        email = request.session.get("email")  # Get stored email
        otp_time_str = request.session.get("otp_time")

        if not stored_otp or not otp_time_str:
            messages.error(request, "Session expired. Request a new OTP.")
            return redirect("forgot_password")

        otp_time = datetime.strptime(otp_time_str, "%Y-%m-%d %H:%M:%S.%f")

        if datetime.now() > otp_time + timedelta(minutes=5):
            messages.error(request, "OTP has expired. Request a new one.")
            return redirect("forgot_password")

        if entered_otp == stored_otp:
            request.session.pop("otp")  # Remove OTP after successful verification
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP. Try again.")
    
    return render(request, "verify_otp1.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reg_form  # Your user model

def reset_password(request):
    if request.method == "POST":
        email = request.session.get("email")  # Get email from session
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not email:
            messages.error(request, "Session expired. Please request OTP again.")
            return redirect("forgot_password")

        user = Reg_form.objects.filter(email=email).first()

        if user:
            if new_password == confirm_password:
                user.password = new_password  # Save password as plain text (no hashing)
                user.save()
                messages.success(request, "Password updated successfully! Please login.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "User not found.")

    return render(request, "reset_password.html")




from django.shortcuts import render, redirect, get_object_or_404
from . import models

def list111(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(models.Product, id=product_id)
        product.delete()
        return redirect("list111")
    
    p = models.Product.objects.all()
    return render(request, 'list111.html', {'p': p})





from django.shortcuts import render
from .models import Product

def search_results(request):
    query = request.GET.get("location", "").strip()
    if query:
        results = Product.objects.filter(location__icontains=query).prefetch_related('images', 'nearest_places')
    else:
        results = []
    return render(request, "search_results.html", {"results": results, "query": query})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        return HttpResponse("<script>alert('Product deleted successfully'); window.location.href='/userhome/';</script>")

    return redirect('userhome') 





from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, ProductImage, NearestPlace

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Retrieve updated data
        product_type = request.POST.get('product')
        name = request.POST.get('name')
        price = request.POST.get('price')
        weekly_price = request.POST.get('weekly_price')
        daily_price = request.POST.get('daily_price')
        location = request.POST.get('location')
        description = request.POST.get('description')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        whatsapp_number = request.POST.get('whatsapp_number')
        availability = request.POST.get('availability') == "available"

        # Update product fields
        product.product = product_type
        product.name = name
        product.price = float(price) if price else product.price
        product.weekly_price = float(weekly_price) if weekly_price else None
        product.daily_price = float(daily_price) if daily_price else None
        product.location = location
        product.description = description
        product.phone_number = phone_number
        product.email = email
        product.whatsapp_number = whatsapp_number
        product.availability = availability
        product.save()

        # Handle existing nearest places
        for place in product.nearest_places.all():
            place_type = request.POST.get(f'place_type_{place.id}')
            place_name = request.POST.get(f'place_name_{place.id}')
            place_distance = request.POST.get(f'place_distance_{place.id}')
            if place_type and place_name and place_distance:
                place.place_type = place_type
                place.name = place_name
                place.distance = float(place_distance)
                place.save()

        # Handle new nearest places
        for key in request.POST:
            if key.startswith('place_type_new_'):
                suffix = key.replace('place_type_new_', '')
                place_type = request.POST.get(f'place_type_new_{suffix}')
                place_name = request.POST.get(f'place_name_new_{suffix}')
                place_distance = request.POST.get(f'place_distance_new_{suffix}')
                if place_type and place_name and place_distance:
                    NearestPlace.objects.create(
                        product=product,
                        place_type=place_type,
                        name=place_name,
                        distance=float(place_distance)
                    )

        # Delete selected images
        delete_image_ids = request.POST.getlist('delete_images')
        if delete_image_ids:
            images_to_delete = ProductImage.objects.filter(id__in=delete_image_ids, product=product)
            images_to_delete.delete()

        # Add new images
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return HttpResponse("<script>alert('Property updated successfully'); window.location.href='/userhome/';</script>")

    # Pass PLACE_TYPES to template
    nearest_place_types = NearestPlace.PLACE_TYPES
    return render(request, 'edit_product.html', {
        'product': product,
        'nearest_place_types': nearest_place_types
    })


# Removed invalid line





from django.shortcuts import render, redirect
from .models import Product, NearestPlace, ProductImage, Feature, Reg_form
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Feature, ProductImage, Reg_form

def register_product(request):
    semail = request.session.get('email')
    if not semail:
        messages.error(request, "You must be logged in to register a property.")
        return redirect('login')

    try:
        owner = Reg_form.objects.get(email=semail)
    except Reg_form.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        try:
            print("POST Data:", request.POST)
            print("FILES Data:", request.FILES)

            required_fields = ['product', 'name', 'price', 'location', 'description']
            for field in required_fields:
                if not request.POST.get(field):
                    raise ValueError(f"Missing required field: {field}")

            product = Product(
                product=request.POST.get('product'),
                name=request.POST.get('name'),
                price=float(request.POST.get('price')),
                weekly_price=float(request.POST.get('weekly_price', 0)),
                daily_price=float(request.POST.get('daily_price', 0)),
                location=request.POST.get('location'),
                description=request.POST.get('description'),
                contact_details=request.POST.get('contact_details', ''),
                phone_number=request.POST.get('phone_number', ''),
                email=request.POST.get('email', ''),
                whatsapp_number=request.POST.get('whatsapp_number', ''),
                availability=bool(int(request.POST.get('availability'))),
                owner=owner
            )
            product.save()
            print("Product saved with ID:", product.id)

            # Save features
            features = request.POST.getlist('features')
            print("Selected Features:", features)
            if features:
                feature_objects = Feature.objects.filter(name__in=features)
                existing_features = set(feature_objects.values_list('name', flat=True))
                missing_features = set(features) - existing_features
                if missing_features:
                    messages.warning(request, f"Some features not found: {missing_features}")
                if feature_objects.exists():
                    product.features.set(feature_objects)
                    print("Features associated:", list(product.features.all()))
                else:
                    print("No valid features to associate.")
            else:
                print("No features selected.")

            # Save images
            images = request.FILES.getlist('images')  # Get list of uploaded files
            if images:
                for image in images:
                    product_image = ProductImage(
                        product=product,
                        image=image
                    )
                    product_image.save()
                    print(f"Image saved for product: {product.name}")
            else:
                print("No images uploaded.")

            # Save nearest places
            nearest_places_count = int(request.POST.get('nearest_places_count', 0))
            for i in range(nearest_places_count):
                place_type = request.POST.get(f'place_{i}_place_type')
                name = request.POST.get(f'place_{i}_name')
                distance = request.POST.get(f'place_{i}_distance')
                if place_type and name and distance:
                    try:
                        NearestPlace.objects.create(
                            product=product,
                            place_type=place_type,
                            name=name,
                            distance=float(distance)
                        )
                        print(f"Nearest place {i}: {place_type}, {name}, {distance}km saved to database")
                    except Exception as e:
                        print(f"Error saving nearest place {i}: {str(e)}")
                        messages.warning(request, f"Error saving nearest place {name}: {str(e)}")
                else:
                    print(f"Skipping incomplete nearest place {i}")

            messages.success(request, "Property registered successfully!")
            return redirect('userhome')

        except ValueError as e:
            messages.error(request, f"Invalid input: {str(e)}")
            print("ValueError:", str(e))
        except Exception as e:
            messages.error(request, f"Error registering property: {str(e)}")
            print("Exception:", str(e))

    # For GET request, pass all available features to the template
    features = Feature.objects.all()
    return render(request, 'register_product.html', {'features': features})






def rooms(request):
    # Base queryset for rooms
    rooms_list = models.Product.objects.filter(product='rooms').prefetch_related('images', 'nearest_places')

    # Handle wishlist
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    email = request.session.get('email')
    user = None

    if email:
        try:
            user = models.Reg_form.objects.get(email=email)
            session_key = None
        except models.Reg_form.DoesNotExist:
            user = None

    wishlist_items = models.AnonymousWishlist.objects.filter(
        Q(user=user) | Q(session_key=session_key if not user else None)
    )
    wishlist = [item.product.id for item in wishlist_items]

    # Apply filters
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', '')  # Get sort_by parameter

    print(f"Received sort_by: {sort_by}")  # Debug the received sort_by value

    if location:
        rooms_list = rooms_list.filter(location__icontains=location)
    if min_price:
        try:
            min_price = float(min_price)
            rooms_list = rooms_list.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass
    if max_price:
        try:
            max_price = float(max_price)
            rooms_list = rooms_list.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass

    # Apply sorting
    if sort_by:
        print(f"Applying sorting: {sort_by}")  # Debug sorting application
        if sort_by == 'price_asc':
            rooms_list = rooms_list.order_by('price')
        elif sort_by == 'price_desc':
            rooms_list = rooms_list.order_by('-price')
        elif sort_by == 'name_asc':
            rooms_list = rooms_list.order_by('name')
        elif sort_by == 'name_desc':
            rooms_list = rooms_list.order_by('-name')
        else:
            print(f"Invalid sort_by value: {sort_by}")  # Debug invalid sort_by

    # Check the sorted queryset
    print("Sorted rooms:", list(rooms_list.values('id', 'name', 'price','weekly_price','daily_price')))  # Debug the result

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        rooms_data = [{
            'id': room.id,
            'name': room.name,
            'location': room.location,
            'price': float(room.price),
            'weekly_price': float(room.weekly_price),
            'daily_price': float(room.daily_price),
            'availability': room.availability,
            'description': room.description,
            'images': [image.image.url for image in room.images.all()],
            'phone_number': room.phone_number or '',
            'email': room.email or '',
            'whatsapp_number': room.whatsapp_number or '',
            'in_wishlist': room.id in wishlist
        } for room in rooms_list]
        return JsonResponse({'rooms': rooms_data})

    return render(request, 'rooms.html', {'rooms_list': rooms_list, 'wishlist': wishlist})




from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from . import models

def pg_list_view(request):
    # Base queryset for PGs
    pg_list = models.Product.objects.filter(product='pg').prefetch_related('images', 'nearest_places', 'features')

    # Handle wishlist for both authenticated and anonymous users
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    email = request.session.get('email')
    user = None

    if email:
        try:
            user = models.Reg_form.objects.get(email=email)
            session_key = None  # Use user instead of session_key for authenticated users
        except models.Reg_form.DoesNotExist:
            user = None

    wishlist_items = models.AnonymousWishlist.objects.filter(
        Q(user=user) | Q(session_key=session_key if not user else None)
    )
    wishlist = [item.product.id for item in wishlist_items]

    # Apply filters from GET request
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', '')

    # Debugging
    print(f"Received parameters - Location: {location}, Min Price: {min_price}, Max Price: {max_price}, Sort By: {sort_by}")

    if location:
        pg_list = pg_list.filter(location__icontains=location)
    if min_price:
        try:
            min_price = float(min_price)
            pg_list = pg_list.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass  # Ignore invalid min_price
    if max_price:
        try:
            max_price = float(max_price)
            pg_list = pg_list.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass  # Ignore invalid max_price

    # Apply sorting
    if sort_by:
        print(f"Applying sorting: {sort_by}")
        if sort_by == 'price_asc':
            pg_list = pg_list.order_by('price')
        elif sort_by == 'price_desc':
            pg_list = pg_list.order_by('-price')
        elif sort_by == 'name_asc':
            pg_list = pg_list.order_by('name')
        elif sort_by == 'name_desc':
            pg_list = pg_list.order_by('-name')
        else:
            print(f"Invalid sort_by value: {sort_by}")

    # Debug the sorted queryset
    print("Sorted PGs:", list(pg_list.values('id', 'name', 'price', 'weekly_price', 'daily_price')))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        pg_data = [{
            'id': pg.id,
            'name': pg.name,
            'location': pg.location,
            'price': float(pg.price),
             'weekly_price': float(pg.weekly_price),
            'daily_price': float(pg.daily_price),
            'availability': pg.availability,
            'description': pg.description,
            'images': [image.image.url for image in pg.images.all()],
            'phone_number': pg.phone_number or '',
            'email': pg.email or '',
            'whatsapp_number': pg.whatsapp_number or '',
            'in_wishlist': pg.id in wishlist,
            'features': [{'name': feature.name} for feature in pg.features.all()]  # Added features
        } for pg in pg_list]
        return JsonResponse({'pgs': pg_data})

    return render(request, 'PG.html', {'pg_list': pg_list, 'wishlist': wishlist})


from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from . import models

def hostels(request):
    # Base queryset for hostels
    hostels_list = models.Product.objects.filter(product='hostels').prefetch_related('images', 'nearest_places')

    # Handle wishlist for both authenticated and anonymous users
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    email = request.session.get('email')
    user = None

    if email:
        try:
            user = models.Reg_form.objects.get(email=email)
            session_key = None  # Use user instead of session_key for authenticated users
        except models.Reg_form.DoesNotExist:
            user = None

    wishlist_items = models.AnonymousWishlist.objects.filter(
        Q(user=user) | Q(session_key=session_key if not user else None)
    )
    wishlist = [item.product.id for item in wishlist_items]

    # Apply filters from GET request
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', '')  # Get sort_by parameter

    # Debugging
    print(f"Received parameters - Location: {location}, Min Price: {min_price}, Max Price: {max_price}, Sort By: {sort_by}")

    if location:
        hostels_list = hostels_list.filter(location__icontains=location)
    if min_price:
        try:
            min_price = float(min_price)
            hostels_list = hostels_list.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass  # Ignore invalid min_price
    if max_price:
        try:
            max_price = float(max_price)
            hostels_list = hostels_list.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass  # Ignore invalid max_price

    # Apply sorting (exact same as pg.html)
    if sort_by:
        print(f"Applying sorting: {sort_by}")
        if sort_by == 'price_asc':
            hostels_list = hostels_list.order_by('price')
        elif sort_by == 'price_desc':
            hostels_list = hostels_list.order_by('-price')
        elif sort_by == 'name_asc':
            hostels_list = hostels_list.order_by('name')
        elif sort_by == 'name_desc':
            hostels_list = hostels_list.order_by('-name')
        else:
            print(f"Invalid sort_by value: {sort_by}")

    # Debug the sorted queryset
    print("Sorted Hostels:", list(hostels_list.values('id', 'name', 'price', 'weekly_price', 'daily_price')))

    # Handle AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        hostels_data = [{
            'id': hostel.id,
            'name': hostel.name,
            'location': hostel.location,
            'price': float(hostel.price),
            'weekly_price': float(hostel.weekly_price),
            'daily_price': float(hostel.daily_price),
            'description': hostel.description,
            'availability': hostel.availability,
            'phone_number': hostel.phone_number or '',
            'email': hostel.email or '',
            'whatsapp_number': hostel.whatsapp_number or '',
            'images': [img.image.url for img in hostel.images.all()],
            'in_wishlist': hostel.id in wishlist
        } for hostel in hostels_list]
        return JsonResponse({'hostels': hostels_data})

    return render(request, 'hostels.html', {'hostels_list': hostels_list, 'wishlist': wishlist})


def search_nearby_places(request, product_id, place_type):
    # Get the product and its nearest places of the specified type
    product = Product.objects.get(id=product_id)
    nearby_places = product.nearest_places.filter(place_type=place_type)
    return render(request, 'nearby_places.html', {'product': product, 'nearby_places': nearby_places, 'place_type': place_type})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models

@csrf_exempt
def toggle_wishlist(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        print(f"Room ID: {room_id}")

        # Get email from session (if set)
        email = request.session.get('email')
        if email:
            try:
                user = models.Reg_form.objects.get(email=email)
                session_key = None  # No session_key if user is identified by email
                print(f"User detected via email: {user.name}")
            except models.Reg_form.DoesNotExist:
                user = None
                print(f"No user found for email: {email}")
        else:
            user = None
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            print(f"Anonymous Session Key: {session_key}")

        try:
            room = models.Product.objects.get(id=room_id)
            wishlist_item, created = models.AnonymousWishlist.objects.get_or_create(
                user=user,
                session_key=session_key,
                product=room
            )
            if not created:
                wishlist_item.delete()
                print(f"Removed {room_id} from wishlist")
                return JsonResponse({'added': False})
            print(f"Added {room_id} to wishlist")
            return JsonResponse({'added': True})
        except models.Product.DoesNotExist:
            print(f"Room {room_id} not found")
            return JsonResponse({'error': 'Room not found'}, status=404)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)



from django.http import JsonResponse
from . import models

def toggle_hostel_wishlist(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    hostel_id = request.POST.get('hostel_id')
    if not hostel_id:
        return JsonResponse({'error': 'Hostel ID is required'}, status=400)

    print(f"Hostel ID: {hostel_id}")

    # Ensure session exists for anonymous users
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    email = request.session.get('email')
    user = None

    if email:
        try:
            user = models.Reg_form.objects.get(email=email)
            session_key = None  # Use user instead of session_key for authenticated users
            print(f"User detected via email: {user.name}")
        except models.Reg_form.DoesNotExist:
            print(f"No user found for email: {email}")
            user = None
    else:
        print(f"Anonymous Session Key: {session_key}")

    try:
        hostel = models.Product.objects.get(id=hostel_id, product='hostels')
        wishlist_item, created = models.AnonymousWishlist.objects.get_or_create(
            user=user,
            session_key=session_key if not user else None,
            product=hostel
        )
        if not created:
            wishlist_item.delete()
            print(f"Removed {hostel_id} from wishlist")
            return JsonResponse({'added': False})
        print(f"Added {hostel_id} to wishlist")
        return JsonResponse({'added': True})
    except models.Product.DoesNotExist:
        print(f"Hostel {hostel_id} not found")
        return JsonResponse({'error': 'Hostel not found'}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)




from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from . import models

def toggle_pg_wishlist(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    room_id = request.POST.get('room_id')
    if not room_id:
        return JsonResponse({'error': 'Room ID is required'}, status=400)

    print(f"Room ID: {room_id}")

    # Ensure session exists for anonymous users
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    email = request.session.get('email')
    user = None

    if email:
        try:
            user = models.Reg_form.objects.get(email=email)
            session_key = None  # Use user instead of session_key for authenticated users
            print(f"User detected via email: {user.name}")
        except models.Reg_form.DoesNotExist:
            print(f"No user found for email: {email}")
            user = None
    else:
        print(f"Anonymous Session Key: {session_key}")

    try:
        pg = models.Product.objects.get(id=room_id, product='pg')  # Ensure it's a PG
        wishlist_item, created = models.AnonymousWishlist.objects.get_or_create(
            user=user,
            session_key=session_key if not user else None,
            product=pg
        )
        if not created:
            wishlist_item.delete()
            print(f"Removed {room_id} from wishlist")
            return JsonResponse({'added': False})
        print(f"Added {room_id} to wishlist")
        return JsonResponse({'added': True})
    except models.Product.DoesNotExist:
        print(f"PG {room_id} not found")
        return JsonResponse({'error': 'PG not found'}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    
    from django.shortcuts import render
from .models import Reviews

def show_reviews(request):
    reviews = Reviews.objects.all()
    return render(request, 'list_reviews.html', {'reviews': reviews})

from django.shortcuts import redirect, get_object_or_404
from .models import Reviews

def delete_review(request, review_id):
    review = get_object_or_404(Reviews, id=review_id)
    if request.method == 'POST':
        review.delete()
    return redirect('show_reviews')  # Redirect to the review list
