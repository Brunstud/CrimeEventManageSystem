from django.db import models
from django.contrib.auth.models import User

# UserProfile 用户表
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Visitor', 'Visitor'),
        ('Related', 'Related Person'),
        ('Officer', 'Officer'),
        ('Cid', 'Criminal Investigator'),
        ('Admin', 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES)

# ActionLog 用户日志表
class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Action: {self.action} | User: {self.user.username} | Time: {self.timestamp}"

# CrimeEvent 犯罪事件表
class CrimeEvent(models.Model):
    crime_description = models.TextField()
    main_type = models.ForeignKey('CrimeType', on_delete=models.CASCADE, related_name='events')
    main_criminal = models.ForeignKey('Resident', on_delete=models.SET_NULL, null=True, related_name='crimes_committed')
    main_victim = models.ForeignKey('Resident', on_delete=models.SET_NULL, null=True, related_name='crimes_victimized')
    main_weapon = models.ForeignKey('Weapon', on_delete=models.SET_NULL, null=True, blank=True)
    time_reported = models.DateTimeField()
    time_occurred = models.DateTimeField()
    block = models.ForeignKey('Block', on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    current_status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

# CrimeType 犯罪类型表
class CrimeType(models.Model):
    type_code = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    type_description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

# Resident 居民信息表
class Resident(models.Model):
    person_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()
    occupation = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    block = models.ForeignKey('Block', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='residents/', blank=True, null=True)

# Block 区块信息表
class Block(models.Model):
    block_name = models.CharField(max_length=50, primary_key=True)
    domain_description = models.CharField(max_length=255)

# Police 警官信息表
class Police(models.Model):
    officer_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Resident, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

# Weapon 武器类型表
class Weapon(models.Model):
    weapon_code = models.AutoField(primary_key=True)
    weapon_description = models.CharField(max_length=255)

# CaseProgress 案件进展表
class CaseProgress(models.Model):
    progress_code = models.AutoField(primary_key=True)
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    time_progress = models.DateTimeField()
    status = models.CharField(max_length=50)
    notes = models.TextField()

# Clue 线索记录表
class Clue(models.Model):
    clue_code = models.AutoField(primary_key=True)
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    clue_type = models.CharField(max_length=50, default='General')
    clue_description = models.TextField()
    clue_image = models.ImageField(upload_to='clues/', blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    chosen_as_evidence = models.BooleanField(default=False)

# Certification 用户认证关系表
class Certification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_police = models.BooleanField(default=False)
    person = models.ForeignKey(Resident, on_delete=models.CASCADE)
    officer = models.ForeignKey(Police, on_delete=models.CASCADE, null=True, blank=True)

# CrimeEventType 事件类型关系表
class CrimeEventType(models.Model):
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    type_code = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

# CrimeEventPerson 事件相关人员关系表
class CrimeEventPerson(models.Model):
    RELATION_CHOICES = [
        ('Susp', 'Suspect'),
        ('Crim', 'Criminal'),
        ('Vict', 'Victim'),
        ('Eyew', 'Eyewitness'),
        ('Witn', 'Witness'),
    ]
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    person = models.ForeignKey(Resident, on_delete=models.CASCADE)
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES)

# CrimeEventPolice 事件负责警官关系表
class CrimeEventPolice(models.Model):
    LEVEL_CHOICES = [
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('supervisor', 'Supervisor'),
    ]
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    officer = models.ForeignKey(Police, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    in_date = models.DateField()
    out_date = models.DateField(null=True, blank=True)

# CrimeEventWeap 事件相关武器关系表
class CrimeEventWeap(models.Model):
    event = models.ForeignKey(CrimeEvent, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    weapon_detail = models.CharField(max_length=255)
