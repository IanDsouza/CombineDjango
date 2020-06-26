from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from .models import *
from django.db.models import Count, Avg,F,Sum
from django.db.models.functions import Cast
import datetime


def all_users(request):
    data = []
    data_set = list(User.objects.all())

    for i in  data_set:
        data.append(i.get_json())

    return HttpResponse(json.dumps({ "data": data, "status": True}), content_type="application/json")

@csrf_protect
@csrf_exempt
def get_user_count(request):
    try:
        jsonObj = json.loads(request.body)
    except:
        return HttpResponse(json.dumps({"redirectConstant":'/', "validation": 'No data found', "status": False}), content_type="application/json")
    user_data = jsonObj.get('users')
    user_list = []
    for i in user_data:
        print ("i",i)
        user_list.append(i["id"])

    print("user list", user_list)        
    query_set =  Audio.objects.filter(user__id__in=user_list)
    new_list = query_set.values('user__name').annotate(dcount=Count('user'))

    return HttpResponse(json.dumps({ "data": list(new_list), "status": True}), content_type="application/json")



@csrf_protect
@csrf_exempt
def get_average_contrbution(request):
    try:
        jsonObj = json.loads(request.body)
    except:
        return HttpResponse(json.dumps({"redirectConstant":'/', "validation": 'No data found', "status": False}), content_type="application/json")

    user_data = jsonObj.get('users')
    user_list = []
    for i in user_data:
        print ("i",i)
        user_list.append(i["id"])

    final_list = []
    for i in user_list:
        query_set = Audio.objects.filter(user__id = i)
        data = get_averate(list(query_set))
        print("type", type(data))
        final_list.append(data)

    return HttpResponse(json.dumps({ "data": final_list, "status": True}), content_type="application/json")


def most_and_least_contribution(request):

    users = list(User.objects.all())
    user_list = []
    for i in users:
        print ("i",i)
        user_list.append(i.get_json()["id"])
    print ("all users", user_list)

    final_list = []
    for i in user_list:
        query_set = Audio.objects.filter(user__id = i)
        data = get_overall_contribution(list(query_set))
        final_list.append(data)

    total = sum(item["percentage_contribution"] for item in final_list)
    if total is not 100:
        data_format ={ "name": "Others", "diff": 0, "percentage_contribution":  round(float((100 - total))) }
        final_list.append(data_format)
    
    most_and_least = { "most" : max(final_list, key=lambda x:x['diff']) , "least": min(final_list, key=lambda x:x['diff'])}  
    data = {}
    data["contribution"] = final_list
    data["most_and_least"] = most_and_least

    

    return HttpResponse(json.dumps({ "data": data, "status": True}), content_type="application/json")


def get_overall_contribution(audios):
    data_format ={ "name": "", "diff": 0, "percentage_contribution":0}
    for i in audios:
        data = i.get_json()
        data_format["name"] = data["user"]
        data_format["diff"] = data_format["diff"] + (get_datetime(data["audio_end"]) - get_datetime(data["audio_start"])).seconds

    total_meeting_time = 900
    percentage_contribution =  round(float(((data_format["diff"]/ total_meeting_time) * 100)), 2) 
    data_format["percentage_contribution"] = percentage_contribution

    return data_format



def get_averate(audios):
    data_format ={ "name": "", "diff": 0, "count" : 0, "avg":0}
    count  = 0
    for i in audios:
        data = i.get_json()
        data_format["name"] = data["user"]
        data_format["diff"] = data_format["diff"] + (get_datetime(data["audio_end"]) - get_datetime(data["audio_start"])).seconds
        data_format["count"] = count
        count = count + 1

    if count == 1:
        data_format["count"] = 1
    data_format["avg"] = data_format["diff"]/ data_format["count"]
    print("final data format", data_format)

    return data_format


def get_datetime(epochof):
	if epochof:
		m_date = datetime.datetime.fromtimestamp(int(epochof))
		return m_date
	else:
		return None