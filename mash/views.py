# Create your views here.
#coding: utf-8
from django.http import HttpResponse
from django.utils import simplejson
from django.template import Context, loader
from mash.models import User
import json, urllib, urllib2, random, hashlib, time, re, redis

chose_db = redis.StrictRedis(host='localhost', port=6379, db=0)
profile_db = redis.StrictRedis(host='localhost', port=6379, db=1)   
API_VERSION='3.0'

def vktime():
    md5 = hashlib.md5()
    api_id='123456'
    secret='secret'
    md5.update('api_id=%s'%api_id)
    md5.update('format=JSON')
    md5.update('method=getServerTime')
    md5.update('v=2.0')
    md5.update(secret)
    url="http://api.vkontakte.ru/api.php?api_id=%s&format=JSON&method=getServerTime&v=2.0&sig=%s" %(api_id, md5.hexdigest()) 
    r = urllib2.urlopen(url).read()
    m = re.match('\{"response":([0-9]+)\}', r)
    if (m):
        return int(m.group(1))
    else:
        return int(time.time())

DELTA_UNIXTIME = vktime() - int(time.time())
def timestamp():
    return int(time.time())+DELTA_UNIXTIME

class VKReq():
    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret
        self.random = 0

    def _update_random(self):
        while(True):
            r = random.randint(0, 1000000)
            if (r != self.random):
                self.random = r
                break

    def _sig(self, params):
        m = hashlib.md5()
        list = params.items()
        list.sort()
        str = ["%s=%s" % (k, v) for k, v in list]
        m.update(''.join(str))
        m.update(self.api_secret)
        return m.hexdigest()

    def _params(self, method_params):
        self._update_random()
        p = {'api_id': self.api_id,
             'format': 'JSON',
             'timestamp': timestamp(),
             'random': self.random,
             'v': API_VERSION}
        p.update(method_params)
        p.update(sig=self._sig(p))
        return p

    def get(self, method_params):
        """return response (dict)"""
        p = self._params(method_params)
        data = urllib.urlencode(p)  
        return simplejson.loads(urllib2.urlopen(urllib2.Request('http://api.vkontakte.ru/api.php', data)).read())

def start(request):
    chose_db.flushdb()
    profile_db.flushdb()
    for y in range(0,99):
        chose_db.zadd('rank',y,0)
    return HttpResponse('redis ready')

def index(request):
    VK = VKReq('2674503', 'Plpau4O1Uu7hItMNWWau')
    friends_req = VK.get({'uid': 56799255, 'count': 500, 'fields': 'uid,first_name,last_name,photo,photo_big', 'method': 'friends.get'})
    User.objects.all()
    for user in friends_req['response']:
        profile_db.set(user['uid'],simplejson.dumps(user))
        muser = User(
                     uid = user['uid'], 
                     last_name = unicode(user['last_name']),
                     first_name = unicode(user['first_name']),
                     photo = user['photo'],
                     photo_big = user['photo_big']
                 )
        muser.save()
    
    template = loader.get_template('index.html')
    c = Context()
    return HttpResponse(template.render(c))

def chose(request):
    set = []
    for m in [0,2]:
        rand = profile_db.randomkey()
        chose = profile_db.get(rand)
        unload = simplejson.loads(chose)
        set.append(unload)
    User.objects.all()
    ans = User.objects.filter(id=227)
    return HttpResponse(ans)#simplejson.dumps(set))

def getchose(request,id):
    chose_db.zincrby('rank',id,1)
    return HttpResponse('ok')

def getres(request,sid,eid):
    answer = chose_db.zrevrange('rank',sid,eid)    
    winner = profile_db.get(answer[0])
    return HttpResponse(winner)