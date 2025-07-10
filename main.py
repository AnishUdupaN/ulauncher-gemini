from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import gemini
import notify2
import os
 
class MyExtension(Extension):
    def __init__(self):
        super(MyExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences.update(event.preferences)


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        extension.preferences[event.id] = event.new_value


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        pref = extension.preferences.get("persistent", False)
        if pref is True:
            pref=[[True,"Click to Search Here"],[False,"Click to Notify the result.."]]
        else:
            pref=[[False,"Click to Notify the result!!"],[True,"Click to Search Here"]]
        stringinput = event.get_argument() or ""

        items.append(ExtensionResultItem(
            icon=os.path.join(os.getcwd(),'images/icon.png'),
            name=stringinput,
            description=pref[0][1],
            on_enter=ExtensionCustomAction({'query':stringinput,'ul':pref[0][0]}, keep_app_open=pref[0][0])
        ))
        items.append(ExtensionResultItem(
            icon=os.path.join(os.getcwd(),'images/icon.png'),
            name=stringinput,
            description=pref[1][1],
            on_enter=ExtensionCustomAction({'query':stringinput,'ul':pref[1][0]}, keep_app_open=pref[1][0])
        ))
        return RenderResultListAction(items[:1])


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        print('EnterEventListener')
        data = event.get_data()
        query=data['query']
        #result=gemini.ask_gemini(query)
        result='Google'
        if data['ul']:
            items.append(ExtensionResultItem(
                icon='./images/icon.png',
                name=query+'\n'+result,
                on_enter=DoNothingAction()
            ))
            return RenderResultListAction(items[:1])
        else:
            notify2.init("Gemini Answers!")
            notification = notify2.Notification(query,result)
            notification.show()



if __name__ == '__main__':
    with open('./main.py','r') as fii:
        print(fii.read())
        fii.close()
    MyExtension().run()
