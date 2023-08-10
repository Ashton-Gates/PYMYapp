from pyupdater.client import Client

def check_for_updates():
    client = Client("<your-config-here>")
    app_update = client.update_check("<app-name>", "<current-version>")

    if app_update is not None:
        app_update.download()
        if app_update.is_downloaded():
            app_update.extract_restart()
