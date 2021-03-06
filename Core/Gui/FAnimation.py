# Copyright (c) 2012 The Khronos Group Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and /or associated documentation files (the "Materials "), to deal in the Materials without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Materials, and to permit persons to whom the Materials are furnished to do so, subject to 
# the following conditions: 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Materials. 
# THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

import wx
import time

from Core.Gui.Grid.FImageRenderArea import *
from Core.Gui.FImageType import *

class FAnimation:
    __REFRESH = 0.1
    __FPS = 10
    
    def __init__(self, imageList, filenameList, row, col, imageWidth, 
                 imageHeight, rect, renderedAreas, bgColour):
        self.__filenameList = filenameList
        self.__imageList = imageList
        self.__index = 0
        self.__imageWidth = imageWidth
        self.__imageHeight = imageHeight
        self.__startTime = 0
        self.__maxTime = FAnimation.__REFRESH * (len(imageList) + 1)
        self.__started = False
        self.__rect = rect
        self.__renderedAreas = renderedAreas
        self.__row = row
        self.__col = col
        self.__oldRenderArea = None
        self.__bgColour = bgColour
    
    def Start(self):
        self.__started = True
        self.__startTime = time.time()
    
    def Update(self, dc):
        if (len(self.__imageList) == 0): return
        
        self.__DrawImage(self.__GetImageIndex(), dc)
    
    def __GetImageIndex(self):
        if (not self.__started): return 0
        
        relativeTime = time.time() - self.__startTime
        
        while (relativeTime > self.__maxTime):
            self.__startTime = self.__startTime + self.__maxTime
            relativeTime = relativeTime - self.__maxTime
        
        index = int(relativeTime * FAnimation.__FPS)
        if (index == len(self.__imageList)):
            index = index - 1 # doubt it will ever happen, but possible
        
        return index
    
    def __DrawImage(self, imageIndex, dc):
        image = self.__imageList[imageIndex]
        # this was mostly copied from FImageRenderer.. need to refactor
        dx = image.GetWidth() - self.__imageWidth
        dy = image.GetHeight() - self.__imageHeight
        
        if ((dx > 0) or (dy > 0)):
            if (dx > dy):
                newWidth = float(self.__imageWidth)
                ratio = newWidth / image.GetWidth()
                newHeight = ratio * image.GetHeight()
            else:
                newHeight = float(self.__imageHeight)
                ratio = newHeight / image.GetHeight()
                newWidth = ratio * image.GetWidth()
            image.Rescale(int(newWidth), int(newHeight))
        
        width, height = image.GetWidth(), image.GetHeight()
        
        if width > self.__rect.width-2:
            width = self.__rect.width-2
        
        if height > self.__rect.height-2:
            height = self.__rect.height-2
        
        offscreenBuffer = wx.EmptyBitmap(width, height)
        imageDC = wx.MemoryDC()
        imageDC.SelectObject(offscreenBuffer)
        
        imageDC.SetPen(wx.Pen(self.__bgColour))
        imageDC.SetBrush(wx.Brush(self.__bgColour))
        imageDC.DrawRectangle(0, 0, width, height)
        imageDC.DrawBitmap(wx.BitmapFromImage(image), 0, 0, True)
        
        dc.Blit(self.__rect.x + 1, self.__rect.y + 1, width, height, imageDC, 
                0, 0, wx.COPY, True)
        
        if (self.__oldRenderArea != None):
            self.__renderedAreas[(self.__row, self.__col)].remove(
                    self.__oldRenderArea)
        
        self.__oldRenderArea = FImageRenderArea(self.__rect.x + 1, 
                self.__rect.y + 1, width, height, self.__filenameList, 
                FImageType.ANIMATION)
        
        self.__renderedAreas[(self.__row, self.__col)].append(
                self.__oldRenderArea)
    