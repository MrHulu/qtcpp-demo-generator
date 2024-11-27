import os
import sys
import re
import argparse


cmake_presets_content = """{
    "version": 3,
    "configurePresets": [
        {
            "name": "base",
            "hidden": true,
            "binaryDir": "${sourceDir}/build/${presetName}",
            "installDir": "${sourceDir}/install/${presetName}",
            "generator": "Ninja",
            "cacheVariables": {
                "CMAKE_INSTALL_PREFIX": "${sourceDir}//install/${presetName}",
                "CMAKE_C_COMPILER": "cl.exe",
                "CMAKE_CXX_COMPILER": "cl.exe"
            }
        },
        {
            "name": "debug-x64",
            "displayName": "Debug Build - x64",
            "description": "Debug build with debug (x64) symbols",
            "inherits": "base",
            "architecture":{
                "value": "x64",
                "strategy": "external"
            },
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug"
            }
        },
        {
            "name": "release-x64",
            "displayName": "Release Build - x64",
            "description": "Optimized build without debug (x64) symbols",
            "inherits": "debug-x64",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release"
            }
        },
        {
            "name": "relWithDebInfo-x64",
            "displayName": "Release with Debug Info - x64",
            "description": "Optimized build with limited debug (x64) symbols",
            "inherits": "debug-x64",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "RelWithDebInfo"
            }
        },
        {
            "name": "debug-x86",
            "displayName": "Debug Build - x86",
            "description": "Debug build with debug (x86) symbols",
            "inherits": "base",
            "architecture":{
                "value": "x86",
                "strategy": "external"
            },
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug"
            }
        },
        {
            "name": "release-x86",
            "displayName": "Release Build - x86",
            "description": "Optimized build without debug (x86) symbols",
            "inherits": "debug-x86",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release"
            }
        },
        {
            "name": "relWithDebInfo-x86",
            "displayName": "Release with Debug Info - x86",
            "description": "Optimized build with limited debug (x86) symbols",
            "inherits": "debug-x86",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "RelWithDebInfo"
            }
        }
    ],
    "buildPresets": [
        {
            "name": "debug-x64",
            "displayName": "Debug Build - x64",
            "configurePreset": "debug-x64",
            "configuration": "Debug"
        },
        {
            "name": "release-x64",
            "displayName": "Release Build - x64",
            "configurePreset": "release-x64",
            "configuration": "Release"
        },
        {
            "name": "relWithDebInfo-x64",
            "displayName": "Release with Debug Info - x64",
            "configurePreset": "relWithDebInfo-x64",
            "configuration": "RelWithDebInfo"
        },
        {
            "name": "debug-x86",
            "displayName": "Debug Build - x86",
            "configurePreset": "debug-x86",
            "configuration": "Debug"
        },
        {
            "name": "release-x86",
            "displayName": "Release Build - x86",
            "configurePreset": "release-x86",
            "configuration": "Release"
        },
        {
            "name": "relWithDebInfo-x86",
            "displayName": "Release with Debug Info - x86",
            "configurePreset": "relWithDebInfo-x86",
            "configuration": "RelWithDebInfo"
        }
    ]
}
"""

cmake_lists_content = """cmake_minimum_required(VERSION 3.16)
project(${PROJECT_NAME} VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 Qt 包
find_package(Qt5 REQUIRED COMPONENTS Core)
# 如果需要其他 Qt 模块，可以在这里添加，例如：
# find_package(Qt5 REQUIRED COMPONENTS Core Gui Widgets Network)

# 定义构建信息变量
function(get_target_architecture target_architecture)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(${target_architecture} "x64" PARENT_SCOPE)
    else()
        set(${target_architecture} "x86" PARENT_SCOPE)
    endif()
endfunction()
get_target_architecture(ARCHITECTURE)
add_compile_definitions(
    BUILD_TYPE="${CMAKE_BUILD_TYPE}"
    CMAKE_GENERATOR="${CMAKE_GENERATOR}"   
    ARCHITECTURE="${ARCHITECTURE}"
)

# 添加源文件
add_executable(${PROJECT_NAME}
    main.cpp
    test.cpp
    test.h
)

# 启用 Qt MOC 自动处理
set_target_properties(${PROJECT_NAME} PROPERTIES
    AUTOMOC ON
    AUTORCC ON
    AUTOUIC ON
)

# 链接 Qt 库
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt5::Core
)

"""

main_content = """#include <QCoreApplication>
#include "test.h"

int main(int argc, char *argv[]) {
    QCoreApplication a(argc, argv);

    Test test;
    test.printMessage();
    return a.exec();
}
"""

test_h_content = """#ifndef TEST_H
#define TEST_H

#include <QObject>
#include <QDebug>

class Test : public QObject {
    Q_OBJECT
public:
    explicit Test(QObject *parent = nullptr);
    void printMessage();
};

#endif // TEST_H
"""

test_cpp_content = """#include "test.h"

Test::Test(QObject *parent) : QObject(parent) {}

void Test::printMessage() {
    qDebug() << "Hello from Test class!";
}
"""

def create_file(file_path, content):
    """创建文件并写入内容"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_qt_project(project_name, project_path):
    """生成一个Qt/C++空项目"""
    try:
        # 创建完整的项目路径
        full_project_path = os.path.join(project_path, project_name)
        os.makedirs(full_project_path, exist_ok=True)

        # 替换 CMakeLists.txt 中的项目名称
        current_cmake_lists = cmake_lists_content.replace("${PROJECT_NAME}", project_name)

        # 创建 CMakePresets.json
        cmake_presets_path = os.path.join(full_project_path, "CMakePresets.json")
        create_file(cmake_presets_path, cmake_presets_content)

        # 创建 CMakeLists.txt
        cmake_lists_path = os.path.join(full_project_path, "CMakeLists.txt")
        create_file(cmake_lists_path, current_cmake_lists)

        # 创建其他文件
        main_cpp_path = os.path.join(full_project_path, "main.cpp")
        create_file(main_cpp_path, main_content)

        test_h_path = os.path.join(full_project_path, "test.h")
        create_file(test_h_path, test_h_content)

        test_cpp_path = os.path.join(full_project_path, "test.cpp")
        create_file(test_cpp_path, test_cpp_content)

        print(f"项目 '{project_name}' 已成功生成在 '{full_project_path}'。")
        print("请确保您的系统上已安装 Qt5 并正确设置了环境变量。")
        
    except Exception as e:
        print(f"创建项目时发生错误: {str(e)}")

def is_valid_project_name(name):
    """
    检查项目名称是否有效
    - 只允许字母、数字、下划线
    - 不能以数字开头
    - 不能是空字符串
    """
    if not name:
        return False
    # 检查是否符合C++项目命名规范
    pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    return bool(pattern.match(name))

# 使用示例
if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='创建Qt/C++项目')
    parser.add_argument('--name', type=str, help='项目名称', default='QtCppDemo')
    parser.add_argument('--path', type=str, help='项目路径', default=os.getcwd())
    
    # 解析命令行参数
    args = parser.parse_args()
    project_name = args.name
    project_path = os.path.abspath(args.path)  # 转换为绝对路径

    # 验证项目名称
    if not is_valid_project_name(project_name):
        print(f"错误: '{project_name}' 不是有效的项目名称。")
        print("项目名称必须:")
        print("- 以字母或下划线开头")
        print("- 只包含字母、数字和下划线")
        print("- 不能为空")
        sys.exit(1)

    # 验证项目路径
    if not os.path.exists(project_path):
        response = input(f"路径 '{project_path}' 不存在。是否创建？(y/N): ")
        if response.lower() == 'y':
            try:
                os.makedirs(project_path)
            except Exception as e:
                print(f"创建路径失败: {str(e)}")
                sys.exit(1)
        else:
            print("操作已取消。")
            sys.exit(0)

    # 检查项目目录是否已存在
    full_project_path = os.path.join(project_path, project_name)
    if os.path.exists(full_project_path):
        response = input(f"项目目录 '{full_project_path}' 已存在。是否覆盖？(y/N): ")
        if response.lower() != 'y':
            print("操作已取消。")
            sys.exit(0)

    # 创建项目
    create_qt_project(project_name, project_path)