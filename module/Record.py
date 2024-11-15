from utils import inputChecker, strIsEmpty, strToFloat, rangeIntToString
from module.Menu import Menu
from enumeration.MenuName import MenuName
from enumeration.RecordType import RecordType
from enumeration.CheckType import CheckType

import configparser


class Record:
    def __init__(self):
        # 初始化所有属性
        self.type = None
        self.date = None
        self.id = None
        self.varietyCoal = None
        self.plateNumber = None
        self.grossWeight = None
        self.tare = None
        self.netWeight = None
        self.primary = None
        self.profitLoss = None
        self.emptyTime = None
        self.excessiveTime = None
        self.shippingUnit = None
        self.receivingUnit = None
        self.weigher = None
        self.creatTime = None
        self.modifyTime = None

        self.isGenerateImage = False
        self.image = None
        self.sheetName = None

        self.methodMapping = {
            '1': self.setDate,
            '2': self.setVarietyCoal,
            '3': self.setPlateNumber,
            '4': self.setGrossWeight,
            '5': self.setTare,
            '6': self.setPrimary,
            '7': self.setEmptyTime,
            '8': self.setExcessiveTime,
            '9': self.setShippingUnit,
            '10': self.setReceivingUnit,
            '11': self.setWeigher
        }

    # 读取配置信息，设置默认值
    def setDefault(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        for attr in self.__dict__:
            value = config.get('InputData', attr, fallback=None)
            if value is not None:
                setattr(self, attr, value)

    def setAttribute(self, attr, prompt, data_type):

        current_value = getattr(self, attr)
        if current_value is None:
            value = inputChecker(CheckType.DATATYPE, data_type, prompt)
            if strIsEmpty(value):
                print(f"输入数据为空，如要修改请按q键，返回主页进行修改")
            setattr(self, attr, value)
        else:
            value = inputChecker(CheckType.DATATYPE, data_type, f'已有设置: {current_value} ，按下enter确定此设置，或输入其他内容以覆盖默认设置：')
            if not strIsEmpty(value):
                setattr(self, attr, value)

    def setType(self):
        Menu.show(MenuName.RECORDTYPE)
        value = inputChecker(CheckType.OPTIONTYPE, ['1', '2'], '请输入类型序号：') 
        if value == '1':
            self.sheetName = '入'
            self.type = RecordType.INCOME
        elif value == '2':
            self.sheetName = '出'
            self.type = RecordType.EXPENSE

    def setDate(self):
        self.setAttribute('date', '请输入日期：', str)

    def setVarietyCoal(self):
        self.setAttribute('varietyCoal', '请输入煤种：', str)

    def setPlateNumber(self):
        self.setAttribute('plateNumber', '请输入车牌号：', str)

    def setGrossWeight(self):
        self.setAttribute('grossWeight', '请输入毛重：', float)

    def setTare(self):
        self.setAttribute('tare', '请输入皮重：', float)

    def setPrimary(self):
        self.setAttribute('primary', '请输入原发：', str)

    def setEmptyTime(self):
        self.setAttribute('emptyTime', '请输入过空时间：', str)

    def setExcessiveTime(self):
        self.setAttribute('excessiveTime', '请输入过重时间：', str)

    def setShippingUnit(self):
        self.setAttribute('shippingUnit', '请输入发货站：', str)

    def setReceivingUnit(self):
        self.setAttribute('receivingUnit', '请输入收货站：', str)

    def setWeigher(self):
        self.setAttribute('weigher', '请输入过磅员：', str)

    # 计算净重
    def calculateNetWeight(self):
        grossWeight = strToFloat(self.grossWeight)
        tare = strToFloat(self.tare)
        if grossWeight is not None and tare is not None:
            netWeight = grossWeight - tare
        else:
            netWeight = None
        self.netWeight = netWeight

    # 计算盈亏
    def calculateProfitLoss(self):
        netWeight = strToFloat(self.netWeight)
        primary = strToFloat(self.primary)
        if netWeight is not None and primary is not None:
            profitLoss = netWeight - primary
        else:
            profitLoss = None
        self.profitLoss = profitLoss

    def __str__(self):
        recordType = ''
        if self.type == RecordType.INCOME:
            recordType = '入库记录'
        elif self.type == RecordType.EXPENSE:
            recordType = '出库记录'
        else:
            recordType = '未知记录'

        return (f"Record(出入库类型={recordType},  日期={self.date}, 磅单编号={self.id}, 煤种={self.varietyCoal}, "
                f"车牌号={self.plateNumber}, 毛重={self.grossWeight}, 皮重={self.tare}, "
                f"净重={self.netWeight}, 原发={self.primary}, 盈亏={self.profitLoss}, "
                f"过空时间={self.emptyTime}, 过重时间={self.excessiveTime}, 供货站={self.shippingUnit}, "
                f"收货站={self.receivingUnit}, 司磅员={self.weigher}, 创建时间={self.creatTime}, "
                f"修改时间={self.modifyTime})")
