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

import logging


class pdfUnicorn(object):
    """
    client = pdfUnicorn( api_key = 'my-api-key' )
    img_meta = client.images.create(file='path/to/image.jpg',path='path/used/in/document.jpg')
    pdf_doc = client.documents.create(file='path/to/doc/source.pdfu');
    
    """
    def __init__(self, api_key, base_url=None, verify=None, timeout=None):
        self.ua = UserAgent(api_key, base_url=base_url, verify=verify, timeout=timeout)
        self.images = Images(self.ua)
        self.documents = Documents(self.ua)


class Images(object):
    
    def __init__(self, ua):
        self.ua = ua

    def create(self, image, src=None):
        return self.ua.post(
            'v1/images',
            files = { 'image': (src, image) }
            #files = { 'image': image }
        ).json

    
class Documents(object):

    def __init__(self, ua):
        self.ua = ua

    def create(self, source, pdf):
        resp = self.ua.post('v1/documents'+('.pdf' if pdf else ''), data=json.dumps({
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
    
    def __init__(self, api_key, base_url='https://pdfunicorn.com', verify=True, timeout=30):
        self.base_url = base_url
        self.api_key = api_key
        self.requests = requests
        self.verify = verify
        

    def get(self):
        pass
    

    def post(self, uri, params=None, files=None, data=None):
        try:
            if params:
                resp = self.requests.post(
                    self.base_url + '/' + uri,
                    auth = HTTPBasicAuth(self.api_key,''),
                    params = params,
                    verify = self.verify
                )
            elif data:
                resp = self.requests.post(
                    self.base_url + '/' + uri,
                    auth = HTTPBasicAuth(self.api_key,''),
                    data = data,
                    verify = self.verify
                )
            else:
                resp = self.requests.post(
                    self.base_url + '/' + uri,
                    auth = HTTPBasicAuth(self.api_key,''),
                    files = files,
                    verify = self.verify
                )
        except ConnectionError:
            raise APIConnectionError
        except HTTPError:
            raise PDFUnicornError

        if resp.status_code != 200:
            self.raise_ex(resp)
            
        return resp

    def raise_ex(self, resp):
        if resp.status_code == 503:
            raise TemporaryError([res.message])
        elif resp.status_code == 422:
            raise InvalidRequestError(resp.json().get('errors') or res.message)
        elif resp.status_code == 401:
            #logging.debug(resp.text)
            print resp.content
            raise AuthenticationError(resp.json().get('error') or 'Authentication Error')
        elif resp.status_code == 404:
            raise NotFound(['Resource Not Found'])
        else:
            raise PDFUError(resp.json().get('errors') or res.message)



class PDFUError(Exception):
    
    def __init__(self, errors):
        self.errors = errors
        
    def __str__(self):
        return repr("\n".join(self.errors))
    
    
class InvalidRequestError(PDFUError):
    pass

class AuthenticationError(PDFUError):
    pass

class APIConnectionError(PDFUError):
    pass

class TemporaryError(PDFUError):
    pass

class PDFUnicornError(PDFUError):
    pass

class NotFound(PDFUError):
    pass






