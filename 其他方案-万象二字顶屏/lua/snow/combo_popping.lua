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

  local input = snow.current(context) or ""
  local incoming = utf8.char(key_event.keycode)

  -- 3. 如果包含特殊符号，不限制，直接放行
  -- 2. 【关键修改】优先判断符号，直接放行并重置状态
  -- 使用 incoming 匹配当前按键，而不是 input
  if rime_api.regex_match(incoming, "[`;/\\\\ ]+") then
    env.active = true  -- 恢复初始状态，准备下一次输入
    return snow.kNoop  -- 放行，让 Rime 默认处理这个符号
  end
  if rime_api.regex_match(incoming, "[7890]") then
      return snow.kNoop
  end
  if env.active then
    -- 4. 修正后的正则：支持数字声调(7890)的顶屏逻辑
    -- 注意：以下正则假设前两位为基础双拼编码
    local match1, match2, match3

    match1 = rime_api.regex_match(input, "^[a-z]{2}[7890]?[a-z]{2}[7890]?")

    match2 = rime_api.regex_match(input, "^[a-z]{2}[7890]?[A-Z]?[a-z]{2}[7890]?[A-Z]?")

    match3 = rime_api.regex_match(input, "^[a-z]{2}[A-Z]?[7890]?[a-z]{2}[A-Z]?[7890]?")


    if match1 or match2 or match3 then
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
