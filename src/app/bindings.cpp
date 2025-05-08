#include <pybind11/pybind11.h>

namespace py = pybind11;

// A simple example function
int stupidadd(int a, int b) {
    return a + b;
}

// This is the Python module definition
PYBIND11_MODULE(module_name11, m) {
    m.doc() = "Example pybind11 module named module_name";
    m.def("add", &stupidadd, "Add two integers");
}
