'''
PlugSy - SDK Gui Confirmation Dialog - Holds all confirmation dialog classes
'''

# Import libs
import wx

# Import project libs
from .SdkGuiAbs import ConfirmationDialog

# ======================================
# = _ConfirmationDialogAbs Class
# ======================================
class _ConfirmationDialogAbs(ConfirmationDialog):
    '''
    Provides ab abstract confirmation dialog with a customisable message
    '''

    def __init__(self, parent, message):
        '''
        Constructor
        @param parent: Handle to parent object
        @param message: The dialog confirmation message
        '''
        self.parent = parent
        ConfirmationDialog.__init__(self, parent=parent)
        self.update_message(message)

        # Set events
        self.__set_events()

        # Disable parent
        self.parent.Disable()


    def update_message(self, message):
        '''
        Sets the Dialog box message
        @return:
        @todo Fix refreshing so that size of dialog is adjusted... or rather so that word wrap works
        '''

        self.ConfirmationLabel.SetLabelText(message)
        self.ConfirmationLabel.Wrap(250)
        self.ConfirmationLabel.Layout()


    def __set_events(self):
        '''
        Set dialog event handlers
        @return:
        '''

        self.Bind(wx.EVT_BUTTON, self.__cancel, self.OkCancelSizerCancel)


    def __cancel(self, event):
        '''
        Cancels plugin creation and re-enables Main GUI
        @return:
        '''

        self.parent.Enable()
        self.Destroy()


# ======================================
# = DeletePluginConfirmation Class
# ======================================
class DeletePluginConfirmation(_ConfirmationDialogAbs):
    '''
    Provides ab abstract confirmation dialog with a customisable message
    '''

    def __init__(self, parent, plugin_name, sdk):
        '''
        Constructor
        @param parent: Handle to parent object
        @param plugin_name: The name of the plugin being deleted
        @param sdk: A handle to the SDK object
        '''
        self.__message = "Are you sure you want to delete the '%s' plugin?" % plugin_name
        self.__sdk = sdk
        _ConfirmationDialogAbs.__init__(self, parent, self.__message)

        # Set events
        self.__set_events()


    def __set_events(self):
        '''
        Bind events
        '''

        self.Bind(wx.EVT_BUTTON, self.__delete_plugin, self.OkCancelSizerOK)


    def __delete_plugin(self, event):
        '''
        Deletes the specified plugin
        @return:
        '''
        selected_plugin = self.parent.plugins_tree.get_current_selection_text()

        self.__sdk.delete_plugin(selected_plugin)
        self.parent.plugins_tree.remove_plugin()

        self.parent.clear_config_fields()
        self.parent.Enable()
        self.Destroy()

