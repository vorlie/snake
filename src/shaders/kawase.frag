#version 330
in vec2 v_uv;
uniform sampler2D tex;
uniform float offset;
uniform vec2 texel; // 1/width, 1/height
out vec4 f_color;
void main() {
    vec3 sum = vec3(0.0);
    // center weight
    sum += texture(tex, v_uv).rgb * 0.25;
    // four corners
    sum += texture(tex, v_uv + vec2( offset,  offset) * texel).rgb * 0.1875;
    sum += texture(tex, v_uv + vec2( offset, -offset) * texel).rgb * 0.1875;
    sum += texture(tex, v_uv + vec2(-offset,  offset) * texel).rgb * 0.1875;
    sum += texture(tex, v_uv + vec2(-offset, -offset) * texel).rgb * 0.1875;
    f_color = vec4(sum, 1.0);
}