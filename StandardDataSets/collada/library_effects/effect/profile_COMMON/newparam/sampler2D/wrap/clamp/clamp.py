# Copyright (C) 2007 Khronos Group
# Available only to Khronos members.
# Distribution of this file or its content is strictly prohibited.

# See Core.Logic.FJudgementContext for the information
# of the 'context' parameter.

# This sample judging object does the following:
#
# JudgeBaseline: just verifies that the standard steps did not crash.
# JudgeSuperior: also verifies that the validation steps are not in error.
# JudgeExemplary: same as intermediate badge.

# We import an assistant script that includes the common verifications
# methods. The assistant buffers its checks, so that running them again
# does not incurs an unnecessary performance hint.
from StandardDataSets.scripts import JudgeAssistant

# Please feed your node list here:
tagLst = [['library_effects', 'effect', 'newparam', 'sampler2D', 'wrap_s'], ['library_effects', 'effect', 'newparam', 'sampler2D', 'wrap_t']]
tagLst2 = [['library_effects', 'effect', 'profile_COMMON', 'newparam', 'sampler2D', 'wrap_s'], ['library_effects', 'effect', 'profile_COMMON', 'newparam', 'sampler2D', 'wrap_t']]
attrName = ''
attrVal = ''
dataToCheck = 'CLAMP'

class SimpleJudgingObject:
    def __init__(self, _tagLst, _tagLst2, _attrName, _attrVal, _data):
        self.tagList = _tagLst
        self.tagList2 = _tagLst2
        self.attrName = _attrName
        self.attrVal = _attrVal
        self.dataToCheck = _data
        self.status_baseline = False
        self.status_superior = False
        self.status_exemplary = False
        self.__assistant = JudgeAssistant.JudgeAssistant()
    
    def dataPreserved(self, context):
        inEffectS = self.__assistant.ElementDataCheck(context, self.tagList[0], self.dataToCheck, "string")
        inEffectT = self.__assistant.ElementDataCheck(context, self.tagList[1], self.dataToCheck, "string")
        
        if (inEffectS and inEffectT)
            return True
        
        inProfileS = self.__assistant.ElementDataCheck(context, self.tagList2[0], self.dataToCheck, "string")
        inProfileT = self.__assistant.ElementDataCheck(context, self.tagList2[1], self.dataToCheck, "string")
        
        if (inProfileS and inProfileT)
            return True
            
        return False
    
    def JudgeBaseline(self, context):
        # No step should not crash
        self.__assistant.CheckCrashes(context)
        
        # Import/export/validate must exist and pass, while Render must only exist.
        self.__assistant.CheckSteps(context, ["Import", "Export", "Validate"], ["Render"])
        
        if (self.__assistant.GetResults() == False): 
            self.status_baseline = False
            return False
            
        # Compare the rendered images between import and export
        # Then compare images against reference test
        # Last, check for preservation of element data
        if ( self.__assistant.CompareRenderedImages(context) ):
            if ( self.__assistant.CompareImagesAgainst(context, "_reference_wrap", None, None, 5, True, False) ):
                if ( self.dataPreserved(context) ):
                    self.status_baseline = True
                    return self.status_baseline
        
        self.status_baseline = False
        return self.status_baseline
  
    # To pass intermediate you need to pass basic, this object could also include additional 
    # tests that were specific to the intermediate badge.
    def JudgeSuperior(self, context):
        self.status_superior = self.status_baseline
        return self.status_superior 
            
    # To pass advanced you need to pass intermediate, this object could also include additional
    # tests that were specific to the advanced badge
    def JudgeExemplary(self, context):
        self.status_exemplary = self.status_superior
        return self.status_exemplary 
       
# This is where all the work occurs: "judgingObject" is an absolutely necessary token.
# The dynamic loader looks very specifically for a class instance named "judgingObject".
#
judgingObject = SimpleJudgingObject(tagLst, tagLst2, attrName, attrVal, dataToCheck);