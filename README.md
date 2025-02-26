# 🚀 Qt/C++ 项目生成器

一个简单但强大的 Qt/C++ 项目生成器，让您的项目创建变得轻松愉快！

C++的项目有时候创建比较麻烦，这个小脚本仅需要点击几下鼠标即可生成一个C++项目。

![image](https://github.com/user-attachments/assets/11a2929d-989d-4d73-adc7-4b154335476c)

## 🎯 功能特点

- 一键生成标准的 Qt/C++ 项目结构
- 支持 CMake 构建系统
- 包含预配置的 CMakePresets.json
- 自动生成示例代码
- 支持 x86 和 x64 架构
- 支持 Debug 和 Release 模式

## 🛠️ 使用前提

- Python 3.6+
- Qt5 SDK
- CMake 3.16+
- 编译器（MSVC）

## 📦 快速开始

1. 使用默认配置创建项目：
```bash
python create_qtcpp_project.py
```

2. 指定项目名称：
```bash
python create_qtcpp_project.py --name MyAwesomeProject
```

3. 指定项目路径：
```bash
python create_qtcpp_project.py --path D:\Projects
```

4. 同时指定名称和路径：
```bash
python create_qtcpp_project.py --name MyAwesomeProject --path D:\Projects 
```


## 📁 项目结构

生成的项目结构如下：

```
MyAwesomeProject/
├── CMakeLists.txt
├── CMakePresets.json
├── main.cpp
├── test.h
└── test.cpp
```

## 🎨 自定义选项

- `--name`: 项目名称（默认：QtCppDemo）
  - 必须以字母或下划线开头
  - 只能包含字母、数字和下划线
- `--path`: 项目路径（默认：当前目录）

## 🚗 构建说明

1. 打开项目目录
2. 选择合适的构建预设：
   - debug-x64：调试版本（64位）
   - release-x64：发布版本（64位）
   - debug-x86：调试版本（32位）
   - release-x86：发布版本（32位）

## ⌛未来改进
这个脚本还有很大的改进空间。以下是一些可能的改进方向：

- 支持快速创建出带有Qml界面的Qt项目
- 支持快速创建出带有QWidget界面的Qt项目
- ...

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！让我们一起把这个工具变得更好！

## 📝 许可证

MIT License - 随意使用，但请保留署名！

## 🧡 致谢

如果这个项目对你有帮助，请给个Star支持一下！
