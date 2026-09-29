# Unofficial Linux repack of Cue's platform-independent Electron application.
pkgname=cue-linux
pkgver=1.0.1
pkgrel=2
pkgdesc='Cue desktop client (unofficial Linux repack with bundled Electron)'
arch=('x86_64' 'aarch64')
url='https://cue.im'
license=('LicenseRef-proprietary')
depends=('alsa-lib' 'at-spi2-core' 'cairo' 'dbus' 'expat' 'gcc-libs' 'glib2'
         'glibc' 'gtk3' 'libcups' 'libdrm' 'libx11' 'libxcb' 'libxcomposite'
         'libxdamage' 'libxext' 'libxfixes' 'libxkbcommon' 'libxrandr' 'mesa'
         'nspr' 'nss' 'pango' 'xdg-utils')
makedepends=('7zip' 'python' 'unzip')
optdepends=('gnome-keyring: credential storage via Secret Service'
            'libnotify: desktop notifications')
provides=('cue')
conflicts=('cue')
# Do not strip Chromium or produce a very large, useless debug package.
options=('!strip' '!debug')
_electron=43.6.0
source=("https://download.cue.im/Cue-${pkgver}-mac-arm64.dmg"
        'cue' 'cue-desktop.desktop' 'extract-icon.py')
source_x86_64=("https://github.com/electron/electron/releases/download/v${_electron}/electron-v${_electron}-linux-x64.zip")
source_aarch64=("https://github.com/electron/electron/releases/download/v${_electron}/electron-v${_electron}-linux-arm64.zip")
noextract=("Cue-${pkgver}-mac-arm64.dmg"
           "electron-v${_electron}-linux-x64.zip"
           "electron-v${_electron}-linux-arm64.zip")
sha256sums=('55ee16923e73911d3f7b63f2e8e4e736f0a564503e0e778654e7ff8c6c112eb9'
            'SKIP' 'SKIP' 'SKIP')
sha256sums_x86_64=('3075c82d0749e136bca77563d4dd24e881714d17d98241fafd02320da5d6e237')
sha256sums_aarch64=('e8b4ef7acdfb3f254463f832dded44c17cb8c65f790d0377e8c04f91bbeeb3a4')

prepare() {
    local electron_arch=x64
    [[ $CARCH == aarch64 ]] && electron_arch=arm64
    mkdir -p "$srcdir/dmg" "$srcdir/electron"
    7z x -y -o"$srcdir/dmg" "$srcdir/Cue-${pkgver}-mac-arm64.dmg" \
        "Cue ${pkgver}-arm64/Cue.app/Contents/Resources/app.asar" \
        "Cue ${pkgver}-arm64/Cue.app/Contents/Resources/icon.icns"
    unzip -q -o "$srcdir/electron-v${_electron}-linux-${electron_arch}.zip" -d "$srcdir/electron"
    python "$srcdir/extract-icon.py" \
        "$srcdir/dmg/Cue ${pkgver}-arm64/Cue.app/Contents/Resources/icon.icns" \
        "$srcdir/cue.png"
}

package() {
    local resources="$srcdir/dmg/Cue ${pkgver}-arm64/Cue.app/Contents/Resources"
    install -d "$pkgdir/opt/cue" "$pkgdir/usr/share/licenses/$pkgname"
    cp -a "$srcdir/electron/." "$pkgdir/opt/cue/"
    mv "$pkgdir/opt/cue/electron" "$pkgdir/opt/cue/cue"
    rm "$pkgdir/opt/cue/resources/default_app.asar"
    install -m644 "$resources/app.asar" "$pkgdir/opt/cue/resources/app.asar"
    # Preserve Chromium's sandbox; never launch the app with --no-sandbox.
    chmod 4755 "$pkgdir/opt/cue/chrome-sandbox"
    install -Dm755 "$srcdir/cue" "$pkgdir/usr/bin/cue"
    # Electron derives this filename from app.asar/package.json's name.
    install -Dm644 "$srcdir/cue-desktop.desktop" "$pkgdir/usr/share/applications/cue-desktop.desktop"
    install -Dm644 "$srcdir/cue.png" "$pkgdir/usr/share/icons/hicolor/512x512/apps/cue.png"
    install -m644 "$srcdir/electron/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE.electron"
    install -m644 "$srcdir/electron/LICENSES.chromium.html" "$pkgdir/usr/share/licenses/$pkgname/"
}
