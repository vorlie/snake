#version 330

out vec4 f_color;
uniform vec4 u_color;

void main() {
    // simple solid color segments
    f_color = u_color;
}