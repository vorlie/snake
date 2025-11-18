#version 330
in vec2 v_uv;
uniform sampler2D tex;
uniform float threshold;
out vec4 f_color;
void main() {
    vec3 c = texture(tex, v_uv).rgb;
    float lum = max(max(c.r, c.g), c.b);
    float mask = step(threshold, lum);
    f_color = vec4(c * mask, 1.0);
}