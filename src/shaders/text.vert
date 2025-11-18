#version 330
in vec2 in_pos; // pixel coords
in vec2 in_uv;
uniform vec2 u_screen;
out vec2 v_uv;
void main() {
    vec2 ndc = (in_pos / u_screen) * 2.0 - 1.0;
    ndc.y = -ndc.y;
    gl_Position = vec4(ndc, 0.0, 1.0);
    v_uv = in_uv;
}
