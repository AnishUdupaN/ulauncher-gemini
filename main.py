import subprocess
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

class ClipboardHistoryExtension(Extension):
    def __init__(self):
        super(ClipboardHistoryExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        persistent = extension.preferences.get("persistent", False)
        stringinput = event.get_argument() or ""
        items.append(ExtensionResultItem(
            icon=os.path.join(os.getcwd(),'images/icon.png'),
            name='Hello World',
            description="Click to Open",
            on_enter=RunScriptAction(f'xdg-open "Hello World"', [])
        ))
        return RenderResultListAction(items[:1])

if __name__ == '__main__':
    ClipboardHistoryExtension().run()
