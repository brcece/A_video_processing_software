import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

class Frame_Grab(ABC):
	def BGR2HSV(self, img, lhsv, uhsv):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lhsv, uhsv)
		return cv2.bitwise_and(img, img, mask= mask)

class Sliders_Data(ABC):
	def __init__(self):
		self.__spositions = []

	def Set_Slider_Data(self, slider_data):
		self.__spositions = slider_data

	def Get_Slider_Data(self):
		return self.__spositions

class Region(Frame_Grab, Sliders_Data):
	def __init__(self):
		Frame_Grab.__init__(self)
		Sliders_Data.__init__(self)

		self.PixelNO = 0

	@abstractmethod
	def Pixel_Calculation(self, img):
		pass

	def GetPixelNo(self):
		return self.PixelNO

class Region1(Region):
	def __init__(self):
		Region.__init__(self)

	def Pixel_Calculation(self, img):
		slider_data = self.Get_Slider_Data()
		lhsv = np.array([slider_data[0], slider_data[2], slider_data[4]])
		uhsv = np.array([slider_data[1], slider_data[3], slider_data[5]])

		img = self.BGR2HSV(img, np.array(lhsv), np.array(uhsv))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.PixelNO = cv2.countNonZero(img)

class Region2(Region):
	def __init__(self):
		Region.__init__(self)

	def Pixel_Calculation(self, img):
		slider_data = self.Get_Slider_Data()
		lhsv = np.array([slider_data[0], slider_data[2], slider_data[4]])
		uhsv = np.array([slider_data[1], slider_data[3], slider_data[5]])

		img = self.BGR2HSV(img, np.array(lhsv), np.array(uhsv))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.PixelNO = cv2.countNonZero(img)

class Region3(Region):
	def __init__(self):
		Region.__init__(self)

	def Pixel_Calculation(self, img):
		slider_data = self.Get_Slider_Data()
		lhsv = np.array([slider_data[0], slider_data[2], slider_data[4]])
		uhsv = np.array([slider_data[1], slider_data[3], slider_data[5]])

		img = self.BGR2HSV(img, np.array(lhsv), np.array(uhsv))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		self.PixelNO = cv2.countNonZero(img)

class Filter(Frame_Grab, Sliders_Data):
	def __init__(self):
		Frame_Grab.__init__(self)
		Sliders_Data.__init__(self)

		self.Set_Slider_Data(255)

	def Filter_Implement(self, img):
		_, res = cv2.threshold(img, self.Get_Slider_Data(), 255, cv2.THRESH_TRUNC)
		return res

window = tk.Tk()
window.title("video işleme ")
window.geometry("900x800")
window.configure(bg="DodgerBlue4")

global secondWindow, secondWindowLabelImage
secondWindow = None
secondWindowLabelImage = None
lhsv = np.array([110,50,50])
uhsv = np.array([110,50,50])
threshold = 0
regions = []
regions.append(Region1())
regions.append(Region2())
regions.append(Region3())

filter = Filter()


s = ttk.Style()

s.configure('new.TFrame', background='lightskyblue1')

mainFrame = ttk.Frame(window, style='new.TFrame')
mainFrame.pack()
frameCam = ttk.Frame(mainFrame, style='new.TFrame')
frameCam.grid(row = 0, column = 0, padx=5, pady=5)
frameSliders = ttk.Frame(mainFrame, style='new.TFrame')
frameSliders.grid(row = 1, column = 0, padx=5, pady=5)
frameButtons = ttk.Frame(mainFrame, style='new.TFrame')
frameButtons.grid(row = 0, column = 1, rowspan=2, padx=5, pady=5)
frame1 = ttk.Label(frameCam)
frame1.pack()
videoCapturer = cv2.VideoCapture(0)

labels = [
	ttk.Label(frameSliders, text='LH: 0'),
	ttk.Label(frameSliders, text='UH: 0'),
	ttk.Label(frameSliders, text='LV: 0'),
	ttk.Label(frameSliders, text='UV: 0'),
	ttk.Label(frameSliders, text='LS: 0'),
	ttk.Label(frameSliders, text='US: 0'),
	ttk.Label(frameSliders, text='Threshold: 0')
]

for i in range(7):
	labels[i].grid(row=i)

sliders = []

def do_Slider(val):
	labels[0].config(text='LH: %d' % int(sliders[0].get()))
	labels[1].config(text='UH: %d' % int(sliders[1].get()))
	labels[2].config(text='LV: %d' % int(sliders[2].get()))
	labels[3].config(text='UV: %d' % int(sliders[3].get()))
	labels[4].config(text='LS: %d' % int(sliders[4].get()))
	labels[5].config(text='US: %d' % int(sliders[5].get()))
	labels[6].config(text='Threshold: %d' % int(sliders[6].get()))

for i in range(7):
	slider = ttk.Scale(frameSliders,length=400,from_=0,to=255,orient='horizontal',command=do_Slider)
	slider.grid(row = i, column=1)
	sliders.append(slider)

def press_Threshold():
	filter.Set_Slider_Data(sliders[6].get())

	global secondWindow, secondWindowLabelImage
	try:
		secondWindow.destroy()
	except:
		pass

	secondWindow = tk.Toplevel(window)
	secondWindow.geometry("800x600")
	label = ttk.Label(secondWindow)
	label.pack()
	img = videoCapturer.read()[1].copy()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	secondWindowLabelImage = ImageTk.PhotoImage(Image.fromarray(filter.Filter_Implement(img)))
	label['image'] = secondWindowLabelImage


def OnPressCalcRegion(regNo):
	img = videoCapturer.read()[1]
	f1, f2, f3 = np.array_split(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 3, axis=1)

	if regNo == 1: img = f1
	elif regNo == 2: img = f2
	elif regNo == 3: img = f3

	region = regions[regNo-1]
	region.Set_Slider_Data([float(sliders[0].get()),float(sliders[1].get()),float(sliders[2].get()),float(sliders[3].get()),float(sliders[4].get()),float(sliders[5].get()),])

	region.Pixel_Calculation(img)
	messagebox.showinfo("Info", " pixel count result: %d" % (region.GetPixelNo()))


buttonApplyThreshold = tk.Button(frameButtons, text ="Apply \nThreshold",font=("Calvin",15,"bold","italic"),bg="steel blue",fg="goldenrod2",activebackground = "SkyBlue2",command=press_Threshold)
buttonApplyThreshold.grid(row = 0, pady=10)
buttonCalc1 = tk.Button(frameButtons, text ="CALCULATE \nREGION 1",font=("Calvin",15,"bold","italic"),bg="SlateBlue4",fg="LavenderBlush4",activebackground = "SkyBlue2" ,command = lambda regNo = 1 : OnPressCalcRegion(regNo))
buttonCalc1.grid(row = 1, pady=10)
buttonCalc2 = tk.Button(frameButtons, text ="CALCULATE \nREGION 2", font=("Calvin",15,"bold","italic"),bg="SlateBlue4",fg="LavenderBlush4",activebackground = "SkyBlue2" ,command = lambda regNo = 2 : OnPressCalcRegion(regNo))
buttonCalc2.grid(row = 2, pady=10)
buttonCalc3 = tk.Button(frameButtons, text ="CALCULATE \nREGION 3",font=("Calvin",15,"bold","italic"),bg="SlateBlue4",fg="LavenderBlush4",activebackground = "SkyBlue2" ,command = lambda regNo = 3 : OnPressCalcRegion(regNo))
buttonCalc3.grid(row = 3, pady=10)
sliders[-1].set(255)
sliders[1].set(255)
sliders[3].set(255)
sliders[5].set(255)

while True:
	img = videoCapturer.read()[1]
	f1, f2, f3  = np.array_split(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 3, axis=1)

	line = np.ones((f1.shape[:2][0] , 3, 3), dtype=np.uint8) * 255

	slider_data = [float(sliders[0].get()),float(sliders[1].get()),float(sliders[2].get()),float(sliders[3].get()),float(sliders[4].get()),float(sliders[5].get())]

	lhsv = np.array([slider_data[0], slider_data[2], slider_data[4]])
	uhsv = np.array([slider_data[1], slider_data[3], slider_data[5]])

	f1 = cv2.bitwise_and(f1, f1, mask= cv2.inRange(cv2.cvtColor(f1, cv2.COLOR_RGB2HSV), lhsv, uhsv))
	f2 = cv2.bitwise_and(f2, f2, mask= cv2.inRange(cv2.cvtColor(f2, cv2.COLOR_RGB2HSV), lhsv, uhsv))
	f3 = cv2.bitwise_and(f3, f3, mask= cv2.inRange(cv2.cvtColor(f3, cv2.COLOR_RGB2HSV), lhsv, uhsv))

	img = ImageTk.PhotoImage(Image.fromarray(np.concatenate((f1, line, f2, line, f3), axis=1)))
	frame1['image'] = img

	window.update()

videoCapturer.release()
cv2.destroyAllWindows()
