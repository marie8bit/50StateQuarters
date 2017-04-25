from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Coin
from .forms import CoinCollectorForm, CoinDetailForm
from django.http import HttpResponse
from django.template import Context, loader

from django.utils import timezone
import json
import folium
# Create your views here.
def coin_collector(request):
    coins = Coin.objects.order_by('state')
    if not (coins):
        states_abbr = json.load(open('statecoin50/fixtures/us_states_abbr.json.txt'))
        f = open('statecoin50/fixtures/50sqReport.txt', 'rb').read()
        text = f.decode('utf-16')
        textn = text.replace('\n', '')
        state_dets = textn.split('\r')
        caseDetsLower = []
        for line in state_dets:
            lline = line.lower()
            caseDetsLower.append(lline)
        # stateabbr_list = list(states_abbr.values())
        # state_list = list(states_abbr.keys())
        for key in states_abbr:
            # dex = stateabbr_list.index(item)
            state = key
            abr= states_abbr[key]
            owned = False
            url= 'https://www.usmint.gov/images/mint_programs/50sq_program/states/'+abr+'_Designs.gif'
            caseState = state.lower()
            dex = caseDetsLower.index(caseState)
            dates = state_dets[dex+1]
            details = state_dets[dex+2]
            coin = Coin(state = state, stAbbr = abr, owned= owned, stURL=url, dates = dates, details = details)
            coin.save()
            map_us = folium.Map(location=[40, -102], zoom_start=3)
            #map_us.geo_json(geo_path = statesOwned, data = statesOwned, columns=['State','Owned'], fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2)
            map_us.save('statecoin50/templates/statecoin50/map_coins.html')
        return render(request, 'statecoin50/coin_collector.html', {'coins':coins})
    else:
        statesOwned = Coin.objects.order_by('stAbbr')


        all_state_map={}
        for coin in statesOwned:
            if coin.owned:
                number = 10
            else:
                number = 1
            all_state_map[coin.stAbbr]=number

        map_us = folium.Map(location=[50, -118], zoom_start=3)
        us_states_file='statecoin50/fixtures/us_states.json'
        #state_list=list(us_states_file)
        #us_states_file=us_states_file.sort()
        #all_state_map['stAbbr']=us_states_file['state']
        map_us.choropleth(geo_path = us_states_file,
                        data = all_state_map,
                        columns=['state','number'],
                        key_on='id',
                        fill_color = 'YlGn', fill_opacity=0.7, line_opacity =0.2,
                        threshold_scale = [1,3,5,7,10],
                        legend_name = "Coins Collected: Yellow= Not Collected - Green = Collected")
        map_us.save('statecoin50/templates/statecoin50/map_coins.html')
        return render(request, 'statecoin50/coin_collector.html', {'coins':coins})
        #
        # state = 'Delaware'
        # abr = 'DE'
        # owned = False
        # url ='https://www.usmint.gov/images/mint_programs/50sq_program/states/DE_Designs.gif'
        # coin = Coin(state, abr, owned, url)
        # coins.append(coin)

def coindetail(request, coin_pk):
    coin = get_object_or_404(Coin, pk=coin_pk)
    form = CoinDetailForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            coin2=form.save(commit = False)
            coin.owned=True
            coin.dateOwned=(timezone.now())
            coin.save()

            return render(request, 'statecoin50/coindetail.html', {'coin':coin}, {'form':form})
        else:
            print('form is not valid')
    else:
        form = CoinDetailForm(instance = coin)
        return render(request, 'statecoin50/coindetail.html', {'coin':coin}, {'form':form})

#source reference http://stackoverflow.com/questions/14400035/how-to-return-a-static-html-file-as-a-response-in-django
#http://stackoverflow.com/questions/17168256/template-does-not-exist
def map_coins(request):
    # template = loader.get_template("statecoin50/fixtures/map_coins.html")
    # return HttpResponse(template.render)
    #return render_to_response('statecoin50/fixtures/map_coins.html')
    return render(request, 'statecoin50/fixtures/map_coins.html')
