from __future__ import absolute_import, unicode_literals
from apps.models import CeleryScan

from celery import Task
from apps.celery import app
from apps.model.tracker import ObjectTracker
from rest_framework.response import Response
from rest_framework import status

class ScanCode(Task):
    ignore_result = True
    #name = 'scancode'
    def __init__(self, *args, **kwargs):
        # scan_code_async 메소드에서 self 사용했으므로 초기화 할 필요없음 
        self.id_no = kwargs.get('id_no', None)
        
        

    
    
            
        

@app.task
def scan_code_async(file_save_name, date, id_no):    
 
    print("file_save_name = ", file_save_name)
    
    model = ObjectTracker()
    results = model.track(file_save_name, date)
    r = Response(results, status=status.HTTP_201_CREATED)
    
    
    
    print("r.status_code = ", r.status_code)
    if r.status_code == 201:
        print("results = ", results)
        
        return apply_scan_async.delay(results, id_no)
    else:
        return 'Some error has occured'
@app.task
def apply_scan_async(results, id_key):
    json_result = results
    #("scan_result = ", scan_result)
    #("scan_result_type = ", type(scan_result))
    #json_data = json.loads(json_result)
    #json_data = json.dumps(json_result)
    celery_scan = CeleryScan.objects.get(id_key=id_key)
    celery_scan.json_results = json_result
    celery_scan.is_complete = True
    celery_scan.save()