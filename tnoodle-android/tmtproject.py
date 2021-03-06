import tmt
import os
import os.path

class Project(tmt.TmtProject):
    def configure(self):
        self.gradlew = "(cd %s; ./gradlew %%s)" % self.name

    def getDependencies(self):
        return [ tmt.TmtProject.projects['scrambles'] ]

    def runGradleTask(self, task):
        retVal = os.system(self.gradlew % task)
        assert retVal == 0

    def compile(self):
        # Note that we skip signing here in order to prevent
        # travis ci issue.
        self.runGradleTask("assemble -x signArchives")

    def clean(self):
        self.runGradleTask("clean")

    def check(self):
        pass

    def publishToMavenCentral(self):
        self.runGradleTask("uploadArchives")
        self.runGradleTask("nexusStagingRelease")

Project(tmt.projectName(), description="Android scrambling library")
