from django.contrib import admin
from .models import DateModel
from .models import WindSpeed
from .models import totalPower
from .models import totalLoad
from .models import totalDiesel, totalWind, totalSolar, batterySOC, batteryPower
# Register your models here.


admin.site.register(DateModel)
admin.site.register(WindSpeed)
admin.site.register(totalPower)
admin.site.register(totalLoad)
admin.site.register(totalDiesel)
admin.site.register(totalWind)
admin.site.register(totalSolar)
admin.site.register(batterySOC)
admin.site.register(batteryPower)