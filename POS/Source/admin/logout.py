class LogoutHandler:
    @staticmethod
    def logout(widget):
        """
        Logout by going back to the first widget (login screen)
        """
        # Go back to first widget (login screen)
        widget.setCurrentIndex(0)
        
        # Clear all other widgets (admin/cashier panels)
        while widget.count() > 1:
            widget.removeWidget(widget.widget(1))
        
        # Get the login widget and clear fields
        login_widget = widget.widget(0)
        if hasattr(login_widget, 'usernameField'):
            login_widget.usernameField.clear()
        if hasattr(login_widget, 'passwordField'):
            login_widget.passwordField.clear()
        
        # Reset window size and title
        widget.setWindowTitle("POS System")
        widget.setFixedSize(569, 299)
        widget.setGeometry(569, 299, 800, 400)