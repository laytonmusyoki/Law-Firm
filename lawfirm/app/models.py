from django.db import models

class Clients(models.Model):
    # Profile fields
    first_name = models.CharField(max_length=100)
    sir_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    county = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    status= models.CharField(max_length=100,choices=[('ongoing','ongoing'),('case closed','case closed')],default='ongoing',blank=True,null=True)

    # Pleading fields
    matter_number = models.CharField(max_length=100)
    matter_name = models.CharField(max_length=100)
    document_upload = models.FileField(upload_to='documents/')
    description = models.TextField()
    pleading_status = models.CharField(
        max_length=50,
        choices=[('plaintiff', 'Plaintiff'), ('defendant', 'Defendant')]
    )

    # Case Statement fields
    MATTER_TYPE_CHOICES = [
        ('criminal', 'Criminal'),
        ('civil', 'Civil'),
        ('other', 'Other Services'),
    ]

    CRIMINAL_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ]

    CIVIL_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ]

    OTHER_SERVICES_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ]

    statement = models.TextField()
    dispute = models.CharField(max_length=50, choices=MATTER_TYPE_CHOICES)
    criminal_sub_option = models.CharField(max_length=50, blank=True, null=True, choices=CRIMINAL_CHOICES)
    civil_sub_option = models.CharField(max_length=50, blank=True, null=True, choices=CIVIL_CHOICES)
    other_services_sub_option = models.CharField(max_length=50, blank=True, null=True, choices=OTHER_SERVICES_CHOICES)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.dispute == 'criminal' and not self.criminal_sub_option:
            raise ValidationError({'criminal_sub_option': 'This field is required for criminal disputes.'})
        elif self.dispute == 'civil' and not self.civil_sub_option:
            raise ValidationError({'civil_sub_option': 'This field is required for civil disputes.'})
        elif self.dispute == 'other' and not self.other_services_sub_option:
            raise ValidationError({'other_services_sub_option': 'This field is required for other services.'})

        super().clean()

    
    def __str__(self):
        return self.first_name + ' ' + self.sir_name

    
class courtAttendance(models.Model):
    date=models.CharField(max_length=100)
    matterNumber=models.CharField(max_length=100)
    matterName=models.CharField(max_length=100)
    parties=models.CharField(max_length=100)
    purpose=models.CharField(max_length=100)
    court_presiding=models.CharField(max_length=100)
    advocates=models.CharField(max_length=100)
    timeTaken=models.CharField(max_length=100)
    furtherAction=models.CharField(max_length=100)
    signedBy=models.CharField(max_length=100)

    def __str__(self):
        return self.matterNumber + ' ' + self.matterName