#include "mr76_radar.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
namespace py = pybind11;

// MR76::MR76(){
//     _total_objects = 0;
//     _cycles = 0;
//     object_counter = 0;
// }

MR76::MR76() {}


void MR76::parse_data(int id, int len, unsigned int int1, unsigned int int2, unsigned int int3, unsigned int int4, unsigned int int5, unsigned int int6, unsigned int int7,unsigned int int8){

    unsigned char a = static_cast<unsigned char>(int1); // char1 will be 65 ('A')
    unsigned char b = static_cast<unsigned char>(int2); // char2 will be 44 (300 % 256)
    unsigned char c = static_cast<unsigned char>(int3); // char3 will be 246 (-10 + 256)
    unsigned char d = static_cast<unsigned char>(int4); // char1 will be 65 ('A')
    unsigned char e = static_cast<unsigned char>(int5); // char2 will be 44 (300 % 256)
    unsigned char f = static_cast<unsigned char>(int6); // char3 will be 246 (-10 + 256)
    unsigned char g = static_cast<unsigned char>(int7); // char1 will be 65 ('A')
    unsigned char h = static_cast<unsigned char>(int8); // char2 will be 44 (300 % 256)

    
    
    if ((id & 0x60B) == 0x60B && len == 8){


        int16_t data_stream[8]; // stream of extracted bits defining data
      
        data_stream[0] = a;                                                            // object id
        data_stream[1] = int16_t(((b << 8) | (c & 0xF8)) >> 3);                 // distance long
        data_stream[2] = int16_t((c & 0x07) << 8 | d);                          // distance lat
        data_stream[3] = int16_t(((e << 8) | (f & 0xC0)) >> 6);                 // Vrelative long
        data_stream[4] = int16_t(((((f & 0x3F) << 8) | (g & 0xE0))) >> 5);      // Vrelative lat
        data_stream[5] = int16_t((g & 0x18) >> 3);                                     // Object class
        data_stream[6] = int16_t(g & 0x07);                                            // Object dynamic prop
        data_stream[7] = h;

        _object_data.id = int(data_stream[0])+1;
        _object_data.distance_long= float(data_stream[1]*0.2 - 500);
        _object_data.distance_lat = float(data_stream[2]*0.2 - 204.2);
        _object_data.velocity_long = float(data_stream[3]*0.25 - 128.0);
        _object_data.velocity_lat = float(data_stream[4]*0.25 - 64.0);
        _object_data.obj_section = int(data_stream[5]);
        _object_data.obj_state = int(data_stream[6]);
        _object_data.rcs = float(data_stream[7]*0.5 - 64.0);
        _object[object_counter] = _object_data;
        object_counter ++;

        std::cout<<static_cast<int>(_object_data.distance_long) <<std::endl;


    }

    else if ((id & 0x60A) == 0x60A && len == 8){

        update_data();
        object_counter = 0;
        _total_objects = a;
        _cycles = int16_t((b << 8 )| (c));
    }
}

void MR76::update_data(){
    is_object_complete = 0;
    if(object_counter == _total_objects) is_object_complete = 1;
    is_ready = is_object_complete;
    object_detected = object_counter;
    for (int iter = 0; iter < object_counter; iter++){
        object[iter]=_object[iter];
    }
    this->total_objects = _total_objects;
    this->cycles = _cycles;

}
void MR76::configure(unsigned long int *id, unsigned char _buffer[8] ,int previous_id, int max_distance, int sensor_id, int output_type, int radar_power, int sort_index){
    int set_distance = 0;
    int set_id = 0;
    int set_power = 0;
    int set_output = 0;
    int set_quality = 0;
    int set_ext = 0;
    int set_sort = 0;
    int set_nvm = 1;
    if (max_distance != 0) set_distance = 1;
    if (sensor_id != 0) set_id = 1;
    if (output_type != 0) set_output = 1;
    if (radar_power != 0) set_power = 1;
    if (sort_index != 0) set_sort = 1;
    *id = 0x200;
    _buffer[0] = (
        set_distance |
        set_id << 1 |
        set_power << 2 |
        set_output << 3 |
        set_quality << 4 |
        set_ext << 5 |
        set_sort << 6|
        set_nvm << 7 
        );

    _buffer[1] = (max_distance & 0x1FC) >> 2;
    _buffer[2] = (max_distance & 0x3) << 6;
    _buffer[4] = (radar_power << 5) | (output_type << 3) | (sensor_id);
    _buffer[5] = (0x01 << 7) | (sort_index << 4);
}

int MR76::isready(){
    if (is_ready != 2 and cycles%(skip_cycle + 1) == 0){
        is_ready = 2;
        return 1;
    }
    else {
        return 0;
    }
}




PYBIND11_MODULE(radar_modules, m) {
    // Bind the nested struct first
    py::class_<MR76::mr76_data>(m, "mr76_data")
        .def(py::init<>())
        .def_readonly("id", &MR76::mr76_data::id)
        .def_readonly("distance_long", &MR76::mr76_data::distance_long)
        .def_readonly("distance_lat", &MR76::mr76_data::distance_lat)
        .def_readonly("velocity_long", &MR76::mr76_data::velocity_long)
        .def_readonly("velocity_lat", &MR76::mr76_data::velocity_lat)
        .def_readonly("obj_section", &MR76::mr76_data::obj_section)
        .def_readonly("obj_state", &MR76::mr76_data::obj_state)
        .def_readonly("rcs", &MR76::mr76_data::rcs);
    
    // Then bind the main class
    py::class_<MR76>(m, "MR76")
        .def(py::init<>())
        .def("parse_data", &MR76::parse_data, "parse_data")
        .def("configure", &MR76::configure, "configure")
        .def("isready", &MR76::isready, "isready")
        .def_readwrite("skip_cycle", &MR76::skip_cycle)
        .def_readwrite("total_objects", &MR76::total_objects)
        .def_readwrite("object_detected", &MR76::object_detected)
        .def_readwrite("cycles", &MR76::cycles)
        .def_readwrite("is_object_complete", &MR76::is_object_complete)
        .def_readwrite("object", &MR76::object);  // Make sure name matches variable
}
