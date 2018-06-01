cmake_minimum_required(VERSION 2.8)

project(test)


add_definitions(-std=c++11)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS} )

add_library("opencv_dep_cudart" UNKNOWN IMPORTED)
set_target_properties("opencv_dep_cudart" PROPERTIES IMPORTED_LOCATION /usr/local/cuda/lib64/libcudart.so)   


add_executable(test 
    ../test.cpp
)

target_link_libraries(test ${OpenCV_LIBS})