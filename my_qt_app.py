import requests, sys, subprocess
import platform
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox

# Replace with your GitHub username and repository name
GITHUB_USERNAME = "malikcodergreen"
REPOSITORY_NAME = "version_updater_app"

# URL for the version info file
VERSION_INFO_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}/master/version_info.txt"


def check_for_updates():
    try:
        response = requests.get(VERSION_INFO_URL)
        latest_version = response.text.strip()

        # Replace with your logic to get current version (e.g., from a file)
        version_file = "version_info.txt"
        try:
            with open(version_file, "r") as file:
                current_version = file.readline().strip()
        except IOError:
            raise IOError(f"Error opening version file: {version_file}")
    
        # Display an error message to the user
        if latest_version != current_version:
            message_box = QMessageBox()
            message_box.setWindowTitle("Update Available")
            message_box.setText(f"A new version ({latest_version}) is available! You're currently on version {current_version}.")
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            try:
                # Replace with your Git repository URL
                repo_url = f"https://github.com/{GITHUB_USERNAME}/{REPOSITORY_NAME}.git"
                if message_box.exec_() == QMessageBox.Yes:
                    subprocess.run(["git", "pull", repo_url])
                    # Option 1: Restart using a separate script (recommended)
                    # Create a separate script (e.g., restart.bat or restart.sh) to relaunch the application
                    if platform.system() == "Windows":
                        subprocess.run(["path/to/restart.bat"])  # Windows example
                    else:
                        subprocess.run(["path/to/restart.sh"])  # Linux/macOS example
                        print("Update pulled successfully. Restarting application...")
                else:
                    print("User declined update")
            except subprocess.CalledProcessError as e:
                print(e.output)
            

            
            # Add an optional "Remind Later" button (custom button)
            # remind_later_button = message_box.addButton("Remind Later", QMessageBox.NoRole)
            # You can connect a signal to this button for later reminder functionality

            ret = message_box.exec_()

            if ret == QMessageBox.Yes:
                # Handle update download/installation logic here (refer to previous explanation)
                print("User chose to update. Implement update logic here.")

    except requests.exceptions.RequestException as e:
        print(f"Error checking for updates: {e}")


class HelloWorld(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Hello Wurld!")

        # Create a label widget
        self.label = QLabel("Hello Wurld!", self)

        # Center the label in the window
        self.label.setAlignment(Qt.AlignCenter)

        # Set the window size
        self.resize(400, 300)

        # Schedule update check every minute
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(60000)  # Milliseconds in a minute
        self.update_timer.timeout.connect(check_for_updates)
        self.update_timer.start()

        # Show the widget (make the window visible)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = HelloWorld()
    sys.exit(app.exec_())

