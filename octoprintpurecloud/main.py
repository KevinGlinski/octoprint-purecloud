# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests
import json

class OctoprintPurecloudPlugin(octoprint.plugin.ProgressPlugin,
                        octoprint.plugin.SettingsPlugin):

    running_print = ""                    
    
    def on_print_progress(self, storage, path, progress):
        if progress == 0 and self.running_print != path:
            self.send_web_hook("Print " + path + " complete")
            self.running_print = path

        if progress == 100 and self.running_print == path:
            self.send_web_hook("Print " + path + " complete")
            self.running_print = ""
  
    def get_settings_defaults(self):
        return dict(webhook_uri="", printer_name="")


    def send_web_hook(self, message):
        url = self._settings.get(["webhook_uri"])

        payload = json.dumps({
            message: message,
            metadata: self._settings.get(["printer_name"])
        })

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
    
__plugin_name__ = "PureCloud Chat Notifications"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Sends chat notifications to PureCloud rooms"
__plugin_implementation__ = OctoprintPurecloudPlugin()        