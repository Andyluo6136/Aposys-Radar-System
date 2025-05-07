cmake_minimum_required(VERSION 3.10)
project(Pybind_project)

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
list(FILTER LIB_SRC EXCLUDE REGEX ".*/test1\\.cpp$")

# ------------------- Building the executable ------------------- #
if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/app/bindings.cpp")
    message(FATAL_ERROR "BUILDING EXECUTABLE but src/app/bindings.cpp not found")
endif()



# ------------------- Pybind11 Module ------------------- #
pybind11_add_module(mr76_radar MODULE MR76_Radar/src/mr76_radar.cpp)
target_sources(mr76_radar PRIVATE ${LIB_SRC})
target_link_libraries(mr76_radar PRIVATE ${COMMON_LIBRARIES})
target_include_directories(mr76_radar PRIVATE ${COMMON_INCLUDES})
