from widgets import *
from os import path
result_pth=path.join(path.dirname(__file__),'samples','results')
project_pth=path.dirname(__file__)
avatar_pth=path.join(project_pth,'samples','avatar.jpg')
def profile_renderer():
	def func_avatar(**kwargs):
		avt=kwargs.get("avatar")
		avt=Image.open(avt)
		return avt
	def func_name(**kwargs):
		return kwargs.get("username")
	def func_introduction(**kwargs):
		return kwargs.get("intro")
	
	avt=avatarCircle(func_avatar,size=50)
	name=text(func_name,fontSize=36)
	row1=row([avt,name],alignY=0.618)
	row2=richText(func_introduction,300,fontSize=24)
	
	ret=column([row1,row2],width=300)
	return ret
def IM_style_message():
	def func_avatar(**kwargs):
		avt=kwargs.get("avatar")
		if(isinstance(avt,Image.Image)):
			return avt
		else:
			return Image.open(avt)
	def extract_kwa(key):
		def inner(key=key,**kwargs):
			return kwargs.get(key)
		return inner
	w_avt=avatarCircle(func_avatar,size=100)
	uname=text(extract_kwa("username"),fontSize=24)
	message=richText(extract_kwa("message"),alignX=0,alignY=1,fontSize=18,width=300,autoSplit=True,dont_split=True)
	bub=bubble.default(message,border_size=30)
	col=column([uname,bub],alignX=0.1)
	transparent=row([w_avt,col],alignY=0)
	with_bg=compositeBG(transparent,extract_kwa("BG"))
	return transparent,with_bg
def im_message_example():
	transparent,with_bg=IM_style_message()
	rich_text_message=[]
	rich_text_message.append("Hi, greets! \nIsn't my avatar cute?\n")
	rich_text_message.append(Image.open(avatar_pth))
	rich_text_message.append("This widget can combine text contents and image contents. Like QQ messages.")
	a=with_bg.render(avatar=avatar_pth,username="TkskKurumi",message=rich_text_message)
	b=transparent.render(avatar=avatar_pth,username="TkskKurumi",message=rich_text_message)
	save_example('im_message_exampleA',a)
	save_example('im_message_exampleB',b)
def setKwargs_example():
	t=text('content1')
	a=setKwargs(content=t,fill=c_color_BLUE)
	r=row([t,a],bg=c_color_WHITE)
	r.render().save(path.join(result_pth,'setKwargs1.png'))
	#wont overwrite bg's own attribute
	b=setKwargs(content=r,bg=c_color_RED_lighten)
	b.render().save(path.join(result_pth,'setKwargs2.png'))
	#will pass to row renderer because its bg is None
	r.bg=None
	b.render().save(path.join(result_pth,'setKwargs3.png'))
	
if(False and __name__=='__main__'):
	from os import path
	pth=path.dirname(__file__)
	avt=path.join(pth,'samples','avatar.jpg')
	renderer=profile_renderer()
	renderer.render(avatar=avt,username='TkskKurumi',intro='this is users introduction').show()
	_,__=IM_style_message()
	az=[i+' ' for i in "Hi! \nI'm TkskKurumi! Nice to meet you!".split()]+[Image.open(avt)]
	__.render(avatar=avt,username="TkskKurumi",message=az,bg=None).show()
def save_example(name,im):
	p=path.join(result_pth,name+'.png')
	im.save(p)
def row_example():
	a=text('content1',fill=c_color_RED)
	b=text('content2',fill=c_color_GREEN)
	c=text('content3',fill=c_color_BLUE)
	r=row([a,b,c])
	save_example('row_example',r.render())
def callable_content_example():
	def func(**kwargs):
		from datetime import datetime
		return datetime.now().strftime("%Y%m%d%H%M")+"\n,kwargs=%s"%kwargs
	t=text(func)
	t.render(bg=c_color_WHITE).save(path.join(result_pth,'callable_content_example1.png'))
	t.render(bg=c_color_BLACK,fill=c_color_WHITE).save(path.join(result_pth,'callable_content_example2.png'))

	
if(__name__=='__main__'):
	setKwargs_example()
	callable_content_example()
	row_example()
	im_message_example()