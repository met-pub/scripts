
local lastPoint  = nil
-- 跳到下一个屏幕的位置
hs.hotkey.bind(nil, 'F19', function()
	-- initial, set Mouse to center of next Monitor
	if (lastPoint == nil) then
	    local screen = hs.mouse.getCurrentScreen()
	    local nextScreen = screen:next()
	    local rect = nextScreen:fullFrame()
	    lastPoint = hs.geometry.rectMidPoint(rect)
	end
	
	local thisPoint = hs.mouse.getAbsolutePosition()
    hs.mouse.setAbsolutePosition(lastPoint)
    lastPoint = thisPoint
    -- k.triggered = true
end)
