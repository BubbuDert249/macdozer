import os
import shutil

class MacDozer:
    def __init__(self):
        self.app_path = None
        self.app_name = "ExampleApp"
        self.app_desc = "An example Mac app"
        self.app_dev = "Developer"
        self.app_ver = "1.0"
        self.script_content = None
        self.script_file_path = None
        self.icon_file_path = None

    def appcreate(self, path):
        self.app_path = os.path.join(path, self.app_name + ".app")
        contents = os.path.join(self.app_path, "Contents")
        macos = os.path.join(contents, "MacOS")
        resources = os.path.join(contents, "Resources")

        # Create directories
        for d in [self.app_path, contents, macos, resources]:
            if not os.path.exists(d):
                os.mkdir(d)

        # Create run.sh in MacOS
        run_sh = os.path.join(macos, "run.sh")
        with open(run_sh, "w") as f:
            f.write("#!/bin/sh\n")
            f.write('DIR="$(cd "$(dirname "$0")" && pwd)"\n')
            f.write('osascript "$DIR/../Resources/Script.applescript"\n')

        print(f"App structure created at: {self.app_path}")
        print("Don't forget to chmod +x run.sh manually!")

        # Write plist now
        self._write_plist()

        # Write script if given
        if self.script_content:
            self.script(script=self.script_content)
        elif self.script_file_path:
            self.scriptfile(self.script_file_path)

        # Copy icon if given
        if self.icon_file_path:
            self.icon(self.icon_file_path)

    def appname(self, name):
        self.app_name = name
        if self.app_path:
            # Update app folder name and plist
            base_path = os.path.dirname(os.path.dirname(self.app_path))
            new_app_path = os.path.join(base_path, self.app_name + ".app")
            if self.app_path != new_app_path:
                os.rename(self.app_path, new_app_path)
                self.app_path = new_app_path
            self._write_plist()

    def appdesc(self, desc):
        self.app_desc = desc
        if self.app_path:
            self._write_plist()

    def appdev(self, dev):
        self.app_dev = dev
        if self.app_path:
            self._write_plist()

    def appver(self, ver):
        self.app_ver = ver
        if self.app_path:
            self._write_plist()

    def scriptfile(self, file_path):
        if not self.app_path:
            raise Exception("Create app first with appcreate()")

        resources = os.path.join(self.app_path, "Contents", "Resources")
        dest = os.path.join(resources, "Script.applescript")

        shutil.copyfile(file_path, dest)
        print(f"Copied AppleScript from {file_path} to {dest}")

    def script(self, script):
        if not self.app_path:
            raise Exception("Create app first with appcreate()")

        resources = os.path.join(self.app_path, "Contents", "Resources")
        dest = os.path.join(resources, "Script.applescript")

        with open(dest, "w") as f:
            f.write(script)
        print(f"Wrote AppleScript to {dest}")

    def icon(self, icon_path):
        if not self.app_path:
            raise Exception("Create app first with appcreate()")

        resources = os.path.join(self.app_path, "Contents", "Resources")
        dest = os.path.join(resources, "icon.icns")

        shutil.copyfile(icon_path, dest)
        print(f"Copied icon file to {dest}")

        self._write_plist()

    def _write_plist(self):
        if not self.app_path:
            return

        contents = os.path.join(self.app_path, "Contents")
        plist_path = os.path.join(contents, "Info.plist")

        # Identifier org.{dev}.{appname}
        identifier = f"org.{self.app_dev.replace(' ', '')}.{self.app_name.replace(' ', '')}"

        # Start building plist XML manually
        plist_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>{self.app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>{identifier}</string>
    <key>CFBundleVersion</key>
    <string>{self.app_ver}</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.app_ver}</string>
    <key>CFBundleExecutable</key>
    <string>run.sh</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>'''

        # Add icon only if icon file exists
        icon_file = os.path.join(self.app_path, "Contents", "Resources", "icon.icns")
        if os.path.isfile(icon_file):
            plist_xml += '''
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>'''

        plist_xml += '''
</dict>
</plist>'''

        with open(plist_path, "w", encoding="utf-8") as f:
            f.write(plist_xml)

        print(f"Wrote Info.plist at {plist_path}")
