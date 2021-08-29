from PIL import Image,ImageFont,ImageDraw
from constants import *
import resize
#const:
#c_color_* for const colors
import mylocale
def solveCallable(i,**kwargs):
	while(callable(i)):
		i=i(**kwargs)
	return i
def _render_content(i,**kwargs):
	solveCallable(i,**kwargs)
	if(isinstance(i,Image.Image)):
		return i.convert("RGBA")
	elif(isinstance(i,widget)):
		return i.render(**kwargs)
	else:
		raise Exception("Unsupported widget content")
class widget:
	def get_rendered_contents(self,**kwargs):
		ret=list()
		for i in self.contents:
			ret.append(_render_content(i,**kwargs))
		return ret
	pass
class column(widget):
	pass
class row(widget):
	#layouts a row of widgets
	#if row widget has specified height attribute, it will force its children column layout evenly by setting their height attribute.
	#if row widget has specified width attribute, it will layout children evenly. But won't inherit the attribute to children.
	def __init__(self,contents,bg=None,borderWidth=None,borderColor=None, \
	stretchHeight=None,expandHeight=None,cropHeight=None,alignY=None,height=None,width=None,stretchWH=None):
		self.contents=contents
		self.stretchHeight=stretchHeight
		self.expandHeight=expandHeight
		self.cropHeight=cropHeight
		self.bg=bg
		self.borderColor=borderColor
		self.borderWidth=borderWidth
		self.alignY=alignY
		self.height=height
		self.width=width
		self.stretchWH=stretchWH
	def get_rendered_contents(self,**kwargs):
		if(self.height):
			for i in self.contents:
				if(isinstance(i,column)):
					if(i.height is None):
						i.height=self.height
		return super().get_rendered_contents(**kwargs)
	def render(self,**kwargs):
		#**kwargs are inherited attributes like bg color from parznt downwards to children when render
		print(kwargs)
		bg=self.bg or kwargs.get('bg') or c_color_TRANSPARENT
		borderWidth=self.borderWidth or kwargs.get('borderWidth') or 0
		borderColor=self.borderColor or kwargs.get('borderColor') or bg
		alignY=self.alignY or kwargs.get('alignY') or 0.5
		
		kwargs['bg']=bg						#inherit settings
		kwargs['borderWidth']=borderWidth
		kwargs['borderColor']=borderColor
		kwargs['alignY']=alignY
		
		r_contents=self.get_rendered_contents(**kwargs)
		if(self.stretchWH):
			for idx,i in enumerate(r_contents):
				i=i.resize(self.stretchWH,Image.LANCZOS)
				r_contents[idx]=i
		if(self.stretchHeight):
			for idx,i in enumerate(r_contents):
				i=resize.stretchHeight(i,self.stretchHeight)
				r_contents[idx]=i
		elif(self.expandHeight):
			for idx,i in enumerate(r_contents):
				i=resize.expandHeight(i,self.expandHeight)
				r_contents[idx]=i
		mxHeight=0
		sWidth=0
		for i in r_contents:
			w,h=i.size
			mxHeight=max(h,mxHeight)
			sWidth+=w
		if(self.width):
			width=self.width
			borderWidthX=(width-sWidth)/(1+len(r_contents))
		else:
			borderWidthX=borderWidth
			width=sWidth+borderWidthX*(1+len(r_contents))
		height=mxHeight+borderWidth*2
		
		ret=Image.new("RGBA",(width,height),bg.astuple())
		left=0
		for idx,i in enumerate(r_contents):
			w,h=i.size
			left+=borderWidthX
			top=int(borderWidth+(mxHeight-h)*alignY)
			ret.paste(i,box=(int(left),top),mask=i)
			left+=w
		return ret
class column(widget):
	def __init__(self,contents,bg=None,borderWidth=None,borderColor=None, \
	stretchWidth=None,expandWidth=None,cropWidth=None,alignX=None,height=None,width=None,stretchWH=None):
		self.contents=contents
		self.stretchWidth=stretchWidth
		self.stretchWH=stretchWH
		self.expandWidth=expandWidth
		self.cropWidth=cropWidth
		self.bg=bg
		self.borderColor=borderColor
		self.borderWidth=borderWidth
		self.alignX=alignX
		self.height=height
		self.width=width
	def get_rendered_contents(self,**kwargs):
		if(self.width):
			for i in self.contents:
				if(isinstance(i,row)):
					if(i.width is None):
						i.width=self.width
		return super().get_rendered_contents(**kwargs)
	def render(self,**kwargs):
		#**kwargs are inherited attributes like bg color from parent downwards to children when render
		bg=self.bg or kwargs.get('bg') or c_color_TRANSPARENT
		borderWidth=self.borderWidth or kwargs.get('borderWidth') or 0
		borderColor=self.borderColor or kwargs.get('borderColor') or bg
		alignX=self.alignX or kwargs.get('alignX') or 0.5
		
		kwargs['bg']=bg						#inherit settings
		kwargs['borderWidth']=borderWidth
		kwargs['borderColor']=borderColor
		kwargs['alignX']=alignX
		
		r_contents=self.get_rendered_contents(**kwargs)
		if(self.stretchWH):
			for idx,i in enumerate(r_contents):
				i=i.resize(self.stretchWH,Image.LANCZOS)
				r_contents[idx]=i
		if(self.stretchWidth):
			for idx,i in enumerate(r_contents):
				i=resize.stretchWidth(i,self.stretchWidth)
				r_contents[idx]=i
		elif(self.expandWidth):
			for idx,i in enumerate(r_contents):
				i=resize.expandWidth(i,self.expandWidth)
				r_contents[idx]=i
		mxWidth=0
		sHeight=0
		for i in r_contents:
			w,h=i.size
			mxWidth=max(mxWidth,w)
			sHeight+=h
		if(self.height):
			height=self.height
			borderWidthY=(height-sHeight)/(1+len(r_contents))
		else:
			borderWidthY=borderWidth
			height=sHeight+borderWidthY*(1+len(r_contents))
		width=mxWidth+2*borderWidth
		
		ret=Image.new("RGBA",(width,height),bg.astuple())
		top=0
		for idx,i in enumerate(r_contents):
			w,h=i.size
			top+=borderWidthY
			left=int(borderWidth+(mxWidth-w)*alignX)
			ret.paste(i,box=(int(left),int(top)),mask=i)
			top+=h
		return ret
class sizer(widget):
	def __init__(self,content,stretchWH=None,stretchWidth=None,stretchHeight=None,expandHeight=None,expandWidth=None,cropWH=None):
		self.content=content
		self.stretchWidth=stretchWidth
		self.stretchHeight=stretchHeight
		self.expandHeight=expandHeight
		self.expandWidth=expandWidth
		self.stretchWH=stretchWH
		self.cropWH=cropWH
	def render(self,**kwargs):
		ret=_render_content(self.content,**kwargs)
		if(self.cropWH):
			ret=resize.cropWH(ret,cropWH)
			return ret
		if(self.stretchWH):
			ret=ret.resize(self.stretchWH,Image.LANCZOS)
			return ret
		if(self.stretchWidth):
			ret=resize.stretchWidth(ret,self.stretchWidth)
			return ret
		if(self.stretchHeight):
			ret=resize.stretchHeight(ret,self.stretchHeight)
			return ret
class setfont(widget):
	#used to pass font attribute down to children widgets
	def __init__(self,content,font=None,fontSize=None):
		self.font=font
		self.fontSize=fontSize
		self.content=content
		self.lang=lang
	def render(self,**kwargs):
		kwargs['font']=self.font or kwargsget('font')
		kwargs['fontSize']=self.fontSize or kwargs.get('fontSize')
		kwargs['lang']=self.lang or kwargs.get('lang')
		return self.content.render(**kwargs)
class setkwargs(widget):
	def __init__(self,content,**kwargs):
		self.content=content
		self.kwargs=kwargs
	def render(self,**kwargs):
		kwargs.update(self.kwargs)
		return _render_content(self.content,**kwargs)
class _lineFeed:
	pass
class RTF(widget):
	def __init__(self,contents,width,font=None,fontSize=None,bg=None,lang=None,fill=None,alignY=None):
		self.width=width
		self.alignY=alignY
		self.font=font
		self.fontSize=fontSize
		self.bg=bg
		self.fill=fill
		self.contents=contents
	def render(self,**kwargs):
		font=self.font or kwargs.get('font') or mylocale.get_default_font()
		fontSize=self.fontSize or kwargs.get('fontSize') or 12
		bg=self.bg or kwargs.get('bg') or c_color_TRANSPARENT
		fill=self.fill or kwargs.get('fill') or c_color_BLACK
		width=self.width or kwargs.get('width')
		
		_contents=list()
		for i in self.contents:
			try:
				content=_render_content(i,**kwargs)
			except Exception as e:
				if(isinstance(i,str)):
					content=solveCallable(i,**kwargs)	#is string
				else:
					raise e
			if(isinstance(content,str)):
				for j in content:
					if(j=='\n'):
						_contents.append(_lineFeed())
					else:
						_contents.append(j)
		rows=list()
		_row=list()
		def render_text(text):
			if(not text):
				return Image.new("RGBA",(1,fontSize),tuple(bg))
			size=fnt.getsize(text)
			ret=Image.new("RGBA",size,tuple(c_color_TRANSPARENT))
			dr=ImageDraw.Draw(ret)
			dr.text((0,0),text,font=fnt,fill=tuple(fill))
			return ret
		def render_row(_row):
			if(not _row):
				return Image.new("RGBA",(1,fontSize),tuple(bg))
			width=0
			height=0
			now_str=""
			_text_rendered=[]
			for i in _row:
				if(isinstance(i,str)):
					now_str+=i
				elif(isinstance(i,Image.Image) or isinstance(i,_lineFeed)):
					if(now_str):
						_text_rendered.append(render_text(now_str))
						now_str=''
					if(isinstance(i,Image.Image)):
						_text_rendered.append(i)
			for i in _text_rendered:
				w,h=i.size
				width+=w
				height=max(height,h)
			ret=Image.new("RGBA",(width,height),bg)
			left=0
			for i in _text_rendered:
				w,h=i.size
				upper=int((height-h)*alignY)
				ret.paste(i,box=(left,upper),mask=i)
				left+=w
			return ret
		def calc_row_width(_row):
			if(not _row):
				return 0
			now_str=""
			ret=0
			for i in _row:
				if(isinstance(i,str)):
					now_str+=i
				elif(isinstance(i,Image.Image) or isinstance(i,_lineFeed)):
					if(now_str):
						#_text_rendered.append(render_text(now_str))
						ret+=fnt.getsize(now_str)[0]
						now_str=''
					if(isinstance(i,Image.Image)):
						ret+=i.size[0]
			return ret
		for i in _contents:
			
		
class text(widget):
	#content should be str or callable object that returns str
	def __init__(self,content,font=None,fontSize=None,bg=None,lang=None,fill=None):
		self.font=font
		self.fontSize=fontSize
		self.bg=bg
		self.fill=fill
		self.content=content
		#self.lang=lang
	def render(self,**kwargs):
		font=self.font or kwargs.get('font') or mylocale.get_default_font()
		fontSize=self.fontSize or kwargs.get('fontSize') or 12
		#lang=self.lang or kwargs.get('lang') or mylocale.get_default_lang()
		bg=self.bg or kwargs.get('bg') or c_color_TRANSPARENT
		fill=self.fill or kwargs.get('fill') or c_color_BLACK
		
		content=solveCallable(self.content,**kwargs)
		
		
		fnt=ImageFont.truetype(font,fontSize)
		size=fnt.getsize_multiline(content)
		ret=Image.new("RGBA",size,tuple(bg))
		dr=ImageDraw.Draw(ret)
		dr.multiline_text((0,0),content,font=fnt,fill=tuple(fill))
		return ret
if(__name__=='__main__'):

	def textFunction(**kwargs):
		from datetime import datetime
		return datetime.now().strftime("%Y%m%d\n%H%M\n")+"嗯喵め😀"

	im=Image.open(r"M:\pic\夜巡\小清水.png")
	row1=row([im]*2,stretchWH=(200,120),borderWidth=10)
	row2=row([im]*3,stretchHeight=120,borderWidth=10)
	row3=sizer(row2,stretchWH=(300,30))
	row4=text(textFunction)
	col1=column([row1,row2,row3,row4],borderWidth=10,bg=c_color_WHITE)
	col1.render().show()