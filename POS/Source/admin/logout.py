class LogoutHandler:
    @staticmethod
    def logout(widget):
        """
        Simple one-click logout that goes back to login page
        """
        from main import Login
        login_window = Login()
        
        # Clear the widget stack and add login window
        widget.clear()
        widget.addWidget(login_window)
        widget.setCurrentIndex(0)