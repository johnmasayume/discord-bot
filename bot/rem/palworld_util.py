import os
import shutil
import psutil
import subprocess
from rcon import SourceRcon
from datetime import datetime
from pathlib import Path
from palworld_config import PalworldConfig


palworld_config = PalworldConfig()


def rcon_save(rcon: SourceRcon):
    response = rcon.send_command("Save")
    return response


def rcon_do_exit(rcon: SourceRcon):
    response = rcon.send_command("DoExit")
    return response


def rcon_show_players(rcon: SourceRcon):
    response = rcon.send_command("ShowPlayers", [])
    return response


def rcon_broadcast_message(rcon: SourceRcon, message):
    response = rcon.send_command("Broadcast", [message])
    return response


def rcon_info(rcon: SourceRcon):
    response = rcon.send_command("Info", [])
    return response


def get_process_resource(process_name):
    # Get all processes
    all_processes = psutil.process_iter()

    # Search for the process with the specified name
    target_process = None
    for process in all_processes:
        if process.name() == process_name:
            target_process = process
            break

    if target_process is not None:
        return target_process

    return None


def check_for_process(process_name: str) -> bool:
    return process_name in (p.name() for p in psutil.process_iter())


def kill_process(process_name: str) -> None:
    for p in psutil.process_iter():
        if p.name() == process_name:
            p.kill()


def save_server_state(rcon: SourceRcon) -> bool:
    if check_for_process(palworld_config.palworld_server_proc_name):
        SAVE_FINISHED_RESPONSE = "Complete Save"

        print("Saving game state for Palworld server.")
        response = rcon_save(rcon)
        if response.strip() == SAVE_FINISHED_RESPONSE:
            print("Palworld server save game state finished.")
            return True
        else:
            print("Palworld server save game state failed!")
            return False

    return False


def server_backup(
        palworld_backup_path,
        palworld_backup_folder_name,
        palworld_game_saved_path,
        timestamp_format: str = "%Y%m%d_%H%M%S",
        rotate_backups=True
):
    timestamp = datetime.now().strftime(timestamp_format)
    destination_folder = os.path.join(
        palworld_backup_path,
        os.path.basename(palworld_backup_folder_name) + "_" + timestamp,
    )

    print(f"Copying: {palworld_game_saved_path} -> {destination_folder}")
    shutil.copytree(palworld_game_saved_path, destination_folder)

    if rotate_backups:
        _rotate_backups(palworld_backup_path)


def _rotate_backups(palworld_backup_path, delete_after_backups=200):
    path_backup = Path(palworld_backup_path)
    backups = sorted(list(path_backup.iterdir()), key=os.path.getmtime)

    # Keep only the newest backups
    if len(backups) > delete_after_backups:
        backups_to_delete = backups[:-delete_after_backups]

        for backup in backups_to_delete:
            if backup.is_dir():
                shutil.rmtree(backup)
                print(f"Deleted old backup: {backup}")


def update_game_server(steamcmd_executable, steam_app_id, palworld_server_path, start_new_session):
        print("Checking for game Palworld server updates...")
        subprocess.call(
            [
                steamcmd_executable,
                "+login",
                "anonymous",
                "+app_update",
                steam_app_id,
                "validate",
                "+quit",
            ],
            cwd=palworld_server_path,
            start_new_session=start_new_session,
            shell=not start_new_session,
        )


def launch_server(
    palworld_server_path,
    update_server: bool = True,
    wait_for_rcon_port: bool = False,
    wait_for_rcon_port_timeout: int = 10,
) -> bool:
    server_launch_args = []
    server_name = "Eggplant Palworld Server"
    server_port = 8211
    max_players = 10
    steamcmd_executable = "steamcmd.exe"
    palserver_executable = "PalServer.exe"
    steam_app_id: str = "2394010"
    start_new_session = False
    server_launch_args.append("start")
    server_launch_args.append(palserver_executable)
    server_launch_args.append(f"-ServerName={server_name}")
    server_launch_args.append(f"-port={server_port}")
    server_launch_args.append(f"-players={max_players}")
    server_launch_args.append("-log")
    server_launch_args.append("-nosteam")
    server_launch_args.append("-useperfthreads")
    server_launch_args.append("-NoAsyncLoadingThread")
    server_launch_args.append("-UseMultithreadForDS")


    # Check for server updates before launching.
    if update_server:
        update_game_server(steamcmd_executable, steam_app_id, palworld_server_path, start_new_session)
    else:
        print("Skipping game Palworld server updates.")

    print(
        f"Launching {palserver_executable} : {server_launch_args}..."
    )
    subprocess.Popen(
        server_launch_args,
        cwd=os.path.join(
            palworld_server_path, "steamapps", "common", "PalServer"
        ),
        start_new_session=start_new_session,
        shell=not start_new_session,
    )


def restart_server(
    rcon: SourceRcon,
    palworld_backup_path,
    palworld_backup_folder_name,
    palworld_game_saved_path,
    palworld_server_path,
    save_game: bool = True,
    check_for_server_updates: bool = True,
    backup_server: bool = True,
    wait_for_rcon_port: bool = False,
    wait_for_rcon_port_timeout: int = 10,
):
    print("Palworld Server restart process started.")

    # Save game state if needed.
    if save_game:
        saved_server = save_server_state(rcon)

    print("Restarting Palworld server now.")

    if saved_server:
        print("Ending palworld server process.")
        kill_process(palworld_config.palworld_server_proc_name)
    else:
        print("Palworld server might not be running, not saved and no process to kill")

    # Take backup of server if needed.
    if backup_server and saved_server:
        server_backup(palworld_backup_path, palworld_backup_folder_name, palworld_game_saved_path)
    else:
        print("Skipping Palworld server backup.")

    # Launch server.
    launch_server(
        palworld_server_path,
        update_server=check_for_server_updates,
        wait_for_rcon_port=wait_for_rcon_port,
        wait_for_rcon_port_timeout=wait_for_rcon_port_timeout,
    )