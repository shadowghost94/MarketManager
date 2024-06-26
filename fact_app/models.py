from django.db import models
from django.contrib.auth.models import User
  
class Customer(models.Model):
    """
        Nom: définition du modèle pour un client
    """
    SEX_TYPES = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=12)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_date = models.DateField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

class Invoice(models.Model):
    """
        Nom: Définition du modèle Invoice
        Description:
    """
    INVOICE_TYPE = (
        ('R', 'RECU'),
        ('P', 'PROFORMA FACTURE'),
        ('F', 'FACTURE')
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    #models.SET_NULL = models.PROTECT dans le sens où la suppression de l'un
    #n'entraine pas le supression de l'autre
    
    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    invoice_date_time = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(max_digits=65, decimal_places=2)

    last_updated_date = models.DateTimeField(null=True, blank=True)

    paid = models.BooleanField(default=False)

    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)

    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f"{self.customer.name} {self.invoice_date_time}"
    
    @property
    def get_total(self):
        articles = self.article_set.all
        total = sum(article.get_total for article in articles)
    
class Article(models.Model):
    """
    Name:
    Description:
    Author:
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=65, decimal_places=2)
    total = models.DecimalField(max_digits=65, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = "Articles"

    @property
    def get_total(self):
        total = self.quantity * self.unit_price