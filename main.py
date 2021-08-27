from PIL import Image
from constants import *
import resize
#const:
#c_color_* for const colors
import mylocale
def solveCallable(i):
	while(callable(i)):
		i=i()
	return i
def _render_content(i,**kwargs):
	solveCallable(i)
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
	def __init__(self,content,stretchWH=None,stretchWidth=None,stretchHeight=None,expandHeight=None,expandWidth=None):
		self.content=content
		self.stretchWidth=stretchWidth
		self.stretchHeight=stretchHeight
		self.expandHeight=expandHeight
		self.expandWidth=expandWidth
		self.stretchWH=stretchWH
	def render(self,**kwargs):
		ret=_render_content(self.content,**kwargs)
		if(self.stretchWH):
			ret=ret.resize(self.stretchWH,Image.LANCZOS)
			return ret
		if(self.stretchWidth):
			ret=resize.stretchWidth(ret,self.stretchWidth)
			return ret
		if(self.stretchHeight):
			ret=resize.stretchHeight(ret,self.stretchHeight)
			return ret

class text(widget):
	#content should be str or callable object that returns str
	def __init__(self,content,font=None):
		self.font=None
	def render(self,**kwargs):
		font=self.font or kwargs.get('font') or mylocale.get_default_font()
		
if(__name__=='__main__'):
	im=Image.open(r"C:\Users\xiaofan\AppData\Roaming\Typora\themes\autumnus-assets\XiQW8UwuDOf1gjN.png")
	
	row1=row([im]*2,stretchWH=(200,120),borderWidth=10)
	row2=row([im]*3,stretchHeight=120,borderWidth=10)
	row3=sizer(row2,stretchWH=(300,30))
	col1=column([row1,row2,row3],borderWidth=10,bg=c_color_WHITE)
	col1.render().show()