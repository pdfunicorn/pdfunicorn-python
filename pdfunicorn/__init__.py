# -*- coding: utf-8 -*-
"""
pdfunicorn.py
a client for the PDFUnicorn API 

Authors:
    Jason Galea <jason@pdfunicorn.com>

"""
import requests
from requests.auth import HTTPBasicAuth

import StringIO

import json
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

DEBUG = True


class pdfUnicorn(object):
    """
    client = pdfUnicorn( api_key = 'my-api-key' )
    img_meta = client.images.create(file='path/to/image.jpg',path='path/used/in/document.jpg')
    pdf_doc = client.documents.create(file='path/to/doc/source.pdfu');
    
    """
    def __init__(self, api_key, base_url=None):
        self.ua = UserAgent(api_key, base_url=base_url)
        self.images = Images(self.ua)
        self.documents = Documents(self.ua)


class Images(object):
    
    def __init__(self, ua):
        self.ua = ua

    def create(self, image, src=None):
#         if isinstance(image, str):
#             return self.ua.post(
#                 'api/v1/images',
#                 files = {'file': (src, open(image, 'rb'))}
#             ).json
#         else:
        return self.ua.post(
            'v1/images',
            files = { 'image': (src, image) }
            #files = { 'image': image }
        ).json

    
class Documents(object):

    def __init__(self, ua):
        self.ua = ua

    def create(self, source, binary):
        resp = self.ua.post('v1/documents'+('.binary' if binary else ''), data=json.dumps({
            'source': source if '<doc' in source else open(source, 'rb').read()
        }))
        if resp.status_code == 200:
            if resp.headers['content-type'] == 'application/json':
                return resp.json
            else:
                return resp.content
        else:
            data = resp.json
            data['http_status'] = resp.status_code
            raise Exception(data)


class UserAgent(object):
    
    def __init__(self, api_key, base_url='pdfunicorn.com'):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()


    def get(self):
        pass
    

    def post(self, uri, params=None, files=None, data=None):
        if params:
            resp = self.session.post(
                self.base_url + '/' + uri,
                auth = HTTPBasicAuth(self.api_key,''),
                params = params,
            )
        elif data:
            resp = self.session.post(
                self.base_url + '/' + uri,
                auth = HTTPBasicAuth(self.api_key,''),
                data = data,
            )
        else:
            resp = self.session.post(
                self.base_url + '/' + uri,
                auth = HTTPBasicAuth(self.api_key,''),
                files = files
            )
        #resp.raise_for_status()
        return resp




###############################################################################
import unittest
import base64
import re

image_base64='/9j/4AAQSkZJRgABAQEAWgBYAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAyAC4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD36iiigAqvd3trYQGa7nSGMd2OM8ZwPU+wqWSRIonkkZURAWZmOAAOpNcfEbjxFqzSma6treJQsyBQhwfmEQJG5TggsQQfu47ENK4m7C3fjopBHPa6c5iePzkM24GVMZ+TYrDp13EY7jvUNnaW3jy/urrV4Ul0+0byIbBnB2SdWZ8H74+76D5gOmToy6VDdahamyjsTaWv7qSMp93kMQAODkHv0zVnRtPg0vXdThgSOOK4WKeNEQKFwCrAY9wG+r0NCTuUL3Vr97i8ZJ7q2gilMMbQrCV44JO/JY7s8DHTHWn6B4qiubW4jvJpJri2nMLNDbu5PyqcsEX5ep6gdOnWudstWk1GOeVtPNvNDPMfIuAJPJkkKoN3b78rYzjhTXT2ltb6bZxW1vGI4YxhVUfqfc9SapRuS5WHavrlhPZLCt4sBeRd3m/unUKd2drjOCVxyMcmjQFCaNA5LF5gZpC/3tzHJB+mcfQCgOVkypbH0Ixn8KnSVQMAMP8AgJpqNhOVzO1SZ9JuLm8dbg6fcKrTvbAs8LrgbsDJIKgA46Y98ia80258RtGssE+nwRAlZ2IWVyccAA5C9znHIXirN9C13ZSwo4V2AwWGQSDnB9jjB9ia1rC7F9p9vdqpQTRq+09VyOh+nSlIcCHWLN7/AEqe3iIExAeLd03qQy59sgZrCtb8TRZ2MGU7XRuGRh1Uj1FdXXFeP9Q0vwzbWviG8VoyJxbyvEMtIrI2FI74KqfUYPvRCVtGE43V0TanfPb6ZczRDDxxs6+5AyB+dOtL95Lq6jkPETqqgDttBz+ZI/D615lqXxN8M6tFDEDqDW7SbXVI9h3YypzuB4IB/I+ldr4lbTPB2h2HiG/a5SbckNwxkZ2YMjHZtJxw2D68GtHJIzUZNGvqOsrZCJY082WVtqJnGSeBz2G4qM9BurpNOtPsOm21qX3tDEqM2MbiByfxPNeI3nxQ8MX7wvGL1kcPayfuQDtdc8ZPqq/SvcLB5n062e4GJ2iQyD0bAz+tRO3Q0p36liuN+I9pbXnhmVLq3inRZEZVlQMAc4yM98E/nRRUItnnvhbQ9Ja/ty2l2RKzgrm3Tg4HTiuz8dWtvd+F5kuYIpkWRGCyoGAOcZ578miiqWxD3OO8JaHpD6hb79KsW2zgrm3Q4PHTivb4f9UKKKl7FLc//9k='


class PDFUTestBase(unittest.TestCase):
    
    def setUp(self):
        self.pdfu = pdfUnicorn(api_key='testers-api-key', base_url='http://localhost:3000')

            
class TestClient(PDFUTestBase):

    def test_create(self):
        """create an image and a document"""
        
        image = StringIO.StringIO(base64.b64decode(image_base64))
        
        #print image
        
        img = self.pdfu.images.create(image, 'path/to/test_image.jpg')

        self.assertTrue(img)
        self.assertEqual(img.get('src'), 'path/to/test_image.jpg')
        self.assertEqual(img.get('uri'), '/v1/images/' + img.get('id'))
        
        doc = self.pdfu.documents.create(
            source = '<doc size="b5"><page><row><cell>Hello World!</cell><cell><img src="path/to/test_image.jpg" /></cell></row></page></doc>',
            binary = True
        )
        self.assertTrue(re.match('%PDF', doc))
                        
        t = open("pdfu_test.pdf", "wb")
        t.write(doc)
        t.close()
                

if __name__ == "__main__":
    unittest.main()
    
    
###############################################################################
import base64

def dump_base64(image):
    f = open(image)
    data = f.read()
    f.close()

    string = base64.b64encode(data)
    print string
    
# if __name__ == "__main__":
#     dump_base64("unicorn.jpeg")

