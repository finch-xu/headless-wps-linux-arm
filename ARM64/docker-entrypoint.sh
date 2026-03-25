#!/bin/bash
set -e

# WPS 路径
WPS_DIR="/opt/kingsoft/wps-office/office6"
export LD_LIBRARY_PATH="${WPS_DIR}:${LD_LIBRARY_PATH}"
export DISPLAY=:99
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p "$XDG_RUNTIME_DIR" && chmod 0700 "$XDG_RUNTIME_DIR"

# 启动 D-Bus session（WPS RPC 需要）
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval $(dbus-launch --sh-syntax 2>/dev/null) || true
    export DBUS_SESSION_BUS_ADDRESS
fi

# 启动 Xvfb 虚拟显示器
if ! pgrep -x Xvfb > /dev/null 2>&1; then
    Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
    for i in $(seq 1 50); do
        xdpyinfo -display :99 > /dev/null 2>&1 && break
        sleep 0.1
    done
fi

exec "$@"
