from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox
from assets.components.calcBMI import Ui_CalcBMI
import sys


class CalcBMI(QMainWindow, Ui_CalcBMI):
    def __init__(self):
        super(CalcBMI, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Расчет ИМТ")

        self.en = {
            self.header: '<html><head/><body><p>'
            '<span style=" font-size:20pt; font-weight:600;">'
            'Body mass index calculation</span></p></body></html>',
            self.reset_btn: "Reset",
            self.lang_label: "Language",
            self.chooseLang_box: ["Russian", "English"],
            self.weight_label: '<html><head/><body><p>'
            '<span style=" font-size:14pt;">'
            'Weight in kilograms</span></p></body></html>',
            self.kg_label: '<html><head/><body><p>'
            '<span style=" font-size:12pt;">'
            'kg</span></p></body></html>',
            self.growth_label: '<html><head/><body><p>'
            '<span style=" font-size:14pt;">'
            'Height in centimeters</span></p></body></html>',
            self.cm_label: '<html><head/><body><p>'
            '<span style=" font-size:12pt;">'
            'cm</span></p></body></html>',
            self.calc_btn: "Calculate",
            self.yourBMI_label: '<html><head/><body>'
            '<p align="center"><span style=" font-size:18pt;">'
            'Your body mass index:</span></p></body></html>',
            "phrases": [
                "pronounced body weight deficiency",
                "insufficient (deficiency) body weight",
                "standard",
                "overweight (pre-obesity)",
                "obesity of the 1st degree",
                "obesity of the 2nd degree",
                "obesity of the 3rd degree",
                "BMI calculation"
            ]
        }

        self.ru = {
            self.header: '<html><head/><body><p>'
            '<span style=" font-size:20pt; font-weight:600;">'
            'Расчет индекса массы тела</span></p></body></html>',
            self.reset_btn: "Сброс",
            self.lang_label: "Язык",
            self.chooseLang_box: ["Русский", "Английский"],
            self.weight_label: '<html><head/><body><p>'
            '<span style=" font-size:14pt;">'
            'Вес в килограммах</span></p></body></html>',
            self.kg_label: '<html><head/><body><p>'
            '<span style=" font-size:12pt;">'
            'кг</span></p></body></html>',
            self.growth_label: '<html><head/><body><p>'
            '<span style=" font-size:14pt;">'
            'Рост в сантиметрах</span></p></body></html>',
            self.cm_label: '<html><head/><body><p>'
            '<span style=" font-size:12pt;">'
            'см</span></p></body></html>',
            self.calc_btn: "Рассчитать",
            self.yourBMI_label: '<html><head/><body>'
            '<p align="center"><span style=" font-size:18pt;">'
            'Ваш индекс массы тела:</span></p></body></html>',
            "phrases": [
                "выраженный дефицит массы тела",
                "недостаточная (дефицит) масса тела",
                "норма",
                "избыточная масса тела (предожирение)",
                "ожирение 1 степени",
                "ожирение 2 степени",
                "ожирение 3 степени",
                "Расчет ИМТ"
            ]
        }

        self.cur_lang = self.ru
        # первое значение - последний полученный ИМТ
        # второе значение - индекс фразы после тире
        # нужен для более упрощенного перевода фразы
        self.cur_bmi = [-1, 0]
        self.translate()

        self.calc_btn.clicked.connect(self.calc_bmi)
        self.reset_btn.clicked.connect(self.reset)
        self.chooseLang_box.currentTextChanged.connect(self.translate)

    def calc_bmi(self):
        weight = float(self.weight_input.text())
        growth = (float(self.growth_input.text()) / 100) ** 2

        try:
            result = round(weight / growth, 2)
            self.cur_bmi[0] = result

        except ZeroDivisionError:
            self.cur_bmi = [-1, "-"]

            self.result_label.setText(
                '<html><head/><body><p align="center">'
                '<span style=" font-size:12pt;">-'
                '</span></p></body></html>')

            return

        message = f"{result} - "

        if result < 16:
            message += self.cur_lang["phrases"][0]
            self.cur_bmi[1] = 0

        elif 16 < result <= 18.5:
            message += self.cur_lang["phrases"][1]
            self.cur_bmi[1] = 1

        elif 18.5 < result <= 25:
            message += self.cur_lang["phrases"][2]
            self.cur_bmi[1] = 2

        elif 25 < result <= 30:
            message += self.cur_lang["phrases"][3]
            self.cur_bmi[1] = 3

        elif 30 < result <= 35:
            message += self.cur_lang["phrases"][4]
            self.cur_bmi[1] = 4

        elif 35 < result <= 40:
            message += self.cur_lang["phrases"][5]
            self.cur_bmi[1] = 5

        elif result > 40:
            message += self.cur_lang["phrases"][6]
            self.cur_bmi[1] = 6

        self.result_label.setText(
            '<html><head/><body><p align="center">'
            f'<span style=" font-size:12pt;">{message}'
            '</span></p></body></html>')

    def reset(self):
        self.cur_bmi = [-1, 0]

        self.result_label.setText(
            '<html><head/><body><p align="center">'
            '<span style=" font-size:12pt;">-'
            '</span></p></body></html>')
        self.weight_input.setValue(0)
        self.growth_input.setValue(0)

    def translate(self):
        if self.chooseLang_box.currentText() in ["Английский", "English"]:
            self.cur_lang = self.en

        else:
            self.cur_lang = self.ru

        self.setWindowTitle(self.cur_lang["phrases"][7])

        if self.cur_bmi[0] != -1:
            self.result_label.setText(
                '<html><head/><body><p align="center">'
                '<span style=" font-size:12pt;">'
                f'{self.cur_bmi[0]} - {self.cur_lang["phrases"][self.cur_bmi[1]]}'
                '</span></p></body></html>'
            )

        for key, value in self.cur_lang.items():
            if isinstance(key, QComboBox):
                for index, elem in enumerate(value):
                    key.setItemText(index, elem)

            elif key == "phrases":
                break

            else:
                key.setText(value)


def exception_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalcBMI()
    ex.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec_())
