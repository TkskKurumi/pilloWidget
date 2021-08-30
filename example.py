from widgets import *
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
	message=richText(extract_kwa("message"),alignX=0,alignY=1,fontSize=18,dont_split=True,width=210)
	bub=bubble.default(message)
	col=column([uname,bub],alignX=0.1)
	transparent=row([w_avt,col],alignY=0)
	with_bg=compositeBG(transparent,extract_kwa("BG"))
	return transparent,with_bg
if(__name__=='__main__'):
	from os import path
	pth=path.dirname(__file__)
	avt=path.join(pth,'samples','avatar.jpg')
	renderer=profile_renderer()
	renderer.render(avatar=avt,username='TkskKurumi',intro='this is users introduction').show()
	_,__=IM_style_message()
	az=[i+' ' for i in "Hi! \nI'm TkskKurumi! Nice to meet you!".split()]+[Image.open(avt)]
	__.render(avatar=avt,username="TkskKurumi",message=az,bg=None).show()