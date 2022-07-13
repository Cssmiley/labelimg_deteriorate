import uno
import os
from com.sun.star.beans import PropertyValue
from unohelper import systemPathToFileUrl
#Create a wrapper for the document object so it works with 'with'
statement
#Most calls to the object it just forwards to the object it wraps.
class DisposeToExitWrapper(object):
    '''
    This means that you can use with ... as ...:
    '''
    def __init__(self, obj):
                self._wrapped_obj = obj
    def __getattr__(self, attr):
                if attr in self.__dict__:
                    return getattr(self, attr)
                #else
                return getattr(self._wrapped_obj, attr)
    def __exit__(self, type, value, tb):
                self._wrapped_obj.dispose()
    def __enter__(self):
                return self._wrapped_obj
def dictToProperties(dictionary):

    """
    #Utitlity to convert a dictionary to properties
    """
    props = []
    for key in dictionary:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = dictionary[key]
        props.append(prop)
        return tuple(props)
def convertPathToOOPath(document_path):
    #This adds e.g. file:/// to the start of the path, and makes it absolute (has to be done)
    return systemPathToFileUrl(os.path.abspath(document_path))
#Create a function to quickly and easily open the document
def openDocument(document_path):
    '''document_path can be relative'''
    #Connect to OO
    local = uno.getComponentContext() #
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    #Load services
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document_path_full = convertPathToOOPath(document_path)
    document = desktop.loadComponentFromURL(document_path_full ,"_blank", 0, dictToProperties({"Hidden": True})) #"Hidden" ->Doesn't show up in the GUI
    return DisposeToExitWrapper(document)
#open a document and use
document_path = './mydoc.odt'
with openDocument as safe_document:
    print('Document title is '+document.Title)
#Now the document has been properly disposed of.