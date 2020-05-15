import cx_Freeze

executables = [cx_Freeze.Executable("main.py", base = "Win32GUI")]

cx_Freeze.setup(
    name="Tower Defence",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["arrow.png", "btnarrowleft.png", "btnarrowright.png", "btnback.png", "btnblank.png", "btnexit.png", "btnplay.png", "btnsettings.png", "bullet.png", "cursor.png", "enemy.png", "fpsoff.png", "fpson.png", "player.png", "tower.png", "towerplaceholder.png", "towerplaceholder_mouseover.png"]}},
    executables = executables

    )