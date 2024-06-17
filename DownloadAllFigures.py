import os
import time

FileName = "Result"
ProjectLocation = "C:\Users\***\****\*\AutomateSavedFigures\\" + FileName


def DownloadFile(Object, ProjectLocation, FileName, breaking=0):
    if breaking == 0:
        if "Geo" or "Mater" in FileName:
            if Object.GetType().Name != "TreeGroupingFolder":
                for FigureIndex, Figure in enumerate(Object.Figures):
                    print(Figure.Name)
                    Figure.Activate()
                    ImagineName = Figure.Name
                    print(ImagineName)
                    image_settings = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
                    image_settings.CurrentGraphicsDisplay = False
                    image_settings.Resolution = GraphicsResolutionType.NormalResolution
                    image_settings.Capture = GraphicsCaptureType.ImageAndLegend
                    image_settings.Background = GraphicsBackgroundType.White
                    image_settings.FontMagnification = 1
                    Graphics.ExportImage(ProjectLocation + "\\" + FileName + "\\" + ImagineName + ".png",
                                         GraphicsImageExportFormat.PNG)


def CameraSettings(CameraSettingsDict, Location):
    Graphics.Camera.ViewVector = Vector3D(
        CameraSettingsDict[Location]["ViewVector"]["X"],
        CameraSettingsDict[Location]["ViewVector"]["Y"],
        CameraSettingsDict[Location]["ViewVector"]["Z"])

    Graphics.Camera.UpVector = Vector3D(
        CameraSettingsDict[Location]["UpVector"]["X"],
        CameraSettingsDict[Location]["UpVector"]["Y"],
        CameraSettingsDict[Location]["UpVector"]["Z"])

    Graphics.Camera.SetFit()

    HeightObject = float(str(Graphics.Camera.SceneHeight)[:5])
    WidthObject = float(str(Graphics.Camera.SceneWidth)[:5])

    Graphics.Camera.SceneHeight = Quantity(HeightObject + 0.1, "m")
    Graphics.Camera.SceneWidth = Quantity(WidthObject + 0.1, "m")


os.mkdir(ProjectLocation)
for Key, Value in DictGlobalSettings.items():
    os.chdir(ProjectLocation)
    os.mkdir(Key)
    if Key == "Solution" or Key == "Analyses":
        for AnalyseIndex, Analyse in enumerate(Model.Analyses):
            os.chdir(ProjectLocation + "\\" + Key)
            os.mkdir(Analyse.Name)
            if Key == "Solution":
                for SolutionIndex, Solution in enumerate(Analyse.Solution.Children):
                    if Solution.GetType().Name == "TreeGroupingFolder":
                        os.chdir(ProjectLocation + "\\" + Key + "\\" + Analyse.Name)
                        os.mkdir(Solution.Name)

            elif Key == "Analyses":
                for AnalyseBCIndex, AnalyseBC in enumerate(Analyse.Children):
                    if AnalyseBC.GetType().Name == "TreeGroupingFolder":
                        os.chdir(ProjectLocation + "\\" + Key + "\\" + Analyse.Name)
                        os.mkdir(AnalyseBC.Name)

for index, (Key, Value) in enumerate(DictGlobalSettings.items()):

    if "Anal" in Key:
        for Setup in getattr(Model, Key):
            DownloadFile(Setup, ProjectLocation, FileName=Key + "\\" + Setup.Name + "\\")
            GroupListAnalyses = []

            for i in Setup.Children:
                if i.GetType().Name == "Solution":
                    break
                if i.GetType().Name == "TreeGroupingFolder":
                    GroupListAnalyses.append(i)

            for SetupIndex, SetupPart in enumerate(Setup.Children):
                if SetupPart.GetType().Name != "InitialCondition" and SetupPart.Name != "Analysis Settings" and SetupPart.GetType().Name != "Figure" and SetupPart.GetType().Name != "Comment" and SetupPart.GetType().Name != "Solution":
                    GroupName = "NoFolder"

                    for i in GroupListAnalyses:
                        for a in i.Children:
                            if a.Name == SetupPart.Name:
                                GroupName = i.Name

                    if GroupName != "NoFolder":
                        DownloadFile(SetupPart, ProjectLocation, FileName=Key + "\\" + Setup.Name + "\\" + GroupName)
                    else:
                        DownloadFile(SetupPart, ProjectLocation, FileName=Key + "\\" + Setup.Name)

    elif "Solut" in Key:
        for Setup in Model.Analyses:

            GroupList = []

            for i in Setup.Solution.Children:
                if i.GetType().Name == "TreeGroupingFolder":
                    GroupList.append(i)

            for IndexSolution, SolutionPart in enumerate(Setup.Solution.Children):
                if SolutionPart.Name == "Solution Information":
                    pass
                elif SolutionPart.Name != "Solution Information":

                    GroupName = "NoFolder"

                    for i in GroupList:
                        for a in i.Children:
                            if a.Name == SolutionPart.Name:
                                GroupName = i.Name

                    if GroupName != "NoFolder":
                        DownloadFile(SolutionPart, ProjectLocation, FileName=Key + "\\" + Setup.Name + "\\" + GroupName)
                    else:
                        DownloadFile(SolutionPart, ProjectLocation, FileName=Key + "\\" + Setup.Name)


    elif "Geo" or "Mesh" or "Materials" in Key:
        Object = getattr(Model, Key)
        DownloadFile(Object, ProjectLocation, FileName=Key)
