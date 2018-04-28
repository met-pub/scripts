-- turn on/off wifi

wifi_on_off()

on wifi_on_off()
    try
        set wifiStatus to do shell script "networksetup -getairportpower en0"
    on error
        display dialog "The script did not work as intended." buttons {"ok"}
    end try
    
    if wifiStatus is "Wi-Fi Power (en0): On" then
        do shell script "networksetup -setairportpower en0 off"
    else if wifiStatus is "Wi-Fi Power (en0): Off" then
        do shell script "networksetup -setairportpower en0 on"
    else
        display dialog "The script did not work as intended" buttons {"ok"}
    end if
end wifi_on_off
