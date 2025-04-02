from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class HyperlinkButton(QPushButton):
    def __init__(self, text, url, parent=None):
        super().__init__(text, parent)
        self.url = url
        self.clicked.connect(self.open_url)
        self.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")

    def open_url(self):
        QDesktopServices.openUrl(QUrl(self.url))


class AboutMessage(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setText("AstroLab v0.4\n\n AstroLab is a Python-based application designed for astronomy enthusiasts.\n\n"
                     )

        self.setIcon(QMessageBox.Information)

        # Create a hyperlink button
        link_button = HyperlinkButton("Visit GitHub Repo", "https://github.com/Yedi278/AstroLab", self)
        self.addButton(link_button, QMessageBox.AcceptRole)

        # Add an OK button
        ok_button = self.addButton(QMessageBox.Ok)
        ok_button.setText("OK")

        


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    about_message = AboutMessage()
    about_message.exec_()
    sys.exit(app.exec_())