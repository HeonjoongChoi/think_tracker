from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from apps.serializers import FileSerializer
from django.http import FileResponse




import os
from apps.utils import is_image
from apps import file_upload_path
from django.http.request import QueryDict
from pytilhan.utils import log_util
from apps.tasks import scan_code_async, apply_scan_async
from apps.models import CeleryScan


def file_download(request):

    file_path = request.GET.get('file_path', '')

    if file_path == '':
        return None

    response = FileResponse(open(file_path, 'rb'))

    return response


class URLFormViewCelery(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    # success_url = '/thanks/'
    def post(self, req, *args, **kwargs):
        print("test_ini")
        
         # get requested data      
        new_data = req.data.dict()
        
        # requested file object
        file_name = req.data['file_name']
        date = req.data['date']
        
        # create full path for saving file        
        new_file_full_name = file_upload_path(file_name.name)
        
        # new file path
        file_path = '/'.join(new_file_full_name.split('/')[0:-1])        
        
        # file extension
        file_ext = os.path.splitext(file_name.name)[1]
        
        # add new data to QueryDict(for mapping with DB)
        new_data['file_ext'] = file_ext
        new_data['is_img'] = is_image(file_ext)
        new_data['file_path'] = file_path
        new_data['file_origin_name'] = req.data['file_name'].name
        new_data['file_save_name'] = req.data['file_name']
        
        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)
      
                
        celery_scan = CeleryScan(json_results='', is_complete=False)
        celery_scan.save()
        id_no = celery_scan.id_key
            
        file_serializer = FileSerializer(data = new_query_dict)
        print("test1")
        if file_serializer.is_valid():
            print("test2")
            file_serializer.save()
            print("save complete")
            print( file_serializer.data)
                    
                
            
            # create the object so scan can be applied
            result = scan_code_async.delay(file_serializer.data['file_save_name'], date, id_no)
                    
            # return the response as HttpResponse
            url = 'loaclhost:8000/taejo_api_result/' + str(id_no)            
            return Response({"url" : url}, status=status.HTTP_200_OK)
        else:
            
            log_util.error(__name__ , file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
            
            


class ScanResults(APIView):
    
    def get(self, req, *args, **kwargs):
        
        celery_scan = CeleryScan.objects.get(id_key=kwargs['pk'])
        print("celery_scan is complete???? ",celery_scan.is_complete)
        result = {"result": "in progress"  }

        if celery_scan.is_complete == True:

            result = celery_scan.json_results

           

        return Response(result, status=status.HTTP_200_OK)