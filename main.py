from PIL import Image

class widget:
	def get_rendered_contents(self):
		ret=list()
		for i in self.contents:
			while(callable(i)):
				i=i()
			if(isinstance(i,Image.Image)):
				ret.append(i)
			if(isinstance(i,widget)):
				ret.append(i.render())
			
	pass
	
class row(widget):
	def __init__(self,contents,stretchHeight=None,expandHeight=None,cropHeight=None):
		self.contents=contents
		self.stretchHeight=stretchHeight
		self.expandHeight=expandHeight
		self.cropHeight=cropHeight