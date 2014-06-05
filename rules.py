#coding=utf-8
class Rule:
	"""
	所有规则的父类，因为所有的规则类都有action方法，且调用形式几乎一样，所以
	在父类中设置一个action函数即可.condition函数用来判断是不是符合该规则，然后通过type和父类中的action函数，调用相应
	的处理函数
	"""

	def action(self, block, handler):
		handler.start(self.type)
		handler.feed(block)
		handler.end(self.type)
		return True


class HeadingRule(Rule):

	type = 'heading'
	def condition(self, block):
		return not'\n' in block and len(block) <= 70 and not block[-1] == ':'    #回返回是真是假

class TitleRule(HeadingRule):

	type = 'title'
	first = True

	def condition(self, block):
		if not self.first: return False
		self.firt = False
		return HeadingRule.condition(self, block)

class ListItemRule(Rule):

	 type = 'listitem'
	 def condition(self, block):
	 	return block[0] == '-'
	 def action(self, block, handler):
	 	handler.start(self.type)
	 	handler.feed(block[1:].strip())
	 	handler.end(self.type)
	 	return True

class ListRule(ListItemRule):

	type = 'list'
	inside = False
	def condition(self, block):
		return True
	def action(self, block, handler):
		if not self.inside and ListItemRule.condition(self,block):
			handler.start(self.type)
			self.inside = 1
		elif self.inside and not ListItemRule.condition(self, block):
			handler.end(self.type)
			self.inside = False
		return False

class ParagraphRule(Rule):
	type = 'paragraph'
	def condition(self, block):
		return True