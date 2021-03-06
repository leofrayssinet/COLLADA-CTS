# Copyright (c) 2012 The Khronos Group Inc.
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and /or associated documentation files (the "Materials "), to deal in the Materials without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Materials, and to permit persons to whom the Materials are furnished to do so, subject to 
# the following conditions: 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Materials. 
# THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.

from ImageComparators.FImageComparator import *
import os
import os.path

class FByteComparator (FImageComparator):
    """The class which represents byte comparison to the testing framework.
    
    This class uses a byte by byte comparison to compare images.
    
    """
    
    PASS_EXTRA = 0
    FAIL_EXTRA = 10000
    
    def __init__(self, configDict):
        """__init__() -> FByteComparator
        
        arguments:
            configDict
                dict of values taken from the config.txt file with  user
                specified values.
        
        """
        FImageComparator.__init__(self, configDict)
    
    
    def CompareImages(self, filename1, filename2, tolerance=5):
        """CompareImages(filename1, filename2, tolerance = 5) -> FCompareResult
        
        Implements FImageComparator.CompareImages(filename1, filename2, tolerance). 
        
        The result is positive only if both files are byte by byte similar, or 
        if both files do not exist. The tolerance value is not used by the ByteComparator.
        
        arguments:
            filename1
                str corresponding to a file to compare.
            filename2
                str corresponding to another file to compare.
            tolerance
                integer corresponding to the acceptable difference
                between the two images. Not used by the FByteComparator.
        
        returns:
            FCompareResult indicating the images are the same or different. 
            Only the result of FComapreResult is set; the extra is not set.
        
        """
        compareResult = FCompareResult()
        compareResult.SetResult(False)
        compareResult.SetExtra(FByteComparator.FAIL_EXTRA)
        
        filename1 = os.path.normpath(os.path.abspath(filename1))
        filename2 = os.path.normpath(os.path.abspath(filename2))
        if (os.path.isfile(filename1)):
            if (not os.path.isfile(filename2)):
                return compareResult
        else:
            if (os.path.isfile(filename2)):
                return compareResult
            
            compareResult.SetResult(True)
            return compareResult
        
        f1 = open(filename1, "rb")
        f2 = open(filename2, "rb")
        
        block1 = f1.read(10240) # 10 KB
        block2 = f2.read(10240) # 10 KB
        
        while (block1 == block2):
            if ((len(block1) == 0) and (len(block2) == 0)):
                f1.close()
                f2.close()
                compareResult.SetResult(True)
                compareResult.SetExtra(FByteComparator.PASS_EXTRA)
                return compareResult
                
            block1 = f1.read(10240) # 10 KB
            block2 = f2.read(10240) # 10 KB
        
        f1.close()
        f2.close()
        
        return compareResult
    
    def GetMessage(self, compareResultList):
        """GetMessage(compareResultList)->str
        
        Implements FImageComparator.GetMessage(compareResultList). 
        
        The FByteComparator uses the default message.
        
        arguments:
            compareResultList
                list of FCompareResult that this FImageComparator generated for
                a given image/animation. If it is an image it will be in the
                form [FCompareResult1, FCompareResult2, ...] for each blessed
                image there is if none matched, or simply [FCompareResult,] if
                there is a match. If it is an animation, it will be in the form
                [[FCompareResult1, FCompraeResult2,...],...] where the inner 
                list is for each blessed animation there is and the elements of
                that list are for each image in the animation. Similarily to 
                the single image, it will be simply 
                [[FCompareResult1, FCompraeResult2,...],] if there is an 
                animation match.
        
        returns:
            str representing the empty string so that the CTF uses the default
            message.
        
        """
        return ""
