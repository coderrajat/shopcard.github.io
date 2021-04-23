from django.db import models
class product(models.Model):
    f=[('Men_Fashion','Men_Fashion'),('Woman_Fashion','Woman_Fashion'),('Electronics','Electronics'),('Footwear','Footwear'),('Beauty','Beauty'),('Home','Home'),('Gadgets','Gadgets'),('Jewellery','Jewellery'),('Other','Other')]
    products_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=15,choices=f,default="")
    sub_category=models.CharField(max_length=50,default="")
    image=models.ImageField(upload_to="shopcard/image",default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()

    def __str__(self):
        return self.product_name

class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=50,default="")
    desc = models.CharField(max_length=1000,default="")

    def __str__(self):
        return self.name

class checkout(models.Model):
    prod_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=3000)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=300,default="")
    city = models.CharField(max_length=25,default="")
    state = models.CharField(max_length=30, default="")
    zip_code = models.CharField(max_length=10, default="")

class updateorder(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=3000)
    timestamp= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:8]+"..."
