#
# Copyright (c) 2017 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-server/
# The scancode-server software is licensed under the Apache License version 2.0.
# Data generated with scancode-server require an acknowledgment.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with scancode-server or any scancode-server
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with scancode-server and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  scancode-server should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  scancode-server is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-server/ for support and download.

from __future__ import absolute_import, unicode_literals
import os
from django.conf.global_settings import FILE_UPLOAD_MAX_MEMORY_SIZE
import datetime
import uuid

from .celery import app as celery_app
__all__ = ['celery_app']

# 각 media 파일에 대한 URL Prefix
MEDIA_URL = '/media/' # 항상 / 로 끝나도록 설정
# MEDIA_URL = 'http://static.myservice.com/media/' 다른 서버로 media 파일 복사시

MEDIA_ROOT = os.path.join('/usr/src/app/', 'media')

# 파일 업로드 사이즈 100M ( 100 * 1024 * 1024 )
#FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600

# 실제 파일을 저장할 경로 및 파일 명 생성
# 폴더는 일별로 생성됨
def file_upload_path(filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime('%Y/%m/%d')
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s"%(uuid.uuid4().hex, suffix, ext)
    return os.path.join(MEDIA_ROOT, filepath, filename)

# DB 필드에서 호출
def file_upload_path_for_db(intance, filename):
    return file_upload_path(filename)