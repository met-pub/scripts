-- run/quit Karabiner-Elements

ke_on_off()

on ke_on_off()
    set ke to " gui/`id -u`/org.pqrs.karabiner.karabiner_console_user_server"
    set isrun to false
    try
        do shell script "launchctl print" & ke
        set isrun to true
    end try
    if isrun then
        do shell script "launchctl bootout" & ke & "; launchctl disable" & ke
        do shell script "kill $(pgrep Karabiner-Menu)"
    else
        do shell script "launchctl enable" & ke
        launch application "/Applications/Karabiner-Elements.app/Contents/MacOS/Karabiner-Elements"
        delay 1
    end if
    -- 杀掉配置界面
    try
        do shell script "kill $(pgrep Karabiner-Elements)"
    end try
end ke_on_off
