import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QRadioButton, QButtonGroup,
    QLabel, QPushButton, QFrame
)


class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.count=0

    def init_ui(self):
        self.setWindowTitle('User Input and Output Example')
        self.setGeometry(100, 100, 600, 400)

        # 主布局：水平分割，左为输入，右为输出
        main_layout = QHBoxLayout(self)

        # 左侧:输入区域
        input_frame = QFrame(self)  
        input_frame.setFixedWidth(200)  
        input_layout = QVBoxLayout(input_frame)

        # 输入组件 1：文本框
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText('Enter text...')
        input_layout.addWidget(self.text_input)

        # 输入组件 2：下拉框
        self.dropdown = QComboBox()
        self.dropdown.addItems(['Option 1', 'Option 2', 'Option 3'])
        input_layout.addWidget(self.dropdown)

        # 输入组件 3：单选按钮
        self.radio_group = QButtonGroup(self)
        self.radio_buttons = []
        for i, label in enumerate(['Choice A', 'Choice B', 'Choice C']):
            radio_button = QRadioButton(label)
            self.radio_group.addButton(radio_button, i)
            input_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        # submit按钮
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.update_outputs)
        input_layout.addWidget(self.submit_button)

        # 右侧: 输出
        output_frame = QFrame(self)  
        output_frame.setFixedWidth(300)  
        output_layout = QVBoxLayout(output_frame)

        # 输出组件 1：文本显示
        self.text_output = QLabel('Output 1: ')
        output_layout.addWidget(self.text_output)

        # 输出组件 2：下拉框选项显示
        self.dropdown_output = QLabel('Output 2: ')
        output_layout.addWidget(self.dropdown_output)

        # 输出组件 3：单选选项显示
        self.radio_output = QLabel('Output 3: ')
        output_layout.addWidget(self.radio_output)

        # 输出组件 4：最下方的指定字符
        self.final_output = QLabel('') 
        output_layout.addWidget(self.final_output)

        # 将输入和输出布局加入主布局
        main_layout.addWidget(input_frame)
        main_layout.addWidget(output_frame)

        # 设置主布局
        self.setLayout(main_layout)

    def update_outputs(self):
        # 更新文本框
        self.count+=1
        text = self.text_input.text()
        self.text_output.setText(f'Output 1: {text}')

        # 更新下拉框
        dropdown_value = self.dropdown.currentText()
        self.dropdown_output.setText(f'Output 2: {dropdown_value}')

        # 更新单选按钮
        selected_radio = self.radio_group.checkedButton()
        if selected_radio:
            radio_value = selected_radio.text()
            self.radio_output.setText(f'Output 3: {radio_value}')
        else:
            self.radio_output.setText('Radio Output: None')

        self.final_output.setText(f'戳戳最喜欢的姐姐{self.count}次')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec_())
