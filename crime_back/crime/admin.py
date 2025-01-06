from django.contrib import admin

# Register your models here.
from .models import (
    UserProfile, ActionLog, CrimeEvent, CrimeType, Resident, Block, Police, Weapon,
    CaseProgress, Clue, Certification, CrimeEventType, CrimeEventPerson, CrimeEventPolice, CrimeEventWeap
)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ActionLog)
admin.site.register(CrimeEvent)
admin.site.register(CrimeType)
admin.site.register(Resident)
admin.site.register(Block)
admin.site.register(Police)
admin.site.register(Weapon)
admin.site.register(CaseProgress)
admin.site.register(Clue)
admin.site.register(Certification)
admin.site.register(CrimeEventType)
admin.site.register(CrimeEventPerson)
admin.site.register(CrimeEventPolice)
admin.site.register(CrimeEventWeap)
