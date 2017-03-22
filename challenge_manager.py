import os.path

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import mongoengine

from models import Challenge, ChallengePoint

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [ 
            (r'/', IndexHandler),
            (r'/challenges/$', ChallengeListHandler),
            (r'/challenges/(\w+)$', ChallengeDetailHandler),
            (r'/edit/(\w+)$', EditHandler),
            (r'/add', EditHandler),
            (r'/add_point/(\w+)$', EditPointHandler),
            (r'/edit_point/(\w+)x(\d+)$', EditPointHandler),#contains url and key parameter
            ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),'templates'),
            static_path = os.path.join(os.path.dirname(__file__),'static'),
            debug = True
            )
        mongoengine.connect('challenger') #connection to DB named 'challenger via mongoengine driver
        tornado.web.Application.__init__(self,handlers,**settings)

        
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('base.html')
        
class ChallengeListHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('challenge_list.html', challenges=Challenge.objects)


class ChallengeDetailHandler(tornado.web.RequestHandler):
    def get(self, url):
        self.render('challenge_detail.html', challenge=Challenge.objects.get(url=url))


class EditHandler(tornado.web.RequestHandler):
    '''
    Handles both adding and editing of Challenge model.
    You can create new Challenge instance via form, but you need to create at least one ChallengePoint to send the form.
    '''
    def get(self, url=None):

        '''
        If in the url you have url keyword, then it is the argument by get method and it will be only edited
        '''

        if url:
            self.render('edit_challenge.html', challenge=Challenge.objects.get(url=url))
        else:
            self.render('add.html')
         
    def post(self, url=None):

        '''
        If url, then model will be only edited.
        '''

        challenge = dict()
        challenge_fields = ['header', 'url', 'date_start', 'date_end']
        if url:
            challenge = Challenge.objects.get(url=url) #gets challenge object parameters to edit them
        for field in challenge_fields:
            challenge[field] = self.get_argument(field, None)
        if url:
            challenge.save()
        else:
            point = dict()
            point_fields=['title', 'key', 'done', 'required_time']
            for field in point_fields:
                point[field] = self.get_argument(field, None)
            challenge['points'] = [ChallengePoint(**point)] #you have to create at least one point entry to send the form
            Challenge(**challenge).save()#you call new Challenge instance giving it arguments taken from dictionary and saves it
        self.redirect('/challenges/')


class EditPointHandler(tornado.web.RequestHandler):

    '''
    Implements editting and adding of challenge points.
    If key is fetched by url, then point will be just edited
    '''

    def get(self, url, key = None):
        if key:
            self.render('edit_challenge_point.html',
                        challenge_point = Challenge.objects.get(url=url).points.get(key=key))
        else:
            self.render('add_challenge_point.html')
            
    def post(self, url, key = None):
        challenge_point = dict()
        challenge_point_fields = ['title','key','done',
                                  'required_time']
        if key:
            challenge = Challenge.objects.get(url=url)
            challenge_point = challenge.points.get(key=key)
        for field in challenge_point_fields:
            challenge_point[field] = self.get_argument(field, None)
        if key:
            challenge.points.save()
        else:
            c = Challenge.objects.get(url=url).points.create(**challenge_point)
            c.save()

        
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
