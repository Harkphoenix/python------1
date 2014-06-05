#coding=utf-8
class Handler:
	"""
	当从parser中利用handler对象调用方法的时候就会使用这个类里面的函数
	某种意义上说这是整个程序的处理器，由parser发出指令，然后再handler中调用
	相应的函数去执行
	"""

	def callback(self, prefix, name, *args):
		"""
		prefix是函数的前缀名，name为函数名，args为调用这个函数的参数，*args会接受一些冗余参数
		如果要调用的函数存在，那么就返回这个函数，如果没有，那么就自动返回None这也是getattr的作用
		"""
		method = getattr(self, prefix+name, None)
		if callable(method) : return method(*args)

	def start(self, name):
		self.callback('start_', name)
	def end(self, name):
		self.callback('end_', name)

	def sub(self, name):
		def substitution(match):
			"""
			这个函数会被应用在re.sub中的第二个函数参数来使用
			"""
			result = self.callback('sub_', name, match)
			if result is None: result = match.group(0)
			return result
		return substitution

class HTMLRenderer(Handler):


    def start_document(self):
        print "<html><head><title>hahaha</title></head><body>"

    def end_document(self):
        print "</body></html>"

    def start_paragraph(self):
        print "<p>"

    def end_paragraph(self):
        print "</p>"

    def start_heading(self):
        print "<h2>"

    def end_heading(self):
        print '</h2>'

    def start_list(self):
        print "<ul>"

    def end_list(self):
        print "</ul>"

    def start_listitem(self):
        print "<li>"

    def end_listitem(self):
        print "</li>"

    def start_title(self):
        print "<h1>"

    def end_title(self):
        print "</h1>"

    def sub_emphasis(self, match):
        return "<em>%s</em>" % match.group(1)

    def sub_url(self, match):
        return '<a href = "%s"> %s </a>' % (match.group(1), match.group(1))

    def sub_email(self, match):
        return '<a href = "mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def feed(self, data):
        print data
