#coding=utf-8
import sys, re
from handlers import *
from util import *
from rules import *


class Parser:
    """
    整个程序的主类，里面主要是对文本进行相应的语法分析，然后分别用合适的规则和过滤器处理文本，最后输出
    """
    def __init__(self, handler):
        """
        初始化程序的处理对象handler以及规则和过滤器存储数组
        """
        self.handler = handler  
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        """
        利用filter创建一个过滤器，过滤器就是一个函数handler.sub(name)。
        filters列表每个元素都是一个filter函数，只不过name不同，handler调用的方法也就会不同
        """
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        """
        主要的处理程序，程序开始运行最先进入的就是这个函数，是整个程序的入口
        """
        self.handler.start('document')    #处理程序开始写入网页标记的头部
        for block in blocks(file):
            """
            每次读取的都是文本中的一个块
            """
            for each_filter in self.filters:
                block = each_filter(block, self.handler)
            for each_rule in self.rules:
                if each_rule.condition(block):
                    last = each_rule.action(block, self.handler)
                    if last : break;
        self.handler.end('document')

class BasicTextParser(Parser):
    """
    为规则和过滤器进行初始化的添加
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z])', 'mail')


handler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)
