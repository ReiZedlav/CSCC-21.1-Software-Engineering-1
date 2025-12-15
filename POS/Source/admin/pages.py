
class Pages:
    @staticmethod
    def gotoPromotions(session,widget):
        from admin.promotions import Promotions
        panel = Promotions(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoLogs(session,widget):
        from admin.logging import Logging
        panel = Logging(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoInventoryEdit(session,widget,productId):
        from admin.inventory.inventory_edit import InventoryEdit
        panel = InventoryEdit(session,widget,productId)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoInventoryAdd(session,widget):
        from admin.inventory.inventory_add import InventoryAdd
        panel = InventoryAdd(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoInventoryIcons(session,widget):
        from admin.inventory.inventory_icons import InventoryIcons
        panel = InventoryIcons(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoInventoryProduct(session,widget):
        from admin.inventory.inventory_product import InventoryProduct
        panel = InventoryProduct(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    @staticmethod
    def gotoStatistics(session,widget):
        from admin.statistics import Statistics
        panel = Statistics(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    @staticmethod
    def gotoEmployees(session,widget):
        from admin.employees.employees import Employees
        panel = Employees(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoAddEmployee(session,widget):
        from admin.employees.add_employee import AddEmployee
        panel = AddEmployee(session,widget)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def gotoEditEmployee(session,widget,cashierId):
        from admin.employees.edit_employee import EditEmployee
        panel = EditEmployee(session,widget,cashierId)
        widget.addWidget(panel)
        widget.setCurrentIndex(widget.currentIndex() + 1)



