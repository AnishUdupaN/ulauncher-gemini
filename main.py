from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent, PreferencesEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
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
        fpref = extension.preferences.get("preference", False)
        api_key=extension.preferences.get("gemini_api_key")
        stringinput = event.get_argument() or ""
        if fpref == 'man':
            pref = extension.preferences.get("first_preference", "ul")
            if pref=="ul":
                pref=[[True,"Click to Search Here"],[False,"Click to Notify the result.."]]
            else:
                pref=[[False,"Click to Notify the result!!"],[True,"Click to Search Here"]]
            items.append(ExtensionResultItem(
                icon='icon.png',
                name=stringinput,
                description=pref[0][1],
                on_enter=ExtensionCustomAction({'api_key':api_key,'query':stringinput,'ul':pref[0][0],'auto':False}, keep_app_open=pref[0][0])
            ))
            items.append(ExtensionResultItem(
                icon='icon.png',
                name=stringinput,
                description=pref[1][1],
                on_enter=ExtensionCustomAction({'api_key':api_key,'query':stringinput,'ul':pref[1][0],'auto':False}, keep_app_open=pref[1][0])
            ))
            return RenderResultListAction(items[:2])
        else:
            items.append(ExtensionResultItem(
                icon='icon.png',
                name=stringinput,
                description='Click to Get Answer',
                on_enter=ExtensionCustomAction({'api_key':api_key,'query':stringinput,'ul':False,'auto':True}, keep_app_open=True)
            ))
            return RenderResultListAction(items[:1])


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        data = event.get_data()
        query=data['query']
        api_key=data['api_key']
        result=gemini.ask_gemini(api_key,query)
        #result='Google'
        if data['auto']==False:
            if data['ul']:
                items.append(ExtensionResultItem(
                    icon='icon.png',
                    name=query+'\n'+result,
                    on_enter=HideWindowAction()
                ))
                return RenderResultListAction(items[:1])
            else:
                notify2.init("Gemini Answers!")
                notification = notify2.Notification(query,result)
                notification.show()
        else:
            if len(result)<=32:
                items.append(ExtensionResultItem(
                    icon='icon.png',
                    name=query+'\n'+result,
                    on_enter=HideWindowAction()
                ))
                return RenderResultListAction(items[:1])
            else:
                notify2.init("Gemini Answers!")
                notification = notify2.Notification(query,result)
                notification.show()



if __name__ == '__main__':
    MyExtension().run()
