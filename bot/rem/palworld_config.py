import os


class PalworldConfig():
    def __init__(self):
        self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.palworld_server_path = os.path.join(self.desktop_path, 'palworld_server')
        self.palworld_backup_folder_name = "palworld_server_saved"
        self.palworld_backup_parent = "D:/"
        self.palworld_backup_path = os.path.join(self.palworld_backup_parent, 'palworld_backup')
        self.palworld_game_base_path = os.path.join(self.palworld_server_path, "steamapps", "common", "PalServer")
        self.palworld_game_saved_path = os.path.join(self.palworld_game_base_path, "Pal", "Saved")
        self.palworld_server_proc_name = "PalServer-Win64-Test-Cmd.exe"
        self.rotate_backups = True,
        