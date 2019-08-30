import json
import sys
'''
nb_video=sys.argv[1]

with open('testVideos/test'+nb_vedio+'/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata = json.load(json_data)
avgx=(jsondata['dX']['lak'][1]+jsondata['dX']['rak'][1]+jsondata['dX']['rkn'][1]+jsondata['dX']['lkn'][1]+jsondata['dX']['ras'][1]+jsondata['dX']['las'][1])/6
avgy=(jsondata['dY']['lak'][1]+jsondata['dY']['rak'][1]+jsondata['dY']['rkn'][1]+jsondata['dY']['lkn'][1]+jsondata['dY']['ras'][1]+jsondata['dY']['las'][1])/6
avgz=(jsondata['dZ']['lak'][1]+jsondata['dZ']['rak'][1]+jsondata['dZ']['rkn'][1]+jsondata['dZ']['lkn'][1]+jsondata['dZ']['ras'][1]+jsondata['dZ']['las'][1])/6
print(str(round(avgx,2))+'/'+str(round(avgy,2))+'/'+str(round(avgz,2)))
'''

with open('testVedios/test1/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata1 = json.load(json_data)
with open('testVedios/test2/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata2 = json.load(json_data)
with open('testVedios/test3/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata3 = json.load(json_data)
with open('testVedios/test16/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata4 = json.load(json_data)
with open('testVedios/test18/space_recalage.json') as json_data:
        #with open('testVedios/test'+nb_video+'/time_recalage.json') as json_data:
        jsondata5 = json.load(json_data)
avgxlak=(jsondata1['dX']['lak'][1]+jsondata2['dX']['lak'][1]+jsondata3['dX']['lak'][1]+jsondata4['dX']['lak'][1]+jsondata5['dX']['lak'][1])/5
avgxrak=(jsondata1['dX']['rak'][1]+jsondata2['dX']['rak'][1]+jsondata3['dX']['rak'][1]+jsondata4['dX']['rak'][1]+jsondata5['dX']['rak'][1])/5
avgxlkn=(jsondata1['dX']['lkn'][1]+jsondata2['dX']['lkn'][1]+jsondata3['dX']['lkn'][1]+jsondata4['dX']['lkn'][1]+jsondata5['dX']['lkn'][1])/5
avgxrkn=(jsondata1['dX']['rkn'][1]+jsondata2['dX']['rkn'][1]+jsondata3['dX']['rkn'][1]+jsondata4['dX']['rkn'][1]+jsondata5['dX']['rkn'][1])/5
avgxlas=(jsondata1['dX']['las'][1]+jsondata2['dX']['las'][1]+jsondata3['dX']['las'][1]+jsondata4['dX']['las'][1]+jsondata5['dX']['las'][1])/5
avgxras=(jsondata1['dX']['ras'][1]+jsondata2['dX']['ras'][1]+jsondata3['dX']['ras'][1]+jsondata4['dX']['ras'][1]+jsondata5['dX']['ras'][1])/5

avgylak=(jsondata1['dY']['lak'][1]+jsondata2['dY']['lak'][1]+jsondata3['dY']['lak'][1]+jsondata4['dY']['lak'][1]+jsondata5['dY']['lak'][1])/5
avgyrak=(jsondata1['dY']['rak'][1]+jsondata2['dY']['rak'][1]+jsondata3['dY']['rak'][1]+jsondata4['dY']['rak'][1]+jsondata5['dY']['rak'][1])/5
avgylkn=(jsondata1['dY']['lkn'][1]+jsondata2['dY']['lkn'][1]+jsondata3['dY']['lkn'][1]+jsondata4['dY']['lkn'][1]+jsondata5['dY']['lkn'][1])/5
avgyrkn=(jsondata1['dY']['rkn'][1]+jsondata2['dY']['rkn'][1]+jsondata3['dY']['rkn'][1]+jsondata4['dY']['rkn'][1]+jsondata5['dY']['rkn'][1])/5
avgylas=(jsondata1['dY']['las'][1]+jsondata2['dY']['las'][1]+jsondata3['dY']['las'][1]+jsondata4['dY']['las'][1]+jsondata5['dY']['las'][1])/5
avgyras=(jsondata1['dY']['ras'][1]+jsondata2['dY']['ras'][1]+jsondata3['dY']['ras'][1]+jsondata4['dY']['ras'][1]+jsondata5['dY']['ras'][1])/5

avgzlak=(jsondata1['dZ']['lak'][1]+jsondata2['dZ']['lak'][1]+jsondata3['dZ']['lak'][1]+jsondata4['dZ']['lak'][1]+jsondata5['dZ']['lak'][1])/5
avgzrak=(jsondata1['dZ']['rak'][1]+jsondata2['dZ']['rak'][1]+jsondata3['dZ']['rak'][1]+jsondata4['dZ']['rak'][1]+jsondata5['dZ']['rak'][1])/5
avgzlkn=(jsondata1['dZ']['lkn'][1]+jsondata2['dZ']['lkn'][1]+jsondata3['dZ']['lkn'][1]+jsondata4['dZ']['lkn'][1]+jsondata5['dZ']['lkn'][1])/5
avgzrkn=(jsondata1['dZ']['rkn'][1]+jsondata2['dZ']['rkn'][1]+jsondata3['dZ']['rkn'][1]+jsondata4['dZ']['rkn'][1]+jsondata5['dZ']['rkn'][1])/5
avgzlas=(jsondata1['dZ']['las'][1]+jsondata2['dZ']['las'][1]+jsondata3['dZ']['las'][1]+jsondata4['dZ']['las'][1]+jsondata5['dZ']['las'][1])/5
avgzras=(jsondata1['dZ']['ras'][1]+jsondata2['dZ']['ras'][1]+jsondata3['dZ']['ras'][1]+jsondata4['dZ']['ras'][1]+jsondata5['dZ']['ras'][1])/5

print(str(round(avgxlak,2))+'/'+str(round(avgylak,2))+'/'+str(round(avgzlak,2)))
print(str(round(avgxrak,2))+'/'+str(round(avgyrak,2))+'/'+str(round(avgzrak,2)))
print(str(round(avgxlkn,2))+'/'+str(round(avgylkn,2))+'/'+str(round(avgzlkn,2)))
print(str(round(avgxrkn,2))+'/'+str(round(avgyrkn,2))+'/'+str(round(avgzrkn,2)))
print(str(round(avgxlas,2))+'/'+str(round(avgylas,2))+'/'+str(round(avgzlas,2)))
print(str(round(avgxras,2))+'/'+str(round(avgyras,2))+'/'+str(round(avgzras,2)))
