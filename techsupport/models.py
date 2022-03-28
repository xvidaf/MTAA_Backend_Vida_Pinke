from django.db import models

class User(models.Model):
    email = models.CharField('Email of the user', max_length=100, null=False, unique=True)
    password = models.CharField('Password of the user', max_length=100, null=False)
    usertype = models.CharField('Type of the user', max_length=10, null=False)
    lastlogin = models.DateTimeField('Last login date', max_length=10, null=False)
    token = models.CharField('Last valid token', max_length=100, null=True)

    def __str__(self):
        return self.email

class Media(models.Model):
    name = models.CharField('Name of the media', max_length=100, null=False)
    path = models.FileField('Path to the media', upload_to='files/', max_length=255, null=False)
    isvideo = models.BooleanField(null=False)

class Devices(models.Model):
    name = models.CharField('Name of the device', max_length=100, null=False)
    image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Tickets(models.Model):
    name = models.CharField('Name of the ticket', max_length=100, null=False)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name = 'createdBy')
    assignedTo = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name = 'assignedTo')
    deviceType = models.ForeignKey(Devices, on_delete=models.CASCADE)
    issueType = models.CharField('Type of the issue', max_length=100, null=False)
    description = models.CharField('Description of the issue', max_length=10000, null=False)
    stage = models.IntegerField('Stage of the issue', null=False)
    complete = models.BooleanField(null=False)
    solutionText = models.CharField('Text of the solution', max_length=10000, null=True, blank=True)
    solutionVideo = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True, related_name ='solutionVideo')
    image = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True, related_name ='Image')

    def __str__(self):
        return self.name

class ChatMessages(models.Model):
    ticketid = models.ForeignKey(Tickets, on_delete=models.CASCADE, null=False)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'reciever')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name= 'sender')
    timestamp = models.DateTimeField( max_length=10, null=False)
    message = models.CharField(max_length=1000, null=False)
