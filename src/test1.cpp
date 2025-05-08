#include <pybind11/pybind11.h>
namespace py = pybind11;

int dumbadd(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(module_name, m) {
    m.doc() = "Pybind python bindings";
    m.def("add", &dumbadd, "A function that adds two numbers");
}