from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import save_date
from .views import save_speed
from .views import GridOverview
from .views import dateview
from .views import save_totalPower
from .views import save_totalLoad
from .views import power_load_vs_time
from .views import save_diesel, save_wind, save_solar, gen_vs_time , save_batteryPower,save_batterySoc,Batt_vs_time 


urlpatterns = [ 
 path("", GridOverview, name="GridOverview"),

 path('save_date/', save_date, name='save_date'),
 path('save_speed/', save_speed, name='save_speed'),
 path('save_totalPower/', save_totalPower, name='save_totalPower'),
 path('save_totalLoad/', save_totalLoad, name='save_totalLoad'),
 path('save_diesel/', save_diesel, name='save_diesel'),
 path('save_wind/', save_wind, name='save_wind'),
 path('save_solar/', save_solar, name='save_solar'),
 path('save_batterySoc/', save_batterySoc, name='save_batterySoc'),
 path('save_batteryPower/', save_batteryPower, name='save_batteryPower'),
 path('powervsload/',power_load_vs_time, name ='powervsload' ),
 path('generation/', gen_vs_time , name ='generation' ),
 path('generation2/', Batt_vs_time , name ='generation2' ),

]

