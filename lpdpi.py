import os
import tornado.ioloop
import tornado.web

from raspledstrip.ledstrip import *

try:
    led = LEDStrip(160, True)
    status = 'ok'
except:
    from mock import Mock
    led = Mock()
    status = 'error'

class Noop(object):
    def __call__(self, *args, **kwargs):
        pass

class StripHandler(tornado.web.RequestHandler):
    def post(self):
        func = self.get_argument('func')
        if func == 'single-color':
            try:
                r,g,b = [int(self.get_argument(x)) for x in ('red', 'green', 'blue')]
                if 0 <= r < 128 and 0 <= g < 128 and 0 <= b < 128:
                    led.fillRGB(r,g,b)
                    led.update()
            except:
                pass
        if func == 'turn-off':
            led.all_off()
        self.redirect('/', permanent=False)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', status=status)

settings = {
    'debug': True,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/strip', StripHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
