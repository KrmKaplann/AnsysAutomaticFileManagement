import os
import time



def DeleteOrADDFigureAndComment(Key, Selected):
    if Selected.GetType().Name != "TreeGroupingFolder":

        for CountImages in range(DictGlobalSettings[Key]["FigureNo"] + 1):
            if DictGlobalSettings[Key]["FigureNo"] > len(Selected.Figures):
                Selected.AddFigure()
                if DictGlobalSettings[Key]["FigureNo"] == len(Selected.Figures):
                    break

            elif DictGlobalSettings[Key]["FigureNo"] < len(Selected.Figures):
                for IndexFigureNO, Figure in enumerate(Selected.Figures):
                    Figure.Delete()
                    if DictGlobalSettings[Key]["FigureNo"] == len(Selected.Figures):
                        break

        for CountImages in range(DictGlobalSettings[Key]["ExplanationNo"] + 1):
            if DictGlobalSettings[Key]["ExplanationNo"] > len(Selected.Comments):
                Selected.AddComment()
                if DictGlobalSettings[Key]["ExplanationNo"] == len(Selected.Comments):
                    break

            elif DictGlobalSettings[Key]["ExplanationNo"] < len(Selected.Comments):
                for IndexFigureNO, Comment in enumerate(Selected.Comments):
                    Comment.Delete()
                    if DictGlobalSettings[Key]["ExplanationNo"] == len(Selected.Comments):
                        break


# -*- coding: utf-8 -*-

def FigureANDCommentName(Object, Key, Coordinate, EKAciklama=""):
    if Object.GetType().Name != "TreeGroupingFolder":
        for FigureIndex, Figure in enumerate(Object.Figures):
            Figure.Name = "[ " + str(FigureIndex + 1) + " ] " + Key + " " + Coordinate[FigureIndex] + EKAciklama
        for CommentIndex, Comment in enumerate(Object.Comments):
            Comment.Name = "[ " + str(CommentIndex + 1) + " ] " + Key + " " + Coordinate[CommentIndex] + EKAciklama


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


def ImagesPosition(Object, List):
    if Object.GetType().Name != "TreeGroupingFolder":
        EK = []
        TotalNoOfComment = len(Object.Comments)
        TotalNoOfImages = len(Object.Figures)

        if TotalNoOfImages > TotalNoOfComment:
            CountingObject = Object.Figures
        elif TotalNoOfImages <= TotalNoOfComment:
            CountingObject = Object.Comments

        for ObjectIndex, Object in enumerate(CountingObject):
            Object.Activate()
            try:
                CameraSettings(CameraSettingsDict, List[ObjectIndex])
                EK.append(List[ObjectIndex])
            except:
                # CameraSettings(CameraSettingsDict, "ISO")
                pass
                try:
                    EK.append(List[ObjectIndex])
                except:
                    EK.append("Manually")

        return EK


CameraSettingsDict = {
    "XY": {
        "ViewVector": {"X": 0.00001, "Y": 0.00001, "Z": 1},
        "UpVector": {"X": 0.0001, "Y": 1, "Z": 0.00001}
    },
    "XZ": {
        "ViewVector": {"X": 0.00001, "Y": 1, "Z": 0.00001},
        "UpVector": {"X": 0.00001, "Y": 0.00001, "Z": 1}
    },

    "ZY": {
        "ViewVector": {"X": 1, "Y": 0.00001, "Z": 0.00001},
        "UpVector": {"X": 0.00001, "Y": 0.00001, "Z": 1}
    },
    "ISO": {
        "ViewVector": {"X": 0.7, "Y": +0.5, "Z": 0.3},
        "UpVector": {"X": +0.25, "Y": +0.2, "Z": 0.95}
    }
}

DictGlobalSettings = {
    "Analyses": {"FigureNo": 1, "ExplanationNo": 0},
    "Solution": {"FigureNo": 1, "ExplanationNo": 0},
    "Geometry": {"FigureNo": 1, "ExplanationNo": 0},
    "Mesh": {"FigureNo": 3, "ExplanationNo": 0},
    "Materials": {"FigureNo": 1, "ExplanationNo": 0}
}

# XY,XZ,ZY,ISO

PositionForImages = {
    "Analyses": ["Manually"],
    "Solution": ["XY"],
    "Geometry": ["Manually"],
    "Mesh": ["XY", "XY","Manually"],
    "Materials": ["XY", "ISO"]

}



for index, (Key, Value) in enumerate(DictGlobalSettings.items()):


    if "Anal" in Key:
        for Setup in getattr(Model, Key):
            DeleteOrADDFigureAndComment(Key, Setup)
            Text = "\n" + "[ " + str(Setup.Name) + " ] " + " - " + "AltKategori #2 : " + "Global" + ":"
            FigureANDCommentName(Setup, Key, ["Global", "Global"])
            DownloadFile(Setup, ProjectLocation, FileName=Key + "\\" + Setup.Name + "\\")
            ImagesPosition(Setup, PositionForImages[Key])
            GroupListAnalyses = []

            for i in Setup.Children:
                if i.GetType().Name == "Solution":
                    break
                if i.GetType().Name == "TreeGroupingFolder":
                    GroupListAnalyses.append(i)

            for SetupIndex, SetupPart in enumerate(Setup.Children):
                if SetupPart.GetType().Name != "InitialCondition" and SetupPart.Name != "Analysis Settings" and SetupPart.GetType().Name != "Figure" and SetupPart.GetType().Name != "Comment" and SetupPart.GetType().Name != "Solution":
                    GroupName = "NoFolder"

                    DeleteOrADDFigureAndComment(Key, SetupPart)
                    EK = ImagesPosition(SetupPart, PositionForImages[Key])

                    FigureANDCommentName(SetupPart, Key, EK, " " + SetupPart.Name)

                    for i in GroupListAnalyses:
                        for a in i.Children:
                            if a.Name == SetupPart.Name:
                                GroupName = i.Name


    elif "Solut" in Key:
        for Setup in Model.Analyses:

            GroupList = []

            for i in Setup.Solution.Children:
                if i.GetType().Name == "TreeGroupingFolder":
                    GroupList.append(i)

            for IndexSolution, SolutionPart in enumerate(Setup.Solution.Children):
                if SolutionPart.Name == "Solution Information":
                    DeleteOrADDFigureAndComment(Key, SolutionPart)

                    Text = "\n" + "[ " + str(SolutionPart.Name) + " ] " + " - " + "AltKategori #2 : " + "Global" + ":"
                    FigureANDCommentName(SolutionPart, Key, ["Global", "Global"])

                elif SolutionPart.Name != "Solution Information":

                    GroupName = "NoFolder"

                    DeleteOrADDFigureAndComment(Key, SolutionPart)
                    EK = ImagesPosition(SolutionPart, PositionForImages[Key])
                    FigureANDCommentName(SolutionPart, Key, EK, " " + SolutionPart.Name)

                    for i in GroupList:
                        for a in i.Children:
                            if a.Name == SolutionPart.Name:
                                GroupName = i.Name

    elif "Geo" or "Mesh" or "Materials" in Key:
        Object = getattr(Model, Key)
        DeleteOrADDFigureAndComment(Key, Object)
        EK = ImagesPosition(Object, PositionForImages[Key])
        FigureANDCommentName(Object, Key, EK)
