from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel
from qfluentwidgets import ScrollArea, ExpandLayout, Pivot, SettingCardGroup, PushSettingCard, ComboBoxSettingCard

from app_front.card.comboboxsettingcard1 import ComboBoxSettingCard1
from qfluentwidgets import FluentIcon as FIF

from app_front.card.switchsettingcard import SwitchSettingCard1
from app_front.common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """ Setting interface """

    Nav = Pivot

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.pivot = self.Nav(self)
        # 堆叠部件
        self.stackedWidget = QStackedWidget(self)

        self.settingLabel = QLabel(self.tr("设置"), self)
        # 程序设置组
        self.ProgramGroup = SettingCardGroup(self.tr('程序设置'), self.scrollWidget)
        self.gamePathCard = PushSettingCard(
            self.tr('修改'),
            FIF.GAME,
            self.tr("游戏路径"),
            'D:\game\\xxx\\xxx'
        )
        self.checkUpdateCard = SwitchSettingCard1(
            FIF.UPDATE,
            self.tr('启动时检测更新'),
            "新版本将更加稳定并拥有更多功能（建议启用）",
            "check_update"
        )
        # 刷体力设置组
        self.PowerGroup = SettingCardGroup(self.tr('体力设置'), self.scrollWidget)
        self.instanceTypeCard = ComboBoxSettingCard1(
            "instance_type",
            FIF.ALIGNMENT,
            self.tr('副本类型'),
            None,
            texts=['5-5', '临界深渊']
        )
        self.doubleEnableCard = SwitchSettingCard1(
            FIF.EDIT,
            self.tr('使用双倍体力'),
            None,
            "double_enable"
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        # self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(10, 20)
        # 将卡片添加入对应分组中
        self.ProgramGroup.addSettingCard(self.gamePathCard)
        self.ProgramGroup.addSettingCard(self.checkUpdateCard)

        self.PowerGroup.addSettingCard(self.instanceTypeCard)
        self.PowerGroup.addSettingCard(self.doubleEnableCard)

        self.ProgramGroup.titleLabel.setHidden(True)
        self.PowerGroup.titleLabel.setHidden(True)

        self.addSubInterface(self.ProgramGroup, 'programInterface', self.tr('程序'))
        self.addSubInterface(self.PowerGroup, 'PowerInterface', self.tr('体力'))
        # 将子菜单添加进页面，并设置好锚点
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )
