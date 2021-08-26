from PIL import Image
def stretchHeight(img,height):
	w,h=img.size
	rate=height/h
	w=int(w*rate)
	return img.resize((w,height),Image.LANCZOS)
def stretchWidth(img,width):
	w,h=img.size
	rate=width/w
	h=int(h*rate)
	return img.resize((width,h),Image.LANCZOS)
def expandHeight(img,height,bg=(0,0,0,0)):
	pass