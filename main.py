from service.Service import Service
import utils
from module.RecordList import RecordList
from module.Menu import Menu
from enumeration.MenuName import MenuName
from enumeration.CheckType import CheckType
from exception.QuitException import QuitException
import os
import xlwings as xw


def main(workBook: xw.Book, recordList: RecordList):
    print("已经入本系统")
    
    while True:
        Menu.show(MenuName.MAIN)
        switch = utils.inputChecker(optional=CheckType.OPTIONTYPE, optionalArgs=utils.rangeIntToString(range(1, 7)), instructions='请输入选项：')
        print()

        if switch == '1':
            Service.creatRecord(recordList)

        elif switch == '2':
            Service.list(recordList)

        elif switch == '3':
            Service.updateRecord(recordList)

        elif switch == '4':
            Service.removeRecord(recordList)

        elif switch == '5':
            Service.generateImage(recordList, workBook)
            Service.saveToExcel(recordList, workBook)

        elif switch == '6':
            raise Warning("系统退出")


if __name__ == '__main__':

    # 创建excel应用程序
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False

    #  打开excel文件
    filePath = './出入库明细.xlsx'
    workBook = app.books.open(filePath)
    print('已经打开工作簿：' + filePath)
    print('请勿尝试修改此文件，请关闭此系统后尝试修改')
    print()

    recordList = RecordList()
    while True:
        try:
            main(workBook, recordList)
        except QuitException as e:
            os.system("cls")
        except Warning as w:
            print('系统退出')
            workBook.close()
            app.quit()
            exit()
        except ValueError as e:
            workBook.close()
            app.quit()
            print(e)
        except Exception as e:
            workBook.close()
            app.quit()
            e.with_traceback()
