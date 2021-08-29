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
	w,h=img.size
	ret=Image.new(img.mode,(w,height),bg)
	top=int((height-h)/2)
	ret.paste(img,box=(0,top),mask=img)
	return ret
def expandWidth(img,width,bg=(0,0,0,0)):
	w,h=img.size
	ret=Image.new(img.mode,(width,h),bg)
	left=int((width-w)/2)
	ret.paste(img,box=(left,0),mask=img)
	return ret
def cropWidth(img,width):
	w,h=img.size
	left=int((w-width)/2)
	return img.crop((left,0,left+width,h))
def cropHeight(img,height):
	w,h=img.size
	upper=int((h-height)/2)
	return img.crop((0,upper,w,upper+height))
def cropWH(img,size):
	width,height=size
	rate=width/height
	w,h=img.size
	r=w/h
	if(r>rate):
		return cropWidth(stretchHeight(img,height),width)
	else:
		return cropHeight(stretchWidth(img,width),height)
if(__name__=='__main__'):
	im=Image.open(r"M:\pic\夜巡\小清水2.png")
	cropWH(im,1000,300).show()