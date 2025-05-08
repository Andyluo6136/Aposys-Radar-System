cmake_minimum_required(VERSION 3.10)
project(Aposys-Radar-System)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Allow specifying build type at compile-time
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Complier Flags
add_compile_options(
    "$<$<CONFIG:Debug>:-O0;-g;-Wno-unused-variable;-Wno-unused-parameter>"
    "$<$<CONFIG:Release>:-O3;-DNDEBUG>"
)

# dependencies
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

# Debug print
message(STATUS "Python include dirs: ${Python3_INCLUDE_DIRS}")
# ------------------- Include Header and Source Directories ------------------- #
set(COMMON_INCLUDES
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${Python3_INCLUDE_DIRS} 
)
# Collect all header files
file(GLOB_RECURSE HEADER_FILES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/include/*.hpp)
find_package(TBB REQUIRED)
# Libraries
set(COMMON_LIBRARIES
    TBB::tbb
    yaml-cpp
)

# Collect all source files
file(GLOB_RECURSE SRC_FILES CONFIGURE_DEPENDS src/*.cpp)

# Anything that ends in /main.cpp is **not** part of the reusable core
set(LIB_SRC ${SRC_FILES})
list(FILTER LIB_SRC EXCLUDE REGEX ".*/mr76_radar\\.cpp$")

# ------------------- Building the executable ------------------- #
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/MR76_Radar/src/mr76_radar.cpp")
    message(FATAL_ERROR "BUILDING EXECUTABLE but MR76_Radar/src/mr76_radar.cpp not found")
endif()



# ------------------- Pybind11 Module ------------------- #
pybind11_add_module(radar_modules MODULE MR76_Radar/src/mr76_radar.cpp)
target_sources(radar_modules PRIVATE ${LIB_SRC})
target_link_libraries(radar_modules PRIVATE ${COMMON_LIBRARIES})
target_include_directories(radar_modules PRIVATE ${COMMON_INCLUDES})

