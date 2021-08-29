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
if(__name__=='__main__'):
	renderer=profile_renderer()
	renderer.render(avatar=r"C:\pilloWidget\samples\avatar.jpg",username='TkskKurumi',intro='this is users introduction').show()