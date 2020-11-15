from openpyxl import load_workbook


class HandleExcel(object):

    def __init__(self, excel_path, sheet):
        self.web = load_workbook(excel_path)
        self.sh = self.web[sheet]

    def _read_fist_line(self):
        self._get_rows_obj()
        title_list = []
        for item in self.all_rows[0]:
            title_list.append(item.value)
        return title_list

        # 获取所有的数据，与第一行数据拼接，按key-value的形式。

    def read_all_data(self):
        title = self._read_fist_line()
        cases = []
        for item in self.all_rows[1:]:  # 获取每一行对象
            value = []  # 存放每一行数据
            for cell in item:
                value.append(cell.value)  # 将每一行单元格里数据放到列表中
            case = dict(zip(title, value))  # 将每一行数据和表头数据合并成一条字典格式的用例
            cases.append(case)  # 将每一条用例放在整个用例列表中
        return cases

    # 获取所有的行对象
    def _get_rows_obj(self):
        self.all_rows = list(self.sh.rows)


if __name__ == '__main__':
    import os
    from common.handle_path import datadir

    excel_path = os.path.join(datadir, "api_cases.xlsx")
    he = HandleExcel(excel_path, "register")
    cases = he.read_all_data()
    print(cases)
