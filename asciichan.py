
import webapp2
import jinja2

from google.appengine.ext import db 

loader = jinja2.FileSystemLoader('')
jinja_env = jinja2.Environment(loader=loader, autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Art(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
	def render_front(self, error="", title="", art=""):
		arts = db.GqlQuery("select * from Art order by created DESC")
		self.render("front.html", error=error, title=title, art=art, arts=arts)

	def get(self):
		self.render('front.html')

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title=title, art=art)
			a.put()

			self.redirect("/")
		else:
			error = "we need both a title and artwork!"
			self.render_front(error, title=title, art=art)

app = webapp2.WSGIApplication([('/', MainPage),
	], debug=True)