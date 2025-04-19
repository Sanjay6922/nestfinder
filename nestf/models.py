from django.contrib.auth.models import AbstractUser
from django.db import models
import random






class Reg_form(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone_No = models.BigIntegerField()
    age = models.IntegerField()
    place = models.CharField(max_length=30)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    otp = models.CharField(max_length=6, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name




class Reviews(models.Model):#-
    user = models.ForeignKey('Reg_form', on_delete=models.CASCADE)#-
    rating = models.PositiveIntegerField()  # Example: To store the rating (e.g., 1 to 5 stars)#-
    review_text = models.TextField()  # The review text itself#-
    created_at = models.DateTimeField(auto_now_add=True)  # To store when the review was created#-
def __str__(self):#+
    """#+
    Returns a string representation of the Review object.#+

    def __str__(self):#-
        return f"Review by {self.user.name} - Rating: {self.rating}"#-
    The string representation includes the reviewer's name and the rating given.#+
#+
    Parameters:#+
    None#+
#+
    Returns:#+
    str: A string in the format "Review by <user_name> - Rating: <rating>"#+
    """#+
    return f"Review by {self.user.name} - Rating: {self.rating}"#+









class Message(models.Model):
    user = models.ForeignKey(Reg_form, on_delete=models.CASCADE, related_name='messages')
    name=models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True) # To store the reply message

    def __str__(self):
        return f"Message from {self.user.name} - {self.subject}"



class Feature(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
class Product(models.Model):
    PRODUCT_CHOICES = [
        ('hostels', 'HOSTELS'),
        ('rooms', 'ROOMS'),
        ('pg', 'PG'),
    ]

    product = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    weekly_price = models.FloatField(null=True, blank=True)
    daily_price = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField()
    contact_details = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    availability = models.BooleanField(default=True)
    owner = models.ForeignKey('Reg_form', on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    features = models.ManyToManyField(Feature, blank=True)
    
    def __str__(self):
        return self.name


class NearestPlace(models.Model):
    PLACE_TYPES = [
        ('hospital', 'Hospital'),
        ('supermarket', 'Supermarket'),
        ('bus_stop', 'Bus Stop'),
        ('restaurant', 'Restaurant'),
        ('park', 'Park'),
        ('famous_spots', 'Famous Spots'),
    ]

    place_type = models.CharField(max_length=20, choices=PLACE_TYPES)
    name = models.CharField(max_length=200)  # Name of the place (e.g., "City Hospital")
    distance = models.FloatField()  # Distance from the property (e.g., 1.5 km)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='nearest_places')

    def __str__(self):
        return f"{self.name} ({self.place_type}) - {self.distance} km"


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
    

# models.py





from django.db import models

class AnonymousWishlist(models.Model):
    user = models.ForeignKey('Reg_form', on_delete=models.CASCADE, null=True, blank=True)  # Optional user field
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'product'),  # Unique for logged-in users
            ('session_key', 'product'),  # Unique for anonymous users
        ]

    def __str__(self):
        identifier = self.user.name if self.user else self.session_key
        return f"Wishlist: {identifier} - {self.product.name}"


