from django.shortcuts import render
from django.http import HttpResponse
from pulp import *
import json
from GridOverview.models import totalLoad, totalPower, totalSolar, totalWind, batteryPower, totalDiesel
from GridOverview.serializers import TotalPowerSerializer, TotalLoadSerializer, DieselSerializer, WindSerializer, SolarSerializer, batteryPowerSerializer 
def optimize(request):
    if request.method == 'POST':
        # Get the daily power demand input
        detailed_summary = " "
        daily_power_demand = float(request.POST.get('daily_power_demand'))

        # Retrieve the data from the models
       
        total_solar1 = totalSolar.objects.latest('id')
        total_wind1 = totalWind.objects.latest('id')
        total_diesel1 = totalDiesel.objects.latest('id')
        battery_power1 = batteryPower.objects.latest('id')
        total_load1 = totalLoad.objects.latest('id')
        total_power1 = totalPower.objects.latest('id')

        #convert this json data to lists
        total_solar = json.loads(total_solar1.power) if not isinstance(total_solar1.power, list) else total_solar1.power
        total_wind = json.loads(total_wind1.power) if not isinstance(total_wind1.power, list) else total_wind1.power
        total_diesel = json.loads(total_diesel1.power) if not isinstance(total_diesel1.power, list) else total_diesel1.power
        battery_power = json.loads(battery_power1.power) if not isinstance(battery_power1.power, list) else battery_power1.power
        total_load = json.loads(total_load1.load) if not isinstance(total_load1.load, list) else total_load1.load
        total_power = json.loads(total_power1.power) if not isinstance(total_power1.power, list) else total_power1.power

        #Add each our generation to the report
        detailed_summary += "Power Generation Over 24 hours\n "
        for x in range(24):
            detailed_summary += f" Hour {x}: PV = {total_solar[x]} ,   WF = {total_wind[x]}  ,   DG = {total_diesel[x]}  ,   BAT = {battery_power[x]}  ,   LOAD= {total_load[x]}\n\n"
        # Define the optimization problem
        prob = LpProblem("Power Generation Optimization", LpMinimize)

        # Define the decision variables
        PV = LpVariable("PV", 0, 0.5, LpContinuous)
        WF = LpVariable("WF", 0, 6.9, LpContinuous)
        DG = LpVariable("DG", 0, 15, LpContinuous)
        BAT = LpVariable("BAT", 0, None, LpContinuous)

        # Define the objective function
        prob += 64*PV + 297*WF + 615.7*DG + 24.3*BAT, "Total Cost"

        # Define the constraints
        prob += PV + WF + DG + BAT >= daily_power_demand, "Power Demand"
        prob += PV <= 0.2*(PV + WF + DG + BAT), "PV Capacity"
        prob += WF <= 0.4*(PV + WF + DG + BAT), "Wind Capacity"
        prob += DG <= 0.6*(PV + WF + DG + BAT), "Diesel Capacity"
        prob += BAT <= 0.1*daily_power_demand, "Battery Capacity"

        # Initialize variables for cost analysis
        total_cost_no_opt = 0
        total_cost_opt = 0
        total_diesel_no_opt = 0
        total_diesel_opt = 0
        total_pv =0;
        total_w = 0;
        total_d = 0;
        total_b=0;
        total_c = 0;
        # Add the data from the models as constraints
        for i in range (24):
            prob += PV*total_solar[i] + WF*total_wind[i] + DG*total_diesel[i] + BAT*battery_power[i] >= total_load[i], "Hour " + str(int(i)+1)
        # Solve the optimization problem
        prob.solve()

        # Retrieve the optimal values and objective function value for the current hour
        optimal_pv = PV.varValue
        optimal_wind = WF.varValue
        optimal_dg = DG.varValue
        optimal_bat = BAT.varValue
        optimal_cost = value(prob.objective)

        #total optimal power generations 
        total_pv +=optimal_pv
        total_w +=optimal_wind
        total_d +=optimal_dg
        total_b +=optimal_bat
        total_c =optimal_cost
        total_g = total_pv + total_w + total_d + total_b

        # Add the optimal cost for the current hour to the total cost variables
        total_cost_opt += optimal_cost

        # Calculate the cost of using diesel without optimization for the current hour
        cost_no_opt = 1.5*total_power[i]

        # Add the cost without optimization for the current hour to the total cost variables
        total_cost_no_opt += cost_no_opt

        # Calculate the diesel consumption without optimization for the current hour
        diesel_no_opt = total_power[i] / 5

        # Add the diesel consumption without optimization for the current hour to the total diesel variables
        total_diesel_no_opt += diesel_no_opt

        # Calculate the diesel consumption with optimization for the current hour
        diesel_opt = optimal_dg / 5

        # Add the diesel consumption with optimization for the current hour to the total diesel variables
        total_diesel_opt += diesel_opt

        # Update the detailed summary for the current hour
       
        

        # Calculate the max and min cost after optimization
        max_cost_opt = max(total_cost_opt, total_cost_no_opt)
        #min_cost_opt = min(total_cost_opt, total_cost_no_opt)

        # Calculate the percentage of diesel reduced after optimization
        percentage_diesel_reduced = ((total_diesel_no_opt - total_diesel_opt) / total_diesel_no_opt) * 100
        # Cost before optimization

        
        cost_before_opt = 651.4*total_g

        # Update the detailed summary with the cost analysis results
        detailed_summary += f"\nMax Cost after Optimization = {round(max_cost_opt,2)}, $CAD/MWH\n"
        detailed_summary += f"\nMax Cost before Optimization = {round(cost_before_opt,2)}, $CAD/MWH\n\n"
        detailed_summary += f"Percentage of Diesel Reduced = {round(percentage_diesel_reduced,2)}%\n\n"

        # Render the results template with the optimal values and detailed summary
        return render(request, 'optimizer.html', {
            'optimal_pv': total_pv,
            'optimal_wind': total_w,
            'optimal_diesel': total_d,
            'optimal_battery': total_b,
            'optimal_cost': round(total_c,2),
            'total_gen': total_g,
            'detailed_summary': detailed_summary
        })

    else:
        # Render the optimizer template
        return render(request, 'optimizer.html')

