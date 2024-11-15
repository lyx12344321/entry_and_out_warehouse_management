from module.Record import Record
from module.RecordList import RecordList
from module.Menu import *
import utils
from enumeration.CheckType import CheckType
from enumeration.MenuName import MenuName
from exception.QuitException import QuitException
from exception.RecordTypeUndefined import RecordTypeUndefined

import datetime
import xlwings as xw
import configparser
import os

class Service:

    @staticmethod
    def creatRecord(recordList: RecordList):

        complete = False
        record = Record()
        record.setDefault()
        Menu.show(MenuName.RECORDTYPE)

        try:
            print('开始记录数据，部分数据可以选择默认值，可在默认配置信息.ini文件修改：')
            record.setType()
            record.setVarietyCoal()
            record.setPlateNumber()
            record.setGrossWeight()
            record.setTare()
            record.setPrimary()
            record.setEmptyTime()
            record.setExcessiveTime()
            record.setShippingUnit()
            record.setReceivingUnit()
            record.setWeigher()

            complete = True
        except QuitException as e:
            print('输入中断！')
        except Exception as e:
            print('未知异常!')

        # 计算净重
        record.calculateNetWeight()
        # 计算盈亏
        record.calculateProfitLoss()

        today = datetime.datetime.today()
        record.creatTime = today
        record.modifyTime = today

        uid = recordList.add(record)
        if complete:
            print('记录添加成功，记录uid为: ' + uid)
        else:
            print("已保存未完成的输入，记录uid为: " + uid)
         
    @staticmethod
    def updateRecord(recordList: RecordList):

        Menu.show(MenuName.UPDATE)

        uid = utils.inputChecker(CheckType.DATATYPE, str, '请输入要修改记录的uid：')
        print(uid)
        record = recordList.findByUid(uid)
        if record is None:
            print('uid不存在, 请重新输入，或退出修改界面进行查询。')
            return
        print('你要修改哪一个数据?')
        Menu.show(MenuName.RECORDINFO)
        try:
            while True:
                recordNumber = utils.inputChecker(CheckType.OPTIONTYPE, utils.rangeIntToString(range(1, 13)), '请输入要修改记录的序号：')
                print(f'你将操作的为：{Menu.menus[MenuName.RECORDINFO][recordNumber]}')
                record.methodMapping[recordNumber]()
        except QuitException:
            return
        except Exception as e:
            print(e)
            return
        
    @staticmethod
    def removeRecord(recordList: RecordList):
        Menu.show(MenuName.REMOVE)
        uid = utils.inputChecker(CheckType.DATATYPE, str, '请输入要删除记录的uid：')
        print(uid)
        record = recordList.findByUid(uid)
        if record is None:
            print('uid不存在, 请重新输入，或退出修改界面进行查询。')
            return
        isRemove = utils.inputChecker(CheckType.DATATYPE, str, '请确认是否删除（回车确认）')
        if (utils.strIsEmpty(isRemove)):
            recordList.removeById(uid)
            print('删除成功！')
        else:
            print('删除已取消！')

    @staticmethod
    def list(recordList: RecordList):
        if recordList.length() == 0:
            print('当前记录为空！')
            return
        print(recordList)
    @staticmethod
    def generateImage(recordList: RecordList, workBook: xw.Book):
        if recordList.length() == 0:
            print('当前记录为空！')
            return
        
        config = configparser.ConfigParser()
        config.read('./config.ini')
        # 创建输出文件夹
        outputFolder = config.get('other', 'imagesPath')
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        for record in recordList:
            try:
                image = utils.recordToImage(record, workBook)
            except RecordTypeUndefined as e:
                print(e)
                continue
            if image is None:
                continue

            filePath = os.path.join(outputFolder, f'{record.creatTime.strftime('%Y年%m月%d日%H时%M分%S秒')}.png')
            print(filePath)
            image.save(filePath)
            record.isGenerateImage = True
    
    def saveToExcel(recordList: RecordList, workBook: xw.Book):
        if recordList.length() == 0:
            print('当前记录为空！')
            return
        for record in recordList:
            currentRow = utils.getSheetLength(workBook, record.sheetName)

            workBook.sheets[record.sheetName].range(f'A{currentRow}').value = record.date
            workBook.sheets[record.sheetName].range(f'B{currentRow}').value = record.id
            workBook.sheets[record.sheetName].range(f'C{currentRow}').value = record.varietyCoal
            workBook.sheets[record.sheetName].range(f'D{currentRow}').value = record.plateNumber
            workBook.sheets[record.sheetName].range(f'E{currentRow}').value = record.grossWeight
            workBook.sheets[record.sheetName].range(f'F{currentRow}').value = record.tare
            workBook.sheets[record.sheetName].range(f'G{currentRow}').value = record.netWeight
            workBook.sheets[record.sheetName].range(f'H{currentRow}').value = record.primary
            workBook.sheets[record.sheetName].range(f'I{currentRow}').value = record.profitLoss
            workBook.sheets[record.sheetName].range(f'J{currentRow}').value = record.emptyTime
            workBook.sheets[record.sheetName].range(f'K{currentRow}').value = record.excessiveTime
            workBook.sheets[record.sheetName].range(f'L{currentRow}').value = record.shippingUnit
            workBook.sheets[record.sheetName].range(f'N{currentRow}').value = record.receivingUnit
            workBook.sheets[record.sheetName].range(f'M{currentRow}').value = record.weigher

            workBook.save()
