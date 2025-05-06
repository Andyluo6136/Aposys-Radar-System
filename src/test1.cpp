#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(module_name, m) {
    m.doc() = "Pybind python bindings";
    m.def("add", &add, "A function that adds two numbers");
}