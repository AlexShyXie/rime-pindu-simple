-- lua/super_processor.lua
-- @amzxyz (精简版：仅保留符号快打功能)
-- 用法: 在 schema.yaml 中 engine/processors 列表添加 - lua_processor@*super_processor

local M = {}
local K_REJECT, K_ACCEPT, K_NOOP = 0, 1, 2

-- [QuickSymbol] 默认符号映射表
local SYMBOL_DEFAULT = {
    q="：", w="？", e="（", r="）", t="~", y="·", u="『", i="』", o="〖", p="〗",
    a="！", s="……", d="、", f="“", g="”", h="‘", j="’", k="【", l="】",
    z="。", x="？", c="！", v="——", b="%", n="《", m="》"
}

-- 初始化函数
function M.init(env)
    local engine = env.engine
    local config = engine.schema.config
    local context = engine.context

    -- [QuickSymbol] 配置加载
    -- 默认触发规则：单字母+斜杠，如 a/
    env.qs_trigger = "^([a-z])/$"
    if config then
        local ok, s = pcall(function() return config:get_string("quick_symbol_text/trigger") end)
        if ok and type(s)=="string" and #s>0 then
            env.qs_trigger = s
        end
    end

    -- 加载符号映射表 (优先读取方案配置，否则使用默认)
    env.qs_mapping = {}
    for k, v in pairs(SYMBOL_DEFAULT) do
        env.qs_mapping[k] = v
    end
    
    local ok_map, map = pcall(function() return config:get_map("quick_symbol_text/symkey") end)
    if ok_map and map then
        local ok_keys, keys = pcall(function() return map:keys() end)
        if ok_keys and keys then
            for _, key in ipairs(keys) do
                local v = config:get_string("quick_symbol_text/symkey/" .. key)
                if v then
                    env.qs_mapping[tostring(key)] = v
                end
            end
        end
    end
    
    -- 记录最后一次上屏内容 (用于 repeat 功能)
    env.qs_last_commit = ""

    -- 监听输入更新，实现自动上屏
    env.conn_update = context.update_notifier:connect(function(ctx)
        local input = ctx.input or ""
        local qkey = string.match(input, env.qs_trigger)
        if qkey then
            local symbol = env.qs_mapping[qkey]
            if symbol and symbol ~= "" then
                -- 如果配置为 "repeat"，则重复上屏最后一次提交的内容
                if type(symbol)=="string" and symbol:lower()=="repeat" then
                    if env.qs_last_commit ~= "" then
                        engine:commit_text(env.qs_last_commit)
                        ctx:clear()
                    end
                else
                    -- 否则上屏对应的符号
                    engine:commit_text(symbol)
                    ctx:clear()
                end
            end
        end
    end)

    -- 监听上屏事件，记录最后上屏内容
    env.conn_commit = context.commit_notifier:connect(function(ctx)
        local t = ctx:get_commit_text()
        if t ~= "" then
            env.qs_last_commit = t
        end
    end)
end

-- 清理函数
function M.fini(env)
    if env.conn_update then
        env.conn_update:disconnect()
        env.conn_update = nil
    end
    if env.conn_commit then
        env.conn_commit:disconnect()
        env.conn_commit = nil
    end
end

-- 按键处理主入口
function M.func(key, env)
    local ctx = env.engine.context
    
    -- 1. 优先处理按键释放 (这里不做处理，直接放行)
    if key:release() then
        return K_NOOP
    end

    local kc = key.keycode

    -- 2. QuickSymbol 拦截逻辑
    -- 检测当前输入是否符合触发规则
    local input = ctx.input or ""
    -- 为了保证兼容性，我们检查当前输入是否处于快符触发的前置状态
    -- 例如：输入了 "a"，还没有按 "/" 之前，这里不做拦截
    -- 当 "/" 按下时，Update Notifier 会触发上屏，按键本身直接放行即可
    -- 但如果需要在按键阶段就拦截 '/' (防止某些方案将其视为编码)，可以取消下面注释：
    -- if string.char(kc) == "/" and string.match(input, "^[a-z]$") then
    --    return K_ACCEPT 
    -- end

    -- 其他所有按键均不拦截
    return K_NOOP
end

return M
