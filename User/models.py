from django.db import models

# Create your models here.
class ImageEncryptionDecryption(models.Model):
    Encrypted_Image=models.CharField(max_length=100)
    Decrypted_Image=models.CharField(max_length=100)

class Encryption(models.Model):
    Encrypted_Image=models.TextField()

class Decryption(models.Model):
    Decrypted_Image=models.TextField()