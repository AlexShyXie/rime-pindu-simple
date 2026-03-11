-- 并击顶功处理器
-- 由于 Rime chord_composer 的特殊性，不能复用串击的顶功处理器

local snow = require "snow.snow"

local processor = {}

---@class ComboPoppingEnv: Env
---@field active boolean

---@param env ComboPoppingEnv
function processor.init(env)
  env.active = true
end

---@param key_event KeyEvent
---@param env ComboPoppingEnv
function processor.func(key_event, env)
  local context = env.engine.context
  
  -- 1. 过滤功能键和修饰键
  if key_event:release() or key_event:alt() or key_event:shift() or key_event:ctrl() or key_event:caps() then
      return snow.kNoop
  end


  -- 2. 关键修复：如果是删除键(Backspace)，直接返回，不进行顶屏判断
  -- 这样删除键才能正常工作，不会被误判为顶屏
  if key_event.keycode == 0xFF08 then -- 0xFF08 是 Backspace 的通用 keycode
    return snow.kNoop
  end

  local incoming = utf8.char(key_event.keycode)
  local input = snow.current(context) or ""

  -- 3. 符号和翻页键处理 (保持不变，这是对的)
  if rime_api.regex_match(incoming, "[`;/\\\\ ]+") then
    env.active = true
    return snow.kNoop
  end
  
  if rime_api.regex_match(incoming, "[7890]") then
    return snow.kNoop
  end

  -- 【核心修改】：判断是否为翻页键或方向键
  -- 方向键键码: Left=0xFF51, Up=0xFF52, Right=0xFF53, Down=0xFF54
  local is_navigation_key = (incoming == "-" or incoming == "=" or 
                             key_event.keycode == 0xFF51 or 
                             key_event.keycode == 0xFF52 or 
                             key_event.keycode == 0xFF53 or 
                             key_event.keycode == 0xFF54)

  -- 如果是功能键，并且当前正在输入中
  if is_navigation_key and context:is_composing() then
      -- 【关键点】直接返回，完全跳过后面的顶屏逻辑
      -- 这样按键就会顺利传给 key_binder 执行翻页或移动光标
      env.active=false
      return snow.kNoop
  end
  
  
  if env.active then
    -- 4. 修正后的正则：支持数字声调(7890)的顶屏逻辑
    -- 注意：以下正则假设前两位为基础双拼编码
    local match2, match3

    match2 = rime_api.regex_match(input, "^[a-z]{2}[7890]?[A-Z]{0,2}[a-z]{2}[7890]?[A-Z]{0,2}")

    match3 = rime_api.regex_match(input, "^[a-z]{2}[A-Z]{0,2}[7890]?[a-z]{2}[A-Z]{0,2}[7890]?")

    if match2 or match3 then
      context:confirm_current_selection()
      context:commit()
    end
  else
    -- 如果 active 为 false，在这里设为 true
    env.active = true
  end

  return snow.kNoop
end


return processor
