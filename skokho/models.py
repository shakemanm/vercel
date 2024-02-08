from django.db import models

import uuid







class Contact_item(models.Model):
    phone = models.CharField(max_length=10)
    def __str__ (self):
        return str(self.phone)

class Opt_item(models.Model):
    otp = models.CharField(max_length=4)
    def __str__ (self):
        return str(self.otp)
    
    





def generate_filename(instance, filename, image_type):
    extension = filename.split('.')[-1]
    image_type_str = "passport" if image_type == "passport_image" else "ck"
    
    # Extract first and last names
    first_name = instance.first_name
    surname = instance.surname

    # Check if the client has multiple names
    if hasattr(instance, 'middle_name') and instance.middle_name:
        # Use middle name if available
        full_name = f"{first_name}_{instance.middle_name}_{surname}"
    else:
        # Use only first name and surname
        full_name = f"{first_name}_{surname}"

    # Exclude unique ID from the filename
    if image_type == "passport_image":
        new_filename = f"{full_name}_image1.{extension}"
    elif image_type == "ck_image":
        new_filename = f"{full_name}_image2.{extension}"
    else:
        # Handle other image types if needed
        new_filename = f"{full_name}.{extension}"

    return new_filename



def passport_upload_to(instance, filename):
    return generate_filename(instance, filename, "passport_image")

def ck_upload_to(instance, filename):
    return generate_filename(instance, filename, "ck_image")

class Client(models.Model):
    first_name = models.CharField(max_length=255, default="name")
    middle_name = models.CharField(max_length=255, default="middle name",null=True, blank=True)
    surname = models.CharField(max_length=255, default="surname")
    business_name = models.CharField(max_length=255, default="business name")
    passport_number = models.CharField(max_length=20, default="EN000000")
    business_number = models.CharField(max_length=12, default="000000000000")
    passport_image = models.ImageField(upload_to=passport_upload_to, null=True, blank=True)
    ck_image = models.ImageField(upload_to=ck_upload_to, null=True, blank=True)
    registration_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.surname}"




    
