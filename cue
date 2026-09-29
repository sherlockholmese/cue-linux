#!/bin/sh
# Electron uses this desktop filename for Linux protocol registration.
export CHROME_DESKTOP=cue-desktop.desktop
exec /opt/cue/cue "$@"
