# Copyright (C) 2007 Khronos Group
# Available only to Khronos members.
# Distribution of this file or its content is strictly prohibited.

# Basic: doesn't allow crashes.
# Intermediate: verifies validation
# Advanced: checks that intermediate passes.

from StandardDataSets.scripts import JudgeAssistant

class SimpleJudgingObject:
    def __init__(self):
        self.__assistant = JudgeAssistant.JudgeAssistant()
        
    def JudgeBasic(self, context):
        # To support the case when Intermediate is run before Basic: we reset the judgement result.
        # This does not affect the cached results, though, so performance is still greatly improved.
        self.__assistant.ResetJudgement()
        self.__assistant.CheckCrashes(context)
        return self.__assistant.DeferJudgement(context)

    def JudgeIntermediate(self, context):
        self.JudgeBasic(context)
        self.__assistant.CheckSteps(context, ["Import", "Export", "Validate"], ["Render"])
        return self.__assistant.DeferJudgement(context)

    def JudgeAdvanced(self, context): return self.JudgeIntermediate(context)

judgingObject = SimpleJudgingObject();